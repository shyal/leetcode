// lc_submit - submit the solution in current.py to leetcode and record the
// verdict in the file's notes, so the judge sees what leetcode saw (a brute
// force that passes the file's small asserts still TLEs on the real tests;
// 2542 on 2026-09-14 was judged clean that way).
//
//   lc_submit                 # submit current.py, write "LEETCODE: <verdict>" into its notes
//   lc_submit --file F        # another file
//   lc_submit --auto          # the `make solved` step: silently skip a drill (no URL
//                             # line) or a missing browser, and say so when the notes
//                             # mark a learning rep; exit 1 when leetcode's verdict
//                             # is anything but Accepted, so the make stops
//   lc_submit --auto --force  # record the verdict and exit 0 whatever it is
//                             # (`make solved FORCE=1`)
//   lc_submit --show          # print the code that would be submitted and stop
//   lc_submit --check F...    # print "F: <names>" for every file whose submission
//                             # uses a name leetcode lacks; exit 1 if any (the corpus test)
//
// Transport: every request to leetcode runs inside the browser at
// LC_CDP_ENDPOINT (kg::lc, misc/lc_fetch.mjs), the one that carries the
// browser's login and passes Cloudflare.
//
// What is submitted: see strip.rs.

use std::time::Duration;

use kg::console::Console;
use kg::lc::{ensure_browser, fetch, json_of, no_browser, slug_of};
use serde_json::{json, Value};

mod strip;

const QUESTION_QUERY: &str =
    "query q($slug: String!) { question(titleSlug: $slug) { questionId } }";

fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(1)
}

fn question_id(slug: &str) -> Result<String, String> {
    let (_, body) = fetch(
        "POST",
        "/graphql/",
        Some(&json!({"query": QUESTION_QUERY, "variables": {"slug": slug}})),
    )?;
    match json_of(&body)?["data"]["question"]["questionId"].as_str() {
        Some(id) => Ok(id.to_string()),
        None => Err(format!("leetcode knows no problem with slug {slug}")),
    }
}

/// One POST; a 429 (leetcode allows a submission every few seconds) is
/// waited out and retried a few times.
fn submit(slug: &str, qid: &str, code: &str) -> Result<u64, String> {
    let mut wait = 5;
    loop {
        let (status, body) = fetch(
            "POST",
            &format!("/problems/{slug}/submit/"),
            Some(&json!({"lang": "python3", "question_id": qid, "typed_code": code})),
        )?;
        match status {
            429 if wait <= 40 => {
                eprintln!("leetcode is rate limiting; retrying in {wait}s");
                std::thread::sleep(Duration::from_secs(wait));
                wait *= 2;
            }
            403 => {
                return Err(
                    "leetcode refused the submission (403): is the browser logged in?".into(),
                )
            }
            200 => {
                return json_of(&body)?["submission_id"]
                    .as_u64()
                    .ok_or_else(|| format!("no submission_id in {body:.200}"))
            }
            _ => return Err(format!("submit: http {status}")),
        }
    }
}

/// Polls, one a second, before the wait gives up on the judge.
const POLLS: usize = 90;
/// Polls in a row that may fail before the wait gives up: the tab reloads,
/// or the browser drops one request ("Failed to fetch" on 2026-10-27, and
/// the one failed poll lost a Wrong Answer: the solve was filed without it).
const POLL_FAILURES: usize = 5;

/// Poll `once` until it returns the finished check payload. An error is
/// retried unless POLL_FAILURES of them came in a row.
fn poll_verdict(mut once: impl FnMut() -> Result<Value, String>) -> Result<Value, String> {
    let mut failures = 0;
    for _ in 0..POLLS {
        match once() {
            Ok(data) if data["state"].as_str() == Some("SUCCESS") => return Ok(data),
            Ok(_) => failures = 0,
            Err(e) => {
                failures += 1;
                if failures == POLL_FAILURES {
                    return Err(e);
                }
            }
        }
    }
    Err(format!("leetcode did not finish judging in {POLLS}s"))
}

/// Poll until the judge is done; returns the check payload.
fn wait_verdict(id: u64) -> Result<Value, String> {
    let path = format!("/submissions/detail/{id}/check/");
    poll_verdict(|| {
        std::thread::sleep(Duration::from_secs(1));
        let (_, body) = fetch("GET", &path, None)?;
        json_of(&body)
    })
    .map_err(|e| format!("check of submission {id}: {e}"))
}

/// One line for the notes and the screen: the status, then what qualifies it.
fn verdict_line(v: &Value) -> String {
    let status = v["status_msg"].as_str().unwrap_or("unknown");
    let s = |k: &str| v[k].as_str().unwrap_or("").to_string();
    let detail = match status {
        "Accepted" => format!("{}, {}", s("status_runtime"), s("status_memory")),
        "Compile Error" => s("compile_error"),
        "Runtime Error" => s("runtime_error"),
        _ => format!(
            "{}/{} cases",
            v["total_correct"].as_u64().unwrap_or(0),
            v["total_testcases"].as_u64().unwrap_or(0)
        ),
    };
    let detail = detail.trim().replace('\n', " ");
    if detail.is_empty() {
        status.to_string()
    } else {
        format!("{status} ({detail})")
    }
}

/// Put `LEETCODE: <line>` into the module docstring's notes (below the
/// `---` rule, added when missing), replacing an earlier LEETCODE line.
fn record(code: &str, line: &str) -> String {
    let Some(open) = code.find("\"\"\"") else {
        return format!("{code}\n# LEETCODE: {line}\n");
    };
    let Some(close_rel) = code[open + 3..].find("\"\"\"") else {
        return format!("{code}\n# LEETCODE: {line}\n");
    };
    let close = open + 3 + close_rel;
    let doc = &code[open + 3..close];
    let mut kept: Vec<&str> = doc
        .lines()
        .filter(|l| !l.trim_start().starts_with("LEETCODE:"))
        .collect();
    while kept.last().is_some_and(|l| l.trim().is_empty()) {
        kept.pop();
    }
    let mut body = kept.join("\n");
    if !body.contains("\n---") && !body.starts_with("---") {
        body.push_str("\n\n---");
    }
    body.push_str(&format!("\n\nLEETCODE: {line}\n"));
    format!("{}{}{}", &code[..open + 3], body, &code[close..])
}

/// Every file whose submission would hit a NameError on leetcode, with the
/// names; 0 when none.
fn check(files: &[String]) -> i32 {
    let root = kg::data::repo_root();
    let mut bad = 0;
    for f in files {
        let Ok(code) = std::fs::read_to_string(f) else {
            continue;
        };
        let Some(sub) = strip::strip(&root, &code) else {
            continue;
        };
        let missing = strip::undefined_names(&root, &sub);
        if !missing.is_empty() {
            bad += 1;
            println!("{f}: {}", missing.into_iter().collect::<Vec<_>>().join(" "));
        }
    }
    i32::from(bad > 0)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "--help" || a == "-h") {
        println!("usage: lc_submit [--file F] [--auto [--force]] [--show] | --check F...");
        return;
    }
    if args.first().is_some_and(|a| a == "--check") {
        std::process::exit(check(&args[1..]));
    }
    let auto = args.iter().any(|a| a == "--auto");
    let force = args.iter().any(|a| a == "--force");
    let show = args.iter().any(|a| a == "--show");
    let file = args
        .iter()
        .position(|a| a == "--file")
        .and_then(|i| args.get(i + 1))
        .cloned()
        .unwrap_or_else(|| "current.py".into());
    let console = Console::full_width();

    let code = match std::fs::read_to_string(&file) {
        Ok(c) => c,
        Err(_) if auto => return,
        Err(e) => die(&format!("{file}: {e}")),
    };
    let Some(slug) = slug_of(&code) else {
        if auto {
            return; // a drill: nothing to submit
        }
        die(&format!(
            "{file}: no `URL: https://leetcode.com/problems/<slug>/` line"
        ));
    };
    if auto && learning_solve(&code) {
        console.print(
            "[yellow]leetcode submit skipped: the notes mark a learning rep, and only \
             his own solves go on his leetcode record[/yellow]",
        );
        return;
    }
    let Some(class) = strip::strip(&kg::data::repo_root(), &code) else {
        if auto {
            return;
        }
        die(&format!("{file}: no top-level class to submit"));
    };
    if show {
        print!("{class}");
        return;
    }
    let missing = strip::undefined_names(&kg::data::repo_root(), &class);
    if !missing.is_empty() {
        let names = missing.into_iter().collect::<Vec<_>>().join(", ");
        let msg = format!(
            "{file}: the class calls {names}, which leetcode does not have; take it out first"
        );
        if auto {
            console.print(&format!("[yellow]leetcode submit skipped: {msg}[/yellow]"));
            return;
        }
        die(&msg);
    }
    if auto && no_browser() {
        return; // no browser to submit through: make solved goes on without a verdict
    }

    let outcome = (|| {
        ensure_browser()?;
        let qid = question_id(&slug)?;
        let id = submit(&slug, &qid, &class)?;
        console.print(&format!(
            "[dim]submitted {slug} as {id}; waiting for leetcode...[/dim]"
        ));
        wait_verdict(id)
    })();
    let verdict = match outcome {
        Ok(v) => v,
        Err(e) if auto => {
            console.print(&format!("[yellow]leetcode submit skipped: {e}[/yellow]"));
            return;
        }
        Err(e) => die(&e),
    };
    let line = verdict_line(&verdict);
    let colour = if rejected(&line) { "red" } else { "green" };
    console.print(&format!("[{colour}]LEETCODE: {line}[/{colour}]"));
    if line.starts_with("Wrong Answer") {
        let s = |k: &str| verdict[k].as_str().unwrap_or("").trim().replace('\n', " ");
        console.print(&format!(
            "[dim]input {}\nexpected {}\ngot {}[/dim]",
            s("last_testcase"),
            s("expected_output"),
            s("code_output")
        ));
    }
    std::fs::write(&file, record(&code, &line)).unwrap_or_else(|e| die(&format!("{file}: {e}")));
    if auto && !force && rejected(&line) {
        console.print(
            "[red]leetcode did not accept this solution, so it is not filed. Fix it and run \
             `make solved` again, or `make solved FORCE=1` to file it as it is.[/red]",
        );
        std::process::exit(1);
    }
}

/// True when leetcode's verdict line is anything but Accepted: the gate
/// `make solved` stops on.
fn rejected(line: &str) -> bool {
    !line.starts_with("Accepted")
}

/// The notes under the rule mark the solve as a learning rep, the word
/// `learning` in plain prose (kg::data::notes_assist_level): a solution he
/// looked up and copied. `make solved` keeps it off his leetcode record, so
/// the problems leetcode shows as solved are the ones he solved (2026-10-27).
/// The statement above the rule is not read, so a problem about learning
/// rates is submitted as usual.
fn learning_solve(code: &str) -> bool {
    kg::data::notes_assist_level(&kg::pysrc::notes_of(code)) == "learning"
}

#[cfg(test)]
mod tests {
    use super::*;

    const FILE: &str = "\"\"\"\nURL: https://leetcode.com/problems/two-sum/description/?envType=x\n\n1. Two Sum\n\nGiven nums, return.\n\n---\n\nmy notes\n\"\"\"\n\n\nclass Solution:\n    def twoSum(self, nums):\n        return [0, 1]\n\n\nclass Solution:\n    def twoSum(self, nums):\n        # final\n        return [1, 0]\n\n\nsol = Solution()\n\nassert sol.twoSum([1]) == [1, 0]\n";

    #[test]
    fn only_accepted_passes_the_gate() {
        assert!(!rejected("Accepted (85 ms, 30.1 MB)"));
        assert!(rejected("Time Limit Exceeded (34/58 cases)"));
        assert!(rejected("Wrong Answer (3/58 cases)"));
        assert!(rejected("Runtime Error"));
    }

    #[test]
    fn a_learning_rep_is_not_submitted() {
        assert!(!learning_solve(FILE));
        let copied = FILE.replace("my notes", "learning rep, copied the solution");
        assert!(learning_solve(&copied));
        let statement = FILE.replace("Given nums, return.", "Given a learning rate, return.");
        assert!(!learning_solve(&statement));
    }

    #[test]
    fn poll_rides_out_a_few_failed_requests() {
        let mut calls = 0;
        let got = poll_verdict(|| {
            calls += 1;
            match calls {
                1 => Ok(json!({"state": "PENDING"})),
                2 | 3 => Err("Failed to fetch".into()),
                _ => Ok(json!({"state": "SUCCESS", "status_msg": "Accepted"})),
            }
        });
        assert_eq!(got.unwrap()["status_msg"], "Accepted");
        assert_eq!(calls, 4);
    }

    #[test]
    fn poll_gives_up_after_failures_in_a_row() {
        let mut calls = 0;
        let got = poll_verdict(|| {
            calls += 1;
            Err("Failed to fetch".into())
        });
        assert_eq!(got.unwrap_err(), "Failed to fetch");
        assert_eq!(calls, POLL_FAILURES);
    }

    #[test]
    fn slug_from_url_line() {
        assert_eq!(slug_of(FILE).as_deref(), Some("two-sum"));
        assert_eq!(
            slug_of("URL: https://leetcode.com/problems/max-score/\n").as_deref(),
            Some("max-score")
        );
        assert_eq!(slug_of("DRILL: Something\n"), None);
    }

    #[test]
    fn verdict_lines() {
        let ok = json!({"status_msg": "Accepted", "status_runtime": "85 ms", "status_memory": "30.1 MB"});
        assert_eq!(verdict_line(&ok), "Accepted (85 ms, 30.1 MB)");
        let tle = json!({"status_msg": "Time Limit Exceeded", "total_correct": 34, "total_testcases": 58});
        assert_eq!(verdict_line(&tle), "Time Limit Exceeded (34/58 cases)");
    }

    #[test]
    fn record_goes_under_the_rule_once() {
        let once = record(FILE, "Time Limit Exceeded (34/58 cases)");
        assert!(once.contains("my notes\n\nLEETCODE: Time Limit Exceeded (34/58 cases)\n\"\"\""));
        let twice = record(&once, "Accepted (85 ms, 30.1 MB)");
        assert_eq!(twice.matches("LEETCODE:").count(), 1);
        assert!(twice.contains("LEETCODE: Accepted"));
        assert_eq!(
            kg::pysrc::notes_of(&twice).trim_end(),
            "notes: \n\nmy notes\n\nLEETCODE: Accepted (85 ms, 30.1 MB)"
        );
        let no_rule = record(
            "\"\"\"\nURL: x\n\nstatement\n\"\"\"\n\nclass Solution:\n    pass\n",
            "Accepted",
        );
        assert!(no_rule.contains("statement\n\n---\n\nLEETCODE: Accepted\n\"\"\""));
    }
}
