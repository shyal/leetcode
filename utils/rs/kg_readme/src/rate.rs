// The first-sight rate, in Elo points per 100 recorded hours, rendered into
// graph/rate_badge.svg (a badge) and graph/rate_gauge.svg (a gauge).
//
// The rate is onsite::first_sight_rate. The gauge spans -SPAN to +SPAN
// with the Carnegie Mellon rate (25 per 100 hours) marked on it. Green
// above zero, red below.
//
// Ported from utils/readme/kg_rate_svg (Python) on 2026-09-13.

use kg::ctx::Ctx;
use kg::evidence::Evidence;

use crate::common::*;
use crate::{elo, hours, onsite};

const SPAN: i64 = 150;
const GAUGE_GRID: &str = "#30363d";
const CMU: &str = BLUE;

fn color_of(v: f64) -> &'static str {
    if v > 0.0 {
        GREEN
    } else if v < 0.0 {
        RED
    } else {
        MUTED
    }
}

pub fn rate_badge(v: f64) -> String {
    badge("elo per 100h, new problems only", &s0(v), color_of(v))
}

/// A half dial from -SPAN on the left to +SPAN on the right, the needle at
/// the rate, clipped to the ends, the Carnegie Mellon rate marked.
pub fn gauge(v: f64, window: i64, p0: f64, p1: f64, cmu: f64) -> String {
    let (w, h) = (420i64, 200i64);
    let (cx, cy, r) = (w as f64 / 2.0, 160i64, 120i64);
    let point = |x: f64, radius: i64| {
        let a = std::f64::consts::PI
            * (1.0 - (x.clamp(-(SPAN as f64), SPAN as f64) + SPAN as f64) / (2 * SPAN) as f64);
        (
            cx + radius as f64 * a.cos(),
            cy as f64 - radius as f64 * a.sin(),
        )
    };
    let arc = |v0: f64, v1: f64, radius: i64, color: &str, width: i64, opacity: &str| {
        let (x0, y0) = point(v0, radius);
        let (x1, y1) = point(v1, radius);
        format!(
            "<path d=\"M{},{} A{radius},{radius} 0 0 1 {},{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"{width}\" stroke-opacity=\"{opacity}\"/>",
            f1(x0),
            f1(y0),
            f1(x1),
            f1(y1)
        )
    };
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {w} {h}\" width=\"{w}\" height=\"{h}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{w}\" height=\"{h}\" fill=\"{BG}\"/>"),
        arc(-(SPAN as f64), 0.0, r, RED, 14, "0.35"),
        arc(0.0, SPAN as f64, r, GREEN, 14, "0.35"),
    ];
    if v != 0.0 {
        svg.push(arc(v.min(0.0), v.max(0.0), r, color_of(v), 14, "1.0"));
    }
    let mut t = -SPAN;
    while t <= SPAN {
        let (x0, y0) = point(t as f64, r - 12);
        let (x1, y1) = point(t as f64, r + 12);
        svg.push(format!(
            "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{GAUGE_GRID}\" stroke-width=\"1\"/>",
            f1(x0),
            f1(y0),
            f1(x1),
            f1(y1)
        ));
        let (tx, ty) = point(t as f64, r + 24);
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"10\" fill=\"{MUTED}\">{t:+}</text>",
            f1(tx),
            f1(ty + 4.0)
        ));
        t += 50;
    }
    let (x0, y0) = point(cmu, r - 10);
    let (x1, y1) = point(cmu, r + 10);
    svg.push(format!(
        "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{CMU}\" stroke-width=\"2\"/>",
        f1(x0),
        f1(y0),
        f1(x1),
        f1(y1)
    ));
    let (tx, ty) = point(cmu, r - 30);
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"10\" fill=\"{CMU}\">CMU {}</text>",
        f1(tx),
        f1(ty + 4.0),
        f0(cmu)
    ));
    let (nx, ny) = point(v, r - 20);
    svg.push(format!(
        "<line x1=\"{}\" y1=\"{cy}\" x2=\"{}\" y2=\"{}\" stroke=\"{INK}\" stroke-width=\"2.5\" stroke-linecap=\"round\"/>",
        pyf(cx),
        f1(nx),
        f1(ny)
    ));
    svg.push(format!(
        "<circle cx=\"{}\" cy=\"{cy}\" r=\"5\" fill=\"{INK}\"/>",
        pyf(cx)
    ));
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"26\" font-weight=\"bold\" fill=\"{}\">{}</text>",
        pyf(cx),
        cy - 40,
        color_of(v),
        s0(v)
    ));
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">elo per 100h on new problems, {} to {}, first vs last {window} days</text>",
        pyf(cx),
        cy + 28,
        f0(p0),
        f0(p1)
    ));
    svg.push("</svg>".to_string());
    svg.join("\n") + "\n"
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let badge_path = ctx.graph_dir().join("rate_badge.svg");
    let gauge_path = ctx.graph_dir().join("rate_gauge.svg");
    let gs = elo::games(ctx, ev);
    let (per_hour, p0, p1) = onsite::first_sight_rate(&gs, &hours::hours_by_day(ctx));
    let v = per_hour * 100.0;
    let cmu = hours::CMU_PER_HOUR * 100.0;
    std::fs::write(&badge_path, rate_badge(v)).unwrap();
    std::fs::write(&gauge_path, gauge(v, onsite::FS_WINDOW, p0, p1, cmu)).unwrap();
    println!(
        "wrote {} and {} (first-sight {} elo per 100h)",
        badge_path.display(),
        gauge_path.display(),
        s0(v)
    );
}
