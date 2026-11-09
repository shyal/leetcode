//! A Wrong Answer becomes an assert: the input leetcode failed on and the
//! output it expected, as one line `assert sol.<method>(<input>) == <expected>`.
//!
//! The method and the type of each parameter come from leetcode's metaData
//! for the problem. A TreeNode parameter is built with build_tree, a ListNode
//! with build_linked_list; a TreeNode answer is read with get_level_order, a
//! ListNode answer with get_list_values; a double answer is compared within
//! 1e-5, as leetcode compares it. A design problem, a void method (the
//! answer is the changed argument), a parameter of another node type, or an
//! input line leetcode adds that the signature does not have (141's `pos`)
//! gets no assert, and the reason is printed.
//!
//! The reference solution in .prepare_cache/<num>.json runs with the line
//! added first. When it fails the line, leetcode accepts more than one
//! answer and `==` cannot test it, so no file changes. When it passes, the
//! line joins the cached solution and its stub (commented there, as the
//! other asserts are), and the file that was submitted: current.mu through
//! `mu/session.py assert`, or current.py.

use std::path::Path;
use std::process::Command;
use std::time::Duration;

use prepare::stub::strip_solution;
use prepare::{cache_entry, pyrun, write_entry};
use serde_json::Value;

/// A line longer than this is a workload, not a case for the file.
const MAX_LINE: usize = 2000;

/// A json literal as a Python literal: true, false and null become True,
/// False and None outside strings, and a comma or a colon gets one space
/// after it, as the served asserts are written. The digits are copied as
/// they are, so a big integer keeps all of them.
pub fn py_literal(json: &str) -> String {
    let mut out = String::new();
    let mut word = String::new();
    let (mut in_str, mut escaped) = (false, false);
    let flush = |word: &mut String, out: &mut String| {
        out.push_str(match word.as_str() {
            "true" => "True",
            "false" => "False",
            "null" => "None",
            w => w,
        });
        word.clear();
    };
    for c in json.trim().chars() {
        if in_str {
            out.push(c);
            if escaped {
                escaped = false;
            } else if c == '\\' {
                escaped = true;
            } else if c == '"' {
                in_str = false;
            }
            continue;
        }
        if c.is_ascii_alphabetic() {
            word.push(c);
            continue;
        }
        flush(&mut word, &mut out);
        match c {
            '"' => {
                in_str = true;
                out.push(c);
            }
            ',' | ':' => {
                out.push(c);
                out.push(' ');
            }
            c if c.is_whitespace() => {}
            c => out.push(c),
        }
    }
    flush(&mut word, &mut out);
    out
}

/// The argument for one parameter of leetcode type `ty`, or None when the
/// type has no builder here.
fn argument(ty: &str, json: &str) -> Option<String> {
    let lit = py_literal(json);
    match ty {
        "TreeNode" => Some(format!("build_tree({lit})")),
        "ListNode" => Some(format!("build_linked_list({lit})")),
        "ListNode[]" => {
            let lists: Vec<Value> = serde_json::from_str(json).ok()?;
            let built: Vec<String> = lists
                .iter()
                .map(|l| format!("build_linked_list({})", py_literal(&l.to_string())))
                .collect();
            Some(format!("[{}]", built.join(", ")))
        }
        t if t.contains("Node") => None,
        _ => Some(lit),
    }
}

/// The assert line for a Wrong Answer, or why there is none.
pub fn assert_line(meta: &Value, input: &str, expected: &str) -> Result<String, String> {
    if meta.get("classname").is_some() || meta["systemdesign"].as_bool() == Some(true) {
        return Err("a design problem is a sequence of calls, not one".into());
    }
    let method = meta["name"]
        .as_str()
        .ok_or("leetcode's metaData names no method")?;
    let params = meta["params"].as_array().cloned().unwrap_or_default();
    let ret = meta["return"]["type"].as_str().unwrap_or("");
    if ret == "void" {
        return Err(format!(
            "{method} returns nothing; the answer is the changed argument"
        ));
    }
    let lines: Vec<&str> = input.lines().filter(|l| !l.trim().is_empty()).collect();
    if lines.len() != params.len() {
        return Err(format!(
            "the input has {} lines and {method} has {} parameters",
            lines.len(),
            params.len()
        ));
    }
    let mut args = Vec::new();
    for (p, json) in params.iter().zip(&lines) {
        let ty = p["type"].as_str().unwrap_or("");
        serde_json::from_str::<Value>(json)
            .map_err(|_| format!("the input line {json} is not json"))?;
        args.push(argument(ty, json).ok_or_else(|| format!("no builder for a {ty} argument"))?);
    }
    serde_json::from_str::<Value>(expected)
        .map_err(|_| format!("the expected output {expected} is not json"))?;
    let call = format!("sol.{method}({})", args.join(", "));
    let want = py_literal(expected);
    let line = match ret {
        "TreeNode" => format!("assert get_level_order({call}) == {want}"),
        "ListNode" => format!("assert get_list_values({call}) == {want}"),
        "double" => format!("assert abs({call} - {want}) < 1e-5"),
        t if t.contains("Node") => return Err(format!("no reader for a {t} answer")),
        _ => format!("assert {call} == {want}"),
    };
    if line.len() > MAX_LINE {
        return Err(format!(
            "the line is {} characters, more than {MAX_LINE}",
            line.len()
        ));
    }
    Ok(line)
}

/// `text` with `line` added after its last line (commented when `comment`),
/// unchanged when it has the line already.
pub fn with_assert(text: &str, line: &str, comment: bool) -> String {
    if text
        .lines()
        .any(|l| l.trim_start_matches(['#', ' ']).trim_end() == line)
    {
        return text.to_string();
    }
    let mut out = text.trim_end_matches('\n').to_string();
    out.push('\n');
    if comment {
        out.push_str("# ");
    }
    out.push_str(line);
    out.push('\n');
    out
}

/// The problem number on the statement's title line (`287. Find ...`).
pub fn number_of(code: &str) -> Option<String> {
    code.lines().take(20).find_map(|l| {
        let (n, rest) = l.trim().split_once(". ")?;
        (!n.is_empty() && n.chars().all(|c| c.is_ascii_digit()) && !rest.is_empty())
            .then(|| n.to_string())
    })
}

/// Put the assert for this Wrong Answer in the cache and in the submitted
/// file. Ok is what was done, Err why nothing was.
pub fn fold(
    root: &Path,
    file: &str,
    code: &str,
    meta: &Value,
    input: &str,
    expected: &str,
) -> Result<String, String> {
    let line = assert_line(meta, input, expected)?;
    let mut touched = Vec::new();
    if let Some(num) = number_of(code) {
        if let Some(mut entry) = cache_entry(root, &num) {
            let solution = entry["solution"].as_str().unwrap_or("").to_string();
            if !solution.is_empty() {
                let merged = with_assert(&solution, &line, false);
                if merged != solution {
                    let out = pyrun::run(root, &merged, Duration::from_secs(60));
                    if !out.ok {
                        return Err(
                            "the reference solution fails it too, so leetcode accepts more \
                             than one answer here"
                                .into(),
                        );
                    }
                    entry["code"] = Value::String(strip_solution(&merged)?);
                    entry["solution"] = Value::String(merged);
                    write_entry(root, &num, &entry);
                }
                touched.push(format!(".prepare_cache/{num}.json"));
            }
        }
    }
    if Path::new(file)
        .file_name()
        .is_some_and(|n| n == ".mu_current.py")
    {
        let out = Command::new(root.join(".venv/bin/python3"))
            .args(["mu/session.py", "assert", &line])
            .current_dir(root)
            .output()
            .map_err(|e| format!("mu/session.py assert: {e}"))?;
        if !out.status.success() {
            return Err(format!(
                "mu/session.py assert: {}",
                String::from_utf8_lossy(&out.stderr).trim()
            ));
        }
        touched.push("current.mu".into());
    } else {
        let text = std::fs::read_to_string(file).map_err(|e| format!("{file}: {e}"))?;
        std::fs::write(file, with_assert(&text, &line, false))
            .map_err(|e| format!("{file}: {e}"))?;
        touched.push(file.to_string());
    }
    Ok(format!(
        "the failed case is an assert in {}",
        touched.join(" and ")
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn json_becomes_python() {
        assert_eq!(py_literal("[2,5,9]"), "[2, 5, 9]");
        assert_eq!(
            py_literal(r#"[1,null,true,"a,b:null\"x"]"#),
            r#"[1, None, True, "a,b:null\"x"]"#
        );
        assert_eq!(
            py_literal("123456789012345678901234567890"),
            "123456789012345678901234567890"
        );
    }

    #[test]
    fn a_plain_call() {
        let meta = json!({"name": "findDuplicate", "params": [{"name": "nums", "type": "integer[]"}], "return": {"type": "integer"}});
        assert_eq!(
            assert_line(&meta, "[1,3,4,2,2]", "2").unwrap(),
            "assert sol.findDuplicate([1, 3, 4, 2, 2]) == 2"
        );
    }

    #[test]
    fn nodes_are_built_and_read() {
        let meta = json!({"name": "f", "params": [{"name": "root", "type": "TreeNode"}, {"name": "k", "type": "integer"}], "return": {"type": "ListNode"}});
        assert_eq!(
            assert_line(&meta, "[1,null,2]\n3", "[2,1]").unwrap(),
            "assert get_list_values(sol.f(build_tree([1, None, 2]), 3)) == [2, 1]"
        );
        let meta = json!({"name": "m", "params": [{"name": "lists", "type": "ListNode[]"}], "return": {"type": "double"}});
        assert_eq!(
            assert_line(&meta, "[[1,2],[]]", "1.5").unwrap(),
            "assert abs(sol.m([build_linked_list([1, 2]), build_linked_list([])]) - 1.5) < 1e-5"
        );
    }

    #[test]
    fn no_assert_without_one_call() {
        let design = json!({"classname": "LRUCache", "methods": []});
        assert!(assert_line(&design, "[]\n[]", "[]").is_err());
        let void = json!({"name": "f", "params": [{"name": "a", "type": "integer[]"}], "return": {"type": "void"}});
        assert!(assert_line(&void, "[1]", "[1]").is_err());
        let pos = json!({"name": "hasCycle", "params": [{"name": "head", "type": "ListNode"}], "return": {"type": "boolean"}});
        assert!(assert_line(&pos, "[3,2,0]\n1", "true").is_err());
    }

    #[test]
    fn the_line_joins_once() {
        let line = "assert sol.f(1) == 2";
        let once = with_assert("x = 1\n", line, true);
        assert_eq!(once, "x = 1\n# assert sol.f(1) == 2\n");
        assert_eq!(with_assert(&once, line, false), once);
    }

    #[test]
    fn number_from_the_title_line() {
        assert_eq!(
            number_of("\"\"\"\nURL: https://x\n\n287. Find the Duplicate Number\n").as_deref(),
            Some("287")
        );
    }
}
