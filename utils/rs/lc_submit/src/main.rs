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
// Login: the cookie file LC_COOKIE_FILE (default ~/.leetcode_cookies.json)
// holding {"LEETCODE_SESSION": ..., "csrftoken": ...}; `make lc-login`
// writes it from a browser (misc/lc_cookies.mjs).
//
// What is submitted: see strip.rs.

use std::path::{Path, PathBuf};
use std::time::Duration;

use kg::console::Console;
use serde_json::{json, Value};

mod strip;

const UA: &str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36";
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

fn cookie_file() -> PathBuf {
    if let Ok(p) = std::env::var("LC_COOKIE_FILE") {
        return PathBuf::from(p);
    }
    let home = std::env::var("HOME").unwrap_or_default();
    Path::new(&home).join(".leetcode_cookies.json")
}

struct Login {
    cookie: String,
    csrf: String,
}

fn login() -> Option<Login> {
    let jar = kg::pyjson::load(&cookie_file())?;
    let session = jar.get("LEETCODE_SESSION")?.as_str()?.to_string();
    let csrf = jar.get("csrftoken")?.as_str()?.to_string();
    Some(Login {
        cookie: format!("LEETCODE_SESSION={session}; csrftoken={csrf}"),
        csrf,
    })
}

fn question_id(slug: &str) -> String {
    let mut resp = ureq::post("https://leetcode.com/graphql/")
        .header("Content-Type", "application/json")
        .header("User-Agent", UA)
        .send_json(json!({"query": QUESTION_QUERY, "variables": {"slug": slug}}))
        .unwrap_or_else(|e| die(&format!("graphql: {e}")));
    let data: Value = resp
        .body_mut()
        .read_json()
        .unwrap_or_else(|e| die(&format!("graphql: {e}")));
    match data["data"]["question"]["questionId"].as_str() {
        Some(id) => id.to_string(),
        None => die(&format!("leetcode knows no problem with slug {slug}")),
    }
}

/// One POST; a 429 (leetcode allows a submission every few seconds) is
/// waited out and retried a few times.
fn submit(login: &Login, slug: &str, qid: &str, code: &str) -> Result<u64, String> {
    let mut wait = 5;
    loop {
        match submit_once(login, slug, qid, code) {
            Err(ureq::Error::StatusCode(429)) if wait <= 40 => {
                eprintln!("leetcode is rate limiting; retrying in {wait}s");
                std::thread::sleep(Duration::from_secs(wait));
                wait *= 2;
            }
            Err(ureq::Error::StatusCode(403)) => {
                return Err("leetcode refused the login (403): run make lc-login".to_string())
            }
            Err(e) => return Err(format!("submit: {e}")),
            Ok(id) => return Ok(id),
        }
    }
}

fn submit_once(login: &Login, slug: &str, qid: &str, code: &str) -> Result<u64, ureq::Error> {
    let url = format!("https://leetcode.com/problems/{slug}/submit/");
    let mut resp = ureq::post(&url)
        .header("Content-Type", "application/json")
        .header("User-Agent", UA)
        .header("Cookie", &login.cookie)
        .header("x-csrftoken", &login.csrf)
        .header("Referer", &format!("https://leetcode.com/problems/{slug}/"))
        .header("Origin", "https://leetcode.com")
        .send_json(json!({"lang": "python3", "question_id": qid, "typed_code": code}))?;
    let data: Value = resp.body_mut().read_json()?;
    data["submission_id"]
        .as_u64()
        .ok_or_else(|| ureq::Error::BadUri(format!("no submission_id in {data}")))
}

/// Poll until the judge is done; returns the check payload.
fn wait_verdict(login: &Login, id: u64) -> Result<Value, String> {
    let url = format!("https://leetcode.com/submissions/detail/{id}/check/");
    for _ in 0..90 {
        std::thread::sleep(Duration::from_secs(1));
        let mut resp = ureq::get(&url)
            .header("User-Agent", UA)
            .header("Cookie", &login.cookie)
            .header("Referer", "https://leetcode.com/")
            .call()
            .map_err(|e| format!("check: {e}"))?;
        let data: Value = resp
            .body_mut()
            .read_json()
            .map_err(|e| format!("check: {e}"))?;
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
    let Some(login) = login() else {
        if auto {
            return;
        }
        die(&format!(
            "no login: {} is missing (make lc-login)",
            cookie_file().display()
        ));
    };

    let outcome = (|| {
        let qid = question_id(&slug);
        let id = submit(&login, &slug, &qid, &class)?;
        console.print(&format!(
            "[dim]submitted {slug} as {id}; waiting for leetcode...[/dim]"
        ));
        wait_verdict(&login, id)
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
