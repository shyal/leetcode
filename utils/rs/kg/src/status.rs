// Mastery derived from evidence, as kg_lib derives it: the forgetting
// curve (node_status / node_axes), the carry bar and maturity, ownership,
// the graduating ladder, and the small evidence readers (last_solved,
// latest_carrier, owned). Nothing is stored; every answer is a function of
// the records and the day.

use std::collections::{HashMap, HashSet};
use std::fmt;

use chrono::{Duration, NaiveDate};

use crate::ctx::{Ctx, PView};
use crate::data::{assist_weight, is_numeric_id, Nodes, SOLID_WINDOW_DAYS};
use crate::evidence::Evidence;

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug, PartialOrd, Ord)]
pub enum Status {
    Solid,
    Stale,
    Fragile,
    Missing,
}

impl fmt::Display for Status {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            Status::Solid => "SOLID",
            Status::Stale => "STALE",
            Status::Fragile => "FRAGILE",
            Status::Missing => "MISSING",
        })
    }
}

pub use Status::{Fragile as FRAGILE, Missing as MISSING, Solid as SOLID, Stale as STALE};

pub type Statuses = HashMap<String, (Status, Option<NaiveDate>)>;

pub const DEEP_STALE_DAYS: i64 = 2 * SOLID_WINDOW_DAYS;
pub const STARVED_DAYS: i64 = 14;
pub const MATURE_SPACING_DAYS: i64 = 5;
pub const MATURE_CARRY_MEDIUMS: i64 = 2;
pub const BREADTH_FULL: i64 = 3;
pub const CARRIER_COOLDOWN_DAYS: i64 = MATURE_SPACING_DAYS;
pub const GRAD_LADDER: [i64; 3] = [3, 10, 25];
pub const GRAD_LADDER_SPARSE: [i64; 3] = [2, 7, 18];
pub const GRAD_SPARSE_CARRIERS: i64 = 2;

/// The status of a node the statuses table does not carry: Python would
/// raise, and the callers guard against it; MISSING keeps the Rust side
/// from panicking on the same input.
pub fn st(statuses: &Statuses, n: &str) -> (Status, Option<NaiveDate>) {
    statuses.get(n).copied().unwrap_or((MISSING, None))
}

pub fn is_solid(statuses: &Statuses, n: &str) -> bool {
    st(statuses, n).0 == SOLID
}

/// kg_lib._node_curve: (status, last relevant date, recall, memory).
/// kg_lib.node_status over the records dated on or before `cut` (the
/// `seen` table of kg_next.due_on), without building that table: a
/// drill record's first-rep flag is re-read against the cut, since the
/// first rep of a drill inside the subset may be a later record.
pub fn node_status_cut(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    cut: &str,
    today: NaiveDate,
) -> (Status, Option<NaiveDate>) {
    let mut entries: Vec<(NaiveDate, &str, &str, &str)> = Vec::new();
    for e in ev.node_entries(node) {
        let rec = ev.rec(e.idx);
        if rec.date.as_str() > cut {
            continue;
        }
        let fname = ev.fname(e.idx);
        let first = crate::evidence::drill_key(fname).is_some_and(|k| {
            ev.drill_key_order
                .get(&k)
                .and_then(|v| v.iter().find(|i| ev.rec(**i).date.as_str() <= cut))
                == Some(&e.idx)
        });
        let assist = if first { "none" } else { rec.assist_for(node) };
        entries.push((e.date, e.verdict.as_str(), assist, fname));
    }
    curve_of(ctx, node, entries, today).0
}

pub fn node_curve(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    today: NaiveDate,
) -> (Status, Option<NaiveDate>, f64, f64) {
    let entries: Vec<(NaiveDate, &str, &str, &str)> = ev
        .node_entries(node)
        .iter()
        .map(|e| {
            (
                e.date,
                e.verdict.as_str(),
                e.assist.as_str(),
                ev.fname(e.idx),
            )
        })
        .collect();
    let (st, recall, memory) = curve_of(ctx, node, entries, today);
    (st.0, st.1, recall, memory)
}

/// The curve over one node's (date, verdict, assist, fname) entries.
fn curve_of(
    ctx: &Ctx,
    node: &str,
    mut entries: Vec<(NaiveDate, &str, &str, &str)>,
    today: NaiveDate,
) -> ((Status, Option<NaiveDate>), f64, f64) {
    if entries.is_empty() {
        return ((MISSING, None), 0.0, 0.0);
    }
    entries.sort();
    let (last_date, last_verdict, _, _) = *entries.last().unwrap();
    let clean_dates: Vec<NaiveDate> = entries
        .iter()
        .filter(|(_, v, a, _)| *v == "clean" && *a != "learning")
        .map(|(d, _, _, _)| *d)
        .collect();
    if (last_verdict == "struggled" || last_verdict == "avoided")
        && clean_dates.last().is_none_or(|c| *c < last_date)
    {
        return ((FRAGILE, Some(last_date)), 0.0, 0.0);
    }
    if clean_dates.is_empty() {
        return ((FRAGILE, Some(last_date)), 0.0, 0.0);
    }
    let clean_last = *clean_dates.last().unwrap();
    if let Some(cv) = &ctx.curve {
        let cleans = clean_dates.iter().collect::<HashSet<_>>().len() as f64;
        let struggles = entries
            .iter()
            .filter(|(_, v, _, _)| *v == "struggled")
            .count() as f64;
        let mut assisted = 0.0;
        for (_, _, a, _) in &entries {
            assisted += assist_weight(a);
        }
        let cn = cv.conn.get(node).copied().unwrap_or(cv.conn_mean);
        let stability = (cv.a + cv.b * cleans.ln_1p() - cv.c * struggles - cv.d * assisted
            + cv.e * (cn - cv.conn_mean))
            .exp()
            .clamp(7.0, 3650.0);
        let gap = (today - clean_last).num_days().max(0) as f64;
        let memory = (1.0 + gap / stability).powf(-cv.beta);
        let recall = (1.0 - cv.slip) * memory;
        let status = if memory >= cv.target_retention {
            SOLID
        } else {
            STALE
        };
        return ((status, Some(clean_last)), recall, memory);
    }
    if today - clean_last <= Duration::days(SOLID_WINDOW_DAYS) {
        ((SOLID, Some(clean_last)), 1.0, 1.0)
    } else {
        ((STALE, Some(clean_last)), 0.0, 0.0)
    }
}

pub fn node_status(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    today: NaiveDate,
) -> (Status, Option<NaiveDate>) {
    let (s, l, _, _) = node_curve(ctx, node, ev, today);
    (s, l)
}

pub fn all_statuses(ctx: &Ctx, ev: &Evidence, today: NaiveDate) -> Statuses {
    ctx.nodes
        .keys()
        .map(|n| (n.clone(), node_status(ctx, n, ev, today)))
        .collect()
}

/// kg_lib.carry_bar: ("medium", 2), ("real", 1) or ("none", 0).
pub fn carry_bar(ctx: &Ctx, node: &str, pv: &PView) -> (&'static str, i64) {
    pv.bar_of(ctx, node)
}

pub fn bar_of(kinds: &HashSet<String>) -> (&'static str, i64) {
    if kinds.contains("Medium") {
        ("medium", MATURE_CARRY_MEDIUMS)
    } else if !kinds.is_empty() {
        ("real", 1)
    } else {
        ("none", 0)
    }
}

/// kg_lib._at_bar: the distinct real problems among `pnums` that count
/// toward the bar.
pub fn at_bar(ctx: &Ctx, pnums: &HashSet<String>, bar: (&str, i64), pv: &PView) -> HashSet<String> {
    let mut out: HashSet<String> = pnums.iter().filter(|p| is_numeric_id(p)).cloned().collect();
    if bar.0 == "medium" {
        out.retain(|p| {
            let d = ctx.problem_difficulty(p, &pv.map);
            d == "Medium" || d == "Hard"
        });
    }
    out
}

pub fn mature_from(ctx: &Ctx, clean: &[(NaiveDate, String)], bar: (&str, i64), pv: &PView) -> bool {
    if clean.is_empty() {
        return false;
    }
    let mut dates: Vec<NaiveDate> = clean.iter().map(|(d, _)| *d).collect();
    dates.sort();
    if (dates[dates.len() - 1] - dates[0]).num_days() < MATURE_SPACING_DAYS {
        return false;
    }
    if bar.0 == "none" {
        return true;
    }
    let pnums: HashSet<String> = clean.iter().map(|(_, p)| p.clone()).collect();
    at_bar(ctx, &pnums, bar, pv).len() as i64 >= bar.1
}

/// The clean, non-learning reps of a node as (date, problem).
pub fn clean_reps(ev: &Evidence, node: &str) -> Vec<(NaiveDate, String)> {
    ev.node_entries(node)
        .iter()
        .filter(|e| e.verdict == "clean" && e.assist != "learning")
        .map(|e| (e.date, ev.rec(e.idx).problem.clone().unwrap_or_default()))
        .collect()
}

pub fn mature(ctx: &Ctx, node: &str, ev: &Evidence, pv: &PView) -> bool {
    mature_from(ctx, &clean_reps(ev, node), carry_bar(ctx, node, pv), pv)
}

/// kg_lib.immature_nodes: the nodes mature() rejects, memoized per
/// evidence version and bank size.
pub fn immature_nodes(ctx: &Ctx, ev: &Evidence, pv: &PView) -> HashSet<String> {
    let young = |n: &str| !mature_from(ctx, &clean_reps(ev, n), pv.bar_of(ctx, n), pv);
    let cached = ev.cold_cache().immature.clone();
    if let Some((n, mut out)) = cached {
        if n == pv.map.len() {
            // only the nodes touched since can have changed (kg_lib._IMMATURE)
            let dirty: Vec<String> = ev.cold_cache().immature_dirty.drain().collect();
            for node in dirty {
                if !ctx.nodes.contains_key(&node) {
                    continue;
                }
                out.remove(&node);
                if young(&node) {
                    out.insert(node);
                }
            }
            ev.cold_cache().immature = Some((n, out.clone()));
            return out;
        }
    }
    let out: HashSet<String> = ctx.nodes.keys().filter(|n| young(n)).cloned().collect();
    let mut c = ev.cold_cache();
    c.immature = Some((pv.map.len(), out.clone()));
    c.immature_dirty.clear();
    out
}

/// kg_lib.proven_carriers: the distinct real problems that gave the node a
/// clean non-learning rep at its bar; `unaided`, only reps with no help.
pub fn proven_carriers(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    pv: &PView,
    unaided: bool,
) -> HashSet<String> {
    let pnums: HashSet<String> = ev
        .node_entries(node)
        .iter()
        .filter(|e| {
            e.verdict == "clean" && e.assist != "learning" && (!unaided || e.assist == "none")
        })
        .map(|e| ev.rec(e.idx).problem.clone().unwrap_or_default())
        .collect();
    at_bar(ctx, &pnums, carry_bar(ctx, node, pv), pv)
}

pub fn breadth_score(carriers: i64, bar: (&str, i64), any_unaided: bool) -> f64 {
    if !any_unaided {
        return 0.0;
    }
    if bar.0 == "none" {
        return 1.0;
    }
    (1 + carriers.min(BREADTH_FULL)) as f64 / (1 + BREADTH_FULL) as f64
}

#[derive(Clone, Copy, Debug)]
pub struct Axes {
    pub status: Status,
    pub last: Option<NaiveDate>,
    pub memory: f64,
    pub carriers: i64,
    pub breadth: f64,
    pub degree: f64,
}

/// kg_lib.node_axes, cached per (node, day, bank size).
pub fn node_axes(ctx: &Ctx, node: &str, ev: &Evidence, pv: &PView, today: NaiveDate) -> Axes {
    let key = (node.to_string(), today, pv.map.len());
    if let Some(a) = ev.cold_cache().axes.get(&key) {
        return *a;
    }
    let a = node_axes_uncached_(ctx, node, ev, pv, today);
    ev.cold_cache().axes.insert(key, a);
    a
}

fn node_axes_uncached_(ctx: &Ctx, node: &str, ev: &Evidence, pv: &PView, today: NaiveDate) -> Axes {
    let (status, last, _, memory) = node_curve(ctx, node, ev, today);
    let bar = carry_bar(ctx, node, pv);
    let carriers = proven_carriers(ctx, node, ev, pv, true).len() as i64;
    let any_unaided = ev
        .node_entries(node)
        .iter()
        .any(|e| e.verdict == "clean" && e.assist == "none");
    let breadth = breadth_score(carriers, bar, any_unaided);
    Axes {
        status,
        last,
        memory,
        carriers,
        breadth,
        degree: memory.min(breadth),
    }
}

pub fn node_degree(ctx: &Ctx, node: &str, ev: &Evidence, pv: &PView, today: NaiveDate) -> f64 {
    node_axes(ctx, node, ev, pv, today).degree
}

/// kg_lib.owned: the node's most recent clean rep was unaided on this move.
pub fn owned(ev: &Evidence, node: &str) -> bool {
    let mut latest = "";
    let mut ok = false;
    for e in ev.node_entries(node) {
        if e.verdict != "clean" {
            continue;
        }
        let unaided = e.assist == "none";
        let date = ev.rec(e.idx).date.as_str();
        if date > latest {
            latest = date;
            ok = unaided;
        } else if date == latest {
            ok = ok || unaided;
        }
    }
    ok
}

/// kg_lib.graduation_due: (due date, floor days) for a young move's next
/// unaided rep, or None.
pub fn graduation_due(ev: &Evidence, node: &str, carriers: i64) -> Option<(NaiveDate, i64)> {
    let key = (node.to_string(), carriers);
    if let Some(g) = ev.cold_cache().graduation.get(&key) {
        return *g;
    }
    let g = graduation_due_uncached(ev, node, carriers);
    ev.cold_cache().graduation.insert(key, g);
    g
}

fn graduation_due_uncached(ev: &Evidence, node: &str, carriers: i64) -> Option<(NaiveDate, i64)> {
    let rows = ev.node_entries(node);
    let mut unaided: Vec<NaiveDate> = rows
        .iter()
        .filter(|e| e.verdict == "clean" && e.assist == "none")
        .map(|e| e.date)
        .collect();
    unaided.sort();
    unaided.dedup();
    if unaided.is_empty() {
        return None;
    }
    let proof: HashSet<NaiveDate> = rows
        .iter()
        .filter(|e| e.verdict == "clean" && e.assist == "none" && !ev.first_reps.contains(&e.idx))
        .map(|e| e.date)
        .collect();
    let mut days = vec![unaided[0]];
    days.extend(unaided[1..].iter().filter(|d| proof.contains(d)));
    let ladder = if carriers <= GRAD_SPARSE_CARRIERS {
        GRAD_LADDER_SPARSE
    } else {
        GRAD_LADDER
    };
    if unaided
        .windows(2)
        .any(|w| (w[1] - w[0]).num_days() >= ladder[2] && proof.contains(&w[1]))
    {
        return None;
    }
    let floor = ladder[days.len().min(ladder.len()) - 1];
    Some((days[days.len() - 1] + Duration::days(floor), floor))
}

/// kg_lib.last_solved: the latest record date of a problem, "" if none.
pub fn last_solved(ev: &Evidence, pnum: &str) -> String {
    ev.problem_recs(pnum)
        .iter()
        .map(|(d, _, _)| *d)
        .max()
        .unwrap_or("")
        .to_string()
}

/// kg_lib.last_clean_solve: latest all-clean unaided solve date, "" if none.
pub fn last_clean_solve(ev: &Evidence, pnum: &str) -> String {
    ev.problem_recs(pnum)
        .iter()
        .filter(|(_, _, i)| {
            let r = ev.rec(*i);
            r.all_clean() && r.assist_any() == "none"
        })
        .map(|(d, _, _)| *d)
        .max()
        .unwrap_or("")
        .to_string()
}

/// kg_lib.cooled: the last solve is old enough to review again.
pub fn cooled(ev: &Evidence, pnum: &str, today: NaiveDate) -> bool {
    let last = last_solved(ev, pnum);
    last.is_empty() || (today - crate::data::parse_date(&last)).num_days() >= CARRIER_COOLDOWN_DAYS
}

/// kg_lib.latest_carrier: (date, fname, problem) of the node's latest rep.
pub fn latest_carrier(ev: &Evidence, node: &str) -> Option<(NaiveDate, String, Option<String>)> {
    let mut best: Option<(NaiveDate, String, Option<String>)> = None;
    for e in ev.node_entries(node) {
        if best.as_ref().is_none_or(|b| e.date > b.0) {
            best = Some((
                e.date,
                ev.fname(e.idx).to_string(),
                ev.rec(e.idx).problem.clone(),
            ));
        }
    }
    best
}

/// kg_lib.input_tree: transitive prerequisite closure of a walk.
pub fn input_tree(moves: &[String], nodes: &Nodes) -> HashSet<String> {
    let mut seen = HashSet::new();
    let mut stack: Vec<String> = moves.to_vec();
    while let Some(n) = stack.pop() {
        if seen.contains(&n) {
            continue;
        }
        let Some(node) = nodes.get(&n) else {
            continue;
        };
        seen.insert(n);
        stack.extend(node.prereqs.iter().cloned());
    }
    seen
}

/// kg_lib.tree_size: (input-tree size, walk length).
pub fn tree_size(ctx: &Ctx, pnum: &str, pv: &PView) -> (usize, usize) {
    let moves = pv.get(pnum).map(|p| p.moves.as_slice()).unwrap_or(&[]);
    (input_tree(moves, &ctx.nodes).len(), moves.len())
}

pub fn diff_rank(d: &str) -> i64 {
    match d {
        "Easy" => 0,
        "Medium" => 1,
        "Hard" => 2,
        _ => 1,
    }
}

/// kg_lib.gentleness: (difficulty tier, tree size).
pub fn gentleness(ctx: &Ctx, pnum: &str, pv: &PView) -> (i64, (usize, usize)) {
    let tier = pv
        .get(pnum)
        .and_then(|p| p.difficulty.as_deref())
        .map(diff_rank)
        .unwrap_or(1);
    (tier, tree_size(ctx, pnum, pv))
}

/// kg_lib.route_gaps: (gap nodes, gap count, consolidation count).
pub fn route_gaps(
    ctx: &Ctx,
    pnum: &str,
    pv: &PView,
    statuses: &Statuses,
    immature: &HashSet<String>,
) -> (Vec<String>, usize, usize) {
    let p = pv.get(pnum).expect("route_gaps: problem");
    let closure = input_tree(&p.moves, &ctx.nodes);
    let gaps: Vec<String> = closure
        .into_iter()
        .filter(|n| !is_solid(statuses, n) || immature.contains(n))
        .collect();
    let count = gaps.len() + p.unmapped.len();
    let consolidation = gaps.iter().filter(|n| st(statuses, n).0 != MISSING).count();
    (gaps, count, consolidation)
}

/// kg_lib.rank_summits: fewest gaps, then most consolidation, then number.
pub fn rank_summits(
    ctx: &Ctx,
    candidates: &[String],
    pv: &PView,
    statuses: &Statuses,
    immature: &HashSet<String>,
) -> Vec<String> {
    let mut scored: Vec<((usize, i64), (i64, String), String)> = candidates
        .iter()
        .filter(|p| pv.contains(p))
        .map(|p| {
            let (_, count, cons) = route_gaps(ctx, p, pv, statuses, immature);
            ((count, -(cons as i64)), crate::data::pnum_key(p), p.clone())
        })
        .collect();
    scored.sort_by(|a, b| (a.0, &a.1).cmp(&(b.0, &b.1)));
    scored.into_iter().map(|(_, _, p)| p).collect()
}

/// kg_lib.node_conn: log2 carrier count per node.
pub fn node_conn(pv: &PView, ctx: &Ctx) -> HashMap<String, f64> {
    pv.carrier_counts(ctx)
        .iter()
        .map(|(n, c)| (n.clone(), ((1 + c) as f64).log2()))
        .collect()
}

/// kg_lib.node_curve_recall / current_recall: predicted recall per node he
/// has met (distinct clean days, learning included, as the Python counts).
pub fn current_recall(ctx: &Ctx, ev: &Evidence, today: NaiveDate) -> HashMap<String, f64> {
    let Some(cv) = &ctx.curve else {
        return HashMap::new();
    };
    let mut out = HashMap::new();
    for nid in ctx.nodes.keys() {
        let (status, last) = node_status(ctx, nid, ev, today);
        if status == MISSING {
            continue;
        }
        let Some(last) = last else { continue };
        let cleans = ev
            .node_entries(nid)
            .iter()
            .filter(|e| e.verdict == "clean")
            .map(|e| e.date)
            .collect::<HashSet<_>>()
            .len() as f64;
        if cleans == 0.0 {
            continue;
        }
        let s = (cv.a + cv.b * cleans.ln_1p()).exp().clamp(7.0, 3650.0);
        let r = (1.0 + (today - last).num_days() as f64 / s).powf(-cv.beta);
        out.insert(nid.clone(), r);
    }
    out
}
