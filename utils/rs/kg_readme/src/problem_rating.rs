// The contest rating of every problem attempted, one dot per attempt,
// rendered into graph/problem_rating.svg.
//
// A rating is zerotrac's where the problem has one, else CLIST's rescaled
// onto that scale (kg::model::solve_ratings). The Elo of elo.rs is scored
// against the same numbers and drawn as the second line. Every evidenced
// attempt on a numbered problem is a dot, coloured by how it went:
// unaided, then the assist level (hint, walkthrough, learning), then
// failed. The solid blue line is the median rating of the last WINDOW
// attempts.
//
// Past today the chart is a forecast: the real picker run forward HORIZON
// days on simulated evidence (utils/rs/kg_simulate --json), once per seed
// in SEEDS, the runs cached in graph/problem_forecast.json for CACHE_DAYS.
// Each first sight plays an Elo game priced as elo.rs prices one, stepped
// from the Elo the history ends on. --forecast reruns now; --no-forecast
// skips the fan. The same runs carry a day-by-day series (solves by kind,
// STALE and FRAGILE counts, the review backlog) that backlog.rs draws
// after its history, so one set of runs serves both charts.
//
// Ported from utils/readme/kg_problem_rating_svg (Python) on 2026-09-13.

use std::collections::HashMap;
use std::path::Path;
use std::process::Command;

use chrono::{Duration, NaiveDate};
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::evidence::Evidence;
use kg::model::solve_ratings;
use serde_json::{json, Value};

use crate::common::*;
use crate::elo::{self, G, MA, MA_LINE, RANKS, START};

const WINDOW: usize = 50;
const HORIZON: i64 = 180;
const SEEDS: [i64; 5] = [1, 2, 3, 4, 5];
const CACHE_DAYS: i64 = 7;

const W: i64 = 1200;
const H: i64 = 1000;
const H_MONTH: i64 = 600;
/// The zoomed chart's window, in days.
const MONTH: i64 = 30;
const DOT: &str = BLUE;
const ELO: &str = GREEN;
const SIM: &str = "#6e7681";
const TODAY: &str = "#f0f6fc";
// (outcome, label, colour, opacity) heaviest last
const OUTCOMES: [(&str, &str, &str, &str); 5] = [
    ("none", "unaided", DOT, "0.35"),
    ("hint", "hint", "#d29922", "0.9"),
    ("walkthrough", "walkthrough", "#db6d28", "0.9"),
    ("learning", "learning", "#a371f7", "0.9"),
    ("failed", "failed", "#f85149", "0.9"),
];
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 40;

/// (date, rating, outcome): one evidenced attempt.
type Att = (NaiveDate, f64, String);

/// One per evidenced attempt on a numbered problem the rating tables
/// cover, oldest first.
fn attempts(ctx: &Ctx, ev: &Evidence) -> Vec<Att> {
    let ratings = solve_ratings(ctx);
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| (&ev.rec(a).date, ev.fname(a)).cmp(&(&ev.rec(b).date, ev.fname(b))));
    let mut out = Vec::new();
    for i in order {
        let rec = ev.rec(i);
        let pnum = rec.problem.clone().unwrap_or_default();
        if !pnum.chars().next().is_some_and(|c| c.is_ascii_digit()) {
            continue;
        }
        let Some(r) = ratings.get(&pnum) else {
            continue;
        };
        if kg::clock::is_studied(ev.fname(i)) {
            continue; // read, not attempted
        }
        let outcome = if ev.fname(i).contains("FAILED") {
            "failed"
        } else {
            rec.assist_any()
        };
        out.push((parse_date(&rec.date), *r, outcome.to_string()));
    }
    out
}

/// [(date, median rating of the last WINDOW attempts)] one per day with an
/// attempt; a gap of over a month starts the window again.
fn trailing_median(att: &[Att]) -> Vec<(NaiveDate, f64)> {
    let mut by_day: Vec<(NaiveDate, f64)> = Vec::new();
    let mut window: Vec<f64> = Vec::new();
    let mut prev: Option<NaiveDate> = None;
    for (d, r, _) in att {
        if prev.is_some_and(|p| days_between(p, *d) > 31) {
            window.clear();
        }
        window.push(*r);
        if window.len() > WINDOW {
            window.drain(..window.len() - WINDOW);
        }
        let m = median(&window);
        match by_day.iter_mut().find(|(dd, _)| dd == d) {
            Some(slot) => slot.1 = m,
            None => by_day.push((*d, m)),
        }
        prev = Some(*d);
    }
    by_day.sort_by_key(|(d, _)| *d);
    by_day
}

pub struct Run {
    pub seed: i64,
    pub start: NaiveDate,
    /// every attempt on a numbered problem: date, problem, difficulty,
    /// rating, first, score
    pub attempts: Vec<Value>,
    /// one row per simulated day: day, solves (by kind), stale, fragile,
    /// missing, open, due, drills_due, onsite, screen, hard
    pub series: Vec<Value>,
    pub hours: f64,
    pub source: String,
}

impl Run {
    fn from_value(seed: i64, start: NaiveDate, r: &Value) -> Run {
        Run {
            seed,
            start,
            attempts: r["attempts"].as_array().cloned().unwrap_or_default(),
            series: r["series"].as_array().cloned().unwrap_or_default(),
            hours: r["hours"].as_f64().unwrap_or(0.0),
            source: r["source"].as_str().unwrap_or("").to_string(),
        }
    }
}

/// One run of the real picker, HORIZON days from today, as the simulator
/// prints it under --json; None when the run cannot start.
fn simulate(root: &Path, seed: i64) -> Option<Value> {
    // the sibling binary of this workspace build
    let bin = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.join("kg_simulate")))
        .unwrap_or_else(|| root.join("utils/rs/target/release/kg_simulate"));
    let out = Command::new(bin)
        .args([
            "--seed",
            &seed.to_string(),
            "--days",
            &HORIZON.to_string(),
            "--json",
        ])
        .current_dir(root)
        .output()
        .ok()?;
    if !out.status.success() {
        println!(
            "no forecast: {}",
            String::from_utf8_lossy(&out.stderr).trim()
        );
        return None;
    }
    serde_json::from_slice(&out.stdout).ok()
}

fn cache_path(ctx: &Ctx) -> std::path::PathBuf {
    ctx.graph_dir().join("problem_forecast.json")
}

/// The cached runs when written within CACHE_DAYS with the same seeds and
/// horizon, every run carrying its series; else None.
fn cached_runs(ctx: &Ctx) -> Option<Vec<Run>> {
    let c: Value = serde_json::from_str(&std::fs::read_to_string(cache_path(ctx)).ok()?).ok()?;
    let start = parse_date(c.get("start")?.as_str()?);
    if days_between(start, ctx.today()) >= CACHE_DAYS
        || c.get("seeds") != Some(&json!(SEEDS))
        || c.get("horizon") != Some(&json!(HORIZON))
    {
        return None;
    }
    let runs = c["runs"].as_array()?;
    if runs.iter().any(|r| !r["series"].is_array()) {
        return None;
    }
    Some(
        runs.iter()
            .map(|r| Run::from_value(r["seed"].as_i64().unwrap_or(0), start, r))
            .collect(),
    )
}

/// The runs behind the forecast: the cache when it is fresh, else every
/// seed run now; none under --no-forecast. --forecast reruns now.
pub fn forecast_runs(ctx: &Ctx, args: &[String]) -> Vec<Run> {
    if args.iter().any(|a| a == "--no-forecast") {
        return Vec::new();
    }
    let runs = if args.iter().any(|a| a == "--forecast") {
        None
    } else {
        cached_runs(ctx)
    };
    runs.unwrap_or_else(|| fresh_runs(ctx))
}

/// Run every seed, one process each, and write the cache.
fn fresh_runs(ctx: &Ctx) -> Vec<Run> {
    let root: &Path = &ctx.root;
    let results: Vec<Option<Value>> = std::thread::scope(|sc| {
        let hs: Vec<_> = SEEDS
            .iter()
            .map(|s| sc.spawn(move || simulate(root, *s)))
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).collect()
    });
    let runs: Vec<(i64, Value)> = SEEDS
        .iter()
        .zip(results)
        .filter_map(|(s, r)| r.map(|r| (*s, r)))
        .collect();
    if runs.is_empty() {
        return Vec::new();
    }
    let start = runs[0].1["start"].as_str().unwrap().to_string();
    let cache = json!({
        "start": start,
        "seeds": SEEDS,
        "horizon": HORIZON,
        "runs": runs.iter().map(|(s, r)| json!({
            "seed": s,
            "hours": r["hours"],
            "source": r["source"],
            "attempts": r["attempts"],
            "series": r["series"],
        })).collect::<Vec<_>>(),
    });
    std::fs::write(cache_path(ctx), serde_json::to_string(&cache).unwrap()).expect("write cache");
    let start = parse_date(&start);
    runs.into_iter()
        .map(|(seed, r)| Run::from_value(seed, start, &r))
        .collect()
}

struct Forecast {
    start: NaiveDate,
    sim: Vec<(NaiveDate, f64)>,
    med: Vec<(NaiveDate, f64)>,
    elo: Vec<(NaiveDate, f64)>,
    ma: Vec<(NaiveDate, f64)>,
}

/// One per seed that ran: the simulated attempts, the trailing median
/// continued over them, and the Elo and its moving average stepped on
/// from the history's games up to the start day.
fn forecast(ctx: &Ctx, ev: &Evidence, att: &[Att], args: &[String]) -> Vec<Forecast> {
    let runs = forecast_runs(ctx, args);
    let gs = elo::games(ctx, ev);
    let (ratings, imputed) = elo::pricing(ctx);
    let mut out = Vec::new();
    for run in runs {
        let past_games: Vec<G> = gs.iter().filter(|g| g.0 <= run.start).cloned().collect();
        let after = elo::elo_after(&past_games, START);
        let elo0 = after.last().map(|a| a.1).unwrap_or(START);
        let sim: Vec<(NaiveDate, f64)> = run
            .attempts
            .iter()
            .map(|a| {
                (
                    parse_date(a["date"].as_str().unwrap()),
                    a["rating"].as_f64().unwrap(),
                )
            })
            .collect();
        let games: Vec<G> = run
            .attempts
            .iter()
            .filter(|a| !a["score"].is_null())
            .map(|a| {
                (
                    parse_date(a["date"].as_str().unwrap()),
                    elo::price(
                        &ratings,
                        &imputed,
                        &kg::data::value_str(&a["problem"]),
                        a["difficulty"].as_str().unwrap_or(""),
                    ),
                    a["score"].as_f64().unwrap(),
                )
            })
            .collect();
        let mut past: Vec<Att> = att.iter().filter(|a| a.0 <= run.start).cloned().collect();
        past.extend(sim.iter().map(|(d, r)| (*d, *r, "sim".to_string())));
        let med = trailing_median(&past)
            .into_iter()
            .filter(|(d, _)| *d > run.start)
            .collect();
        let _ = run.seed;
        out.push(Forecast {
            start: run.start,
            sim,
            med,
            elo: elo::elo(&games, elo0),
            ma: elo::elo_ma(&games, elo0, &after),
        });
    }
    out
}

/// " - forecast: N game average A to B in D days over S seeds", or "".
fn forecast_note(fc: &[Forecast], n: usize) -> String {
    let ends: Vec<f64> = fc.iter().filter_map(|f| f.ma.last().map(|x| x.1)).collect();
    if ends.is_empty() {
        return String::new();
    }
    let days = fc
        .iter()
        .filter(|f| !f.sim.is_empty())
        .map(|f| days_between(f.sim[0].0, f.sim[f.sim.len() - 1].0) + 1)
        .max()
        .unwrap_or(0);
    let lo = ends.iter().cloned().fold(f64::INFINITY, f64::min);
    let hi = ends.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    format!(
        " - forecast: {n} game average {}{} in {days} days over {} seed{}",
        f0(lo),
        if hi - lo >= 1.0 {
            format!(" to {}", f0(hi))
        } else {
            String::new()
        },
        fc.len(),
        if fc.len() > 1 { "s" } else { "" }
    )
}

fn draw_forecast<F: Fn(NaiveDate) -> f64 + Copy, Y: Fn(f64) -> f64 + Copy>(
    svg: &mut Vec<String>,
    fc: &[Forecast],
    x_of: F,
    y_of: Y,
    top: i64,
    bottom: i64,
    today: NaiveDate,
) {
    let start = fc[0].start;
    let x = x_of(start);
    svg.push(format!(
        "<line x1=\"{}\" y1=\"{top}\" x2=\"{}\" y2=\"{bottom}\" stroke=\"{TODAY}\" stroke-width=\"1\" stroke-opacity=\"0.5\" stroke-dasharray=\"2 3\"/>",
        f1(x),
        f1(x)
    ));
    let label = if start >= today {
        "today".to_string()
    } else {
        format!("forecast from {start}")
    };
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{TODAY}\" fill-opacity=\"0.7\">{label}</text>",
        f1(x + 4.0),
        top + 12
    ));
    let sim = sim_opacity();
    for (d, r) in &fc[0].sim {
        svg.push(format!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"2.5\" fill=\"{SIM}\" fill-opacity=\"{sim}\"/>",
            f1(x_of(*d)),
            f1(y_of(*r))
        ));
    }
    for (i, f) in fc.iter().enumerate() {
        let width = if i == 0 { 2 } else { 1 };
        for (series, color) in [(&f.elo, ELO), (&f.ma, MA_LINE), (&f.med, DOT)] {
            for run in runs(series) {
                svg.push(format!(
                    "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"{width}\" stroke-opacity=\"{sim}\" stroke-dasharray=\"6 4\"/>",
                    points(&run, x_of, y_of)
                ));
            }
        }
    }
}

/// A series with its colour and its label, for annotate_ends.
type Labelled<'a> = (&'a Vec<(NaiveDate, f64)>, &'a str, &'a str);

/// An arrow from a label to the last point of each series, the current
/// value on the label, so the three lines can be read where they end.
/// Labels sit to the left of the point and are pushed apart vertically
/// when two ends are close.
fn annotate_ends<F: Fn(NaiveDate) -> f64, Y: Fn(f64) -> f64>(
    svg: &mut Vec<String>,
    series: &[Labelled],
    x_of: F,
    y_of: Y,
    top: i64,
    bottom: i64,
) {
    const GAP: f64 = 14.0;
    const REACH: f64 = 90.0;
    let mut ends: Vec<(f64, f64, f64, &str, &str)> = series
        .iter()
        .filter_map(|(s, color, label)| {
            s.last()
                .map(|(d, v)| (x_of(*d), y_of(*v), *v, *color, *label))
        })
        .collect();
    ends.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());
    // the labels stack above the highest end, so no line runs through
    // them; the topmost end gets the lowest label
    let base = ends.first().map(|e| e.1).unwrap_or(0.0) - 12.0;
    let mut ys: Vec<f64> = (0..ends.len()).map(|i| base - GAP * i as f64).collect();
    let overflow = (top as f64 + 10.0 - ys.last().copied().unwrap_or(0.0)).max(0.0);
    for y in ys.iter_mut() {
        *y = (*y + overflow).min(bottom as f64 - 4.0);
    }
    for ((x, y, v, color, label), ly) in ends.iter().zip(ys) {
        let (tx, ty) = (x - REACH, ly);
        let (dx, dy) = (x - tx, y - ty);
        let len = (dx * dx + dy * dy).sqrt().max(1.0);
        let (ux, uy) = (dx / len, dy / len);
        let (hx, hy) = (x - ux * 5.0, y - uy * 5.0);
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"1\"/>",
            f1(tx + 2.0),
            f1(ty),
            f1(hx),
            f1(hy)
        ));
        svg.push(format!(
            "<polygon points=\"{},{} {},{} {},{}\" fill=\"{color}\"/>",
            f1(*x - ux * 2.0),
            f1(*y - uy * 2.0),
            f1(hx - uy * 3.0),
            f1(hy + ux * 3.0),
            f1(hx + uy * 3.0),
            f1(hy - ux * 3.0)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{color}\">{label} {}</text>",
            f1(tx - 2.0),
            f1(ty + 4.0),
            f0(*v)
        ));
    }
}

pub fn render(ctx: &Ctx, ev: &Evidence, args: &[String]) {
    draw(ctx, ev, args, None);
}

/// problem_rating_month.svg: the same chart over the last MONTH days,
/// without the forecast.
pub fn render_month(ctx: &Ctx, ev: &Evidence) {
    draw(ctx, ev, &[], Some(MONTH));
}

fn draw(ctx: &Ctx, ev: &Evidence, args: &[String], days: Option<i64>) {
    let out = ctx.graph_dir().join(if days.is_some() {
        "problem_rating_month.svg"
    } else {
        "problem_rating.svg"
    });
    let mut att = attempts(ctx, ev);
    if att.is_empty() {
        println!("no rated attempts");
        return;
    }
    let mut med = trailing_median(&att);
    let gs = elo::games(ctx, ev);
    let (mut elo_hist, mut ma) = (elo::elo(&gs, START), elo::elo_ma(&gs, START, &[]));
    // the proven rating (kg::model::proven_series, settled 2026-09-20)
    let mut proven = elo::proven(&gs);
    let fc = if days.is_some() {
        Vec::new()
    } else {
        forecast(ctx, ev, &att, args)
    };
    let today = elo_hist
        .last()
        .map(|e| e.0.max(att[att.len() - 1].0))
        .unwrap_or(att[att.len() - 1].0);
    let d0 = match days {
        Some(n) => {
            let since = today - Duration::days(n);
            att.retain(|a| a.0 >= since);
            med.retain(|m| m.0 >= since);
            elo_hist.retain(|e| e.0 >= since);
            ma.retain(|m| m.0 >= since);
            proven.retain(|m| m.0 >= since);
            if att.is_empty() {
                println!("no rated attempts in the last {n} days");
                return;
            }
            since
        }
        None => elo_hist
            .first()
            .map(|e| e.0.min(att[0].0))
            .unwrap_or(att[0].0),
    };
    let d1 = fc
        .iter()
        .flat_map(|f| f.sim.iter().map(|s| s.0))
        .fold(today, NaiveDate::max);
    let span = days_between(d0, d1).max(1);
    let h = if days.is_some() { H_MONTH } else { H };
    let (top, bottom) = (MT, h - MB);
    let vals: Vec<f64> = att
        .iter()
        .map(|a| a.1)
        .chain(elo_hist.iter().map(|e| e.1))
        .chain(fc.iter().flat_map(|f| f.sim.iter().map(|s| s.1)))
        .chain(fc.iter().flat_map(|f| f.elo.iter().map(|e| e.1)))
        .collect();
    let (vmin, vmax) = (
        vals.iter().cloned().fold(f64::INFINITY, f64::min),
        vals.iter().cloned().fold(f64::NEG_INFINITY, f64::max),
    );
    // the month zooms: 50 point grid, no padding to the top rank
    let step = if days.is_some() { 50 } else { 100 };
    let lo = floor_to(vmin, step) - step;
    let hi = if days.is_some() {
        ceil_to(vmax, step) + step
    } else {
        ceil_to(vmax, step).max(RANKS[0].0) + step
    };
    let x_of =
        |d: NaiveDate| ML as f64 + days_between(d0, d) as f64 / span as f64 * (W - ML - MR) as f64;
    let y_of = |v: f64| bottom as f64 - (v - lo as f64) / (hi - lo) as f64 * (bottom - top) as f64;

    let mut counts: HashMap<&str, usize> = HashMap::new();
    for a in &att {
        *counts.entry(a.2.as_str()).or_default() += 1;
    }
    let tally = OUTCOMES
        .iter()
        .filter(|(k, _, _, _)| counts.get(k).copied().unwrap_or(0) > 0)
        .map(|(k, label, _, _)| format!("{} {label}", counts[k]))
        .collect::<Vec<_>>()
        .join(", ");
    let med_all = median(&att.iter().map(|a| a.1).collect::<Vec<_>>());
    let note = forecast_note(&fc, MA);
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {h}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{h}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{}{} attempts - {tally} - median rating {}{note}</text>",
            f0(W as f64 / 2.0),
            days.map(|n| format!("last {n} days: ")).unwrap_or_default(),
            att.len(),
            f0(med_all)
        ),
    ];
    let ranks: Vec<(i64, &str, &str)> = RANKS
        .iter()
        .filter(|r| r.0 > lo && r.0 < hi)
        .cloned()
        .collect();
    rank_bands(&mut svg, &ranks, y_of, ML, W, MR, top);
    if days.is_some() {
        value_ticks(&mut svg, lo, hi, step, y_of, ML, W - MR);
        day_ticks(&mut svg, d0, d1, x_of, top, bottom, 7);
    } else {
        value_ticks(&mut svg, lo, hi, 200, y_of, ML, W - MR);
        month_ticks(&mut svg, d0, d1, x_of, top, bottom, 1);
    }
    // dots first, lines over them; unaided dots go down first so the rare
    // assisted and failed ones sit on top of the pile
    let order = |k: &str| OUTCOMES.iter().position(|o| o.0 == k).unwrap_or(0);
    let mut sorted: Vec<&Att> = att.iter().collect();
    sorted.sort_by_key(|a| order(&a.2));
    for (d, r, outcome) in sorted {
        let (color, opacity) = OUTCOMES
            .iter()
            .find(|o| o.0 == outcome)
            .map(|o| (o.2, o.3))
            .unwrap_or((OUTCOMES[0].2, OUTCOMES[0].3));
        svg.push(format!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"2.5\" fill=\"{color}\" fill-opacity=\"{opacity}\"/>",
            f1(x_of(*d)),
            f1(y_of(*r))
        ));
    }
    for (series, color, opacity) in [
        (&elo_hist, ELO, elo_opacity().as_str()),
        (&ma, MA_LINE, "1"),
        (&med, DOT, "1"),
        (&proven, elo::PROVEN_LINE, "1"),
    ] {
        for run in runs(series) {
            svg.push(format!(
                "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\" stroke-opacity=\"{opacity}\"/>",
                points(&run, x_of, y_of)
            ));
        }
    }
    if !fc.is_empty() {
        draw_forecast(&mut svg, &fc, x_of, y_of, top, bottom, today);
    }
    annotate_ends(
        &mut svg,
        &[
            (&elo_hist, ELO, "elo"),
            (&ma, MA_LINE, "average"),
            (&med, DOT, "median"),
            (&proven, elo::PROVEN_LINE, "proven"),
        ],
        x_of,
        y_of,
        top,
        bottom,
    );
    let mut legend = Legend::new(ML, true, MT - 18);
    for (k, label, color, _) in OUTCOMES {
        if counts.get(k).copied().unwrap_or(0) > 0 {
            legend.dot(&mut svg, color, label);
        }
    }
    legend.line(&mut svg, DOT, &format!("median of last {WINDOW}"), false);
    legend.line(&mut svg, ELO, "elo", false);
    legend.line(
        &mut svg,
        MA_LINE,
        &format!("{MA} game moving average"),
        false,
    );
    legend.line(
        &mut svg,
        elo::PROVEN_LINE,
        &format!(
            "proven rating, last {} first sights",
            kg::model::PROVEN_WINDOW
        ),
        false,
    );
    if !fc.is_empty() {
        legend.dot(
            &mut svg,
            SIM,
            &format!("forecast, dashed: {} seeds of the picker", fc.len()),
        );
    }
    svg.push("</svg>".to_string());
    write(&out, &svg);
    println!(
        "wrote {} ({} attempts - {tally} - median {}{note})",
        out.display(),
        att.len(),
        f0(med_all)
    );
}
