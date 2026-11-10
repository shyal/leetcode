// Does each group agree with the one global forgetting curve? Rendered
// into graph/residuals.svg.
//
// The curve in graph/curve.json gives P(recall) for every recall trial.
// For each group (the group field in nodes.json) the chart shows
// z = sum(observed - predicted) / sqrt(sum p(1-p)) over the trials of the
// group up to each date: the distance between the observed recall of the
// group and the prediction of the curve, in standard deviations. A group
// below -2 forgets faster than the curve says. A group above +2 recalls
// better than the curve says. The white line is every trial together: the
// bias of the curve. The series come from kg_residuals --series-json,
// which make residuals prints as a table.
//
// The Python renderer (an animation) was retired on 2026-09-12; this one
// draws the full history as a still and is live since 2026-11-10.

use std::process::Command;

use chrono::NaiveDate;
use kg::ctx::Ctx;
use kg::data::parse_date;
use serde_json::Value;

use crate::common::*;

const W: i64 = 1200;
const H: i64 = 470;
const ML: i64 = 48;
/// The right margin holds the group labels.
const MR: i64 = 190;
const MT: i64 = 60;
const MB: i64 = 40;
/// A group at or past this |z| is outside the band (the flag of make
/// residuals).
const Z_FLAG: f64 = 2.0;
/// The lowest half-height of the y axis.
const Z_MIN: i64 = 3;
/// The y axis has a grid line for each z up to this half-height, then for
/// each second z.
const Z_DENSE: i64 = 6;
/// The lowest distance between two labels, in pixels.
const LABEL_GAP: f64 = 14.0;
const POOLED: &str = "#f0f6fc";
const QUIET: &str = "#484f58";
/// The colours of the groups outside the band, in the sequence of their z.
/// Red is the band, white is the pooled line.
const PALETTE: [&str; 8] = [
    "#ffa657", "#a371f7", BLUE, "#39c5cf", GREEN, "#f778ba", GOLD, "#d2a8ff",
];

/// One group: its name, its trial count, its last z and (date, running z).
#[derive(Clone, Debug, PartialEq)]
pub struct Series {
    pub group: String,
    pub n: i64,
    pub z: f64,
    pub points: Vec<(NaiveDate, f64)>,
}

fn series(v: &Value) -> Option<Series> {
    let points: Vec<(NaiveDate, f64)> = v["points"]
        .as_array()?
        .iter()
        .filter_map(|p| Some((parse_date(p[0].as_str()?), p[1].as_f64()?)))
        .collect();
    if points.is_empty() {
        return None;
    }
    Some(Series {
        group: v["group"].as_str()?.to_string(),
        n: v["n"].as_i64()?,
        z: v["z"].as_f64()?,
        points,
    })
}

/// (the groups, every trial pooled) from kg_residuals; None without the
/// binary, the curve file or a trial.
fn load(ctx: &Ctx) -> Option<(Vec<Series>, Series)> {
    let bin = ctx.root.join("utils/rs/target/release/kg_residuals");
    let o = Command::new(bin)
        .arg("--series-json")
        .current_dir(&ctx.root)
        .output()
        .ok()
        .filter(|o| o.status.success())?;
    let v: Value = serde_json::from_slice(&o.stdout).ok()?;
    let groups: Vec<Series> = v["groups"].as_array()?.iter().filter_map(series).collect();
    Some((groups, series(&v["pooled"])?))
}

pub fn is_outside(s: &Series) -> bool {
    s.z.abs() >= Z_FLAG
}

/// The half-height of the y axis: it holds every point, and it is even
/// when the grid shows each second z.
pub fn z_limit(all: &[&Series]) -> i64 {
    let top = all
        .iter()
        .flat_map(|s| s.points.iter().map(|p| p.1.abs()))
        .fold(0.0f64, f64::max);
    let lim = (top.ceil() as i64).max(Z_MIN);
    if lim > Z_DENSE {
        lim + lim % 2
    } else {
        lim
    }
}

/// The y of each label, in the given sequence, moved apart until no two
/// are nearer than LABEL_GAP and none is outside top..=bottom.
pub fn spread(ys: &[f64], top: f64, bottom: f64) -> Vec<f64> {
    let mut order: Vec<usize> = (0..ys.len()).collect();
    order.sort_by(|a, b| ys[*a].partial_cmp(&ys[*b]).unwrap());
    let mut out = ys.to_vec();
    let mut prev = f64::NEG_INFINITY;
    for &i in &order {
        out[i] = out[i].max(top).max(prev + LABEL_GAP);
        prev = out[i];
    }
    let mut next = f64::INFINITY;
    for &i in order.iter().rev() {
        out[i] = out[i].min(bottom).min(next - LABEL_GAP);
        next = out[i];
    }
    out
}

/// A step line: each z stays until the next date with a trial, and the
/// last z goes on to `end`.
fn step_points<F: Fn(NaiveDate) -> f64, G: Fn(f64) -> f64>(
    s: &Series,
    end: NaiveDate,
    x_of: F,
    y_of: G,
) -> String {
    let mut out: Vec<String> = Vec::new();
    let mut prev: Option<f64> = None;
    for (d, z) in &s.points {
        let (x, y) = (x_of(*d), y_of(*z));
        if let Some(p) = prev {
            out.push(format!("{},{}", f1(x), f1(p)));
        }
        out.push(format!("{},{}", f1(x), f1(y)));
        prev = Some(y);
    }
    if let (Some(p), Some(last)) = (prev, s.points.last()) {
        if last.0 < end {
            out.push(format!("{},{}", f1(x_of(end)), f1(p)));
        }
    }
    out.join(" ")
}

pub fn chart(today: NaiveDate, groups: &[Series], pooled: &Series) -> Vec<String> {
    let (top, bottom, right) = (MT, H - MB, W - MR);
    let mut all: Vec<&Series> = groups.iter().collect();
    all.push(pooled);
    let d0 = all.iter().map(|s| s.points[0].0).min().unwrap();
    let d1 = today.max(
        all.iter()
            .map(|s| s.points.last().unwrap().0)
            .max()
            .unwrap(),
    );
    let span = days_between(d0, d1).max(1) as f64;
    let x_of = |d: NaiveDate| ML as f64 + days_between(d0, d) as f64 / span * (right - ML) as f64;
    let lim = z_limit(&all);
    let y_of = |z: f64| bottom as f64 - (z + lim as f64) / (2 * lim) as f64 * (bottom - top) as f64;

    // the groups outside the band, from the lowest z, each with a colour
    let mut flagged: Vec<&Series> = groups.iter().filter(|s| is_outside(s)).collect();
    flagged.sort_by(|a, b| a.z.partial_cmp(&b.z).unwrap());
    let color_of = |s: &Series| {
        flagged
            .iter()
            .position(|f| f.group == s.group)
            .map(|i| PALETTE[i % PALETTE.len()])
            .unwrap_or(QUIET)
    };

    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} recall trials - {} of {} groups are outside the band of z = ±{}</text>",
            f0(W as f64 / 2.0),
            pooled.n,
            flagged.len(),
            groups.len(),
            f0(Z_FLAG)
        ),
    ];
    let mut legend = Legend::new(ML, false, MT - 18);
    legend.line(&mut svg, POOLED, "all groups together", false);
    legend.line(
        &mut svg,
        PALETTE[0],
        "a group outside the band, with its name at the right",
        false,
    );
    legend.line(&mut svg, QUIET, "a group inside the band", false);
    legend.line(
        &mut svg,
        RED,
        &format!("the band, z = ±{}", f0(Z_FLAG)),
        true,
    );

    let months = days_between(d0, d1) / 30;
    let step = if months > 24 {
        3
    } else if months > 12 {
        2
    } else {
        1
    };
    month_ticks(&mut svg, d0, d1, x_of, top, bottom, step);
    let grid = if lim > Z_DENSE { 2 } else { 1 };
    let mut z = -lim;
    while z <= lim {
        let y = y_of(z as f64);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{right}\" y2=\"{}\" stroke=\"{GRID}\" stroke-width=\"{}\"/>",
            f1(y),
            f1(y),
            if z == 0 { 2 } else { 1 }
        ));
        let label = if z == 0 {
            "0".to_string()
        } else {
            format!("{z:+}")
        };
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{label}</text>",
            ML - 8,
            f1(y + 4.0)
        ));
        z += grid;
    }
    for sign in [1.0, -1.0] {
        let y = y_of(sign * Z_FLAG);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{right}\" y2=\"{}\" stroke=\"{RED}\" stroke-width=\"1\" stroke-dasharray=\"6 4\" opacity=\"0.7\"/>",
            f1(y),
            f1(y)
        ));
    }

    // the groups inside the band first, so that the others are on top
    let mut drawn: Vec<&Series> = groups.iter().filter(|s| !is_outside(s)).collect();
    drawn.extend(flagged.iter().copied());
    for s in &drawn {
        svg.push(format!(
            "<polyline points=\"{}\" fill=\"none\" stroke=\"{}\" stroke-width=\"{}\" stroke-linejoin=\"round\"/>",
            step_points(s, d1, x_of, y_of),
            color_of(s),
            if is_outside(s) { "1.5" } else { "1" }
        ));
    }
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{POOLED}\" stroke-width=\"2\" stroke-linejoin=\"round\"/>",
        step_points(pooled, d1, x_of, y_of)
    ));

    // the meaning of each side of the band, on top of the lines
    for (sign, text) in [
        (1.0, "recall is better than the curve predicts"),
        (-1.0, "recall is worse than the curve predicts"),
    ] {
        let y = y_of(sign * Z_FLAG);
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"10\" fill=\"{RED}\" stroke=\"{BG}\" stroke-width=\"3\" paint-order=\"stroke\" stroke-linejoin=\"round\">z = {}: {text}</text>",
            ML + 4,
            f1(if sign > 0.0 { y - 5.0 } else { y + 13.0 }),
            s0(sign * Z_FLAG)
        ));
    }

    // the labels at the right: the groups outside the band and the pooled line
    let mut labelled: Vec<(&Series, &str, String)> = flagged
        .iter()
        .map(|s| (*s, color_of(s), s.group.clone()))
        .collect();
    labelled.push((pooled, POOLED, "all groups".to_string()));
    let ends: Vec<f64> = labelled.iter().map(|(s, _, _)| y_of(s.z)).collect();
    let ys = spread(&ends, top as f64 + 4.0, bottom as f64);
    for (((s, color, name), end), y) in labelled.iter().zip(&ends).zip(&ys) {
        svg.push(format!(
            "<line x1=\"{right}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{color}\" stroke-width=\"1\" opacity=\"0.6\"/>",
            f1(*end),
            right + 8,
            f1(*y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{color}\">{name} {:+.1} ({} trials)</text>",
            right + 12,
            f1(y + 4.0),
            s.z,
            s.n
        ));
    }
    svg.push("</svg>".to_string());
    svg
}

pub fn render(ctx: &Ctx) {
    let out = ctx.graph_dir().join("residuals.svg");
    let Some((groups, pooled)) = load(ctx) else {
        println!(
            "no chart: no series from kg_residuals (graph/curve.json or the binary is missing)"
        );
        return;
    };
    write(&out, &chart(ctx.today(), &groups, &pooled));
    println!(
        "wrote {} ({} groups, {} outside the band)",
        out.display(),
        groups.len(),
        groups.iter().filter(|s| is_outside(s)).count()
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    fn d(s: &str) -> NaiveDate {
        parse_date(s)
    }

    fn s(group: &str, pts: &[(&str, f64)]) -> Series {
        Series {
            group: group.to_string(),
            n: pts.len() as i64,
            z: pts.last().unwrap().1,
            points: pts.iter().map(|(day, z)| (d(day), *z)).collect(),
        }
    }

    #[test]
    fn the_axis_holds_every_point_and_is_even_past_the_dense_grid() {
        let a = s("a", &[("2026-06-01", 0.4), ("2026-06-02", -1.2)]);
        assert_eq!(z_limit(&[&a]), 3);
        let b = s("b", &[("2026-06-01", 4.2)]);
        assert_eq!(z_limit(&[&a, &b]), 5);
        let c = s("c", &[("2026-06-01", -6.3)]);
        assert_eq!(z_limit(&[&a, &c]), 8);
    }

    #[test]
    fn a_group_is_outside_at_two_standard_deviations() {
        assert!(is_outside(&s("a", &[("2026-06-01", -2.0)])));
        assert!(is_outside(&s("a", &[("2026-06-01", 2.4)])));
        assert!(!is_outside(&s("a", &[("2026-06-01", 1.99)])));
    }

    #[test]
    fn spread_moves_near_labels_apart_and_keeps_the_sequence() {
        let ys = spread(&[100.0, 103.0, 200.0], 0.0, 400.0);
        assert_eq!(ys, vec![100.0, 114.0, 200.0]);
        // the second label was the higher one: it stays the higher one
        let ys = spread(&[103.0, 100.0], 0.0, 400.0);
        assert_eq!(ys, vec![114.0, 100.0]);
    }

    #[test]
    fn spread_keeps_the_labels_inside_the_plot() {
        let ys = spread(&[395.0, 398.0, 399.0], 0.0, 400.0);
        assert_eq!(ys, vec![372.0, 386.0, 400.0]);
        assert_eq!(spread(&[-20.0], 0.0, 400.0), vec![0.0]);
    }

    #[test]
    fn the_chart_labels_the_groups_outside_the_band_and_the_pooled_line() {
        let groups = [
            s("graphs", &[("2026-06-01", -1.0), ("2026-07-01", -2.5)]),
            s("trees", &[("2026-06-10", 0.5)]),
        ];
        let pooled = s("", &[("2026-06-01", -1.0), ("2026-07-01", -1.4)]);
        let svg = chart(d("2026-08-01"), &groups, &pooled).join("\n");
        assert_eq!(svg.matches("<polyline").count(), 3);
        assert!(svg.contains(">2 recall trials - 1 of 2 groups are outside the band of z = ±2<"));
        assert!(svg.contains(">graphs -2.5 (2 trials)<"));
        assert!(svg.contains(">all groups -1.4 (2 trials)<"));
        assert!(!svg.contains(">trees "));
    }

    #[test]
    fn a_line_goes_on_to_the_day_of_the_run() {
        let a = s("a", &[("2026-06-01", 1.0), ("2026-06-11", 2.0)]);
        let pts = step_points(
            &a,
            d("2026-06-21"),
            |day| days_between(d("2026-06-01"), day) as f64,
            |z| z,
        );
        assert_eq!(pts, "0.0,1.0 10.0,1.0 10.0,2.0 20.0,2.0");
    }
}
