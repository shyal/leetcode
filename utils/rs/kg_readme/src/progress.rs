// Is the recent play beating the fitted model? Rendered into
// graph/progress.svg.
//
// The cold-solve model (graph/curve.json "solve", fitted by kg_curve on
// the scored games) prices every first-sight game by the problem's
// rating, the walk's recall and its never-met moves. It is the null
// hypothesis of no skill growth, and the residual, actual score minus the
// model's probability, is the test of it. One point per first-sight game,
// on its date: the mean residual of the last WINDOW games. The band is
// ±2 standard errors of that mean under the model, sqrt(sum p(1-p))/n.
// Features come from kg_curve --solve-rows-json, built from evidence
// strictly older than each game.
//
// Ported from utils/readme/kg_progress_svg (Python) on 2026-09-13.

use std::process::Command;

use chrono::NaiveDate;
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::evidence::Evidence;
use kg::model::{elo_games, solve_ratings};
use serde_json::Value;

use crate::common::*;

pub const WINDOW: usize = 30;

const W: i64 = 1200;
const H: i64 = 400;
const LINE: &str = BLUE;
const BAND: &str = BLUE;
const ZERO: &str = INK;
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 40;

/// (date, actual score, model probability): one first-sight scored game.
pub type Row = (NaiveDate, f64, f64);

/// The per-game feature rows under the fitted curve, from the Rust fitter:
/// [[features, score, date]].
fn solve_rows(ctx: &Ctx) -> Vec<Value> {
    let bin = ctx.root.join("utils/rs/target/release/kg_curve");
    match Command::new(bin)
        .arg("--solve-rows-json")
        .current_dir(&ctx.root)
        .output()
    {
        Ok(o) if o.status.success() => serde_json::from_slice::<Value>(&o.stdout)
            .ok()
            .and_then(|v| v.as_array().cloned())
            .unwrap_or_default(),
        _ => Vec::new(),
    }
}

/// One per first-sight scored game, oldest first; empty without a fitted
/// model.
pub fn first_sight_rows(ctx: &Ctx, ev: &Evidence) -> Vec<Row> {
    let Some(coef) = ctx
        .curve
        .as_ref()
        .and_then(|c| c.raw.get("solve")?.get("features").cloned())
    else {
        return Vec::new();
    };
    if !kg::data::truthy(&coef) {
        return Vec::new();
    }
    let ratings = solve_ratings(ctx);
    let rows = solve_rows(ctx);
    let games = elo_games(ctx, ev, &ratings);
    let first = crate::elo::first_dates(ev);
    let c = |k: &str| coef.get(k).and_then(Value::as_f64).unwrap_or(0.0);
    let mut out = Vec::new();
    for (row, (g, _, _)) in rows.iter().zip(&games) {
        let (f, y, d) = (&row[0], row[1].as_f64().unwrap(), row[2].as_str().unwrap());
        if first.get(&g.problem).map(String::as_str) != Some(d) {
            continue;
        }
        let z = c("intercept")
            + ["rating", "recall", "unseen"]
                .iter()
                .fold(0.0, |a, k| a + c(k) * f[*k].as_f64().unwrap());
        out.push((parse_date(d), y, 1.0 / (1.0 + (-z).exp())));
    }
    out
}

/// [(date, mean residual, its standard error under the model)] one per
/// game from the n-th on: the last n games ending at that game.
pub fn windows(rows: &[Row], n: usize) -> Vec<(NaiveDate, f64, f64)> {
    let mut out = Vec::new();
    for i in (n.saturating_sub(1))..rows.len() {
        if i + 1 < n {
            continue;
        }
        let w = &rows[i + 1 - n..=i];
        let resid = w.iter().fold(0.0, |a, (_, y, p)| a + (y - p)) / n as f64;
        let se = w.iter().fold(0.0, |a, (_, _, p)| a + p * (1.0 - p)).sqrt() / n as f64;
        out.push((w[w.len() - 1].0, resid, se));
    }
    out
}

/// Python's round(x, 6).
fn round6(x: f64) -> f64 {
    format!("{:.6}", x).parse().unwrap()
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("progress.svg");
    let rows = first_sight_rows(ctx, ev);
    let win = windows(&rows, WINDOW);
    if win.is_empty() {
        println!(
            "no chart: {} first-sight games, {WINDOW} needed",
            rows.len()
        );
        return;
    }
    let (d0, d1) = (win[0].0, win[win.len() - 1].0);
    let span = days_between(d0, d1).max(1);
    let (top, bottom) = (MT, H - MB);
    let lim = win
        .iter()
        .map(|(_, r, se)| r.abs() + 2.0 * se)
        .fold(0.25f64, f64::max);
    let lim = (lim * 20.0).ceil() / 20.0;
    let x_of =
        |d: NaiveDate| ML as f64 + days_between(d0, d) as f64 / span as f64 * (W - ML - MR) as f64;
    let y_of = |v: f64| bottom as f64 - (v + lim) / (2.0 * lim) * (bottom - top) as f64;

    let (last_d, last_r, last_se) = win[win.len() - 1];
    let z = if last_se != 0.0 {
        last_r / last_se
    } else {
        0.0
    };
    let verdict = if z > 2.0 {
        "above the model"
    } else if z < -2.0 {
        "below the model"
    } else {
        "inside noise"
    };
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} first-sight games - last {WINDOW}: actual minus model {:+.2} ({:+.1} standard errors, {verdict})</text>",
            f0(W as f64 / 2.0),
            rows.len(),
            last_r,
            z
        ),
    ];
    // both swatches are LINE's colour, so both print opacity 1 (the Python
    // compared the colour, not the entry)
    let mut legend = Legend::new(ML, false, MT - 18);
    legend.swatch(
        &mut svg,
        LINE,
        "1",
        &format!("mean residual of the last {WINDOW} first sights"),
    );
    legend.swatch(
        &mut svg,
        BAND,
        if BAND == LINE { "1" } else { "0.15" },
        "±2 standard errors under the model",
    );
    let step = if lim <= 0.5 { 0.1 } else { 0.25 };
    let mut v = -lim;
    while v <= lim + 1e-9 {
        let yy = y_of(v);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{GRID}\" stroke-width=\"1\"/>",
            f1(yy),
            W - MR,
            f1(yy)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{v:+.2}</text>",
            ML - 8,
            f1(yy + 4.0)
        ));
        v = round6(v + step);
    }
    month_ticks(&mut svg, d0, d1, x_of, top, bottom, 1);
    let series: Vec<(NaiveDate, (f64, f64))> =
        win.iter().map(|(d, r, se)| (*d, (*r, *se))).collect();
    for run in runs(&series) {
        let up: Vec<String> = run
            .iter()
            .map(|(d, (r, se))| format!("{},{}", f1(x_of(*d)), f1(y_of(r + 2.0 * se))))
            .collect();
        let down: Vec<String> = run
            .iter()
            .rev()
            .map(|(d, (r, se))| format!("{},{}", f1(x_of(*d)), f1(y_of(r - 2.0 * se))))
            .collect();
        svg.push(format!(
            "<polygon points=\"{} {}\" fill=\"{BAND}\" fill-opacity=\"0.15\"/>",
            up.join(" "),
            down.join(" ")
        ));
    }
    let yz = y_of(0.0);
    svg.push(format!(
        "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{ZERO}\" stroke-width=\"1\" stroke-dasharray=\"4 4\"/>",
        f1(yz),
        W - MR,
        f1(yz)
    ));
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{ZERO}\">the model</text>",
        W - MR - 4,
        f1(yz - 5.0)
    ));
    for run in runs(&series) {
        let pts: Vec<String> = run
            .iter()
            .map(|(d, (r, _))| format!("{},{}", f1(x_of(*d)), f1(y_of(*r))))
            .collect();
        svg.push(format!(
            "<polyline points=\"{}\" fill=\"none\" stroke=\"{LINE}\" stroke-width=\"2\"/>",
            pts.join(" ")
        ));
    }
    let color = if z > 2.0 {
        GREEN
    } else if z < -2.0 {
        RED
    } else {
        LINE
    };
    svg.push(format!(
        "<circle cx=\"{}\" cy=\"{}\" r=\"4\" fill=\"{color}\"/>",
        f1(x_of(last_d)),
        f1(y_of(last_r))
    ));
    svg.push("</svg>".to_string());
    write(&out, &svg);
    println!(
        "wrote {} ({} first-sight games, last {WINDOW}: {:+.2}, {:+.1} se, {verdict})",
        out.display(),
        rows.len(),
        last_r,
        z
    );
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::Duration;

    #[test]
    fn windows_mean_residual_and_its_error() {
        let d0 = NaiveDate::from_ymd_opt(2026, 1, 1).unwrap();
        let rows: Vec<Row> = (0..5)
            .map(|i| (d0 + Duration::days(i), (i % 2) as f64, 0.5))
            .collect();
        let win = windows(&rows, 4);
        assert_eq!(
            win.iter().map(|w| w.0).collect::<Vec<_>>(),
            vec![rows[3].0, rows[4].0]
        );
        assert!(win.iter().all(|w| w.1.abs() < 1e-9));
        assert!(win.iter().all(|w| (w.2 - 0.25).abs() < 1e-12));
        assert!(windows(&rows[..3], 4).is_empty());
    }
}
