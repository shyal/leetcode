//! Derive a candidate stub from a validated solution.
//!
//! The prepare cache stores the full solution that passed its own asserts;
//! the stub written to `current.py` is derived from it here. The transform
//! is line-based and driven by the AST (ruff's parser), so the docstring,
//! spacing and comments of the original survive byte-for-byte - only method
//! bodies and asserts are touched.
//!
//! Ported from utils/kg/stub_utils.py on 2026-09-14. Line numbers are
//! 1-based and columns are byte offsets, as Python's `ast` reports them, so
//! the two read side by side.

use std::collections::{BTreeMap, HashSet, VecDeque};

use ruff_python_ast::statement_visitor::{walk_stmt, StatementVisitor};
use ruff_python_ast::visitor::source_order::{SourceOrderVisitor, TraversalSignal};
use ruff_python_ast::{AnyNodeRef, Expr, ExprCall, Stmt, StmtClassDef, StmtFunctionDef};
use ruff_python_parser::parse_module;
use ruff_text_size::{Ranged, TextRange};

/// Injected by sitecustomize; if a generator redefines one anyway, leave it
/// working rather than gutting it and breaking the file.
pub const HELPER_CLASSES: [&str; 4] = ["TreeNode", "ListNode", "GraphNode", "Node"];

/// Modules whose contents sitecustomize already injects; importing from
/// them is always redundant in a solve file.
pub const INJECTED_MODULES: [&str; 8] = [
    "typing",
    "collections",
    "functools",
    "itertools",
    "math",
    "heapq",
    "bisect",
    "string",
];

/// builder -> the variable name used when the callee's parameter name is unknown
const BUILDERS: [(&str, &str); 2] = [("build_tree", "root"), ("build_linked_list", "head")];

fn is_helper(name: &str) -> bool {
    HELPER_CLASSES.contains(&name)
}

fn is_injected(module: &str) -> bool {
    INJECTED_MODULES.contains(&module)
}

/// Python's `str.splitlines()` for the newlines a solve file has.
pub fn splitlines(code: &str) -> Vec<String> {
    let mut lines: Vec<String> = code.split('\n').map(str::to_string).collect();
    if lines.last().is_some_and(|l| l.is_empty()) {
        lines.pop();
    }
    lines
}

/// Line and column lookup for the byte offsets ruff reports.
struct Lines {
    starts: Vec<usize>,
}

impl Lines {
    fn new(code: &str) -> Lines {
        let mut starts = vec![0];
        for (i, b) in code.bytes().enumerate() {
            if b == b'\n' {
                starts.push(i + 1);
            }
        }
        Lines { starts }
    }

    /// 1-based line of a byte offset (ast.lineno).
    fn line(&self, off: usize) -> usize {
        self.starts.partition_point(|&s| s <= off)
    }

    /// Byte column of an offset on its line (ast.col_offset).
    fn col(&self, off: usize) -> usize {
        off - self.starts[self.line(off) - 1]
    }

    fn start_line(&self, r: TextRange) -> usize {
        self.line(r.start().to_usize())
    }

    /// ast.end_lineno: the line the node's last character is on.
    fn end_line(&self, r: TextRange) -> usize {
        self.line(r.end().to_usize())
    }
}

/// ast.lineno of a def or class: the keyword's line, decorators excluded
/// (ruff's range starts at the first decorator).
fn def_line(lines: &Lines, name: &ruff_python_ast::Identifier) -> usize {
    lines.start_line(name.range())
}

fn indent_of(line: &str) -> &str {
    &line[..line.len() - line.trim_start().len()]
}

fn is_docstring(stmt: &Stmt) -> bool {
    matches!(stmt, Stmt::Expr(e) if matches!(&*e.value, Expr::StringLiteral(_)))
}

fn as_call(stmt: &Stmt) -> Option<&ExprCall> {
    match stmt {
        Stmt::Expr(e) => match &*e.value {
            Expr::Call(c) => Some(c),
            _ => None,
        },
        _ => None,
    }
}

fn name_id(e: &Expr) -> Option<&str> {
    match e {
        Expr::Name(n) => Some(n.id.as_str()),
        _ => None,
    }
}

/// The fallback variable name when `node` calls a builder, else None.
fn builder_default(node: &Expr) -> Option<&'static str> {
    let Expr::Call(c) = node else { return None };
    let id = name_id(&c.func)?;
    BUILDERS.iter().find(|(b, _)| *b == id).map(|(_, d)| *d)
}

fn is_builder_call(node: &Expr) -> bool {
    builder_default(node).is_some()
}

/// `print(x)` / `draw_tree(x)` of a plain name: shows a value, tests nothing.
fn is_bare_print(stmt: &Stmt) -> bool {
    let Some(call) = as_call(stmt) else {
        return false;
    };
    if name_id(&call.func).is_none() || call.arguments.args.len() != 1 {
        return false;
    }
    name_id(&call.arguments.args[0]).is_some() && call.arguments.keywords.is_empty()
}

/// The first-example call: a print or draw that is not a bare `print(x)`.
pub fn is_demo(stmt: &Stmt) -> bool {
    let Some(call) = as_call(stmt) else {
        return false;
    };
    let name = match &*call.func {
        Expr::Name(n) => n.id.as_str(),
        Expr::Attribute(a) => a.attr.as_str(),
        _ => "",
    };
    let shows = matches!(name, "print" | "tabulate" | "rich_print") || name.starts_with("draw_");
    shows && !is_bare_print(stmt)
}

/// Parameter names of the method or constructor `call` invokes, minus self.
/// None when the callee is not defined in the file.
fn param_names(body: &[Stmt], call: &ExprCall) -> Option<Vec<String>> {
    for stmt in body {
        let Stmt::ClassDef(cls) = stmt else { continue };
        for member in &cls.body {
            let Stmt::FunctionDef(f) = member else {
                continue;
            };
            let hit = match &*call.func {
                Expr::Attribute(a) => f.name.as_str() == a.attr.as_str(),
                Expr::Name(n) => {
                    n.id.as_str() == cls.name.as_str() && f.name.as_str() == "__init__"
                }
                _ => false,
            };
            if hit {
                return Some(
                    f.parameters
                        .args
                        .iter()
                        .skip(1)
                        .map(|p| p.parameter.name.to_string())
                        .collect(),
                );
            }
        }
    }
    None
}

/// The direct children of a node, in Python's `iter_child_nodes` order: a
/// call's positional arguments before its keywords (ruff interleaves them
/// by position under one Arguments node).
struct Children<'a>(Vec<AnyNodeRef<'a>>);

impl<'a> SourceOrderVisitor<'a> for Children<'a> {
    fn enter_node(&mut self, node: AnyNodeRef<'a>) -> TraversalSignal {
        if let AnyNodeRef::Arguments(a) = node {
            self.0.extend(a.args.iter().map(AnyNodeRef::from));
            self.0.extend(a.keywords.iter().map(AnyNodeRef::from));
        } else {
            self.0.push(node);
        }
        TraversalSignal::Skip
    }
}

/// ast.walk over a statement: breadth-first, the calls in the order Python
/// yields them.
fn walk_calls(stmt: &Stmt) -> Vec<&ExprCall> {
    let mut out = Vec::new();
    let mut queue: VecDeque<AnyNodeRef> = VecDeque::from([AnyNodeRef::from(stmt)]);
    while let Some(node) = queue.pop_front() {
        if let AnyNodeRef::ExprCall(c) = node {
            out.push(c);
        }
        let mut kids = Children(Vec::new());
        node.visit_source_order(&mut kids);
        queue.extend(kids.0);
    }
    out
}

/// One statement's rewrite: the builder calls to hoist, each with the name
/// it gets, and the builder-assigned names to print after it.
type Edit<'a> = (&'a Stmt, Vec<(TextRange, String)>, Vec<String>);

/// Replace the source of `range` (0-based lines list) with `text`.
fn splice(lines: &mut Vec<String>, index: &Lines, range: TextRange, text: &str) {
    let r0 = index.start_line(range) - 1;
    let c0 = index.col(range.start().to_usize());
    let r1 = index.end_line(range) - 1;
    let c1 = index.col(range.end().to_usize());
    let joined = format!("{}{}{}", &lines[r0][..c0], text, &lines[r1][c1..]);
    lines.splice(r0..=r1, [joined]);
}

fn collapse_blank_runs(text: &str) -> String {
    let mut text = text.to_string();
    while text.contains("\n\n\n\n") {
        text = text.replace("\n\n\n\n", "\n\n\n");
    }
    text
}

/// Remove top-level statements a generator emits out of habit that the
/// sitecustomize environment makes redundant: imports from injected modules
/// and redefinitions of the helper classes. Returns the cleaned source.
pub fn sanitize(code: &str) -> Result<String, String> {
    let parsed = parse_module(code).map_err(|e| e.to_string())?;
    let index = Lines::new(code);
    let mut drop: HashSet<usize> = HashSet::new();
    for stmt in &parsed.syntax().body {
        let range = match stmt {
            Stmt::ImportFrom(i) if i.module.as_ref().is_some_and(|m| is_injected(m.as_str())) => {
                Some((index.start_line(i.range()), index.end_line(i.range())))
            }
            Stmt::Import(i) if i.names.iter().all(|a| is_injected(a.name.as_str())) => {
                Some((index.start_line(i.range()), index.end_line(i.range())))
            }
            Stmt::ClassDef(c) if is_helper(c.name.as_str()) => {
                Some((def_line(&index, &c.name), index.end_line(c.range())))
            }
            _ => None,
        };
        if let Some((a, b)) = range {
            drop.extend(a..=b);
        }
    }
    let code = if drop.is_empty() {
        code.to_string()
    } else {
        let kept: Vec<String> = splitlines(code)
            .into_iter()
            .enumerate()
            .filter(|(i, _)| !drop.contains(&(i + 1)))
            .map(|(_, l)| l)
            .collect();
        // collapse the blank run left where a block was removed
        let text = collapse_blank_runs(&kept.join("\n"));
        format!("{}\n", text.trim_start_matches('\n').trim_end())
    };
    hoist_builders(&code)
}

/// A tree or linked list passed inline to the first-example call is built
/// into a variable named after the parameter, printed on its own line (the
/// harness draws it), then passed. Statements after the demo are untouched.
pub fn hoist_builders(code: &str) -> Result<String, String> {
    let parsed = parse_module(code).map_err(|e| e.to_string())?;
    let body = &parsed.syntax().body;
    let index = Lines::new(code);
    let Some(demo) = body.iter().find(|s| is_demo(s)) else {
        return Ok(code.to_string());
    };
    let demo_line = index.start_line(demo.range());
    let mut lines = splitlines(code);
    let mut taken: HashSet<String> = HashSet::new();
    let mut printed: HashSet<String> = HashSet::new();
    for s in body {
        if index.start_line(s.range()) > demo_line {
            continue;
        }
        if let Stmt::Assign(a) = s {
            taken.extend(a.targets.iter().filter_map(name_id).map(str::to_string));
        }
        if is_bare_print(s) {
            let call = as_call(s).unwrap();
            printed.insert(name_id(&call.arguments.args[0]).unwrap().to_string());
        }
    }
    let mut edits: Vec<Edit> = Vec::new();
    for stmt in body {
        if index.start_line(stmt.range()) > demo_line
            || !matches!(stmt, Stmt::Expr(_) | Stmt::Assign(_))
        {
            continue;
        }
        let mut hoists: Vec<(TextRange, String)> = Vec::new();
        for call in walk_calls(stmt) {
            if is_builder_call(&Expr::Call(call.clone())) {
                continue;
            }
            let params = param_names(body, call);
            for (i, arg) in call.arguments.args.iter().enumerate() {
                if let Some(default) = builder_default(arg) {
                    let base = params
                        .as_ref()
                        .and_then(|p| p.get(i))
                        .filter(|b| !b.is_empty())
                        .cloned()
                        .unwrap_or_else(|| default.to_string());
                    hoists.push((arg.range(), base));
                }
            }
            for kw in &call.arguments.keywords {
                if let Some(default) = builder_default(&kw.value) {
                    let base = kw
                        .arg
                        .as_ref()
                        .map(|a| a.to_string())
                        .unwrap_or_else(|| default.to_string());
                    hoists.push((kw.value.range(), base));
                }
            }
        }
        let mut named: Vec<(TextRange, String)> = Vec::new();
        for (range, base) in hoists {
            let mut name = base.clone();
            let mut k = 1;
            while taken.contains(&name) {
                k += 1;
                name = format!("{base}{k}");
            }
            taken.insert(name.clone());
            named.push((range, name));
        }
        let mut unprinted: Vec<String> = Vec::new();
        if let Stmt::Assign(a) = stmt {
            if is_builder_call(&a.value) && a.targets.len() == 1 {
                if let Some(t) = name_id(&a.targets[0]) {
                    if !printed.contains(t) {
                        unprinted.push(t.to_string());
                    }
                }
            }
        }
        if !named.is_empty() || !unprinted.is_empty() {
            edits.push((stmt, named, unprinted));
        }
    }
    if edits.is_empty() {
        return Ok(code.to_string());
    }
    for (stmt, mut named, unprinted) in edits.into_iter().rev() {
        let mut hoisted: Vec<String> = Vec::new();
        // latest first, so a splice never shifts an earlier one's columns
        named.sort_by_key(|(r, _)| {
            std::cmp::Reverse((index.start_line(*r), index.col(r.start().to_usize())))
        });
        for (range, name) in &named {
            let segment = &code[range.start().to_usize()..range.end().to_usize()];
            hoisted.insert(0, format!("{name} = {segment}"));
            hoisted.insert(1, format!("print({name})"));
            splice(&mut lines, &index, *range, name);
        }
        let after: Vec<String> = unprinted.iter().map(|n| format!("print({n})")).collect();
        let end = index.end_line(stmt.range());
        lines.splice(end..end, after);
        let start = index.start_line(stmt.range()) - 1;
        if !hoisted.is_empty() {
            hoisted.push(String::new());
        }
        lines.splice(start..start, hoisted);
    }
    Ok(format!("{}\n", lines.join("\n").trim_end()))
}

/// The house-format violations in a finished solution file.
pub fn structure_problems(code: &str) -> Vec<String> {
    let mut problems = Vec::new();
    let parsed = match parse_module(code) {
        Ok(p) => p,
        Err(e) => return vec![format!("syntax error: {e}")],
    };
    let body = &parsed.syntax().body;
    if !body.first().is_some_and(is_docstring) {
        problems.push("file must start with the description docstring".to_string());
    }
    if !code.contains("URL: https://leetcode.com") {
        problems.push("docstring must contain the URL line".to_string());
    }
    // house rule: zero imports unless genuinely needed. Imports of injected
    // modules are never needed (sanitize removes them); anything else (re,
    // random, ...) is allowed.
    let redundant = body.iter().any(|n| match n {
        Stmt::ImportFrom(i) => i.module.as_ref().is_some_and(|m| is_injected(m.as_str())),
        Stmt::Import(i) => i.names.iter().any(|a| is_injected(a.name.as_str())),
        _ => false,
    });
    if redundant {
        problems.push("file imports from an injected module".to_string());
    }
    // ordinary problems define class Solution; design problems keep
    // leetcode's natural class name (Trie, NumArray, ...) per the house
    // convention, so any non-helper class satisfies this.
    if !body
        .iter()
        .any(|n| matches!(n, Stmt::ClassDef(c) if !is_helper(c.name.as_str())))
    {
        problems.push("file must define the problem's class".to_string());
    }
    if !code.contains("assert") {
        problems.push("file must end with assert statements".to_string());
    }
    problems
}

/// ast.walk's classes and asserts, at any depth.
#[derive(Default)]
struct Found<'a> {
    classes: Vec<&'a StmtClassDef>,
    asserts: Vec<TextRange>,
}

impl<'a> StatementVisitor<'a> for Found<'a> {
    fn visit_stmt(&mut self, stmt: &'a Stmt) {
        match stmt {
            Stmt::ClassDef(c) => self.classes.push(c),
            Stmt::Assert(a) => self.asserts.push(a.range()),
            _ => {}
        }
        walk_stmt(self, stmt);
    }
}

/// `code` with class method bodies replaced by `pass` and every assert
/// commented out. Prints stay live so the file still runs.
pub fn strip_solution(code: &str) -> Result<String, String> {
    let parsed = parse_module(code).map_err(|e| e.to_string())?;
    let body = &parsed.syntax().body;
    let index = Lines::new(code);
    let src = splitlines(code);

    // start line -> (last line consumed, replacement lines)
    let mut replace: BTreeMap<usize, (usize, Vec<String>)> = BTreeMap::new();
    let mut commented: HashSet<usize> = HashSet::new();

    // everything after the first-example demo call is the test block: it
    // gets commented wholesale (asserts AND any setup they need), so the
    // whole tail toggles back on with one cmd+/ in an editor.
    if let Some(demo) = body.iter().find(|s| is_demo(s)) {
        let demo_end = index.end_line(demo.range());
        let mut live_defs: HashSet<usize> = HashSet::new();
        for stmt in body {
            // defs/classes stay live even after the demo (their bodies are
            // stripped separately); only plain statements join the block.
            let (start, end) = match stmt {
                Stmt::ClassDef(c) => (def_line(&index, &c.name), index.end_line(c.range())),
                Stmt::FunctionDef(f) => (def_line(&index, &f.name), index.end_line(f.range())),
                s => (index.start_line(s.range()), index.end_line(s.range())),
            };
            if start <= demo_end {
                continue;
            }
            if matches!(stmt, Stmt::ClassDef(_) | Stmt::FunctionDef(_)) {
                live_defs.extend(start..=end);
            } else {
                commented.extend(start..=end);
            }
        }
        // prose comments between block statements join the block too
        for (i, line) in src.iter().enumerate() {
            let no = i + 1;
            if no > demo_end && !live_defs.contains(&no) && line.trim_start().starts_with('#') {
                commented.insert(no);
            }
        }
    }

    let mut found = Found::default();
    found.visit_body(body);
    for cls in found.classes {
        if is_helper(cls.name.as_str()) {
            continue;
        }
        for member in &cls.body {
            let Stmt::FunctionDef(f) = member else {
                continue;
            };
            strip_method(&index, &src, f, &mut replace);
        }
    }
    for range in found.asserts {
        commented.extend(index.start_line(range)..=index.end_line(range));
    }

    let mut out: Vec<String> = Vec::new();
    let mut line_no = 1;
    while line_no <= src.len() {
        if let Some((last, replacement)) = replace.get(&line_no) {
            out.extend(replacement.iter().cloned());
            line_no = last + 1;
            continue;
        }
        let line = &src[line_no - 1];
        if commented.contains(&line_no) && !line.trim().is_empty() {
            // existing comments get a second layer, so an editor's
            // uncomment-block action returns them to comments, not to code
            out.push(format!("# {line}"));
        } else {
            out.push(line.clone());
        }
        line_no += 1;
    }
    Ok(format!("{}\n", out.join("\n").trim_end()))
}

fn strip_method(
    index: &Lines,
    src: &[String],
    f: &StmtFunctionDef,
    replace: &mut BTreeMap<usize, (usize, Vec<String>)>,
) {
    let mut body: &[Stmt] = &f.body;
    // leetcode ships some signatures with a docstring ("modify nums
    // in-place instead"); that is part of the problem, so keep it and
    // strip only what follows.
    if body.len() > 1 && is_docstring(&body[0]) {
        body = &body[1..];
    }
    let (first, last) = (&body[0], &body[body.len() - 1]);
    let first_line = index.start_line(first.range());
    let last_end = index.end_line(last.range());
    if first_line == def_line(index, &f.name) {
        // `def f(self): return 1` - keep the signature, drop the body
        let col = index.col(first.range().start().to_usize());
        let head = src[first_line - 1][..col].trim_end().to_string();
        let body_indent = format!("{}    ", indent_of(&head));
        replace.insert(
            first_line,
            (last_end, vec![head, format!("{body_indent}pass")]),
        );
    } else {
        let body_indent = indent_of(&src[first_line - 1]).to_string();
        replace.insert(first_line, (last_end, vec![format!("{body_indent}pass")]));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // utils/tests/test_stub_utils.py, moved here: the prepared stub builds a
    // tree or linked list into a named variable, prints it (the harness
    // draws it), then passes it. hoist_builders rewrites a generator's
    // inline call into that shape; strip_solution must still find the
    // first-example call after the rewrite.
    const HEAD: &str = "\"\"\"URL: https://leetcode.com/problems/x/\"\"\"\n\n\nclass Solution:\n    def mergeTrees(self, root1, root2):\n        return root1\n\n    def depth(self, root):\n        return 1\n\n\nsol = Solution()\n\n";

    #[test]
    fn hoists_into_parameter_names() {
        let code = format!(
            "{HEAD}print(get_level_order(sol.mergeTrees(build_tree([1, 3]), build_tree([2]))))  # [3]\nassert sol.mergeTrees(build_tree([1]), build_tree([2]))\n"
        );
        let out = hoist_builders(&code).unwrap();
        assert_eq!(
            out,
            format!(
                "{HEAD}root1 = build_tree([1, 3])\nprint(root1)\nroot2 = build_tree([2])\nprint(root2)\n\nprint(get_level_order(sol.mergeTrees(root1, root2)))  # [3]\nassert sol.mergeTrees(build_tree([1]), build_tree([2]))\n"
            )
        );
        assert_eq!(hoist_builders(&out).unwrap(), out);
    }

    #[test]
    fn default_name_and_existing_variable_gets_printed() {
        let code = format!(
            "{HEAD}head = build_linked_list([1, 2])\nprint(get_list_values(sol.other(head)))  # [1]\n"
        );
        assert_eq!(
            hoist_builders(&code).unwrap(),
            format!(
                "{HEAD}head = build_linked_list([1, 2])\nprint(head)\nprint(get_list_values(sol.other(head)))  # [1]\n"
            )
        );
        let code = format!("{HEAD}print(sol.other(build_tree([1])))  # 1\n");
        assert_eq!(
            hoist_builders(&code).unwrap(),
            format!("{HEAD}root = build_tree([1])\nprint(root)\n\nprint(sol.other(root))  # 1\n")
        );
    }

    #[test]
    fn strip_keeps_hoisted_lines_live() {
        let code = hoist_builders(&format!(
            "{HEAD}print(sol.depth(build_tree([1])))  # 1\nassert sol.depth(build_tree([1])) == 1\n"
        ))
        .unwrap();
        let stub = strip_solution(&code).unwrap();
        assert!(
            stub.contains("root = build_tree([1])\nprint(root)\n\nprint(sol.depth(root))  # 1\n")
        );
        assert!(stub.contains("# assert sol.depth(build_tree([1])) == 1"));
        assert!(stub.contains("        pass\n"));
    }

    #[test]
    fn sanitize_drops_injected_imports_and_helper_classes() {
        let code = "from typing import List\nimport math\n\n\nclass TreeNode:\n    pass\n\n\nclass Solution:\n    def f(self, x: int) -> int:\n        return x\n";
        assert_eq!(
            sanitize(code).unwrap(),
            "class Solution:\n    def f(self, x: int) -> int:\n        return x\n"
        );
        assert_eq!(
            structure_problems(code),
            vec![
                "file must start with the description docstring",
                "docstring must contain the URL line",
                "file imports from an injected module",
                "file must end with assert statements",
            ]
        );
    }

    #[test]
    fn strip_comments_the_tail_and_keeps_one_liners_signature() {
        let code = "\"\"\"URL: https://leetcode.com/problems/x/\"\"\"\n\n\nclass Solution:\n    def f(self, x): return x\n\n    @cache\n    def g(self, x):\n        \"\"\"keep me\"\"\"\n        return x\n\n\nsol = Solution()\n\nprint(sol.f(1))  # 1\n\n# the tests\nassert sol.f(1) == 1\nassert sol.g(2) == 2\n";
        assert_eq!(
            strip_solution(code).unwrap(),
            "\"\"\"URL: https://leetcode.com/problems/x/\"\"\"\n\n\nclass Solution:\n    def f(self, x):\n        pass\n\n    @cache\n    def g(self, x):\n        \"\"\"keep me\"\"\"\n        pass\n\n\nsol = Solution()\n\nprint(sol.f(1))  # 1\n\n# # the tests\n# assert sol.f(1) == 1\n# assert sol.g(2) == 2\n"
        );
    }
}
