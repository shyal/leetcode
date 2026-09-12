// The problem bank as the picker reads it: which problems can carry a
// move (carriers_for, proving_carriers), the "after" holds (held_behind,
// warm, gates), and the drafted tier (unlocks, predicted_carrier,
// drafted_in_reach) over the walks of graph/problems.json. Mirrors the
// middle of utils/kg/kg_lib.py; the numpy matrix there is a list of walks
// here.

use std::collections::{HashMap, HashSet};

use chrono::NaiveDate;

use crate::ctx::{Ctx, PView};
use crate::data::{is_numeric_id, parse_date, pnum_key, Problem, Problems, SOLID_WINDOW_DAYS};
use crate::drills::{drill_clean, drill_warm, latest_drill_rep, node_drill_hold};
use crate::evidence::Evidence;
use crate::status::{
    carry_bar, diff_rank, input_tree, is_solid, last_clean_solve, owned, Statuses, MISSING, SOLID,
    STALE,
};

pub const CONN_MASS_CAP: i64 = 30;

/// kg_lib.walk_nodes: every node a problem's solution might walk.
pub fn walk_nodes(p: &Problem) -> Vec<String> {
    let mut out = p.moves.clone();
    for alt in &p.alt_walks {
        out.extend(alt.iter().cloned());
    }
    for w in &p.walks {
        out.extend(w.moves.iter().cloned());
    }
    out
}

/// kg_lib.warm: whether an "after" id is owned, by the bar its kind
/// carries. None for an id nothing carries.
pub fn warm(
    ctx: &Ctx,
    vid: &str,
    problems: &PView,
    ev: &Evidence,
    today: NaiveDate,
    early: bool,
) -> Option<bool> {
    match ctx.vertex_kind(vid, &problems.map)? {
        "problem" => {
            let last = last_clean_solve(ev, vid);
            Some(!last.is_empty() && (today - parse_date(&last)).num_days() <= SOLID_WINDOW_DAYS)
        }
        "drill" => {
            let path = ctx.drill_path(vid);
            match path {
                None => Some(false),
                Some(p) => Some(if early {
                    drill_clean(ctx, &p, ev)
                } else {
                    drill_warm(ctx, &p, ev, today)
                }),
            }
        }
        "node" => Some(owned(ev, vid)),
        _ => None,
    }
}

/// kg_lib.held_behind: the predecessor this problem waits for, or None.
pub fn held_behind(
    ctx: &Ctx,
    pnum: &str,
    problems: &PView,
    ev: &Evidence,
    today: NaiveDate,
) -> Option<String> {
    let entry = problems.get(pnum).or_else(|| ctx.ro.get(pnum));
    let entry = entry?;
    for pred in &entry.after {
        let pred_entry = problems.get(pred).or_else(|| ctx.ro.get(pred));
        let unservable = match pred_entry {
            Some(p) => ctx.unservable(pred, p),
            None => ctx.paid_only(pred),
        };
        if unservable {
            continue;
        }
        if warm(ctx, pred, problems, ev, today, false) == Some(false) {
            return Some(pred.clone());
        }
    }
    let mut seen = HashSet::new();
    for node in walk_nodes(entry) {
        if !seen.insert(node.clone()) {
            continue;
        }
        if let Some(held) = node_drill_hold(ctx, &node, ev, today) {
            return Some(held);
        }
    }
    None
}

/// kg_lib.gates: the problems and drills whose "after" names `vid`.
pub fn gates(ctx: &Ctx, vid: &str, problems: &Problems) -> Vec<String> {
    let mut held: Vec<String> = problems
        .iter()
        .filter(|(_, p)| p.after.iter().any(|a| a == vid))
        .map(|(k, _)| k.clone())
        .collect();
    held.sort_by_key(|p| pnum_key(p));
    let mut drills: Vec<String> = ctx
        .drills
        .iter()
        .filter(|(_, d)| d.after.iter().any(|a| a == vid))
        .map(|(i, _)| i.clone())
        .collect();
    drills.sort_by_key(|p| pnum_key(p));
    held.extend(drills);
    held
}

/// kg_lib.vertex_status: SOLID when warm, STALE with a rep, MISSING else.
pub fn vertex_status(
    ctx: &Ctx,
    vid: &str,
    problems: &PView,
    ev: &Evidence,
    today: NaiveDate,
) -> crate::status::Status {
    if warm(ctx, vid, problems, ev, today, false) == Some(true) {
        return SOLID;
    }
    match ctx.vertex_kind(vid, &problems.map) {
        Some("problem") if !ev.problem_recs(vid).is_empty() => STALE,
        Some("drill")
            if ctx
                .drill_path(vid)
                .is_some_and(|p| latest_drill_rep(ctx, &p, ev).is_some()) =>
        {
            STALE
        }
        _ => MISSING,
    }
}

/// kg_lib.carriers_for: problems with the target whose every other move is
/// SOLID, not Hard, servable, and not held behind a predecessor.
pub fn carriers_for(
    ctx: &Ctx,
    target: &str,
    pv: &PView,
    statuses: &Statuses,
    ev: &Evidence,
    today: NaiveDate,
) -> Vec<String> {
    let mut found = Vec::new();
    for (pnum, p) in &pv.map {
        if ctx.unservable(pnum, p)
            || p.is_hard()
            || !p.moves.iter().any(|m| m == target)
            || !p.moves.iter().all(|m| ctx.nodes.contains_key(m))
        {
            continue;
        }
        if p.moves.iter().all(|m| m == target || is_solid(statuses, m))
            && held_behind(ctx, pnum, pv, ev, today).is_none()
        {
            found.push(pnum.clone());
        }
    }
    found
}

/// kg_lib.proving_carriers: real, non-Hard problems carrying the target in
/// ANY recorded walk whose every other move is SOLID, at the node's bar.
pub fn proving_carriers(
    ctx: &Ctx,
    target: &str,
    pv: &PView,
    statuses: &Statuses,
    ev: &Evidence,
    today: NaiveDate,
) -> Vec<String> {
    let (kind, _) = carry_bar(ctx, target, pv);
    let mut found = Vec::new();
    let table = pv.walks_carrying(ctx);
    for (pnum, walks) in table.get(target).map(Vec::as_slice).unwrap_or(&[]) {
        let p = pv.get(pnum).unwrap();
        if kind == "medium" && p.difficulty() != "Medium" {
            continue;
        }
        let ok = walks.iter().any(|walk| {
            walk.iter().all(|m| ctx.nodes.contains_key(m))
                && walk.iter().all(|m| m == target || is_solid(statuses, m))
        });
        if !ok {
            continue;
        }
        if held_behind(ctx, pnum, pv, ev, today).is_some() {
            continue;
        }
        found.push(pnum.clone());
    }
    found
}

/// kg_lib.dodgeable: a recorded alt walk avoids the target.
pub fn dodgeable(pv: &PView, pnum: &str, target: &str) -> bool {
    pv.get(pnum)
        .is_some_and(|p| p.alt_walks.iter().any(|w| !w.iter().any(|m| m == target)))
}

// ---- the drafted tier ---------------------------------------------------

/// kg_lib._DraftMatrix: the drafted walks as rows over the node ids.
pub struct DraftWalk {
    pub prob: usize,
    pub known: Vec<usize>,
    pub unknown: usize,
    pub missing: bool,
    pub moves: Vec<String>,
}

pub struct DraftMatrix {
    pub node_ids: Vec<String>,
    pub index: HashMap<String, usize>,
    pub problems: Vec<String>,
    pub walks: Vec<DraftWalk>,
    pub diff: Vec<String>,
    pub acc: Vec<f64>,
    pub pkey: Vec<i64>,
}

impl DraftMatrix {
    pub fn build(ctx: &Ctx, predicted: &Problems, node_ids: Vec<String>) -> DraftMatrix {
        let index: HashMap<String, usize> = node_ids
            .iter()
            .enumerate()
            .map(|(i, n)| (n.clone(), i))
            .collect();
        let mut problems = Vec::new();
        let mut walks = Vec::new();
        for (num, entry) in predicted {
            let pi = problems.len();
            problems.push(num.clone());
            for w in &entry.walks {
                if w.moves.is_empty() {
                    continue;
                }
                let mut known: Vec<usize> = Vec::new();
                let mut unknown = 0;
                for m in &w.moves {
                    match index.get(m) {
                        Some(&i) => {
                            if !known.contains(&i) {
                                known.push(i);
                            }
                        }
                        None => unknown += 1,
                    }
                }
                known.sort();
                walks.push(DraftWalk {
                    prob: pi,
                    known,
                    unknown,
                    missing: w.missing,
                    moves: w.moves.clone(),
                });
            }
        }
        let diff = problems.iter().map(|n| ctx.meta_difficulty(n)).collect();
        let acc = problems.iter().map(|n| ctx.acceptance(n)).collect();
        let pkey = problems.iter().map(|n| pnum_key(n).0).collect();
        DraftMatrix {
            node_ids,
            index,
            problems,
            walks,
            diff,
            acc,
            pkey,
        }
    }

    /// The problems not in the evidenced view: unsolved, unmapped.
    fn live(&self, pv: &PView) -> Vec<bool> {
        self.problems.iter().map(|n| !pv.contains(n)).collect()
    }

    fn counts_vec(&self, pv: &PView, ctx: &Ctx) -> Vec<f64> {
        let counts = pv.carrier_counts(ctx);
        self.node_ids
            .iter()
            .map(|n| counts.get(n).copied().unwrap_or(0) as f64)
            .collect()
    }
}

fn sorted_node_ids(statuses: &Statuses) -> Vec<String> {
    let mut ids: Vec<String> = statuses.keys().cloned().collect();
    ids.sort();
    ids
}

/// kg_lib.unlocks: node -> how many unsolved drafted problems are blocked
/// only by it.
pub fn unlocks(
    ctx: &Ctx,
    statuses: &Statuses,
    pv: &PView,
    immature: &HashSet<String>,
) -> HashMap<String, i64> {
    let dm = ctx.draft_matrix(sorted_node_ids(statuses));
    let reach: Vec<bool> = dm
        .node_ids
        .iter()
        .map(|n| is_solid(statuses, n) && !immature.contains(n))
        .collect();
    let gaps: Vec<usize> = dm
        .walks
        .iter()
        .map(|w| w.known.iter().filter(|&&i| !reach[i]).count() + w.unknown)
        .collect();
    let live = dm.live(pv);
    let mut in_reach = vec![false; dm.problems.len()];
    for (wi, w) in dm.walks.iter().enumerate() {
        if !w.missing && gaps[wi] == 0 {
            in_reach[w.prob] = true;
        }
    }
    let mut pairs: HashSet<(usize, usize)> = HashSet::new();
    for (wi, w) in dm.walks.iter().enumerate() {
        if !w.missing && gaps[wi] == 1 && w.unknown == 0 && live[w.prob] && !in_reach[w.prob] {
            let blocker = *w.known.iter().find(|&&i| !reach[i]).unwrap();
            pairs.insert((w.prob, blocker));
        }
    }
    let mut counts: HashMap<String, i64> = HashMap::new();
    for (_, b) in pairs {
        *counts.entry(dm.node_ids[b].clone()).or_insert(0) += 1;
    }
    counts
}

/// The first qualifying walk of each problem, in file order.
fn first_walk_per_problem(dm: &DraftMatrix, sel: &[bool]) -> Vec<usize> {
    let mut seen: HashSet<usize> = HashSet::new();
    let mut out = Vec::new();
    for (wi, w) in dm.walks.iter().enumerate() {
        if sel[wi] && seen.insert(w.prob) {
            out.push(wi);
        }
    }
    out.sort_by_key(|&wi| dm.walks[wi].prob);
    out
}

/// kg_lib.predicted_carrier: the best drafted problem whose walk needs
/// nothing but the target, promoted in memory as (pnum, entry).
pub fn predicted_carrier(
    ctx: &Ctx,
    target: &str,
    pv: &PView,
    statuses: &Statuses,
    ev: &Evidence,
    skip: &HashSet<String>,
    difficulties: &[&str],
    today: NaiveDate,
) -> Option<(String, Problem)> {
    let dm = ctx.draft_matrix(sorted_node_ids(statuses));
    let t = *dm.index.get(target)?;
    let solid: Vec<bool> = dm.node_ids.iter().map(|n| is_solid(statuses, n)).collect();
    let live = dm.live(pv);
    let sel: Vec<bool> = dm
        .walks
        .iter()
        .map(|w| {
            let gaps = w.known.iter().filter(|&&i| i != t && !solid[i]).count() + w.unknown;
            w.known.contains(&t) && !w.missing && gaps == 0 && live[w.prob]
        })
        .collect();
    let walks = first_walk_per_problem(&dm, &sel);
    if walks.is_empty() {
        return None;
    }
    let counts = dm.counts_vec(pv, ctx);
    let predicted = &ctx.predicted_view;
    let mut best: Vec<(String, Vec<String>, String, i64)> = Vec::new();
    for wi in walks {
        let w = &dm.walks[wi];
        let mass = w
            .known
            .iter()
            .filter(|&&i| i != t)
            .map(|&i| counts[i])
            .fold(f64::INFINITY, f64::min);
        let mass = if mass.is_finite() {
            mass
        } else {
            CONN_MASS_CAP as f64
        };
        let num = &dm.problems[w.prob];
        let diff = &dm.diff[w.prob];
        if skip.contains(num)
            || !(diff == "Easy" || diff == "Medium")
            || !difficulties.contains(&diff.as_str())
        {
            continue;
        }
        if held_behind(ctx, num, predicted, ev, today).is_some() {
            continue;
        }
        best.push((
            num.clone(),
            w.moves.clone(),
            diff.clone(),
            (mass as i64).min(CONN_MASS_CAP),
        ));
    }
    if best.is_empty() {
        return None;
    }
    best.sort_by(|a, b| {
        let ka = (
            diff_rank(&a.2),
            -a.3,
            (input_tree(&a.1, &ctx.nodes).len(), a.1.len()),
        );
        let kb = (
            diff_rank(&b.2),
            -b.3,
            (input_tree(&b.1, &ctx.nodes).len(), b.1.len()),
        );
        ka.cmp(&kb)
            .then_with(|| {
                ctx.acceptance(&b.0)
                    .partial_cmp(&ctx.acceptance(&a.0))
                    .unwrap()
            })
            .then_with(|| pnum_key(&a.0).cmp(&pnum_key(&b.0)))
    });
    let (num, moves, diff, _) = &best[0];
    let title = ctx
        .predicted
        .get(num)
        .map(|p| p.title.clone())
        .filter(|t| !t.is_empty())
        .or_else(|| ctx.meta_title(num))
        .unwrap_or_else(|| format!("problem {num}"));
    Some((
        num.clone(),
        Problem {
            title,
            difficulty: Some(diff.clone()),
            moves: moves.clone(),
            predicted: true,
            ..Default::default()
        },
    ))
}

/// kg_lib.drafted_in_reach: unsolved drafted problems whose walk is
/// entirely in reach, `first` difficulty ahead, Easy last.
pub fn drafted_in_reach(
    ctx: &Ctx,
    pv: &PView,
    statuses: &Statuses,
    immature: &HashSet<String>,
    ev: &Evidence,
    skip: &HashSet<String>,
    first: &str,
    limit: usize,
    today: NaiveDate,
) -> Vec<(String, Problem)> {
    let dm = ctx.draft_matrix(sorted_node_ids(statuses));
    let reach: Vec<bool> = dm
        .node_ids
        .iter()
        .map(|n| is_solid(statuses, n) && !immature.contains(n))
        .collect();
    let live = dm.live(pv);
    let sel: Vec<bool> = dm
        .walks
        .iter()
        .map(|w| {
            let gaps = w.known.iter().filter(|&&i| !reach[i]).count() + w.unknown;
            !w.missing && gaps == 0 && live[w.prob]
        })
        .collect();
    let walks = first_walk_per_problem(&dm, &sel);
    if walks.is_empty() {
        return vec![];
    }
    let counts = dm.counts_vec(pv, ctx);
    let rank_of = |d: &str| -> i64 {
        if d == first {
            2
        } else {
            match d {
                "Easy" => 0,
                "Medium" | "Hard" => 1,
                _ => -1,
            }
        }
    };
    struct Row {
        wi: usize,
        mass: f64,
        rank: i64,
    }
    let mut rows: Vec<Row> = walks
        .iter()
        .map(|&wi| {
            let w = &dm.walks[wi];
            let mass = w
                .known
                .iter()
                .map(|&i| counts[i])
                .fold(f64::INFINITY, f64::min);
            let mass = if mass.is_finite() {
                mass
            } else {
                CONN_MASS_CAP as f64
            }
            .min(CONN_MASS_CAP as f64);
            Row {
                wi,
                mass,
                rank: rank_of(&dm.diff[w.prob]),
            }
        })
        .filter(|r| r.rank >= 0)
        .collect();
    // np.lexsort((pkey, -acc, -mass, -rank)): rank desc, mass desc, acc
    // desc, pkey asc, stable
    rows.sort_by(|a, b| {
        let pa = dm.walks[a.wi].prob;
        let pb = dm.walks[b.wi].prob;
        b.rank
            .cmp(&a.rank)
            .then_with(|| b.mass.partial_cmp(&a.mass).unwrap())
            .then_with(|| dm.acc[pb].partial_cmp(&dm.acc[pa]).unwrap())
            .then_with(|| dm.pkey[pa].cmp(&dm.pkey[pb]))
    });
    let predicted = &ctx.predicted_view;
    let mut out = Vec::new();
    for r in rows {
        let w = &dm.walks[r.wi];
        let num = &dm.problems[w.prob];
        if skip.contains(num) || held_behind(ctx, num, predicted, ev, today).is_some() {
            continue;
        }
        let title = ctx
            .predicted
            .get(num)
            .map(|p| p.title.clone())
            .filter(|t| !t.is_empty())
            .or_else(|| ctx.meta_title(num))
            .unwrap_or_else(|| format!("problem {num}"));
        out.push((
            num.clone(),
            Problem {
                title,
                difficulty: Some(dm.diff[w.prob].clone()),
                moves: w.moves.clone(),
                predicted: true,
                ..Default::default()
            },
        ));
        if out.len() >= limit {
            break;
        }
    }
    out
}

/// kg_lib.carrier_counts over any table (the RO one for due_drill).
pub fn carrier_counts(problems: &Problems) -> HashMap<String, i64> {
    let mut counts = HashMap::new();
    for p in problems.values() {
        for m in &p.moves {
            *counts.entry(m.clone()).or_insert(0) += 1;
        }
    }
    counts
}

pub fn numeric_problems(pv: &PView) -> Vec<String> {
    pv.keys().into_iter().filter(|k| is_numeric_id(k)).collect()
}
