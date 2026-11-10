// The nodes on their forgetting curves, replayed over the full history.
// Rendered into graph/positions.svg.
//
// The curve in graph/curve.json gives each node a stability s, and the
// memory of the node is (1 + gap/s)^(-beta), where gap is the number of
// days since its last clean rep. The replay shows one dot for each node.
// The dot moves to the right on the curve of the node while the gap
// increases. A clean rep puts the dot back at gap zero, on a flatter
// curve, because the stability increases with the reps. A dot is green
// while its memory is at or above the target retention (SOLID) and gold
// below it (STALE). A node whose last rep was a fail (FRAGILE) is not on
// a curve: its dot is hidden until the next clean rep. The replay ends on
// the state of today: the stale nodes have their names, the header gives
// the counts, and the faint lines are the curves of today.
//
// The clock is that of kg_movie: one tick for each day from the day
// before the first record to the last record, the screen time of a day in
// proportion to its solves (a day without a solve gets LULL_WEIGHT of a
// solve), the same loop length and the same dissolve at the end. Change
// them together. Pure SMIL, so the chart plays in the README on GitHub.
//
// The Python renderer was deleted on 2026-09-20; this one is live since
// 2026-11-10.

use std::collections::HashSet;

use chrono::{Datelike, Duration, NaiveDate};
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::evidence::Evidence;
use kg::status::{node_status, node_track, FRAGILE};

use crate::common::*;

const W: i64 = 1200;
const H: i64 = 560;
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 44;
const SOLID_COLOR: &str = GREEN;
const STALE_COLOR: &str = GOLD;
const CURVE: &str = MUTED;
/// The clock of kg_movie: the loop, its dissolve, the weight of a day
/// without a solve.
const SECONDS: f64 = 10.0;
const END_FADE_S: f64 = 1.2;
const FADE_FRACTION: f64 = 0.08;
const LULL_WEIGHT: f64 = 0.25;
/// The smallest step between two key times, and their precision.
const KEY_STEP: f64 = 1e-5;
/// The largest number of points of one slide between two reps.
const SLIDE_SAMPLES: i64 = 6;
/// The number of points of one static curve.
const SAMPLES: usize = 40;
/// The height of one label, for the labels that would overlap.
const LABEL_H: f64 = 12.0;
/// The width of one label character at font size 11.
const CHAR_W: f64 = 6.2;
/// The x axis ticks: (gap in days, label).
const TICKS: [(f64, &str); 10] = [
    (1.0, "1d"),
    (3.0, "3d"),
    (7.0, "1w"),
    (14.0, "2w"),
    (30.0, "1m"),
    (60.0, "2m"),
    (120.0, "4m"),
    (240.0, "8m"),
    (480.0, "16m"),
    (960.0, "32m"),
];
const MONTHS: [&str; 12] = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/// The replay clock. Day 0 is the day before the first record.
#[derive(Clone, Debug, PartialEq)]
pub struct Clock {
    pub first: NaiveDate,
    /// The start of each day, as a fraction of the loop.
    pub fracs: Vec<f64>,
    /// The fraction of the loop where the dissolve starts.
    pub fade_from: f64,
}

impl Clock {
    /// `solves` is the number of solves of each day, from day 0.
    pub fn new(first: NaiveDate, solves: &[f64]) -> Clock {
        let fade_s = END_FADE_S.min(SECONDS * FADE_FRACTION);
        let ticks_s = SECONDS - fade_s;
        let total: f64 = solves.iter().map(|s| s + LULL_WEIGHT).sum();
        let mut cum = 0.0;
        let mut fracs = Vec::with_capacity(solves.len());
        for s in solves {
            fracs.push(cum / total * ticks_s / SECONDS);
            cum += s + LULL_WEIGHT;
        }
        Clock {
            first,
            fracs,
            fade_from: ticks_s / SECONDS,
        }
    }

    /// The fraction of the loop at the start of day `day`; the days after
    /// the last tick are at the start of the dissolve.
    pub fn frac(&self, day: i64) -> f64 {
        self.fracs
            .get(day.max(0) as usize)
            .copied()
            .unwrap_or(self.fade_from)
    }

    fn day_of(&self, d: NaiveDate) -> i64 {
        (d - self.first).num_days()
    }
}

/// A part of the history of one node, from day `start` to day `end`: on a
/// curve (the day of the last clean rep, the stability in days) or not on
/// a curve.
#[derive(Clone, Debug, PartialEq)]
pub struct Seg {
    pub start: i64,
    pub end: i64,
    pub on: Option<(i64, f64)>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Track {
    pub node: String,
    pub segs: Vec<Seg>,
}

/// The state of a node at the end of the replay: (gap, stability).
fn last_on(t: &Track) -> Option<(f64, f64)> {
    let s = t.segs.last()?;
    let (clean, stability) = s.on?;
    Some(((s.end - clean) as f64, stability))
}

fn memory(gap: f64, stability: f64, beta: f64) -> f64 {
    (1.0 + gap / stability).powf(-beta)
}

/// The days of a slide from `start` to `end`, after `start`: at most
/// SLIDE_SAMPLES days, closer together at the start, where a dot on a log
/// axis moves the most. The last one is `end`.
pub fn slide_days(start: i64, end: i64) -> Vec<i64> {
    let len = end - start;
    if len <= 0 {
        return Vec::new();
    }
    let n = len.min(SLIDE_SAMPLES);
    let mut out: Vec<i64> = (1..=n)
        .map(|j| start + (len as f64).powf(j as f64 / n as f64).round() as i64)
        .collect();
    out.dedup();
    out
}

/// Add a key time: after the previous one by KEY_STEP at least, and not
/// after 1. A browser refuses an animation whose key times do not increase.
fn push_key(times: &mut Vec<f64>, t: f64) {
    let t = (t / KEY_STEP).round() * KEY_STEP;
    let t = match times.last() {
        Some(&p) if t < p + KEY_STEP => p + KEY_STEP,
        _ => t,
    };
    times.push(t.min(1.0));
}

fn fmt_frac(t: f64) -> String {
    let s = format!("{t:.5}");
    let s = s.trim_end_matches('0').trim_end_matches('.');
    if s.is_empty() {
        "0".to_string()
    } else {
        s.to_string()
    }
}

fn animate(attr: &str, values: &[String], times: &[f64]) -> String {
    let kt: Vec<String> = times.iter().map(|t| fmt_frac(*t)).collect();
    format!(
        "<animate attributeName=\"{attr}\" calcMode=\"discrete\" values=\"{}\" keyTimes=\"{}\" dur=\"{SECONDS}s\" repeatCount=\"indefinite\"/>",
        values.join(";"),
        kt.join(";")
    )
}

/// A discrete animation from (time, value) changes: a value that repeats
/// the one before it is dropped, and the first key is at 0.
fn discrete(attr: &str, start: &str, changes: &[(f64, String)]) -> String {
    let mut times = vec![0.0];
    let mut values = vec![start.to_string()];
    for (t, v) in changes {
        if values.last() == Some(v) {
            continue;
        }
        if *t <= 0.0 {
            *values.last_mut().unwrap() = v.clone();
            continue;
        }
        push_key(&mut times, *t);
        values.push(v.clone());
    }
    animate(attr, &values, &times)
}

/// (the tracks of the nodes that were on a curve, the number of fragile
/// nodes today, the clock, beta, the target retention); None without a
/// fitted curve or a record.
fn load(ctx: &Ctx, ev: &Evidence) -> Option<(Vec<Track>, usize, Clock, f64, f64)> {
    let cv = ctx.curve.as_ref()?;
    let today = ctx.today();
    let mut dates: Vec<&String> = ev.by_date.keys().collect();
    dates.sort();
    let first = parse_date(dates.first()?) - Duration::days(1);
    let last = parse_date(dates.last()?);
    // The solves of a day, as kg_movie counts them: the distinct problems
    // and drills.
    let mut solves = Vec::new();
    let mut d = first;
    while d <= last {
        let ids: HashSet<&str> = ev
            .date_recs(&d.to_string())
            .iter()
            .filter_map(|i| {
                let rec = ev.rec(*i);
                rec.problem
                    .as_deref()
                    .filter(|p| p.chars().next().is_some_and(|c| c.is_ascii_digit()))
                    .or(rec.drill.as_deref())
            })
            .collect();
        solves.push(ids.len() as f64);
        d += Duration::days(1);
    }
    let clock = Clock::new(first, &solves);
    let end = clock.day_of(today.max(last));
    let mut nodes: Vec<&String> = ctx.nodes.keys().collect();
    nodes.sort();
    let mut tracks = Vec::new();
    let mut fragile = 0;
    for n in nodes {
        if node_status(ctx, n, ev, today).0 == FRAGILE {
            fragile += 1;
        }
        let items = node_track(ctx, n, ev);
        let segs: Vec<Seg> = items
            .iter()
            .enumerate()
            .map(|(i, (day, on))| Seg {
                start: clock.day_of(*day),
                end: items.get(i + 1).map_or(end, |next| clock.day_of(next.0)),
                on: on.map(|(clean, s)| (clock.day_of(clean), s)),
            })
            .collect();
        if segs.iter().any(|s| s.on.is_some()) {
            tracks.push(Track {
                node: n.clone(),
                segs,
            });
        }
    }
    if tracks.is_empty() {
        None
    } else {
        Some((tracks, fragile, clock, cv.beta, cv.target_retention))
    }
}

/// The right end of the x axis, in days: the first tick at or after the
/// largest gap of the replay, and one month at least.
pub fn gap_max(tracks: &[Track]) -> f64 {
    let g = tracks
        .iter()
        .flat_map(|t| &t.segs)
        .filter_map(|s| s.on.map(|(clean, _)| (s.end - clean) as f64))
        .fold(30.0f64, f64::max);
    TICKS.iter().map(|t| t.0).find(|t| *t >= g).unwrap_or(g)
}

/// The lowest value of the y axis, in percent: the multiple of 5 below
/// every dot of the replay and below the target retention.
pub fn floor_pct(tracks: &[Track], beta: f64, target: f64) -> i64 {
    let lo = tracks
        .iter()
        .flat_map(|t| &t.segs)
        .filter_map(|s| {
            s.on.map(|(clean, st)| memory((s.end - clean) as f64, st, beta))
        })
        .fold(target, f64::min);
    floor_to(100.0 * lo - 1.0, 5).clamp(0, 95)
}

/// The y of each label: its own y, moved down while it overlaps a label
/// that is already there. `boxes` are (x, y, width), in the sequence of
/// placement.
pub fn spread(boxes: &[(f64, f64, f64)]) -> Vec<f64> {
    let mut placed: Vec<(f64, f64, f64)> = Vec::new();
    for &(x, y, w) in boxes {
        let mut y = y;
        loop {
            let hit = placed
                .iter()
                .find(|(px, py, pw)| x < px + pw && *px < x + w && (y - py).abs() < LABEL_H);
            match hit {
                Some((_, py, _)) => y = py + LABEL_H,
                None => break,
            }
        }
        placed.push((x, y, w));
    }
    placed.iter().map(|b| b.1).collect()
}

pub fn chart(
    tracks: &[Track],
    fragile: usize,
    clock: &Clock,
    beta: f64,
    target: f64,
) -> Vec<String> {
    let (top, bottom) = (MT, H - MB);
    let lo = floor_pct(tracks, beta, target);
    let gmax = gap_max(tracks);
    let x_of = |g: f64| ML as f64 + g.max(1.0).log10() / gmax.log10() * (W - ML - MR) as f64;
    let y_of = |v: f64| {
        bottom as f64 - (100.0 * v - lo as f64) / (100 - lo) as f64 * (bottom - top) as f64
    };
    let finals: Vec<Option<(f64, f64)>> = tracks.iter().map(last_on).collect();
    let on_curve = finals.iter().flatten().count();
    let stale = finals
        .iter()
        .flatten()
        .filter(|(g, s)| memory(*g, *s, beta) < target)
        .count();
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">the history replayed, to today: {} nodes on their forgetting curves, {} solid, {} stale - {} fragile nodes are not on a curve</text>",
            f0(W as f64 / 2.0),
            on_curve,
            on_curve - stale,
            stale,
            fragile
        ),
    ];
    let mut legend = Legend::new(ML, false, MT - 18);
    legend.dot(
        &mut svg,
        SOLID_COLOR,
        "solid: memory at or above the target",
    );
    legend.dot(&mut svg, STALE_COLOR, "stale: memory below the target");
    legend.line(&mut svg, CURVE, "the curve of a node today", false);
    legend.line(
        &mut svg,
        INK,
        &format!("the target retention, {:.0}%", 100.0 * target),
        true,
    );
    let step = if 100 - lo > 50 { 10 } else { 5 };
    let mut g = lo;
    while g <= 100 {
        let y = y_of(g as f64 / 100.0);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{GRID}\" stroke-width=\"1\"/>",
            f1(y),
            W - MR,
            f1(y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{g}%</text>",
            ML - 8,
            f1(y + 4.0)
        ));
        g += step;
    }
    for (t, label) in TICKS.iter().filter(|t| t.0 <= gmax) {
        let x = x_of(*t);
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{bottom}\" x2=\"{}\" y2=\"{}\" stroke=\"{MUTED}\" stroke-width=\"1\"/>",
            f1(x),
            f1(x),
            bottom + 5
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{label}</text>",
            f1(x),
            bottom + 19
        ));
    }
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">days since the last clean rep (log scale)</text>",
        f0(W as f64 / 2.0),
        H - 8
    ));
    // The month of the replay, top right.
    let last_day = clock.fracs.len() as i64 - 1;
    let mut m = month_start(clock.first);
    while clock.day_of(m) <= last_day {
        let next = next_month(m);
        let mut changes = vec![(clock.frac(clock.day_of(m)), "1".to_string())];
        if clock.day_of(next) <= last_day {
            changes.push((clock.frac(clock.day_of(next)), "0".to_string()));
        }
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"16\" fill=\"{INK}\" opacity=\"0\">{} {}{}</text>",
            W - MR,
            MT - 14,
            MONTHS[m.month0() as usize],
            m.year(),
            discrete("opacity", "0", &changes)
        ));
        m = next;
    }
    // One static curve for each stability of today, to the bottom of the
    // axis.
    let mut stabilities: Vec<i64> = finals
        .iter()
        .flatten()
        .map(|f| f.1.round() as i64)
        .collect();
    stabilities.sort();
    stabilities.dedup();
    for s in stabilities {
        let pts: Vec<String> = (0..=SAMPLES)
            .map(|i| 10f64.powf(i as f64 / SAMPLES as f64 * gmax.log10()))
            .map(|g| (g, memory(g, s as f64, beta)))
            .filter(|(_, m)| 100.0 * m >= lo as f64)
            .map(|(g, m)| format!("{},{}", f1(x_of(g)), f1(y_of(m))))
            .collect();
        svg.push(format!(
            "<polyline points=\"{}\" fill=\"none\" stroke=\"{CURVE}\" stroke-width=\"1\" stroke-opacity=\"0.25\"/>",
            pts.join(" ")
        ));
    }
    let yt = y_of(target);
    svg.push(format!(
        "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{INK}\" stroke-width=\"1\" stroke-dasharray=\"6 4\"/>",
        f1(yt),
        W - MR,
        f1(yt)
    ));
    // The names of the nodes that are stale today, from the top down. A
    // name goes to the left of its dot when it does not fit on the right,
    // and a name near the target line goes below the line. The name moves
    // with its dot, so its position is relative to the dot.
    let mut stales: Vec<(usize, f64, f64)> = finals
        .iter()
        .enumerate()
        .filter_map(|(i, f)| f.map(|(g, s)| (i, x_of(g), memory(g, s, beta))))
        .filter(|(_, _, m)| *m < target)
        .collect();
    stales.sort_by(|a, b| b.2.partial_cmp(&a.2).unwrap());
    let boxes: Vec<(f64, f64, f64)> = stales
        .iter()
        .map(|(i, x, m)| {
            let w = CHAR_W * tracks[*i].node.chars().count() as f64;
            let left = x + 8.0 + w > (W - MR) as f64;
            let y = y_of(*m);
            let y = if (y - yt).abs() < LABEL_H {
                yt + LABEL_H
            } else {
                y
            };
            (if left { x - 8.0 - w } else { x + 8.0 }, y, w)
        })
        .collect();
    let ys = spread(&boxes);
    let label_of = |i: usize| -> Option<String> {
        let k = stales.iter().position(|s| s.0 == i)?;
        let (_, x, m) = stales[k];
        Some(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{INK}\">{}</text>",
            f1(boxes[k].0 - x),
            f1(ys[k] - y_of(m) + 4.0),
            tracks[i].node
        ))
    };
    // The dots. Each one is a group that moves: a slide to the right on
    // the curve between two reps, and a step at a rep.
    for (i, t) in tracks.iter().enumerate() {
        let at = |gap: f64, s: f64| format!("{},{}", f1(x_of(gap)), f1(y_of(memory(gap, s, beta))));
        let mut times = vec![0.0];
        let mut places = vec![at(0.0, 1.0)];
        let mut shown: Vec<(f64, String)> = Vec::new();
        let mut fills: Vec<(f64, String)> = Vec::new();
        for seg in &t.segs {
            let from = clock.frac(seg.start);
            let Some((clean, s)) = seg.on else {
                shown.push((from, "0".to_string()));
                continue;
            };
            shown.push((from, "1".to_string()));
            push_key(&mut times, from);
            places.push(at((seg.start - clean) as f64, s));
            for d in slide_days(seg.start, seg.end) {
                push_key(&mut times, clock.frac(d));
                places.push(at((d - clean) as f64, s));
            }
            // The gap where the memory goes below the target.
            let cross = s * (target.powf(-1.0 / beta) - 1.0);
            let color = |gap: f64| {
                if gap > cross {
                    STALE_COLOR
                } else {
                    SOLID_COLOR
                }
            };
            fills.push((from, color((seg.start - clean) as f64).to_string()));
            let day = clean + cross.floor() as i64 + 1;
            if seg.start < day && day <= seg.end {
                fills.push((clock.frac(day), STALE_COLOR.to_string()));
            }
        }
        if *times.last().unwrap() < 1.0 {
            times.push(1.0);
            places.push(places.last().unwrap().clone());
        }
        let stale_now = finals[i].is_some_and(|(g, s)| memory(g, s, beta) < target);
        svg.push(format!(
            "<g opacity=\"0\"><animateTransform attributeName=\"transform\" type=\"translate\" calcMode=\"linear\" values=\"{}\" keyTimes=\"{}\" dur=\"{SECONDS}s\" repeatCount=\"indefinite\"/>{}<circle r=\"{}\" fill=\"{SOLID_COLOR}\" fill-opacity=\"{}\">{}</circle>{}</g>",
            places.join(";"),
            times.iter().map(|t| fmt_frac(*t)).collect::<Vec<_>>().join(";"),
            discrete("opacity", "0", &shown),
            if stale_now { 5 } else { 4 },
            if stale_now { "1" } else { "0.8" },
            discrete("fill", SOLID_COLOR, &fills),
            label_of(i).unwrap_or_default()
        ));
    }
    // The end of the loop dissolves into the background, as in kg_movie.
    svg.push(format!(
        "<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\"><animate attributeName=\"opacity\" calcMode=\"linear\" values=\"0;0;1\" keyTimes=\"0;{};1\" dur=\"{SECONDS}s\" repeatCount=\"indefinite\"/></rect>",
        fmt_frac(clock.fade_from)
    ));
    svg.push("</svg>".to_string());
    svg
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("positions.svg");
    let Some((tracks, fragile, clock, beta, target)) = load(ctx, ev) else {
        println!("no chart: no node is on a fitted curve (graph/curve.json is missing)");
        return;
    };
    let svg = chart(&tracks, fragile, &clock, beta, target);
    write(&out, &svg);
    let finals: Vec<(f64, f64)> = tracks.iter().filter_map(last_on).collect();
    println!(
        "wrote {} ({} nodes on a curve today, {} stale, {} fragile and not on a curve; {} days replayed in the {}s loop, {:.0}KB)",
        out.display(),
        finals.len(),
        finals
            .iter()
            .filter(|(g, s)| memory(*g, *s, beta) < target)
            .count(),
        fragile,
        clock.fracs.len(),
        SECONDS,
        svg.iter().map(|l| l.len() + 1).sum::<usize>() as f64 / 1024.0
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    const BETA: f64 = 0.1143;

    fn day(s: &str) -> NaiveDate {
        NaiveDate::parse_from_str(s, "%Y-%m-%d").unwrap()
    }

    /// 301 days, one solve on each day after day 0.
    fn clock() -> Clock {
        let mut solves = vec![1.0; 301];
        solves[0] = 0.0;
        Clock::new(day("2026-01-31"), &solves)
    }

    fn track(node: &str, segs: &[(i64, i64, Option<(i64, f64)>)]) -> Track {
        Track {
            node: node.to_string(),
            segs: segs
                .iter()
                .map(|&(start, end, on)| Seg { start, end, on })
                .collect(),
        }
    }

    #[test]
    fn the_clock_gives_a_day_without_a_solve_a_quarter_of_a_solve() {
        let c = Clock::new(day("2026-01-31"), &[0.0, 1.0, 0.0, 3.0]);
        // The weights are 0.25, 1.25, 0.25 and 3.25: 5 in total, over
        // the 9.2 seconds before the dissolve of 0.8 seconds.
        assert!((c.fade_from - 0.92).abs() < 1e-9);
        assert!((c.frac(0) - 0.0).abs() < 1e-9);
        assert!((c.frac(1) - 0.25 / 5.0 * 0.92).abs() < 1e-9);
        assert!((c.frac(3) - 1.75 / 5.0 * 0.92).abs() < 1e-9);
        assert!((c.frac(4) - 0.92).abs() < 1e-9);
    }

    #[test]
    fn a_slide_has_few_days_and_ends_on_the_last_day() {
        assert_eq!(slide_days(10, 10), Vec::<i64>::new());
        assert_eq!(slide_days(10, 12), vec![11, 12]);
        assert_eq!(slide_days(0, 64), vec![2, 4, 8, 16, 32, 64]);
    }

    #[test]
    fn key_times_increase_by_one_step_at_least() {
        let mut t = vec![0.0];
        push_key(&mut t, 0.5);
        push_key(&mut t, 0.5);
        push_key(&mut t, 0.2);
        assert!((t[2] - 0.50001).abs() < 1e-9);
        assert!((t[3] - 0.50002).abs() < 1e-9);
        assert_eq!(fmt_frac(t[3]), "0.50002");
        assert_eq!(fmt_frac(0.5), "0.5");
        assert_eq!(fmt_frac(0.0), "0");
    }

    #[test]
    fn the_axes_hold_every_dot_of_the_replay() {
        // The node was 250 days without a rep in the past, and it is at
        // a gap of 20 days today.
        let ts = [track(
            "two-pointers",
            &[(10, 260, Some((10, 60.0))), (260, 280, Some((260, 70.0)))],
        )];
        assert_eq!(gap_max(&ts), 480.0);
        assert_eq!(floor_pct(&ts, BETA, 0.9), 80);
        let short = [track("two-pointers", &[(10, 13, Some((10, 60.0)))])];
        assert_eq!(gap_max(&short), 30.0);
        assert_eq!(floor_pct(&short, BETA, 0.9), 85);
    }

    #[test]
    fn a_label_moves_down_only_when_it_overlaps_another() {
        let ys = spread(&[
            (100.0, 50.0, 60.0),
            (120.0, 55.0, 60.0),
            (300.0, 55.0, 60.0),
            (130.0, 58.0, 60.0),
        ]);
        assert_eq!(ys, vec![50.0, 62.0, 55.0, 74.0]);
    }

    #[test]
    fn the_chart_has_one_moving_dot_for_each_node_and_a_name_for_each_stale_node() {
        let ts = [
            track(
                "two-pointers",
                &[(1, 297, Some((1, 60.0))), (297, 300, Some((297, 70.0)))],
            ),
            // A fail on day 50 takes the node off its curve until day 80.
            track(
                "union-find",
                &[
                    (5, 50, Some((5, 60.0))),
                    (50, 80, None),
                    (80, 300, Some((80, 2000.0))),
                ],
            ),
            track("trie-insert", &[(100, 300, Some((100, 60.0)))]),
        ];
        let s = chart(&ts, 4, &clock(), BETA, 0.9).join("\n");
        assert_eq!(s.matches("<animateTransform").count(), 3);
        assert_eq!(s.matches("<circle").count(), 3 + 2);
        // The curves of today: stability 60, 70 and 2000.
        assert_eq!(s.matches("<polyline").count(), 3);
        assert!(s.contains(
            ">the history replayed, to today: 3 nodes on their forgetting curves, 2 solid, 1 stale - 4 fragile nodes are not on a curve<"
        ));
        assert!(s.contains(">trie-insert</text>"));
        assert!(!s.contains(">union-find</text>"));
        assert!(s.contains(">Jan 2026<"));
        assert!(s.contains(">Nov 2026<"));
        assert!(!s.contains(">Dec 2026<"));
        // two-pointers goes below the target on its long slide and is
        // green again after the rep on day 297.
        let dots: Vec<&str> = s
            .lines()
            .filter(|l| l.contains("animateTransform"))
            .collect();
        assert!(dots[0].contains(&format!("values=\"{GREEN};{GOLD};{GREEN}\"")));
        // union-find is hidden from day 50 to day 80.
        assert!(
            dots[1].contains("attributeName=\"opacity\" calcMode=\"discrete\" values=\"0;1;0;1\"")
        );
    }

    #[test]
    fn every_animation_has_key_times_that_increase_from_0() {
        let ts = [
            track(
                "two-pointers",
                &[
                    (1, 2, Some((1, 60.0))),
                    (2, 3, Some((2, 61.0))),
                    (3, 300, Some((3, 62.0))),
                ],
            ),
            track("trie-insert", &[(100, 300, Some((100, 60.0)))]),
        ];
        let s = chart(&ts, 0, &clock(), BETA, 0.9).join("\n");
        let mut n = 0;
        for part in s.split("keyTimes=\"").skip(1) {
            let kt: Vec<f64> = part
                .split('"')
                .next()
                .unwrap()
                .split(';')
                .map(|t| t.parse().unwrap())
                .collect();
            assert_eq!(kt[0], 0.0);
            assert!(kt.windows(2).all(|w| w[0] < w[1]), "{kt:?}");
            assert!(*kt.last().unwrap() <= 1.0);
            n += 1;
        }
        assert!(n > 6);
        // A linear animation ends at 1 exactly.
        for part in s.split("calcMode=\"linear\"").skip(1) {
            let kt = part
                .split("keyTimes=\"")
                .nth(1)
                .unwrap()
                .split('"')
                .next()
                .unwrap();
            assert!(kt.ends_with(";1"), "{kt}");
        }
    }
}
