// Elo against hours of recorded solving, rendered into graph/hours.svg.
//
// The x axis is cumulative solve time from the "solve time: Xm Ys" trailer
// `make solved` writes into every solve and drill commit, in commit order,
// each solve capped at CAP_MIN minutes. The y axis is the Elo of elo.rs,
// one point per day with a scored game, placed at the hours recorded
// through that day.
//
// The dashed line is the rate the Carnegie Mellon study of Codeforces
// users found (codeforces.com/blog/entry/112510): about 200 rating points
// per 800 hours of practice. It is anchored at game ANCHOR, after the Elo
// has settled from its 1200 start.
//
// Ported from utils/readme/kg_hours_svg (Python) on 2026-09-13.

use std::process::{Command, Stdio};

use chrono::NaiveDate;
use kg::ctx::Ctx;
use kg::data::parse_date;
use kg::evidence::Evidence;
use regex::Regex;

use crate::common::*;
use crate::elo::{self, MA, MA_LINE, RANKS};

pub const CAP_MIN: f64 = 120.0;
pub const ANCHOR: usize = 100;
pub const CMU_PER_HOUR: f64 = 200.0 / 800.0;

const W: i64 = 1200;
const H: i64 = 400;
const ELO: &str = GREEN;
const REF: &str = MUTED;
const ML: i64 = 62;
const MR: i64 = 24;
const MT: i64 = 60;
const MB: i64 = 40;

/// [(date, cumulative hours of recorded solving through that day)] sorted,
/// from the solve-time trailers of the commits adding under solved/ and
/// drills/.
pub fn hours_by_day(ctx: &Ctx) -> Vec<(NaiveDate, f64)> {
    let out = Command::new("git")
        .args([
            "log",
            "--diff-filter=A",
            "--date=short",
            "--format=%x02%ad%x01%B",
            "--",
            "solved/",
            "drills/",
        ])
        .current_dir(&ctx.root)
        .env("TZ", "Asia/Manila")
        .stderr(Stdio::null())
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
        .unwrap_or_default();
    let re = Regex::new(r"solve time: (\d+)m (\d+)s").unwrap();
    // summed in git log order, day by day, as the Python did
    let mut per_day: Vec<(NaiveDate, f64)> = Vec::new();
    for chunk in out.split('\x02').skip(1) {
        let Some((d, body)) = chunk.split_once('\x01') else {
            continue;
        };
        if let Some(m) = re.captures(body) {
            let mins =
                (m[1].parse::<f64>().unwrap() + m[2].parse::<f64>().unwrap() / 60.0).min(CAP_MIN);
            let d = parse_date(d);
            match per_day.iter_mut().find(|(dd, _)| *dd == d) {
                Some(slot) => slot.1 += mins / 60.0,
                None => per_day.push((d, mins / 60.0)),
            }
        }
    }
    per_day.sort_by_key(|(d, _)| *d);
    let mut total = 0.0;
    per_day
        .into_iter()
        .map(|(d, h)| {
            total += h;
            (d, total)
        })
        .collect()
}

/// Hours recorded through day d.
pub fn at(cum: &[(NaiveDate, f64)], d: NaiveDate) -> f64 {
    cum.iter()
        .filter(|(dd, _)| *dd <= d)
        .fold(0.0, |b, (_, h)| b.max(*h))
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("hours.svg");
    let gs = elo::games(ctx, ev);
    let curve = elo::elo(&gs, elo::START);
    let cum = hours_by_day(ctx);
    let pts: Vec<(f64, f64)> = curve.iter().map(|(d, r)| (at(&cum, *d), *r)).collect();
    let anchor_day = gs[ANCHOR.min(gs.len()) - 1].0;
    let anchor = curve
        .iter()
        .zip(&pts)
        .find(|((d, _), _)| *d >= anchor_day)
        .map(|((_, r), (h, _))| (*h, *r))
        .expect("anchor");
    let total = pts[pts.len() - 1].0;
    let x_hi = {
        let v = ceil_to(total.trunc(), 50);
        if v == 0 {
            50
        } else {
            v
        }
    };
    let mut vals: Vec<f64> = pts.iter().map(|p| p.1).collect();
    vals.push(RANKS[0].0 as f64);
    let lo = floor_to(vals.iter().cloned().fold(f64::INFINITY, f64::min), 100) - 100;
    let hi = ceil_to(vals.iter().cloned().fold(f64::NEG_INFINITY, f64::max), 100) + 100;
    let (top, bottom) = (MT, H - MB);
    let x_of = |h: f64| ML as f64 + h / x_hi as f64 * (W - ML - MR) as f64;
    let y_of = |v: f64| bottom as f64 - (v - lo as f64) / (hi - lo) as f64 * (bottom - top) as f64;

    let gained = pts[pts.len() - 1].1 - anchor.1;
    let spent = total - anchor.0;
    let rate = if spent != 0.0 { gained / spent } else { 0.0 };
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} hours recorded - {} elo over {} hours since game {ANCHOR} ({} per 100 hours; the Carnegie Mellon rate is {})</text>",
            f0(W as f64 / 2.0),
            f0(total),
            s0(gained),
            f0(spent),
            f0(rate * 100.0),
            f0(CMU_PER_HOUR * 100.0)
        ),
    ];
    rank_bands(&mut svg, &RANKS, y_of, ML, W, MR, top);
    value_ticks(&mut svg, lo, hi, 100, y_of, ML, W - MR);
    let step = if x_hi <= 500 { 50 } else { 100 };
    let mut h = 0;
    while h <= x_hi {
        let x = f1(x_of(h as f64));
        svg.push(format!(
            "<line x1=\"{x}\" y1=\"{top}\" x2=\"{x}\" y2=\"{bottom}\" stroke=\"{GRID}\" stroke-width=\"1\"/>"
        ));
        svg.push(format!(
            "<text x=\"{x}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{h}h</text>",
            bottom + 18
        ));
        h += step;
    }
    let (x0, y0) = (x_of(anchor.0), y_of(anchor.1));
    let (x1, y1) = (
        x_of(x_hi as f64),
        y_of(anchor.1 + (x_hi as f64 - anchor.0) * CMU_PER_HOUR),
    );
    svg.push(format!(
        "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{REF}\" stroke-width=\"1.5\" stroke-dasharray=\"6 4\"/>",
        f1(x0),
        f1(y0),
        f1(x1),
        f1(y1)
    ));
    let path: Vec<String> = pts
        .iter()
        .map(|(h, r)| format!("{},{}", f1(x_of(*h)), f1(y_of(*r))))
        .collect();
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{ELO}\" stroke-width=\"2\" stroke-opacity=\"0.3\"/>",
        path.join(" ")
    ));
    let path: Vec<String> = elo::elo_ma(&gs, elo::START, &[])
        .iter()
        .map(|(d, r)| format!("{},{}", f1(x_of(at(&cum, *d))), f1(y_of(*r))))
        .collect();
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{MA_LINE}\" stroke-width=\"2\"/>",
        path.join(" ")
    ));
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
        REF,
        "200 elo per 800 hours (Carnegie Mellon, Codeforces users)",
        true,
    );
    svg.push("</svg>".to_string());
    write(&out, &svg);
    println!(
        "wrote {} ({} hours, {} elo over {} hours since game {ANCHOR})",
        out.display(),
        f0(total),
        s0(gained),
        f0(spent)
    );
}
