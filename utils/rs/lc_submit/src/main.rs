// lc_submit - submit the solution in current.py to leetcode and record the
// verdict in the file's notes, so the judge sees what leetcode saw (a brute
// force that passes the file's small asserts still TLEs on the real tests;
// 2542 on 2026-09-14 was judged clean that way).
//
//   lc_submit                 # submit current.py, write "LEETCODE: <verdict>" into its notes
//   lc_submit --file F        # another file
//   lc_submit --auto          # the `make solved` step: silently skip a drill (no URL
//                             # line) or a missing cookie file; never fail the make
//   lc_submit --show          # print the code that would be submitted and stop
//   lc_submit --check F...    # print "F: <names>" for every file whose submission
//                             # uses a name leetcode lacks; exit 1 if any (the corpus test)
//
// Transport: every request to leetcode runs inside the browser at
// LC_CDP_ENDPOINT (misc/lc_fetch.mjs), so it carries the browser's login and
// passes Cloudflare; a copied cookie does not (the WAF 403s "(a or b) or
// (c or d)" from anything but a real browser, 2026-09-17).
//
// What is submitted: see strip.rs.

use std::io::Write;
use std::process::{Command, Stdio};
use std::time::Duration;

use kg::console::Console;
use serde_json::{json, Value};

mod strip;

const QUESTION_QUERY: &str =
    "query q($slug: String!) { question(titleSlug: $slug) { questionId } }";

fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(1)
}

/// The problem slug from the file's `URL: https://leetcode.com/problems/<slug>/...` line.
fn slug_of(code: &str) -> Option<String> {
    let line = code.lines().find(|l| l.trim_start().starts_with("URL:"))?;
    let rest = line.split("/problems/").nth(1)?;
    let slug = rest.split(['/', '?']).next()?;
    (!slug.is_empty()).then(|| slug.to_string())
}

fn no_browser() -> bool {
    std::env::var("LC_CDP_ENDPOINT").map_or(true, |v| v.is_empty())
}

/// One request to leetcode.com through the browser: (status, body).
fn fetch(method: &str, path: &str, body: Option<&Value>) -> Result<(u16, String), String> {
    if no_browser() {
        return Err("no browser: set LC_CDP_ENDPOINT to its devtools endpoint".into());
    }
    let script = kg::data::repo_root().join("misc/lc_fetch.mjs");
    let mut child = Command::new("node")
        .arg(script)
        .arg(method)
        .arg(path)
        .stdin(if body.is_some() {
            Stdio::piped()
        } else {
            Stdio::null()
        })
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("node: {e}"))?;
    if let Some(b) = body {
        let mut stdin = child.stdin.take().ok_or("node: no stdin")?;
        stdin
            .write_all(b.to_string().as_bytes())
            .map_err(|e| format!("node: {e}"))?;
    }
    let out = child.wait_with_output().map_err(|e| format!("node: {e}"))?;
    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).trim().to_string());
    }
    let text = String::from_utf8_lossy(&out.stdout).into_owned();
    let (status, rest) = text.split_once('\n').unwrap_or((&text, ""));
    let status = status
        .parse()
        .map_err(|_| format!("lc_fetch: no status in {text:?}"))?;
    Ok((status, rest.to_string()))
}

fn json_of(body: &str) -> Result<Value, String> {
    serde_json::from_str(body).map_err(|_| format!("leetcode sent no json: {body:.200}"))
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

/// Poll until the judge is done; returns the check payload.
fn wait_verdict(id: u64) -> Result<Value, String> {
    let path = format!("/submissions/detail/{id}/check/");
    for _ in 0..90 {
        std::thread::sleep(Duration::from_secs(1));
        let (_, body) = fetch("GET", &path, None)?;
        let data = json_of(&body).map_err(|e| format!("check: {e}"))?;
        if data["state"].as_str() == Some("SUCCESS") {
            return Ok(data);
        }
    }
    Err("check: leetcode did not finish judging in 90s".into())
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
        println!("usage: lc_submit [--file F] [--auto] [--show] | --check F...");
        return;
    }
    if args.first().is_some_and(|a| a == "--check") {
        std::process::exit(check(&args[1..]));
    }
    let auto = args.iter().any(|a| a == "--auto");
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
    let colour = if line.starts_with("Accepted") {
        "green"
    } else {
        "red"
    };
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
}

#[cfg(test)]
mod tests {
    use super::*;

    const FILE: &str = "\"\"\"\nURL: https://leetcode.com/problems/two-sum/description/?envType=x\n\n1. Two Sum\n\nGiven nums, return.\n\n---\n\nmy notes\n\"\"\"\n\n\nclass Solution:\n    def twoSum(self, nums):\n        return [0, 1]\n\n\nclass Solution:\n    def twoSum(self, nums):\n        # final\n        return [1, 0]\n\n\nsol = Solution()\n\nassert sol.twoSum([1]) == [1, 0]\n";

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
