// The review backlog day by day, rendered into graph/backlog.svg.
//
// Three counts per day, each taken from the evidence on file up to that
// day and the same clocks the picker runs (kg::clock::problem_due,
// kg::drills::anki_due):
//   open cards  - problems on a review clock of their own: an attempt went
//                 badly (a FAILED file, any assist) and no unaided clean
//                 rep has retired the card since.
//   due cards   - the open cards whose clock has run out.
//   due drills  - bank files done at least once whose clock has run out.
//
// Ported from utils/readme/kg_backlog_svg (Python) on 2026-09-13.

use chrono::{Duration, NaiveDate};
use kg::clock::problem_due;
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::drills::anki_due;
use kg::evidence::Evidence;

use crate::common::*;

const W: i64 = 1200;
const H: i64 = 400;
const SERIES: [(&str, &str); 3] = [
    ("open cards", MUTED),
    ("due cards", RED),
    ("due drills", GOLD),
];
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 40;

/// [(date, open cards, due cards, due drills)] one per day from the first
/// evidenced attempt to today.
pub fn counts(ctx: &Ctx, ev: &Evidence) -> Vec<(NaiveDate, i64, i64, i64)> {
    let banks = ctx.every_bank_path();
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| (&ev.rec(a).date, ev.fname(a)).cmp(&(&ev.rec(b).date, ev.fname(b))));
    let d0 = parse_date(&ev.rec(order[0]).date);
    // one table grown a day at a time, in date order
    let mut upto = Evidence::new(Vec::new());
    let (mut i, mut out, mut d) = (0, Vec::new(), d0);
    while d <= ctx.today() {
        let cut = d.format("%Y-%m-%d").to_string();
        while i < order.len() && ev.rec(order[i]).date <= cut {
            upto.push(ev.fname(order[i]).to_string(), ev.rec(order[i]).clone());
            i += 1;
        }
        let cards: Vec<(NaiveDate, i64)> = upto
            .by_problem
            .keys()
            .filter(|p| p.chars().next().is_some_and(|c| c.is_ascii_digit()))
            .filter_map(|p| problem_due(&upto, p))
            .collect();
        let drills = banks
            .iter()
            .filter(|p| anki_due(ctx, p, &upto).is_some_and(|a| a.0 <= d))
            .count();
        out.push((
            d,
            cards.len() as i64,
            cards.iter().filter(|c| c.0 <= d).count() as i64,
            drills as i64,
        ));
        d += Duration::days(1);
    }
    out
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("backlog.svg");
    let rows = counts(ctx, ev);
    let (d0, d1) = (rows[0].0, rows[rows.len() - 1].0);
    let span = days_between(d0, d1).max(1);
    let (top, bottom) = (MT, H - MB);
    let hi = rows.iter().map(|r| r.1.max(r.2).max(r.3)).max().unwrap();
    let step = if hi <= 30 {
        5
    } else if hi <= 80 {
        10
    } else {
        25
    };
    let hi = {
        let v = -(-hi).div_euclid(step) * step;
        if v == 0 {
            step
        } else {
            v
        }
    };
    let x_of =
        |d: NaiveDate| ML as f64 + days_between(d0, d) as f64 / span as f64 * (W - ML - MR) as f64;
    let y_of = |v: f64| bottom as f64 - v / hi as f64 * (bottom - top) as f64;
    let last = rows[rows.len() - 1];
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">today: {} open cards, {} due, {} drills due</text>",
            f0(W as f64 / 2.0),
            last.1,
            last.2,
            last.3
        ),
    ];
    value_ticks(&mut svg, 0, hi, step, y_of, ML, W - MR);
    month_ticks(&mut svg, d0, d1, x_of, top, bottom, 1);
    for (i, (_, color)) in SERIES.iter().enumerate() {
        let pts: Vec<String> = rows
            .iter()
            .map(|r| format!("{},{}", f1(x_of(r.0)), f1(y_of([r.1, r.2, r.3][i] as f64))))
            .collect();
        svg.push(format!(
            "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\"/>",
            pts.join(" ")
        ));
    }
    let mut legend = Legend::new(ML, true, MT - 18);
    for (label, color) in SERIES {
        legend.line(&mut svg, color, label, false);
    }
    svg.push("</svg>".to_string());
    write(&out, &svg);
    println!(
        "wrote {} ({} open cards, {} due, {} drills due)",
        out.display(),
        last.1,
        last.2,
        last.3
    );
}
