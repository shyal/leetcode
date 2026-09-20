// kg_stats - the scored games over a window: `make stats`.
//
//   make stats           # the last 7 days
//   make stats 3         # the last 3 days
//   make stats 30d       # the last 30 days
//   make stats all       # every scored game
//
// One row per problem solve in the window, oldest first, scored exactly as
// the Elo scores it (kg::model::scored_games): a FAILED file, a walkthrough
// or learning rep, or a pass over its tier's clock (10/25/45 minutes for
// Easy/Medium/Hard, the next tier up on a followup) is 0; a pass on a hint
// is 1/2; a clean pass inside the clock is 1. Then the totals: pass/fail,
// inside the clock, first sight against repeat, and under them the two
// counts that say whether ground is being gained and kept (model::Ground):
// first sights at your level solved cold, and recovered problems that
// held on their retest.
//
// Written 2026-09-16, the night these questions took four git-log queries
// to answer by hand. The seconds come from the record itself
// (`seconds`, filed by kg_solved via the placeholder); records older than
// the field are timed from their commit.

use chrono::Duration;
use kg::console::Console;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::model::{elo_games, scored_games, solve_ratings, Game, Ground, Summary};
use kg::table::{print_table, BoxKind, Table};

fn window_days(args: &[String]) -> Option<i64> {
    let a = args.first().map(String::as_str).unwrap_or("7");
    if a == "all" {
        return None;
    }
    Some(a.trim_end_matches('d').parse().unwrap_or(7))
}

fn mmss(secs: Option<i64>) -> String {
    match secs {
        Some(s) => format!("{}m {:02}s", s / 60, s % 60),
        None => "-".to_string(),
    }
}

fn result_cell(g: &Game) -> String {
    if g.failed {
        "[red]fail[/red]".to_string()
    } else if g.over {
        "[yellow]pass, over[/yellow]".to_string()
    } else if g.assist == "none" {
        "[green]pass[/green]".to_string()
    } else {
        format!("[cyan]pass, {}[/cyan]", g.assist)
    }
}

fn score_cell(score: f64) -> String {
    if score == 1.0 {
        "1".to_string()
    } else if score == 0.5 {
        "½".to_string()
    } else {
        "0".to_string()
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_stats [DAYS|DAYSd|all]   (default 7)");
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let ratings = kg::data::read_json(&ctx.graph_dir().join("ratings.json")).unwrap_or_default();
    let since = window_days(&args).map(|d| ctx.today() - Duration::days(d - 1));
    let games: Vec<Game> = scored_games(&ctx, &ev)
        .into_iter()
        .filter(|g| since.is_none_or(|s| kg::data::parse_date(&g.date) >= s))
        .collect();
    let console = Console::full_width();
    if games.is_empty() {
        console.print("[dim]no scored games in the window.[/dim]");
        return;
    }

    let title = match since {
        Some(s) => format!("games since {s}"),
        None => "every game".to_string(),
    };
    let mut table = Table::plain(
        &[
            "date", "problem", "rating", "rep", "result", "time", "score",
        ],
        Some(&title),
        BoxKind::Rounded,
    );
    table.column(
        1,
        kg::table::Column {
            no_wrap: true,
            ..Default::default()
        },
    );
    for g in &games {
        let name = ctx
            .meta_title(&g.problem)
            .map(|t| format!("{}. {t}", g.problem))
            .unwrap_or_else(|| format!("{}.", g.problem));
        let rating = ratings
            .get(&g.problem)
            .and_then(|v| v.as_f64())
            .map(|r| format!("{r:.0}"))
            .unwrap_or_else(|| "-".to_string());
        table.add_row(&[
            g.date.clone(),
            name,
            rating,
            if g.first { "first" } else { "repeat" }.to_string(),
            result_cell(g),
            mmss(g.seconds),
            score_cell(g.score),
        ]);
    }
    print_table(&console, &table);

    for (before, ratio, after) in Summary::of(&games).rows() {
        console.print(&format!("{before}[bold green]{ratio}[/bold green]{after}"));
    }
    // gain and retention need the games before the window: the Elo carried
    // into each game, and whether an earlier game on the problem was lost
    let all = elo_games(&ctx, &ev, &solve_ratings(&ctx));
    let window = match window_days(&args) {
        Some(d) => format!("the last {d} days"),
        None => "all time".to_string(),
    };
    for (before, ratio, after) in Ground::of(&all, since).rows(&window) {
        console.print(&format!("{before}[bold green]{ratio}[/bold green]{after}"));
    }
}
