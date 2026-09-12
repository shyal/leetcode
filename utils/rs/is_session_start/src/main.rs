// is_session_start - predicate: is this the start of the session?
//
// True when fewer than NEXT_WARMUP_COUNT (env, default 2; 0 turns the
// warmup off) solves have been authored since local midnight
// (Asia/Manila - git stamps are UTC, and the evidence-folding amend
// rewrites commit dates, so it counts by AUTHOR date of commits that ADD
// files under solved/ or drills/; meta and tooling commits never count).
//
// Prints true/false; exit code 0/1 to match.
//
//   make is_session_start
//   is_session_start --files     # today's solve files, one per line
//   is_session_start --seconds   # seconds of recorded solving today

use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};

fn main() {
    let root = repo_root();
    load_envrc(&root);
    let (ctx, _) = Ctx::load(root);
    match std::env::args().nth(1).as_deref() {
        Some("--files") => {
            for f in kg::git::solves_today(&ctx) {
                println!("{f}");
            }
            return;
        }
        Some("--seconds") => {
            println!("{}", kg::git::solve_seconds_today(&ctx));
            return;
        }
        _ => {}
    }
    let start = kg::git::is_session_start(&ctx);
    println!("{}", if start { "true" } else { "false" });
    std::process::exit(if start { 0 } else { 1 });
}
