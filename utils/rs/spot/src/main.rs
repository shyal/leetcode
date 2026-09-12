// spot - serve a recognition rep: a problem statement with the title, number
// and tags stripped, as markdown in current.md, on a branch. The candidate
// writes under the rule which move the statement calls for (free text; or
// "direct" for none, or "don't know"), then `make solved` files it under
// recognition/ and the judge scores the answer against the walk's entry move.
//
//   make prepare spot           # the picker's rep (kg::recog::due_spot),
//   make spot                   # whether or not make next says one is due
//   make spot medium            # carried on a Medium (easy|medium|hard); the
//                               # default is the gentlest carrier, like a solve
//   spot --problem 84           # a chosen problem (the number is not shown)
//   spot --dry                  # the pick's reason, nothing served
//   spot --markdown 84          # the cached statement as markdown (the tests)
//
// The number appears nowhere the candidate sees before the answer is in:
// the branch is spot-<stamp>, the marker commit says "spotting", and the
// pick is kept in .spot.json (untracked), keyed by branch, until the judge
// reads it back.
//
// Ported from utils/kg/spot (Python) on 2026-09-12.

use std::collections::HashSet;
use std::process::Command;

use chrono::Utc;
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::git::sleep_state;
use kg::recog;
use kg::status::all_statuses;
use serde_json::{json, Value};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: spot [--problem N] [--dry] [easy|medium|hard]\n\nServe a recognition rep into current.md.");
        return;
    }
    if args.first().map(String::as_str) == Some("--markdown") {
        let root = repo_root();
        let num = args.get(1).cloned().unwrap_or_default();
        match recog::fetch_content(&root, &num) {
            Ok(e) => print!(
                "{}",
                recog::html_to_markdown(e["content"].as_str().unwrap_or(""))
            ),
            Err(e) => {
                eprintln!("{e}");
                std::process::exit(1);
            }
        }
        return;
    }
    let mut problem: Option<String> = None;
    let mut dry = false;
    let mut difficulty: Option<String> = None;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--problem" => {
                i += 1;
                problem = args.get(i).cloned();
            }
            "--dry" => dry = true,
            d @ ("easy" | "medium" | "hard") => {
                let mut c = d.chars();
                difficulty =
                    Some(c.next().unwrap().to_uppercase().collect::<String>() + c.as_str());
            }
            other => {
                eprintln!("usage: spot [--problem N] [--dry] [easy|medium|hard]\nspot: error: argument difficulty: invalid choice: '{other}'");
                std::process::exit(2);
            }
        }
        i += 1;
    }
    let root = repo_root();
    load_envrc(&root);
    let console = Console::full_width();
    for f in ["current.py", "current.md"] {
        if std::fs::read_to_string(root.join(f)).is_ok_and(|s| !s.trim().is_empty()) {
            console.print(&format!("[red]{f} is not empty - record it (make solved) before preparing the next one.[/red]"));
            std::process::exit(1);
        }
    }
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());
    let statuses = all_statuses(&ctx, &ev, today);
    let recog = recog::derived(&ctx, &recog::load_recognition(&ctx), &ev, &pv, &statuses);

    let (pnum, target, reason) = match &problem {
        Some(p) => (p.clone(), None, "chosen by hand".to_string()),
        None => {
            let asleep: HashSet<String> = sleep_state(&ctx, &pv, &ev).into_iter().collect();
            // asked for = served: the SPOT_EVERY ratio governs what make next
            // suggests, not what make prepare spot does
            match recog::due_spot_with(
                &ctx,
                &pv,
                &ev,
                &recog,
                &statuses,
                today,
                &asleep,
                true,
                difficulty.as_deref(),
            ) {
                Some((t, p, r)) => (p, Some(t), r),
                None => {
                    let tier = difficulty
                        .as_deref()
                        .map(|d| format!(" among {d} problems"))
                        .unwrap_or_default();
                    console.print(&format!(
                        "nothing to spot{tier}: no node with reach is waiting for a rep."
                    ));
                    std::process::exit(1);
                }
            }
        }
    };
    if dry {
        console.print(&format!("a spot rep is due ({reason})."));
        return;
    }
    let entry = match recog::fetch_content(&ctx.root, &pnum) {
        Ok(e) => e,
        Err(e) => {
            console.print(&format!("[red]could not fetch the statement: {e}[/red]"));
            std::process::exit(1);
        }
    };
    let statement = recog::html_to_markdown(entry["content"].as_str().unwrap_or(""));
    let title = pv
        .map
        .get(&pnum)
        .map(|p| p.title.clone())
        .filter(|t| !t.is_empty())
        .or_else(|| entry["title"].as_str().map(String::from))
        .unwrap_or_default();

    let stamp = Utc::now().format("%Y%m%dT%H%M%SZ").to_string();
    let branch = format!("spot-{stamp}");
    let mut meta = recog::load_spot_meta(&ctx.root);
    meta[&branch] = json!({
        "problem": pnum,
        "target": target.clone().map(Value::String).unwrap_or(Value::Null),
        "reason": reason,
        "title": title,
        "difficulty": entry.get("difficulty").cloned().unwrap_or_else(|| json!("")),
    });
    recog::save_spot_meta(&ctx.root, &meta).expect("write .spot.json");

    let git = |args: &[&str]| {
        let out = Command::new("git")
            .args(args)
            .current_dir(&ctx.root)
            .output()
            .expect("git");
        if !out.status.success() {
            eprintln!(
                "git {} failed: {}",
                args.join(" "),
                String::from_utf8_lossy(&out.stderr).trim()
            );
            std::process::exit(1);
        }
    };
    git(&["checkout", "master"]);
    std::fs::write(
        ctx.root.join("current.md"),
        recog::spot_document(&statement),
    )
    .expect("write current.md");
    git(&["checkout", "-b", &branch]);
    git(&["add", "current.md"]);
    git(&["commit", "-m", "spotting"]);
    console.print(&format!(
        "current.md is ready on branch [bold]{branch}[/bold]. Read the statement, write under the rule which move it calls for (or \"direct\", or \"don't know\"), then `make solved`."
    ));
}
