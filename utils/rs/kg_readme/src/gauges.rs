// The progress gauges, graph/gauges.svg: one half dial per track, the
// algorithms and each language, on a 0 to 100 scale with a band label
// (learning, intermediate, advanced, expert). Every input is a function of
// the evidence and the forgetting curve, so every gauge decays when the
// solving stops and drops on a fail. No Elo is shown.
//
// algorithms first sight: the honest one. Of the problems met for the
//   first time in the last 30 days at his level (rating within
//   AT_RATING_BAND under the Elo carried into the game, kg::model::Ground,
//   the same count make stats prints), the share solved with no help and
//   inside the clock. Nothing modelled, nothing decayed: what happened.
//   Under the count, the Elo the count is measured against
//   (kg::model::elo_now, the one carried into each game) and the actual
//   rating band of the last BAND_GAMES first sights, lowest to highest.
// current reach: out of all of leetcode. The problems he has met, the
//   evidenced entries of graph/problems.json, each weighted by the
//   smallest degree of ownership (kg::status::node_axes) over the moves
//   of its walk, so a problem counts in full only while every move on it
//   is owned, over every rated problem in the catalog. Under the dial, as
//   text, the theoretical reach: the mean cold-solve odds of
//   the picker's fitted model (kg::model::solve_logit) over every rated
//   problem in the catalog, evidenced or drafted, as a count of problems.
//   It is a model's number over problems never met, so it is a line of
//   text, never a dial.
// a language: the sum of the degrees of its nodes (kg::status::node_axes)
//   over the planned size of its curriculum (LANGUAGES), not over the
//   nodes written so far, so seven Rust drills owned read as seven
//   sixtieths, not as done.

use std::collections::HashMap;

use chrono::Duration;
use kg::ctx::{Ctx, PView};
use kg::evidence::Evidence;
use kg::model::{
    elo_games, elo_now, solve_logit, solve_model, solve_ratings, walk_terms, Ground,
    PROGRESS_WINDOW_DAYS,
};
use kg::status::{current_recall, node_axes};

use crate::common::*;

/// (group id, shown name, planned nodes, where the plan comes from).
/// Algorithms is every other group and needs no plan: its denominator is
/// the catalog.
pub const LANGUAGES: [(&str, &str, i64, &str); 5] = [
    ("python", "python", 38, "The Python Tutorial, one node per section that names a construct (utils/history/backfill_python.py)"),
    (
        "ts",
        "typescript",
        30,
        "the TypeScript handbook, one node per chapter section",
    ),
    ("rust", "rust", 60, "Rustlings, one node per exercise group"),
    (
        "sql",
        "sql",
        25,
        "the LeetCode SQL 50 study plan, grouped into moves",
    ),
    (
        "design",
        "systems design",
        42,
        "the System Design Primer, 30 building blocks and its 8 worked designs, plus 4 blocks from the Stripe and Cloudflare posts on rate limiting and idempotency",
    ),
];

pub const BANDS: [(f64, &str); 4] = [
    (75.0, "expert"),
    (50.0, "advanced"),
    (25.0, "intermediate"),
    (0.0, "learning"),
];

#[derive(Clone, Debug, PartialEq)]
pub struct Gauge {
    pub name: String,
    /// 0 to 100
    pub pct: f64,
    /// owned nodes (degrees summed) or, for algorithms, problems reached
    pub done: f64,
    pub total: i64,
    pub unit: &'static str,
    /// a line under the count, "" for none
    pub note: String,
}

pub fn band(pct: f64) -> &'static str {
    BANDS
        .iter()
        .find(|(floor, _)| pct >= *floor)
        .map_or("learning", |(_, name)| name)
}

pub fn band_color(pct: f64, total: i64) -> &'static str {
    if total == 0 {
        return GRID;
    }
    match band(pct) {
        "expert" => GOLD,
        "advanced" => GREEN,
        "intermediate" => BLUE,
        _ => MUTED,
    }
}

/// Every gauge from the evidence: the first sights, then the languages in
/// LANGUAGES order.
pub fn compute(ctx: &Ctx, ev: &Evidence) -> Vec<Gauge> {
    let today = ctx.today();
    let pv = PView::new(ctx.evidenced());
    let degree: HashMap<&str, f64> = ctx
        .nodes
        .keys()
        .map(|id| (id.as_str(), node_axes(ctx, id, ev, &pv, today).degree))
        .collect();
    let group_of = |id: &str| ctx.nodes[id].group.clone().unwrap_or_default();

    let mut out = vec![first_sight(ctx, ev), reach(ctx, ev, &pv, &degree)];
    for (group, name, planned, _) in LANGUAGES {
        let done: f64 = degree
            .iter()
            .filter(|(id, _)| group_of(id) == group)
            .map(|(_, d)| d)
            .sum();
        let pct = if planned > 0 {
            (100.0 * done / planned as f64).min(100.0)
        } else {
            0.0
        };
        out.push(Gauge {
            name: name.to_string(),
            pct,
            done,
            total: planned,
            unit: "nodes",
            note: String::new(),
        });
    }
    out
}

/// Cold passes over first sights at his level in the last
/// PROGRESS_WINDOW_DAYS days.
fn first_sight(ctx: &Ctx, ev: &Evidence) -> Gauge {
    let today = ctx.today();
    let ratings = solve_ratings(ctx);
    let mut games = elo_games(ctx, ev, &ratings);
    games.retain(|(g, _, _)| kg::data::parse_date(&g.date) <= today);
    let ground = Ground::of(&games, Some(today - Duration::days(PROGRESS_WINDOW_DAYS)));
    let elo = elo_now(ctx, ev);
    let (lo, hi) = rating_band(&games, BAND_GAMES);
    Gauge {
        name: "algorithms first sight".to_string(),
        pct: if ground.tried > 0 {
            100.0 * ground.cold as f64 / ground.tried as f64
        } else {
            0.0
        },
        done: ground.cold as f64,
        total: ground.tried as i64,
        unit: "new problems, 30 days",
        note: format!(
            "elo {}, last {BAND_GAMES} first sights rated {} to {}",
            f0(elo),
            f0(lo),
            f0(hi)
        ),
    }
}

/// How many first sights the shown rating band spans.
pub const BAND_GAMES: usize = 60;

/// The lowest and highest problem rating over the last `n` first sights,
/// chains left out; (0, 0) with none.
pub fn rating_band(games: &[(kg::model::Game, f64, f64)], n: usize) -> (f64, f64) {
    let recent: Vec<f64> = games
        .iter()
        .filter(|(g, _, _)| g.first && !g.chain())
        .map(|(_, rating, _)| *rating)
        .collect();
    let tail = &recent[recent.len().saturating_sub(n)..];
    if tail.is_empty() {
        return (0.0, 0.0);
    }
    tail.iter()
        .fold((f64::MAX, f64::MIN), |(lo, hi), r| (lo.min(*r), hi.max(*r)))
}

/// The walk a problem is priced on: its moves, or its first drafted walk.
fn walk_of(p: &kg::data::Problem) -> Option<&[String]> {
    if !p.moves.is_empty() {
        Some(&p.moves)
    } else {
        p.walks.first().map(|w| w.moves.as_slice())
    }
}

/// A met problem's reach: the smallest degree over the known moves of its
/// walk; a walk with no known move reaches nothing.
fn walk_reach(moves: &[String], degree: &HashMap<&str, f64>) -> f64 {
    moves
        .iter()
        .filter_map(|m| degree.get(m.as_str()).copied())
        .fold(None, |acc: Option<f64>, d| {
            Some(acc.map_or(d, |a| a.min(d)))
        })
        .unwrap_or(0.0)
}

/// The modelled count over the whole catalog: the sum of the cold-solve
/// odds of every rated, walked problem, and how many were priced. None
/// without a fitted model.
fn theoretical_reach(ctx: &Ctx, ev: &Evidence, pv: &PView) -> Option<(f64, i64)> {
    let coef = solve_model(ctx)?;
    let ratings = solve_ratings(ctx);
    let recall = current_recall(ctx, ev, ctx.today());
    let counts = pv.carrier_counts(ctx);
    let (mut expected, mut total) = (0.0, 0);
    for (pnum, p) in ctx.all_problems() {
        let (Some(walk), Some(&rating)) = (walk_of(p), ratings.get(pnum)) else {
            continue;
        };
        let t = walk_terms(walk, &recall, &counts);
        expected += 1.0 / (1.0 + (-solve_logit(&coef, rating, &t)).exp());
        total += 1;
    }
    Some((expected, total))
}

/// Current reach out of all of leetcode: the met problems, each weighted
/// by the smallest degree over its walk, over every rated, walked problem
/// in the catalog. The theoretical reach, over the same catalog, is the
/// note under it.
fn reach(ctx: &Ctx, ev: &Evidence, pv: &PView, degree: &HashMap<&str, f64>) -> Gauge {
    let reached: f64 = pv
        .map
        .values()
        .filter_map(walk_of)
        .map(|walk| walk_reach(walk, degree))
        .sum();
    let (note, total) = match theoretical_reach(ctx, ev, pv) {
        Some((e, n)) if n > 0 => (format!("theoretical reach {} of {n} problems", f0(e)), n),
        _ => (
            String::new(),
            ctx.all_problems()
                .values()
                .filter(|p| walk_of(p).is_some())
                .count() as i64,
        ),
    };
    Gauge {
        name: "algorithms current reach".to_string(),
        pct: if total > 0 {
            100.0 * reached / total as f64
        } else {
            0.0
        },
        done: reached,
        total,
        unit: "problems",
        note,
    }
}

/// A row of half dials, one per gauge: the arc filled to pct in the band's
/// colour, the percentage, the band, and the count under it.
pub fn svg(gauges: &[Gauge]) -> String {
    let (cell, h) = (230i64, 184i64);
    let w = cell * gauges.len() as i64;
    let (r, cy) = (62.0, 96.0);
    let point = |cx: f64, pct: f64, radius: f64| {
        let a = std::f64::consts::PI * (1.0 - pct / 100.0);
        (cx + radius * a.cos(), cy - radius * a.sin())
    };
    let arc = |cx: f64, p0: f64, p1: f64, color: &str, opacity: &str| {
        let (x0, y0) = point(cx, p0, r);
        let (x1, y1) = point(cx, p1, r);
        format!(
            "<path d=\"M{},{} A{r},{r} 0 0 1 {},{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"12\" stroke-opacity=\"{opacity}\" stroke-linecap=\"butt\"/>",
            f1(x0),
            f1(y0),
            f1(x1),
            f1(y1)
        )
    };
    let mut out = vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{w}\" height=\"{h}\" viewBox=\"0 0 {w} {h}\" font-family=\"-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif\">"),
        format!("<rect width=\"{w}\" height=\"{h}\" fill=\"{BG}\"/>"),
    ];
    for (i, g) in gauges.iter().enumerate() {
        let cx = (i as i64 * cell + cell / 2) as f64;
        let color = band_color(g.pct, g.total);
        out.push(arc(cx, 0.0, 100.0, GRID, "1.0"));
        if g.pct > 0.0 {
            out.push(arc(cx, 0.0, g.pct.clamp(0.5, 100.0), color, "1.0"));
        }
        for t in [25.0, 50.0, 75.0] {
            let (x0, y0) = point(cx, t, r - 9.0);
            let (x1, y1) = point(cx, t, r + 9.0);
            out.push(format!(
                "<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{BG}\" stroke-width=\"2\"/>",
                f1(x0),
                f1(y0),
                f1(x1),
                f1(y1)
            ));
        }
        out.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"24\" font-weight=\"bold\" fill=\"{color}\">{}%</text>",
            f1(cx),
            f1(cy - 6.0),
            f0(g.pct)
        ));
        out.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"15\" font-weight=\"bold\" fill=\"{INK}\">{}</text>",
            f1(cx),
            f1(cy + 24.0),
            g.name
        ));
        let (label, count) = if g.total == 0 {
            (
                if g.unit == "nodes" {
                    "no nodes yet"
                } else {
                    "no games yet"
                }
                .to_string(),
                String::new(),
            )
        } else {
            (
                band(g.pct).to_string(),
                format!("{} of {} {}", f0(g.done), g.total, g.unit),
            )
        };
        out.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"12\" fill=\"{color}\">{label}</text>",
            f1(cx),
            f1(cy + 42.0)
        ));
        out.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"10\" fill=\"{MUTED}\">{count}</text>",
            f1(cx),
            f1(cy + 58.0)
        ));
        if !g.note.is_empty() {
            out.push(format!(
                "<text x=\"{}\" y=\"{}\" text-anchor=\"middle\" font-size=\"10\" fill=\"{MUTED}\">{}</text>",
                f1(cx),
                f1(cy + 72.0),
                g.note
            ));
        }
    }
    out.push("</svg>".to_string());
    out.join("\n") + "\n"
}

pub fn render(ctx: &Ctx, ev: &Evidence) {
    let path = ctx.graph_dir().join("gauges.svg");
    let gauges = compute(ctx, ev);
    std::fs::write(&path, svg(&gauges)).expect("write gauges.svg");
    let summary: Vec<String> = gauges
        .iter()
        .map(|g| format!("{} {}% {}", g.name, f0(g.pct), band(g.pct)))
        .collect();
    println!("wrote {} ({})", path.display(), summary.join(", "));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bands_are_quarters_and_the_floor_is_learning() {
        assert_eq!(band(0.0), "learning");
        assert_eq!(band(24.9), "learning");
        assert_eq!(band(25.0), "intermediate");
        assert_eq!(band(50.0), "advanced");
        assert_eq!(band(75.0), "expert");
        assert_eq!(band(100.0), "expert");
        assert_eq!(band_color(10.0, 0), GRID);
        assert_eq!(band_color(80.0, 60), GOLD);
    }

    #[test]
    fn a_met_problem_reaches_as_far_as_its_weakest_known_move() {
        let mut degree = HashMap::new();
        degree.insert("a", 1.0);
        degree.insert("b", 0.25);
        let m = |xs: &[&str]| xs.iter().map(|s| s.to_string()).collect::<Vec<_>>();
        assert_eq!(walk_reach(&m(&["a", "b"]), &degree), 0.25);
        assert_eq!(walk_reach(&m(&["a", "unknown"]), &degree), 1.0);
        assert_eq!(walk_reach(&m(&["unknown"]), &degree), 0.0);
        let mut p = kg::data::Problem::default();
        assert_eq!(walk_of(&p), None);
        p.walks.push(kg::data::Walk {
            moves: m(&["a"]),
            ..Default::default()
        });
        assert_eq!(walk_of(&p).unwrap(), &m(&["a"])[..]);
        p.moves = m(&["b"]);
        assert_eq!(walk_of(&p).unwrap(), &m(&["b"])[..]);
    }

    #[test]
    fn the_svg_has_one_dial_per_gauge_and_a_note_when_given() {
        let gs = vec![
            Gauge {
                name: "algorithms current reach".into(),
                pct: 40.0,
                done: 200.0,
                total: 500,
                unit: "problems",
                note: "theoretical reach 1700 of 3000 problems".into(),
            },
            Gauge {
                name: "python".into(),
                pct: 0.0,
                done: 0.0,
                total: 0,
                unit: "nodes",
                note: String::new(),
            },
        ];
        let s = svg(&gs);
        assert!(
            s.contains(">40%<")
                && s.contains(">intermediate<")
                && s.contains("200 of 500 problems")
        );
        assert!(s.contains(">theoretical reach 1700 of 3000 problems<"));
        assert!(s.contains(">no nodes yet<") && s.contains("width=\"460\""));
    }
}
