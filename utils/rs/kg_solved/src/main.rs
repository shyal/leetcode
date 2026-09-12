// kg_solved - file a finished attempt, then commit it: `make solved`.
//
// Two phases, so a Ctrl-C anywhere in `make solved` loses nothing
// (settled 2026-08-28, after an interrupt cut the judge off mid-ingest):
//
//   kg_solved            file phase: freeze the solve time NOW, archive
//                        current.py into solved/, clear it, park the
//                        frozen commit message in .solve_meta.json
//                        (untracked, gitignored). No git.
//   kg_extract --stub    placeholder evidence for the filed solve, no
//                        model call (a spot rep is judged here, in line:
//                        its walk is revealed after the judge)
//   kg_solved --commit   commit phase: ONE commit carrying the solve and
//                        the placeholder, with the frozen solve time in
//                        the message; then the squash-merge to master;
//                        then the judge is spawned DETACHED on the filed
//                        file (kg::git::spawn_judge). SIGINT-immune - it
//                        is about a second of git.
//
// The judge (kg_extract --file F --commit) lands its own commit when it is
// done, on whatever is checked out then (settled 2026-09-06; before, every
// `make solved` waited a median 38s for it). Interrupted anywhere: re-run
// `make solved`. The file phase sees the meta and skips itself, the stub
// skips an entry already present, the commit phase picks up the meta and
// finishes. A placeholder still pending is respawned by `make next`.
//
// Ported from utils/kg/solved (Python) on 2026-09-12. Paths are relative
// to the working directory, as they were: make runs from the repo root.

use std::path::Path;
use std::process::Command;

use chrono::{DateTime, Utc};
use kg::console::{Console, Text};
use kg::data::{load_evidence_recs, repo_root};
use kg::git::{active_seconds, spawn_judge};
use kg::recog;
use kg::table::panel_expanded;
use regex::Regex;
use serde_json::{json, Value};

const META: &str = ".solve_meta.json";

/// (problem id or "drill", title, content) from current.py's first docstring.
fn parse_current(path: &str) -> Option<(String, String, String)> {
    let content = std::fs::read_to_string(path).ok()?;
    let block = Regex::new(r#"(?s)"""(.*?)""""#).unwrap();
    let doc = block
        .captures(&content)?
        .get(1)?
        .as_str()
        .trim()
        .to_string();
    let lines: Vec<&str> = doc.split('\n').collect();
    let drill = Regex::new(r"^DRILL:\s*(.+)").unwrap();
    let prob = Regex::new(r"^(\d+[a-zA-Z]?)\.\s*(.+)").unwrap();
    for line in &lines {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if let Some(m) = drill.captures(line) {
            return Some(("drill".to_string(), m[1].trim().to_string(), content));
        }
        if let Some(m) = prob.captures(line) {
            return Some((m[1].trim().to_string(), m[2].trim().to_string(), content));
        }
    }
    // not in the first lines: the line after a url
    for (i, line) in lines.iter().enumerate() {
        if line.trim().starts_with("https://") {
            if let Some(next) = lines.get(i + 1) {
                if let Some(m) = prob.captures(next.trim()) {
                    return Some((m[1].trim().to_string(), m[2].trim().to_string(), content));
                }
            }
        }
    }
    None
}

/// re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")
fn clean_title(title: &str) -> String {
    title
        .chars()
        .filter(|c| c.is_alphanumeric() || *c == '_' || c.is_whitespace() || *c == '-')
        .collect::<String>()
        .trim()
        .replace(' ', "_")
}

/// solved/ filename for a finished attempt. Stamped in UTC on purpose - the
/// same clock as git - and anything that needs the calendar day converts
/// with kg_lib.manila_date_from_filename rather than reading the digits.
fn solved_filename(problem_id: &str, title: &str, failed: bool, now: DateTime<Utc>) -> String {
    // datetime.isoformat(): the microseconds only when they are not zero
    let iso = if now.timestamp_subsec_micros() == 0 {
        now.format("%Y-%m-%dT%H:%M:%S+00:00").to_string()
    } else {
        now.format("%Y-%m-%dT%H:%M:%S%.6f+00:00").to_string()
    };
    let sanitized: String = format!("{iso}Z")
        .chars()
        .map(|c| {
            if c.is_alphanumeric() || c == '_' {
                c
            } else {
                '_'
            }
        })
        .collect();
    let marker = if failed { "_FAILED" } else { "" };
    let prefix = if problem_id == "drill" {
        "d".to_string()
    } else {
        format!("p{problem_id}")
    };
    format!("{prefix}_{}{marker}_{sanitized}.py", clean_title(title))
}

fn read_nonempty(path: &str) -> bool {
    std::fs::read_to_string(path).is_ok_and(|s| !s.trim().is_empty())
}

/// A recognition rep is on the branch: current.md has content (and
/// current.py does not). `make solved` files it under recognition/ instead
/// of solved/; the judge (kg_extract) scores it after this phase.
fn spot_pending() -> bool {
    read_nonempty("current.md") && !read_nonempty("current.py")
}

fn git_branch() -> String {
    Command::new("git")
        .args(["rev-parse", "--abbrev-ref", "HEAD"])
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default()
}

/// The spot rep's file phase: reveal nothing yet, archive current.md as
/// recognition/s<num>_<title>_<ts>.md with the pick and the clock in a
/// footer comment the judge reads, clear current.md.
fn spot_file_phase(
    console: &Console,
    root: &Path,
    failed: bool,
    solve_time: &str,
    slept_line: &str,
) {
    let branch = git_branch();
    let metas = recog::load_spot_meta(root);
    let Some(meta) = metas.get(&branch).filter(|m| m.is_object()) else {
        console.print(&format!(
            "[red]no pick recorded for branch {branch} (.spot.json) - cannot file this spot rep.[/red]"
        ));
        return;
    };
    let pnum = kg::data::value_str(&meta["problem"]);
    let title = meta
        .get("title")
        .and_then(Value::as_str)
        .unwrap_or("")
        .to_string();
    if failed {
        console.print(
            "[yellow]a spot rep is not failed, it is answered: write \"don't know\" under the rule and run make solved.[/yellow]",
        );
        return;
    }
    let active = active_seconds(root, "HEAD", now()).0;
    let footer = json!({
        "problem": pnum,
        "target": meta.get("target").cloned().unwrap_or(Value::Null),
        "reason": meta.get("reason").cloned().unwrap_or(Value::Null),
        "seconds": active,
    });
    let content = format!(
        "{}\n\n<!-- spot {} -->\n",
        std::fs::read_to_string("current.md")
            .unwrap_or_default()
            .trim_end(),
        kg::pyjson::dumps(&footer, None)
    );
    let mut filename = solved_filename(&pnum, &title, false, Utc::now());
    filename.truncate(filename.len() - 3);
    filename.push_str(".md");
    // s<num>_ marks a spot rep the way p<num>_ marks a solve
    let filename = format!("s{}", &filename[1..]);
    let _ = std::fs::create_dir_all("recognition");
    let filepath = format!("recognition/{filename}");
    std::fs::write(&filepath, content).expect("write the spot file");
    let message = format!("spot: {pnum}. {title}\n\nsolve time: {solve_time}{slept_line}");
    kg::pyjson::save(
        Path::new(META),
        &json!({"message": message, "file": filepath, "kind": "spot"}),
        None,
    )
    .expect("write .solve_meta.json");
    let _ = std::fs::remove_file("current.md");
    console.print(&format!(
        "[green]filed[/green] [bold]{filepath}[/bold] [cyan]({solve_time})[/cyan]; the walk is revealed after the judge."
    ));
}

fn now() -> i64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs() as i64)
        .unwrap_or(0)
}

/// Freeze the clock and archive the attempt. No git.
fn file_phase(console: &Console, root: &Path, failed: bool) {
    if Path::new(META).exists() {
        // a stage whose file is gone is a leftover, not a resume: `make drop`
        // git-cleans the filed solve but spares the gitignored META, and the
        // 2026-09-02 run committed the NEXT solve under the dropped one's
        // message because of it. Discard and file the current attempt fresh.
        let staged = kg::pyjson::load(Path::new(META)).unwrap_or_else(|| json!({}));
        let file = staged.get("file").and_then(Value::as_str).unwrap_or("");
        if file.is_empty() || !Path::new(file).exists() {
            console.print(
                "[red]stale stage: its solve file is gone (dropped?) — discarding it.[/red]",
            );
            let _ = std::fs::remove_file(META);
        } else {
            console.print("[yellow]a filed solve is already staged — resuming its ingest and commit.[/yellow]");
            return;
        }
    }

    // the clock stops when the operator runs `make solved`, not when the
    // judge finishes minutes later: active time is computed here and frozen
    // into the message the commit phase will use. Active time only: awake
    // intervals on the branch, the sleeping:/woke: marker commits (make
    // sleep / make wake) subtracted out.
    let (active, slept_seconds, sleeps) = active_seconds(root, "HEAD", now());
    let solve_time = format!("{}m {}s", active / 60, active % 60);
    let slept_line = if sleeps > 0 {
        format!(
            "\nslept: {}h {:02}m over {sleeps} park(s)",
            slept_seconds / 60 / 60,
            slept_seconds / 60 % 60
        )
    } else {
        String::new()
    };

    if spot_pending() {
        spot_file_phase(console, root, failed, &solve_time, &slept_line);
        return;
    }
    if !Path::new("current.py").exists() {
        console.print("[red]current.py does not exist. Exiting.[/red]");
        return;
    }
    if !read_nonempty("current.py") {
        console.print("[red]current.py is empty — nothing to file.[/red]");
        return;
    }
    let Some((problem_id, title, mut content)) = parse_current("current.py") else {
        console.print("[red]Could not parse problem id and title from current.py. Exiting.[/red]");
        return;
    };
    let filename = solved_filename(&problem_id, &title, failed, Utc::now());
    if failed {
        content.push_str(&format!(
            "\n\n# FAILED: walked away after {solve_time}; no working solution.\n# Judge the moves actually attempted as struggled, not clean.\n"
        ));
    }
    let _ = std::fs::create_dir_all("./solved");
    let filepath = format!("./solved/{filename}");
    std::fs::write(&filepath, &content).expect("write the solve file");

    let mut message = if problem_id == "drill" {
        format!("drill: {title}\n\nsolve time: {solve_time}{slept_line}")
    } else {
        format!("{problem_id}. {title}\n\nsolve time: {solve_time}{slept_line}")
    };
    if failed {
        message = format!("failed: {message}");
    }
    // the meta is written BEFORE current.py is cleared: a kill between the
    // two re-runs into the staged branch above instead of filing twice
    kg::pyjson::save(
        Path::new(META),
        &json!({"message": message, "file": filepath}),
        None,
    )
    .expect("write .solve_meta.json");
    std::fs::write("current.py", "").expect("clear current.py");
    console.print(&format!(
        "[green]filed[/green] [bold]{filepath}[/bold] [cyan]({solve_time})[/cyan]; the commit lands after the judge."
    ));
}

fn git(console: &Console, what: &str, args: &[&str]) -> bool {
    let status = Command::new("git").args(args).status();
    if status.as_ref().is_ok_and(|s| s.success()) {
        return true;
    }
    // subprocess.CalledProcessError's text, as the Python printed it
    let code = status.ok().and_then(|s| s.code()).unwrap_or(1);
    console.print(&format!(
        "[red]Error {what}: Command '['git', {}]' returned non-zero exit status {code}.[/red]",
        args.iter()
            .map(|a| format!("'{a}'"))
            .collect::<Vec<_>>()
            .join(", ")
    ));
    false
}

/// ONE commit: the solve, its evidence, the refit curve - with the frozen
/// solve time in the message - then the squash-merge to master.
fn commit_phase(console: &Console, root: &Path) {
    let Some(meta) = kg::pyjson::load(Path::new(META)) else {
        console.print("[yellow]nothing staged — no commit to make.[/yellow]");
        return;
    };
    let message = meta["message"].as_str().unwrap_or("").to_string();
    if !git(console, "running git add", &["add", "."]) {
        return;
    }
    if !git(console, "running git commit", &["commit", "-m", &message]) {
        return;
    }
    let branch = git_branch();
    if branch == "master" {
        let _ = std::fs::remove_file(META);
        finish(console, root, &meta);
        return;
    }
    if !git(
        console,
        "checking out master",
        &["checkout", "-q", "master"],
    ) {
        return;
    }
    if !git(
        console,
        "squash merging",
        &["merge", "-q", "--squash", &branch],
    ) {
        return;
    }
    if !git(
        console,
        "committing squash merge",
        &["commit", "-m", &message],
    ) {
        return;
    }
    if !git(console, "deleting branch", &["branch", "-q", "-D", &branch]) {
        return;
    }
    let _ = std::fs::remove_file(META);
    finish(console, root, &meta);
    // the Claude Code pane follows the branch: a fresh conversation on master
    let chat = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join("kg_chat")))
        .unwrap_or_else(|| root.join("utils/rs/target/release/kg_chat"));
    let _ = Command::new(chat).arg("--switch").status();
}

fn print_panel(console: &Console, text: &str, title: &str) {
    let body: Vec<kg::console::Line> = text
        .split('\n')
        .map(|l| Text::plain(l).segments())
        .collect();
    console.print_lines(panel_expanded(&body, title, console.width));
}

/// The last thing `make solved` prints. A spot rep: the judge's reveal. A
/// solve: its placeholder is committed, so the judge is spawned detached
/// here; its account of the solve lands in its own commit's body.
fn finish(console: &Console, root: &Path, meta: &Value) {
    let message = meta["message"].as_str().unwrap_or("");
    console.print(&format!(
        "[green]✓ committed[/green] [bold]{}[/bold]",
        message.lines().next().unwrap_or("")
    ));
    let file = meta.get("file").and_then(Value::as_str).unwrap_or("");
    let key = file.strip_prefix("./").unwrap_or(file).to_string();
    if meta.get("kind").and_then(Value::as_str) == Some("spot") {
        if let Some(rec) = recog::load_recognition_raw(root).get(&key) {
            print_panel(console, &recog::reveal(rec), "the rep");
        }
        return;
    }
    let recs = load_evidence_recs(root);
    let Some((_, rec)) = recs.iter().find(|(f, _)| *f == key) else {
        return;
    };
    if rec.pending.as_deref().is_some_and(|p| !p.is_empty()) {
        spawn_judge(root, &key);
        console.print(
            "[dim]judge running in the background; it commits when done (.judge.log).[/dim]",
        );
    } else if let Some(summary) = kg::pyjson::load(&root.join("graph/evidence.json"))
        .and_then(|v| v["evidence"][&key]["summary"].as_str().map(String::from))
        .filter(|s| !s.is_empty())
    {
        print_panel(console, &summary, "the solve");
    }
}

fn main() {
    // SIGINT off for both phases (children inherit it, so git is covered):
    // each phase is a second of work, and the interruptible waiting happens
    // between them, where a re-run of `make solved` resumes cleanly.
    // SAFETY: installing SIG_IGN has no preconditions
    unsafe {
        libc::signal(libc::SIGINT, libc::SIG_IGN);
    }
    let args: Vec<String> = std::env::args().skip(1).collect();
    let failed = args.iter().any(|a| a == "--failed");
    let commit = args.iter().any(|a| a == "--commit");
    let root = repo_root();
    let console = Console::full_width();
    if commit {
        commit_phase(&console, &root);
    } else {
        file_phase(&console, &root, failed);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn filenames() {
        let f = solved_filename("1004", "Max Consecutive Ones III", false, Utc::now());
        assert!(f.starts_with("p1004_Max_Consecutive_Ones_III_20"), "{f}");
        assert!(f.ends_with("Z.py"));
        assert!(f
            .chars()
            .all(|c| c.is_alphanumeric() || c == '_' || c == '.'));
        let d = solved_filename("drill", "Paid Orders Per Customer", true, Utc::now());
        assert!(d.starts_with("d_Paid_Orders_Per_Customer_FAILED_"), "{d}");
        assert_eq!(clean_title("It's a (test) - ok!"), "Its_a_test_-_ok");
    }

    fn utc(y: i32, mo: u32, d: u32, h: u32, mi: u32, s: u32, micro: u32) -> DateTime<Utc> {
        chrono::NaiveDate::from_ymd_opt(y, mo, d)
            .unwrap()
            .and_hms_micro_opt(h, mi, s, micro)
            .unwrap()
            .and_utc()
    }

    /// The UTC stamp round-trips to the Manila day (utils/tests/test_kg_dates
    /// pinned these before the port).
    #[test]
    fn roundtrip_across_midnight() {
        let name = solved_filename(
            "drill",
            "Number Scanner",
            false,
            utc(2026, 8, 23, 19, 44, 54, 884512),
        );
        assert_eq!(
            name,
            "d_Number_Scanner_2026_08_23T19_44_54_884512_00_00Z.py"
        );
        assert_eq!(
            kg::data::manila_date_from_filename(&name).as_deref(),
            Some("2026-08-24")
        );
    }

    #[test]
    fn roundtrip_daytime() {
        let name = solved_filename(
            "560",
            "Subarray Sum Equals K",
            false,
            utc(2026, 8, 23, 9, 5, 0, 0),
        );
        assert!(
            name.starts_with("p560_Subarray_Sum_Equals_K_2026_08_23T09_05_00"),
            "{name}"
        );
        assert_eq!(
            kg::data::manila_date_from_filename(&name).as_deref(),
            Some("2026-08-23")
        );
    }

    #[test]
    fn failed_marker_survives_roundtrip() {
        let name = solved_filename(
            "227",
            "Basic Calculator II",
            true,
            utc(2026, 8, 23, 23, 59, 59, 0),
        );
        assert!(name.contains("_FAILED_"));
        assert_eq!(
            kg::data::manila_date_from_filename(&name).as_deref(),
            Some("2026-08-24")
        );
        assert_eq!(
            kg::data::manila_date_from_filename("drill@2026-07-05-monotonic-stack"),
            None
        );
        assert_eq!(
            kg::data::manila_date_from_filename(
                "p88_Merge_Sorted_Array_2025_10_01T21_36_57_880900.py"
            )
            .as_deref(),
            Some("2025-10-02")
        );
    }
}
