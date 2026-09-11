// What the picker reads from git and the clock rather than the graph
// files: the parked problems (`<num>-slept` branches and their marker
// commits), the session-start count and the seconds solved since Manila
// midnight (utils/kg/is_session_start), the mined solve times behind the
// pacing forecast (kg_lib.mined_solve_times, cached per HEAD in
// .solvetimes_cache.json), and the judge queue.

use std::collections::{HashMap, HashSet};
use std::path::Path;
use std::process::{Command, Stdio};
use std::rc::Rc;

use chrono::{DateTime, Duration, NaiveDate, NaiveDateTime, TimeZone, Utc};

use crate::ctx::{Ctx, PView};
use crate::data::{env_str, manila, PENDING_STALE_SECONDS};
use crate::evidence::Evidence;
use crate::status::{input_tree, is_solid, Statuses};

fn git_out(root: &Path, args: &[&str]) -> String {
    Command::new("git")
        .args(args)
        .current_dir(root)
        .stderr(Stdio::null())
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
        .unwrap_or_default()
}

/// What the picker reads from git, read once per process and kept on
/// disk between runs (.next_cache.json, gitignored): the heads with
/// their commit hashes (`git show-ref --heads`, one call), the marker
/// commits of every `<num>-slept` branch (kept by branch tip hash), and
/// the solve commits of the last three days (kept by HEAD hash and day).
/// A hash that has not moved is the same history, so nothing is re-read
/// that git would answer the same way.
#[derive(Clone, Default)]
pub struct GitState {
    pub head: String,
    pub heads: Vec<(String, String)>,
    pub branch_events: HashMap<String, (String, Vec<(i64, String)>)>,
    /// (author ts, body, files added) per commit of the 3-day window
    pub recent: Vec<(i64, String, Vec<String>)>,
}

fn cache_path(root: &Path) -> std::path::PathBuf {
    root.join(".next_cache.json")
}

fn read_head(root: &Path) -> Option<String> {
    // .git/HEAD: "ref: refs/heads/x" or a bare hash (a worktree's .git
    // file says where the real directory is)
    let dot_git = root.join(".git");
    let git_dir = if dot_git.is_file() {
        let text = std::fs::read_to_string(&dot_git).ok()?;
        let rest = text.trim().strip_prefix("gitdir:")?.trim();
        let p = std::path::PathBuf::from(rest);
        if p.is_absolute() {
            p
        } else {
            root.join(p)
        }
    } else {
        dot_git
    };
    let head = std::fs::read_to_string(git_dir.join("HEAD")).ok()?;
    Some(head.trim().to_string())
}

fn load_state(ctx: &Ctx) -> Rc<GitState> {
    if let Some(g) = ctx.git.borrow().as_ref() {
        return g.clone();
    }
    let fetched = ctx
        .git_prefetch
        .borrow_mut()
        .take()
        .and_then(|h| h.join().ok());
    let st = Rc::new(fetched.unwrap_or_else(|| fetch_git_state(&ctx.root)));
    *ctx.git.borrow_mut() = Some(st.clone());
    st
}

/// The git state read fresh (cache checked, misses fetched and written).
/// Runs on a thread from main's first line: git and the cache file are
/// read while the graph JSON parses.
pub fn fetch_git_state(root: &Path) -> GitState {
    let mut st = GitState::default();
    // the heads, one call
    for line in git_out(root, &["show-ref", "--heads"]).lines() {
        if let Some((sha, name)) = line.split_once(' ') {
            if let Some(short) = name.strip_prefix("refs/heads/") {
                st.heads.push((short.to_string(), sha.to_string()));
            }
        }
    }
    st.head = match read_head(root) {
        Some(h) if h.starts_with("ref: ") => {
            let name = h["ref: ".len()..].trim().to_string();
            let short = name.strip_prefix("refs/heads/").unwrap_or(&name);
            st.heads
                .iter()
                .find(|(n, _)| n == short)
                .map(|(_, sha)| sha.clone())
                .unwrap_or_else(|| git_out(root, &["rev-parse", "HEAD"]).trim().to_string())
        }
        Some(h) if !h.is_empty() => h,
        _ => git_out(root, &["rev-parse", "HEAD"]).trim().to_string(),
    };
    let cached = crate::data::read_json(&cache_path(root)).unwrap_or(serde_json::Value::Null);
    let mut dirty = false;
    // the slept branches' marker commits, by tip hash
    for (name, sha) in &st.heads {
        if !name.ends_with("-slept") {
            continue;
        }
        let hit = cached["branches"][name].as_object().and_then(|b| {
            if b.get("sha")?.as_str()? != sha {
                return None;
            }
            let events = b
                .get("events")?
                .as_array()?
                .iter()
                .filter_map(|e| Some((e.get(0)?.as_i64()?, e.get(1)?.as_str()?.to_string())))
                .collect();
            Some(events)
        });
        let events = match hit {
            Some(e) => e,
            None => {
                dirty = true;
                git_branch_events(root, name)
            }
        };
        st.branch_events.insert(name.clone(), (sha.clone(), events));
    }
    // the last three days of solve commits, by HEAD and day
    let day = crate::data::real_today().format("%Y-%m-%d").to_string();
    let hit = cached["log"].as_object().and_then(|l| {
        if l.get("head")?.as_str()? != st.head || l.get("day")?.as_str()? != day {
            return None;
        }
        Some(
            l.get("commits")?
                .as_array()?
                .iter()
                .filter_map(|c| {
                    Some((
                        c.get(0)?.as_i64()?,
                        c.get(1)?.as_str()?.to_string(),
                        c.get(2)?
                            .as_array()?
                            .iter()
                            .filter_map(|f| f.as_str().map(String::from))
                            .collect(),
                    ))
                })
                .collect::<Vec<_>>(),
        )
    });
    st.recent = match hit {
        Some(r) => r,
        None => {
            dirty = true;
            git_recent(root)
        }
    };
    if dirty {
        let doc = serde_json::json!({
            "branches": st.branch_events.iter().map(|(n, (sha, ev))| {
                (n.clone(), serde_json::json!({"sha": sha, "events": ev}))
            }).collect::<serde_json::Map<String, serde_json::Value>>(),
            "log": {"head": st.head, "day": day, "commits": st.recent},
        });
        let _ = std::fs::write(cache_path(root), doc.to_string());
    }
    st
}

/// kg_lib.branch_events, straight from git: (unix ts, subject) of a
/// branch's own commits, oldest first.
fn git_branch_events(root: &Path, branch: &str) -> Vec<(i64, String)> {
    let out = git_out(
        root,
        &[
            "log",
            "--reverse",
            "--format=%ct%x09%s",
            branch,
            "--not",
            "master",
        ],
    );
    let mut events = Vec::new();
    for line in out.lines() {
        let (ts, subj) = line.split_once('\t').unwrap_or((line, ""));
        if !ts.is_empty() && ts.chars().all(|c| c.is_ascii_digit()) {
            events.push((ts.parse().unwrap_or(0), subj.to_string()));
        }
    }
    events
}

/// The commits of the last three days adding files under solved/ or
/// drills/: (author ts, message, files). is_session_start reads the
/// same set twice (names, then bodies); one call carries both.
fn git_recent(root: &Path) -> Vec<(i64, String, Vec<String>)> {
    let out = git_out(
        root,
        &[
            "log",
            "--since=3.days",
            "--diff-filter=A",
            "--format=%x01%at%x01%B%x02",
            "--name-only",
            "--",
            "solved/",
            "drills/",
        ],
    );
    let parts: Vec<&str> = out.split('\x01').skip(1).collect();
    let mut recent = Vec::new();
    for pair in parts.chunks(2) {
        if pair.len() < 2 {
            break;
        }
        let ts: i64 = pair[0].trim().parse().unwrap_or(0);
        let (body, tail) = pair[1].split_once('\x02').unwrap_or((pair[1], ""));
        let files: Vec<String> = tail.split_whitespace().map(String::from).collect();
        recent.push((ts, body.to_string(), files));
    }
    recent
}

pub fn head_sha(ctx: &Ctx) -> String {
    load_state(ctx).head.clone()
}

/// kg_lib.branch_events for a slept branch, from the cached state.
pub fn branch_events(ctx: &Ctx, branch: &str) -> Vec<(i64, String)> {
    let st = load_state(ctx);
    match st.branch_events.get(branch) {
        Some((_, e)) => e.clone(),
        None => git_branch_events(&ctx.root, branch),
    }
}

/// kg_lib.slept_branches: {problem number: branch} of every `-slept` branch.
pub fn slept_branches(ctx: &Ctx) -> Vec<(String, String)> {
    let st = load_state(ctx);
    let mut out: Vec<(String, String)> = st
        .heads
        .iter()
        .filter(|(n, _)| n.ends_with("-slept"))
        .map(|(n, _)| (n[..n.len() - "-slept".len()].to_string(), n.clone()))
        .collect();
    // for-each-ref lists refs in name order
    out.sort_by(|a, b| a.1.cmp(&b.1));
    out
}

#[derive(Clone, Debug)]
pub struct SleepRec {
    pub pnum: String,
    pub branch: String,
    pub title: String,
    pub slept: i64,
    pub cycles: i64,
}

fn manila_date_of(ts: i64) -> NaiveDate {
    manila().timestamp_opt(ts, 0).unwrap().date_naive()
}

/// kg_lib.sleep_records: the unresolved parks, in branch order.
pub fn sleep_records(ctx: &Ctx, pv: &PView, ev: &Evidence) -> Vec<SleepRec> {
    let mut recs = Vec::new();
    for (pnum, branch) in slept_branches(ctx) {
        let Some(p) = pv.get(&pnum) else { continue };
        let events = branch_events(ctx, &branch);
        let marks: Vec<i64> = events
            .iter()
            .filter(|(_, s)| s.starts_with("sleeping:"))
            .map(|(t, _)| *t)
            .collect();
        let ts = match marks.last() {
            Some(t) => *t,
            None => match events.last() {
                Some((t, _)) => *t,
                None => continue,
            },
        };
        let slept_day = manila_date_of(ts).format("%Y-%m-%d").to_string();
        if ev
            .problem_recs(&pnum)
            .iter()
            .any(|(d, _, _)| *d >= slept_day.as_str())
        {
            continue;
        }
        recs.push(SleepRec {
            pnum: pnum.clone(),
            branch,
            title: p.title.clone(),
            slept: ts,
            cycles: (marks.len() as i64).max(1),
        });
    }
    recs
}

/// kg_lib.sleep_state: (asleep, woken); woken is always empty.
pub fn sleep_state(ctx: &Ctx, pv: &PView, ev: &Evidence) -> Vec<String> {
    let mut recs = sleep_records(ctx, pv, ev);
    recs.sort_by_key(|r| (-r.cycles, r.slept));
    recs.into_iter().map(|r| r.pnum).collect()
}

/// kg_lib.sleep_rows: (pnum, title, rusty nodes, since, cycles) per park.
pub fn sleep_rows(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
) -> Vec<(String, String, Vec<String>, String, i64)> {
    let recs = sleep_records(ctx, pv, ev);
    if recs.is_empty() {
        return vec![];
    }
    let by_pnum: HashMap<String, SleepRec> =
        recs.into_iter().map(|r| (r.pnum.clone(), r)).collect();
    let mut rows = Vec::new();
    for pnum in sleep_state(ctx, pv, ev) {
        let rec = &by_pnum[&pnum];
        let since = manila()
            .timestamp_opt(rec.slept, 0)
            .unwrap()
            .format("%Y-%m-%dT%H:%M")
            .to_string();
        let moves = pv.get(&pnum).map(|p| p.moves.clone()).unwrap_or_default();
        let mut rusty: Vec<String> = input_tree(&moves, &ctx.nodes)
            .into_iter()
            .filter(|n| !is_solid(statuses, n))
            .collect();
        rusty.sort();
        rows.push((pnum, rec.title.clone(), rusty, since, rec.cycles));
    }
    rows
}

// ---- is_session_start ---------------------------------------------------

fn manila_midnight_ts() -> i64 {
    let now = Utc::now().with_timezone(&manila());
    now.date_naive()
        .and_hms_opt(0, 0, 0)
        .unwrap()
        .and_local_timezone(manila())
        .unwrap()
        .timestamp()
}

/// is_session_start.solves_today: solve files authored since local
/// midnight (added under solved/ or drills/).
pub fn solves_today(ctx: &Ctx) -> Vec<String> {
    let midnight = manila_midnight_ts();
    let st = load_state(ctx);
    let mut solves: HashSet<String> = HashSet::new();
    for (ts, _, files) in &st.recent {
        if *ts >= midnight {
            solves.extend(files.iter().cloned());
        }
    }
    let mut v: Vec<String> = solves.into_iter().collect();
    v.sort();
    v
}

pub fn warmup_threshold() -> i64 {
    env_str("NEXT_WARMUP_COUNT").trim().parse().unwrap_or(2)
}

/// is_session_start: fewer than NEXT_WARMUP_COUNT solves since midnight.
pub fn is_session_start(ctx: &Ctx) -> bool {
    (solves_today(ctx).len() as i64) < warmup_threshold()
}

/// kg_next.solved_today_pnums: the problem numbers solved today.
pub fn solved_today_pnums(ctx: &Ctx) -> HashSet<String> {
    let mut out = HashSet::new();
    for f in solves_today(ctx) {
        let name = f.rsplit('/').next().unwrap_or(&f);
        if let Some(rest) = name.strip_prefix('p') {
            let num = rest.split('_').next().unwrap_or("");
            if !num.is_empty() && num.chars().all(|c| c.is_ascii_digit()) {
                out.insert(num.to_string());
            }
        }
    }
    out
}

fn solve_time_secs(body: &str) -> Option<i64> {
    // r"solve time: (\d+)m (\d+)s"
    let idx = body.find("solve time: ")?;
    let rest = &body[idx + "solve time: ".len()..];
    let (m, rest) = rest.split_once('m')?;
    if m.is_empty() || !m.chars().all(|c| c.is_ascii_digit()) {
        return solve_time_secs(&body[idx + 1..]);
    }
    let rest = rest.strip_prefix(' ')?;
    let s: String = rest.chars().take_while(|c| c.is_ascii_digit()).collect();
    if s.is_empty() || !rest[s.len()..].starts_with('s') {
        return solve_time_secs(&body[idx + 1..]);
    }
    Some(m.parse::<i64>().ok()? * 60 + s.parse::<i64>().ok()?)
}

/// is_session_start.solve_seconds_today.
pub fn solve_seconds_today(ctx: &Ctx) -> i64 {
    let midnight = manila_midnight_ts();
    let st = load_state(ctx);
    let mut total = 0;
    for (ts, body, _) in &st.recent {
        if *ts < midnight {
            continue;
        }
        if let Some(s) = solve_time_secs(body) {
            total += s;
        }
    }
    total
}

// ---- mined solve times --------------------------------------------------

pub type SolveRep = (String, NaiveDate, i64, String);

/// kg_lib.mined_solve_times(with_file=True): (key, date, seconds, file) per
/// timed solve commit, oldest first; cached per HEAD.
pub fn mined_solve_times(ctx: &Ctx) -> Vec<SolveRep> {
    if let Some(v) = ctx.solve_times.borrow().as_ref() {
        return v.clone();
    }
    let root = &ctx.root;
    let head = head_sha(ctx);
    let cache = root.join(".solvetimes_cache.json");
    let mut reps: Option<Vec<SolveRep>> = None;
    if let Some(v) = crate::data::read_json(&cache) {
        if v.get("head").and_then(|h| h.as_str()) == Some(head.as_str()) {
            let parsed: Option<Vec<SolveRep>> = v.get("reps").and_then(|r| r.as_array()).map(|a| {
                a.iter()
                    .filter_map(|t| {
                        let t = t.as_array()?;
                        Some((
                            crate::data::value_str(t.first()?),
                            crate::data::parse_date(t.get(1)?.as_str()?),
                            t.get(2)?.as_i64()?,
                            t.get(3)?.as_str()?.to_string(),
                        ))
                    })
                    .collect()
            });
            reps = parsed;
        }
    }
    let reps = match reps {
        Some(r) => r,
        None => {
            let r = mine_solve_times(root);
            let json = serde_json::json!({
                "head": head,
                "reps": r.iter().map(|(k, d, s, f)| serde_json::json!([k, d.format("%Y-%m-%d").to_string(), s, f])).collect::<Vec<_>>(),
            });
            let _ = std::fs::write(&cache, json.to_string());
            r
        }
    };
    *ctx.solve_times.borrow_mut() = Some(reps.clone());
    reps
}

fn mine_solve_times(root: &Path) -> Vec<SolveRep> {
    let out = git_out(
        root,
        &[
            "log",
            "--diff-filter=A",
            "--format=%x01%at%x01%B%x02",
            "--name-only",
            "--",
            "solved/",
        ],
    );
    let parts: Vec<&str> = out.split('\x01').skip(1).collect();
    let mut reps: Vec<SolveRep> = Vec::new();
    for pair in parts.chunks(2) {
        if pair.len() < 2 {
            break;
        }
        let at: i64 = pair[0].trim().parse().unwrap_or(0);
        let (body, tail) = pair[1].split_once('\x02').unwrap_or((pair[1], ""));
        let Some(secs) = solve_time_secs(body) else {
            continue;
        };
        let added: Vec<&str> = tail
            .lines()
            .filter_map(|l| l.strip_prefix("solved/"))
            .filter(|l| l.ends_with(".py") && !l.contains(char::is_whitespace))
            .collect();
        if added.len() != 1 || added[0].contains("FAILED") || !(0 < secs && secs < 36000) {
            continue;
        }
        let name = added[0];
        let key = if let Some(rest) = name.strip_prefix('p') {
            let digits: String = rest.chars().take_while(|c| c.is_ascii_digit()).collect();
            if !digits.is_empty() && rest[digits.len()..].starts_with('_') {
                Some(digits)
            } else {
                None
            }
        } else {
            None
        };
        let key = key.or_else(|| {
            // r"d_(.+?)_\d{4}_": the shortest stem before an _YYYY_ block
            let rest = name.strip_prefix("d_")?;
            let b = rest.as_bytes();
            for i in 1..b.len() {
                if b[i] == b'_'
                    && i + 6 <= b.len()
                    && b[i + 1..i + 5].iter().all(u8::is_ascii_digit)
                    && b[i + 5] == b'_'
                {
                    return Some(format!("d:{}", &rest[..i]));
                }
            }
            None
        });
        if let Some(key) = key {
            let d = manila().timestamp_opt(at, 0).unwrap().date_naive();
            reps.push((key, d, secs, format!("solved/{name}")));
        }
    }
    reps.sort_by_key(|r| r.1);
    reps
}

// ---- the judge queue ----------------------------------------------------

/// kg_lib.pending_judgements: [(path, seconds pending)], oldest first.
pub fn pending_judgements(ev: &Evidence) -> Vec<(String, f64)> {
    let now = Utc::now().timestamp() as f64;
    let mut out = Vec::new();
    for (path, rec) in &ev.recs {
        let Some(stamp) = &rec.pending else { continue };
        if stamp.is_empty() {
            continue;
        }
        let age = match DateTime::parse_from_rfc3339(stamp) {
            Ok(dt) => now - dt.timestamp() as f64,
            Err(_) => match NaiveDateTime::parse_from_str(stamp, "%Y-%m-%dT%H:%M:%S%.f")
                .or_else(|_| NaiveDateTime::parse_from_str(stamp, "%Y-%m-%dT%H:%M:%S"))
            {
                Ok(naive) => now - naive.and_local_timezone(manila()).unwrap().timestamp() as f64,
                Err(_) => f64::INFINITY,
            },
        };
        out.push((path.clone(), age));
    }
    out.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    out
}

pub fn is_stale(age: f64) -> bool {
    age > PENDING_STALE_SECONDS
}

/// kg_lib.spawn_judge: one detached kg_extract on the file.
pub fn spawn_judge(root: &Path, path: &str) {
    let venv = root.join(".venv/bin/python3");
    let py = if venv.exists() {
        venv
    } else {
        std::path::PathBuf::from("python3")
    };
    let pythonpath = format!("{}:{}", root.join("utils").display(), env_str("PYTHONPATH"));
    let log = std::fs::OpenOptions::new()
        .append(true)
        .create(true)
        .open(root.join(".judge.log"));
    let Ok(log) = log else { return };
    let err = log.try_clone().ok();
    let mut cmd = Command::new(py);
    cmd.arg(root.join("utils/kg/kg_extract"))
        .arg("--file")
        .arg(path)
        .arg("--commit")
        .current_dir(root)
        .env("PYTHONPATH", pythonpath)
        .stdin(Stdio::null())
        .stdout(Stdio::from(log));
    if let Some(e) = err {
        cmd.stderr(Stdio::from(e));
    }
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        cmd.process_group(0);
    }
    let _ = cmd.spawn();
}

/// The Manila day `days` back from `day`.
pub fn days_ago(day: NaiveDate, days: i64) -> NaiveDate {
    day - Duration::days(days)
}
