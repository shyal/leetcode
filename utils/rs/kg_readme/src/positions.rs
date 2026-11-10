// Where is each node on its forgetting curve today? Rendered into
// graph/positions.svg.
//
// The curve in graph/curve.json gives each node a stability s, and the
// memory of the node is (1 + gap/s)^(-beta), where gap is the number of
// days since its last clean rep. The chart shows one faint curve for each
// node and one dot at the gap of the node today. A node is SOLID while its
// memory is at or above the target retention, and STALE below it; the
// stale nodes have their names. A node whose last rep was a fail (FRAGILE)
// is not on a curve, and the header gives the count of those nodes.
//
// The Python renderer (a replay of the full history) was deleted on
// 2026-09-20; this one draws the current state and is live since
// 2026-11-10.

use kg::ctx::Ctx;
use kg::evidence::Evidence;
use kg::status::{node_position, node_status, FRAGILE, STALE};

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
/// The number of points of one curve.
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

/// One node on its curve: days since the last clean rep, stability in
/// days, memory today.
#[derive(Clone, Debug, PartialEq)]
pub struct Pos {
    pub node: String,
    pub stale: bool,
    pub gap: f64,
    pub stability: f64,
    pub memory: f64,
}

/// (the nodes on a curve, the number of fragile nodes, beta, the target
/// retention); None without a fitted curve.
fn load(ctx: &Ctx, ev: &Evidence) -> Option<(Vec<Pos>, usize, f64, f64)> {
    let cv = ctx.curve.as_ref()?;
    let today = ctx.today();
    let mut nodes: Vec<&String> = ctx.nodes.keys().collect();
    nodes.sort();
    let mut out = Vec::new();
    let mut fragile = 0;
    for n in nodes {
        match node_position(ctx, n, ev, today) {
            Some((st, gap, stability, memory)) => out.push(Pos {
                node: n.clone(),
                stale: st == STALE,
                gap,
                stability,
                memory,
            }),
            None => {
                if node_status(ctx, n, ev, today).0 == FRAGILE {
                    fragile += 1;
                }
            }
        }
    }
    if out.is_empty() {
        None
    } else {
        Some((out, fragile, cv.beta, cv.target_retention))
    }
}

/// The right end of the x axis, in days: the first tick at or after the
/// largest gap, and one month at least.
pub fn gap_max(ps: &[Pos]) -> f64 {
    let g = ps.iter().map(|p| p.gap).fold(30.0f64, f64::max);
    TICKS.iter().map(|t| t.0).find(|t| *t >= g).unwrap_or(g)
}

/// The lowest value of the y axis, in percent: the multiple of 5 below
/// every dot and below the target retention.
pub fn floor_pct(ps: &[Pos], target: f64) -> i64 {
    let lo = ps.iter().map(|p| p.memory).fold(target, f64::min);
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

pub fn chart(ps: &[Pos], fragile: usize, beta: f64, target: f64) -> Vec<String> {
    let (top, bottom) = (MT, H - MB);
    let lo = floor_pct(ps, target);
    let gmax = gap_max(ps);
    let x_of = |g: f64| ML as f64 + g.max(1.0).log10() / gmax.log10() * (W - ML - MR) as f64;
    let y_of = |v: f64| {
        bottom as f64 - (100.0 * v - lo as f64) / (100 - lo) as f64 * (bottom - top) as f64
    };
    let stale = ps.iter().filter(|p| p.stale).count();
    let mut svg = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {H}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{H}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"20\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{} nodes on their forgetting curves today: {} solid, {} stale - {} fragile nodes are not on a curve</text>",
            f0(W as f64 / 2.0),
            ps.len(),
            ps.len() - stale,
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
    legend.line(&mut svg, CURVE, "the curve of a node", false);
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
    // One curve for each stability, to the bottom of the axis.
    let mut stabilities: Vec<i64> = ps.iter().map(|p| p.stability.round() as i64).collect();
    stabilities.sort();
    stabilities.dedup();
    for s in stabilities {
        let pts: Vec<String> = (0..=SAMPLES)
            .map(|i| 10f64.powf(i as f64 / SAMPLES as f64 * gmax.log10()))
            .map(|g| (g, (1.0 + g / s as f64).powf(-beta)))
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
    for p in ps.iter().filter(|p| !p.stale) {
        svg.push(format!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"4\" fill=\"{SOLID_COLOR}\" fill-opacity=\"0.8\"/>",
            f1(x_of(p.gap)),
            f1(y_of(p.memory))
        ));
    }
    // The stale nodes, from the top down, each with its name. A name goes
    // to the left of its dot when it does not fit on the right.
    let mut stales: Vec<&Pos> = ps.iter().filter(|p| p.stale).collect();
    stales.sort_by(|a, b| b.memory.partial_cmp(&a.memory).unwrap());
    let boxes: Vec<(f64, f64, f64)> = stales
        .iter()
        .map(|p| {
            let w = CHAR_W * p.node.chars().count() as f64;
            let x = x_of(p.gap);
            let left = x + 8.0 + w > (W - MR) as f64;
            // A name near the target line goes below the line.
            let y = y_of(p.memory);
            let y = if (y - yt).abs() < LABEL_H {
                yt + LABEL_H
            } else {
                y
            };
            (if left { x - 8.0 - w } else { x + 8.0 }, y, w)
        })
        .collect();
    let ys = spread(&boxes);
    for ((p, b), y) in stales.iter().zip(&boxes).zip(&ys) {
        svg.push(format!(
            "<circle cx=\"{}\" cy=\"{}\" r=\"5\" fill=\"{STALE_COLOR}\"/>",
            f1(x_of(p.gap)),
            f1(y_of(p.memory))
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{INK}\">{}</text>",
            f1(b.0),
            f1(y + 4.0),
            p.node
        ));
    }
    svg.push("</svg>".to_string());
    svg
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let out = ctx.graph_dir().join("positions.svg");
    let Some((ps, fragile, beta, target)) = load(ctx, ev) else {
        println!("no chart: no node is on a fitted curve (graph/curve.json is missing)");
        return;
    };
    write(&out, &chart(&ps, fragile, beta, target));
    println!(
        "wrote {} ({} nodes, {} stale, {} fragile and not on a curve)",
        out.display(),
        ps.len(),
        ps.iter().filter(|p| p.stale).count(),
        fragile
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    fn p(node: &str, stale: bool, gap: f64, stability: f64, memory: f64) -> Pos {
        Pos {
            node: node.to_string(),
            stale,
            gap,
            stability,
            memory,
        }
    }

    #[test]
    fn the_x_axis_ends_at_the_first_tick_after_the_largest_gap() {
        assert_eq!(gap_max(&[p("a", false, 3.0, 50.0, 0.99)]), 30.0);
        assert_eq!(gap_max(&[p("a", true, 130.0, 50.0, 0.86)]), 240.0);
        assert_eq!(gap_max(&[p("a", true, 240.0, 50.0, 0.82)]), 240.0);
    }

    #[test]
    fn the_y_axis_starts_below_every_dot_and_the_target() {
        assert_eq!(floor_pct(&[p("a", false, 3.0, 50.0, 0.99)], 0.9), 85);
        assert_eq!(floor_pct(&[p("a", true, 130.0, 50.0, 0.86)], 0.9), 85);
        assert_eq!(floor_pct(&[p("a", true, 400.0, 50.0, 0.78)], 0.9), 75);
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
    fn the_chart_has_one_dot_for_each_node_and_a_name_for_each_stale_node() {
        let ps = [
            p("two-pointers", false, 3.0, 60.0, 0.994),
            p("union-find", false, 20.0, 60.0, 0.968),
            p("trie-insert", true, 200.0, 60.0, 0.846),
        ];
        let s = chart(&ps, 4, 0.1143, 0.9).join("\n");
        assert_eq!(s.matches("<circle").count(), 3 + 2);
        assert_eq!(s.matches("<polyline").count(), 1);
        assert!(s.contains(
            ">3 nodes on their forgetting curves today: 2 solid, 1 stale - 4 fragile nodes are not on a curve<"
        ));
        assert!(s.contains(">trie-insert</text>"));
        assert!(!s.contains(">union-find</text>"));
        assert!(s.contains(">8m</text>"));
        assert!(!s.contains(">16m</text>"));
    }
}
