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
//
// Login: the cookie file LC_COOKIE_FILE (default ~/.leetcode_cookies.json)
// holding {"LEETCODE_SESSION": ..., "csrftoken": ...}; `make lc-login`
// writes it from a browser (misc/lc_cookies.mjs).
//
// What is submitted: the LAST top-level `class Solution` block in the file,
// with every harness helper it uses (cells, nbrs, like, grid_bfs, the
// maxheap functions) pasted above it from HELPER_FILES, transitively. Imports
// are not sent; leetcode preloads the ones the harness mirrors
// (utils/harness/sitecustomize.py).

use std::path::{Path, PathBuf};
use std::time::Duration;

use kg::console::Console;
use serde_json::{json, Value};

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

/// The last top-level `class Solution` block: from its header to the line
/// before the next top-level statement.
fn solution_class(code: &str) -> Option<String> {
    let lines: Vec<&str> = code.lines().collect();
    let start = lines
        .iter()
        .rposition(|l| l.starts_with("class Solution") && l.trim_end().ends_with(':'))?;
    let mut end = lines.len();
    for (i, l) in lines.iter().enumerate().skip(start + 1) {
        let top_level = !l.is_empty() && !l.starts_with([' ', '\t']);
        if top_level && !l.starts_with('#') {
            end = i;
            break;
        }
    }
    Some(lines[start..end].join("\n").trim_end().to_string() + "\n")
}

/// The files whose top-level names a solution may call bare, and which
/// leetcode does not have: each used name is pasted in, with what it needs.
const HELPER_FILES: [&str; 2] = ["utils/harness/grid_utils.py", "dsa/maxheapq.py"];

/// Every top-level `def`, `class` or assignment in a python file, by name:
/// the block runs to the next top-level statement. Imports and the
/// `if __name__` demo are not blocks.
fn top_level_blocks(src: &str) -> Vec<(String, String)> {
    let lines: Vec<&str> = src.lines().collect();
    let name_of = |l: &str| -> Option<String> {
        let head = l.split(['(', ':', '=', ' ']).find(|w| !w.is_empty())?;
        let name = match head {
            "def" | "class" => l[head.len()..]
                .trim_start()
                .split(['(', ':'])
                .next()?
                .trim()
                .to_string(),
            "import" | "from" | "if" | "print" | "@" => return None,
            _ if l.contains('=') || l.contains(':') => head.to_string(),
            _ => return None,
        };
        let ok = name.chars().all(|c| c.is_ascii_alphanumeric() || c == '_');
        (ok && !name.is_empty()).then_some(name)
    };
    let starts: Vec<(usize, String)> = lines
        .iter()
        .enumerate()
        .filter(|(_, l)| !l.is_empty() && !l.starts_with([' ', '\t', '#', '"', ')']))
        .filter_map(|(i, l)| name_of(l).map(|n| (i, n)))
        .collect();
    let mut out = Vec::new();
    for (k, (start, name)) in starts.iter().enumerate() {
        let mut end = starts.get(k + 1).map_or(lines.len(), |(s, _)| *s);
        // an `if __name__` (or any other statement) between two blocks ends the
        // earlier one too; a `)` at column 0 closes a multi-line signature
        for (i, l) in lines
            .iter()
            .enumerate()
            .skip(start + 1)
            .take(end - start - 1)
        {
            if !l.is_empty() && !l.starts_with([' ', '\t', '#', ')']) {
                end = i;
                break;
            }
        }
        let block = lines[*start..end].join("\n").trim_end().to_string();
        out.push((name.clone(), block));
    }
    out
}

/// The block without its docstrings and comments, so a helper named in
/// prose is not pulled in.
fn code_only(block: &str) -> String {
    let mut out = String::new();
    let mut in_doc = false;
    for l in block.lines() {
        let quotes = l.matches("\"\"\"").count();
        if in_doc {
            in_doc = quotes % 2 == 0;
            continue;
        }
        if quotes % 2 == 1 {
            in_doc = true;
            continue;
        }
        if quotes == 0 {
            out.push_str(l.split('#').next().unwrap_or(""));
            out.push('\n');
        }
    }
    out
}

fn uses(code: &str, name: &str) -> bool {
    let bytes = code.as_bytes();
    let mut from = 0;
    while let Some(pos) = code[from..].find(name) {
        let i = from + pos;
        let j = i + name.len();
        let word = |b: u8| b.is_ascii_alphanumeric() || b == b'_';
        let before = i > 0 && word(bytes[i - 1]);
        let after = j < bytes.len() && word(bytes[j]);
        if !before && !after {
            return true;
        }
        from = j;
    }
    false
}

/// The blocks `class_src` needs, dependencies first: harness helpers, then
/// the file's own top-level definitions (a State class, a helper function)
/// other than the Solution classes themselves.
fn expand_helpers(root: &Path, file_src: &str, class_src: &str) -> String {
    let mut blocks: Vec<(String, String)> = Vec::new();
    for f in HELPER_FILES {
        if let Ok(src) = std::fs::read_to_string(root.join(f)) {
            blocks.extend(top_level_blocks(&src));
        }
    }
    blocks.extend(
        top_level_blocks(file_src)
            .into_iter()
            .filter(|(name, block)| {
                // assignments in a solve are test setup (root = build_tree(...))
                name != "Solution" && (block.starts_with("def ") || block.starts_with("class "))
            }),
    );
    let mut needed = vec![false; blocks.len()];
    let mut frontier: Vec<usize> = (0..blocks.len())
        .filter(|&i| !blocks[i].0.starts_with('_') && uses(class_src, &blocks[i].0))
        .collect();
    while let Some(i) = frontier.pop() {
        if needed[i] {
            continue;
        }
        needed[i] = true;
        for (j, (name, _)) in blocks.iter().enumerate() {
            if j != i && !needed[j] && uses(&code_only(&blocks[i].1), name) {
                frontier.push(j);
            }
        }
    }
    blocks
        .iter()
        .zip(&needed)
        .filter(|(_, &n)| n)
        .map(|((_, b), _)| format!("{b}\n\n\n"))
        .collect()
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

fn submit(login: &Login, slug: &str, qid: &str, code: &str) -> Result<u64, String> {
    let url = format!("https://leetcode.com/problems/{slug}/submit/");
    let mut resp = ureq::post(&url)
        .header("Content-Type", "application/json")
        .header("User-Agent", UA)
        .header("Cookie", &login.cookie)
        .header("x-csrftoken", &login.csrf)
        .header("Referer", &format!("https://leetcode.com/problems/{slug}/"))
        .header("Origin", "https://leetcode.com")
        .send_json(json!({"lang": "python3", "question_id": qid, "typed_code": code}))
        .map_err(|e| match e {
            ureq::Error::StatusCode(403) => {
                "leetcode refused the login (403): run make lc-login".to_string()
            }
            e => format!("submit: {e}"),
        })?;
    let data: Value = resp
        .body_mut()
        .read_json()
        .map_err(|e| format!("submit: {e}"))?;
    data["submission_id"]
        .as_u64()
        .ok_or_else(|| format!("submit: no submission_id in {data}"))
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

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "--help" || a == "-h") {
        println!("usage: lc_submit [--file F] [--auto] [--show]");
        return;
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
    let Some(class) = solution_class(&code) else {
        if auto {
            return;
        }
        die(&format!("{file}: no top-level `class Solution:`"));
    };
    let class = format!(
        "{}{class}",
        expand_helpers(&kg::data::repo_root(), &code, &class)
    );
    if show {
        print!("{class}");
        return;
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
    fn last_class_only() {
        let c = solution_class(FILE).unwrap();
        assert!(c.starts_with("class Solution:\n    def twoSum"));
        assert!(c.contains("# final"));
        assert!(!c.contains("[0, 1]"));
        assert!(!c.contains("sol = Solution()"));
        assert!(c.ends_with("return [1, 0]\n"));
    }

    #[test]
    fn helpers_expand_transitively() {
        let root = kg::data::repo_root();
        let plain = expand_helpers(
            &root,
            "",
            "class Solution:\n    def f(self):\n        return 1\n",
        );
        assert_eq!(plain, "");
        let grid = expand_helpers(
            &root,
            "",
            "class Solution:\n    def f(self, grid):\n        return like(grid)\n",
        );
        assert!(grid.starts_with("def like("), "{grid}");
        assert!(!grid.contains("def nbrs("));
        let bfs = expand_helpers(
            &root,
            "",
            "class Solution:\n    def f(self, g):\n        return grid_bfs(g, [(0, 0)])\n",
        );
        let at = |s: &str| {
            bfs.find(s)
                .unwrap_or_else(|| panic!("{s} missing in:\n{bfs}"))
        };
        assert!(at("CARDINALS") < at("def nbrs(") && at("def nbrs(") < at("def grid_bfs("));
        assert!(at("def like(") < at("def grid_bfs("));
        assert!(!bfs.contains("def cells("), "named only in a docstring");
        assert!(!bfs.contains("import "));
        let heap = expand_helpers(
            &root,
            "",
            "class Solution:\n    def f(self, h):\n        maxheappush(h, 1)\n",
        );
        assert!(heap.contains("class _Rev:") && heap.contains("def maxheappush("));
        assert!(!heap.contains("def maxheappop("));
        assert!(!heap.contains("__name__"));
    }

    #[test]
    fn own_definitions_come_along() {
        let file = "\"\"\"\nURL: x\n\"\"\"\n\nclass State:\n    A = 1\n\n\ndef unused():\n    pass\n\n\nroot = build_tree([1])\n\n\nclass Solution:\n    def f(self, root):\n        return State.A\n\n\nsol = Solution()\n";
        let class = solution_class(file).unwrap();
        let pre = expand_helpers(&kg::data::repo_root(), file, &class);
        assert_eq!(pre, "class State:\n    A = 1\n\n\n");
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
