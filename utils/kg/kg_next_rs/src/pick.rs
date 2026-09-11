// The picker: utils/kg/kg_next's pick() and the functions around it,
// rule for rule. The frontier is one sorted list of due moves and one
// way to serve a move (its own drill, the drill opening its hold, a
// carrier, a drafted carrier, the predecessor its carriers wait on); the
// rules are only the order of the list. See the header of kg_next for
// the rules and the dates they were settled on.

use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::path::PathBuf;

use chrono::{Duration, NaiveDate};

use crate::bank::{
    carriers_for, dodgeable, drafted_in_reach, held_behind, predicted_carrier, proving_carriers,
    unlocks, warm,
};
use crate::clock::{due_problems, last_attempt};
use crate::ctx::{Ctx, PView};
use crate::data::{is_numeric_id, max_asleep, parse_date, pnum_key, Problem, Rec};
use crate::drills::{
    anki, anki_due, anki_frontier, cold_drill, drill_capped, drill_gated, drill_held, drills_left,
    due_drill, group_caps, group_reps, last_drilled,
};
use crate::evidence::Evidence;
use crate::model::{problem_solve_p, solve_model, solve_ratings, target_pass_rate};
use crate::recog;
use crate::status::{
    all_statuses, cooled, current_recall, gentleness, graduation_due, immature_nodes, input_tree,
    is_solid, last_solved, latest_carrier, node_degree, node_status, owned, rank_summits,
    route_gaps, st, tree_size, Status, Statuses, CARRIER_COOLDOWN_DAYS, DEEP_STALE_DAYS, FRAGILE,
    MISSING, SOLID, STALE, STARVED_DAYS,
};

pub const WARMUP_COOLDOWN_DAYS: i64 = 14;

/// KG_TRACE=2: microseconds spent per phase of pick(), summed over the run.
pub fn ptrace(label: &'static str, t: std::time::Instant) {
    use std::cell::RefCell;
    use std::collections::BTreeMap;
    thread_local! { static ACC: RefCell<BTreeMap<&'static str, f64>> = const { RefCell::new(BTreeMap::new()) }; }
    use std::sync::OnceLock;
    static ON: OnceLock<bool> = OnceLock::new();
    if !*ON.get_or_init(|| std::env::var("KG_TRACE").as_deref() == Ok("2")) {
        return;
    }
    ACC.with(|a| {
        *a.borrow_mut().entry(label).or_insert(0.0) += t.elapsed().as_secs_f64() * 1000.0;
        if label == "dump" {
            for (k, v) in a.borrow().iter() {
                eprintln!("  pick phase {k:<14} {v:8.1} ms");
            }
        }
    });
}
pub const CLASSICS: [&str; 23] = [
    "4", "23", "25", "32", "41", "42", "76", "84", "85", "124", "127", "212", "224", "239", "295",
    "297", "460", "502", "815", "895", "968", "1235", "2402",
];

#[derive(Clone, Debug, PartialEq)]
pub struct Choice {
    pub target: String,
    pub status: Status,
    pub pnum: String,
    pub reason: String,
}

impl Choice {
    fn new(target: &str, status: Status, pnum: &str, reason: String) -> Choice {
        Choice {
            target: target.to_string(),
            status,
            pnum: pnum.to_string(),
            reason,
        }
    }

    pub fn is_drill(&self) -> bool {
        self.pnum.starts_with("drill:")
    }
}

#[derive(Clone, Default)]
pub struct PickArgs {
    pub asleep: Vec<String>,
    pub woken: Vec<String>,
    pub exclude: HashSet<String>,
    pub session_start: bool,
    pub group: Option<String>,
    pub cram: bool,
    pub early: bool,
    pub assisted: bool,
}

fn warmup_hot(ev: &Evidence, pnum: &str, today: NaiveDate) -> bool {
    let last = last_solved(ev, pnum);
    if last.is_empty() {
        return false;
    }
    (today - parse_date(&last)).num_days() < WARMUP_COOLDOWN_DAYS
}

/// kg_next.trivial_easies: the gentlest all-SOLID easies not done in the
/// last WARMUP_COOLDOWN_DAYS.
pub fn trivial_easies(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    today: NaiveDate,
) -> Vec<String> {
    let mut cands: Vec<(i64, (usize, usize), f64, String, String)> = Vec::new();
    for (pnum, p) in &pv.map {
        if ctx.unservable(pnum, p) || p.difficulty() != "Easy" || p.moves.is_empty() {
            continue;
        }
        if !p
            .moves
            .iter()
            .all(|m| ctx.nodes.contains_key(m) && is_solid(statuses, m))
        {
            continue;
        }
        cands.push((
            warmup_hot(ev, pnum, today) as i64,
            tree_size(ctx, pnum, pv),
            -ctx.acceptance(pnum),
            last_solved(ev, pnum),
            pnum.clone(),
        ));
    }
    cands.sort_by(|a, b| {
        (a.0, a.1)
            .cmp(&(b.0, b.1))
            .then_with(|| a.2.partial_cmp(&b.2).unwrap())
            .then_with(|| (&a.3, &a.4).cmp(&(&b.3, &b.4)))
    });
    cands.into_iter().map(|c| c.4).collect()
}

/// kg_next.review_queue: due problems minus the unservable ones.
pub fn review_queue(
    ctx: &Ctx,
    ev: &Evidence,
    pv: &PView,
    today: NaiveDate,
) -> Vec<(String, NaiveDate, i64)> {
    due_problems(ev, today, Some(pv))
        .into_iter()
        .filter(|(p, _, _)| !ctx.unservable(p, pv.get(p).unwrap()))
        .collect()
}

/// kg_next.drill_clock_reason.
pub fn drill_clock_reason(
    ctx: &Ctx,
    path: Option<&PathBuf>,
    ev: &Evidence,
    today: NaiveDate,
) -> String {
    let due = path.and_then(|p| anki_due(ctx, p, ev));
    match due {
        None => "drill never done - on its own clock".to_string(),
        Some((d, interval)) => {
            let late = (today - d).num_days();
            let mut s = format!("drill due on its own clock - {interval}d interval");
            if late > 0 {
                s.push_str(&format!(", {late}d overdue"));
            }
            s
        }
    }
}

/// kg_next.counted_toward_bar: the problem already gave the target a
/// clean rep.
pub fn counted_toward_bar(ev: &Evidence, pnum: &str, target: &str) -> bool {
    ev.node_entries(target)
        .iter()
        .any(|e| e.verdict == "clean" && ev.rec(e.idx).problem.as_deref() == Some(pnum))
}

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Kind {
    Fragile,
    Floor,
    Drill,
    Stale,
    Thin,
    Missing,
}

fn order(k: Kind) -> i64 {
    match k {
        Kind::Fragile => 0,
        Kind::Floor => 1,
        Kind::Drill => 2,
        Kind::Stale => 3,
        Kind::Thin => 4,
        Kind::Missing => 5,
    }
}

const PROMOTED: &str = "no unsolved mapped carrier - promoted a drafted one (predicted walk)";

struct Picker<'a> {
    ctx: &'a Ctx,
    pv: &'a RefCell<PView>,
    ev: &'a Evidence,
    statuses: &'a Statuses,
    args: &'a PickArgs,
    today: NaiveDate,
    cram: bool,
    early: bool,
    assisted: bool,
    solved_ever: HashSet<String>,
    capped: HashSet<String>,
    immature: HashSet<String>,
    degrees: HashMap<String, f64>,
    carr: HashMap<String, i64>,
    unl: HashMap<String, i64>,
    gain: HashMap<String, i64>,
    dodged: HashMap<String, String>,
    under: HashMap<String, String>,
    model: RefCell<
        Option<(
            HashMap<String, f64>,
            Option<HashMap<String, f64>>,
            HashMap<String, f64>,
        )>,
    >,
    // pure per pick: memoized (the Python recomputes them; the answers
    // are the same, only sooner)
    due_memo: RefCell<HashMap<String, Option<String>>>,
    kind_memo: RefCell<HashMap<String, Option<Kind>>>,
    opener_memo: RefCell<HashMap<String, Option<(String, String)>>>,
}

impl<'a> Picker<'a> {
    fn in_scope(&self, n: &str) -> bool {
        match &self.args.group {
            Some(g) => self.ctx.group_of(n) == Some(g.as_str()),
            None => {
                !self.capped.contains(self.ctx.group_of(n).unwrap_or(""))
                    || self.ctx.group_of(n).is_none()
            }
        }
    }

    fn group_capped(&self, n: &str) -> bool {
        self.ctx
            .group_of(n)
            .is_some_and(|g| self.capped.contains(g))
    }

    fn status(&self, n: &str) -> (Status, Option<NaiveDate>) {
        st(self.statuses, n)
    }

    fn skip_set(&self) -> HashSet<String> {
        let mut s: HashSet<String> = self.args.asleep.iter().cloned().collect();
        s.extend(self.args.exclude.iter().cloned());
        s.extend(self.solved_ever.iter().cloned());
        s
    }

    /// The drill pseudo-pick for a node, or None if none is due.
    fn due(&self, target: &str) -> Option<String> {
        if let Some(d) = self.due_memo.borrow().get(target) {
            return d.clone();
        }
        let d = self.due_uncached(target);
        self.due_memo
            .borrow_mut()
            .insert(target.to_string(), d.clone());
        d
    }

    fn due_uncached(&self, target: &str) -> Option<String> {
        if !self.cram && drill_held(self.ctx, target, self.statuses, self.ev, &HashSet::new()) {
            return None;
        }
        if self.early
            && !self.assisted
            && self.ctx.prereqs(target).iter().any(|p| {
                self.in_scope(p)
                    && self.ctx.has_drill_bank(p)
                    && drills_left(self.ctx, p, self.ev, true)
            })
        {
            return None;
        }
        let drill_id = format!("drill:{target}");
        if self.args.exclude.contains(&drill_id) {
            return None;
        }
        let path = due_drill(
            self.ctx,
            target,
            self.ev,
            self.today,
            self.early,
            self.assisted,
        )
        .or_else(|| {
            // once a day: a drill done today with a hint is still cold, and
            // the same file was served straight back (2026-09-11, No
            // Repeat Siblings right after its rep)
            cold_drill(self.ctx, target, self.ev, self.today, true).filter(|p| {
                last_drilled(self.ctx, p, self.ev).as_str()
                    < self.today.format("%Y-%m-%d").to_string().as_str()
            })
        });
        match path {
            Some(p) if !drill_capped(self.ctx, &p, self.ev, self.today) => Some(drill_id),
            _ => None,
        }
    }

    /// The frontier mover: promote a drafted carrier when every mapped one
    /// is solved.
    fn promote(&self, target: &str, unsolved: &[String]) -> Option<String> {
        if !unsolved.is_empty() {
            return None;
        }
        let promo = {
            let pv = self.pv.borrow();
            predicted_carrier(
                self.ctx,
                target,
                &pv,
                self.statuses,
                self.ev,
                &self.skip_set(),
                &["Easy", "Medium"],
                self.today,
            )
        };
        let (num, entry) = promo?;
        self.pv.borrow_mut().insert(num.clone(), entry);
        Some(num)
    }

    /// Serve the root of the "after" chain no carrier of target can pass.
    fn unhold(&self, target: &str) -> Option<Choice> {
        let keys = self.pv.borrow().keys_sorted();
        for pnum in keys {
            let pv = self.pv.borrow();
            let p = pv.get(&pnum).unwrap().clone();
            let moves = &p.moves;
            if !moves.iter().any(|m| m == target)
                || self.ctx.unservable(&pnum, &p)
                || p.is_hard()
                || !moves.iter().all(|m| self.ctx.nodes.contains_key(m))
                || moves
                    .iter()
                    .any(|m| m != target && !is_solid(self.statuses, m))
            {
                continue;
            }
            let mut pred = held_behind(self.ctx, &pnum, &pv, self.ev, self.today);
            let mut seen: HashSet<String> = HashSet::new();
            while let Some(pr) = pred.clone() {
                if seen.contains(&pr) {
                    break;
                }
                seen.insert(pr.clone());
                let kind = self.ctx.vertex_kind(&pr, &pv.map);
                if kind == Some("problem") {
                    if let Some(up) = held_behind(self.ctx, &pr, &pv, self.ev, self.today) {
                        pred = Some(up);
                        continue;
                    }
                    let pm = pv.get(&pr).map(|p| p.moves.clone()).unwrap_or_default();
                    let hard = pv.get(&pr).is_some_and(|p| p.is_hard());
                    if hard
                        || self.args.asleep.contains(&pr)
                        || self.args.exclude.contains(&pr)
                        || !cooled(self.ev, &pr, self.today)
                        || pm.is_empty()
                        || !pm.iter().all(|m| self.ctx.nodes.contains_key(m))
                    {
                        break;
                    }
                    let t2 = pm
                        .iter()
                        .find(|m| !is_solid(self.statuses, m))
                        .unwrap_or(&pm[0])
                        .clone();
                    return Some(Choice::new(
                        &t2,
                        self.status(&t2).0,
                        &pr,
                        format!("{pnum} carries {target} but waits on {pr} - {pr} first"),
                    ));
                }
                let mut node: Option<String> = Some(pr.clone());
                if kind == Some("drill") {
                    let path = self.ctx.drill_path(&pr);
                    node = path.as_ref().and_then(|p| {
                        p.parent()
                            .and_then(|d| d.file_name())
                            .and_then(|s| s.to_str())
                            .map(String::from)
                    });
                    let up = path.as_ref().and_then(|p| {
                        self.ctx.drill_after(p).into_iter().find(|a| {
                            warm(self.ctx, a, &pv, self.ev, self.today, false) == Some(false)
                        })
                    });
                    if let Some(up) = up {
                        let node_due = node.as_deref().is_some_and(|n| n == target)
                            || node.as_deref().is_none_or(|n| self.due(n).is_none());
                        if node_due {
                            pred = Some(up);
                            continue;
                        }
                    }
                }
                if let Some(n) = &node {
                    if self.ctx.nodes.contains_key(n) {
                        if let Some(d) = self.due(n) {
                            let why = if n == target {
                                format!("every carrier of {target} waits on {pr} - drill first")
                            } else {
                                format!(
                                    "{pnum} carries {target} but waits on {pr} - drill {n} first"
                                )
                            };
                            return Some(Choice::new(n, self.status(n).0, &d, why));
                        }
                    }
                }
                break;
            }
        }
        None
    }

    fn ladder(&self, n: &str) -> Option<(NaiveDate, i64)> {
        graduation_due(self.ev, n, self.carr.get(n).copied().unwrap_or(0))
    }

    fn floor(&self, n: &str) -> Option<(NaiveDate, i64)> {
        self.ladder(n).filter(|(d, _)| *d <= self.today)
    }

    fn kind(&self, n: &str) -> Option<Kind> {
        if let Some(k) = self.kind_memo.borrow().get(n) {
            return *k;
        }
        let k = self.kind_uncached(n);
        self.kind_memo.borrow_mut().insert(n.to_string(), k);
        k
    }

    fn kind_uncached(&self, n: &str) -> Option<Kind> {
        let status = self.status(n).0;
        if status == MISSING {
            return if self
                .ctx
                .prereqs(n)
                .iter()
                .all(|p| is_solid(self.statuses, p))
            {
                Some(Kind::Missing)
            } else {
                None
            };
        }
        if status == SOLID {
            if self.floor(n).is_some() {
                return Some(Kind::Floor);
            }
            if anki() && self.due(n).is_some() {
                return Some(Kind::Drill);
            }
            return if self.immature.contains(n) && self.ladder(n).is_none() {
                Some(Kind::Thin)
            } else {
                None
            };
        }
        Some(match status {
            FRAGILE => Kind::Fragile,
            STALE => Kind::Stale,
            _ => unreachable!(),
        })
    }

    /// The banked prereq drill_held parks n behind, or None.
    fn holding(&self, n: &str) -> Option<String> {
        self.ctx
            .prereqs(n)
            .iter()
            .find(|p| {
                self.ctx.has_drill_bank(p)
                    && self.statuses.contains_key(*p)
                    && (!is_solid(self.statuses, p)
                        || !owned(self.ev, p)
                        || drills_left(self.ctx, p, self.ev, false))
            })
            .cloned()
    }

    /// (prereq, drill id) that opens the hold on n.
    fn opener(&self, n: &str) -> Option<(String, String)> {
        if let Some(o) = self.opener_memo.borrow().get(n) {
            return o.clone();
        }
        let o = self.opener_uncached(n);
        self.opener_memo
            .borrow_mut()
            .insert(n.to_string(), o.clone());
        o
    }

    fn opener_uncached(&self, n: &str) -> Option<(String, String)> {
        if self.cram || !drill_held(self.ctx, n, self.statuses, self.ev, &HashSet::new()) {
            return None;
        }
        let mut pre = self.holding(n);
        let mut seen: HashSet<String> = HashSet::new();
        while let Some(p) = pre.clone() {
            if seen.contains(&p)
                || !drill_held(self.ctx, &p, self.statuses, self.ev, &HashSet::new())
            {
                break;
            }
            seen.insert(p.clone());
            pre = self.holding(&p);
        }
        let pre = pre?;
        if !is_solid(self.statuses, &pre) {
            return None;
        }
        let drill_id = format!("drill:{pre}");
        if self.args.exclude.contains(&drill_id) {
            return None;
        }
        let path = due_drill(self.ctx, &pre, self.ev, self.today, false, false)?;
        if drill_capped(self.ctx, &path, self.ev, self.today) {
            return None;
        }
        Some((pre, drill_id))
    }

    fn drill_for(&self, n: &str) -> Option<(String, String)> {
        match self.due(n) {
            Some(d) => Some((n.to_string(), d)),
            None => self.opener(n),
        }
    }

    fn solve_state(
        &self,
    ) -> (
        HashMap<String, f64>,
        Option<HashMap<String, f64>>,
        HashMap<String, f64>,
    ) {
        if let Some(s) = self.model.borrow().as_ref() {
            return s.clone();
        }
        let coef = solve_model(self.ctx);
        let ratings = if coef.is_some() {
            solve_ratings(self.ctx)
        } else {
            HashMap::new()
        };
        let recall = if coef.is_some() {
            current_recall(self.ctx, self.ev, self.today)
        } else {
            HashMap::new()
        };
        let state = (recall, coef, ratings);
        *self.model.borrow_mut() = Some(state.clone());
        state
    }

    /// The rep that widens a THIN move's breadth.
    fn prove(&self, target: &str) -> Option<Choice> {
        let waiting = self.gain.get(target).copied().unwrap_or(0);
        let mut why = format!("widen reach - prove {target} on a real problem");
        if waiting != 0 {
            why.push_str(&format!("; {waiting} drafted problems wait on it"));
        }
        let mut cands: Vec<String> = {
            let pv = self.pv.borrow();
            proving_carriers(self.ctx, target, &pv, self.statuses, self.ev, self.today)
                .into_iter()
                .filter(|c| {
                    !self.args.asleep.contains(c)
                        && !self.args.exclude.contains(c.as_str())
                        && cooled(self.ev, c, self.today)
                })
                .collect()
        };
        let aim = target_pass_rate();
        let (recall, coef, ratings) = self.solve_state();
        {
            let pv = self.pv.borrow();
            let informative = |p: &str| -> (bool, f64) {
                let odds = problem_solve_p(p, &pv, &recall, coef.as_ref(), &ratings);
                match odds {
                    None => (true, 0.0),
                    Some(o) => (false, (o - aim).abs()),
                }
            };
            cands.sort_by(|a, b| {
                let ia = informative(a);
                let ib = informative(b);
                ia.0.cmp(&ib.0)
                    .then_with(|| ia.1.partial_cmp(&ib.1).unwrap())
                    .then_with(|| gentleness(self.ctx, a, &pv).cmp(&gentleness(self.ctx, b, &pv)))
                    .then_with(|| last_solved(self.ev, a).cmp(&last_solved(self.ev, b)))
                    .then_with(|| {
                        self.ctx
                            .acceptance(b)
                            .partial_cmp(&self.ctx.acceptance(a))
                            .unwrap()
                    })
                    .then_with(|| pnum_key(a).cmp(&pnum_key(b)))
            });
        }
        let fresh: Vec<&String> = cands
            .iter()
            .filter(|c| !counted_toward_bar(self.ev, c, target))
            .collect();
        if let Some(f) = fresh.first() {
            return Some(Choice::new(target, SOLID, f, why));
        }
        let promo = {
            let pv = self.pv.borrow();
            let (bar_kind, _) = crate::status::carry_bar(self.ctx, target, &pv);
            let diffs: &[&str] = if bar_kind == "medium" {
                &["Medium"]
            } else {
                &["Easy", "Medium"]
            };
            predicted_carrier(
                self.ctx,
                target,
                &pv,
                self.statuses,
                self.ev,
                &self.skip_set(),
                diffs,
                self.today,
            )
        };
        if let Some((num, entry)) = promo {
            self.pv.borrow_mut().insert(num.clone(), entry);
            return Some(Choice::new(
                target,
                SOLID,
                &num,
                format!("{why} (drafted carrier)"),
            ));
        }
        if let Some(c) = cands.first() {
            return Some(Choice::new(
                target,
                SOLID,
                c,
                format!("{why} (re-solve: no fresh carrier)"),
            ));
        }
        None
    }

    /// The pick that gives n its rep today, or None.
    fn serve(&self, n: &str, due_list: &[String]) -> Option<Choice> {
        let k = self.kind(n)?;
        if k == Kind::Thin {
            return self.prove(n);
        }
        let (status, last) = self.status(n);
        let age = last.map(|l| (self.today - l).num_days());
        let deep = k == Kind::Stale && age.is_some_and(|a| a > DEEP_STALE_DAYS);
        let sleeper = self.under.get(n).cloned();
        if let Some((node, drill_id)) = self.drill_for(n) {
            if node != n {
                let why = if owned(self.ev, &node) {
                    "next undone drill"
                } else {
                    "own it unaided"
                };
                let held = due_list
                    .iter()
                    .filter(|m| self.opener(m).map(|(p, _)| p) == Some(node.clone()))
                    .count();
                return Some(Choice::new(
                    &node,
                    SOLID,
                    &drill_id,
                    format!(
                        "{why} - {held} held move{} wait{} on it",
                        if held > 1 { "s" } else { "" },
                        if held > 1 { "" } else { "s" }
                    ),
                ));
            }
            let reason = if let Some(s) = &sleeper {
                format!("warm the ground under sleeping {s} \u{2014} drill {n} first")
            } else if k == Kind::Fragile {
                "fragile move \u{2014} drill until clean, carrier after".to_string()
            } else if k == Kind::Floor {
                format!(
                    "graduating rep - young move at its {}d floor - drill first, carrier after",
                    self.floor(n).unwrap().1
                )
            } else if k == Kind::Drill {
                let path = due_drill(self.ctx, n, self.ev, self.today, false, false);
                drill_clock_reason(self.ctx, path.as_ref(), self.ev, self.today)
            } else if deep {
                format!(
                    "re-enter a deep-stale move ({}d since clean) \u{2014} drill until clean, carrier after",
                    age.unwrap()
                )
            } else if k == Kind::Stale {
                format!(
                    "stale move ({}d since clean) - drill first, carrier after",
                    age.unwrap()
                )
            } else {
                "new move \u{2014} drill until clean, carrier after".to_string()
            };
            return Some(Choice::new(n, status, &drill_id, reason));
        }
        if drill_gated(self.ctx, n, status, last, self.today) {
            return None;
        }
        if k == Kind::Floor && self.immature.contains(n) {
            if let Some(proof) = self.prove(n) {
                return Some(proof);
            }
        }
        let mapped: Vec<String> = {
            let pv = self.pv.borrow();
            carriers_for(self.ctx, n, &pv, self.statuses, self.ev, self.today)
        };
        let unsolved: Vec<String> = mapped
            .iter()
            .filter(|c| last_solved(self.ev, c).is_empty())
            .cloned()
            .collect();
        let mut cands: Vec<String> = mapped
            .iter()
            .filter(|c| {
                !self.args.asleep.contains(c)
                    && !self.args.exclude.contains(c.as_str())
                    && cooled(self.ev, c, self.today)
            })
            .cloned()
            .collect();
        if !cands.is_empty() {
            if let Some(s) = &sleeper {
                let pv = self.pv.borrow();
                cands.sort_by(|a, b| {
                    (
                        last_solved(self.ev, a),
                        tree_size(self.ctx, a, &pv),
                        pnum_key(a),
                    )
                        .cmp(&(
                            last_solved(self.ev, b),
                            tree_size(self.ctx, b, &pv),
                            pnum_key(b),
                        ))
                });
                return Some(Choice::new(
                    n,
                    status,
                    &cands[0],
                    format!("warm the ground under sleeping {s} ({n})"),
                ));
            }
            if k == Kind::Fragile && self.dodged.contains_key(n) {
                let pv = self.pv.borrow();
                cands.sort_by(|a, b| {
                    (
                        dodgeable(&pv, a, n),
                        tree_size(self.ctx, a, &pv),
                        last_solved(self.ev, a),
                        pnum_key(a),
                    )
                        .cmp(&(
                            dodgeable(&pv, b, n),
                            tree_size(self.ctx, b, &pv),
                            last_solved(self.ev, b),
                            pnum_key(b),
                        ))
                });
                return Some(Choice::new(
                    n,
                    status,
                    &cands[0],
                    format!(
                        "you dodged this move on {} \u{2014} carrier chosen to resist the dodge",
                        self.dodged[n]
                    ),
                ));
            }
            if k == Kind::Stale && !deep {
                let carrier = latest_carrier(self.ev, n);
                let pnum = match carrier {
                    Some((_, _, Some(p))) if cands.contains(&p) => p,
                    _ => {
                        let mut s = cands.clone();
                        // sorted(..., reverse=True) keeps equal keys in order
                        s.sort_by_key(|b| std::cmp::Reverse(last_solved(self.ev, b)));
                        s[0].clone()
                    }
                };
                return Some(Choice::new(
                    n,
                    status,
                    &pnum,
                    "spaced re-solve of a stale move's carrier".to_string(),
                ));
            }
            if k != Kind::Floor {
                if let Some(promo) = self.promote(n, &unsolved) {
                    return Some(Choice::new(n, status, &promo, PROMOTED.to_string()));
                }
            }
            {
                let pv = self.pv.borrow();
                cands.sort_by(|a, b| {
                    (
                        !last_solved(self.ev, a).is_empty(),
                        gentleness(self.ctx, a, &pv),
                        last_solved(self.ev, a),
                    )
                        .cmp(&(
                            !last_solved(self.ev, b).is_empty(),
                            gentleness(self.ctx, b, &pv),
                            last_solved(self.ev, b),
                        ))
                        .then_with(|| {
                            self.ctx
                                .acceptance(b)
                                .partial_cmp(&self.ctx.acceptance(a))
                                .unwrap()
                        })
                        .then_with(|| pnum_key(a).cmp(&pnum_key(b)))
                });
            }
            let reason = if k == Kind::Fragile {
                "consolidate a fragile move on a fresh carrier".to_string()
            } else if k == Kind::Floor {
                format!(
                    "graduating rep - young move at its {}d floor",
                    self.floor(n).unwrap().1
                )
            } else if deep {
                format!(
                    "re-enter a deep-stale move ({}d since clean) on a gentle fresh carrier",
                    age.unwrap()
                )
            } else {
                "one genuinely new move, prereqs all solid".to_string()
            };
            return Some(Choice::new(n, status, &cands[0], reason));
        }
        if k != Kind::Floor {
            if let Some(promo) = self.promote(n, &unsolved) {
                return Some(Choice::new(n, status, &promo, PROMOTED.to_string()));
            }
        }
        self.unhold(n)
    }

    /// rule 2c: a problem on a review clock of its own.
    fn review(&self) -> Option<Choice> {
        let pv = self.pv.borrow();
        for (pnum, _due, _interval) in review_queue(self.ctx, self.ev, &pv, self.today) {
            if self.args.asleep.contains(&pnum) || self.args.exclude.contains(&pnum) {
                continue;
            }
            let moves = pv.get(&pnum).map(|p| p.moves.clone()).unwrap_or_default();
            if moves.is_empty() || !moves.iter().all(|m| self.ctx.nodes.contains_key(m)) {
                continue;
            }
            if moves.iter().any(|m| self.group_capped(m)) {
                continue;
            }
            let (when, label) = last_attempt(self.ev, &pnum).expect("a due problem has an attempt");
            let age = (self.today - when).num_days();
            let target = moves
                .iter()
                .min_by(|a, b| {
                    (is_solid(self.statuses, a), self.degrees[*a])
                        .partial_cmp(&(is_solid(self.statuses, b), self.degrees[*b]))
                        .unwrap()
                        .then_with(|| a.cmp(b))
                })
                .unwrap();
            return Some(Choice::new(
                target,
                self.status(target).0,
                &pnum,
                format!("{label} on this problem {age}d ago - the unaided rep it is waiting for"),
            ));
        }
        None
    }

    fn sort_key(&self, n: &str, drill_none: bool) -> (bool, i64, bool, SortSub) {
        let k = self.kind(n).unwrap();
        let last = self.status(n).1.unwrap_or(NaiveDate::MIN);
        let payoff = if k == Kind::Thin {
            &self.gain
        } else {
            &self.unl
        };
        let sub = if k == Kind::Floor {
            SortSub::Floor(
                self.floor(n).unwrap().0,
                self.degrees[n],
                -self.unl.get(n).copied().unwrap_or(0),
                n.to_string(),
            )
        } else {
            SortSub::Other(
                self.degrees[n],
                -payoff.get(n).copied().unwrap_or(0),
                last,
                n.to_string(),
            )
        };
        (!self.under.contains_key(n), order(k), drill_none, sub)
    }
}

#[derive(Clone, Debug, PartialEq)]
enum SortSub {
    Floor(NaiveDate, f64, i64, String),
    Other(f64, i64, NaiveDate, String),
}

impl PartialOrd for SortSub {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        match (self, other) {
            (SortSub::Floor(a, b, c, d), SortSub::Floor(e, f, g, h)) => Some(
                a.cmp(e)
                    .then_with(|| b.partial_cmp(f).unwrap())
                    .then_with(|| c.cmp(g))
                    .then_with(|| d.cmp(h)),
            ),
            (SortSub::Other(a, b, c, d), SortSub::Other(e, f, g, h)) => Some(
                a.partial_cmp(e)
                    .unwrap()
                    .then_with(|| b.cmp(f))
                    .then_with(|| c.cmp(g))
                    .then_with(|| d.cmp(h)),
            ),
            // a floor sub and an other sub are never compared: the kind
            // ranks before the sub
            _ => Some(std::cmp::Ordering::Equal),
        }
    }
}

/// kg_next.pick: (target, status, pnum, reason) or None.
pub fn pick(
    ctx: &Ctx,
    pv: &RefCell<PView>,
    ev: &Evidence,
    statuses: &Statuses,
    args: &PickArgs,
) -> Option<Choice> {
    let t = std::time::Instant::now();
    let early = args.early || args.assisted;
    let cram = args.cram || early;
    let today = ctx.today();
    let solved_ever: HashSet<String> = ev.recs.iter().map(|(_, r)| r.problem_str()).collect();

    let caps = if args.group.is_some() || cram {
        vec![]
    } else {
        group_caps()
    };
    let capped: HashSet<String> = caps
        .iter()
        .filter(|(g, c)| group_reps(ctx, g, ev, today) >= *c)
        .map(|(g, _)| g.clone())
        .collect();

    // the clock
    if anki() {
        let scope: Vec<String> = ctx
            .nodes
            .keys()
            .filter(|n| args.group.is_none() || ctx.group_of(n) == args.group.as_deref())
            .cloned()
            .collect();
        for (path, node) in anki_frontier(ctx, ev, today, None, Some(&scope), args.assisted) {
            let drill_id = format!("drill:{node}");
            if args.exclude.contains(&drill_id) || !statuses.contains_key(&node) {
                continue;
            }
            if ctx.group_of(&node).is_some_and(|g| capped.contains(g)) {
                continue;
            }
            if drill_capped(ctx, &path, ev, today) {
                continue;
            }
            return Some(Choice::new(
                &node,
                statuses[&node].0,
                &drill_id,
                drill_clock_reason(ctx, Some(&path), ev, today),
            ));
        }
    }

    ptrace("clock", t);
    let t = std::time::Instant::now();
    let (immature, degrees, carr, unl, gain) = {
        let p = pv.borrow();
        let immature = immature_nodes(ctx, ev, &p);
        let degrees: HashMap<String, f64> = ctx
            .nodes
            .keys()
            .map(|n| (n.clone(), node_degree(ctx, n, ev, &p, today)))
            .collect();
        // (node_degree caches its axes per (node, day) in the evidence)
        let carr: HashMap<String, i64> = p.carrier_counts(ctx).as_ref().clone();
        let unl = unlocks(ctx, statuses, &p, &HashSet::new());
        let gain = unlocks(ctx, statuses, &p, &immature);
        (immature, degrees, carr, unl, gain)
    };
    let dodged = ev.dodged_nodes();
    ptrace("tables", t);
    let t = std::time::Instant::now();

    let mut under: HashMap<String, String> = HashMap::new();
    if args.group.is_none() {
        let p = pv.borrow();
        for pnum in &args.asleep {
            let moves = p.get(pnum).map(|x| x.moves.clone()).unwrap_or_default();
            let mut tree: Vec<String> = input_tree(&moves, &ctx.nodes).into_iter().collect();
            tree.sort();
            for n in tree {
                if !is_solid(statuses, &n) {
                    under.entry(n).or_insert_with(|| pnum.clone());
                }
            }
        }
    }

    let picker = Picker {
        ctx,
        pv,
        ev,
        statuses,
        args,
        today,
        cram,
        early,
        assisted: args.assisted,
        solved_ever,
        capped: capped.clone(),
        immature,
        degrees,
        carr,
        unl,
        gain,
        dodged,
        under,
        model: RefCell::new(None),
        due_memo: RefCell::new(HashMap::new()),
        kind_memo: RefCell::new(HashMap::new()),
        opener_memo: RefCell::new(HashMap::new()),
    };

    // rule -1: the session-start easy
    if args.session_start {
        let easies = {
            let p = pv.borrow();
            trivial_easies(ctx, &p, ev, statuses, today)
        };
        for pnum in easies {
            if !args.asleep.contains(&pnum) && !args.exclude.contains(&pnum) {
                let m0 = pv.borrow().get(&pnum).unwrap().moves[0].clone();
                return Some(Choice::new(
                    &m0,
                    SOLID,
                    &pnum,
                    "session start \u{2014} trivial easy to get the juices flowing".to_string(),
                ));
            }
        }
    }

    // rule 0a: a woken problem
    for pnum in &args.woken {
        if args.exclude.contains(pnum) {
            continue;
        }
        let moves = pv
            .borrow()
            .get(pnum)
            .map(|p| p.moves.clone())
            .unwrap_or_default();
        let target = moves
            .iter()
            .find(|m| !is_solid(statuses, m))
            .unwrap_or(&moves[0])
            .clone();
        return Some(Choice::new(
            &target,
            st(statuses, &target).0,
            pnum,
            format!("woken from sleep \u{2014} the ground is ready; make wake {pnum} to resume"),
        ));
    }

    // rule 0b: warm the rusty ground under a sleeping problem
    if args.group.is_none() {
        for pnum in &args.asleep {
            let moves = pv
                .borrow()
                .get(pnum)
                .map(|p| p.moves.clone())
                .unwrap_or_default();
            let mut rusty: Vec<String> = input_tree(&moves, &ctx.nodes)
                .into_iter()
                .filter(|n| !is_solid(statuses, n))
                .collect();
            rusty.sort_by(|a, b| {
                let la = st(statuses, a).1;
                let lb = st(statuses, b).1;
                (la.is_some(), la)
                    .cmp(&(lb.is_some(), lb))
                    .then_with(|| a.cmp(b))
            });
            for target in rusty {
                let (status, last) = st(statuses, &target);
                if drill_gated(ctx, &target, status, last, today) {
                    if let Some(d) = picker.due(&target) {
                        return Some(Choice::new(
                            &target,
                            status,
                            &d,
                            format!("warm the ground under sleeping {pnum} \u{2014} drill {target} first"),
                        ));
                    }
                    continue;
                }
                let mut cands: Vec<String> = {
                    let p = pv.borrow();
                    carriers_for(ctx, &target, &p, statuses, ev, today)
                        .into_iter()
                        .filter(|c| {
                            !args.asleep.contains(c)
                                && !args.exclude.contains(c)
                                && cooled(ev, c, today)
                        })
                        .collect()
                };
                if !cands.is_empty() {
                    let p = pv.borrow();
                    cands.sort_by(|a, b| {
                        (last_solved(ev, a), tree_size(ctx, a, &p), pnum_key(a)).cmp(&(
                            last_solved(ev, b),
                            tree_size(ctx, b, &p),
                            pnum_key(b),
                        ))
                    });
                    return Some(Choice::new(
                        &target,
                        status,
                        &cands[0],
                        format!("warm the ground under sleeping {pnum} ({target})"),
                    ));
                }
                if let Some(d) = picker.due(&target) {
                    return Some(Choice::new(
                        &target,
                        status,
                        &d,
                        format!("warm the ground under sleeping {pnum} \u{2014} no READY carrier, drill {target}"),
                    ));
                }
            }
        }
    }

    // rule 0d: the early review
    if early {
        let mut review: Vec<String> = ctx
            .nodes
            .keys()
            .filter(|n| picker.in_scope(n))
            .cloned()
            .collect();
        review.sort_by_key(|n| {
            (
                input_tree(std::slice::from_ref(n), &ctx.nodes).len(),
                n.clone(),
            )
        });
        for target in review {
            if let Some(d) = picker.due(&target) {
                let reason = if args.assisted {
                    "assisted review - the unaided rep this drill is waiting for"
                } else {
                    "early review - next drill, atoms first"
                };
                return Some(Choice::new(
                    &target,
                    st(statuses, &target).0,
                    &d,
                    reason.to_string(),
                ));
            }
        }
    }

    // the frontier
    let mut due_list: Vec<String> = ctx
        .nodes
        .keys()
        .filter(|n| picker.in_scope(n) && picker.kind(n).is_some())
        .cloned()
        .collect();
    ptrace("rules -1..0d", t);
    let t = std::time::Instant::now();
    let keys: HashMap<String, (bool, i64, bool, SortSub)> = due_list
        .iter()
        .map(|n| (n.clone(), picker.sort_key(n, picker.drill_for(n).is_none())))
        .collect();
    due_list.sort_by(|a, b| {
        let ka = &keys[a];
        let kb = &keys[b];
        (ka.0, ka.1, ka.2)
            .cmp(&(kb.0, kb.1, kb.2))
            .then_with(|| ka.3.partial_cmp(&kb.3).unwrap())
    });

    ptrace("due_list", t);
    let t = std::time::Instant::now();
    let mut reviewed = false;
    if crate::drills::reviews_first() {
        reviewed = true;
        if let Some(c) = picker.review() {
            return Some(c);
        }
    }
    for n in &due_list {
        if !reviewed && order(picker.kind(n).unwrap()) >= order(Kind::Stale) {
            reviewed = true;
            if let Some(c) = picker.review() {
                return Some(c);
            }
        }
        let choice = picker.serve(n, &due_list);
        if let Some(c) = choice {
            if ctx.group_of(&c.target).is_some_and(|g| capped.contains(g)) {
                continue;
            }
            ptrace("serve", t);
            return Some(c);
        }
    }
    ptrace("serve", t);
    if !reviewed {
        if let Some(c) = picker.review() {
            return Some(c);
        }
    }

    // rule 4: a summit
    if args.group.is_none() {
        let summits: Vec<String> = {
            let p = pv.borrow();
            ready_hards(ctx, &p, ev, statuses, Some(&picker.immature), None, today)
                .into_iter()
                .filter(|s| !args.asleep.contains(s) && !args.exclude.contains(s))
                .collect()
        };
        if !summits.is_empty() {
            let p = pv.borrow();
            let pnum = rank_summits(ctx, &summits, &p, statuses, &HashSet::new())[0].clone();
            let m0 = p.get(&pnum).unwrap().moves[0].clone();
            return Some(Choice::new(
                &m0,
                SOLID,
                &pnum,
                "summit \u{2014} its walk has no gaps left".to_string(),
            ));
        }
    }

    // rule 6: an unsolved drafted problem entirely in reach
    if args.group.is_none() {
        let t = today.format("%Y-%m-%d").to_string();
        let mut solved_today: Vec<(&str, usize)> = ev
            .date_recs(&t)
            .iter()
            .filter(|&&i| ev.rec(i).problem.as_deref().is_some_and(is_numeric_id))
            .map(|&i| (ev.fname(i), i))
            .collect();
        solved_today.sort_by(|a, b| a.0.cmp(b.0));
        let last = solved_today
            .last()
            .map(|(_, i)| ev.rec(*i).problem.clone().unwrap());
        let first = match &last {
            Some(l) if ctx.problem_difficulty(l, &pv.borrow().map) == "Hard" => "Medium",
            _ => "Hard",
        };
        let mut skip: HashSet<String> = args.asleep.iter().cloned().collect();
        skip.extend(args.exclude.iter().cloned());
        let drafted = {
            let p = pv.borrow();
            drafted_in_reach(
                ctx,
                &p,
                statuses,
                &picker.immature,
                ev,
                &skip,
                first,
                20,
                today,
            )
        };
        if let Some((num, entry)) = drafted.into_iter().next() {
            let m0 = entry.moves[0].clone();
            pv.borrow_mut().insert(num.clone(), entry);
            return Some(Choice::new(
                &m0,
                SOLID,
                &num,
                "in reach - unsolved drafted problem, every move solid and mature".to_string(),
            ));
        }
    }
    None
}

pub const EXPLORE_REASONS: [&str; 3] = ["summit", "widen reach", "in reach"];

pub fn exploratory(status: Status, reason: &str) -> bool {
    status == MISSING || EXPLORE_REASONS.iter().any(|r| reason.starts_with(r))
}

/// kg_next.withheld: the park is full and the pick is new ground.
pub fn withheld(choice: Option<&Choice>, asleep: &[String]) -> bool {
    match choice {
        None => false,
        Some(c) => (asleep.len() as i64) >= max_asleep() && exploratory(c.status, &c.reason),
    }
}

pub fn park_full_lines(asleep: &[String]) -> Vec<String> {
    vec![format!(
        "{} asleep (cap {}) - new ground is withheld until you face one (make wake <n>), then: keep going (make solved) / learn it (notes say \"learning\", make solved) / fail it (make failed)",
        asleep.len(),
        max_asleep()
    )]
}

/// kg_next.ready_hards: unsolved Hards with no gaps in their route, ranked.
pub fn ready_hards(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    immature: Option<&HashSet<String>>,
    recog: Option<&recog::Recog>,
    today: NaiveDate,
) -> Vec<String> {
    let solved = ev.solved_problems();
    let imm_own;
    let immature = match immature {
        Some(i) => i,
        None => {
            imm_own = immature_nodes(ctx, ev, pv);
            &imm_own
        }
    };
    let recog_own;
    let recog = match recog {
        Some(r) => r,
        None => {
            recog_own = recog::derived(ctx, &recog::load_recognition(ctx), ev, pv, statuses);
            &recog_own
        }
    };
    let node_ids: Vec<String> = ctx.nodes.keys().cloned().collect();
    let rstat = recog::recognition_statuses(recog, &node_ids, today);
    let mut out = Vec::new();
    for (pnum, p) in &pv.map {
        if !p.is_hard() || ctx.unservable(pnum, p) || solved.contains(pnum) || p.moves.is_empty() {
            continue;
        }
        if p.moves.iter().any(|m| {
            rstat
                .get(m)
                .map(|(s, _)| *s)
                .unwrap_or_else(|| recog::recognition_status(m, recog, today).0)
                == recog::FAILED_TO_RECOGNIZE
        }) {
            continue;
        }
        if route_gaps(ctx, pnum, pv, statuses, immature).1 == 0 {
            out.push(pnum.clone());
        }
    }
    let classics: Vec<String> = out
        .iter()
        .filter(|p| CLASSICS.contains(&p.as_str()))
        .cloned()
        .collect();
    let pool = if classics.is_empty() { out } else { classics };
    rank_summits(ctx, &pool, pv, statuses, immature)
}

/// kg_next.blocked_frontier: (node, status, why, dry) per frontier node
/// pick() had to walk past.
pub fn blocked_frontier(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    asleep: &[String],
    exclude: &HashSet<String>,
    today: NaiveDate,
) -> Vec<(String, Status, String, bool)> {
    let mut out = Vec::new();
    for nid in ctx.nodes.keys() {
        let (status, last) = st(statuses, nid);
        if status == SOLID {
            continue;
        }
        let prereqs: Vec<&String> = ctx
            .prereqs(nid)
            .iter()
            .filter(|p| statuses.contains_key(*p))
            .collect();
        if status == MISSING && !prereqs.iter().all(|p| is_solid(statuses, p)) {
            continue;
        }
        if drill_held(ctx, nid, statuses, ev, &HashSet::new()) {
            let holders: Vec<String> = prereqs
                .iter()
                .filter(|p| {
                    ctx.has_drill_bank(p)
                        && (!is_solid(statuses, p)
                            || !owned(ev, p)
                            || drills_left(ctx, p, ev, false))
                })
                .map(|p| (*p).clone())
                .collect();
            out.push((
                nid.clone(),
                status,
                format!(
                    "held behind {} (unaided clean rep or undone drills)",
                    holders.join(", ")
                ),
                false,
            ));
            continue;
        }
        if drill_gated(ctx, nid, status, last, today)
            && due_drill(ctx, nid, ev, today, false, false).is_none()
        {
            out.push((
                nid.clone(),
                status,
                "drilled today, still not clean - holds until a clean rep".to_string(),
                false,
            ));
            continue;
        }
        let ready = carriers_for(ctx, nid, pv, statuses, ev, today);
        let live: Vec<&String> = ready
            .iter()
            .filter(|c| !asleep.contains(c) && !exclude.contains(*c))
            .collect();
        if live.iter().any(|c| cooled(ev, c, today)) {
            continue;
        }
        let path = due_drill(ctx, nid, ev, today, false, false);
        if let Some(p) = &path {
            if !drill_capped(ctx, p, ev, today) {
                continue;
            }
            out.push((
                nid.clone(),
                status,
                "its drill is due, the day's drill budget is spent (MAX_NEW_DRILLS / MAX_DRILL_REVIEWS)".to_string(),
                false,
            ));
            continue;
        }
        if !ready.iter().any(|c| last_solved(ev, c).is_empty()) {
            let mut skip: HashSet<String> = asleep.iter().cloned().collect();
            skip.extend(exclude.iter().cloned());
            if predicted_carrier(
                ctx,
                nid,
                pv,
                statuses,
                ev,
                &skip,
                &["Easy", "Medium"],
                today,
            )
            .is_some()
            {
                continue;
            }
        }
        if !live.is_empty() {
            let soonest = live.iter().min_by_key(|c| last_solved(ev, c)).unwrap();
            let cools =
                parse_date(&last_solved(ev, soonest)) + Duration::days(CARRIER_COOLDOWN_DAYS);
            let mut why = format!("carrier {soonest} cools {}", cools.format("%Y-%m-%d"));
            if ctx.has_drill_bank(nid) {
                why.push_str(", and its drill is done for today");
            }
            out.push((nid.clone(), status, why, false));
            continue;
        }
        let walks: Vec<String> = pv
            .map
            .iter()
            .filter(|(_, v)| v.moves.iter().any(|m| m == nid))
            .map(|(p, _)| p.clone())
            .collect();
        let usable: Vec<&String> = walks
            .iter()
            .filter(|p| !ctx.unservable(p, pv.get(p).unwrap()) && !pv.get(p).unwrap().is_hard())
            .collect();
        let mut listed = walks.clone();
        listed.sort_by_key(|p| pnum_key(p));
        let listed = listed.join(", ");
        let mut dry = true;
        let mut why = if walks.is_empty() {
            "no problem in the graph uses this move".to_string()
        } else if usable.is_empty() {
            if walks.len() == 1 {
                format!("the only problem using it is {listed}, a Hard or banned one (hards are summits, never used to introduce a move)")
            } else {
                format!("every problem using it ({listed}) is a Hard or banned")
            }
        } else if ready.is_empty() {
            dry = false;
            "every problem using it also needs a second rusty move made solid first".to_string()
        } else {
            dry = false;
            let parked: Vec<&String> = ready.iter().filter(|c| asleep.contains(c)).collect();
            if parked.is_empty() {
                "every problem using it is already solved today".to_string()
            } else {
                format!(
                    "its carrier {} is asleep (make wake)",
                    parked
                        .iter()
                        .map(|s| s.as_str())
                        .collect::<Vec<_>>()
                        .join(", ")
                )
            }
        };
        if ctx.has_drill_bank(nid) {
            why.push_str(", and its drill is done for today");
        } else {
            why.push_str(", and no drill exists for it");
        }
        why.push_str(", and no drafted walk can carry it alone");
        out.push((nid.clone(), status, why, dry));
    }
    out
}

/// kg_next.due_on: move n is due on `day` by pick()'s own kind().
pub fn due_on(
    ctx: &Ctx,
    n: &str,
    ev: &Evidence,
    carr: &HashMap<String, i64>,
    day: NaiveDate,
    cache: &mut HashMap<String, Evidence>,
) -> bool {
    let (status, _) = node_status(ctx, n, ev, day);
    if status == STALE || status == FRAGILE {
        return true;
    }
    if status == SOLID {
        return graduation_due(ev, n, carr.get(n).copied().unwrap_or(0))
            .is_some_and(|(d, _)| d <= day);
    }
    let prereqs = ctx.prereqs(n);
    if prereqs.is_empty() {
        return true;
    }
    let cut = day.format("%Y-%m-%d").to_string();
    let _ = cache;
    prereqs
        .iter()
        .all(|p| crate::status::node_status_cut(ctx, p, ev, &cut, day).0 == SOLID)
}

/// kg_next.starved: {move: days} for every move due today that has been
/// due STARVED_DAYS or more days in a row with no rep aimed at it.
pub fn starved(ctx: &Ctx, pv: &PView, ev: &Evidence, today: NaiveDate) -> Vec<(String, i64)> {
    let carr = pv.carrier_counts(ctx);
    let mut cache: HashMap<String, Evidence> = HashMap::new();
    let mut out = Vec::new();
    for n in ctx.nodes.keys() {
        let last = ev.node_entries(n).iter().map(|e| e.date).max();
        let (mut days, mut day) = (0i64, today);
        while last.is_none_or(|l| day > l)
            && days < 365
            && due_on(ctx, n, ev, &carr, day, &mut cache)
        {
            days += 1;
            day -= Duration::days(1);
        }
        if days >= STARVED_DAYS {
            out.push((n.clone(), days));
        }
    }
    out
}

/// kg_next.routed_around: {move: carrier} for a starved move whose carrier
/// was solved without it during the starvation run.
pub fn routed_around(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    today: NaiveDate,
) -> Vec<(String, String)> {
    routed_around_from(pv, ev, today, &starved(ctx, pv, ev, today))
}

/// routed_around over a starved list already computed.
pub fn routed_around_from(
    pv: &PView,
    ev: &Evidence,
    today: NaiveDate,
    hungry: &[(String, i64)],
) -> Vec<(String, String)> {
    let mut out: Vec<(String, String)> = Vec::new();
    for (n, days) in hungry.iter().map(|(n, d)| (n.clone(), *d)) {
        let since = today - Duration::days(days);
        'probs: for (pnum, p) in &pv.map {
            if !p.moves.iter().any(|m| m == &n) {
                continue;
            }
            for (d, _, i) in ev.problem_recs(pnum) {
                if parse_date(d) >= since && !ev.rec(i).moves.contains_key(&n) {
                    out.push((n.clone(), pnum.clone()));
                    break 'probs;
                }
            }
        }
    }
    out
}

pub fn parked_summits(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    asleep: &[String],
    today: NaiveDate,
) -> Vec<String> {
    ready_hards(ctx, pv, ev, statuses, None, None, today)
        .into_iter()
        .filter(|p| asleep.contains(p))
        .collect()
}

pub fn unmapped_summits(ctx: &Ctx, pv: &PView, ev: &Evidence, statuses: &Statuses) -> Vec<String> {
    let solved = ev.solved_problems();
    let immature = immature_nodes(ctx, ev, pv);
    let mut out = Vec::new();
    for (pnum, p) in &pv.map {
        if !p.is_hard()
            || ctx.unservable(pnum, p)
            || solved.contains(pnum)
            || p.moves.is_empty()
            || p.unmapped.is_empty()
        {
            continue;
        }
        let (gaps, count, _) = route_gaps(ctx, pnum, pv, statuses, &immature);
        if gaps.is_empty() && count > 0 {
            out.push(pnum.clone());
        }
    }
    out.sort_by_key(|p| pnum_key(p));
    out
}

/// The replay both review_ahead and upcoming run: every pick granted a
/// clean unaided rep dated the replay day.
fn grant(
    ctx: &Ctx,
    pv: &RefCell<PView>,
    ev: &mut Evidence,
    statuses: &mut Statuses,
    choice: &Choice,
    day: NaiveDate,
    seq: usize,
) -> Option<(bool, String)> {
    let stamp = format!("{}T{:06}_00_00Z", day.format("%Y_%m_%d"), seq);
    let (moves, fname, problem, is_drill) = if choice.is_drill() {
        let path = due_drill(ctx, &choice.target, ev, day, false, false)?;
        let mut moves = ctx.drill_trains(&path);
        if moves.is_empty() {
            moves = vec![choice.target.clone()];
        }
        (
            moves,
            format!("solved/d_{}_{stamp}.py", ctx.drill_solved_stem(&path)),
            "drill".to_string(),
            true,
        )
    } else {
        let moves = pv
            .borrow()
            .get(&choice.pnum)
            .map(|p| p.moves.clone())
            .unwrap_or_default();
        (
            moves,
            format!("solved/p{}_{stamp}.py", choice.pnum),
            choice.pnum.clone(),
            false,
        )
    };
    let rec = Rec {
        date: day.format("%Y-%m-%d").to_string(),
        problem: Some(problem),
        moves: moves
            .iter()
            .filter(|m| ctx.nodes.contains_key(*m))
            .map(|m| (m.clone(), "clean".to_string()))
            .collect(),
        assist: crate::data::Assist::None,
        followup: None,
        pending: None,
    };
    ev.push(fname, rec);
    for m in &moves {
        if ctx.nodes.contains_key(m) {
            statuses.insert(m.clone(), node_status(ctx, m, ev, day));
        }
    }
    Some((is_drill, choice.pnum.clone()))
}

/// kg_next.review_ahead: (drills, problems, reached) between now and the
/// first exploratory pick.
pub fn review_ahead(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    asleep: &[String],
    exclude: &HashSet<String>,
    group: Option<&str>,
    days: i64,
    cap: i64,
) -> (i64, i64, bool) {
    let t = std::time::Instant::now();
    let mut ev = ev.clone();
    let pv = RefCell::new(pv.clone());
    ptrace("replay clone", t);
    let mut exclude = exclude.clone();
    let (mut drills, mut solves, mut seq) = (0i64, 0i64, 0usize);
    let real = ctx.today();
    let start = real;
    let result = (|| {
        for day_no in 0..days {
            let day = start + Duration::days(day_no);
            ctx.freeze(day);
            let t = std::time::Instant::now();
            let mut statuses = all_statuses(ctx, &ev, day);
            ptrace("replay statuses", t);
            let mut exhausted = false;
            while drills + solves < cap {
                let args = PickArgs {
                    asleep: asleep.to_vec(),
                    woken: vec![],
                    exclude: exclude.clone(),
                    session_start: false,
                    group: group.map(String::from),
                    cram: false,
                    early: false,
                    assisted: false,
                };
                let Some(choice) = pick(ctx, &pv, &ev, &statuses, &args) else {
                    exhausted = true;
                    break;
                };
                if exploratory(choice.status, &choice.reason) {
                    return (drills, solves, true);
                }
                seq += 1;
                let Some((is_drill, pnum)) =
                    grant(ctx, &pv, &mut ev, &mut statuses, &choice, day, seq)
                else {
                    exhausted = true;
                    break;
                };
                if is_drill {
                    drills += 1;
                } else {
                    solves += 1;
                }
                exclude.insert(pnum);
            }
            if !exhausted {
                break; // the cap: the while ran to its end without break
            }
            exclude = HashSet::new();
        }
        (drills, solves, false)
    })();
    ctx.freeze(real);
    result
}

/// kg_next.upcoming: the next `count` problem numbers the picker would
/// serve, drills skipped.
pub fn upcoming(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    count: usize,
    asleep: &[String],
    days: i64,
) -> Vec<String> {
    let mut ev = ev.clone();
    let pv = RefCell::new(pv.clone());
    let mut exclude: HashSet<String> = HashSet::new();
    let mut out: Vec<String> = Vec::new();
    let real = ctx.today();
    let start = real;
    let mut seq = 0usize;
    for day_no in 0..days {
        let day = start + Duration::days(day_no);
        ctx.freeze(day);
        let mut statuses = all_statuses(ctx, &ev, day);
        while out.len() < count {
            let args = PickArgs {
                asleep: asleep.to_vec(),
                exclude: exclude.clone(),
                ..Default::default()
            };
            let Some(choice) = pick(ctx, &pv, &ev, &statuses, &args) else {
                break;
            };
            seq += 1;
            let Some((is_drill, pnum)) = grant(ctx, &pv, &mut ev, &mut statuses, &choice, day, seq)
            else {
                break;
            };
            if !is_drill {
                out.push(pnum.clone());
            }
            exclude.insert(pnum);
        }
        if out.len() >= count {
            break;
        }
        exclude = HashSet::new();
    }
    ctx.freeze(real);
    out
}

pub fn review_line(drills: i64, solves: i64, reached: bool) -> String {
    if drills == 0 && solves == 0 {
        return if reached {
            "review ahead: none - this pick is new ground".to_string()
        } else {
            "review ahead: none, and nothing new to serve either".to_string()
        };
    }
    let mut parts = Vec::new();
    if drills != 0 {
        parts.push(format!(
            "{drills} drill{}",
            if drills != 1 { "s" } else { "" }
        ));
    }
    if solves != 0 {
        parts.push(format!(
            "{solves} problem{}",
            if solves != 1 { "s" } else { "" }
        ));
    }
    let tail = if reached {
        "then new ground"
    } else {
        "and still nothing new"
    };
    format!(
        "review ahead: {}, {tail} (if every rep is clean)",
        parts.join(", ")
    )
}

/// The unlabeled picks kg_next.serve dumps for the golden diff: (target,
/// status, pnum, reason) of the first pick under each argument set.
pub fn choice_tuple(c: &Choice) -> (String, String, String, String) {
    (
        c.target.clone(),
        c.status.to_string(),
        c.pnum.clone(),
        c.reason.clone(),
    )
}

pub fn has_problem(pv: &PView, pnum: &str) -> Option<Problem> {
    pv.get(pnum).cloned()
}
