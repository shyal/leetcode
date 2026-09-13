// kg_extract - populate graph/evidence.json (and problems.json) from solved/
// files: the judge.
//
// For each solve file not already in evidence.json: ONE small claude call
// (taxonomy + that file's code - no history) extracting which moves the
// actual code exercised, with verdicts. Incremental and resumable: results
// are written back after every file, so interrupting is always safe.
//
//   kg_extract --limit 5          # trial run on the 5 newest unprocessed
//   kg_extract                    # process everything unprocessed
//   kg_extract --model sonnet     # default is haiku (cheap/fast)
//   kg_extract --stub             # placeholder entry for the staged solve (no model call)
//   kg_extract --file F --commit  # the detached judge: judge F, fold, refit, commit
//   kg_extract --pending          # also re-judge every placeholder still pending
//   kg_extract --followup-of F    # the statement's follow-up question (the tests)
//   kg_extract --strip F          # the prompt body of a file (the tests)
//
// The judge queue (settled 2026-09-06): `make solved` writes the placeholder
// and commits at once; the judge runs detached and lands its own commit on
// whatever branch is checked out when it finishes, then folds that commit
// into the solve's own commit and rewrites every branch cut from it
// (fold_into); a pushed solve keeps the "judge:" commit on top instead.
//
// Ported from utils/kg/kg_extract (Python) on 2026-09-12. The candidate's
// notes come from kg::pysrc, a docstring reader in place of Python's ast; a
// file that does not parse as Python but starts with a docstring keeps its
// notes here where the Python dropped them.

use std::collections::HashSet;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::sync::mpsc;
use std::time::{Duration, Instant};

use chrono::{DateTime, Utc};
use indexmap::IndexMap;
use kg::bank::unlocks;
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{
    apply_assist_floor, harness_env_note, load_envrc, manila_date_from_filename, normalise_assist,
    notes_assist_level, repo_root, DrillMap, Rec,
};
use kg::evidence::Evidence;
use kg::llm::claude_json;
use kg::pyjson;
use kg::pysrc::{module_docstring, notes_of};
use kg::recog;
use kg::status::{all_statuses, node_status, SOLID};
use regex::Regex;
use serde_json::{json, Map, Value};

const RUN_TIMEOUT: u64 = 30;
const GRAPH_FILES: [&str; 5] = [
    "graph/evidence.json",
    "graph/problems.json",
    "graph/recognition.json",
    "graph/curve.json",
    "graph/solvecost.json",
];
const FOLLOWUP_VERDICTS: [&str; 2] = ["solved", "not solved"];

fn basename(path: &str) -> &str {
    path.rsplit('/').next().unwrap_or(path)
}

/// Drop the leading problem statement, keep the code AND the candidate's
/// notes (below the `---` rule in the docstring), then the raw body.
pub fn strip_statement(code: &str) -> String {
    let body = Regex::new(r#"(?s)^""".*?"""\s*"#)
        .unwrap()
        .replace(code, "")
        .into_owned();
    let notes = notes_of(code);
    if notes.trim().is_empty() {
        body
    } else {
        format!("{notes}\n\n{body}")
    }
}

/// The follow-up question in the problem statement, or "". Only the
/// statement is read (the docstring above the `---` rule), never the notes.
pub fn followup_of(code: &str) -> String {
    let doc = match module_docstring(code) {
        Some(d) => d,
        None => {
            // the Python fell back to a plain regex on a file that does not parse
            let m = Regex::new(r#"(?s)^\s*"""(.*?)""""#).unwrap();
            match m.captures(code) {
                Some(c) => c[1].to_string(),
                None => return String::new(),
            }
        }
    };
    if doc.is_empty() {
        return String::new();
    }
    let statement = doc.split("---").next().unwrap_or("");
    let re = Regex::new(r"(?im)^\s*\**follow[ -]?up\**:?\**\s*(.*)$").unwrap();
    let Some(m) = re.captures(statement) else {
        return String::new();
    };
    let rest = format!("{}{}", &m[1], &statement[m.get(0).unwrap().end()..]);
    let first = rest.trim().split("\n\n").next().unwrap_or("").to_string();
    first.split_whitespace().collect::<Vec<_>>().join(" ")
}

/// Execute a solve file the way the candidate does: (status, detail).
fn run_solve(root: &Path, path: &str) -> (String, String) {
    let py = root.join(".venv/bin/python3");
    let py = if py.exists() {
        py
    } else {
        PathBuf::from("python3")
    };
    let pythonpath = format!(
        "{}:{}:{}:{}",
        root.display(),
        root.join("utils").display(),
        root.join("utils/harness").display(),
        std::env::var("PYTHONPATH").unwrap_or_default()
    );
    let abs = if Path::new(path).is_absolute() {
        PathBuf::from(path)
    } else {
        root.join(path)
    };
    let child = Command::new(py)
        .arg(&abs)
        .current_dir(root)
        .env("PYTHONPATH", pythonpath)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn();
    let mut child = match child {
        Ok(c) => c,
        Err(e) => {
            return (
                "unknown".into(),
                format!(
                    "could not execute: {}",
                    e.to_string().chars().take(200).collect::<String>()
                ),
            )
        }
    };
    let mut out_pipe = child.stdout.take().unwrap();
    let mut err_pipe = child.stderr.take().unwrap();
    let out_t = std::thread::spawn(move || {
        let mut s = String::new();
        let _ = std::io::Read::read_to_string(&mut out_pipe, &mut s);
        s
    });
    let err_t = std::thread::spawn(move || {
        let mut s = String::new();
        let _ = std::io::Read::read_to_string(&mut err_pipe, &mut s);
        s
    });
    let start = Instant::now();
    let status = loop {
        if let Ok(Some(st)) = child.try_wait() {
            break Some(st);
        }
        if start.elapsed() > Duration::from_secs(RUN_TIMEOUT) {
            let _ = child.kill();
            let _ = child.wait();
            break None;
        }
        std::thread::sleep(Duration::from_millis(50));
    };
    let stdout = out_t.join().unwrap_or_default();
    let stderr = err_t.join().unwrap_or_default();
    let tail = |s: &str, n: usize| -> String {
        let t = s.trim();
        let chars: Vec<char> = t.chars().collect();
        chars[chars.len().saturating_sub(n)..].iter().collect()
    };
    match status {
        None => (
            "timeout".into(),
            format!("exceeded {RUN_TIMEOUT}s — likely TLE or an infinite loop"),
        ),
        Some(st) if st.success() => ("passed".into(), tail(&stdout, 600)),
        Some(_) => (
            "failed".into(),
            tail(
                if stderr.trim().is_empty() {
                    &stdout
                } else {
                    &stderr
                },
                800,
            ),
        ),
    }
}

/// One authoritative paragraph about the run, for the judge's prompt.
fn runtime_note(status: &str, detail: &str) -> String {
    match status {
        "passed" => format!(
            "RUNTIME RESULT (authoritative): the file was EXECUTED and exited 0 — every active assertion passed and no exception was raised. The solution WORKS. Do NOT report bugs, failing assertions, or undefined names; if you think you see one, you have misread the code. Note that `assert f(x) is False` PASSES when f(x) returns False — a negative expectation is not a failure. Judge only WHICH technique moves the working code exercises.{}",
            if detail.is_empty() { String::new() } else { format!("\nProgram output:\n{detail}") }
        ),
        "failed" => format!(
            "RUNTIME RESULT (authoritative): the file was EXECUTED and exited NON-ZERO. It genuinely fails. Use the traceback below as the evidence for any 'struggled' verdict, and quote the real error in the note. Attribute the failure to the ONE move the defective line belongs to; the moves that ran correctly around it stay 'clean'.\n{detail}"
        ),
        "timeout" => format!(
            "RUNTIME RESULT (authoritative): the file was EXECUTED and TIMED OUT ({detail}). Treat the move responsible for the complexity blowup as 'struggled'."
        ),
        _ => format!(
            "RUNTIME RESULT: the file could not be executed, so judge statically — but assume the code works unless a bug is unmistakable. ({detail})"
        ),
    }
}

/// Record the walk this solve actually took as an alt walk on the problem,
/// when it routed around a mapped move. True if the entry changed. The walk
/// may legitimately be EMPTY: the map contradicted outright.
pub fn record_alt_walk(
    problems: &mut Map<String, Value>,
    pnum: &str,
    moves: &IndexMap<String, String>,
    skipped: &HashSet<String>,
) -> bool {
    let mut taken: Vec<String> = moves
        .iter()
        .filter(|(_, v)| *v == "clean")
        .map(|(m, _)| m.clone())
        .collect();
    taken.sort();
    let Some(entry) = problems.get_mut(pnum).and_then(Value::as_object_mut) else {
        return false;
    };
    if skipped.is_empty() {
        return false;
    }
    let taken_v = json!(taken);
    let walks = entry.entry("alt_walks").or_insert_with(|| json!([]));
    if walks.as_array().is_some_and(|a| a.contains(&taken_v)) {
        return false;
    }
    walks.as_array_mut().unwrap().push(taken_v);
    true
}

/// A drill is a drill even when its filename lacks the d_ prefix: the
/// DRILL: header is authoritative.
fn is_drill_file(path: &str, code: &str) -> bool {
    basename(path).starts_with("d_") || Regex::new(r"(?m)^\s*\**DRILL:").unwrap().is_match(code)
}

/// The nodes a drill file trains: its DRILL title looked up in drills.json
/// (the "trains" list), a TRAINS header only for an old solved copy whose
/// title the bank no longer carries.
pub fn trains_in(code: &str, drills: &DrillMap) -> Vec<String> {
    if let Some(m) = Regex::new(r"(?m)^\s*\**DRILL:\**\s*(.+?)\s*$")
        .unwrap()
        .captures(code)
    {
        let title = m[1].to_string();
        for entry in drills.values().rev() {
            if entry.title == title {
                if let Some(t) = &entry.trains {
                    return t.clone();
                }
            }
        }
    }
    Regex::new(r"TRAINS:\s*([a-z0-9\-, ]+)")
        .unwrap()
        .captures(code)
        .map(|m| m[1].split(',').map(|t| t.trim().to_string()).collect())
        .unwrap_or_default()
}

fn problem_of_fname(path: &str) -> Option<(String, String)> {
    Regex::new(r"p(\d+)_(.+?)_\d{4}_\d{2}_\d{2}T")
        .unwrap()
        .captures(basename(path))
        .map(|m| (m[1].to_string(), m[2].to_string()))
}

/// The placeholder `make solved` files before the judge runs: the rep,
/// dated, on the moves the file is FOR - a drill's TRAINS, a problem's
/// canonical walk - marked clean; a FAILED file records the rep with no
/// moves at all. Assist read from the level word in the notes.
pub fn stub_entry(
    path: &str,
    code: &str,
    nodes: &HashSet<String>,
    problem_moves: &dyn Fn(&str) -> Vec<String>,
    drills: &DrillMap,
    now: DateTime<Utc>,
) -> Value {
    let is_drill = is_drill_file(path, code);
    let (problem, moves) = if is_drill {
        ("drill".to_string(), trains_in(code, drills))
    } else {
        let p = problem_of_fname(path)
            .map(|(n, _)| n)
            .unwrap_or_else(|| "?".to_string());
        let m = problem_moves(&p);
        (p, m)
    };
    let failed = basename(path).contains("_FAILED_");
    let moves: Vec<String> = if failed {
        vec![]
    } else {
        moves.into_iter().filter(|m| nodes.contains(m)).collect()
    };
    let mut moves_map = Map::new();
    for m in &moves {
        moves_map.insert(m.clone(), json!("clean"));
    }
    let mut entry = Map::new();
    entry.insert(
        "date".into(),
        json!(manila_date_from_filename(path).unwrap_or_else(|| "1970-01-01".into())),
    );
    entry.insert("problem".into(), json!(problem));
    entry.insert("moves".into(), Value::Object(moves_map));
    entry.insert(
        "pending".into(),
        json!(now.format("%Y-%m-%dT%H:%M:%S+00:00").to_string()),
    );
    if let Some(a) = apply_assist_floor(None, notes_assist_level(&notes_of(code)), &moves) {
        entry.insert("assist".into(), assist_json(&a));
    }
    Value::Object(entry)
}

fn assist_json(a: &IndexMap<String, String>) -> Value {
    Value::Object(a.iter().map(|(k, v)| (k.clone(), json!(v))).collect())
}

/// "Slide Never Shrink" from d_Slide_Never_Shrink_2026_..., "1539. Kth
/// Missing" from p1539_...: the subject of the judge's commit.
pub fn judge_title(path: &str) -> String {
    let base = Regex::new(r"_\d{4}_\d{2}_\d{2}T.*$")
        .unwrap()
        .replace(basename(path), "")
        .into_owned();
    if let Some(rest) = base.strip_prefix("d_") {
        return rest.replace("_FAILED", "").replace('_', " ");
    }
    match Regex::new(r"^p(\d+)_(.*)").unwrap().captures(&base) {
        Some(m) => format!(
            "{}. {}",
            &m[1],
            m[2].replace("_FAILED", "").replace('_', " ")
        ),
        None => base,
    }
}

struct Git {
    root: PathBuf,
}

impl Git {
    fn run(&self, args: &[&str], cwd: Option<&Path>, env: &[(&str, &str)]) -> std::process::Output {
        let mut c = Command::new("git");
        c.args(args).current_dir(cwd.unwrap_or(&self.root));
        for (k, v) in env {
            c.env(k, v);
        }
        c.output().expect("git")
    }
    fn out(&self, args: &[&str]) -> String {
        String::from_utf8_lossy(&self.run(args, None, &[]).stdout)
            .trim()
            .to_string()
    }
    fn ok(&self, args: &[&str], cwd: Option<&Path>, env: &[(&str, &str)]) -> bool {
        self.run(args, cwd, env).status.success()
    }
    fn tree(&self, sha: &str) -> String {
        self.out(&["rev-parse", &format!("{sha}^{{tree}}")])
    }
}

/// macOS dialog with the full verdict, so the detached judge's answer
/// reaches the operator without opening .judge.log or git log. A dialog,
/// not a notification: a notification truncates the text, and clicking it
/// opens Script Editor (osascript's owner) rather than anything useful.
/// The dialog closes itself after ten minutes; the judge is detached, so
/// the wait costs nothing.
fn notify_verdict(title: &str, moves: &IndexMap<String, String>, note: &str) {
    if !cfg!(target_os = "macos") {
        return;
    }
    let mut body: Vec<String> = moves.iter().map(|(m, v)| format!("{m}: {v}")).collect();
    if !note.is_empty() {
        body.push(note.to_string());
    }
    let esc = |s: &str| s.replace('\\', "\\\\").replace('"', "\\\"");
    let script = format!(
        "display dialog \"{}\" with title \"judge: {}\" buttons {{\"OK\"}} \
         default button 1 giving up after 600",
        esc(&body.join("\n")),
        esc(title)
    );
    let _ = Command::new("osascript")
        .arg("-e")
        .arg(script)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();
}

/// The commit that added this solved/ file, in HEAD's history.
fn solve_commit(git: &Git, path: &str) -> Option<String> {
    let out = git.out(&[
        "log",
        "--diff-filter=A",
        "--format=%H",
        "-1",
        "HEAD",
        "--",
        path,
    ]);
    if out.is_empty() {
        None
    } else {
        Some(out)
    }
}

fn commit_pushed(git: &Git, sha: &str) -> bool {
    git.ok(
        &["merge-base", "--is-ancestor", sha, "origin/master"],
        None,
        &[],
    )
}

/// Rewrite history so the judge's commit is part of the solve's commit,
/// then replay everything after the solve - on master and on every branch
/// cut from it - onto the rewritten commit. All in a temporary worktree;
/// the checked-out branch is moved only when its new tip has exactly the
/// tree it has now. Returns (ok, why); on any doubt nothing is moved.
fn fold_into(git: &Git, solve: &str, judge: &str) -> (bool, String) {
    let tmp = std::env::temp_dir().join(format!(
        "judge_{}_{}",
        std::process::id(),
        Utc::now().timestamp_nanos_opt().unwrap_or(0)
    ));
    let current = git.out(&["rev-parse", "--abbrev-ref", "HEAD"]);
    let refs: Vec<(String, String)> = git
        .out(&[
            "for-each-ref",
            "refs/heads",
            "--contains",
            solve,
            "--format=%(refname:short) %(objectname)",
        ])
        .lines()
        .filter_map(|l| {
            l.split_once(' ')
                .map(|(a, b)| (a.to_string(), b.to_string()))
        })
        .collect();
    let result = (|| -> (bool, String) {
        let r = git.run(
            &[
                "worktree",
                "add",
                "-q",
                "--detach",
                tmp.to_str().unwrap(),
                solve,
            ],
            None,
            &[],
        );
        if !r.status.success() {
            return (
                false,
                format!(
                    "no worktree: {}",
                    String::from_utf8_lossy(&r.stderr)
                        .trim()
                        .chars()
                        .take(120)
                        .collect::<String>()
                ),
            );
        }
        let dated = |sha: &str| git.out(&["show", "-s", "--format=%cI", sha]);
        let changed = git.out(&["diff-tree", "--no-commit-id", "--name-only", "-r", judge]);
        for path in changed.split_whitespace() {
            git.run(&["checkout", judge, "--", path], Some(&tmp), &[]);
        }
        let solve_date = dated(solve);
        let r = git.run(
            &["commit", "-q", "--amend", "--no-edit"],
            Some(&tmp),
            &[("GIT_COMMITTER_DATE", solve_date.as_str())],
        );
        if !r.status.success() {
            return (
                false,
                format!(
                    "amend failed: {}",
                    String::from_utf8_lossy(&r.stderr)
                        .trim()
                        .chars()
                        .take(120)
                        .collect::<String>()
                ),
            );
        }
        let rewritten =
            String::from_utf8_lossy(&git.run(&["rev-parse", "HEAD"], Some(&tmp), &[]).stdout)
                .trim()
                .to_string();
        let mut new: Vec<(String, String, String)> = Vec::new();
        for (name, old) in &refs {
            git.run(&["checkout", "-q", "--detach", &rewritten], Some(&tmp), &[]);
            let list = git.out(&["rev-list", "--reverse", &format!("{solve}..{old}")]);
            for c in list.split_whitespace() {
                if c == judge {
                    continue;
                }
                let was_empty = git.tree(c) == git.tree(&format!("{c}^"));
                let cd = dated(c);
                let mut args = vec!["cherry-pick"];
                if was_empty {
                    args.push("--allow-empty");
                }
                args.push(c);
                let r = git.run(&args, Some(&tmp), &[("GIT_COMMITTER_DATE", cd.as_str())]);
                if !r.status.success() {
                    let staged = !git.ok(&["diff", "--cached", "--quiet"], Some(&tmp), &[]);
                    let dirty = !git.ok(&["diff", "--quiet"], Some(&tmp), &[]);
                    if staged || dirty {
                        git.run(&["cherry-pick", "--abort"], Some(&tmp), &[]);
                        return (
                            false,
                            format!("{} does not replay cleanly on {name}", &c[..8]),
                        );
                    }
                    git.run(&["cherry-pick", "--skip"], Some(&tmp), &[]); // became empty: its change is in the fold
                }
            }
            let tip =
                String::from_utf8_lossy(&git.run(&["rev-parse", "HEAD"], Some(&tmp), &[]).stdout)
                    .trim()
                    .to_string();
            if *name == current && git.tree(&tip) != git.tree(old) {
                return (false, format!("the tree of {name} would change"));
            }
            new.push((name.clone(), old.clone(), tip));
        }
        new.sort_by_key(|(n, _, _)| n != "master");
        for (name, old, tip) in &new {
            let r = git.run(
                &["update-ref", &format!("refs/heads/{name}"), tip, old],
                None,
                &[],
            );
            if !r.status.success() && name == "master" {
                return (false, "master moved meanwhile".to_string());
            }
        }
        (true, String::new())
    })();
    git.run(
        &["worktree", "remove", "--force", tmp.to_str().unwrap()],
        None,
        &[],
    );
    git.run(&["worktree", "prune"], None, &[]);
    result
}

/// Land the judge's result in git: a commit of the graph files by path on
/// whatever is checked out now, then the fold into the solve's own commit
/// (a pushed solve keeps the judge: commit on top).
pub fn commit_judgement(root: &Path, judged: &[(String, Value)], refit: bool) -> String {
    let git = Git {
        root: root.to_path_buf(),
    };
    if refit {
        for tool in ["kg_curve", "kg_solvecost"] {
            let bin = std::env::current_exe()
                .ok()
                .and_then(|p| p.parent().map(|d| d.join(tool)))
                .unwrap_or_else(|| root.join("utils/rs/target/release").join(tool));
            let _ = Command::new(bin)
                .arg("--if-stale")
                .current_dir(root)
                .output();
        }
    }
    let paths: Vec<&str> = GRAPH_FILES
        .iter()
        .copied()
        .filter(|p| root.join(p).exists())
        .collect();
    let mut status_args = vec!["status", "--porcelain", "--"];
    status_args.extend(&paths);
    if git.out(&status_args).is_empty() {
        return "judge: nothing to commit".to_string();
    }
    let mut lines = Vec::new();
    for (path, entry) in judged {
        let verdicts: Vec<String> = entry["moves"]
            .as_object()
            .into_iter()
            .flatten()
            .map(|(m, v)| format!("{m}={}", v.as_str().unwrap_or("")))
            .collect();
        lines.push(format!(
            "{}: {}",
            judge_title(path),
            if verdicts.is_empty() {
                "-".to_string()
            } else {
                verdicts.join(", ")
            }
        ));
        if let Some(s) = entry
            .get("summary")
            .and_then(Value::as_str)
            .filter(|s| !s.is_empty())
        {
            lines.push(s.to_string());
        }
        lines.push(String::new());
    }
    let subject = format!(
        "judge: {}",
        judged
            .iter()
            .map(|(p, _)| judge_title(p))
            .collect::<Vec<_>>()
            .join(", ")
    );
    let message = format!("{subject}\n\n{}\n", lines.join("\n").trim_end());
    let mut committed = false;
    for _ in 0..40 {
        let mut args = vec!["commit", "-q", "-m", message.as_str(), "--"];
        args.extend(&paths);
        let r = git.run(&args, None, &[]);
        if r.status.success() {
            committed = true;
            break;
        }
        let err = String::from_utf8_lossy(&r.stderr).into_owned();
        if err.contains("index.lock") {
            std::thread::sleep(Duration::from_millis(1500));
            continue;
        }
        let out = String::from_utf8_lossy(&r.stdout).into_owned();
        let text = if err.trim().is_empty() { out } else { err };
        return format!(
            "judge: commit failed: {}",
            text.trim().chars().take(300).collect::<String>()
        );
    }
    if !committed {
        return "judge: commit failed: index.lock held for a minute".to_string();
    }
    if judged.len() != 1 {
        return format!("judge: committed {subject}");
    }
    let judge = git.out(&["rev-parse", "HEAD"]);
    let Some(solve) = solve_commit(&git, &judged[0].0) else {
        return format!("judge: committed {subject} (no solve commit to fold into)");
    };
    if commit_pushed(&git, &solve) {
        return format!("judge: committed {subject} (solve already pushed, not folded)");
    }
    let (ok, why) = fold_into(&git, &solve, &judge);
    if ok {
        format!(
            "judge: folded into {}",
            git.out(&["show", "-s", "--format=%s", &solve])
        )
    } else {
        format!("judge: committed {subject} (not folded: {why})")
    }
}

/// Rich-markup lines explaining what this solve meant to the graph: for each
/// non-solid move the problem was serving, did it get its rep and what did
/// that do to its status, plus the reach a new SOLID opens.
#[allow(clippy::too_many_arguments)]
fn serve_receipt(
    ctx: &Ctx,
    pnum: &str,
    moves: &[String],
    pre_moves: &[String],
    was_mapped: bool,
    pv: &PView,
    ev: &Evidence,
    before: &Evidence,
) -> Vec<String> {
    let today = ctx.today();
    let drafted: Vec<Vec<String>> = ctx
        .predicted
        .get(pnum)
        .map(|p| p.walks.iter().map(|w| w.moves.clone()).collect())
        .unwrap_or_default();
    let mut expected: Vec<String> = Vec::new();
    for m in pre_moves.iter().chain(drafted.iter().flatten()) {
        if !expected.contains(m) {
            expected.push(m.clone());
        }
    }
    let targets: Vec<&String> = expected
        .iter()
        .filter(|m| ctx.nodes.contains_key(*m) && node_status(ctx, m, before, today).0 != SOLID)
        .collect();
    let mut lines = Vec::new();
    for t in targets {
        let b = node_status(ctx, t, before, today).0;
        let a = node_status(ctx, t, ev, today).0;
        let line = if moves.contains(t) {
            let mut line = if a != b {
                format!("served for [bold]{t}[/bold]: {b} → {a}")
            } else {
                format!("served for [bold]{t}[/bold]: got its rep, stays {a}")
            };
            if a == SOLID && b != SOLID {
                let statuses_before = all_statuses(ctx, before, today);
                let gained = unlocks(ctx, &statuses_before, pv, &HashSet::new())
                    .get(t)
                    .copied()
                    .unwrap_or(0);
                if gained != 0 {
                    line.push_str(&format!(
                        " — brings {gained} drafted problem{} into reach",
                        if gained != 1 { "s" } else { "" }
                    ));
                }
            }
            line
        } else if !moves.is_empty() {
            format!(
                "served for [bold]{t}[/bold] — the code went {} instead; {t} stays {a}",
                moves.join(", ")
            )
        } else {
            format!("served for [bold]{t}[/bold] — the solve evidenced no moves; {t} stays {a}")
        };
        lines.push(line);
    }
    if !was_mapped && !drafted.is_empty() && !moves.is_empty() {
        let mut guess: Vec<String> = Vec::new();
        for m in drafted.iter().flatten() {
            if !guess.contains(m) {
                guess.push(m.clone());
            }
        }
        lines.push(format!(
            "draft guessed ({}) → evidenced ({})",
            guess.join(", "),
            moves.join(", ")
        ));
    }
    lines
}

struct Judged {
    result: Value,
    is_drill: bool,
    trains: Vec<String>,
    notes: String,
    followup: String,
}

/// Read + claude call only - no shared state touched here.
fn extract_one(
    root: &Path,
    path: &str,
    system: &str,
    model: &str,
    drills: &DrillMap,
    canon_of: &dyn Fn(&str) -> Vec<String>,
) -> Result<Judged, String> {
    let code = std::fs::read_to_string(root.join(path)).map_err(|e| e.to_string())?;
    let is_drill = is_drill_file(path, &code);
    let trains = if is_drill {
        trains_in(&code, drills)
    } else {
        vec![]
    };
    let body: String = strip_statement(&code).chars().take(6000).collect();
    let (status, detail) = run_solve(root, path);
    let mut prompt = format!(
        "File: {}\n\n{}\n\n{body}",
        basename(path),
        runtime_note(&status, &detail)
    );
    let followup = if is_drill {
        String::new()
    } else {
        followup_of(&code)
    };
    if !followup.is_empty() {
        prompt = format!(
            "The statement ends with a follow-up question: {followup} Judge whether the code as written meets it and answer in \"followup\": \"solved\" or \"not solved\".\n\n{prompt}"
        );
    }
    if is_drill {
        prompt = format!(
            "This is a DRILL file targeting these taxonomy nodes: {}. Judge at least those moves.\n\n{prompt}",
            if trains.is_empty() { "unknown".to_string() } else { trains.join(", ") }
        );
    } else if let Some((pnum, _)) = problem_of_fname(path) {
        let canon = canon_of(&pnum);
        if !canon.is_empty() {
            prompt = format!(
                "This problem's canonical walk in our curated map: {}. Judge EVERY one of those moves explicitly: 'clean' or 'struggled' if the code exercises it, 'avoided' if the solution routes around it. Also add any other moves the code actually exercises.\n\n{prompt}",
                canon.join(", ")
            );
        }
    }
    let notes = notes_of(&code);
    let result = claude_json(&prompt, system, model, 2).map_err(|e| e.to_string())?;
    Ok(Judged {
        result,
        is_drill,
        trains,
        notes,
        followup,
    })
}

fn system_prompt(ctx: &Ctx) -> String {
    format!(
        r#"You judge which atomic technique moves a candidate's LeetCode solution ACTUALLY exercised.

Taxonomy (use ONLY these ids):
{}

Rules:
- {}
- Every file is EXECUTED for you before you see it, and the result is stated in the prompt. That result OUTWEIGHS your reading of the source in every case. If the run passed, the code is correct — no "struggled" for suspected bugs, and no note claiming a failure. Only a non-zero exit, a timeout, or the candidate's own notes (looked-up/hints/TLE/failed) justify "struggled".
- Judge the code as written, not the problem's canonical solution. Batch math on a streaming-carrier problem means the streaming move was NOT exercised — if the canonical solution's central move was sidestepped by an alternative approach, record that move as "avoided".
- Verdicts: "clean" (executed correctly), "struggled" (bugs/confusion visible in code or notes, e.g. notes saying looked-up/hints/TLE/failed), "avoided" (canonical move sidestepped).
- A failing run condemns ONE move, not the whole walk. Find the defect - the line the traceback points at, the wrong bound, the missing case - and mark "struggled" only on the move that line belongs to. Every other move the code exercised correctly stays "clean": an IndexError in a grid boundary test is not evidence against the recursion or the memoization that ran fine around it. If the defect belongs to no node in the taxonomy - index arithmetic, an off-by-one in a bound, a typo - mark NO move "struggled" and say where the defect was in the note.
- A drill file (DRILL: header) is a rung written to train exactly its TRAINS node. If it ran and its REQUIRED line is met, that node is "clean", whatever API spelling the code used: select("a", "b") trains a column-expression rung as well as select(F.col("a")) does. "avoided" is for a leetcode carrier whose central move was sidestepped, never for a drill that passed.
- "assist" is a SEPARATE axis from the verdict, read ONLY from the candidate's own notes — never inferred from how the code looks. A confident-looking solve with a note saying it was walked through is "walkthrough"; a messy solve with no note is "none". Levels: "none" (no note claiming help), "hint" (a nudge, a question, a pointer at the wrong branch), "walkthrough" (the approach/recurrence was talked through before the code existed), "learning" (the solution was given and copied). An explicit `ASSIST: <level>` line in the notes overrides your reading. Assist is PER MOVE: when the notes say what the help was on ("assisted on the window bookkeeping, the prefix sums were mine"), put the level on that move only and leave the others out, because a level on a move says the candidate could not recall THAT move unaided. When the notes claim help without saying where, put the level on every move in "moves". Omit the key, or use {{}}, when there was no help.
- Only include moves with real evidence in this code. 1-6 moves is typical.
- If a required move has no taxonomy node, put a 3-8 word description in "unmapped".
- If the file has no working solution (skeleton body, abandoned attempt), still return the JSON with "moves": {{}} and a note like "abandoned attempt" — never prose.
- "recognition": read ONLY from the candidate's own notes, like assist. When the notes say a move was not seen from the statement ("recognition failure", "failed to see it was binary search on the answer", "didn't recognise the monotonic stack"), list that move's id under "missed". A move being wrong or slow is not a recognition miss; only the notes saying it was not recognised is. Omit the key when the notes say nothing of the kind.
- "followup": only when the prompt states the statement's follow-up question. "solved" when the code as written meets it (the bound it asks for, or the iterative/recursive form), "not solved" when it does not. Judge the code, not the notes.
- "summary": 2-4 sentences of plain english for the candidate to read after filing: what the code does and how, which moves it exercised, and what the notes say happened (hints, look-ups, TLEs, dead ends) if anything. Facts only: no praise, no grading, no advice, no adjectives about the candidate. Refer to the code by its real names (its variables, clauses, functions).

Output STRICT JSON only:
{{"problem": "<number>", "title": "<title>", "moves": {{"<node-id>": "clean|struggled|avoided"}}, "assist": {{"<node-id>": "hint|walkthrough|learning"}}, "recognition": {{"missed": ["<node-id>"]}}, "followup": "solved|not solved", "unmapped": [], "note": "<one line, only if noteworthy>", "summary": "<2-4 sentences>"}}"#,
        ctx.taxonomy_summary(),
        harness_env_note(&ctx.root)
    )
}

fn load_problems_raw(root: &Path) -> Map<String, Value> {
    pyjson::load(&root.join("graph/problems.json"))
        .and_then(|v| v["problems"].as_object().cloned())
        .unwrap_or_default()
}

/// The evidenced problems' moves from the raw table (kg_lib.load_problems).
fn canonical_moves(problems: &Map<String, Value>, pnum: &str) -> Vec<String> {
    problems
        .get(pnum)
        .filter(|p| !p.get("draft").is_some_and(kg::data::truthy))
        .and_then(|p| p["moves"].as_array())
        .map(|a| a.iter().map(kg::data::value_str).collect())
        .unwrap_or_default()
}

/// Score every recognition/*.md not yet in recognition.json.
#[allow(clippy::regex_creation_in_loops)]
fn judge_spots(console: &Console, ctx: &Ctx, model: &str) {
    let mut recog = recog::load_recognition_raw(&ctx.root);
    for path in recog::pending_spots(&ctx.root, &recog) {
        let text = std::fs::read_to_string(ctx.root.join(&path)).unwrap_or_default();
        let foot = recog::read_footer(&text);
        let pnum = foot
            .get("problem")
            .map(kg::data::value_str)
            .filter(|p| !p.is_empty())
            .or_else(|| {
                Regex::new(r"^s(\d+)_")
                    .unwrap()
                    .captures(basename(&path))
                    .map(|m| m[1].to_string())
            })
            .unwrap_or_else(|| "?".to_string());
        let (statement, answer) = recog::split_answer(&text);
        let mut pv = PView::new(ctx.evidenced());
        let mut title = pv
            .map
            .get(&pnum)
            .map(|p| p.title.clone())
            .unwrap_or_default();
        if pv.map.get(&pnum).is_none_or(|p| p.moves.is_empty()) {
            console.print(&format!(
                "[dim]{pnum} has no walk - one claude call to map it (cached after)...[/dim]"
            ));
            let mapped = (|| -> Result<(), String> {
                if title.is_empty() {
                    title = recog::fetch_content(&ctx.root, &pnum)?["title"]
                        .as_str()
                        .unwrap_or("")
                        .to_string();
                }
                recog::map_problem(ctx, &pnum, &title, model)?;
                Ok(())
            })();
            if let Err(e) = mapped {
                console.print(&format!(
                    "[red]FAIL {path}: could not map {pnum}: {}[/red]",
                    e.chars().take(200).collect::<String>()
                ));
                continue;
            }
            pv = PView::new(kg::data::evidenced_view(&kg::data::load_all_problems(
                &ctx.root,
            )));
            title = pv
                .map
                .get(&pnum)
                .map(|p| p.title.clone())
                .filter(|t| !t.is_empty())
                .unwrap_or(title);
        }
        let (named, summary) = match recog::judge_answer(ctx, &statement, &answer, model) {
            Ok(v) => v,
            Err(e) => {
                console.print(&format!(
                    "[red]FAIL {path}: {}[/red]",
                    e.chars().take(200).collect::<String>()
                ));
                continue;
            }
        };
        let target = foot.get("target").and_then(Value::as_str);
        let (mut moves, mut false_) = recog::score(&named, &pv, &pnum, target);
        let mut rec = Map::new();
        rec.insert(
            "date".into(),
            json!(manila_date_from_filename(&path).unwrap_or_else(|| "1970-01-01".into())),
        );
        rec.insert("problem".into(), json!(pnum));
        rec.insert("kind".into(), json!("spot"));
        rec.insert("title".into(), json!(title));
        rec.insert(
            "target".into(),
            foot.get("target").cloned().unwrap_or(Value::Null),
        );
        rec.insert(
            "reason".into(),
            foot.get("reason").cloned().unwrap_or(Value::Null),
        );
        rec.insert(
            "seconds".into(),
            foot.get("seconds").cloned().unwrap_or(json!(0)),
        );
        rec.insert("named".into(), json!(named));
        rec.insert(
            "walk".into(),
            json!(pv
                .map
                .get(&pnum)
                .map(|p| p.moves.clone())
                .unwrap_or_default()),
        );
        rec.insert(
            "moves".into(),
            Value::Object(moves.iter().map(|(k, v)| (k.clone(), json!(v))).collect()),
        );
        rec.insert("false".into(), json!(false_));
        rec.insert("summary".into(), json!(summary));
        if !answer.is_empty() {
            rec.insert(
                "answer".into(),
                json!(answer.chars().take(1000).collect::<String>()),
            );
        }
        if !answer.trim().is_empty() && !named.is_empty() {
            let (valid, why) = match recog::judge_route(&statement, &answer, &named, "sonnet") {
                Ok(v) => (Some(v.0), v.1),
                Err(e) => (
                    None,
                    format!(
                        "route not judged: {}",
                        e.chars().take(120).collect::<String>()
                    ),
                ),
            };
            rec.insert(
                "valid".into(),
                valid.map(Value::Bool).unwrap_or(Value::Null),
            );
            rec.insert("why".into(), json!(why));
            if valid == Some(true)
                && moves.values().any(|v| v == recog::MISSED)
                && !false_.is_empty()
            {
                // a valid alternative walk: a hit on every named move, the
                // target's miss goes, the walk filed under spotted_walks
                moves = named
                    .iter()
                    .map(|n| (n.clone(), recog::HIT.to_string()))
                    .collect();
                if let Some(t) = target {
                    if !moves.contains_key(t) {
                        moves.insert(t.to_string(), recog::ALTERNATIVE.to_string());
                    }
                }
                false_ = vec![];
                rec.insert(
                    "moves".into(),
                    Value::Object(moves.iter().map(|(k, v)| (k.clone(), json!(v))).collect()),
                );
                rec.insert("false".into(), json!(false_));
                rec.insert("alternative".into(), json!(named));
                rec.insert("why".into(), json!(why));
                let mut problems = load_problems_raw(&ctx.root);
                let entry = problems.entry(pnum.clone()).or_insert_with(|| json!({}));
                let walks = entry["spotted_walks"]
                    .as_array()
                    .cloned()
                    .unwrap_or_default();
                let mut walks = walks;
                if !walks.contains(&json!(named)) {
                    walks.push(json!(named));
                }
                let mut e = entry.clone();
                e["spotted_walks"] = json!(walks);
                let _ = pyjson::save_problem_entry(&ctx.root, &pnum, &e);
            }
        }
        recog[path.as_str()] = Value::Object(rec.clone());
        let _ = recog::save_recognition(&ctx.root, &recog);
        let verdict = moves
            .iter()
            .map(|(n, v)| format!("{n}={v}"))
            .collect::<Vec<_>>()
            .join(", ");
        console.print(&format!(
            "[green]spot[/green] {} → {}",
            basename(&path).chars().take(60).collect::<String>(),
            if verdict.is_empty() {
                "unscored".to_string()
            } else {
                verdict
            }
        ));
    }
}

fn main() {
    let argv: Vec<String> = std::env::args().skip(1).collect();
    if argv.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_extract [--limit N] [--model M] [--workers N] [--followup] [--stub] [--file F] [--pending] [--commit]");
        return;
    }
    let flag = |name: &str| -> Option<String> {
        argv.iter()
            .position(|a| a == name)
            .and_then(|i| argv.get(i + 1).cloned())
    };
    // the test hooks: pure functions over one file
    if let Some(f) = flag("--followup-of") {
        println!(
            "{}",
            followup_of(&std::fs::read_to_string(&f).unwrap_or_default())
        );
        return;
    }
    if let Some(f) = flag("--strip") {
        print!(
            "{}",
            strip_statement(&std::fs::read_to_string(&f).unwrap_or_default())
        );
        return;
    }
    let limit: usize = flag("--limit").and_then(|s| s.parse().ok()).unwrap_or(0);
    let model = flag("--model").unwrap_or_else(|| "haiku".to_string());
    let workers: usize = flag("--workers").and_then(|s| s.parse().ok()).unwrap_or(8);
    let (followup_mode, stub, pending, commit) = (
        argv.iter().any(|a| a == "--followup"),
        argv.iter().any(|a| a == "--stub"),
        argv.iter().any(|a| a == "--pending"),
        argv.iter().any(|a| a == "--commit"),
    );
    let file = flag("--file");

    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let console = Console::full_width();
    let mut evidence = Evidence::new(recs);
    let problems_raw = load_problems_raw(&ctx.root);
    let node_set: HashSet<String> = ctx.nodes.keys().cloned().collect();

    if stub {
        let Some(meta) = pyjson::load(&ctx.root.join(".solve_meta.json")) else {
            console.print("[yellow]nothing staged - no placeholder to write.[/yellow]");
            return;
        };
        if meta.get("kind").and_then(Value::as_str) != Some("spot") {
            let file = meta["file"].as_str().unwrap_or("");
            let path = file.strip_prefix("./").unwrap_or(file).to_string();
            if let Some(&i) = evidence.by_fname.get(&path) {
                if evidence.rec(i).pending.as_deref().is_none_or(str::is_empty) {
                    return; // judged already (a resumed run)
                }
            }
            let code = std::fs::read_to_string(ctx.root.join(&path)).unwrap_or_default();
            let entry = stub_entry(
                &path,
                &code,
                &node_set,
                &|p| canonical_moves(&problems_raw, p),
                &ctx.drills,
                Utc::now(),
            );
            pyjson::store_evidence_entry(&ctx.root, &path, &entry)
                .expect("write graph/evidence.json");
            let moves: Vec<&str> = entry["moves"]
                .as_object()
                .map(|m| m.keys().map(String::as_str).collect())
                .unwrap_or_default();
            console.print(&format!(
                "[dim]placeholder filed on {}; the judge runs detached.[/dim]",
                if moves.is_empty() {
                    "-".to_string()
                } else {
                    moves.join(", ")
                }
            ));
            return;
        }
        // a spot rep reveals its walk after the judge: judged now, in line
    }

    let mut files: Vec<(std::time::SystemTime, String)> =
        std::fs::read_dir(ctx.root.join("solved"))
            .into_iter()
            .flatten()
            .filter_map(Result::ok)
            .filter(|e| e.path().extension().is_some_and(|x| x == "py"))
            .map(|e| {
                let m = e
                    .metadata()
                    .and_then(|m| m.modified())
                    .unwrap_or(std::time::UNIX_EPOCH);
                (m, format!("solved/{}", e.file_name().to_string_lossy()))
            })
            .collect();
    files.sort_by(|a, b| b.0.cmp(&a.0));
    let files: Vec<String> = files.into_iter().map(|(_, p)| p).collect();
    let mut todo: Vec<String> = match &file {
        Some(f) => vec![f.strip_prefix("./").unwrap_or(f).to_string()],
        None => files
            .iter()
            .filter(|f| match evidence.by_fname.get(*f) {
                None => true,
                Some(&i) => {
                    pending
                        && evidence
                            .rec(i)
                            .pending
                            .as_deref()
                            .is_some_and(|p| !p.is_empty())
                }
            })
            .cloned()
            .collect(),
    };
    if limit > 0 {
        todo.truncate(limit);
    }
    console.print(&format!(
        "{} solve files, {} to process this run.\n",
        files.len(),
        todo.len()
    ));
    let system = system_prompt(&ctx);

    if followup_mode {
        rejudge_followups(
            &console,
            &ctx,
            &evidence,
            &system,
            &model,
            workers,
            &problems_raw,
        );
        return;
    }

    // the workers: one claude call each, results handed back as they land
    let (tx, rx) = mpsc::channel::<(String, Result<Judged, String>)>();
    let queue = std::sync::Mutex::new(todo.clone());
    std::thread::scope(|scope| {
        // Ctx is single-threaded (RefCell caches): the workers get copies of
        // the little they read
        let root = ctx.root.clone();
        let drills = ctx.drills.clone();
        for _ in 0..workers.max(1).min(todo.len().max(1)) {
            let tx = tx.clone();
            let queue = &queue;
            let root = root.clone();
            let drills = drills.clone();
            let system = &system;
            let model = &model;
            let problems_raw = &problems_raw;
            scope.spawn(move || loop {
                let next = queue.lock().unwrap().pop();
                let Some(path) = next else { break };
                let r = extract_one(&root, &path, system, model, &drills, &|p| {
                    canonical_moves(problems_raw, p)
                });
                let _ = tx.send((path, r));
            });
        }
        drop(tx);
        let mut done = 0;
        let mut failed = 0;
        let mut landed: Vec<(String, Value)> = Vec::new();
        for (path, r) in rx {
            let judged = match r {
                Ok(j) => j,
                Err(e) => {
                    failed += 1;
                    console.print(&format!(
                        "[red]FAIL {path}: {}[/red]",
                        e.chars().take(200).collect::<String>()
                    ));
                    continue;
                }
            };
            let result = &judged.result;
            let fname_problem = problem_of_fname(&path);
            let solve_date =
                manila_date_from_filename(&path).unwrap_or_else(|| "1970-01-01".into());
            let all_moves: IndexMap<String, String> = result["moves"]
                .as_object()
                .into_iter()
                .flatten()
                .map(|(k, v)| (k.clone(), v.as_str().unwrap_or("").to_string()))
                .collect();
            let judged_moves: IndexMap<String, String> = all_moves
                .iter()
                .filter(|(k, _)| node_set.contains(*k))
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect();
            let rejected: Vec<String> = all_moves
                .keys()
                .filter(|k| !node_set.contains(*k))
                .cloned()
                .collect();
            // free-mode evidence discipline: record only what the code DID
            let moves: IndexMap<String, String> = judged_moves
                .iter()
                .filter(|(_, v)| *v != "avoided")
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect();
            let mut skipped: HashSet<String> = judged_moves
                .iter()
                .filter(|(_, v)| *v == "avoided")
                .map(|(k, _)| k.clone())
                .collect();
            let problems_now = load_problems_raw(&ctx.root);
            if !judged.is_drill {
                if let Some((pnum, _)) = &fname_problem {
                    for mv in canonical_moves(&problems_now, pnum) {
                        if node_set.contains(&mv) && !judged_moves.contains_key(&mv) {
                            skipped.insert(mv);
                        }
                    }
                }
            }
            let problem = if judged.is_drill {
                "drill".to_string()
            } else {
                result
                    .get("problem")
                    .map(kg::data::value_str)
                    .filter(|p| !p.is_empty())
                    .unwrap_or_else(|| {
                        fname_problem
                            .as_ref()
                            .map(|(p, _)| p.clone())
                            .unwrap_or_else(|| "?".to_string())
                    })
            };
            let move_names: Vec<String> = moves.keys().cloned().collect();
            let mut assist = normalise_assist(result.get("assist"), &move_names);
            let floor = notes_assist_level(&judged.notes);
            let targets: Vec<String> = if judged.is_drill {
                judged
                    .trains
                    .iter()
                    .filter(|t| moves.contains_key(*t))
                    .cloned()
                    .collect()
            } else {
                vec![]
            };
            assist = apply_assist_floor(
                assist,
                floor,
                if targets.is_empty() {
                    &move_names
                } else {
                    &targets
                },
            );
            let recog_raw = recog::load_recognition_raw(&ctx.root);
            let spotted = if judged.is_drill {
                None
            } else {
                recog::spotted_before_raw(&recog_raw, &problem, &solve_date)
            };
            if spotted.is_some_and(|(_, v)| v == recog::MISSED) {
                assist = apply_assist_floor(assist, "hint", &move_names);
            }
            let mut entry = Map::new();
            entry.insert("date".into(), json!(solve_date));
            entry.insert("problem".into(), json!(problem));
            entry.insert(
                "moves".into(),
                Value::Object(moves.iter().map(|(k, v)| (k.clone(), json!(v))).collect()),
            );
            if let Some(a) = &assist {
                entry.insert("assist".into(), assist_json(a));
            }
            let mut missed: Vec<String> = result["recognition"]["missed"]
                .as_array()
                .into_iter()
                .flatten()
                .filter_map(|v| v.as_str())
                .filter(|n| node_set.contains(*n))
                .map(String::from)
                .collect();
            let pv_now = PView::new(kg::data::evidenced_view(&kg::data::load_all_problems(
                &ctx.root,
            )));
            if missed.is_empty() && !judged.is_drill && recog::notes_say_missed(&judged.notes) {
                missed = recog::entry_nodes(&pv_now, &problem)
                    .into_iter()
                    .take(1)
                    .collect();
            }
            if !judged.followup.is_empty()
                && result
                    .get("followup")
                    .and_then(Value::as_str)
                    .is_some_and(|v| FOLLOWUP_VERDICTS.contains(&v))
            {
                entry.insert("followup".into(), result["followup"].clone());
            }
            if result.get("note").is_some_and(kg::data::truthy) {
                entry.insert("note".into(), result["note"].clone());
            }
            if result.get("summary").is_some_and(kg::data::truthy) {
                entry.insert(
                    "summary".into(),
                    json!(kg::data::value_str(&result["summary"]).trim()),
                );
            }
            let unmapped_answer: Vec<Value> =
                result["unmapped"].as_array().cloned().unwrap_or_default();
            if !unmapped_answer.is_empty() || !rejected.is_empty() {
                let mut all = unmapped_answer;
                all.extend(rejected.iter().map(|r| json!(r)));
                entry.insert("unmapped".into(), Value::Array(all));
            }
            let entry = Value::Object(entry);

            // against the files as they are NOW: another judge, or the next
            // solve's placeholder, may have written since we loaded
            let fresh = pyjson::store_evidence_entry(&ctx.root, &path, &entry)
                .expect("write graph/evidence.json");
            landed.push((path.clone(), entry.clone()));
            let mut recs: Vec<(String, Rec)> = fresh
                .as_object()
                .into_iter()
                .flatten()
                .map(|(k, v)| (k.clone(), Rec::parse(v)))
                .collect();
            evidence = Evidence::new(recs.clone());
            let before: Vec<(String, Rec)> = {
                recs.retain(|(k, _)| *k != path);
                recs
            };
            let before_ev = Evidence::new(before);
            let mut recog_raw = recog::load_recognition_raw(&ctx.root);
            if !missed.is_empty() {
                recog_raw[path.as_str()] = json!({
                    "date": solve_date,
                    "problem": problem,
                    "kind": "solve",
                    "moves": missed.iter().map(|n| (n.clone(), json!(recog::MISSED))).collect::<Map<String, Value>>(),
                    "note": "the notes say the move was not recognised",
                });
                let _ = recog::save_recognition(&ctx.root, &recog_raw);
                console.print(&format!(
                    "    [red]recognition miss on [bold]{}[/bold][/red] (from the notes)",
                    missed.join(", ")
                ));
            }
            if let Some((d, v)) = spotted {
                console.print(&format!(
                    "    [dim]spotted {d} ({v}){}[/dim]",
                    if v == recog::MISSED {
                        ": assist floored to hint"
                    } else {
                        ""
                    }
                ));
            }
            let mut problems_now = load_problems_raw(&ctx.root);
            let was_mapped = problems_now
                .get(&problem)
                .is_some_and(|p| !p.get("draft").is_some_and(kg::data::truthy));
            let pre_moves = canonical_moves(&problems_now, &problem);
            if !judged.is_drill && record_alt_walk(&mut problems_now, &problem, &moves, &skipped) {
                let e = problems_now[&problem].clone();
                pyjson::save_problem_entry(&ctx.root, &problem, &e)
                    .expect("write graph/problems.json");
            }
            if !judged.is_drill && !was_mapped && !moves.is_empty() {
                let title = result
                    .get("title")
                    .and_then(Value::as_str)
                    .map(String::from)
                    .unwrap_or_else(|| {
                        fname_problem
                            .as_ref()
                            .map(|(_, t)| t.replace('_', " "))
                            .unwrap_or_default()
                    });
                let e = json!({
                    "title": title,
                    "difficulty": ctx.meta_difficulty(&problem),
                    "moves": move_names,
                    "source": "extracted",
                });
                pyjson::save_problem_entry(&ctx.root, &problem, &e)
                    .expect("write graph/problems.json");
            }
            done += 1;
            if file.is_some() {
                let note = result
                    .get("note")
                    .map(kg::data::value_str)
                    .unwrap_or_default();
                notify_verdict(&judge_title(&path), &moves, note.trim());
            }
            let painted: Vec<String> = moves
                .iter()
                .map(|(m, v)| {
                    let st = match v.as_str() {
                        "clean" => "green",
                        "struggled" => "red",
                        "avoided" => "yellow",
                        _ => "white",
                    };
                    format!("[{st}]{m}[/{st}]")
                })
                .collect();
            let tag = match &assist {
                Some(a) => format!(
                    " [yellow](assist: {})[/yellow]",
                    a.iter()
                        .map(|(m, v)| format!("{m}={v}"))
                        .collect::<Vec<_>>()
                        .join(", ")
                ),
                None => String::new(),
            };
            console.print(&format!(
                "[green]{done}/{}[/green] {} → {}{tag}",
                todo.len(),
                basename(&path).chars().take(60).collect::<String>(),
                if painted.is_empty() {
                    "—".to_string()
                } else {
                    painted.join(", ")
                }
            ));
            // the receipt: struggles change the graph - say so
            let today = ctx.today();
            for (mv, verdict) in &moves {
                if verdict != "struggled" {
                    continue;
                }
                let b = node_status(&ctx, mv, &before_ev, today).0;
                let a = node_status(&ctx, mv, &evidence, today).0;
                let change = if a != b {
                    format!("[red]{b} → {a}[/red]")
                } else {
                    format!("stays {a}")
                };
                console.print(&format!(
                    "    [red]⚠ struggled on [bold]{mv}[/bold][/red] ({change})"
                ));
            }
            if !judged.is_drill {
                let pv = PView::new(kg::data::evidenced_view(&kg::data::load_all_problems(
                    &ctx.root,
                )));
                for line in serve_receipt(
                    &ctx,
                    &problem,
                    &move_names,
                    &pre_moves,
                    was_mapped,
                    &pv,
                    &evidence,
                    &before_ev,
                ) {
                    console.print(&format!("    [dim]{line}[/dim]"));
                }
            }
        }
        console.print(&format!(
            "\nDone: {done} processed, {failed} failed (re-run to retry), evidence.json now has {} entries.",
            evidence.len()
        ));
        if file.is_none() {
            judge_spots(&console, &ctx, &model);
        }
        if commit && !landed.is_empty() {
            console.print(&commit_judgement(&ctx.root, &landed, true));
        }
    });
}

/// Fill the "followup" field on evidenced problem solves whose statement
/// asks one and whose entry predates the field: ONLY that field is taken.
fn rejudge_followups(
    console: &Console,
    ctx: &Ctx,
    evidence: &Evidence,
    system: &str,
    model: &str,
    workers: usize,
    problems: &Map<String, Value>,
) {
    let todo: Vec<String> = evidence
        .recs
        .iter()
        .filter(|(p, e)| {
            e.problem.as_deref() != Some("drill")
                && e.followup.is_none()
                && ctx.root.join(p).exists()
                && !followup_of(&std::fs::read_to_string(ctx.root.join(p)).unwrap_or_default())
                    .is_empty()
        })
        .map(|(p, _)| p.clone())
        .collect();
    console.print(&format!(
        "{} evidenced solves with a follow-up and no verdict on it.\n",
        todo.len()
    ));
    let (tx, rx) = mpsc::channel::<(String, Result<Judged, String>)>();
    let queue = std::sync::Mutex::new(todo.clone());
    let (mut done, mut failed) = (0, 0);
    std::thread::scope(|scope| {
        let root = ctx.root.clone();
        let drills = ctx.drills.clone();
        for _ in 0..workers.max(1).min(todo.len().max(1)) {
            let tx = tx.clone();
            let queue = &queue;
            let root = root.clone();
            let drills = drills.clone();
            scope.spawn(move || loop {
                let next = queue.lock().unwrap().pop();
                let Some(path) = next else { break };
                let r = extract_one(&root, &path, system, model, &drills, &|p| {
                    canonical_moves(problems, p)
                });
                let _ = tx.send((path, r));
            });
        }
        drop(tx);
        for (path, r) in rx {
            let verdict = r.ok().and_then(|j| {
                j.result
                    .get("followup")
                    .and_then(Value::as_str)
                    .map(String::from)
            });
            match verdict.filter(|v| FOLLOWUP_VERDICTS.contains(&v.as_str())) {
                None => {
                    failed += 1;
                    console.print(&format!("[red]no follow-up verdict for {path}[/red]"));
                }
                Some(v) => {
                    let _lock = pyjson::EvidenceLock::take(&ctx.root);
                    let ev_path = ctx.root.join("graph/evidence.json");
                    if let Some(mut data) = pyjson::load(&ev_path) {
                        data["evidence"][path.as_str()]["followup"] = json!(v);
                        let _ = pyjson::save(&ev_path, &data, Some(2));
                    }
                    done += 1;
                    let style = if v == "solved" { "green" } else { "yellow" };
                    console.print(&format!(
                        "[green]{done}/{}[/green] {} → follow-up [{style}]{v}[/{style}]",
                        todo.len(),
                        basename(&path).chars().take(60).collect::<String>()
                    ));
                }
            }
        }
    });
    console.print(&format!(
        "\nDone: {done} judged, {failed} failed (re-run to retry)."
    ));
}

#[cfg(test)]
mod tests {
    use super::*;

    const SOLVE: &str = "\"\"\"\n1. Two Sum\n\nGiven an array of integers, return indices of the two numbers that add to\ntarget.\n\n---\nPeeked at the editorial for the complement trick.\n\"\"\"\n\nfrom typing import List\n\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        seen = {}  # running dict, built as we scan\n        for i, n in enumerate(nums):\n            if target - n in seen:\n                return [seen[target - n], i]\n            seen[n] = i\n\n\nsol = Solution()\nassert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]\n";

    /// utils/tests/test_kg_extract.py: the notes survive the statement strip.
    #[test]
    fn notes_and_code_survive_the_statement_strip() {
        let out = strip_statement(SOLVE);
        assert!(out.contains("Peeked at the editorial"));
        assert!(!out.contains("Given an array of integers"));
        assert!(out.contains("def twoSum") && out.contains("running dict, built as we scan"));
        let code = "class Solution:\n    pass\n";
        assert_eq!(strip_statement(code), code);
        let broken = "\"\"\"\n1. Two Sum\n\n---\nGave up.\n\"\"\"\n\ndef f(:\n";
        assert!(strip_statement(broken).contains("def f(:"));
    }

    #[test]
    fn alt_walks() {
        let mut problems: Map<String, Value> =
            serde_json::from_str(r#"{"1512": {"moves": ["streaming-accumulate-pairs"]}}"#).unwrap();
        let mut moves = IndexMap::new();
        moves.insert("counter-build".to_string(), "clean".to_string());
        let skipped: HashSet<String> = ["streaming-accumulate-pairs".to_string()].into();
        assert!(record_alt_walk(&mut problems, "1512", &moves, &skipped));
        assert_eq!(problems["1512"]["alt_walks"], json!([["counter-build"]]));
        // an empty alt walk is still recorded, once
        let mut problems: Map<String, Value> =
            serde_json::from_str(r#"{"3042": {"moves": ["pair-count-formula"]}}"#).unwrap();
        let skipped: HashSet<String> = ["pair-count-formula".to_string()].into();
        assert!(record_alt_walk(
            &mut problems,
            "3042",
            &IndexMap::new(),
            &skipped
        ));
        assert_eq!(problems["3042"]["alt_walks"], json!([[]]));
        assert!(!record_alt_walk(
            &mut problems,
            "3042",
            &IndexMap::new(),
            &skipped
        ));
        // nothing recorded when no mapped move was skipped, or for an unmapped problem
        let mut problems: Map<String, Value> =
            serde_json::from_str(r#"{"1512": {"moves": ["streaming-accumulate-pairs"]}}"#).unwrap();
        let mut moves = IndexMap::new();
        moves.insert(
            "streaming-accumulate-pairs".to_string(),
            "clean".to_string(),
        );
        assert!(!record_alt_walk(
            &mut problems,
            "1512",
            &moves,
            &HashSet::new()
        ));
        assert!(problems["1512"].get("alt_walks").is_none());
        assert!(!record_alt_walk(
            &mut Map::new(),
            "9999",
            &IndexMap::new(),
            &skipped
        ));
    }

    const FOLLOWUP_SOLVE: &str = "\"\"\"\n1539. Kth Missing Positive Number\n\nGiven an array arr sorted in strictly increasing order, return the kth\nmissing positive integer.\n\nFollow up:\n\nCould you solve this problem in less than O(n) complexity?\n\n---\nFollow up: none of this line is the statement.\n\"\"\"\n\n\nclass Solution:\n    def findKthPositive(self, arr, k):\n        return k\n";

    #[test]
    fn followups() {
        let q = "Could you solve this problem in less than O(n) complexity?";
        assert_eq!(followup_of(FOLLOWUP_SOLVE), q);
        assert_eq!(
            followup_of(&FOLLOWUP_SOLVE.replace("Follow up:\n\nCould", "Follow-up: Could")),
            q
        );
        assert_eq!(
            followup_of(
                &FOLLOWUP_SOLVE.replace("complexity?\n", "complexity?\n\nConstraints:\n\n1 <= k\n")
            ),
            q
        );
        assert_eq!(followup_of(SOLVE), "");
        assert_eq!(
            followup_of(&SOLVE.replace("Peeked at", "Follow up: I peeked at")),
            ""
        );
    }

    /// utils/tests/test_judge_queue.py: the placeholder's shape.
    const DRILL: &str = "\"\"\"\nDRILL: Slide, Never Shrink\nTRAINS: sliding-window, prefix-sum\nGrow the window.\n\n---\nasked for a walkthrough on the shrink step\n\"\"\"\nclass Solution:\n    pass\n";

    fn nodes() -> HashSet<String> {
        ["sliding-window", "prefix-sum", "two-pointers"]
            .iter()
            .map(|s| s.to_string())
            .collect()
    }

    fn problem_moves(p: &str) -> Vec<String> {
        if p == "1539" {
            vec!["two-pointers".into(), "prefix-sum".into()]
        } else {
            vec![]
        }
    }

    fn at(y: i32, mo: u32, d: u32, h: u32, mi: u32) -> DateTime<Utc> {
        chrono::NaiveDate::from_ymd_opt(y, mo, d)
            .unwrap()
            .and_hms_opt(h, mi, 0)
            .unwrap()
            .and_utc()
    }

    #[test]
    fn placeholders() {
        let drills = DrillMap::new();
        let path = "solved/d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py";
        let e = stub_entry(
            path,
            DRILL,
            &nodes(),
            &problem_moves,
            &drills,
            at(2026, 9, 6, 4, 32),
        );
        assert_eq!(e["problem"], "drill");
        assert_eq!(e["date"], "2026-09-06");
        assert_eq!(
            e["moves"],
            json!({"sliding-window": "clean", "prefix-sum": "clean"})
        );
        assert_eq!(e["pending"], "2026-09-06T04:32:00+00:00");
        // the level word in the notes is the mark
        assert_eq!(
            e["assist"],
            json!({"sliding-window": "walkthrough", "prefix-sum": "walkthrough"})
        );
        // a problem: its canonical walk, no assist
        let e = stub_entry(
            "solved/p1539_Kth_Missing_2026_09_05T21_08_16_000000_00_00Z.py",
            "\"\"\"\n1539. Kth Missing\n\"\"\"\nclass Solution:\n    pass\n",
            &nodes(),
            &problem_moves,
            &drills,
            Utc::now(),
        );
        assert_eq!(e["problem"], "1539");
        assert_eq!(
            e["moves"],
            json!({"two-pointers": "clean", "prefix-sum": "clean"})
        );
        assert!(e.get("assist").is_none());
        // a failed file marks no move
        let e = stub_entry(
            "solved/d_Slide_Never_Shrink_FAILED_2026_09_06T04_31_57_473199_00_00Z.py",
            DRILL,
            &nodes(),
            &problem_moves,
            &drills,
            Utc::now(),
        );
        assert_eq!(e["moves"], json!({}));
        assert_eq!(e["problem"], "drill");
        assert!(e["pending"].as_str().is_some_and(|p| !p.is_empty()));
        // unknown trains are dropped and the rep still exists
        let e = stub_entry(
            "solved/d_X_2026_09_06T04_31_57_473199_00_00Z.py",
            "\"\"\"\nDRILL: X\nTRAINS: no-such-node\n\"\"\"\n",
            &nodes(),
            &problem_moves,
            &drills,
            Utc::now(),
        );
        assert_eq!(e["moves"], json!({}));
    }

    #[test]
    fn trains_come_from_drills_json_not_the_file() {
        let mut drills = DrillMap::new();
        drills.insert(
            "d9".into(),
            kg::data::DrillEntry {
                title: "Slide, Never Shrink".into(),
                after: vec![],
                trains: Some(vec!["two-pointers".into()]),
            },
        );
        let no_header = DRILL.replace("TRAINS: sliding-window, prefix-sum\n", "");
        assert_eq!(
            trains_in(&no_header, &drills),
            vec!["two-pointers".to_string()]
        );
        assert_eq!(
            trains_in(DRILL, &DrillMap::new()),
            vec!["sliding-window".to_string(), "prefix-sum".to_string()]
        );
    }

    #[test]
    fn judge_titles() {
        assert_eq!(
            judge_title("solved/d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py"),
            "Slide Never Shrink"
        );
        assert_eq!(
            judge_title("solved/p542_01_Matrix_FAILED_2026_09_03T03_48_58_768516_00_00Z.py"),
            "542. 01 Matrix"
        );
    }

    // --- two writers, one file; the commit rule, in a scratch git repo ---------

    fn scratch(name: &str) -> PathBuf {
        let d = std::env::temp_dir().join(format!("kg_extract_{}_{name}", std::process::id()));
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(d.join("graph")).unwrap();
        std::fs::create_dir_all(d.join("solved")).unwrap();
        std::fs::write(d.join("graph/evidence.json"), r#"{"evidence": {}}"#).unwrap();
        d
    }

    #[test]
    fn a_landing_judge_does_not_clobber_the_next_placeholder() {
        let root = scratch("writers");
        let stale = pyjson::load(&root.join("graph/evidence.json")).unwrap();
        pyjson::store_evidence_entry(
            &root,
            "solved/next.py",
            &json!({"date": "2026-09-06", "moves": {}, "pending": "x"}),
        )
        .unwrap();
        assert!(stale["evidence"].get("solved/next.py").is_none());
        let fresh = pyjson::store_evidence_entry(
            &root,
            "solved/judged.py",
            &json!({"date": "2026-09-06", "moves": {"prefix-sum": "clean"}}),
        )
        .unwrap();
        let keys: HashSet<String> = fresh.as_object().unwrap().keys().cloned().collect();
        assert_eq!(
            keys,
            ["solved/next.py".to_string(), "solved/judged.py".to_string()].into()
        );
        let _ = std::fs::remove_dir_all(&root);
    }

    fn git(root: &Path, args: &[&str]) -> String {
        let out = Command::new("git")
            .args(args)
            .current_dir(root)
            .output()
            .unwrap();
        assert!(
            out.status.success(),
            "git {:?}: {}",
            args,
            String::from_utf8_lossy(&out.stderr)
        );
        String::from_utf8_lossy(&out.stdout).into_owned()
    }

    fn repo(name: &str) -> (PathBuf, String) {
        let root = scratch(name);
        git(&root, &["init", "-q", "-b", "master"]);
        git(&root, &["config", "user.email", "t@t"]);
        git(&root, &["config", "user.name", "t"]);
        let path = "solved/d_Slide_Never_Shrink_2026_09_06T04_31_57_473199_00_00Z.py".to_string();
        std::fs::write(root.join(&path), DRILL).unwrap();
        std::fs::write(root.join("current.py"), "").unwrap();
        git(&root, &["add", "."]);
        git(
            &root,
            &[
                "commit",
                "-qm",
                "drill: Slide, Never Shrink\n\nsolve time: 1m 2s",
            ],
        );
        (root, path)
    }

    fn judged_entry() -> Value {
        json!({"date": "2026-09-06", "problem": "drill", "moves": {"sliding-window": "struggled"}, "summary": "The loop grows r and never shrinks."})
    }

    fn commits(root: &Path, r: &str) -> Vec<String> {
        git(root, &["log", "--format=%s", r])
            .lines()
            .map(String::from)
            .collect()
    }

    fn tracked_status(root: &Path) -> Vec<String> {
        git(root, &["status", "--porcelain"])
            .lines()
            .filter(|l| !l.starts_with("??"))
            .map(String::from)
            .collect()
    }

    #[test]
    fn the_judge_folds_into_the_solves_commit_when_it_is_head() {
        let (root, path) = repo("fold_head");
        pyjson::store_evidence_entry(&root, &path, &judged_entry()).unwrap();
        std::fs::write(root.join("current.py"), "# half typed next solve").unwrap();
        let out = commit_judgement(&root, &[(path.clone(), judged_entry())], false);
        assert_eq!(out, "judge: folded into drill: Slide, Never Shrink");
        assert_eq!(commits(&root, "HEAD"), vec!["drill: Slide, Never Shrink"]);
        assert_eq!(tracked_status(&root), vec![" M current.py"]); // never swept in
        let shown = git(&root, &["show", "--name-only", "--format=", "HEAD"]);
        assert!(shown.contains("graph/evidence.json") && shown.contains("current.py"));
        assert!(git(&root, &["show", "HEAD:graph/evidence.json"]).contains("never shrinks"));
        let _ = std::fs::remove_dir_all(&root);
    }

    #[test]
    fn the_judge_folds_from_the_next_branch_and_rebases_it() {
        let (root, path) = repo("fold_branch");
        git(&root, &["checkout", "-qb", "2"]);
        std::fs::write(root.join("current.py"), "# statement of the next one").unwrap();
        git(&root, &["commit", "-qam", "Next"]);
        std::fs::write(
            root.join("current.py"),
            "# statement of the next one\n# and my half solve",
        )
        .unwrap();
        pyjson::store_evidence_entry(&root, &path, &judged_entry()).unwrap();
        let out = commit_judgement(&root, &[(path.clone(), judged_entry())], false);
        assert!(out.starts_with("judge: folded into"), "{out}");
        assert_eq!(
            git(&root, &["rev-parse", "--abbrev-ref", "HEAD"]).trim(),
            "2"
        );
        assert_eq!(commits(&root, "master"), vec!["drill: Slide, Never Shrink"]);
        assert_eq!(
            commits(&root, "2"),
            vec!["Next", "drill: Slide, Never Shrink"]
        );
        assert_eq!(
            git(&root, &["merge-base", "master", "2"]).trim(),
            git(&root, &["rev-parse", "master"]).trim()
        );
        assert!(git(&root, &["show", "master:graph/evidence.json"]).contains("never shrinks"));
        assert_eq!(tracked_status(&root), vec![" M current.py"]);
        assert!(std::fs::read_to_string(root.join("current.py"))
            .unwrap()
            .ends_with("my half solve"));
        // nothing left for the squash-merge to conflict on
        git(&root, &["stash", "-q"]);
        git(&root, &["checkout", "-q", "master"]);
        git(&root, &["merge", "-q", "--squash", "2"]);
        let _ = std::fs::remove_dir_all(&root);
    }

    #[test]
    fn the_judge_rebases_a_parked_branch_too() {
        let (root, path) = repo("fold_parked");
        git(&root, &["checkout", "-qb", "parked"]);
        std::fs::write(root.join("current.py"), "# parked statement").unwrap();
        git(&root, &["commit", "-qam", "Parked"]);
        git(
            &root,
            &["commit", "-q", "--allow-empty", "-m", "sleeping: 2. Parked"],
        );
        let stamp = git(&root, &["show", "-s", "--format=%at %ct", "parked"]);
        git(&root, &["checkout", "-q", "master"]);
        pyjson::store_evidence_entry(&root, &path, &judged_entry()).unwrap();
        let out = commit_judgement(&root, &[(path.clone(), judged_entry())], false);
        assert!(out.starts_with("judge: folded into"), "{out}");
        assert_eq!(
            commits(&root, "parked"),
            vec![
                "sleeping: 2. Parked",
                "Parked",
                "drill: Slide, Never Shrink"
            ]
        );
        assert_eq!(
            git(&root, &["merge-base", "master", "parked"]).trim(),
            git(&root, &["rev-parse", "master"]).trim()
        );
        assert_eq!(
            git(&root, &["show", "-s", "--format=%at %ct", "parked"]),
            stamp
        );
        let _ = std::fs::remove_dir_all(&root);
    }

    #[test]
    fn the_judge_never_rewrites_a_pushed_solve() {
        let (root, path) = repo("pushed");
        git(&root, &["update-ref", "refs/remotes/origin/master", "HEAD"]);
        pyjson::store_evidence_entry(&root, &path, &judged_entry()).unwrap();
        let out = commit_judgement(&root, &[(path.clone(), judged_entry())], false);
        assert!(
            out.starts_with("judge: committed judge: Slide Never Shrink (solve already pushed"),
            "{out}"
        );
        assert_eq!(
            commits(&root, "HEAD"),
            vec!["judge: Slide Never Shrink", "drill: Slide, Never Shrink"]
        );
        let body = git(&root, &["log", "-1", "--format=%b"]);
        assert!(body.contains("sliding-window=struggled") && body.contains("never shrinks"));
        let _ = std::fs::remove_dir_all(&root);
    }

    #[test]
    fn a_branch_that_does_not_replay_keeps_the_judges_commit_on_top() {
        let (root, path) = repo("noreplay");
        git(&root, &["checkout", "-qb", "2"]);
        std::fs::write(
            root.join("graph/evidence.json"),
            format!(r#"{{"evidence": {{"{path}": {{"date": "2026-09-06", "moves": {{"prefix-sum": "clean"}}}}}}}}"#),
        )
        .unwrap();
        git(&root, &["commit", "-qam", "hand edit"]);
        git(&root, &["checkout", "-q", "master"]);
        let before = git(&root, &["rev-parse", "master", "2"]);
        pyjson::store_evidence_entry(&root, &path, &judged_entry()).unwrap();
        let out = commit_judgement(&root, &[(path.clone(), judged_entry())], false);
        assert!(
            out.contains("(not folded:") && out.contains("does not replay cleanly on 2"),
            "{out}"
        );
        assert_ne!(git(&root, &["rev-parse", "master", "2"]), before);
        assert_eq!(
            commits(&root, "master"),
            vec!["judge: Slide Never Shrink", "drill: Slide, Never Shrink"]
        );
        assert_eq!(
            commits(&root, "2"),
            vec!["hand edit", "drill: Slide, Never Shrink"]
        );
        assert!(git(&root, &["worktree", "list"]).lines().count() == 1);
        let _ = std::fs::remove_dir_all(&root);
    }
}
