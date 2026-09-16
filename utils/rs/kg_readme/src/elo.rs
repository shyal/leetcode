// The Elo over the solve history, scored on a contest clock, rendered into
// graph/elo.svg (the curve) and graph/elo_badge.svg (the current number).
//
// Problem ratings are zerotrac's (data/leetcode_ratings.tsv); a problem
// that never ran in a contest gets the median contest rating of its
// difficulty. Each attempt is one game against the problem, scored by
// kg::model::scored_games: unaided inside budget is a win, a hint inside
// budget a draw, a fail, an over-budget solve, a walkthrough or a learning
// rep a loss. Standard Elo, K=32, from 1200.
//
// Only first sights are games: the attempts on the day of a problem's
// first evidenced attempt. Every Elo on the README comes from this list;
// the picker keeps its own over every timed attempt (settled 2026-09-12).
//
// The cutoffs drawn are LeetCode's badge cutoffs: Knight is the top 25%
// of contest users, Guardian the top 5%.
//
// Ported from utils/readme/kg_elo_svg (Python) on 2026-09-13.

use std::collections::HashMap;

use chrono::NaiveDate;
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::evidence::Evidence;
use kg::model::scored_games;

use crate::common::*;

pub const K: f64 = 32.0;
pub const START: f64 = 1200.0;
pub const RANKS: [(i64, &str, &str); 2] = [(2200, "guardian", GOLD), (1850, "knight", BLUE)];
pub const MA_LINE: &str = "#e3b341";
pub const MA: usize = 60;
pub const LINE: &str = GREEN;

const W: i64 = 1200;
const H: i64 = 400;
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 44;
const MB: i64 = 40;

/// (date, problem rating, score): one scored first-sight game.
pub type G = (NaiveDate, f64, f64);

/// data/leetcode_ratings.tsv in file order: (problem, rating).
pub fn load_ratings(ctx: &Ctx) -> Vec<(String, f64)> {
    let text = std::fs::read_to_string(ctx.root.join("data/leetcode_ratings.tsv"))
        .expect("data/leetcode_ratings.tsv");
    text.lines()
        .skip(1)
        .map(|l| {
            let mut f = l.split('\t');
            let r: f64 = f.next().unwrap().parse().unwrap();
            (f.next().unwrap().to_string(), r)
        })
        .collect()
}

/// problem -> date of its first evidenced attempt, timed or not.
pub fn first_dates(ev: &Evidence) -> HashMap<String, String> {
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| (&ev.rec(a).date, ev.fname(a)).cmp(&(&ev.rec(b).date, ev.fname(b))));
    let mut first = HashMap::new();
    for i in order {
        let rec = ev.rec(i);
        first
            .entry(rec.problem.clone().unwrap_or_default())
            .or_insert_with(|| rec.date.clone());
    }
    first
}

/// (problem -> contest rating, difficulty -> the median rating of its
/// rated problems): what a game is priced at.
pub fn pricing(ctx: &Ctx) -> (HashMap<String, f64>, HashMap<String, f64>) {
    let ratings = load_ratings(ctx);
    let mut by_diff: HashMap<String, Vec<f64>> = HashMap::new();
    for (pid, rt) in &ratings {
        if let Some(d) = ctx.meta.get(pid).and_then(|m| m.difficulty.clone()) {
            by_diff.entry(d).or_default().push(*rt);
        }
    }
    (
        ratings.into_iter().collect(),
        by_diff.into_iter().map(|(d, v)| (d, median(&v))).collect(),
    )
}

pub fn price(
    ratings: &HashMap<String, f64>,
    imputed: &HashMap<String, f64>,
    problem: &str,
    difficulty: &str,
) -> f64 {
    match ratings.get(problem) {
        Some(r) => *r,
        None => *imputed
            .get(difficulty)
            .unwrap_or_else(|| panic!("no median rating for {difficulty}")),
    }
}

/// [(date, problem rating, score)] oldest first, one per scored first-sight
/// attempt.
pub fn games(ctx: &Ctx, ev: &Evidence) -> Vec<G> {
    let (ratings, imputed) = pricing(ctx);
    let first = first_dates(ev);
    scored_games(ctx, ev)
        .into_iter()
        .filter(|g| first.get(&g.problem) == Some(&g.date))
        .map(|g| {
            (
                parse_date(&g.date),
                price(&ratings, &imputed, &g.problem, &g.difficulty),
                g.score,
            )
        })
        .collect()
}

/// [(date, rating after the game)] one per game, from `start`.
pub fn elo_after(gs: &[G], start: f64) -> Vec<(NaiveDate, f64)> {
    let mut r = start;
    gs.iter()
        .map(|(d, rp, s)| {
            r += K * (s - 1.0 / (1.0 + 10f64.powf((rp - r) / 400.0)));
            (*d, r)
        })
        .collect()
}

fn last_per_day(after: Vec<(NaiveDate, f64)>) -> Vec<(NaiveDate, f64)> {
    let mut by_day: Vec<(NaiveDate, f64)> = Vec::new();
    for (d, r) in after {
        match by_day.iter_mut().find(|(dd, _)| *dd == d) {
            Some(slot) => slot.1 = r,
            None => by_day.push((d, r)),
        }
    }
    by_day.sort_by_key(|(d, _)| *d);
    by_day
}

/// [(date, rating after the day's last game)] one per day with a game.
pub fn elo(gs: &[G], start: f64) -> Vec<(NaiveDate, f64)> {
    last_per_day(elo_after(gs, start))
}

/// [(date, mean of the Elo after each of the last n games)] one per day
/// with a game, once n games exist. `tail` is the per-game Elo the window
/// starts full of, for a series that continues another: only dates past it
/// are returned.
pub fn elo_ma(gs: &[G], start: f64, tail: &[(NaiveDate, f64)]) -> Vec<(NaiveDate, f64)> {
    let n = MA;
    let mut after = tail.to_vec();
    after.extend(elo_after(gs, start));
    let mut out = Vec::new();
    for i in (n - 1).max(tail.len())..after.len() {
        let s = after[i + 1 - n..=i].iter().fold(0.0, |a, (_, r)| a + r);
        out.push((after[i].0, s / n as f64));
    }
    last_per_day(out)
}

pub fn rank_of(r: f64) -> (String, &'static str) {
    for (cut, name, color) in RANKS {
        if r >= cut as f64 {
            return (name.to_string(), color);
        }
    }
    (
        format!("{} to knight", RANKS[1].0 - r.round_ties_even() as i64),
        MUTED,
    )
}

pub fn elo_badge(r: f64) -> String {
    let (name, color) = rank_of(r);
    badge("elo", &format!("{} · {name}", f0(r)), color)
}

/// The current Elo: the last day's, or START with nothing scored.
pub fn current(ctx: &Ctx, ev: &Evidence) -> f64 {
    elo(&games(ctx, ev), START)
        .last()
        .map(|x| x.1)
        .unwrap_or(START)
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("elo.svg");
    let badge_path = ctx.graph_dir().join("elo_badge.svg");
    let gs = games(ctx, ev);
    if gs.is_empty() {
        println!("no scored attempts");
        return;
    }
    let hist = elo(&gs, START);
    let (d0, d1) = (hist[0].0, hist[hist.len() - 1].0);
    let span = days_between(d0, d1).max(1);
    let (top, bottom) = (MT, H - MB);
    let vals: Vec<f64> = hist.iter().map(|x| x.1).collect();
    let lo = vals
        .iter()
        .cloned()
        .fold(f64::INFINITY, f64::min)
        .min(RANKS[1].0 as f64)
        - 100.0;
    let hi = vals
        .iter()
        .cloned()
        .fold(f64::NEG_INFINITY, f64::max)
        .max(RANKS[0].0 as f64)
        + 100.0;
    let (lo, hi) = (floor_to(lo, 100), ceil_to(hi, 100));
    let x_of =
        |d: NaiveDate| ML as f64 + days_between(d0, d) as f64 / span as f64 * (W - ML - MR) as f64;
    let y_of = |v: f64| bottom as f64 - (v - lo as f64) / (hi - lo) as f64 * (bottom - top) as f64;

    let n_win = gs.iter().filter(|g| g.2 == 1.0).count();
    let n_draw = gs.iter().filter(|g| g.2 == 0.5).count();
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"26\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} games, {n_win} wins, {n_draw} draws, {} losses</text>",
            f0(W as f64 / 2.0),
            gs.len(),
            gs.len() - n_win - n_draw
        ),
    ];
    rank_bands(&mut svg, &RANKS, y_of, ML, W, MR, top);
    value_ticks(&mut svg, lo, hi, 100, y_of, ML, W - MR);
    month_ticks(&mut svg, d0, d1, x_of, top, bottom, 1);
    for (series, color, opacity) in [
        (&hist, LINE, elo_opacity().as_str()),
        (&elo_ma(&gs, START, &[]), MA_LINE, "1"),
    ] {
        for run in runs(series) {
            svg.push(format!(
                "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\" stroke-opacity=\"{opacity}\"/>",
                points(&run, x_of, y_of)
            ));
        }
    }
    let mut legend = Legend::new(ML, true, MT - 18);
    legend.line(&mut svg, LINE, "elo", false);
    legend.line(
        &mut svg,
        MA_LINE,
        &format!("{MA} game moving average"),
        false,
    );
    let last = hist[hist.len() - 1].1;
    svg.push(format!(
        "<circle cx=\"{}\" cy=\"{}\" r=\"4\" fill=\"{LINE}\"/>",
        f1(x_of(d1)),
        f1(y_of(last))
    ));
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"12\" fill=\"{LINE}\">{}</text>",
        f1(x_of(d1)),
        f1(y_of(last) - 12.0),
        f0(last)
    ));
    svg.push("</svg>".to_string());
    write(&out, &svg);
    std::fs::write(&badge_path, elo_badge(last)).expect("write badge");
    let (name, _) = rank_of(last);
    println!(
        "wrote {} and {} ({} games, elo {}, {name})",
        out.display(),
        badge_path.display(),
        gs.len(),
        f0(last)
    );
}

/// The numbers make elo shows, from the same functions as the chart. None
/// with nothing scored.
pub struct Numbers {
    /// the first-sight Elo after the last game
    pub elo: f64,
    /// mean of the Elo after each of the last MA games, once MA exist
    pub ma: Option<f64>,
    /// performance rating over the last onsite::FS_WINDOW days
    pub late: f64,
    /// kg::model::elo_now: the picker's Elo over every timed attempt
    pub picker: f64,
    /// (date, Elo after the day's last game) one per day with a game
    pub history: Vec<(NaiveDate, f64)>,
    pub games: usize,
    pub wins: usize,
    pub draws: usize,
    /// every scored game of the last WEEK days, repeats included, as
    /// `make stats` counts them
    pub week: kg::model::Summary,
}

/// The window of the summary under the dashboard's gauges.
pub const WEEK: i64 = 7;

pub fn numbers(ctx: &Ctx, ev: &Evidence) -> Option<Numbers> {
    let gs = games(ctx, ev);
    if gs.is_empty() {
        return None;
    }
    let history = elo(&gs, START);
    let (_, _, late) = crate::onsite::first_sight_rate(&gs, &crate::hours::hours_by_day(ctx));
    let all = scored_games(ctx, ev);
    let week = kg::model::Summary::of(kg::model::games_since(
        &all,
        ctx.today() - chrono::Duration::days(WEEK - 1),
    ));
    Some(Numbers {
        elo: history[history.len() - 1].1,
        ma: elo_ma(&gs, START, &[]).last().map(|x| x.1),
        late,
        picker: kg::model::elo_now(ctx, ev),
        history,
        games: gs.len(),
        wins: gs.iter().filter(|g| g.2 == 1.0).count(),
        draws: gs.iter().filter(|g| g.2 == 0.5).count(),
        week,
    })
}
