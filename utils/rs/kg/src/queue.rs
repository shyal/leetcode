// The queue: the next problems the picker would serve if every rep is
// clean (pick::upcoming, drills skipped), each with its contest rating
// against his Elo. Printed under every `make next` and by `make queue`;
// `make queue gate` asks a model which plainer problems should gate the
// ones rated well above him, and learning mode (kg::learning) asks the
// same for each first sight it serves.
//
// A gate is a plainer problem that isolates one piece of a harder one, so
// a clean solve of it proves the piece before the harder one is served
// (215 gates 2542). The model reads the target's cached solution
// (.prepare_cache) and picks from every rated problem GATE_MARGIN or more
// below it, by number and title alone. Moves are not sent: the mapped
// moves of 2542 are the brute force, and a move filter never reaches 215
// (experiment of 2026-09-14: solution + all titles found 215, 84, 875
// and 1011; moves alone missed two of three). Its reasons name no
// technique.

use std::collections::{HashMap, HashSet};

use serde_json::{json, Map, Value};

use crate::ctx::{Ctx, PView};
use crate::evidence::Evidence;
use crate::model::{
    account_first_dates, display_difficulty, first_sight_elo_now, first_sight_open, solve_ratings,
};
use crate::pick::upcoming;
use crate::table::{BoxKind, Table};

pub const QUEUE_LEN: usize = 10;
const DAYS: i64 = 30;
pub const GATE_MARGIN: f64 = 150.0;

pub const GATE_SYSTEM_PROMPT: &str = "You maintain the prerequisite edges of one operator's leetcode practice\ngraph. A gate is a plainer problem that isolates one piece of a harder\ntarget problem, so that a clean solve of the gate proves the piece before\nthe target is served. Each target comes with its solution; read it and\nname the pieces yourself.\n\nFor each target, name up to three gates, taken from the candidates only,\none per distinct piece, each isolating that piece as purely as possible.\nNever name a problem that is not in the candidates. Never repeat a problem\nalready in the target's after list.\n\nWriting rules for `why`: one short declarative sentence in plain English.\nRefer to problems by number and title only. Never name a technique, a\nmove, or a data structure.\n\nReply with one JSON object and nothing else:\n{\"gates\": [{\"problem\": \"<target number>\", \"gate\": \"<candidate number>\", \"why\": \"<one sentence>\"}]}\n";

/// One row of the queue: number, title, LeetCode's label, the label the
/// rating earns (model::display_difficulty), rating (None when the problem has no contest
/// rating), and whether serving it would be a first sight (no record of
/// the problem in the evidence and no earlier acceptance on the leetcode
/// account, model::first_sight_open).
pub struct QueueRow {
    pub pnum: String,
    pub title: String,
    pub leetcode: String,
    pub difficulty: String,
    pub rating: Option<f64>,
    pub first_sight: bool,
}

/// The next `len` problems the picker would serve.
pub fn queue_rows(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    asleep: &[String],
    len: usize,
) -> Vec<QueueRow> {
    let ratings = solve_ratings(ctx);
    let account = account_first_dates(&ctx.root);
    let today = ctx.today().to_string();
    upcoming(ctx, pv, ev, len, asleep, DAYS)
        .into_iter()
        .map(|pnum| QueueRow {
            title: pv
                .get(&pnum)
                .or_else(|| ctx.all_problems().get(&pnum))
                .map(|p| p.title.clone())
                .unwrap_or_default(),
            leetcode: ctx.problem_difficulty(&pnum, &pv.map),
            difficulty: display_difficulty(ctx, &pnum, pv),
            rating: ratings.get(&pnum).copied(),
            first_sight: first_sight_open(ev, &account, &pnum, &today),
            pnum,
        })
        .collect()
}

/// The rating line's colour for a gap: red 100 above him, yellow inside
/// 100, green below.
pub fn gap_colour(gap: f64) -> &'static str {
    if gap > 100.0 {
        "red"
    } else if gap > -100.0 {
        "yellow"
    } else {
        "green"
    }
}

/// The colour of a difficulty label.
pub fn difficulty_colour(d: &str) -> &'static str {
    match d {
        "Easy" => "green",
        "Medium" => "yellow",
        "Hard" => "red",
        _ => "dim",
    }
}

/// kg_next.queue_table: the queue as a table, coloured like the rating
/// line, `len` rows long. None when the replay serves nothing.
pub fn queue_table(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    asleep: &[String],
    len: usize,
) -> Option<Table> {
    let rows = queue_rows(ctx, pv, ev, asleep, len);
    if rows.is_empty() {
        return None;
    }
    let elo = first_sight_elo_now(ctx, ev);
    let mut table = Table::plain(
        &[
            "Problem",
            "LeetCode",
            "Real",
            "Rating",
            "Gap",
            "Odds",
            "First sight",
            "Crowd",
        ],
        Some(&format!("queue (elo {elo:.0})")),
        BoxKind::Rounded,
    );
    for row in rows {
        let label = |d: &str| {
            let style = difficulty_colour(d);
            format!("[{style}]{d}[/{style}]")
        };
        let [r, g, o] = match row.rating {
            None => ["-".into(), "-".into(), "-".into()],
            Some(rating) => {
                let gap = rating - elo;
                let odds = 1.0 / (1.0 + 10f64.powf(gap / 400.0));
                let colour = gap_colour(gap);
                [
                    format!("[bold]{rating:.0}[/bold]"),
                    format!("[{colour}]{gap:+.0}[/{colour}]"),
                    format!("[{colour}]{:.0}%[/{colour}]", odds * 100.0),
                ]
            }
        };
        table.add_row(&[
            format!("{}. {}", row.pnum, row.title),
            label(&row.leetcode),
            label(&row.difficulty),
            r,
            g,
            o,
            if row.first_sight {
                "[green]yes[/green]".into()
            } else {
                "[dim]no[/dim]".into()
            },
            crowd_cell(ctx, &row.pnum),
        ]);
    }
    Some(table)
}

/// The crowd column: submissions and the dislike share, red when the
/// crowd dislikes the problem (crowd::Stats::bad), yellow when almost
/// nobody does it (crowd::Crowd::obscure), dim when unsynced.
pub fn crowd_cell(ctx: &Ctx, pnum: &str) -> String {
    match ctx.crowd_stats(pnum) {
        None => "[dim]-[/dim]".into(),
        Some(s) => {
            let text = format!(
                "{} {}%",
                crate::crowd::compact(s.submissions),
                s.dislike_pct()
            );
            if s.bad() {
                format!("[red]{text}[/red]")
            } else if ctx.obscure(pnum) {
                format!("[yellow]{text}[/yellow]")
            } else {
                text
            }
        }
    }
}

/// Every rated problem at least GATE_MARGIN below the lowest target, by
/// number, with its title. Drafted and evidenced alike; nothing else
/// filters them.
fn candidates(
    ctx: &Ctx,
    targets: &[&QueueRow],
    ratings: &HashMap<String, f64>,
) -> Vec<(String, String, f64)> {
    let ceiling = targets
        .iter()
        .filter_map(|t| t.rating)
        .fold(f64::INFINITY, f64::min)
        - GATE_MARGIN;
    let mut out: Vec<(String, String, f64)> = ratings
        .iter()
        .filter(|(k, r)| **r <= ceiling && !targets.iter().any(|t| &t.pnum == *k))
        .filter_map(|(k, r)| {
            let title = ctx
                .all_problems()
                .get(k)
                .map(|p| p.title.clone())
                .or_else(|| ctx.meta_title(k))?;
            let banned = ctx.all_problems().get(k).is_some_and(|p| p.banned);
            (!banned && !ctx.paid_only(k)).then(|| (k.clone(), title, *r))
        })
        .collect();
    out.sort_by_key(|(k, _, _)| crate::data::pnum_key(k));
    out
}

/// The target's cached solution file (.prepare_cache/<num>.json), or "".
fn solution(ctx: &Ctx, pnum: &str) -> String {
    crate::pyjson::load(&ctx.root.join(".prepare_cache").join(format!("{pnum}.json")))
        .map(|v| crate::data::value_str(&v["solution"]))
        .unwrap_or_default()
}

/// What the gate model reads: the targets with their solutions, and the
/// candidates below them.
pub fn gate_context(ctx: &Ctx, targets: &[&QueueRow], elo: f64) -> Value {
    let ratings = solve_ratings(ctx);
    let target_json: Vec<Value> = targets
        .iter()
        .map(|t| {
            let p = ctx.all_problems().get(&t.pnum);
            json!({
                "problem": t.pnum,
                "title": t.title,
                "rating": t.rating.map(|r| r.round_ties_even() as i64),
                "after": p.map(|p| p.after.clone()).unwrap_or_default(),
                "solution": solution(ctx, &t.pnum),
            })
        })
        .collect();
    let cand_json: Vec<Value> = candidates(ctx, targets, &ratings)
        .into_iter()
        .map(|(k, title, r)| {
            json!({ "problem": k, "title": title, "rating": r.round_ties_even() as i64 })
        })
        .collect();
    json!({
        "elo": elo.round_ties_even() as i64,
        "targets": target_json,
        "candidates": cand_json,
    })
}

pub struct Gate {
    pub problem: String,
    pub gate: String,
    pub why: String,
}

/// The model's gates, kept only where the target is a target and the gate
/// a candidate it does not already come after.
pub fn valid_gates(reply: &Value, context: &Value) -> Vec<Gate> {
    let targets: Map<String, Value> = context["targets"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|t| (crate::data::value_str(&t["problem"]), t.clone()))
        .collect();
    let cands: HashSet<String> = context["candidates"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|c| crate::data::value_str(&c["problem"]))
        .collect();
    let mut seen: HashSet<(String, String)> = HashSet::new();
    reply["gates"]
        .as_array()
        .into_iter()
        .flatten()
        .filter_map(|g| {
            let problem = crate::data::value_str(&g["problem"]);
            let gate = crate::data::value_str(&g["gate"]);
            let t = targets.get(&problem)?;
            let already = t["after"]
                .as_array()
                .into_iter()
                .flatten()
                .any(|a| crate::data::value_str(a) == gate);
            if !cands.contains(&gate) || already || !seen.insert((problem.clone(), gate.clone())) {
                return None;
            }
            Some(Gate {
                problem,
                gate,
                why: crate::data::value_str(&g["why"]),
            })
        })
        .collect()
}

/// Each target's "after" list with its new gates, sorted. Two gates on one
/// target land in one list: each write replaces the whole list, so a write
/// per gate kept only the last one.
pub fn merged_after(ctx: &Ctx, gates: &[Gate]) -> Vec<(String, Vec<String>)> {
    let mut out: Vec<(String, Vec<String>)> = Vec::new();
    for g in gates {
        let i = match out.iter().position(|(p, _)| *p == g.problem) {
            Some(i) => i,
            None => {
                let after = ctx
                    .all_problems()
                    .get(&g.problem)
                    .map(|p| p.after.clone())
                    .unwrap_or_default();
                out.push((g.problem.clone(), after));
                out.len() - 1
            }
        };
        if !out[i].1.contains(&g.gate) {
            out[i].1.push(g.gate.clone());
        }
    }
    for (_, after) in &mut out {
        after.sort_by_key(|p| crate::data::pnum_key(p));
    }
    out
}

/// Write each target's merged "after" list into graph/problems.json; the
/// number of gates added.
pub fn apply_gates(ctx: &Ctx, gates: &[Gate]) -> std::io::Result<usize> {
    let mut written = 0;
    for (problem, after) in merged_after(ctx, gates) {
        let before = ctx
            .all_problems()
            .get(&problem)
            .map_or(0, |p| p.after.len());
        crate::pyjson::save_problem_entry(&ctx.root, &problem, &json!({ "after": after }))?;
        written += after.len() - before;
    }
    Ok(written)
}
