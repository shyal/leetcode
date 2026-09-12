// kg_llm_next - a second opinion on the pick. The model reads what `make
// next` printed and the last three weeks of evidence (every rep, its
// verdicts, its note, the failure notes, the rating gap on each problem) and
// names the problem it would schedule, with its reasons.
//
//   make next llm              # the model's pick and the plan behind it
//   make next llm prepare      # prepare that pick: stub + branch, clock on
//   make next sql llm          # the same, inside a group
//   kg_llm_next --context      # the context the model is handed (the tests)
//   kg_llm_next --key          # the cache key
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
use kg::evidence::{drill_key, Evidence};
use kg::git::mined_solve_times;
use kg::llm::claude_json;
use kg::model::{elo_now, solve_ratings};
use kg::pyjson::{self, dumps};
use kg::table::panel_titled;
use regex::Regex;
use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};

const WINDOW_DAYS: i64 = 21;
const PROMPT_VERSION: i64 = 1;

const SYSTEM_PROMPT: &str = "You schedule the next leetcode problem for one operator. You are given what\nhis own picker printed, and the last three weeks of his evidence: every rep,\nits verdicts, his notes, the failure notes, the contest rating of each problem\nagainst his elo. Name the one problem he should open next.\n\nRules of the schedule, in order:\n1. A due review of a problem he failed outranks new ground.\n2. When a hard problem leans on a plainer problem he failed recently, the\n   plain one comes first.\n3. A problem he walked away from without ever reaching a working solution\n   gets a learning rep first: look the solution up, step through it. An\n   unaided rep of it comes days later. Do not schedule the unaided rep cold.\n4. Measure a problem by its contest rating against his elo, never by the\n   Easy/Medium/Hard label.\n5. What worked in the last few days is the pattern to continue.\n\nWriting rules: short declarative sentences, plain English, no analogies, no\ncoined words. Refer to problems by number and title only. Never name a\ntechnique, a graph node, or a move. Never say a problem should be easy.\nNever tell him when to rest.\n\nReply with one JSON object and nothing else:\n{\n  \"problem\": \"<number>\",\n  \"title\": \"<title>\",\n  \"agrees\": <true if this is the picker's own pick>,\n  \"reason\": \"<two to four sentences>\",\n  \"plan\": [{\"problem\": \"<number>\", \"title\": \"<title>\", \"note\": \"<one sentence>\"}]\n}\nThe plan is the next two or three problems after this one, in order.\n";

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

/// Problems with a failed rep and no clean unaided problem rep since.
fn open_failures(ctx: &Ctx, ev: &Evidence, ratings: &HashMap<String, f64>) -> Vec<Value> {
    let mut last_fail: HashMap<String, String> = HashMap::new();
    let mut last_clean: HashMap<String, String> = HashMap::new();
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
        if path.contains("_FAILED_") {
            let e = last_fail.entry(pnum.clone()).or_default();
            if rec.date > *e {
                *e = rec.date.clone();
            }
            if !order.contains(&pnum) {
                order.push(pnum);
            }
        } else if rec.assist_any() == "none" && rec.moves.values().all(|v| v == "clean") {
            let e = last_clean.entry(pnum).or_default();
            if rec.date > *e {
                *e = rec.date.clone();
            }
        }
    }
    // sorted(last_fail.items(), key=date): stable on insertion order
    order.sort_by(|a, b| last_fail[a].cmp(&last_fail[b]));
    let mut out = Vec::new();
    for pnum in order {
        let d = &last_fail[&pnum];
        if last_clean.get(&pnum).is_some_and(|c| c > d) {
            continue;
        }
        out.push(json!({
            "problem": pnum,
            "title": ctx.ro.map.get(&pnum).map(|p| p.title.clone()).unwrap_or_default(),
            "failed": d,
            "rating": ratings.get(&pnum).map(|r| json!(round_i(*r))).unwrap_or(Value::Null),
        }));
    }
    out
}

fn build_context(ctx: &Ctx, ev: &Evidence, words: &[String]) -> Value {
    let ratings = solve_ratings(ctx);
    let since = ctx.today() - Duration::days(WINDOW_DAYS);
    json!({
        "today": ctx.today().format("%Y-%m-%d").to_string(),
        "elo": round_i(elo_now(ctx, ev)),
        "picker": picker_frame(ctx, words),
        "failed_without_a_clean_unaided_rep_since": open_failures(ctx, ev, &ratings),
        "reps": recent_reps(ctx, ev, &ratings, since),
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
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
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
        let cur = ctx.root.join("current.py");
        if std::fs::read_to_string(&cur).is_ok_and(|s| !s.trim().is_empty()) {
            console.print("[yellow]current.py is not empty - record it (make solved) before preparing the next one.[/yellow]");
            std::process::exit(1);
        }
        let _ = Command::new(ctx.root.join(".venv/bin/python3"))
            .arg(ctx.root.join("utils/kg/prepare"))
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
