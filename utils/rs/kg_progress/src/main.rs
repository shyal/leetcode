// kg_progress - `make progress`: the answer to "am i progressing", in
// three short paragraphs of plain English. A verdict, the drills, and
// what is being done about it. No table, no rates; the numbers live in
// `make stats`.
//
//   make progress                    # as of today
//   KG_TODAY=2026-08-15 make progress  # as of a past day, on the evidence to then
//
// Written 2026-09-20, the day "am i progressing" took nine replies to
// answer. The verdict is kg::model::progress.

use kg::console::Console;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::model::progress;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_progress   (KG_TODAY=YYYY-MM-DD for a past day)");
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let cutoff = today.format("%Y-%m-%d").to_string();
    // the evidence as it stood on that day
    let recs = recs
        .into_iter()
        .filter(|(_, r)| r.date.as_str() <= cutoff.as_str())
        .collect();
    let ev = Evidence::new(recs);
    if args.iter().any(|a| a == "--elo") {
        // both Elo series by month: every game, and first sights only
        let games = kg::model::elo_games(&ctx, &ev, &kg::model::solve_ratings(&ctx));
        let fs = kg::model::elo_after(
            &kg::model::first_sight_elo_games(&ctx, &ev),
            kg::model::ELO_START,
        );
        let pv = kg::model::proven_series(&kg::model::proven_games(&ctx, &ev));
        let mut months: Vec<String> = games
            .iter()
            .map(|(g, _, _)| g.date[..7].to_string())
            .collect();
        months.dedup();
        let peak = fs.iter().map(|(_, e)| *e).fold(0.0, f64::max);
        let now = fs.last().map_or(kg::model::ELO_START, |(_, e)| *e);
        println!("first-sight peak {peak:.0}, now {now:.0}");
        println!("month    every game   first sight   proven");
        for m in months {
            let all = games
                .iter()
                .rev()
                .find(|(g, _, _)| g.date.starts_with(&m))
                .map(|(_, _, e)| *e)
                .unwrap_or(0.0);
            let f = fs
                .iter()
                .rev()
                .find(|(d, _)| d.format("%Y-%m").to_string() == m)
                .map(|(_, e)| *e)
                .unwrap_or(f64::NAN);
            let p = pv
                .iter()
                .rev()
                .find(|(d, _)| d.format("%Y-%m").to_string() == m)
                .map(|(_, e)| *e)
                .unwrap_or(f64::NAN);
            println!("{m}  {all:>10.0}   {f:>10.0}   {p:>7.0}");
        }
        return;
    }
    let console = Console::full_width();
    for (i, para) in progress(&ctx, &ev, today).iter().enumerate() {
        if i == 0 {
            console.print(&format!("[bold]{para}[/bold]"));
        } else {
            console.print(para);
        }
        console.print("");
    }
}
