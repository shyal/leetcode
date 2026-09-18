// kg_readme - the README pipeline: the charts and badges under graph/, the
// S3 upload and the README's generated regions.
//
//   kg_readme                       # every chart and badge (make readme)
//   kg_readme update                # upload + rewrite README.md
//   kg_readme rank-table            # refresh data/leetcode_rank_table.json
//   kg_readme now [--once]          # the Elo dashboard (make elo); --once is one frame
//   kg_readme <chart> [--forecast | --no-forecast]
//
// <chart> is one of elo, streak, rank, rate, problem-rating, backlog,
// problem-rating-month, hours, onsite, progress. The forecast flags reach
// problem-rating and backlog, which share the cached runs.
//
// Ported from the utils/readme/*_svg scripts and update_readme.py
// (Python) on 2026-09-13.

mod backlog;
mod common;
mod dash;
mod elo;
mod hours;
mod onsite;
mod problem_rating;
mod progress;
mod rank;
mod rank_fetch;
mod rate;
mod streak;
mod update;

use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;

const CHARTS: [&str; 10] = [
    "elo",
    "streak",
    "rank",
    "rate",
    "problem-rating",
    "problem-rating-month",
    "backlog",
    "hours",
    "onsite",
    "progress",
];

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let names: Vec<&str> = args
        .iter()
        .filter(|a| !a.starts_with("--"))
        .map(String::as_str)
        .collect();
    let names: Vec<&str> = if names.is_empty() {
        CHARTS.to_vec()
    } else {
        names
    };
    for name in names {
        match name {
            "elo" => elo::render(&ctx, &ev),
            "streak" => streak::render(&ctx),
            "rank" => rank::render(&ctx, &ev),
            "rate" => rate::render(&ctx, &ev),
            "problem-rating" => problem_rating::render(&ctx, &ev, &args),
            "problem-rating-month" => problem_rating::render_month(&ctx, &ev),
            "backlog" => backlog::render(&ctx, &ev, &args),
            "hours" => hours::render(&ctx, &ev),
            "onsite" => onsite::render(&ctx, &ev),
            "progress" => progress::render(&ctx, &ev),
            "update" => update::run(&ctx, &ev),
            "rank-table" => rank_fetch::run(&ctx),
            "now" => dash::run(&ctx, &ev, args.iter().any(|a| a == "--once")),
            other => {
                eprintln!(
                    "kg_readme: unknown target {other}; one of {}, update, rank-table, now",
                    CHARTS.join(", ")
                );
                std::process::exit(2);
            }
        }
    }
}
