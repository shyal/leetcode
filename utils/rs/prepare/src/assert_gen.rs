//! Extra asserts for a prepared problem, computed by running the reference.
//!
//! The prepare pipeline's edge-case stage proposes single-call expressions,
//! which a design problem cannot express - a class is driven by a SEQUENCE
//! of calls, so 2349 shipped with nothing but its two official asserts, and
//! a solve whose find() popped the heap passed both.
//!
//! Every assert here is one self-contained line: a class is built inline
//! with the walrus operator, so no line depends on any other and the block
//! can be uncommented whole or a line at a time. The expected values are
//! frozen by executing the validated reference solution from the prepare
//! cache, so none is ever guessed, and each line carries the case it covers
//! as a trailing comment.
//!
//! Run it again on the same problem and the block grows: the cases already
//! covered are handed to the model as labels it must look past, and the new
//! lines are appended under them.
//!
//! Ported from utils/kg/assert_gen.py on 2026-09-14.

use std::collections::HashSet;

use regex::Regex;
use ruff_python_ast::visitor::{walk_expr, Visitor};
use ruff_python_ast::{Expr, Number, Operator, UnaryOp};
use ruff_python_parser::parse_expression;

pub const MARK: &str = "# edge cases: one line each, the values are the reference solution's.";

/// A line the solve file has to stay readable with. Anything longer is a
/// workload, not a case, and gets dropped.
const MAX_LINE: usize = 240;

const PROMPT: &str = r#"The file below contains a correct, validated solution to a LeetCode problem.

Propose test expressions for its edge cases: ONE line each, formatted as

    <expression>  # <label>

Rules for the expression:

- it evaluates to a plain comparable value (int, string, tuple, list of them).
  Wrap structure results with helpers like get_level_order / get_list_values,
  as the existing asserts do.
- it is entirely self-contained - no line may depend on another having run,
  and none may use `sol` or any other object the file already built. A problem
  driven by a class is built inline with the walrus operator and the query
  taken last, like this:

    [(nc := NumberContainers()), nc.change(5, 7), nc.change(5, 8), nc.find(7)][-1]

- it stays under 200 characters, and it defines no function

Rules for the label:

- it describes what the INPUT does, in the problem's own words, and never how
  a solution copes with it: "index_reassigned_then_queried", not
  "stale_heap_entry_skipped". The file is read by someone about to solve the
  problem; a label naming heaps, caches, memoization or two pointers hands
  them the answer.

Cover the boundaries that actually bite this problem: the smallest legal
input, an empty or absent lookup, a value replaced by itself, duplicates,
negatives, a query before anything exists, the extremes the constraints allow,
and a longer mixed sequence or two.

At most 12 lines. Output ONLY those lines - no asserts, no expected values, no
blank lines, no prose.
{more}
{code}
"#;

const MORE: &str = r#"
These cases are already covered:

{labels}

Propose ones they miss. A repeat of a case above is wasted: the point of this
pass is what the existing labels do not name.
"#;

/// prepare.strip_fences: some models wrap output in markdown fences despite
/// the system prompt.
pub fn strip_fences(out: &str) -> String {
    if !out.starts_with("```") {
        return out.to_string();
    }
    let mut lines: Vec<&str> = out.lines().skip(1).collect();
    if lines.last().is_some_and(|l| l.trim() == "```") {
        lines.pop();
    }
    lines.join("\n").trim().to_string()
}

struct HasLambda(bool);

impl Visitor<'_> for HasLambda {
    fn visit_expr(&mut self, expr: &Expr) {
        if matches!(expr, Expr::Lambda(_)) {
            self.0 = true;
        }
        walk_expr(self, expr);
    }
}

/// (expression, label) for each usable line the model proposed.
fn proposals(text: &str) -> Vec<(String, String)> {
    let non_word = Regex::new(r"\W+").unwrap();
    let mut out = Vec::new();
    for line in text.lines() {
        let line = line.trim().trim_end_matches(',');
        if line.is_empty()
            || line.starts_with('#')
            || line.starts_with("```")
            || line.starts_with("assert ")
        {
            continue;
        }
        let (expr, label) = match line.split_once('#') {
            Some((e, l)) => (e.trim(), l.trim()),
            None => (line, ""),
        };
        if expr.is_empty() || label.is_empty() {
            continue;
        }
        let Ok(parsed) = parse_expression(expr) else {
            continue;
        };
        let mut lambda = HasLambda(false);
        lambda.visit_expr(&parsed.syntax().body);
        if lambda.0 {
            continue;
        }
        let label = non_word
            .replace_all(label, "_")
            .trim_matches('_')
            .to_string();
        out.push((expr.to_string(), label));
    }
    out
}

/// The labels a file's one-line asserts already carry.
pub fn covered(code: &str) -> Vec<String> {
    Regex::new(r"(?m)^assert .*#\s*(\S+)\s*$")
        .unwrap()
        .captures_iter(code)
        .map(|m| m[1].to_string())
        .collect()
}

fn is_num(e: &Expr) -> bool {
    matches!(e, Expr::NumberLiteral(_))
}

fn is_complex(e: &Expr) -> bool {
    matches!(e, Expr::NumberLiteral(n) if matches!(n.value, Number::Complex { .. }))
}

fn is_signed_num(e: &Expr) -> bool {
    match e {
        Expr::UnaryOp(u) if matches!(u.op, UnaryOp::UAdd | UnaryOp::USub) => is_num(&u.operand),
        e => is_num(e),
    }
}

/// ast.literal_eval accepts it: the literals, containers of literals, signed
/// numbers and `a+bj` complex forms, nothing that names or calls.
pub fn is_literal(text: &str) -> bool {
    fn ok(e: &Expr) -> bool {
        match e {
            Expr::StringLiteral(_)
            | Expr::BytesLiteral(_)
            | Expr::NumberLiteral(_)
            | Expr::BooleanLiteral(_)
            | Expr::NoneLiteral(_)
            | Expr::EllipsisLiteral(_) => true,
            Expr::Tuple(t) => t.elts.iter().all(ok),
            Expr::List(l) => l.elts.iter().all(ok),
            Expr::Set(s) => s.elts.iter().all(ok),
            Expr::Dict(d) => d
                .items
                .iter()
                .all(|it| it.key.as_ref().is_some_and(ok) && ok(&it.value)),
            Expr::UnaryOp(_) => is_signed_num(e),
            Expr::BinOp(b) if matches!(b.op, Operator::Add | Operator::Sub) => {
                is_signed_num(&b.left) && !is_complex(&b.left) && is_complex(&b.right)
            }
            _ => false,
        }
    }
    parse_expression(text).is_ok_and(|p| ok(&p.syntax().body))
}

/// Run every proposal against the reference and keep the ones that come
/// back as a literal. A proposal that raises, hangs on a helper the file
/// does not have, or answers with a repr like <TreeNode object> is dropped.
fn freeze(
    run: &dyn Fn(&str) -> (bool, String),
    code: &str,
    proposals: &[(String, String)],
) -> Vec<(String, String, String)> {
    let mut harness = vec![code.to_string(), String::new()];
    for (i, (expr, _)) in proposals.iter().enumerate() {
        harness.push(format!(
            "try:\n    print('@@', {i}, repr(({expr})))\nexcept Exception:\n    pass"
        ));
    }
    let (ok, output) = run(&harness.join("\n"));
    if !ok {
        return Vec::new();
    }
    let mut frozen: Vec<(usize, String)> = Vec::new();
    for line in output.lines() {
        let Some(rest) = line.strip_prefix("@@ ") else {
            continue;
        };
        let Some((idx, rep)) = rest.split_once(' ') else {
            continue;
        };
        let Ok(idx) = idx
            .parse::<usize>()
            .ok()
            .filter(|i| *i < proposals.len())
            .ok_or(())
        else {
            continue;
        };
        if !is_literal(rep) {
            continue;
        }
        frozen.retain(|(i, _)| *i != idx);
        frozen.push((idx, rep.to_string()));
    }
    frozen.sort_by_key(|(i, _)| *i);
    frozen
        .into_iter()
        .map(|(i, rep)| (proposals[i].0.clone(), proposals[i].1.clone(), rep))
        .collect()
}

/// `code` with one assert line appended per new edge case it survives.
pub fn extra_asserts(
    code: &str,
    llm: &dyn Fn(&str) -> Result<String, String>,
    run: &dyn Fn(&str) -> (bool, String),
) -> Result<String, String> {
    let already = covered(code);
    let more = if already.is_empty() {
        String::new()
    } else {
        let labels: Vec<String> = already.iter().map(|l| format!("- {l}")).collect();
        MORE.replace("{labels}", &labels.join("\n"))
    };
    let prompt = PROMPT.replace("{more}", &more).replace("{code}", code);
    let proposed: Vec<(String, String)> = proposals(&strip_fences(&llm(&prompt)?))
        .into_iter()
        .filter(|(_, l)| !already.contains(l))
        .collect();
    if proposed.is_empty() {
        return Ok(code.to_string());
    }

    let mut lines: Vec<String> = Vec::new();
    let mut seen: HashSet<String> = already.iter().cloned().collect();
    for (expr, label, rep) in freeze(run, code, &proposed) {
        let line = format!("assert {expr} == {rep}  # {label}");
        if seen.contains(&label) || line.len() > MAX_LINE {
            continue;
        }
        seen.insert(label);
        lines.push(line);
    }
    if lines.is_empty() {
        return Ok(code.to_string());
    }

    let mut block: Vec<String> = if code.contains(MARK) {
        Vec::new()
    } else {
        vec![String::new(), String::new(), MARK.to_string()]
    };
    block.extend(lines);
    let merged = format!("{}\n{}\n", code.trim_end(), block.join("\n"));
    // one line that fails against the reference itself poisons the block, so
    // the whole pass is dropped rather than a guess being cached
    Ok(if run(&merged).0 {
        merged
    } else {
        code.to_string()
    })
}

pub fn has_extra(code: &str) -> bool {
    code.contains(MARK)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn proposals_keep_parsable_labelled_lines() {
        let text = "```python\nsol.f(1)  # one item\nassert x == 1  # skipped\nsol.f(lambda: 1)  # a lambda\nsol.f(  # no label\nsol.f(2),  # two items!\n```";
        assert_eq!(
            proposals(&strip_fences(text)),
            vec![
                ("sol.f(1)".to_string(), "one_item".to_string()),
                ("sol.f(2),".to_string(), "two_items".to_string()),
            ]
        );
    }

    #[test]
    fn covered_reads_the_trailing_labels() {
        let code = "assert f(1) == 2  # smallest\nassert f(2) == 3\nx = 1  # not_an_assert\nassert g() == [1, 2]  # empty_query\n";
        assert_eq!(covered(code), vec!["smallest", "empty_query"]);
    }

    #[test]
    fn literal_eval_shapes() {
        for good in [
            "1",
            "-1.5",
            "'a'",
            "[1, (2, 3)]",
            "{'a': None}",
            "(1+2j)",
            "True",
            "b'x'",
            "{1, 2}",
        ] {
            assert!(is_literal(good), "{good}");
        }
        for bad in [
            "<TreeNode object>",
            "f(1)",
            "inf",
            "nan",
            "[x]",
            "{**a}",
            "1 + 2",
        ] {
            assert!(!is_literal(bad), "{bad}");
        }
    }

    #[test]
    fn extra_asserts_appends_a_marked_block_once() {
        let code = "class S:\n    def f(self, x):\n        return x\n\n\nassert S().f(1) == 1\n";
        let llm = |_: &str| Ok("S().f(0)  # zero\nS().f(2)  # two\nS().f(9)  # nine".to_string());
        let run = |src: &str| {
            let mut out = String::new();
            if src.contains("print('@@'") {
                out.push_str("@@ 0 0\n@@ 1 2\n@@ 2 <object>\n");
            }
            (true, out)
        };
        let merged = extra_asserts(code, &llm, &run).unwrap();
        assert_eq!(
            merged,
            format!(
                "{}\n\n\n{MARK}\nassert S().f(0) == 0  # zero\nassert S().f(2) == 2  # two\n",
                code.trim_end()
            )
        );
        assert!(has_extra(&merged));
        // the second pass hands the labels over and appends under the mark
        let llm2 = |p: &str| {
            assert!(p.contains("- zero\n- two"));
            Ok("S().f(0)  # zero\nS().f(3)  # three".to_string())
        };
        let run2 = |src: &str| {
            let mut out = String::new();
            if src.contains("print('@@'") {
                out.push_str("@@ 0 3\n");
            }
            (true, out)
        };
        let again = extra_asserts(&merged, &llm2, &run2).unwrap();
        assert_eq!(again, format!("{merged}assert S().f(3) == 3  # three\n"));
        // a block the reference rejects is dropped whole
        let failing = |_: &str| (false, String::new());
        assert_eq!(extra_asserts(code, &llm, &failing).unwrap(), code);
    }
}
