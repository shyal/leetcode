// The Elo history and its projection to the onsite line, on calendar
// dates, rendered into graph/onsite.svg.
//
// The onsite is two easies, two mediums and two hards in one sitting,
// passed when both easies, both mediums and at least one hard are solved.
// Each problem is drawn from the rated problems of its difficulty and
// solved with the Elo win probability against its rating, and the onsite
// line is the Elo at which that passes half the time - once for the
// repo's bank (graph/problems.json) and once for every rated problem.
//
// Two projections run forward from today's Elo at the hours per calendar
// day recorded over the last PACE_DAYS days: the Carnegie Mellon rate and
// the first-sight rate, the change in first-sight performance rating
// between the first and the last FS_WINDOW days of history, per recorded
// hour in between. Performance rating is the Elo at which the expected
// score equals the actual score. The served line is the median contest
// rating of the last SERVED games. Each projection is labelled with the
// date it crosses each onsite line.
//
// Ported from utils/readme/kg_onsite_svg (Python) on 2026-09-13.

use chrono::{Duration, NaiveDate};
use kg::ctx::Ctx;
use kg::evidence::Evidence;
use kg::mock::PyRandom;

use crate::common::*;
use crate::elo::{self, G, MA, MA_LINE, RANKS};
use crate::hours;

pub const PACE_DAYS: i64 = 60;
pub const FS_WINDOW: i64 = 60;
pub const SERVED: usize = 50;
pub const CMU_PER_HOUR: f64 = 200.0 / 800.0;
const MAX_YEARS: i64 = 4;

const W: i64 = 1200;
const H: i64 = 400;
const ELO: &str = GREEN;
const SERVED_COLOR: &str = "#bc8cff";
const SLOW: &str = MUTED;
const FAST: &str = BLUE;
const BANK: &str = GOLD;
const ALL: &str = RED;
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 40;

/// Performance rating of [(problem rating, score)]: the Elo at which the
/// expected score equals the actual one.
pub fn perf(rows: &[(f64, f64)]) -> f64 {
    let s = rows.iter().fold(0.0, |a, (_, x)| a + x);
    let (mut lo, mut hi) = (500.0f64, 3500.0f64);
    for _ in 0..50 {
        let mid = (lo + hi) / 2.0;
        let e = rows.iter().fold(0.0, |a, (r, _)| {
            a + 1.0 / (1.0 + 10f64.powf((r - mid) / 400.0))
        });
        if e < s {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    (lo + hi) / 2.0
}

/// [(date, median rating of the last SERVED games)] one per day with a
/// game, once SERVED games exist.
pub fn served(gs: &[G]) -> Vec<(NaiveDate, f64)> {
    let mut out: Vec<(NaiveDate, f64)> = Vec::new();
    for i in (SERVED - 1)..gs.len() {
        let m = median(
            &gs[i + 1 - SERVED..=i]
                .iter()
                .map(|g| g.1)
                .collect::<Vec<_>>(),
        );
        match out.iter_mut().find(|(d, _)| *d == gs[i].0) {
            Some(slot) => slot.1 = m,
            None => out.push((gs[i].0, m)),
        }
    }
    out.sort_by_key(|(d, _)| *d);
    out
}

/// (points per recorded hour, performance rating over the first FS_WINDOW
/// days, the same over the last FS_WINDOW days).
pub fn first_sight_rate(gs: &[G], cum: &[(NaiveDate, f64)]) -> (f64, f64, f64) {
    let (d0, d1) = (gs[0].0, gs[gs.len() - 1].0);
    let early: Vec<(f64, f64)> = gs
        .iter()
        .filter(|g| g.0 < d0 + Duration::days(FS_WINDOW))
        .map(|g| (g.1, g.2))
        .collect();
    let late: Vec<(f64, f64)> = gs
        .iter()
        .filter(|g| g.0 > d1 - Duration::days(FS_WINDOW))
        .map(|g| (g.1, g.2))
        .collect();
    let hours_between = hours::at(cum, d1) - hours::at(cum, d0 - Duration::days(1));
    let (p0, p1) = (perf(&early), perf(&late));
    (
        if hours_between > 0.0 {
            (p1 - p0) / hours_between
        } else {
            0.0
        },
        p0,
        p1,
    )
}

/// The Elo at which the onsite passes half the time against this pool
/// (E, M, H).
pub fn onsite_elo(pool: &[Vec<f64>; 3], rng: &mut PyRandom) -> i64 {
    let mut p = |elo: f64| {
        let n = 4000;
        let mut ok = 0;
        for _ in 0..n {
            let mut s = [0, 0, 0];
            for d in [0, 0, 1, 1, 2, 2] {
                let r = pool[d][rng.randbelow(pool[d].len() as u32) as usize];
                if rng.random() < 1.0 / (1.0 + 10f64.powf((r - elo) / 400.0)) {
                    s[d] += 1;
                }
            }
            if s[0] == 2 && s[1] == 2 && s[2] >= 1 {
                ok += 1;
            }
        }
        ok as f64 / n as f64
    };
    let (mut lo, mut hi) = (1200.0f64, 3000.0f64);
    for _ in 0..12 {
        let mid = (lo + hi) / 2.0;
        if p(mid) < 0.5 {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    ((lo + hi) / 2.0).round_ties_even() as i64
}

fn diff_index(d: &str) -> Option<usize> {
    match d.chars().next()? {
        'E' => Some(0),
        'M' => Some(1),
        'H' => Some(2),
        _ => None,
    }
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("onsite.svg");
    let gs = elo::games(ctx, ev);
    let curve = elo::elo(&gs, elo::START);
    let cum = hours::hours_by_day(ctx);
    let today = ctx.today();

    let bank = ctx.evidenced();
    let mut pools: [[Vec<f64>; 3]; 2] = Default::default();
    for (pid, rt) in elo::load_ratings(ctx) {
        if let Some(i) = ctx
            .meta
            .get(&pid)
            .and_then(|m| m.difficulty.as_deref())
            .and_then(diff_index)
        {
            pools[1][i].push(rt);
            if bank.contains_key(&pid) {
                pools[0][i].push(rt);
            }
        }
    }
    let mut rng = PyRandom::new(1);
    let lines = [
        (
            onsite_elo(&pools[0], &mut rng),
            "onsite 50%, the bank",
            BANK,
        ),
        (
            onsite_elo(&pools[1], &mut rng),
            "onsite 50%, every rated problem",
            ALL,
        ),
    ];

    let pace = (hours::at(&cum, today) - hours::at(&cum, today - Duration::days(PACE_DAYS)))
        / PACE_DAYS as f64;
    let (fs_rate, _, _) = first_sight_rate(&gs, &cum);
    let elo_now = curve[curve.len() - 1].1;
    let fs_label = format!("first-sight rate, {} per 100 hours", f0(fs_rate * 100.0));
    let rates = [
        (
            CMU_PER_HOUR,
            "200 per 800 hours (Carnegie Mellon; the Elo's own rate)".to_string(),
            SLOW,
        ),
        (fs_rate, fs_label, FAST),
    ];

    let cross = |rate: f64, target: f64| -> Option<NaiveDate> {
        if rate <= 0.0 || pace <= 0.0 {
            return None;
        }
        let days = ((target - elo_now) / (rate * pace)).floor() as i64;
        today.checked_add_signed(Duration::days(days))
    };

    let mut horizon = today + Duration::days(365);
    for (r, _, _) in &rates {
        for (t, _, _) in &lines {
            if let Some(c) = cross(*r, *t as f64) {
                if c <= today + Duration::days(365 * MAX_YEARS) {
                    horizon = horizon.max(c);
                }
            }
        }
    }
    let (x0, x1) = (curve[0].0, horizon);
    let span = days_between(x0, x1);
    let (top, bottom) = (MT, H - MB);
    let srv = served(&gs);
    let lo = floor_to(
        curve
            .iter()
            .chain(srv.iter())
            .map(|x| x.1)
            .fold(f64::INFINITY, f64::min),
        100,
    ) - 100;
    let hi = lines.iter().map(|l| l.0).max().unwrap() / 100 * 100 + 200;
    let x_of =
        |d: NaiveDate| ML as f64 + days_between(x0, d) as f64 / span as f64 * (W - ML - MR) as f64;
    let y_of = |v: f64| bottom as f64 - (v - lo as f64) / (hi - lo) as f64 * (bottom - top) as f64;

    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">elo {} - {} recorded hours a day over the last {PACE_DAYS} days</text>",
            f0(W as f64 / 2.0),
            f0(elo_now),
            f1(pace)
        ),
    ];
    value_ticks(&mut svg, lo, hi, 200, y_of, ML, W - MR);
    month_ticks(
        &mut svg,
        x0,
        x1,
        x_of,
        top,
        bottom,
        if span > 900 { 3 } else { 1 },
    );
    for (cut, name, color) in RANKS {
        let y = y_of(cut as f64);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"1\" stroke-dasharray=\"4 4\" stroke-opacity=\"0.6\"/>",
            f1(y),
            W - MR,
            f1(y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{color}\">{name} {cut}</text>",
            ML + 4,
            f1(y - 5.0)
        ));
    }
    for (target, label, color) in &lines {
        let y = y_of(*target as f64);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"1.5\"/>",
            f1(y),
            W - MR,
            f1(y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{color}\">{label} {target}</text>",
            ML + 4,
            f1(y + 14.0)
        ));
    }
    let xt = x_of(today);
    svg.push(format!(
        "<line x1=\"{}\" y1=\"{top}\" x2=\"{}\" y2=\"{bottom}\" stroke=\"{MUTED}\" stroke-width=\"1\" stroke-dasharray=\"2 3\"/>",
        f1(xt),
        f1(xt)
    ));
    for (rate, _, color) in &rates {
        let end = if *rate > 0.0 {
            cross(*rate, hi as f64).unwrap_or(x1).min(x1)
        } else {
            x1
        };
        let y_end = elo_now + rate * pace * days_between(today, end) as f64;
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"1.5\" stroke-dasharray=\"6 4\"/>",
            f1(xt),
            f1(y_of(elo_now)),
            f1(x_of(end)),
            f1(y_of(y_end))
        ));
        for (target, _, _) in &lines {
            let Some(c) = cross(*rate, *target as f64) else {
                continue;
            };
            let ty = y_of(*target as f64);
            if c <= x1 {
                let cx = x_of(c);
                let near_edge = cx > (W - MR - 70) as f64;
                svg.push(format!(
                    "<circle cx=\"{}\" cy=\"{}\" r=\"4\" fill=\"{color}\"/>",
                    f1(cx),
                    f1(ty)
                ));
                svg.push(format!(
                    "<text x=\"{}\" y=\"{}\" text-anchor=\"{}\" font-size=\"11\" fill=\"{color}\">{}</text>",
                    f1(if near_edge { cx - 7.0 } else { cx + 7.0 }),
                    f1(ty + 14.0),
                    if near_edge { "end" } else { "start" },
                    c.format("%b %Y")
                ));
            } else {
                svg.push(format!(
                    "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{color}\">{} at this rate</text>",
                    W - MR - 4,
                    f1(ty + 14.0),
                    c.format("%b %Y")
                ));
            }
        }
    }
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{SERVED_COLOR}\" stroke-width=\"1.5\"/>",
        points(&srv, x_of, y_of)
    ));
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{ELO}\" stroke-width=\"2\" stroke-opacity=\"{}\"/>",
        points(&curve, x_of, y_of),
        elo_opacity()
    ));
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{MA_LINE}\" stroke-width=\"2\"/>",
        points(&elo::elo_ma(&gs, elo::START, &[]), x_of, y_of)
    ));
    // the proven rating (kg::model::proven_series): the level line that the
    // easy problems of 2025 cannot inflate (settled 2026-09-20)
    let proven = elo::proven(&gs);
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{}\" stroke-width=\"2\"/>",
        points(&proven, x_of, y_of),
        elo::PROVEN_LINE
    ));
    if let Some((d, v)) = proven.last() {
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"12\" fill=\"{}\">{}</text>",
            f1(x_of(*d)),
            f1(y_of(*v) + 16.0),
            elo::PROVEN_LINE,
            f0(*v)
        ));
    }
    let mut legend = Legend::new(ML, true, MT - 18);
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
    legend.line(
        &mut svg,
        SERVED_COLOR,
        &format!("median rating of the last {SERVED} problems served"),
        false,
    );
    for (_, label, color) in &rates {
        legend.line(&mut svg, color, label, false);
    }
    svg.push("</svg>".to_string());
    write(&out, &svg);
    let crossings: Vec<String> = rates
        .iter()
        .flat_map(|(r, l, _)| {
            lines.iter().map(move |(t, _, _)| {
                let c = cross(*r, *t as f64);
                format!(
                    "{} -> {t}: {}",
                    l.split(',').next().unwrap(),
                    c.map(|c| c.format("%b %Y").to_string())
                        .unwrap_or_else(|| "never".to_string())
                )
            })
        })
        .collect();
    println!(
        "wrote {} (elo {}, {}h/day, first-sight rate {}/100h, onsite at {} (bank) / {} (all); {})",
        out.display(),
        f0(elo_now),
        f1(pace),
        f0(fs_rate * 100.0),
        lines[0].0,
        lines[1].0,
        crossings.join(", ")
    );
}
