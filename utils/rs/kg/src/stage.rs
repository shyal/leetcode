// The three stages of a problem solve (settled 2026-11-12).
//
//   stage 1  the approach, in plain English, in the notes of current.mu
//   stage 2  the pseudocode, as comment lines in the solve
//   stage 3  the code
//
// `make solved` is the gate of each stage (kg_stage). Stages 1 and 2 are
// judged by a model call: a pass opens the next stage, a miss asks what
// to do (try again, a hint, the answer of the stage, stop). Stage 3 is the
// leetcode submit, as before.
//
// The state is in current.mu itself, in the notes under `# ---`, so the
// filed solve carries it and the judge reads it (kg_extract):
//
//   # STAGE 1 of 3 - the approach. ...      the prompt of a stage
//   # STAGE 1: miss (recognition failure)   a miss (the words the judge
//                                           reads as a recognition miss)
//   # HINT: ...                             a hint that was asked for
//   # GIVEN: ...                            the answer of a stage, asked for
//   # ASSIST: hint | walkthrough            the heaviest help so far
//   # STAGE 2: miss (slow)                  a miss of a plan that is correct
//                                           and too slow for the constraints
//   # STAGE 1: pass
//
// The current stage is the highest prompt in the notes. A file with no
// prompt is not staged (a drill, a file served before this, STAGES=0).
// This module is text only; the model calls are in kg_stage.

use crate::data::env_str;

/// STAGES=0 switches the stages off. Unset or any other value: on.
pub fn enabled() -> bool {
    env_str("STAGES").trim() != "0"
}

pub const LAST: u8 = 3;

/// The work a Python solve can do inside LeetCode's time limit: the
/// product of the sizes of the nested loops of a plan, at the largest
/// input the constraints allow, with no division by a constant. A plan
/// above this is slow. Under it: 3713 at 2.6e7 (accepted), a counter made
/// again for each substring of 1781 at 1.25e8. Above it: two loops over
/// 2 * 10^4 items at 4e8, 3960 at 1e9 (a TLE, 2026-11-13).
pub const OPS_LIMIT: f64 = 2e8;

/// A count that the model wrote as text: "26000000", "1,000,000", "1e9",
/// "10^9", or a product of those ("500 * 500 * 26"). Not a count: 0.
fn count(text: &str) -> f64 {
    let one = |t: &str| -> Option<f64> {
        let t = t.trim().replace([',', '_', ' '], "");
        match t.split_once('^') {
            Some((b, e)) => Some(b.parse::<f64>().ok()?.powf(e.parse().ok()?)),
            None => t.parse().ok(),
        }
    };
    text.split(['*', 'x', '×'])
        .map(one)
        .try_fold(1.0, |acc, f| f.map(|f| acc * f))
        .unwrap_or(0.0)
}

/// What the judge of a stage decided. The model says whether the plan is
/// correct and counts its work; the tool decides `slow` from the count.
#[derive(Debug, Clone, PartialEq)]
pub struct Verdict {
    pub correct: bool,
    pub operations: f64,
    pub loops: String,
    pub why: String,
}

impl Verdict {
    /// From the judge's JSON: {"nest": [{"loop", "size"}], "correct",
    /// "why"}. The operations are the product of the sizes. A size can be
    /// a number or a string that holds one (count). No nest: the key
    /// "operations", or 0, and the plan is not slow.
    pub fn read(v: &serde_json::Value) -> Verdict {
        let text = |k: &str| match v.get(k) {
            Some(serde_json::Value::String(s)) => s.clone(),
            Some(serde_json::Value::Null) | None => String::new(),
            Some(other) => other.to_string(),
        };
        let size = |x: &serde_json::Value| match x {
            serde_json::Value::Number(n) => n.as_f64().unwrap_or(0.0),
            serde_json::Value::String(s) => count(s),
            _ => 0.0,
        };
        // the nest of loops: the tool multiplies the sizes
        let nest: Vec<(String, f64)> = v
            .get("nest")
            .and_then(serde_json::Value::as_array)
            .map(|a| {
                a.iter()
                    .map(|e| (e.get("loop").and_then(serde_json::Value::as_str).unwrap_or("").to_string(), e.get("size").map(size).unwrap_or(0.0)))
                    .filter(|(_, n)| *n > 0.0)
                    .collect()
            })
            .unwrap_or_default();
        let operations = if nest.is_empty() {
            v.get("operations").map(size).unwrap_or(0.0)
        } else {
            nest.iter().map(|(_, n)| n).product()
        };
        let loops = if nest.is_empty() {
            text("loops")
        } else {
            nest.iter().map(|(l, n)| format!("{l}: {n}")).collect::<Vec<_>>().join(", ")
        };
        let correct = match v.get("correct") {
            Some(serde_json::Value::Bool(b)) => *b,
            Some(serde_json::Value::String(s)) => s.trim().eq_ignore_ascii_case("true"),
            _ => false,
        };
        Verdict { correct, operations, loops, why: text("why") }
    }

    pub fn slow(&self) -> bool {
        self.operations > OPS_LIMIT
    }

    pub fn valid(&self) -> bool {
        self.correct && !self.slow()
    }
}

/// The prompt line of a stage, without the comment mark.
pub fn prompt(stage: u8) -> String {
    let what = match stage {
        1 => "the approach. Write it in plain English under this line. Then run make solved.",
        2 => "the pseudocode. Write one comment line for each step in the solve below. Then run make solved.",
        _ => "the code. Replace each pseudocode line with code. Then run make solved.",
    };
    format!("STAGE {stage} of {LAST} - {what}")
}

/// The lines of the statement block: the comment lines the file starts
/// with. (count of lines, the lines without the `# ` mark).
fn block(text: &str) -> (usize, Vec<String>) {
    let mut out = Vec::new();
    let mut n = 0;
    for line in text.split('\n') {
        if let Some(rest) = line.strip_prefix('#') {
            out.push(rest.strip_prefix(' ').unwrap_or(rest).trim_end().to_string());
        } else if line.trim().is_empty() && out.is_empty() {
        } else {
            break;
        }
        n += 1;
    }
    (n, out)
}

fn rule(lines: &[String]) -> Option<usize> {
    lines.iter().position(|l| l == "---")
}

/// The statement: the block above the `---` line.
pub fn statement(text: &str) -> String {
    let (_, lines) = block(text);
    let end = rule(&lines).unwrap_or(lines.len());
    lines[..end].join("\n").trim().to_string()
}

fn notes(text: &str) -> Vec<String> {
    let (_, lines) = block(text);
    match rule(&lines) {
        Some(k) => lines[k + 1..].to_vec(),
        None => Vec::new(),
    }
}

/// A line of the notes that this tool or lc_submit wrote.
fn is_record(line: &str) -> bool {
    ["STAGE ", "HINT:", "GIVEN:", "ASSIST:", "LEETCODE:"]
        .iter()
        .any(|p| line.starts_with(p))
}

/// The current stage: the highest prompt in the notes. 0: not staged.
pub fn stage(text: &str) -> u8 {
    (1..=LAST)
        .rev()
        .find(|s| {
            let head = format!("STAGE {s} of {LAST}");
            notes(text).iter().any(|l| l.starts_with(&head))
        })
        .unwrap_or(0)
}

/// The approach: the lines of the notes that the candidate wrote.
pub fn approach(text: &str) -> String {
    notes(text)
        .into_iter()
        .filter(|l| !is_record(l))
        .collect::<Vec<_>>()
        .join("\n")
        .trim()
        .to_string()
}

/// The pseudocode: the comment lines in the solve, with their indentation.
/// The solve is the part between the `# mu` line and the script (the
/// first top-level line that is not a class, a def, a decorator or an
/// import).
pub fn pseudocode(text: &str) -> String {
    let (n, _) = block(text);
    let mut out = Vec::new();
    for line in text.split('\n').skip(n) {
        let t = line.trim_start();
        if t.is_empty() {
            continue;
        }
        let top = t.len() == line.len();
        if let Some(rest) = t.strip_prefix('#') {
            if top && rest.trim_start().starts_with("mu ") {
                continue;
            }
            let indent = &line[..line.len() - t.len()];
            out.push(format!("{indent}{}", rest.trim()));
        } else if top
            && !["class ", "def ", "@", "import ", "from "]
                .iter()
                .any(|p| t.starts_with(p))
        {
            break;
        }
    }
    out.join("\n").trim_end().to_string()
}

/// The hints given so far.
pub fn hints(text: &str) -> Vec<String> {
    notes(text)
        .iter()
        .filter_map(|l| l.strip_prefix("HINT:"))
        .map(|l| l.trim().to_string())
        .collect()
}

fn level(name: &str) -> u8 {
    match name {
        "hint" => 1,
        "walkthrough" => 2,
        "learning" => 3,
        _ => 0,
    }
}

/// The text with `lines` last in its notes. An `ASSIST:` line replaces the
/// one before it when it is heavier, and is dropped when it is not.
pub fn with_notes(text: &str, lines: &[String]) -> String {
    let (n, _) = block(text);
    let all: Vec<&str> = text.split('\n').collect();
    let mut head: Vec<String> = all[..n].iter().map(|l| l.to_string()).collect();
    // the empty comment lines the notes end with are not kept under a record
    while head.last().is_some_and(|l| l.trim() == "#") && head.len() > 1 {
        if head[head.len() - 2].trim() == "# ---" {
            break;
        }
        head.pop();
    }
    for line in lines {
        if let Some(new) = line.strip_prefix("ASSIST:") {
            let old = head
                .iter()
                .filter_map(|l| l.strip_prefix("# ASSIST:"))
                .map(|l| level(l.trim()))
                .max()
                .unwrap_or(0);
            if level(new.trim()) <= old {
                continue;
            }
            head.retain(|l| !l.starts_with("# ASSIST:"));
        }
        for part in line.split('\n') {
            head.push(format!("# {part}").trim_end().to_string());
        }
    }
    let mut out = head.join("\n");
    out.push('\n');
    out.push_str(&all[n..].join("\n"));
    out
}

/// A fresh serve with the prompt of stage 1 under its `---` line, and an
/// empty line to write on. None when the file has no notes rule or is
/// staged already.
pub fn served(text: &str) -> Option<String> {
    if stage(text) != 0 {
        return None;
    }
    let (n, lines) = block(text);
    let k = rule(&lines)?;
    let all: Vec<&str> = text.split('\n').collect();
    // block() skips the blank lines above the block: find the rule's line
    let at = all[..n]
        .iter()
        .enumerate()
        .filter(|(_, l)| l.starts_with('#'))
        .nth(k)?
        .0;
    let mut out: Vec<String> = all[..=at].iter().map(|l| l.to_string()).collect();
    out.push(format!("# {}", prompt(1)));
    out.push("#".to_string());
    out.extend(all[at + 1..].iter().map(|l| l.to_string()));
    Some(out.join("\n"))
}

/// What a miss, a hint, a given answer and a pass write into the notes.
pub fn miss(stage: u8) -> Vec<String> {
    vec![if stage == 1 {
        "STAGE 1: miss (recognition failure)".to_string()
    } else {
        format!("STAGE {stage}: miss")
    }]
}

/// The miss of a plan that is correct and too slow.
pub fn miss_slow(stage: u8) -> Vec<String> {
    vec![if stage == 1 {
        "STAGE 1: miss (recognition failure, slow)".to_string()
    } else {
        format!("STAGE {stage}: miss (slow)")
    }]
}

pub fn hint(text: &str) -> Vec<String> {
    vec![
        format!("HINT: {}", text.trim().replace('\n', " ")),
        "ASSIST: hint".to_string(),
    ]
}

pub fn given(stage: u8, text: &str) -> Vec<String> {
    let mut out = vec![format!("STAGE {stage}: given")];
    out.extend(text.trim_end().lines().map(|l| format!("GIVEN: {l}")));
    out.push("ASSIST: walkthrough".to_string());
    out.push(prompt(stage + 1));
    out
}

pub fn pass(stage: u8) -> Vec<String> {
    vec![format!("STAGE {stage}: pass"), prompt(stage + 1)]
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::data::{notes_assist_level, reset_test_env, test_env};
    use crate::recog::notes_say_missed;

    const SERVE: &str = "# URL: https://leetcode.com/problems/x/\n#\n# 3016. Minimum Number of Pushes to Type Word II\n#\n# Return the minimum number of pushes.\n#\n# ---\n\n# mu 0.17\n\nclass Solution\n  def minimumPushes(word: str) -> int\n    pass\n\nsol = Solution()\n\n# assert sol.minimumPushes('abcde') == 5\n";

    fn staged() -> String {
        served(SERVE).unwrap()
    }

    #[test]
    fn a_serve_opens_stage_1() {
        let s = staged();
        assert_eq!(stage(SERVE), 0);
        assert_eq!(stage(&s), 1);
        assert!(s.contains("# ---\n# STAGE 1 of 3 - the approach."));
        assert!(s.ends_with(&SERVE[SERVE.find("\n# mu").unwrap()..]));
        assert_eq!(statement(&s), statement(SERVE));
        assert_eq!(served(&s), None);
        assert_eq!(served("class Solution\n  pass\n"), None);
    }

    #[test]
    fn the_approach_is_his_lines_only() {
        let s = staged().replace(
            "make solved.\n#\n",
            "make solved.\n# Take the counts.\n# Map the most frequent letters first.\n#\n",
        );
        assert_eq!(
            approach(&s),
            "Take the counts.\nMap the most frequent letters first."
        );
        assert_eq!(approach(&staged()), "");
        let s = with_notes(&s, &miss(1));
        let s = with_notes(&s, &hint("Count each letter."));
        assert_eq!(
            approach(&s),
            "Take the counts.\nMap the most frequent letters first."
        );
        assert_eq!(hints(&s), vec!["Count each letter."]);
    }

    #[test]
    fn a_pass_opens_the_next_stage() {
        let s = with_notes(&staged(), &pass(1));
        assert_eq!(stage(&s), 2);
        let s = with_notes(&s, &pass(2));
        assert_eq!(stage(&s), 3);
        // the code is not moved
        assert!(s.contains("\n\n# mu 0.17\n\nclass Solution\n"));
        assert!(s.ends_with("== 5\n"));
    }

    #[test]
    fn the_pseudocode_is_the_comments_in_the_solve() {
        let s = staged().replace(
            "    pass\n",
            "    # count each letter\n    # for each count, most frequent first\n      # add count * key position\n    pass\n",
        );
        assert_eq!(
            pseudocode(&s),
            "    count each letter\n    for each count, most frequent first\n      add count * key position"
        );
        // the commented asserts of the script are not pseudocode
        assert_eq!(pseudocode(&staged()), "");
    }

    #[test]
    fn the_records_say_what_the_judge_reads() {
        reset_test_env();
        let prompts: String = (1..=LAST).map(prompt).collect::<Vec<_>>().join("\n");
        assert_eq!(notes_assist_level(&prompts), "none");
        assert!(!notes_say_missed(&prompts));
        assert!(notes_say_missed(&miss(1).join("\n")));
        assert!(!notes_say_missed(&miss(2).join("\n")));
        assert_eq!(notes_assist_level(&pass(1).join("\n")), "none");
        assert_eq!(notes_assist_level(&hint("x").join("\n")), "hint");
        assert_eq!(notes_assist_level(&given(1, "x").join("\n")), "walkthrough");
    }

    #[test]
    fn the_heaviest_assist_is_the_one_line() {
        let s = with_notes(&staged(), &hint("a"));
        let s = with_notes(&s, &given(1, "line one\nline two"));
        let s = with_notes(&s, &hint("b"));
        assert_eq!(s.matches("# ASSIST:").count(), 1);
        assert!(s.contains("# ASSIST: walkthrough"));
        assert!(s.contains("# GIVEN: line one\n# GIVEN: line two\n"));
        assert_eq!(stage(&s), 2);
    }

    #[test]
    fn the_switch() {
        reset_test_env();
        assert!(enabled());
        test_env("STAGES", "0");
        assert!(!enabled());
        reset_test_env();
    }

    #[test]
    fn the_tool_decides_slow_from_the_count() {
        let v = |j: serde_json::Value| Verdict::read(&j);
        // correct and inside the limit: a pass
        let ok = v(serde_json::json!({"loops": "i: 1000, j: 1000", "operations": 1000000, "correct": true, "why": "x"}));
        assert!(ok.valid() && !ok.slow());
        // correct and above the limit: a miss, slow
        let slow = v(serde_json::json!({"operations": 1e9, "correct": true}));
        assert!(!slow.valid() && slow.slow());
        // the limit itself is not slow
        assert!(v(serde_json::json!({"operations": OPS_LIMIT, "correct": true})).valid());
        assert!(!v(serde_json::json!({"operations": OPS_LIMIT + 1.0, "correct": true})).valid());
        // wrong and fast: a miss that is not slow
        let wrong = v(serde_json::json!({"operations": 10, "correct": false}));
        assert!(!wrong.valid() && !wrong.slow());
        // a count written as a string, a huge count
        assert!(v(serde_json::json!({"operations": "1,000,000,000", "correct": true})).slow());
        assert!(v(serde_json::json!({"operations": "3.5e13", "correct": "true"})).slow());
        assert!(v(serde_json::json!({"operations": 1e30, "correct": true})).slow());
        assert!(v(serde_json::json!({"operations": "1000 * 1000 * 1000", "correct": true})).slow());
        assert!(v(serde_json::json!({"operations": "500 * 500 * 26", "correct": true})).valid());
        assert!(v(serde_json::json!({"operations": "10^9", "correct": true})).slow());
        assert_eq!(count("26000000"), 26000000.0);
        assert_eq!(count("about a million"), 0.0);
        // the tool multiplies the nest
        let nest = v(serde_json::json!({"nest": [{"loop": "start", "size": 1000}, {"loop": "end", "size": 1000}, {"loop": "values of the counter", "size": "1000"}], "correct": true}));
        assert_eq!(nest.operations, 1e9);
        assert!(nest.slow() && !nest.valid());
        assert_eq!(nest.loops, "start: 1000, end: 1000, values of the counter: 1000");
        let nest = v(serde_json::json!({"nest": [{"loop": "start", "size": 500}, {"loop": "end", "size": 500}, {"loop": "counts", "size": 26}], "correct": true}));
        assert_eq!(nest.operations, 6500000.0);
        assert!(nest.valid());
        assert!(v(serde_json::json!({"nest": [], "correct": true})).valid());
        // no count, no verdict: not slow, not valid
        assert!(v(serde_json::json!({"correct": true})).valid());
        assert!(!v(serde_json::json!({"operations": 5})).valid());
        // the notes of a slow miss
        assert!(notes_say_missed(&miss_slow(1).join("\n")));
        assert!(!notes_say_missed(&miss_slow(2).join("\n")));
        assert_eq!(notes_assist_level(&miss_slow(2).join("\n")), "none");
        let s = with_notes(&staged(), &miss_slow(1));
        assert_eq!(stage(&s), 1);
        assert_eq!(approach(&s), "");
    }
}
