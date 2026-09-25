//! What leetcode runs: the solve file stripped to its submitted class and
//! the definitions that class needs, found on the AST (ruff's parser), never
//! by matching text.
//!
//! The submitted class is the last top-level `class Solution`; a design
//! problem has none, so there it is the last top-level class of any name.
//! Above it go, dependencies first: helpers the harness preloads and
//! leetcode lacks (HELPER_FILES: cells, nbrs, like, grid_bfs, Multiset, the
//! maxheap functions, lcs), the dsa modules the file imports from, then the file's own
//! functions, classes, constants and stdlib imports. A name is "used" when
//! the class loads it and binds it nowhere (a parameter called `root` does
//! not pull `root = build_tree(...)` in), and an own assignment that itself
//! calls the harness is test setup and never sent.

use std::collections::{BTreeSet, HashSet};
use std::path::Path;

use ruff_python_ast::visitor::{walk_expr, walk_stmt, Visitor};
use ruff_python_ast::{Expr, ExprContext, Parameter, Stmt};
use ruff_text_size::{Ranged, TextRange};

/// Preloaded by the harness, absent on leetcode: their top-level names are
/// pasted in when the submission uses them. sitecustomize's
/// `builtins.xor = operator.xor` lines count as definitions of the bare name.
/// Only the modules a solution may call belong here; the drawing, building
/// and read-back modules stay out so that a class calling them is refused
/// (`every_solve_time_builtin_is_submittable` keeps the two sets apart).
pub const HELPER_FILES: [&str; 9] = [
    "utils/harness/sitecustomize.py",
    "utils/harness/adj_utils.py",
    "utils/harness/grid_utils.py",
    "utils/harness/bs_utils.py",
    "utils/harness/combo_utils.py",
    "utils/harness/counter_utils.py",
    "utils/harness/gen_utils.py",
    "utils/harness/seq_utils.py",
    "dsa/maxheapq.py",
];

/// Modules the harness imports that leetcode does not install: a helper
/// that needs one (tabulate, pprint) is never sent, so the class calling it
/// is refused by name.
const NOT_ON_LEETCODE: [&str; 6] = [
    "rich",
    "tabulate",
    "PrettyPrintTree",
    "colorama",
    "graphviz",
    "networkx",
];

/// Modules leetcode's python3 preamble star-imports (as the harness mirrors).
const PRELOADED_MODULES: [&str; 8] = [
    "typing",
    "collections",
    "itertools",
    "functools",
    "heapq",
    "bisect",
    "math",
    "string",
];

/// What the submitted code may use without defining: CPython's builtins,
/// the preamble's imports, the given classes, the interactive problems'
/// given functions (a local stub for one of these is never sent).
const GIVEN: &str = "\
abs all any ascii bin bool breakpoint bytearray bytes callable chr classmethod compile complex \
delattr dict dir divmod enumerate eval exec filter float format frozenset getattr globals hasattr \
hash help hex id input int isinstance issubclass iter len list locals map max memoryview min next \
object oct open ord pow print property range repr reversed round set setattr slice sorted \
staticmethod str sum super tuple type vars zip __import__ __name__ __build_class__ __debug__ \
None True False Ellipsis NotImplemented \
BaseException Exception ArithmeticError AssertionError AttributeError EOFError FloatingPointError \
GeneratorExit ImportError IndexError KeyError KeyboardInterrupt LookupError MemoryError NameError \
NotImplementedError OSError OverflowError RecursionError RuntimeError StopIteration \
StopAsyncIteration SyntaxError TypeError UnboundLocalError ValueError ZeroDivisionError \
Warning DeprecationWarning UserWarning \
typing collections itertools functools heapq bisect math string \
List Dict Set Tuple Optional Union Any Callable Iterable Iterator Generator Sequence Mapping \
MutableMapping Deque DefaultDict FrozenSet TypeVar Generic Protocol NamedTuple TypedDict Literal \
Final ClassVar Type cast overload no_type_check Hashable Sized Collection Awaitable \
Counter defaultdict deque OrderedDict namedtuple ChainMap \
accumulate chain combinations combinations_with_replacement permutations product groupby count \
cycle repeat islice starmap takewhile dropwhile zip_longest pairwise compress filterfalse tee \
cache lru_cache reduce partial cmp_to_key wraps cached_property total_ordering singledispatch \
heapify heappush heappop heappushpop heapreplace nlargest nsmallest merge \
bisect_left bisect_right insort insort_left insort_right \
inf nan pi e tau sqrt isqrt ceil floor gcd lcm log log2 log10 log1p exp pow factorial comb perm \
prod hypot dist fabs isclose isfinite isinf isnan fsum copysign trunc atan2 sin cos tan atan asin \
acos degrees radians \
ascii_lowercase ascii_uppercase ascii_letters digits hexdigits octdigits punctuation whitespace \
printable \
TreeNode ListNode Node GraphNode NestedInteger SortedList SortedDict SortedSet sortedcontainers \
guess isBadVersion read4 knows ArrayReader MountainArray Master BinaryMatrix Sea ImmutableListNode \
Robot GridMaster";

fn given() -> HashSet<&'static str> {
    GIVEN.split_whitespace().collect()
}

/// The names a piece of code loads and binds. Free = loaded - bound.
#[derive(Default)]
struct Names {
    loaded: HashSet<String>,
    bound: HashSet<String>,
}

impl Names {
    fn free(&self) -> BTreeSet<String> {
        self.loaded.difference(&self.bound).cloned().collect()
    }
}

impl<'a> Visitor<'a> for Names {
    fn visit_stmt(&mut self, stmt: &'a Stmt) {
        match stmt {
            Stmt::FunctionDef(f) => {
                self.bound.insert(f.name.to_string());
            }
            Stmt::ClassDef(c) => {
                self.bound.insert(c.name.to_string());
            }
            Stmt::Import(i) => {
                for a in &i.names {
                    let n = a.asname.as_ref().unwrap_or(&a.name);
                    self.bound
                        .insert(n.split('.').next().unwrap_or("").to_string());
                }
            }
            Stmt::ImportFrom(i) => {
                for a in &i.names {
                    self.bound
                        .insert(a.asname.as_ref().unwrap_or(&a.name).to_string());
                }
            }
            Stmt::Global(g) => {
                for n in &g.names {
                    self.loaded.insert(n.to_string());
                }
            }
            _ => {}
        }
        walk_stmt(self, stmt);
    }

    fn visit_expr(&mut self, expr: &'a Expr) {
        if let Expr::Name(n) = expr {
            match n.ctx {
                ExprContext::Load => {
                    self.loaded.insert(n.id.to_string());
                }
                _ => {
                    self.bound.insert(n.id.to_string());
                }
            }
        }
        walk_expr(self, expr);
    }

    fn visit_parameter(&mut self, p: &'a Parameter) {
        self.bound.insert(p.name.to_string());
    }

    fn visit_except_handler(&mut self, h: &'a ruff_python_ast::ExceptHandler) {
        let ruff_python_ast::ExceptHandler::ExceptHandler(e) = h;
        if let Some(n) = &e.name {
            self.bound.insert(n.to_string());
        }
        ruff_python_ast::visitor::walk_except_handler(self, h);
    }
}

fn free_names(stmt: &Stmt) -> BTreeSet<String> {
    let mut v = Names::default();
    v.visit_stmt(stmt);
    v.free()
}

/// One top-level definition: the name it binds, its source (decorators
/// included), the names it uses, and whether it imports a module leetcode
/// lacks.
struct Block {
    name: String,
    source: String,
    uses: BTreeSet<String>,
    unrunnable: bool,
}

fn imports_missing_module(stmt: &Stmt) -> bool {
    let top = |m: &str| m.split('.').next().unwrap_or("").to_string();
    let roots: Vec<String> = match stmt {
        Stmt::Import(i) => i.names.iter().map(|a| top(&a.name)).collect(),
        Stmt::ImportFrom(i) => i.module.iter().map(|m| top(m)).collect(),
        _ => vec![],
    };
    roots.iter().any(|r| NOT_ON_LEETCODE.contains(&r.as_str()))
}

fn stmt_source(src: &str, stmt: &Stmt) -> String {
    let start = match stmt {
        Stmt::FunctionDef(f) => f.decorator_list.first().map_or(f.start(), |d| d.start()),
        Stmt::ClassDef(c) => c.decorator_list.first().map_or(c.start(), |d| d.start()),
        s => s.start(),
    };
    src[TextRange::new(start, stmt.end())].to_string()
}

/// A module the harness resolves and leetcode cannot (dsa, the harness
/// itself) or preloads anyway: never sent as an import line.
fn is_local_import(root: &Path, stmt: &Stmt) -> bool {
    match stmt {
        Stmt::ImportFrom(i) => match &i.module {
            None => true,
            Some(m) => {
                let m = m.as_str();
                i.level > 0
                    || m.starts_with("dsa.")
                    || PRELOADED_MODULES.contains(&m)
                    || root.join(format!("utils/harness/{m}.py")).exists()
            }
        },
        Stmt::Import(i) => i.names.iter().all(|a| {
            let m = a.name.as_str();
            PRELOADED_MODULES.contains(&m) || m == "builtins" || m.starts_with("dsa")
        }),
        _ => false,
    }
}

/// `builtins.name = expr` in sitecustomize: the harness defining a bare
/// name. Its source for leetcode is `name = expr`.
fn builtins_alias(src: &str, stmt: &Stmt) -> Option<(String, String)> {
    let Stmt::Assign(a) = stmt else {
        return None;
    };
    let [Expr::Attribute(t)] = a.targets.as_slice() else {
        return None;
    };
    match t.value.as_ref() {
        Expr::Name(n) if n.id.as_str() == "builtins" => Some((
            t.attr.to_string(),
            format!("{} = {}", t.attr, &src[a.value.range()]),
        )),
        _ => None,
    }
}

/// The names a top-level statement binds; empty for one that is not a
/// definition (an assert, a call, an `if __name__` demo).
fn names_bound(stmt: &Stmt) -> Vec<String> {
    match stmt {
        Stmt::FunctionDef(f) => vec![f.name.to_string()],
        Stmt::ClassDef(c) => vec![c.name.to_string()],
        Stmt::Assign(a) => a
            .targets
            .iter()
            .filter_map(|t| match t {
                Expr::Name(n) => Some(n.id.to_string()),
                _ => None,
            })
            .collect(),
        Stmt::AnnAssign(a) => match a.target.as_ref() {
            Expr::Name(n) => vec![n.id.to_string()],
            _ => vec![],
        },
        Stmt::Import(i) => i
            .names
            .iter()
            .map(|a| {
                a.asname.as_ref().map_or_else(
                    || a.name.split('.').next().unwrap_or("").to_string(),
                    |n| n.to_string(),
                )
            })
            .collect(),
        Stmt::ImportFrom(i) => i
            .names
            .iter()
            .map(|a| a.asname.as_ref().unwrap_or(&a.name).to_string())
            .collect(),
        _ => vec![],
    }
}

/// Top-level definitions of `src` in order, the first binding of each name
/// only: a later one in a solve is test setup (`bad = 4 ... bad = 1`).
fn blocks(root: &Path, src: &str, skip: Option<&Stmt>) -> Vec<Block> {
    let Ok(parsed) = ruff_python_parser::parse_module(src) else {
        return vec![];
    };
    let mut seen = HashSet::new();
    let mut out = vec![];
    for stmt in &parsed.syntax().body {
        if skip.is_some_and(|s| s.range() == stmt.range()) || is_local_import(root, stmt) {
            continue;
        }
        let alias = builtins_alias(src, stmt);
        // `builtins.draw_tree = draw_tree` defines nothing leetcode can run:
        // the name comes from a harness star import
        if alias
            .as_ref()
            .is_some_and(|(n, _)| free_names(stmt).contains(n) && !seen.contains(n))
        {
            continue;
        }
        let bound = match &alias {
            Some((name, _)) => vec![name.clone()],
            None => names_bound(stmt),
        };
        let names: Vec<String> = bound
            .into_iter()
            .filter(|n| seen.insert(n.clone()))
            .collect();
        if names.is_empty() {
            continue;
        }
        let source = match &alias {
            Some((_, source)) => source.clone(),
            None => stmt_source(src, stmt),
        };
        let mut uses = free_names(stmt);
        if alias.is_some() {
            uses.remove("builtins");
        }
        for name in names {
            out.push(Block {
                name,
                source: source.clone(),
                uses: uses.clone(),
                unrunnable: imports_missing_module(stmt),
            });
        }
    }
    out
}

fn dsa_imports(src: &str) -> Vec<String> {
    let Ok(parsed) = ruff_python_parser::parse_module(src) else {
        return vec![];
    };
    parsed
        .syntax()
        .body
        .iter()
        .filter_map(|s| match s {
            Stmt::ImportFrom(i) => i
                .module
                .as_ref()
                .filter(|m| m.starts_with("dsa."))
                .map(|m| format!("{}.py", m.replace('.', "/"))),
            _ => None,
        })
        .collect()
}

/// Drop every helper block leetcode cannot run: one importing a module it
/// lacks, or one using a name no remaining block defines (`_drawer_for`
/// calls the drawing functions), and so on to a fixed point.
fn prune_unrunnable(candidates: &mut Vec<Block>, given: &HashSet<&str>) {
    let mut dead = vec![false; candidates.len()];
    loop {
        let defined: HashSet<&str> = candidates
            .iter()
            .zip(&dead)
            .filter(|(_, d)| !**d)
            .map(|(b, _)| b.name.as_str())
            .collect();
        let mut changed = false;
        for (i, b) in candidates.iter().enumerate() {
            let lacks = |u: &String| {
                !given.contains(u.as_str()) && *u != b.name && !defined.contains(u.as_str())
            };
            if !dead[i] && (b.unrunnable || b.uses.iter().any(lacks)) {
                dead[i] = true;
                changed = true;
            }
        }
        if !changed {
            break;
        }
    }
    let mut it = dead.into_iter();
    candidates.retain(|_| !it.next().unwrap_or(false));
}

/// The class to submit: the last `class Solution`, else the last class.
fn target_class(body: &[Stmt]) -> Option<&Stmt> {
    let classes: Vec<&Stmt> = body
        .iter()
        .filter(|s| matches!(s, Stmt::ClassDef(_)))
        .collect();
    classes
        .iter()
        .rev()
        .find(|s| matches!(s, Stmt::ClassDef(c) if c.name.as_str() == "Solution"))
        .or(classes.last())
        .copied()
}

/// The quoted mu source that `make solved` and `make submit` put above
/// the transpiled class: the last top-level comment block before `end`
/// that starts with a mu header. The AST drops comments, so it is found
/// in the text. A `# mu 0.2` header is sent with the block. Solves filed
/// before the version was recorded open with `# mu source (current.mu)`
/// and two more lines down to a bare `#`; those stay home and the quoted
/// mu goes alone.
fn mu_source(src: &str, end: usize) -> Option<String> {
    let before = &src[..end];
    let is_header = |ln: &str| {
        ln.starts_with("# mu source")
            || ln
                .strip_prefix("# mu ")
                .is_some_and(|v| !v.is_empty() && v.chars().all(|c| c.is_ascii_digit() || c == '.'))
    };
    let mut starts = vec![0];
    starts.extend(before.match_indices('\n').map(|(i, _)| i + 1));
    let at = starts
        .into_iter()
        .rfind(|&i| is_header(before[i..].lines().next().unwrap_or("")))?;
    let block: Vec<&str> = before[at..]
        .lines()
        .take_while(|ln| ln.starts_with('#'))
        .collect();
    if !block[0].starts_with("# mu source") {
        return Some(block.join("\n"));
    }
    // the mu's own blank lines are bare `#` lines too, so look in three
    let body = match block.iter().take(3).position(|ln| ln.trim_end() == "#") {
        Some(k) => &block[k + 1..],
        None => &block[1..],
    };
    Some(body.join("\n"))
}

/// The code to submit for the solve file `src`; None when it does not
/// parse or has no class. A quoted mu source goes first, as comments.
pub fn strip(root: &Path, src: &str) -> Option<String> {
    let parsed = ruff_python_parser::parse_module(src).ok()?;
    let target = target_class(&parsed.syntax().body)?;
    let main_source = stmt_source(src, target);
    let given = given();

    let mut candidates: Vec<Block> = vec![];
    for f in HELPER_FILES
        .iter()
        .map(|s| s.to_string())
        .chain(dsa_imports(src))
    {
        if let Ok(text) = std::fs::read_to_string(root.join(&f)) {
            candidates.extend(blocks(root, &text, None));
        }
    }
    prune_unrunnable(&mut candidates, &given);
    let own = blocks(root, src, Some(target));
    let known: HashSet<String> = candidates
        .iter()
        .chain(&own)
        .map(|b| b.name.clone())
        .collect();
    for b in own {
        // an own assignment that calls the harness is test setup
        let foreign = b
            .uses
            .iter()
            .any(|u| !given.contains(u.as_str()) && !known.contains(u));
        if !foreign {
            candidates.push(b);
        }
    }

    let mut needed = vec![false; candidates.len()];
    let mut frontier: Vec<String> = free_names(target)
        .into_iter()
        .filter(|n| !given.contains(n.as_str()))
        .collect();
    while let Some(name) = frontier.pop() {
        for (i, b) in candidates.iter().enumerate() {
            if b.name == name && !needed[i] {
                needed[i] = true;
                frontier.extend(
                    b.uses
                        .iter()
                        .filter(|u| !given.contains(u.as_str()) && **u != b.name)
                        .cloned(),
                );
            }
        }
    }
    let mut parts: Vec<String> = vec![];
    let mut emitted = HashSet::new();
    for (b, n) in candidates.iter().zip(&needed) {
        // an assignment binding two names is one block, sent once
        if *n && emitted.insert(b.source.clone()) {
            parts.push(b.source.clone());
        }
    }
    parts.push(main_source);
    let code = parts.join("\n\n\n") + "\n";
    Some(match mu_source(src, target.start().to_usize()) {
        Some(mu) => format!("{mu}\n\n{code}"),
        None => code,
    })
}

/// The free names of a submission that leetcode will not have: what its
/// own definitions and the preamble leave unbound.
pub fn undefined_names(root: &Path, code: &str) -> BTreeSet<String> {
    let Ok(parsed) = ruff_python_parser::parse_module(code) else {
        return BTreeSet::from(["<does not parse>".to_string()]);
    };
    let given = given();
    let defined: HashSet<String> = blocks(root, code, None)
        .into_iter()
        .map(|b| b.name)
        .collect();
    let mut all = BTreeSet::new();
    for s in &parsed.syntax().body {
        all.extend(free_names(s));
    }
    all.into_iter()
        .filter(|n| !given.contains(n.as_str()) && !defined.contains(n))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    const DOC: &str = "\"\"\"\nURL: https://leetcode.com/problems/x/\n\n---\n\nnotes\n\"\"\"\n\n";

    fn root() -> std::path::PathBuf {
        kg::data::repo_root()
    }

    #[test]
    fn last_solution_class_only() {
        let src = format!(
            "{DOC}class Solution:\n    def a(self):\n        return 1\n\n\n\
             class Solution:\n    def a(self):\n        # final\n        return 2\n\n\n\
             sol = Solution()\n\nassert sol.a() == 2\n"
        );
        assert_eq!(
            strip(&root(), &src).unwrap(),
            "class Solution:\n    def a(self):\n        # final\n        return 2\n"
        );
    }

    #[test]
    fn the_mu_source_goes_first_as_comments() {
        let class = "class Solution:\n    def a(self) -> int:\n        return 1\n";
        let asserts = "\n\nsol = Solution()\n\nassert sol.a() == 1\n";
        let src = format!("{DOC}# mu 0.2\n# def a -> int\n#\n#   1\n\n{class}{asserts}");
        assert_eq!(
            strip(&root(), &src).unwrap(),
            format!("# mu 0.2\n# def a -> int\n#\n#   1\n\n{class}")
        );
        // filed before the version was recorded: the old header stays home
        let src = format!(
            "{DOC}# mu source (current.mu), the candidate's solution. The Python\n\
             # under it is the transpiler's output, and it is what ran.\n#\n\
             # def a -> int\n#   1\n\n{class}{asserts}"
        );
        assert_eq!(
            strip(&root(), &src).unwrap(),
            format!("# def a -> int\n#   1\n\n{class}")
        );
    }

    #[test]
    fn the_helper_check_stays_home_and_the_helper_it_names_comes_along() {
        let src = format!(
            "{DOC}class Solution:\n    def a(self, e):\n        return adjacency(e)\n\n\n\
             sol = Solution()\n\nassert uses(Solution, adjacency)\nassert sol.a([]) == {{}}\n"
        );
        let out = strip(&root(), &src).unwrap();
        assert!(out.contains("def adjacency("), "{out}");
        assert!(!out.contains("uses"), "{out}");
        assert!(!out.contains("assert"), "{out}");
    }

    #[test]
    fn own_defs_classes_constants_and_imports_come_along() {
        let src = format!(
            "{DOC}import copy\nfrom tree_utils import build_tree\n\n\
             class State:\n    A = 1\n\n\n\
             def unused():\n    pass\n\n\n\
             @cache\ndef helper(x):\n    return State.A + x\n\n\n\
             D = {{1: 2}}\n\n\n\
             root = build_tree([1])\n\n\n\
             class Solution:\n    def f(self, root):\n        return helper(D[1]) + copy.copy(1)\n\n\n\
             sol = Solution()\n"
        );
        assert_eq!(
            strip(&root(), &src).unwrap(),
            "import copy\n\n\n\
             class State:\n    A = 1\n\n\n\
             @cache\ndef helper(x):\n    return State.A + x\n\n\n\
             D = {1: 2}\n\n\n\
             class Solution:\n    def f(self, root):\n        return helper(D[1]) + copy.copy(1)\n"
        );
    }

    #[test]
    fn design_problem_takes_the_last_class() {
        let src = format!(
            "{DOC}class Helper:\n    pass\n\n\n\
             class StockPrice:\n    def __init__(self):\n        self.h = Helper()\n\n\n\
             sol = StockPrice()\n"
        );
        assert_eq!(
            strip(&root(), &src).unwrap(),
            "class Helper:\n    pass\n\n\n\
             class StockPrice:\n    def __init__(self):\n        self.h = Helper()\n"
        );
    }

    #[test]
    fn harness_helpers_expand_transitively() {
        let out = strip(
            &root(),
            &format!(
                "{DOC}class Solution:\n    def f(self, g):\n        return grid_bfs(g, [(0, 0)])\n"
            ),
        )
        .unwrap();
        let at = |s: &str| {
            out.find(s)
                .unwrap_or_else(|| panic!("{s} missing in:\n{out}"))
        };
        assert!(at("CARDINALS") < at("def nbrs(") && at("def nbrs(") < at("def grid_bfs("));
        assert!(at("def like(") < at("def grid_bfs("));
        assert!(!out.contains("def cells("), "named only in a docstring");
        assert!(!out.contains("import "));
        let heap = strip(
            &root(),
            &format!("{DOC}class Solution:\n    def f(self, h):\n        maxheappush(h, 1)\n"),
        )
        .unwrap();
        assert!(heap.contains("class _Rev:") && heap.contains("def maxheappush("));
        assert!(!heap.contains("def maxheappop(") && !heap.contains("__name__"));
    }

    #[test]
    fn interactive_stub_is_not_sent() {
        let src = format!(
            "{DOC}pick = 6\n\n\ndef guess(num):\n    return (pick > num) - (pick < num)\n\n\n\
             class Solution:\n    def guessNumber(self, n):\n        return guess(n)\n"
        );
        assert_eq!(
            strip(&root(), &src).unwrap(),
            "class Solution:\n    def guessNumber(self, n):\n        return guess(n)\n"
        );
    }

    #[test]
    fn harness_bare_names_become_definitions() {
        let out = strip(
            &root(),
            &format!("{DOC}class Solution:\n    def f(self, a):\n        return xor(a, maxsize) or dd(int) or match(\"a\", a)\n"),
        )
        .unwrap();
        for line in [
            "import operator",
            "xor = operator.xor",
            "from sys import maxsize",
            "dd = defaultdict",
            "import re",
            "match = re.match",
        ] {
            assert!(out.contains(line), "{line} missing in:\n{out}");
        }
        assert!(out.find("import operator").unwrap() < out.find("xor = ").unwrap());
        assert!(!out.contains("builtins"));
        assert!(undefined_names(&root(), &out).is_empty());
        let draw = strip(
            &root(),
            &format!("{DOC}class Solution:\n    def f(self, t):\n        draw_tree(t)\n"),
        )
        .unwrap();
        assert!(!draw.contains("draw_tree = draw_tree"), "{draw}");
        assert_eq!(
            undefined_names(&root(), &draw),
            BTreeSet::from(["draw_tree".to_string()])
        );
    }

    /// Harness builtins a solution never calls: they print, draw, build a
    /// test input or read a structure back. Everything else sitecustomize
    /// puts into builtins must strip to code leetcode can run.
    const TEST_ONLY: &str = "\
tabulate print_orig pprint rich_print draw_tree draw_linked_list draw_general_tree \
get_level_order debug_var debug_vars draw_ascii_graph draw_graphviz draw_graph draw_heap \
build_tree generate_and_print_random_bst generate_full_binary_tree generate_random_tree \
build_graph_from_edge_list build_nary_tree get_adj_list build_graph get_list_values \
print_linked_list build_linked_list find_node get_inorder is_balanced is_valid_bst same_rows same_seq uses avoids";

    #[test]
    fn every_solve_time_builtin_is_submittable() {
        let root = root();
        let src = std::fs::read_to_string(root.join(HELPER_FILES[0])).unwrap();
        let parsed = ruff_python_parser::parse_module(&src).unwrap();
        let names: Vec<String> = parsed
            .syntax()
            .body
            .iter()
            .filter_map(|s| builtins_alias(&src, s).map(|(n, _)| n))
            .collect();
        assert!(names.len() > 100, "{names:?}");
        let test_only: HashSet<&str> = TEST_ONLY.split_whitespace().collect();
        for name in &names {
            let out = strip(
                &root,
                &format!("{DOC}class Solution:\n    def f(self, a):\n        return {name}(a)\n"),
            )
            .unwrap();
            let missing = undefined_names(&root, &out);
            if test_only.contains(name.as_str()) {
                assert_eq!(
                    missing,
                    BTreeSet::from([name.clone()]),
                    "{name} is on TEST_ONLY but strips to code leetcode can run"
                );
            } else {
                assert!(
                    missing.is_empty(),
                    "{name}: leetcode lacks {missing:?} in:\n{out}"
                );
            }
        }
        for name in test_only {
            assert!(names.contains(&name.to_string()), "{name} is not a builtin");
        }
    }

    #[test]
    fn undefined_names_are_what_leetcode_lacks() {
        let ok =
            "class Solution:\n    def f(self, a):\n        return heappush(a, inf) or Counter()\n";
        assert!(undefined_names(&root(), ok).is_empty());
        let leak = "class Solution:\n    def f(self, a):\n        return build_tree(a)\n";
        assert_eq!(
            undefined_names(&root(), leak),
            BTreeSet::from(["build_tree".to_string()])
        );
    }
}
