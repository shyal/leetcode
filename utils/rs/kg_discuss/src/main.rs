// kg_discuss - why the crowd dislikes a problem: the Discussion tab's
// verdict, read on demand.
//
//   kg_discuss 1733 554                 # judge these problems
//   kg_discuss [--size N] [--model M]   # judge the next N queued problems
//                                       # (default 30) that have no verdict
//   kg_discuss --force ...              # judge again, over a saved verdict
//   kg_discuss --show [--size N]        # print the saved verdicts for the
//                                       # queue, fetch and ask nothing
//   kg_discuss --context 1733           # print the prompt, ask nothing
//   kg_discuss --rescore                # recompute every saved verdict
//                                       # from its stored comments, after
//                                       # a change to the thresholds
//
// For each problem it pulls the most upvoted comments from LeetCode's
// Discussion tab (kg::discuss, no login), asks the model which of them
// complain about the statement itself, and files the answer in
// data/discuss_verdicts.json. Nothing in it enters a pick: the picker
// ranks on the like and dislike counts (kg_crowd, crowd.rs says why).
//
// The model is DISCUSS_MODEL from the environment, else the one LM Studio
// has loaded on this machine (discuss::DEFAULT_MODEL, reasoning off). The
// prompt was tuned against `--model haiku` on 2026-10-13.

use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, real_today, repo_root, Rec};
use kg::discuss::{
    self, fetch_comments, judge, prompt, verdict_of, Comment, COMMENTS, DEFAULT_MODEL,
};
use kg::evidence::Evidence;
use kg::git::sleep_state;
use kg::queue::queue_rows;
use serde_json::{json, Value};

const USAGE: &str = "usage: kg_discuss [--size N] [--model MODEL] [--force] [--show] [--context] [--rescore] [PROBLEM...]";
const DEFAULT_SIZE: usize = 30;

struct Args {
    size: usize,
    model: String,
    force: bool,
    show: bool,
    context: bool,
    rescore: bool,
    problems: Vec<String>,
}

fn usage(msg: &str) -> ! {
    eprintln!("{USAGE}");
    eprintln!("kg_discuss: error: {msg}");
    std::process::exit(2)
}

fn parse_args() -> Args {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    let mut a = Args {
        size: DEFAULT_SIZE,
        model: std::env::var("DISCUSS_MODEL")
            .ok()
            .filter(|m| !m.trim().is_empty())
            .unwrap_or_else(|| DEFAULT_MODEL.to_string()),
        force: false,
        show: false,
        context: false,
        rescore: false,
        problems: Vec::new(),
    };
    let mut i = 0;
    while i < raw.len() {
        match raw[i].as_str() {
            "-h" | "--help" => {
                println!("{USAGE}");
                std::process::exit(0);
            }
            "--force" => a.force = true,
            "--show" => a.show = true,
            "--context" => a.context = true,
            "--rescore" => a.rescore = true,
            "--size" => {
                i += 1;
                a.size = raw
                    .get(i)
                    .and_then(|s| s.parse().ok())
                    .filter(|&n| n > 0)
                    .unwrap_or_else(|| usage("--size takes a positive integer"));
            }
            w if w.starts_with("--size=") => {
                a.size = w["--size=".len()..]
                    .parse()
                    .ok()
                    .filter(|&n| n > 0)
                    .unwrap_or_else(|| usage("--size takes a positive integer"));
            }
            "--model" => {
                i += 1;
                a.model = raw
                    .get(i)
                    .cloned()
                    .unwrap_or_else(|| usage("--model takes a name"));
            }
            w if w.chars().all(|c| c.is_ascii_digit()) && !w.is_empty() => {
                a.problems.push(w.to_string())
            }
            w => usage(&format!("unrecognized argument: {w}")),
        }
        i += 1;
    }
    a
}

/// The problems to judge: the ones named, else the queue.
fn targets(ctx: &Ctx, recs: Vec<(String, Rec)>, args: &Args) -> Vec<(String, String)> {
    if !args.problems.is_empty() {
        return args
            .problems
            .iter()
            .map(|p| {
                let title = ctx
                    .all_problems()
                    .get(p)
                    .map(|q| q.title.clone())
                    .or_else(|| ctx.meta.get(p).and_then(|m| m.title.clone()))
                    .unwrap_or_default();
                (p.clone(), title)
            })
            .collect();
    }
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());
    let asleep = sleep_state(ctx, &pv, &ev);
    queue_rows(ctx, &pv, &ev, &asleep, args.size)
        .into_iter()
        .map(|r| (r.pnum, r.title))
        .collect()
}

fn one_line(pnum: &str, title: &str, entry: &Value) -> String {
    format!(
        "{pnum}. {title}: {} ({}) - {}",
        entry["verdict"].as_str().unwrap_or("?"),
        entry["unhappy"],
        entry["reason"].as_str().unwrap_or("")
    )
}

/// Every comment the model read, numbered as in the prompt, so the
/// `complaints` list in the entry can be checked against them.
fn top_json(comments: &[Comment]) -> Value {
    Value::Array(
        comments
            .iter()
            .enumerate()
            .map(|(i, c)| json!({"n": i + 1, "votes": c.votes, "user": c.user, "text": c.text}))
            .collect(),
    )
}

/// Every saved verdict recomputed from its stored comments and complaint
/// numbers (discuss::verdict_of), one line per verdict that changed.
fn rescore(verdicts: &mut serde_json::Map<String, Value>) {
    for (pnum, entry) in verdicts.iter_mut() {
        let comments: Vec<Comment> = entry["top"]
            .as_array()
            .into_iter()
            .flatten()
            .map(|c| Comment {
                votes: c["votes"].as_i64().unwrap_or(0),
                replies: 0,
                user: String::new(),
                text: String::new(),
            })
            .collect();
        let complaints: Vec<usize> = entry["complaints"]
            .as_array()
            .into_iter()
            .flatten()
            .filter_map(|x| x.as_u64())
            .map(|x| x as usize)
            .collect();
        let (verdict, unhappy) = verdict_of(&comments, &complaints);
        let was = entry["verdict"].as_str().unwrap_or("").to_string();
        if was != verdict || entry["unhappy"] != unhappy {
            println!(
                "{pnum}. {}: {was} -> {verdict} ({unhappy})",
                entry["title"].as_str().unwrap_or("")
            );
        }
        entry["verdict"] = json!(verdict);
        entry["unhappy"] = json!(unhappy);
    }
}

fn main() {
    let args = parse_args();
    let root = repo_root();
    load_envrc(&root);
    let mut verdicts = discuss::load(&root);

    if args.rescore {
        rescore(&mut verdicts);
        if let Err(e) = discuss::save(&root, &verdicts) {
            eprintln!("kg_discuss: {}: {e}", discuss::FILE);
            std::process::exit(1);
        }
        return;
    }

    let (ctx, recs) = Ctx::load(root.clone());
    let targets = targets(&ctx, recs, &args);

    if args.show {
        for (pnum, title) in &targets {
            match verdicts.get(pnum) {
                Some(e) => println!("{}", one_line(pnum, title, e)),
                None => println!("{pnum}. {title}: no verdict yet"),
            }
        }
        return;
    }

    let mut judged = 0;
    for (pnum, title) in &targets {
        if !args.force && !args.context && verdicts.contains_key(pnum) {
            continue;
        }
        let Some(slug) = ctx.meta.get(pnum).and_then(|m| m.slug.clone()) else {
            eprintln!("{pnum}. {title}: no slug in data/problems_metadata.json");
            continue;
        };
        let (total, comments) = match fetch_comments(&slug, COMMENTS) {
            Ok(x) => x,
            Err(e) => {
                eprintln!("{pnum}. {title}: {e}");
                continue;
            }
        };
        let text = prompt(pnum, title, ctx.acceptance(pnum), total, &comments);
        if args.context {
            println!("{text}");
            continue;
        }
        if comments.is_empty() {
            let entry = json!({
                "slug": slug, "title": title, "model": args.model,
                "judged": real_today().format("%Y-%m-%d").to_string(),
                "comments": 0, "verdict": "good", "unhappy": 0,
                "reason": "The Discussion tab is empty.", "top": [],
            });
            println!("{}", one_line(pnum, title, &entry));
            verdicts.insert(pnum.clone(), entry);
        } else {
            let mut entry = match judge(&text, &comments, &args.model) {
                Ok(v) => v,
                Err(e) => {
                    eprintln!("{pnum}. {title}: {e}");
                    continue;
                }
            };
            entry["slug"] = json!(slug);
            entry["title"] = json!(title);
            entry["model"] = json!(args.model);
            entry["judged"] = json!(real_today().format("%Y-%m-%d").to_string());
            entry["comments"] = json!(total);
            entry["top"] = top_json(&comments);
            println!("{}", one_line(pnum, title, &entry));
            verdicts.insert(pnum.clone(), entry);
        }
        judged += 1;
        if let Err(e) = discuss::save(&root, &verdicts) {
            eprintln!("kg_discuss: {}: {e}", discuss::FILE);
            std::process::exit(1);
        }
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
    if judged == 0 && !args.context {
        eprintln!(
            "nothing to judge: every one of the {} has a verdict (--force judges again)",
            targets.len()
        );
    }
}
