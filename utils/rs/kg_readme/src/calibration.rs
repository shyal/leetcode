// Does the forgetting curve agree with the recall results? Rendered into
// graph/calibration.svg.
//
// The curve in graph/curve.json gives P(recall) for every recall trial.
// The trials are grouped by the gap since the last rep of the node. For
// each group the chart shows the mean prediction of the model, a band of
// ±2 standard errors of the observed rate under the model
// (sqrt(sum p(1-p)) / n), and the observed unaided-recall rate. A point
// outside its band is a gap where the curve is wrong. The groups come from
// kg_curve --calibration-json, which uses the trials the curve was fitted
// on.
//
// The Python renderer (a daily replay) was deleted on 2026-09-20; this one
// draws the current state and is live since 2026-11-10.

use std::process::Command;

use kg::ctx::Ctx;
use serde_json::Value;

use crate::common::*;

const W: i64 = 1200;
const H: i64 = 400;
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 56;
const MODEL: &str = BLUE;
const INSIDE: &str = INK;
/// Half the width of a band, in pixels.
const HALF: f64 = 60.0;
/// The band is this many standard errors each side of the model.
const SIGMAS: f64 = 2.0;

/// One gap group: gaps lo..=hi days, the model's mean prediction, the
/// observed rate, its standard error under the model, the trial count.
#[derive(Clone, Debug, PartialEq)]
pub struct Bucket {
    pub lo: i64,
    pub hi: i64,
    pub model: f64,
    pub observed: f64,
    pub se: f64,
    pub n: f64,
}

/// (the era boundary of the fit, the buckets) from the Rust fitter; None
/// without the binary, the curve file or a trial.
fn load(ctx: &Ctx) -> Option<(Option<String>, Vec<Bucket>)> {
    let bin = ctx.root.join("utils/rs/target/release/kg_curve");
    let o = Command::new(bin)
        .arg("--calibration-json")
        .current_dir(&ctx.root)
        .output()
        .ok()
        .filter(|o| o.status.success())?;
    let v: Value = serde_json::from_slice(&o.stdout).ok()?;
    let since = v["since"].as_str().map(str::to_string);
    let buckets: Vec<Bucket> = v["buckets"]
        .as_array()?
        .iter()
        .filter_map(|b| {
            Some(Bucket {
                lo: b["lo"].as_i64()?,
                hi: b["hi"].as_i64()?,
                model: b["model"].as_f64()?,
                observed: b["observed"].as_f64()?,
                se: b["se"].as_f64()?,
                n: b["n"].as_f64()?,
            })
        })
        .collect();
    if buckets.is_empty() {
        None
    } else {
        Some((since, buckets))
    }
}

/// The number of buckets whose observed rate is outside the band.
pub fn outside(buckets: &[Bucket]) -> usize {
    buckets
        .iter()
        .filter(|b| (b.observed - b.model).abs() > SIGMAS * b.se)
        .count()
}

/// The colour of an observed point: green above its band, red below it.
fn color_of(b: &Bucket) -> &'static str {
    let d = b.observed - b.model;
    if d > SIGMAS * b.se {
        GREEN
    } else if d < -SIGMAS * b.se {
        RED
    } else {
        INSIDE
    }
}

fn pct(x: f64) -> String {
    format!("{:.0}%", 100.0 * x)
}

/// The lowest value of the y axis, in percent: the multiple of 5 below
/// every band and every observed point.
pub fn floor_pct(buckets: &[Bucket]) -> i64 {
    let lo = buckets
        .iter()
        .map(|b| (b.model - SIGMAS * b.se).min(b.observed))
        .fold(1.0f64, f64::min);
    (floor_to(100.0 * lo - 1.0, 5)).clamp(0, 95)
}

pub fn chart(since: Option<&str>, buckets: &[Bucket]) -> Vec<String> {
    let (top, bottom) = (MT, H - MB);
    let lo = floor_pct(buckets);
    let y_of = |v: f64| {
        bottom as f64 - (100.0 * v - lo as f64) / (100 - lo) as f64 * (bottom - top) as f64
    };
    let slot = (W - ML - MR) as f64 / buckets.len() as f64;
    let x_of = |i: usize| ML as f64 + slot * (i as f64 + 0.5);
    let trials: f64 = buckets.iter().map(|b| b.n).sum();
    let era = since.map(|s| format!(" since {s}")).unwrap_or_default();
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} recall trials{era} - observed recall is outside the band in {} of {} gap groups</text>",
            f0(W as f64 / 2.0),
            f0(trials),
            outside(buckets),
            buckets.len()
        ),
    ];
    let mut legend = Legend::new(ML, false, MT - 18);
    legend.swatch(&mut svg, MODEL, "1", "the model: mean predicted recall");
    legend.swatch(
        &mut svg,
        MODEL,
        "0.15",
        "±2 standard errors under the model",
    );
    legend.swatch(&mut svg, INSIDE, "1", "observed recall, inside the band");
    legend.swatch(&mut svg, GREEN, "1", "observed above the band");
    legend.swatch(&mut svg, RED, "1", "observed below the band");
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
    for (i, b) in buckets.iter().enumerate() {
        let x = x_of(i);
        let up = y_of((b.model + SIGMAS * b.se).min(1.0));
        let down = y_of(b.model - SIGMAS * b.se);
        let ym = y_of(b.model);
        let yo = y_of(b.observed);
        svg.push(format!(
            "<rect x=\"{}\" y=\"{}\" width=\"{}\" height=\"{}\" fill=\"{MODEL}\" fill-opacity=\"0.15\"/>",
            f1(x - HALF),
            f1(up),
            f1(2.0 * HALF),
            f1(down - up)
        ));
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{MODEL}\" stroke-width=\"2\"/>",
            f1(x - HALF),
            f1(ym),
            f1(x + HALF),
            f1(ym)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MODEL}\">{}</text>",
            f1(x - HALF - 6.0),
            f1(ym + 4.0),
            pct(b.model)
        ));
        let color = color_of(b);
        svg.push(format!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"5\" fill=\"{color}\"/>",
            f1(x),
            f1(yo)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{color}\">{}</text>",
            f1(x + HALF + 6.0),
            f1(yo + 4.0),
            pct(b.observed)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{INK}\">gap {} to {} days</text>",
            f1(x),
            bottom + 20,
            b.lo,
            b.hi
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} trials</text>",
            f1(x),
            bottom + 35,
            f0(b.n)
        ));
    }
    svg.push("</svg>".to_string());
    svg
}

pub fn render(ctx: &Ctx) {
    let out = ctx.graph_dir().join("calibration.svg");
    let Some((since, buckets)) = load(ctx) else {
        println!(
            "no chart: no calibration from kg_curve (graph/curve.json or the binary is missing)"
        );
        return;
    };
    write(&out, &chart(since.as_deref(), &buckets));
    println!(
        "wrote {} ({} gap groups, {} outside the band)",
        out.display(),
        buckets.len(),
        outside(&buckets)
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    fn b(lo: i64, hi: i64, model: f64, observed: f64, se: f64, n: f64) -> Bucket {
        Bucket {
            lo,
            hi,
            model,
            observed,
            se,
            n,
        }
    }

    #[test]
    fn outside_counts_the_points_beyond_two_standard_errors() {
        let bs = [
            b(1, 7, 0.9, 0.95, 0.01, 10.0),
            b(8, 21, 0.9, 0.85, 0.01, 10.0),
            b(22, 42, 0.9, 0.91, 0.01, 10.0),
        ];
        assert_eq!(outside(&bs), 2);
    }

    #[test]
    fn the_axis_starts_below_every_band_and_point() {
        let bs = [
            b(1, 7, 0.94, 0.95, 0.01, 100.0),
            b(8, 21, 0.8, 0.71, 0.03, 50.0),
        ];
        assert_eq!(floor_pct(&bs), 70);
        assert_eq!(floor_pct(&[b(1, 7, 0.94, 0.95, 0.01, 100.0)]), 90);
    }

    #[test]
    fn a_point_takes_its_colour_from_its_side_of_the_band() {
        assert_eq!(color_of(&b(1, 7, 0.9, 0.95, 0.01, 10.0)), GREEN);
        assert_eq!(color_of(&b(1, 7, 0.9, 0.85, 0.01, 10.0)), RED);
        assert_eq!(color_of(&b(1, 7, 0.9, 0.91, 0.01, 10.0)), INSIDE);
    }

    #[test]
    fn the_chart_has_one_band_and_one_point_for_each_bucket() {
        let bs = [
            b(1, 7, 0.94, 0.95, 0.01, 100.0),
            b(8, 21, 0.8, 0.71, 0.03, 50.0),
        ];
        let s = chart(Some("2026-06-01"), &bs).join("\n");
        assert_eq!(s.matches("<circle").count(), 2);
        assert!(s.contains(
            ">150 recall trials since 2026-06-01 - observed recall is outside the band in 1 of 2 gap groups<"
        ));
        assert!(s.contains(">gap 8 to 21 days<"));
        assert!(s.contains(">50 trials<"));
    }
}
