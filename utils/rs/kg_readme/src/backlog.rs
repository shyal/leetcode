// The backlog and the forecast on one time axis, rendered into
// graph/backlog.svg. Left of today, what happened, from evidence.json day
// by day. Right of today, what kg_simulate says happens next: the real
// picker run forward at the measured pace (problem_rating::forecast_runs, the
// cached runs the problems chart draws).
//
// Three lanes share the x axis:
//   backlog  open cards, due cards, due drills (kg::clock::backlog: the
//            same clocks the picker runs)
//   volume   cumulative solves by kind (Easy, Medium, Hard, drill), stacked
//   nodes    STALE and FRAGILE node counts at the end of each day
//
// The forecast is one draw per seed: every seed in the backlog and nodes
// lanes, the first seed alone in the volume lane and in the title.
//
// Ported from utils/readme/kg_backlog_svg and kg_forecast_svg (Python) on
// 2026-09-13; merged, the pass-rate lane dropped, on 2026-09-18.

use chrono::{Duration, NaiveDate};
use kg::clock::backlog;
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::evidence::Evidence;
use kg::status::{all_statuses, FRAGILE, STALE};
use serde_json::Value;

use crate::common::*;
use crate::problem_rating::{self, Run};

const W: i64 = 1200;
const H: i64 = 760;
const ML: i64 = 62;
const MR: i64 = 150;
const TODAY: &str = "#f0f6fc";
const KINDS: [(&str, &str); 4] = [
    ("Easy", "#199e70"),
    ("Medium", "#3987e5"),
    ("Hard", "#d95926"),
    ("drill", "#9085e9"),
];
const BACKLOG: [(&str, &str); 3] = [
    ("open cards", MUTED),
    ("due cards", RED),
    ("due drills", GOLD),
];
const NODES: [(&str, &str); 2] = [("STALE", "#c98500"), ("FRAGILE", "#d55181")];
// (top, bottom) of each lane
const LANE_BACKLOG: (i64, i64) = (64, 250);
const LANE_VOLUME: (i64, i64) = (296, 520);
const LANE_NODES: (i64, i64) = (566, 690);
const LANES: [(i64, i64); 3] = [LANE_BACKLOG, LANE_VOLUME, LANE_NODES];

/// One calendar day, from the history or from a run.
#[derive(Clone, Copy)]
pub struct Day {
    pub date: NaiveDate,
    pub open: i64,
    pub due: i64,
    pub drills: i64,
    /// solves that day, in KINDS order
    pub solves: [i64; 4],
    pub stale: i64,
    pub fragile: i64,
}

fn kind_index(kind: &str) -> Option<usize> {
    KINDS.iter().position(|(k, _)| *k == kind)
}

/// One row per calendar day from the first evidenced attempt to today,
/// each taken from the evidence on file up to that day.
pub fn history(ctx: &Ctx, ev: &Evidence) -> Vec<Day> {
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| (&ev.rec(a).date, ev.fname(a)).cmp(&(&ev.rec(b).date, ev.fname(b))));
    let d0 = parse_date(&ev.rec(order[0]).date);
    // one table grown a day at a time, in date order
    let mut upto = Evidence::new(Vec::new());
    let (mut i, mut out, mut d) = (0, Vec::new(), d0);
    while d <= ctx.today() {
        let cut = d.format("%Y-%m-%d").to_string();
        let mut solves = [0i64; 4];
        while i < order.len() && ev.rec(order[i]).date <= cut {
            let rec = ev.rec(order[i]);
            let kind = match rec.problem.as_deref() {
                Some("drill") => "drill".to_string(),
                Some(p) => ctx.problem_difficulty(p, &ctx.ro.map),
                None => String::new(),
            };
            if let Some(k) = kind_index(&kind) {
                solves[k] += 1;
            }
            upto.push(ev.fname(order[i]).to_string(), rec.clone());
            i += 1;
        }
        let (open, due, drills) = backlog(ctx, &upto, d);
        let statuses = all_statuses(ctx, &upto, d);
        out.push(Day {
            date: d,
            open,
            due,
            drills,
            solves,
            stale: statuses.values().filter(|s| s.0 == STALE).count() as i64,
            fragile: statuses.values().filter(|s| s.0 == FRAGILE).count() as i64,
        });
        d += Duration::days(1);
    }
    out
}

/// A run's series as days.
fn run_days(run: &Run) -> Vec<Day> {
    run.series
        .iter()
        .map(|r: &Value| {
            let mut solves = [0i64; 4];
            for (k, _) in KINDS {
                solves[kind_index(k).unwrap()] = r["solves"][k].as_i64().unwrap_or(0);
            }
            Day {
                date: parse_date(r["day"].as_str().unwrap_or("2000-01-01")),
                open: r["open"].as_i64().unwrap_or(0),
                due: r["due"].as_i64().unwrap_or(0),
                drills: r["drills_due"].as_i64().unwrap_or(0),
                solves,
                stale: r["stale"].as_i64().unwrap_or(0),
                fragile: r["fragile"].as_i64().unwrap_or(0),
            }
        })
        .collect()
}

fn text(x: f64, y: f64, s: &str, size: i64, color: &str, anchor: &str) -> String {
    format!(
        "<text x=\"{}\" y=\"{}\" font-size=\"{size}\" fill=\"{color}\" text-anchor=\"{anchor}\">{s}</text>",
        f1(x),
        f1(y)
    )
}

fn path(pts: &[(f64, f64)], color: &str, width: f64, dash: Option<&str>, opacity: f64) -> String {
    let d = pts
        .iter()
        .map(|(x, y)| format!("{},{}", f1(*x), f1(*y)))
        .collect::<Vec<_>>()
        .join(" L");
    let extra = dash
        .map(|d| format!(" stroke-dasharray=\"{d}\""))
        .unwrap_or_default();
    format!(
        "<path d=\"M{d}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"{width}\" stroke-opacity=\"{opacity}\" stroke-linejoin=\"round\"{extra}/>"
    )
}

fn swatch(svg: &mut Vec<String>, x: f64, y: f64, color: &str, label: &str) {
    svg.push(format!(
        "<rect x=\"{}\" y=\"{}\" width=\"10\" height=\"10\" rx=\"2\" fill=\"{color}\"/>",
        f1(x),
        f1(y - 9.0)
    ));
    svg.push(text(x + 15.0, y, label, 11, INK, "start"));
}

/// The horizontal grid of one lane: a line and a label every `step`.
fn grid(svg: &mut Vec<String>, lane: (i64, i64), ymax: f64, step: f64) {
    let (top, bottom) = lane;
    let mut g = 0.0;
    while g <= ymax + 1e-9 {
        let y = bottom as f64 - g / ymax * (bottom - top) as f64;
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{GRID}\" stroke-width=\"1\"/>",
            f1(y),
            W - MR,
            f1(y)
        ));
        svg.push(text((ML - 8) as f64, y + 4.0, &f0(g), 11, MUTED, "end"));
        g += step;
    }
}

/// A line lane: the history solid, then each run from today on, the
/// first dashed and full, the rest thin and faded.
fn lines<F: Fn(usize) -> f64, Y: Fn(f64) -> f64>(
    svg: &mut Vec<String>,
    past: &[Day],
    runs: &[Vec<Day>],
    pick: impl Fn(&Day) -> i64,
    color: &str,
    x_of: F,
    y_of: Y,
) {
    let p = past.len();
    let hist: Vec<(f64, f64)> = past
        .iter()
        .enumerate()
        .map(|(i, d)| (x_of(i), y_of(pick(d) as f64)))
        .collect();
    svg.push(path(&hist, color, 2.0, None, 1.0));
    for (r, days) in runs.iter().enumerate() {
        let mut pts = vec![hist[p - 1]];
        pts.extend(
            days.iter()
                .enumerate()
                .map(|(j, d)| (x_of(p + j), y_of(pick(d) as f64))),
        );
        if r == 0 {
            svg.push(path(&pts, color, 2.0, Some("5 4"), 1.0));
        } else {
            svg.push(path(&pts, color, 1.0, None, 0.35));
        }
    }
}

pub fn render(ctx: &Ctx, ev: &Evidence, args: &[String]) {
    let out = ctx.graph_dir().join("backlog.svg");
    let past = history(ctx, ev);
    let all_runs = problem_rating::forecast_runs(ctx, args);
    let runs: Vec<Vec<Day>> = all_runs.iter().map(run_days).collect();
    let p = past.len();
    let horizon = runs.iter().map(Vec::len).max().unwrap_or(0);
    let n = p + horizon;
    let x_of = |i: usize| ML as f64 + i as f64 / (n - 1).max(1) as f64 * (W - ML - MR) as f64;
    let today = past[p - 1];

    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
    ];
    let title = match all_runs.first() {
        Some(run) => format!(
            "History, then the forecast: the picker at {}h/day ({}), seed {}, {} days; today: {} open cards, {} due, {} drills due",
            kg::pyjson::g(run.hours),
            run.source,
            run.seed,
            runs[0].len(),
            today.open,
            today.due,
            today.drills
        ),
        None => format!(
            "History; no forecast. today: {} open cards, {} due, {} drills due",
            today.open, today.due, today.drills
        ),
    };
    svg.push(text(W as f64 / 2.0, 24.0, &title, 13, INK, "middle"));

    // the today line through every lane
    let today_x = x_of(p - 1);
    for (top, bottom) in LANES {
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{top}\" x2=\"{}\" y2=\"{bottom}\" stroke=\"{TODAY}\" stroke-width=\"1\" stroke-dasharray=\"2 3\"/>",
            f1(today_x),
            f1(today_x)
        ));
    }
    svg.push(text(
        today_x,
        (LANE_BACKLOG.0 - 8) as f64,
        "today",
        11,
        TODAY,
        "middle",
    ));
    if !runs.is_empty() {
        svg.push(text(
            (today_x + (W - MR) as f64) / 2.0,
            (LANE_BACKLOG.0 - 8) as f64,
            "forecast",
            11,
            MUTED,
            "middle",
        ));
    }

    // --- backlog: open cards, due cards, due drills ---
    {
        let (top, bottom) = LANE_BACKLOG;
        let hi = past
            .iter()
            .chain(runs.iter().flatten())
            .map(|d| d.open.max(d.due).max(d.drills))
            .max()
            .unwrap_or(0)
            .max(5);
        let step = if hi <= 30 {
            5
        } else if hi <= 80 {
            10
        } else {
            25
        };
        let hi = (-(-hi).div_euclid(step) * step) as f64;
        let y_of = |v: f64| bottom as f64 - v / hi * (bottom - top) as f64;
        grid(&mut svg, LANE_BACKLOG, hi, step as f64);
        svg.push(text(
            ML as f64,
            (top - 8) as f64,
            "review backlog: open cards, due cards, due drills",
            11,
            INK,
            "start",
        ));
        let picks: [fn(&Day) -> i64; 3] = [|d| d.open, |d| d.due, |d| d.drills];
        for (i, (label, color)) in BACKLOG.iter().enumerate() {
            lines(&mut svg, &past, &runs, picks[i], color, x_of, y_of);
            let v = [today.open, today.due, today.drills][i];
            swatch(
                &mut svg,
                (W - MR + 6) as f64,
                (top + 14 + i as i64 * 16) as f64,
                color,
                &format!("{label} {v} today"),
            );
        }
    }

    // --- volume: cumulative solves by kind, stacked ---
    {
        let (top, bottom) = LANE_VOLUME;
        let mut cum: [Vec<i64>; 4] = Default::default();
        let mut tot = [0i64; 4];
        for d in past.iter().chain(runs.first().into_iter().flatten()) {
            for k in 0..4 {
                tot[k] += d.solves[k];
                cum[k].push(tot[k]);
            }
        }
        let past_tot: [i64; 4] = std::array::from_fn(|k| cum[k][p - 1]);
        let n_vol = cum[0].len();
        let stack_max = tot.iter().sum::<i64>().max(1) as f64;
        let y_of = |v: f64| bottom as f64 - v / (stack_max * 1.05) * (bottom - top) as f64;
        let step = if stack_max > 1500.0 {
            500.0
        } else if stack_max > 800.0 {
            200.0
        } else if stack_max > 400.0 {
            100.0
        } else if stack_max > 150.0 {
            50.0
        } else {
            20.0
        };
        grid(&mut svg, LANE_VOLUME, stack_max * 1.05, step);
        svg.push(text(
            ML as f64,
            (top - 8) as f64,
            "cumulative solves by kind, stacked (Easy at the bottom)",
            11,
            INK,
            "start",
        ));
        let mut lower = vec![0i64; n_vol];
        for (k, (_, color)) in KINDS.iter().enumerate() {
            let upper: Vec<i64> = lower.iter().zip(&cum[k]).map(|(l, c)| l + c).collect();
            for (lo, hi, op) in [(0, p, "0.75"), (p - 1, n_vol, "0.35")] {
                if hi - lo < 2 {
                    continue;
                }
                let mut pts: Vec<String> = (lo..hi)
                    .map(|i| format!("{},{}", f1(x_of(i)), f1(y_of(upper[i] as f64))))
                    .collect();
                pts.extend(
                    (lo..hi)
                        .rev()
                        .map(|i| format!("{},{}", f1(x_of(i)), f1(y_of(lower[i] as f64)))),
                );
                svg.push(format!(
                    "<polygon points=\"{}\" fill=\"{color}\" fill-opacity=\"{op}\"/>",
                    pts.join(" ")
                ));
            }
            let edge: Vec<(f64, f64)> = upper
                .iter()
                .enumerate()
                .map(|(i, u)| (x_of(i), y_of(*u as f64)))
                .collect();
            svg.push(path(&edge, BG, 2.0, None, 1.0));
            lower = upper;
        }
        // direct labels: count so far, and the forecast's addition
        let mut y_prev: Option<f64> = None;
        let mut lower_end = 0i64;
        for (k, (label, color)) in KINDS.iter().enumerate() {
            let top_end = lower_end + cum[k][n_vol - 1];
            let mut y = y_of((lower_end + top_end) as f64 / 2.0);
            if let Some(yp) = y_prev {
                if yp - y < 13.0 {
                    y = yp - 13.0;
                }
            }
            let mut lab = format!("{label} {}", past_tot[k]);
            if !runs.is_empty() {
                lab += &format!(" +{}", cum[k][n_vol - 1] - past_tot[k]);
            }
            swatch(&mut svg, (W - MR + 6) as f64, y, color, &lab);
            y_prev = Some(y);
            lower_end = top_end;
        }
    }

    // --- nodes: STALE and FRAGILE counts at the end of each day ---
    {
        let (top, bottom) = LANE_NODES;
        let nmax = past
            .iter()
            .chain(runs.iter().flatten())
            .map(|d| d.stale.max(d.fragile))
            .max()
            .unwrap_or(0)
            .max(5) as f64;
        let y_of = |v: f64| bottom as f64 - v / (nmax * 1.15) * (bottom - top) as f64;
        grid(
            &mut svg,
            LANE_NODES,
            nmax * 1.15,
            if nmax > 12.0 { 5.0 } else { 2.0 },
        );
        svg.push(text(
            ML as f64,
            (top - 8) as f64,
            &format!(
                "nodes STALE and FRAGILE at the end of the day, of {}",
                ctx.nodes.len()
            ),
            11,
            INK,
            "start",
        ));
        let picks: [fn(&Day) -> i64; 2] = [|d| d.stale, |d| d.fragile];
        for (i, (label, color)) in NODES.iter().enumerate() {
            lines(&mut svg, &past, &runs, picks[i], color, x_of, y_of);
            swatch(
                &mut svg,
                (W - MR + 6) as f64,
                (top + 14 + i as i64 * 16) as f64,
                color,
                &format!("{label} {} today", [today.stale, today.fragile][i]),
            );
        }
        if runs.len() > 1 {
            svg.push(text(
                (W - MR + 6) as f64,
                (top + 14 + 2 * 16 + 4) as f64,
                &format!(
                    "thin: seeds {}",
                    all_runs[1..]
                        .iter()
                        .map(|r| r.seed.to_string())
                        .collect::<Vec<_>>()
                        .join(", ")
                ),
                11,
                MUTED,
                "start",
            ));
        }
    }

    // month ticks along the bottom; the forecast's dates continue the axis
    let d0 = past[0].date;
    for i in 0..n {
        let d = d0 + Duration::days(i as i64);
        if d.format("%d").to_string() == "01" {
            let x = x_of(i);
            for (top, bottom) in LANES {
                svg.push(format!(
                    "<line x1=\"{}\" y1=\"{top}\" x2=\"{}\" y2=\"{bottom}\" stroke=\"{GRID}\" stroke-width=\"1\"/>",
                    f1(x),
                    f1(x)
                ));
            }
            svg.push(text(
                x,
                (LANE_NODES.1 + 18) as f64,
                &d.format("%b %y").to_string(),
                11,
                MUTED,
                "middle",
            ));
        }
    }
    svg.push(text(
        ML as f64,
        (H - 14) as f64,
        "solid: history from graph/evidence.json. dashed and faded: the forecast, one draw of the real picker per seed (utils/rs/kg_simulate).",
        11,
        MUTED,
        "start",
    ));
    svg.push("</svg>".to_string());
    write(&out, &svg);
    println!(
        "wrote {} ({} days of history, {} forecast days, {} seeds; today: {} open cards, {} due, {} drills due)",
        out.display(),
        p,
        horizon,
        runs.len(),
        today.open,
        today.due,
        today.drills
    );
}
