// kg_crowd - keep data/crowd.json fresh: every free problem's submission,
// like and dislike counts, from LeetCode's public GraphQL (kg::crowd).
//
//   kg_crowd                      # sync the problems with no record or a
//                                 # record older than STALE_DAYS, oldest
//                                 # first, at most LIMIT of them
//   kg_crowd --limit N            # at most N (0: no cap)
//   kg_crowd --stale DAYS         # the age that counts as stale
//   kg_crowd 1733 554             # these problems, whatever their age
//   kg_crowd --show 1733 554      # print the saved records, fetch nothing
//
// The picker ranks on the file (crowd.rs): a disliked problem comes last
// in its rule, and among ties the most attempted problem comes first.
// `make crowd-install` loads the launchd job that runs this hourly; with
// the default cap a week's refresh of the 3000 free problems spreads over
// eight runs, and a problem is never more than STALE_DAYS behind.

use kg::crowd::{self, compact, fetch_stats, stats_of, STALE_DAYS};
use kg::data::{load_envrc, load_metadata, parse_date, real_today, repo_root};

const USAGE: &str = "usage: kg_crowd [--limit N] [--stale DAYS] [--show] [PROBLEM...]";
const LIMIT: usize = 400;
/// The pause between requests: LeetCode answers a burst with 404s and
/// 503s for a minute (2026-10-13).
const PAUSE_MS: u64 = 700;

struct Args {
    limit: usize,
    stale: i64,
    show: bool,
    problems: Vec<String>,
}

fn usage(msg: &str) -> ! {
    eprintln!("{USAGE}");
    eprintln!("kg_crowd: error: {msg}");
    std::process::exit(2)
}

fn parse_args() -> Args {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    let mut a = Args {
        limit: LIMIT,
        stale: STALE_DAYS,
        show: false,
        problems: Vec::new(),
    };
    let mut i = 0;
    while i < raw.len() {
        match raw[i].as_str() {
            "-h" | "--help" => {
                println!("{USAGE}");
                std::process::exit(0);
            }
            "--show" => a.show = true,
            "--limit" => {
                i += 1;
                a.limit = raw
                    .get(i)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or_else(|| usage("--limit takes an integer"));
            }
            "--stale" => {
                i += 1;
                a.stale = raw
                    .get(i)
                    .and_then(|s| s.parse().ok())
                    .filter(|&d| d >= 0)
                    .unwrap_or_else(|| usage("--stale takes a number of days"));
            }
            w if !w.is_empty() && w.chars().all(|c| c.is_ascii_digit()) => {
                a.problems.push(w.to_string())
            }
            w => usage(&format!("unrecognized argument: {w}")),
        }
        i += 1;
    }
    a
}

fn line(pnum: &str, title: &str, e: &serde_json::Value) -> String {
    match stats_of(e) {
        Some(s) => format!(
            "{pnum}. {title}: {} submissions, {} likes, {} dislikes ({}%){}, synced {}",
            compact(s.submissions),
            s.likes,
            s.dislikes,
            s.dislike_pct(),
            if s.bad() { ", disliked" } else { "" },
            e["synced"].as_str().unwrap_or("?")
        ),
        None => format!("{pnum}. {title}: no record"),
    }
}

fn main() {
    let args = parse_args();
    let root = repo_root();
    load_envrc(&root);
    let meta = load_metadata(&root);
    let mut records = crowd::load(&root);
    let today = real_today();
    let today_s = today.format("%Y-%m-%d").to_string();
    let title = |p: &str| {
        meta.get(p)
            .and_then(|m| m.title.clone())
            .unwrap_or_default()
    };

    if args.show {
        for p in &args.problems {
            let e = records.get(p).cloned().unwrap_or_default();
            println!("{}", line(p, &title(p), &e));
        }
        return;
    }

    // the problems to sync: the ones named, else every free problem whose
    // record is missing or stale, the missing first, then the oldest
    let mut todo: Vec<(i64, String)> = if args.problems.is_empty() {
        meta.iter()
            .filter(|(_, m)| !m.paid_only && m.slug.is_some())
            .filter_map(|(p, _)| {
                let age = match records.get(p).and_then(|e| e["synced"].as_str()) {
                    None => i64::MAX,
                    Some(d) => (today - parse_date(d)).num_days(),
                };
                (age >= args.stale).then(|| (age, p.clone()))
            })
            .collect()
    } else {
        args.problems
            .iter()
            .map(|p| (i64::MAX, p.clone()))
            .collect()
    };
    todo.sort_by(|a, b| b.0.cmp(&a.0).then_with(|| a.1.cmp(&b.1)));
    let left = todo.len();
    if args.limit > 0 {
        todo.truncate(args.limit);
    }

    let mut synced = 0;
    for (i, (_, p)) in todo.iter().enumerate() {
        let Some(slug) = meta.get(p).and_then(|m| m.slug.clone()) else {
            eprintln!("{p}: no slug in data/problems_metadata.json");
            continue;
        };
        match fetch_stats(&slug) {
            Ok(s) => {
                records.insert(p.clone(), crowd::entry(&slug, s, &today_s));
                synced += 1;
            }
            Err(e) => eprintln!("{p}. {}: {e}", title(p)),
        }
        if (i + 1) % 25 == 0 || i + 1 == todo.len() {
            if let Err(e) = crowd::save(&root, &records) {
                eprintln!("kg_crowd: {}: {e}", crowd::FILE);
                std::process::exit(1);
            }
        }
        std::thread::sleep(std::time::Duration::from_millis(PAUSE_MS));
    }
    println!(
        "synced {synced} of {} ({} were due, {} records in all)",
        todo.len(),
        left,
        records.len()
    );
}
