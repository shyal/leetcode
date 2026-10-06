// kg_llm_next - a second opinion on the pick. The model reads what `make
// next` printed and the whole solve history, compressed the way the 2025
// recommender compressed it: the last ten solves as code and notes, the
// last three weeks as full records, every older rep as one line with a
// ten-word summary of the solution. It names the problem it would
// schedule, with its reasons.
//
//   make next llm              # the model's pick and the plan behind it
//   make next llm prepare      # prepare that pick: stub + branch, clock on
//   make next sql llm          # the same, inside a group
//   kg_llm_next --context      # the context the model is handed (the tests)
//   kg_llm_next --key          # the cache key
//
// The summaries live in data/summaries.json keyed by the solved file, one
// model call each, made the first time a rep is compressed and never again.
//
// The pick is cached in .llm_next.json under a key made of the evidence file,
// today's date and the words after `next`. So `make next llm` followed by
// `make next llm prepare` prepares the problem that was just read, without a
// second call, and a rep recorded in between changes the key and forces a
// fresh pick.
//
// Ported from utils/kg/kg_llm_next (Python) on 2026-09-12.

use std::collections::HashMap;
use std::process::Command;

use chrono::Duration;
use kg::console::{Console, Text};
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::drills::first_sight_band;
use kg::evidence::{drill_key, Evidence};
use kg::git::mined_solve_times;
use kg::llm::claude_json;
use kg::model::{first_sight_elo_now, solve_ratings};
use kg::pyjson::{self, dumps};
use kg::table::panel_titled;
use regex::Regex;
use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};

const WINDOW_DAYS: i64 = 21;
const FULL_SOLVES: usize = 10;
const PROMPT_VERSION: i64 = 6;
const SUMMARY_WORDS: usize = 10;
/// The rating band of unseen problems handed over as new ground.
const BAND_BELOW: f64 = 150.0;
const BAND_ABOVE: f64 = 300.0;

const SYSTEM_PROMPT: &str = "You schedule the next leetcode problem for one operator. His goal is to get mental\nmodels installed properly: to understand each technique so that it holds on\na problem he has never seen. Passing such a problem at his level, on a\nclock, without help, is the check on that, not the goal itself. You are\ngiven what his own picker printed, and his whole solve history, oldest\nfirst: the last ten solves as code and notes, the last three weeks as full\nrecords, and every older rep as one line with a short summary. Each rep says\nwhether it was the first sight of that problem or a repeat, the minutes it\ntook, how it was judged, and the problem's contest rating against his elo.\nName the one problem he should open next.\n\nRead the history the way a coach reads it. Find what he solves cleanly, what\nhe struggles with, and what he has never met. Build a theory of his weak\nspots from the failures and the notes, and pick the problem that tests that\ntheory.\n\nThe pool is every LeetCode problem, not the picker's queue.\n`unseen_candidates` lists the free problems he has never opened, in his\nrating band; new ground comes from that list. Decide in this order, and stop\nat the first rule that fires:\n1. The first entry of `failed_without_a_clean_unaided_rep_since` whose\n   `days_since_last_learning_rep` is 3 or more: its unaided rep. Drill\n   reps do not count here, only problem reps, and the list already holds\n   the order.\n2. A problem he walked away from today or yesterday without a working\n   solution: a learning rep, look the solution up and step through it.\n3. Otherwise a problem from `unseen_candidates`, at or a little above his\n   elo, that tests the weak spot the recent failures point at. When several\n   fit, take the one closest to his elo.\nA problem he solved cleanly before and has not failed since is never the\npick. Measure a problem by its contest rating against his elo, never by the\nEasy/Medium/Hard label. Never call a problem new when the history shows an\nearlier rep of it. Name the rule that fired in the reason.\n\nWriting rules: short declarative sentences, plain English, no analogies, no\ncoined words. Refer to problems by number and title only. Never name a\ntechnique, a graph node, or a move. Never say a problem should be easy.\nNever tell him when to rest.\n\nReply with one JSON object and nothing else:\n{\n  \"problem\": \"<number>\",\n  \"title\": \"<title>\",\n  \"agrees\": <true if this is the picker's own pick>,\n  \"reason\": \"<two to four sentences>\",\n  \"plan\": [{\"problem\": \"<number>\", \"title\": \"<title>\", \"note\": \"<one sentence>\"}]\n}\nThe plan is the next two or three problems after this one, in order.\n";

fn sibling(ctx: &Ctx, name: &str) -> std::path::PathBuf {
    std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join(name)))
        .unwrap_or_else(|| ctx.root.join("utils/rs/target/release").join(name))
}

/// What `make next` prints for these words, as plain text.
fn picker_frame(ctx: &Ctx, words: &[String]) -> String {
    Command::new(sibling(ctx, "kg_next"))
        .arg("--no-show")
        .args(words)
        .current_dir(&ctx.root)
        .env("COLUMNS", "120")
        .env("TERM", "dumb")
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).into_owned())
        .unwrap_or_default()
}

/// The trailing `# FAILED:` comment of a walked-away file, joined.
fn failure_note(ctx: &Ctx, path: &str) -> String {
    let Ok(text) = std::fs::read_to_string(ctx.root.join(path)) else {
        return String::new();
    };
    text.lines()
        .filter_map(|l| l.strip_prefix("# "))
        .filter(|l| l.starts_with("FAILED"))
        .collect::<Vec<_>>()
        .join(" ")
}

/// Python's round() to an integer: half to even.
fn round_i(x: f64) -> i64 {
    x.round_ties_even() as i64
}

/// One record per rep in the window, oldest first. Move names are left out
/// so the model cannot leak them back.
fn recent_reps(
    ctx: &Ctx,
    ev: &Evidence,
    ratings: &HashMap<String, f64>,
    since: chrono::NaiveDate,
) -> Vec<Value> {
    let times: HashMap<String, i64> = mined_solve_times(ctx)
        .into_iter()
        .map(|(_, _, s, f)| (f, s))
        .collect();
    let drill_name = Regex::new(r"^d_|_\d{4}_\d{2}_\d{2}T.*$").unwrap();
    let mut out: Vec<(String, Value)> = Vec::new();
    for (path, rec) in &ev.recs {
        let Ok(d) = chrono::NaiveDate::parse_from_str(&rec.date, "%Y-%m-%d") else {
            continue;
        };
        if d < since {
            continue;
        }
        let failed = path.contains("_FAILED_");
        let mut item = Map::new();
        item.insert("date".into(), json!(rec.date));
        item.insert("failed".into(), json!(failed));
        item.insert(
            "clean".into(),
            json!(rec.moves.values().filter(|v| *v == "clean").count()),
        );
        item.insert(
            "struggled".into(),
            json!(rec.moves.values().filter(|v| *v == "struggled").count()),
        );
        item.insert("assist".into(), json!(rec.assist_any()));
        let pnum = rec.problem.clone().unwrap_or_default();
        if pnum == "drill" || drill_key(path).is_some() {
            let base = path.rsplit('/').next().unwrap_or(path);
            item.insert(
                "drill".into(),
                json!(drill_name.replace_all(base, "").replace('_', " ")),
            );
        } else {
            item.insert(
                "problem".into(),
                rec.problem
                    .clone()
                    .map(Value::String)
                    .unwrap_or(Value::Null),
            );
            item.insert(
                "title".into(),
                json!(ctx
                    .ro
                    .map
                    .get(&pnum)
                    .map(|p| p.title.clone())
                    .unwrap_or_default()),
            );
            if let Some(r) = ratings.get(&pnum) {
                item.insert("rating".into(), json!(round_i(*r)));
            }
        }
        if let Some(secs) = times.get(path) {
            item.insert("minutes".into(), json!(round_i(*secs as f64 / 60.0)));
        }
        if let Some(note) = rec.note.as_deref().filter(|n| !n.is_empty()) {
            item.insert("note".into(), json!(note));
        }
        if failed {
            item.insert("failure_note".into(), json!(failure_note(ctx, path)));
        }
        out.push((rec.date.clone(), Value::Object(item)));
    }
    out.sort_by(|a, b| a.0.cmp(&b.0)); // stable, as Python's sort
    out.into_iter().map(|(_, v)| v).collect()
}

/// Problems with a failed rep and no clean unaided problem rep since, with
/// the date of their last assisted rep and the days since it, oldest such
/// rep first: rule 1 of the schedule, worked out here so the model reads
/// the order instead of deriving it.
fn open_failures(ctx: &Ctx, ev: &Evidence, ratings: &HashMap<String, f64>) -> Vec<Value> {
    let mut last_fail: HashMap<String, String> = HashMap::new();
    let mut last_clean: HashMap<String, String> = HashMap::new();
    let mut last_assisted: HashMap<String, String> = HashMap::new();
    let mut order: Vec<String> = Vec::new();
    for (path, rec) in &ev.recs {
        let Some(pnum) = rec
            .problem
            .clone()
            .filter(|p| p != "drill" && !p.is_empty())
        else {
            continue;
        };
        if drill_key(path).is_some() {
            continue;
        }
        let later = |m: &mut HashMap<String, String>| {
            let e = m.entry(pnum.clone()).or_default();
            if rec.date > *e {
                *e = rec.date.clone();
            }
        };
        if path.contains("_FAILED_") {
            later(&mut last_fail);
            if !order.contains(&pnum) {
                order.push(pnum.clone());
            }
        } else if rec.assist_any() != "none" {
            later(&mut last_assisted);
        } else if rec.moves.values().all(|v| v == "clean") {
            later(&mut last_clean);
        }
    }
    let today = ctx.today();
    let mut out: Vec<(i64, String, Value)> = Vec::new();
    for pnum in order {
        let d = &last_fail[&pnum];
        if last_clean.get(&pnum).is_some_and(|c| c > d) {
            continue;
        }
        let last_rep = last_assisted.get(&pnum).filter(|a| *a > d);
        let days = last_rep
            .and_then(|a| chrono::NaiveDate::parse_from_str(a, "%Y-%m-%d").ok())
            .map(|a| (today - a).num_days());
        out.push((
            days.unwrap_or(-1),
            pnum.clone(),
            json!({
                "problem": pnum,
                "title": ctx.ro.map.get(&pnum).map(|p| p.title.clone()).unwrap_or_default(),
                "failed": d,
                "rating": ratings.get(&pnum).map(|r| json!(round_i(*r))).unwrap_or(Value::Null),
                "last_learning_rep": last_rep.map(|a| json!(a)).unwrap_or(Value::Null),
                "days_since_last_learning_rep": days.map(|n| json!(n)).unwrap_or(Value::Null),
            }),
        ));
    }
    // most days since the last learning rep first; never studied last
    out.sort_by(|a, b| b.0.cmp(&a.0).then(a.1.cmp(&b.1)));
    out.into_iter().map(|(_, _, v)| v).collect()
}

/// (code, notes) of a solved file: the source after its statement block,
/// cut where the tests start, and what follows `---` in the block.
fn solve_source(ctx: &Ctx, path: &str) -> Option<(String, String)> {
    let full = ctx.root.join(path);
    let lang = kg::lang::of_path(&full)?;
    let text = std::fs::read_to_string(&full).ok()?;
    let tests = Regex::new(r"^(\w+\s*=\s*Solution\(|assert\b|print\()").unwrap();
    let body = kg::lang::strip_header(&text, lang);
    let code: Vec<&str> = body.lines().take_while(|l| !tests.is_match(l)).collect();
    let notes = kg::lang::notes_of(&text, lang)
        .trim_start_matches("notes:")
        .trim()
        .to_string();
    Some((code.join("\n").trim().to_string(), notes))
}

/// data/summaries.json: one ten-word summary per solved file, the 2025
/// recommender's cache, extended here for every rep that lacks one.
struct Summaries {
    path: std::path::PathBuf,
    map: Map<String, Value>,
    dirty: bool,
}

impl Summaries {
    fn load(ctx: &Ctx) -> Summaries {
        let path = ctx.root.join("data/summaries.json");
        let map = pyjson::load(&path)
            .and_then(|v| v.as_object().cloned())
            .unwrap_or_default();
        Summaries {
            path,
            map,
            dirty: false,
        }
    }

    /// The cached summary, or one asked of the judge model and cached.
    fn get(&mut self, ctx: &Ctx, path: &str, title: &str) -> String {
        if let Some(s) = self.map.get(path).and_then(Value::as_str) {
            return s.to_string();
        }
        let Some((code, notes)) = solve_source(ctx, path) else {
            return String::new();
        };
        let prompt = format!(
            "Summarize in {SUMMARY_WORDS} words at most the solution the candidate wrote for {title}. Name the idea, not the problem. Reply with one JSON object: {{\"summary\": \"<words>\"}}\n\nCode:\n{code}\n\nNotes:\n{notes}"
        );
        let system = "You write ten-word summaries of leetcode solutions: the key idea of the code and the notes.";
        let summary = claude_json(&prompt, system, &kg::llm::judge_model("haiku"), 1)
            .ok()
            .and_then(|v| v.get("summary").and_then(Value::as_str).map(str::to_string))
            .unwrap_or_default();
        if !summary.is_empty() {
            self.map.insert(path.to_string(), json!(summary));
            self.dirty = true;
            // a long first fill survives an interruption
            if self.map.len().is_multiple_of(20) {
                self.save();
            }
        }
        summary
    }

    fn save(&self) {
        if self.dirty {
            let _ = pyjson::save(&self.path, &Value::Object(self.map.clone()), Some(1));
        }
    }
}

fn is_drill(path: &str, rec: &kg::data::Rec) -> bool {
    rec.problem.as_deref() == Some("drill") || drill_key(path).is_some()
}

fn outcome(path: &str, rec: &kg::data::Rec) -> String {
    if path.contains("_FAILED_") {
        return "failed".into();
    }
    let struggled = rec.moves.values().filter(|v| *v == "struggled").count();
    let mut s = if struggled == 0 {
        "clean".to_string()
    } else {
        format!("struggled on {struggled}")
    };
    if rec.assist_any() != "none" {
        s.push_str(&format!(", {}", rec.assist_any()));
    }
    s
}

/// The evidence in date order, each with which rep of its problem it is
/// (1 = first sight).
fn dated_reps(ev: &Evidence) -> Vec<(&str, &kg::data::Rec, usize)> {
    let mut idx: Vec<usize> = (0..ev.recs.len()).collect();
    idx.sort_by(|a, b| ev.recs[*a].1.date.cmp(&ev.recs[*b].1.date));
    let mut seen: HashMap<&str, usize> = HashMap::new();
    idx.into_iter()
        .map(|i| {
            let (path, rec) = &ev.recs[i];
            let n = if is_drill(path, rec) {
                0
            } else {
                let e = seen
                    .entry(rec.problem.as_deref().unwrap_or(""))
                    .or_default();
                *e += 1;
                *e
            };
            (path.as_str(), rec, n)
        })
        .collect()
}

/// One line per rep before `since`, oldest first: the 2025 recommender's
/// compressed entry.
fn history_lines(
    ctx: &Ctx,
    ev: &Evidence,
    ratings: &HashMap<String, f64>,
    since: chrono::NaiveDate,
    summaries: &mut Summaries,
) -> Vec<String> {
    let times: HashMap<String, i64> = mined_solve_times(ctx)
        .into_iter()
        .map(|(_, _, s, f)| (f, s))
        .collect();
    let drill_name = Regex::new(r"^d_|_\d{4}_\d{2}_\d{2}T.*$").unwrap();
    let mut out = Vec::new();
    for (path, rec, nth) in dated_reps(ev) {
        let Ok(d) = chrono::NaiveDate::parse_from_str(&rec.date, "%Y-%m-%d") else {
            continue;
        };
        if d >= since {
            continue;
        }
        let secs = rec.seconds.or_else(|| times.get(path).copied());
        let mins = secs
            .map(|s| format!(" {}m", round_i(s as f64 / 60.0)))
            .unwrap_or_default();
        let mut line = if is_drill(path, rec) {
            let base = path.rsplit('/').next().unwrap_or(path);
            format!(
                "{} drill {}{mins} {}",
                rec.date,
                drill_name.replace_all(base, "").replace('_', " "),
                outcome(path, rec)
            )
        } else {
            let pnum = rec.problem.clone().unwrap_or_default();
            let title = ctx
                .ro
                .map
                .get(&pnum)
                .map(|p| p.title.clone())
                .unwrap_or_default();
            let rating = ratings
                .get(&pnum)
                .map(|r| format!(" r{}", round_i(*r)))
                .unwrap_or_default();
            let rep = if nth == 1 {
                "first sight".to_string()
            } else {
                format!("rep {nth}")
            };
            let summary = summaries.get(ctx, path, &format!("{pnum}. {title}"));
            let mut l = format!(
                "{} {pnum}. {title}{rating} {rep}{mins} {}",
                rec.date,
                outcome(path, rec)
            );
            if !summary.is_empty() {
                l.push_str(&format!(": {summary}"));
            }
            l
        };
        if let Some(note) = rec.note.as_deref().filter(|n| !n.is_empty()) {
            let cut: String = note.chars().take(140).collect();
            line.push_str(&format!(" | judge: {cut}"));
        }
        out.push(line);
    }
    out
}

/// The last `n` problem reps as the candidate wrote them: code and notes.
fn latest_solves(ctx: &Ctx, ev: &Evidence, n: usize) -> Vec<Value> {
    let reps = dated_reps(ev);
    let mut out = Vec::new();
    for (path, rec, nth) in reps.iter().rev() {
        if *nth == 0 {
            continue;
        }
        let Some((code, notes)) = solve_source(ctx, path) else {
            continue;
        };
        let pnum = rec.problem.clone().unwrap_or_default();
        out.push(json!({
            "date": rec.date,
            "problem": pnum,
            "title": ctx.ro.map.get(&pnum).map(|p| p.title.clone()).unwrap_or_default(),
            "rep": nth,
            "outcome": outcome(path, rec),
            "code": code,
            "notes": notes,
        }));
        if out.len() == n {
            break;
        }
    }
    out.reverse();
    out
}

/// Problem reps, first sights and unaided in-time first-sight passes over
/// the last `days`: the share of new ground in the serve, and how it went.
fn serve_stats(ctx: &Ctx, ev: &Evidence, days: i64) -> Value {
    let since = ctx.today() - Duration::days(days);
    let (mut reps, mut first, mut passed) = (0, 0, 0);
    for (path, rec, nth) in dated_reps(ev) {
        let Ok(d) = chrono::NaiveDate::parse_from_str(&rec.date, "%Y-%m-%d") else {
            continue;
        };
        if nth == 0 || d < since {
            continue;
        }
        reps += 1;
        if nth == 1 {
            first += 1;
            if outcome(path, rec) == "clean" {
                passed += 1;
            }
        }
    }
    json!({"problem_reps": reps, "first_sights": first, "first_sights_passed_unaided": passed})
}

/// Free problems he has never opened, rated within the band around his
/// elo, closest to his elo first: the new ground the model may pick from.
fn unseen_candidates(
    ctx: &Ctx,
    ev: &Evidence,
    ratings: &HashMap<String, f64>,
    elo: f64,
) -> Vec<Value> {
    let seen = ev.solved_problems();
    // FIRST_SIGHT_WITHIN_BAND narrows the band on both sides, never widens it
    let above = first_sight_band().map_or(BAND_ABOVE, |b| b.min(BAND_ABOVE));
    let below = first_sight_band().map_or(BAND_BELOW, |b| b.min(BAND_BELOW));
    let mut pool: Vec<(f64, &String)> = ratings
        .iter()
        .filter(|(p, r)| {
            **r >= elo - below
                && **r <= elo + above
                && !seen.contains(*p)
                && ctx
                    .meta
                    .get(*p)
                    .is_some_and(|m| !m.paid_only && m.title.is_some())
        })
        .map(|(p, r)| (*r, p))
        .collect();
    pool.sort_by(|a, b| {
        (a.0 - elo)
            .abs()
            .partial_cmp(&(b.0 - elo).abs())
            .unwrap()
            .then(a.1.cmp(b.1))
    });
    pool.into_iter()
        .map(|(r, p)| {
            json!({
                "problem": p,
                "title": ctx.meta[p].title.clone().unwrap_or_default(),
                "rating": round_i(r),
            })
        })
        .collect()
}

fn build_context(ctx: &Ctx, ev: &Evidence, words: &[String]) -> Value {
    let ratings = solve_ratings(ctx);
    let since = ctx.today() - Duration::days(WINDOW_DAYS);
    let mut summaries = Summaries::load(ctx);
    let history = history_lines(ctx, ev, &ratings, since, &mut summaries);
    summaries.save();
    let elo = first_sight_elo_now(ctx, ev);
    json!({
        "today": ctx.today().format("%Y-%m-%d").to_string(),
        "elo": round_i(elo),
        "unseen_candidates": unseen_candidates(ctx, ev, &ratings, elo),
        "picker": picker_frame(ctx, words),
        "serve": {"last_7_days": serve_stats(ctx, ev, 7), "last_30_days": serve_stats(ctx, ev, 30)},
        "failed_without_a_clean_unaided_rep_since": open_failures(ctx, ev, &ratings),
        "history": history,
        "reps": recent_reps(ctx, ev, &ratings, since),
        "latest_solves": latest_solves(ctx, ev, FULL_SOLVES),
    })
}

/// The cache key: the evidence file's bytes, the day, the words, the prompt
/// version. A new rep, a new day or other words ask the model again.
fn context_key(root: &std::path::Path, today: &str, words: &[String]) -> String {
    let mut h = Sha256::new();
    h.update(std::fs::read(root.join("graph/evidence.json")).unwrap_or_default());
    h.update(today.as_bytes());
    h.update(words.join(" ").as_bytes());
    h.update(PROMPT_VERSION.to_string().as_bytes());
    format!("{:x}", h.finalize())
}

/// (pick, cached): the cached pick when its key is this key and `fresh` is
/// off, else `ask` once and cache the answer under the key.
fn recommendation(
    cache_path: &std::path::Path,
    key: &str,
    fresh: bool,
    ask: impl FnOnce() -> Value,
) -> (Value, bool) {
    let cache = pyjson::load(cache_path).unwrap_or_else(|| json!({}));
    if !fresh && cache.get("key").and_then(Value::as_str) == Some(key) {
        return (cache["pick"].clone(), true);
    }
    let pick = ask();
    pyjson::save(cache_path, &json!({"key": key, "pick": pick}), Some(1))
        .expect("write .llm_next.json");
    (pick, false)
}

fn render_pick(console: &Console, pick: &Value, cached: bool, words: &[String]) {
    let s = |k: &str| {
        pick.get(k)
            .and_then(Value::as_str)
            .unwrap_or("")
            .to_string()
    };
    let head = format!("{}. {}", kg::data::value_str(&pick["problem"]), s("title"));
    let tag = if pick.get("agrees").is_some_and(kg::data::truthy) {
        "the picker's pick as well"
    } else {
        "instead of the picker's pick"
    };
    let mut body = vec![format!("[dim]{tag}[/dim]"), String::new(), s("reason")];
    if let Some(plan) = pick
        .get("plan")
        .and_then(Value::as_array)
        .filter(|a| !a.is_empty())
    {
        body.push(String::new());
        body.push("[bold]then[/bold]".to_string());
        for step in plan {
            body.push(format!(
                "  {}. {} [dim]- {}[/dim]",
                kg::data::value_str(&step["problem"]),
                step["title"].as_str().unwrap_or(""),
                step["note"].as_str().unwrap_or("")
            ));
        }
    }
    let mut next_words: Vec<String> = words.to_vec();
    next_words.push("llm".into());
    next_words.push("prepare".into());
    body.push(String::new());
    body.push(format!("[bold]make next {}[/bold]", next_words.join(" ")));
    if cached {
        body.push("[dim]cached: same evidence, same day[/dim]".to_string());
    }
    let lines: Vec<kg::console::Line> = body
        .iter()
        .map(|l| Text::from_markup(l).segments())
        .collect();
    console.print_lines(panel_titled(
        &lines,
        &format!("llm: {head}"),
        console.width.min(100),
        true,
    ));
}

fn main() {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    if raw.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_llm_next [--prepare] [--fresh] [--model MODEL] [--context] [--key] [words ...]");
        return;
    }
    let (mut prepare, mut fresh, mut context, mut key_only) = (false, false, false, false);
    let mut model = "opus".to_string();
    let mut words: Vec<String> = Vec::new();
    let mut i = 0;
    while i < raw.len() {
        match raw[i].as_str() {
            "--prepare" => prepare = true,
            "--fresh" => fresh = true,
            "--context" => context = true,
            "--key" => key_only = true,
            "--model" => {
                i += 1;
                model = raw.get(i).cloned().unwrap_or(model);
            }
            w => words.push(w.to_string()),
        }
        i += 1;
    }
    let root = repo_root();
    load_envrc(&root);
    if !key_only && !context {
        kg::hooks::gate(&root, "next");
    }
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    if !key_only && !context {
        kg::fails::gate(&ctx, &ev);
    }
    let console = Console::full_width();
    let today = ctx.today().format("%Y-%m-%d").to_string();
    if key_only {
        println!("{}", context_key(&ctx.root, &today, &words));
        return;
    }
    if context {
        println!("{}", dumps(&build_context(&ctx, &ev, &words), Some(1)));
        return;
    }
    let key = context_key(&ctx.root, &today, &words);
    let (pick, cached) = recommendation(&ctx.root.join(".llm_next.json"), &key, fresh, || {
        let prompt = dumps(&build_context(&ctx, &ev, &words), Some(1));
        match claude_json(&prompt, SYSTEM_PROMPT, &model, 2) {
            Ok(v) => v,
            Err(e) => {
                console.print(&format!("[red]{e}[/red]"));
                std::process::exit(1);
            }
        }
    });
    render_pick(&console, &pick, cached, &words);
    if prepare {
        if let Some((cur, _)) = kg::lang::busy(&ctx.root) {
            console.print(&format!("[yellow]{} is not empty - record it (make solved) before preparing the next one.[/yellow]", cur.file_name().unwrap().to_string_lossy()));
            std::process::exit(1);
        }
        let _ = Command::new(kg::data::rs_bin(&ctx.root, "prepare"))
            .arg(kg::data::value_str(&pick["problem"]))
            .current_dir(&ctx.root)
            .status();
    }
}

/// utils/tests/test_llm_next.py, moved here: the pick is cached under the
/// evidence file, the day and the words; the model is never called here.
#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::Cell;

    fn pick() -> Value {
        json!({"problem": "543", "title": "Diameter of Binary Tree", "agrees": false, "reason": "one failed rep, nothing since.", "plan": []})
    }

    #[test]
    fn the_cache_contract() {
        let cache = std::env::temp_dir().join(format!("kg_llm_next_{}.json", std::process::id()));
        let _ = std::fs::remove_file(&cache);
        let calls = Cell::new(0);
        let ask = || {
            calls.set(calls.get() + 1);
            pick()
        };
        // the second read is cached
        let (p, cached) = recommendation(&cache, "k1", false, ask);
        assert_eq!((p["problem"].as_str(), cached), (Some("543"), false));
        let (p, cached) = recommendation(&cache, "k1", false, ask);
        assert_eq!((p["problem"].as_str(), cached), (Some("543"), true));
        assert_eq!(calls.get(), 1);
        // another key (new evidence, other words, another day) asks again
        let (_, cached) = recommendation(&cache, "k2", false, ask);
        assert!(!cached && calls.get() == 2);
        // --fresh ignores the cache
        let (_, cached) = recommendation(&cache, "k2", true, ask);
        assert!(!cached && calls.get() == 3);
        // the file holds the key and the pick
        let data = pyjson::load(&cache).unwrap();
        assert_eq!(
            data.as_object().unwrap().keys().collect::<Vec<_>>(),
            vec!["key", "pick"]
        );
        assert_eq!(data["pick"]["problem"], "543");
        let _ = std::fs::remove_file(&cache);
    }

    #[test]
    fn words_and_day_are_part_of_the_key() {
        let root = repo_root();
        let none: Vec<String> = vec![];
        let sql = vec!["sql".to_string()];
        let k = context_key(&root, "2026-09-12", &none);
        assert_ne!(k, context_key(&root, "2026-09-12", &sql));
        assert_ne!(k, context_key(&root, "2026-09-13", &none));
        assert_eq!(k, context_key(&root, "2026-09-12", &none));
    }
}
