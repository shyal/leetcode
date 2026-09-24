// The drill bank as kg_lib schedules it: a file's reps (matched on its
// DRILL title), warm / clean / assisted, the holds ("after" ids, the
// cross-bank hold, the drill gate), the SM-2 clock per file (anki_due,
// anki_frontier, due_drill), the daily budgets (MAX_NEW_DRILLS,
// MAX_DRILL_REVIEWS, KG_GROUP_CAP), and the file's own recall.

use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::rc::Rc;

use chrono::{Duration, NaiveDate};

use crate::bank::warm;
use crate::ctx::Ctx;
use crate::data::{
    assist_weight, env_str, filed_at, is_numeric_id, parse_date, Rec, SOLID_WINDOW_DAYS,
};
use crate::evidence::{drill_key, Evidence};
use crate::status::{
    graduation_due, input_tree, node_status, owned, Statuses, DEEP_STALE_DAYS, FRAGILE, MISSING,
    SOLID, STALE,
};

pub const ANKI_EASE: f64 = 2.5;
pub const ANKI_EASE_MIN: f64 = 1.3;
pub const ANKI_HARD_FACTOR: f64 = 1.2;
pub const ANKI_HARD_EASE_STEP: f64 = 0.15;
pub const ANKI_AGAIN_EASE_STEP: f64 = 0.20;
pub const ANKI_GRADUATING_DAYS: i64 = 1;
pub const ANKI_MAX_INTERVAL: i64 = 365;
/// Fuzz: an interval of at least this many days is shifted by a share of
/// itself, so files first done together drift apart instead of coming
/// back in one batch (Anki's fuzz). The share is 15% under a week, 10%
/// under three weeks, 5% beyond, never less than a day either way. The
/// shift is a hash of the file's evidence key and its rep count, so the
/// clock stays a pure function of the evidence.
pub const ANKI_FUZZ_MIN_DAYS: i64 = 3;

/// kg_lib.drill_scheduler: "node" or "anki" (DRILL_SCHEDULER).
pub fn drill_scheduler() -> String {
    let raw = env_str("DRILL_SCHEDULER").trim().to_lowercase();
    if raw.is_empty() {
        "node".to_string()
    } else {
        raw
    }
}

pub fn anki() -> bool {
    drill_scheduler() == "anki"
}

/// kg_lib.last_drilled: latest date this bank file was solved, "" if never.
pub fn last_drilled(ctx: &Ctx, path: &Path, ev: &Evidence) -> String {
    let key = ctx.drill_evidence_key(path);
    ev.drill_reps(&key)
        .iter()
        .map(|&i| ev.drills[i].0.as_str())
        .max()
        .unwrap_or("")
        .to_string()
}

/// kg_lib.latest_drill_rep: the most recent record of this bank file
/// (same-day reps ordered by the solved filename).
pub fn latest_drill_rep<'a>(ctx: &Ctx, path: &Path, ev: &'a Evidence) -> Option<&'a Rec> {
    latest_drill_index(ctx, path, ev).map(|i| ev.rec(ev.drills[i].2))
}

/// The most recent rep's index into ev.drills, so a caller can read the
/// solved filename next to the record.
fn latest_drill_index(ctx: &Ctx, path: &Path, ev: &Evidence) -> Option<usize> {
    let key = ctx.drill_evidence_key(path);
    // Python's max keeps the first of equal keys
    let mut best: Option<usize> = None;
    for i in ev.drill_reps(&key).iter().copied() {
        let better = match best {
            None => true,
            Some(b) => {
                let (di, bi, _) = &ev.drills[i];
                let (db, bb, _) = &ev.drills[b];
                (di, bi) > (db, bb)
            }
        };
        if better {
            best = Some(i);
        }
    }
    best
}

/// The latest rep as (solved filename, record), the pair Rec::drill_clean
/// and anki_answer grade.
fn latest_drill<'a>(ctx: &Ctx, path: &Path, ev: &'a Evidence) -> Option<(&'a str, &'a Rec)> {
    latest_drill_index(ctx, path, ev).map(|i| {
        let (_, base, ri) = &ev.drills[i];
        (base.as_str(), ev.rec(*ri))
    })
}

pub fn drill_clean(ctx: &Ctx, path: &Path, ev: &Evidence) -> bool {
    latest_drill(ctx, path, ev).is_some_and(|(base, rec)| rec.drill_clean(base))
}

pub fn drill_assisted(ctx: &Ctx, path: &Path, ev: &Evidence) -> bool {
    match latest_drill(ctx, path, ev) {
        None => false,
        Some((base, rec)) => !(rec.drill_clean(base) && rec.assist_any() == "none"),
    }
}

pub fn drill_warm(ctx: &Ctx, path: &Path, ev: &Evidence, today: NaiveDate) -> bool {
    match latest_drill(ctx, path, ev) {
        None => false,
        Some((base, rec)) => {
            rec.drill_clean(base)
                && rec.assist_any() == "none"
                && (today - parse_date(&rec.date)).num_days() <= SOLID_WINDOW_DAYS
        }
    }
}

/// DRILL_GATE_REPS: how many unaided clean reps, each on a day of its
/// own, a drill needs before a problem whose "after" names it is served.
/// Unset means 1. Drills that wait on drills keep the one-rep bar.
pub fn drill_gate_reps() -> usize {
    env_str("DRILL_GATE_REPS")
        .trim()
        .parse()
        .unwrap_or(1)
        .max(1)
}

/// The bar a drill clears before it releases a problem: its latest rep is
/// an unaided clean, and at least DRILL_GATE_REPS unaided cleans fall on
/// distinct days. No age limit: the drill clock decides when the drill
/// comes back, and the gate reads only how that rep went.
pub fn drill_gate_warm(ctx: &Ctx, path: &Path, ev: &Evidence) -> bool {
    if !latest_drill(ctx, path, ev)
        .is_some_and(|(base, rec)| rec.drill_clean(base) && rec.assist_any() == "none")
    {
        return false;
    }
    let key = ctx.drill_evidence_key(path);
    let days: HashSet<&str> = ev
        .drill_reps(&key)
        .iter()
        .filter(|&&i| {
            let (_, base, ri) = &ev.drills[i];
            let rec = ev.rec(*ri);
            rec.drill_clean(base) && rec.assist_any() == "none"
        })
        .map(|&i| ev.drills[i].0.as_str())
        .collect();
    days.len() >= drill_gate_reps()
}

/// kg_lib.servable_drills: files whose "after" ids are all warm and whose
/// other TRAINS nodes are owned.
pub fn servable_drills(
    ctx: &Ctx,
    candidates: &[PathBuf],
    ev: &Evidence,
    node_id: Option<&str>,
    early: bool,
) -> Vec<PathBuf> {
    let ro = &ctx.ro;
    let mut out = Vec::new();
    for path in candidates {
        if ctx
            .drill_after(path)
            .iter()
            .any(|a| warm(ctx, a, ro, ev, ctx.today(), early) == Some(false))
        {
            continue;
        }
        if ctx
            .drill_trains(path)
            .iter()
            .any(|t| Some(t.as_str()) != node_id && !owned(ev, t))
        {
            continue;
        }
        out.push(path.clone());
    }
    out
}

/// Drop the cached due_drill / cold_drill / drills_left answers the
/// records appended since can have changed (Ctx::deps), keep the rest.
fn sync_caches(ctx: &Ctx, ev: &Evidence) {
    let log: Vec<(Vec<String>, Option<String>, Option<String>)> = {
        let mut c = ev.cold_cache();
        if c.push_log.is_empty() {
            return;
        }
        std::mem::take(&mut c.push_log)
    };
    let hit = |node: &str| {
        let d = ctx.deps(node);
        log.iter()
            .any(|(m, b, p)| d.hit(m, b.as_deref(), p.as_deref()))
    };
    let mut c = ev.cold_cache();
    c.due_drill.retain(|(n, _, _, _), _| !hit(n));
    c.drills_left.retain(|(n, _), _| !hit(n));
    c.cold.retain(|(n, _), _| !hit(n));
    c.wanted.clear();
}

/// The node a bank file belongs to: drills/<node>/<file>.
pub fn drill_node(path: &Path) -> Option<String> {
    path.parent()?.file_name()?.to_str().map(String::from)
}

/// The cold drills a held drill waits on. A bank file of a node that is
/// not SOLID names in `after` a drill whose latest rep has gone cold; that
/// node cannot be served its own drill until the predecessor is warm
/// again, and the predecessor's own node, SOLID and off its clock, never
/// serves it. So the predecessor is wanted: due on its own node today,
/// whatever its clock says, and so is any cold drill it waits on in turn
/// (binary-search-on-answer, FRAGILE behind d115 after d98 of
/// binary-search-index, starved 19 days in the 2026-09-16 simulation).
fn wanted_drills(ctx: &Ctx, ev: &Evidence, day: NaiveDate) -> Rc<HashSet<PathBuf>> {
    if let Some(w) = ev.cold_cache().wanted.get(&day) {
        return w.clone();
    }
    let ro = &ctx.ro;
    let mut frontier: Vec<PathBuf> = Vec::new();
    for n in ctx.nodes.keys() {
        if node_status(ctx, n, ev, day).0 != SOLID {
            frontier.extend(ctx.bank_paths(n).iter().cloned());
        }
    }
    let mut wanted: HashSet<PathBuf> = HashSet::new();
    let mut seen: HashSet<PathBuf> = HashSet::new();
    while let Some(p) = frontier.pop() {
        if !seen.insert(p.clone()) {
            continue;
        }
        for a in ctx.drill_after(&p) {
            if ctx.vertex_kind(&a, &ro.map) != Some("drill")
                || warm(ctx, &a, ro, ev, day, false) != Some(false)
            {
                continue;
            }
            if let Some(ap) = ctx.drill_path(&a) {
                wanted.insert(ap.clone());
                frontier.push(ap);
            }
        }
    }
    // a recovery wants the drill under the move it recovered: the retest
    // waits for a clean rep of it since the recovery (recovery_wait)
    for (_, path) in recovery_waits(ctx, ev) {
        wanted.insert(path);
    }
    let w = Rc::new(wanted);
    ev.cold_cache().wanted.insert(day, w.clone());
    w
}

/// The moment of the file's last unaided clean rep (data::filed_at), ""
/// when it has none.
fn last_clean_drilled_at(ctx: &Ctx, path: &Path, ev: &Evidence) -> String {
    let key = ctx.drill_evidence_key(path);
    ev.drill_reps(&key)
        .iter()
        .filter(|&&i| anki_answer(&ev.drills[i].1, ev.rec(ev.drills[i].2)) == "good")
        .map(|&i| filed_at(&ev.drills[i].1, &ev.drills[i].0))
        .max()
        .unwrap_or_default()
}

/// The bank file a recovered problem's retest waits on: a drill of a move
/// the help touched, with no clean rep since the recovery. The least
/// recently drilled one when there are several. Since means after the
/// recovering file was filed, to the second: the drill rep served right
/// after the recovery, the same day, is the rep the wait asked for (d68
/// under 543, served again the next morning, 2026-09-22).
pub fn recovery_wait(ctx: &Ctx, ev: &Evidence, pnum: &str) -> Option<PathBuf> {
    let (since, _) = crate::clock::recovered_at(ev, pnum)?;
    crate::clock::recovery_moves(ev, pnum)
        .iter()
        .flat_map(|m| ctx.bank_paths(m).iter().cloned().collect::<Vec<_>>())
        .filter(|p| last_clean_drilled_at(ctx, p, ev) <= since)
        .min_by_key(|p| last_drilled(ctx, p, ev))
}

/// Every recovered problem still waiting on a drill: (problem, file).
pub fn recovery_waits(ctx: &Ctx, ev: &Evidence) -> Vec<(String, PathBuf)> {
    let mut out: Vec<(String, PathBuf)> = ev
        .by_problem
        .keys()
        .filter(|p| is_numeric_id(p))
        .filter_map(|p| recovery_wait(ctx, ev, p).map(|f| (p.clone(), f)))
        .collect();
    out.sort_by_key(|(p, _)| crate::data::pnum_key(p));
    out
}

/// The recovered problems none of whose moves has a bank file: (problem,
/// the moves). Nothing can be served under them, so the footer says so.
pub fn recoveries_without_drill(ctx: &Ctx, ev: &Evidence) -> Vec<(String, Vec<String>)> {
    let mut out: Vec<(String, Vec<String>)> = Vec::new();
    for p in ev.by_problem.keys() {
        if !is_numeric_id(p) || crate::clock::recovered_on(ev, p).is_none() {
            continue;
        }
        let moves = crate::clock::recovery_moves(ev, p);
        if !moves.is_empty() && moves.iter().all(|m| ctx.bank_paths(m).is_empty()) {
            out.push((p.clone(), moves));
        }
    }
    out.sort_by_key(|(p, _)| crate::data::pnum_key(p));
    out
}

/// The wanted file of `node` to serve today: servable, not yet done
/// today, least recently drilled first.
fn wanted_drill(ctx: &Ctx, node: &str, ev: &Evidence, day: NaiveDate) -> Option<PathBuf> {
    let wanted = wanted_drills(ctx, ev, day);
    let mine: Vec<PathBuf> = ctx
        .bank_paths(node)
        .iter()
        .filter(|p| wanted.contains(*p))
        .cloned()
        .collect();
    if mine.is_empty() {
        return None;
    }
    let today = day.format("%Y-%m-%d").to_string();
    servable_drills(ctx, &mine, ev, Some(node), false)
        .into_iter()
        .filter(|p| last_drilled(ctx, p, ev) < today)
        .min_by_key(|p| last_drilled(ctx, p, ev))
}

/// A bank file landed for `node` mid-run (kg_simulate authors one): the
/// answers kg_lib reads back from the directory on every call go, the
/// ones it memoises stay (Ctx::bank_authored).
pub fn bank_authored(ctx: &Ctx, ev: &Evidence, node: &str) {
    ctx.bank_authored(node);
    let mut c = ev.cold_cache();
    c.due_drill.retain(|(n, _, _, _), _| n != node);
    c.drills_left.retain(|(n, _), _| n != node);
}

/// kg_lib.cold_drill: the bank file of a node not warm yet; servable ones
/// first, and with `ready_only` none at all when none is servable.
pub fn cold_drill(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    today: NaiveDate,
    ready_only: bool,
) -> Option<PathBuf> {
    sync_caches(ctx, ev);
    let key = (node.to_string(), today);
    let hit = ev.cold_cache().cold.get(&key).cloned();
    let (ready, cold) = match hit {
        Some(h) => h,
        None => {
            let cold: Vec<PathBuf> = ctx
                .bank_files(node)
                .iter()
                .filter(|p| !drill_warm(ctx, p, ev, today))
                .cloned()
                .collect();
            let ready = if cold.is_empty() {
                vec![]
            } else {
                servable_drills(ctx, &cold, ev, Some(node), false)
            };
            ev.cold_cache()
                .cold
                .insert(key, (ready.clone(), cold.clone()));
            (ready, cold)
        }
    };
    if ready_only {
        return ready.first().cloned();
    }
    if cold.is_empty() {
        return None;
    }
    if ready.is_empty() {
        cold.first().cloned()
    } else {
        ready.first().cloned()
    }
}

/// kg_lib.node_drill_hold: the id of the node's cold drill, or None.
pub fn node_drill_hold(ctx: &Ctx, node: &str, ev: &Evidence, today: NaiveDate) -> Option<String> {
    let path = cold_drill(ctx, node, ev, today, false)?;
    ctx.drill_id(&path)
}

/// kg_lib.drill_gated: a MISSING/FRAGILE/deep-stale node with a bank trains
/// on its drill only.
pub fn drill_gated(
    ctx: &Ctx,
    node: &str,
    status: crate::status::Status,
    last: Option<NaiveDate>,
    today: NaiveDate,
) -> bool {
    if status == FRAGILE || status == MISSING {
        return ctx.has_drill_bank(node);
    }
    if status == STALE {
        if let Some(last) = last {
            if (today - last).num_days() > DEEP_STALE_DAYS {
                return ctx.has_drill_bank(node);
            }
        }
    }
    false
}

/// kg_lib.drill_held: a banked prereq must train first.
pub fn drill_held(
    ctx: &Ctx,
    node: &str,
    statuses: &Statuses,
    ev: &Evidence,
    pending: &HashSet<String>,
) -> bool {
    for p in ctx.prereqs(node) {
        if pending.contains(p) {
            return true;
        }
        if has_drill_bank(ctx, p)
            && statuses.contains_key(p)
            && (statuses[p].0 != SOLID || !owned(ev, p) || drills_left(ctx, p, ev, false))
        {
            return true;
        }
    }
    false
}

/// ctx.has_drill_bank, or the test's bank (the picker passed its own
/// has_drill_bank into kg_lib.drill_held).
pub fn has_drill_bank(ctx: &Ctx, node: &str) -> bool {
    #[cfg(test)]
    if let Some(b) = ctx.stub(|s| s.bank.contains(node)) {
        return b;
    }
    ctx.has_drill_bank(node)
}

/// kg_lib.drills_left: a drill of this node is never done and reachable.
pub fn drills_left(ctx: &Ctx, node: &str, ev: &Evidence, early: bool) -> bool {
    #[cfg(test)]
    if let Some(b) = ctx.stub(|s| s.undone.contains(node)) {
        return b;
    }
    sync_caches(ctx, ev);
    let key = (node.to_string(), early);
    if let Some(v) = ev.cold_cache().drills_left.get(&key) {
        return *v;
    }
    let v = drills_left_uncached(ctx, node, ev, early);
    ev.cold_cache().drills_left.insert(key, v);
    v
}

fn drills_left_uncached(ctx: &Ctx, node: &str, ev: &Evidence, early: bool) -> bool {
    let candidates: Vec<PathBuf> = ctx.bank_paths(node).as_ref().clone();
    let ro = &ctx.ro;
    let by_id: HashMap<String, PathBuf> = candidates
        .iter()
        .filter_map(|p| ctx.drill_id(p).map(|i| (i, p.clone())))
        .collect();
    let mut reachable: HashSet<PathBuf> = servable_drills(ctx, &candidates, ev, Some(node), early)
        .into_iter()
        .collect();
    let mut grew = true;
    while grew {
        grew = false;
        for path in &candidates {
            if reachable.contains(path) {
                continue;
            }
            if ctx
                .drill_trains(path)
                .iter()
                .any(|t| t != node && !owned(ev, t))
            {
                continue;
            }
            let unmet: Vec<String> = ctx
                .drill_after(path)
                .into_iter()
                .filter(|a| warm(ctx, a, ro, ev, ctx.today(), early) == Some(false))
                .collect();
            if unmet
                .iter()
                .all(|a| by_id.get(a).is_some_and(|p| reachable.contains(p)))
            {
                reachable.insert(path.clone());
                grew = true;
            }
        }
    }
    reachable
        .iter()
        .any(|p| last_drilled(ctx, p, ev).is_empty())
}

// ---- the SM-2 clock ----------------------------------------------------

/// `base` is the rep's solved filename as ev.drills carries it.
pub fn anki_answer(base: &str, rec: &Rec) -> &'static str {
    if rec.drill_clean(base) {
        match rec.assist_any() {
            "none" => return "good",
            "hint" => return "hard",
            _ => {}
        }
    }
    "again"
}

/// kg_lib.anki_due: (due date, interval) for a bank file, None never done.
pub fn anki_due(ctx: &Ctx, path: &Path, ev: &Evidence) -> Option<(NaiveDate, i64)> {
    anki_due_key(&ctx.drill_evidence_key(path), ev)
}

/// anki_due on the file's evidence key (ctx.drill_evidence_key).
pub fn anki_due_key(key: &str, ev: &Evidence) -> Option<(NaiveDate, i64)> {
    let st = anki_state(key, ev)?;
    Some((
        parse_date(&st.last) + Duration::days(st.interval),
        st.interval,
    ))
}

/// The SM-2 clock one step ahead: when the file is answered Good today,
/// (the day it comes back, that interval). A file never done graduates
/// to one day.
pub fn anki_next_if_good(key: &str, ev: &Evidence, today: NaiveDate) -> (NaiveDate, i64) {
    let (interval, ease, reps) =
        anki_state(key, ev).map_or((0, ANKI_EASE, 0), |s| (s.interval, s.ease, s.reps));
    let next = anki_fuzz(anki_good(interval, ease), key, reps);
    (today + Duration::days(next), next)
}

/// The clock's state after the file's last rep: the day of that rep, the
/// interval it set, the ease it left and the number of days it was done on.
struct AnkiState {
    last: String,
    interval: i64,
    ease: f64,
    reps: usize,
}

/// The fuzzed interval: `interval` shifted by up to its fuzz share, the
/// shift drawn from a hash of (key, rep). See ANKI_FUZZ_MIN_DAYS.
pub fn anki_fuzz(interval: i64, key: &str, rep: usize) -> i64 {
    if interval < ANKI_FUZZ_MIN_DAYS {
        return interval;
    }
    let share = if interval < 7 {
        0.15
    } else if interval < 21 {
        0.10
    } else {
        0.05
    };
    let width = ((interval as f64 * share).round() as i64).max(1);
    // FNV-1a over the key and the rep count: stable across Rust releases
    let mut h: u64 = 0xcbf2_9ce4_8422_2325;
    for b in key.bytes().chain(rep.to_le_bytes()) {
        h ^= u64::from(b);
        h = h.wrapping_mul(0x0000_0100_0000_01b3);
    }
    let shift = (h % (2 * width as u64 + 1)) as i64 - width;
    (interval + shift).clamp(ANKI_FUZZ_MIN_DAYS, ANKI_MAX_INTERVAL)
}

pub(crate) fn anki_good(interval: i64, ease: f64) -> i64 {
    let next = if interval == 0 {
        ANKI_GRADUATING_DAYS
    } else {
        (interval + 1).max((interval as f64 * ease + 0.5) as i64)
    };
    next.min(ANKI_MAX_INTERVAL)
}

fn anki_state(key: &str, ev: &Evidence) -> Option<AnkiState> {
    let mut reps: Vec<usize> = ev.drill_reps(key).to_vec();
    reps.sort_by(|&a, &b| {
        let (da, ba, _) = &ev.drills[a];
        let (db, bb, _) = &ev.drills[b];
        (da, ba).cmp(&(db, bb))
    });
    if reps.is_empty() {
        return None;
    }
    let mut by_day: Vec<(String, usize)> = Vec::new();
    for i in reps {
        let d = &ev.drills[i].0;
        match by_day.iter_mut().find(|(day, _)| day == d) {
            Some(slot) => slot.1 = i,
            None => by_day.push((d.clone(), i)),
        }
    }
    by_day.sort_by(|a, b| a.0.cmp(&b.0));
    let (mut interval, mut ease) = (0i64, ANKI_EASE);
    let mut last = String::new();
    let mut days_done = 0usize;
    for (d, i) in by_day {
        let (_, base, ri) = &ev.drills[i];
        match anki_answer(base, ev.rec(*ri)) {
            "good" => interval = anki_good(interval, ease),
            "hard" => {
                interval = if interval == 0 {
                    ANKI_GRADUATING_DAYS
                } else {
                    (interval + 1).max((interval as f64 * ANKI_HARD_FACTOR + 0.5) as i64)
                };
                ease = ANKI_EASE_MIN.max(ease - ANKI_HARD_EASE_STEP);
            }
            _ => {
                interval = ANKI_GRADUATING_DAYS;
                ease = ANKI_EASE_MIN.max(ease - ANKI_AGAIN_EASE_STEP);
            }
        }
        interval = anki_fuzz(interval.min(ANKI_MAX_INTERVAL), key, days_done);
        days_done += 1;
        last = d;
    }
    Some(AnkiState {
        last,
        interval,
        ease,
        reps: days_done,
    })
}

/// The place of a bank file in the `make drill` queue, smallest first:
/// a never-drilled file, then the file due soonest on its SM-2 clock, and
/// among files due the same day the one solved longest ago. The second
/// element is the timestamp part of the latest solved basename ("" if
/// never), so two files solved the same day still order by time.
pub fn drill_queue_key(key: &str, ev: &Evidence) -> (NaiveDate, String) {
    let due = anki_due_key(key, ev).map_or(NaiveDate::MIN, |(d, _)| d);
    let last = ev
        .drill_reps(key)
        .iter()
        .map(|&i| ev.drills[i].1[key.len()..].to_string())
        .max()
        .unwrap_or_default();
    (due, last)
}

/// kg_lib.anki_rank: the sort key of a file due today, or None.
pub type AnkiKey = (i64, NaiveDate, usize, usize, PathBuf);

pub fn anki_rank(
    ctx: &Ctx,
    path: &Path,
    ev: &Evidence,
    day: NaiveDate,
    depth: usize,
) -> Option<AnkiKey> {
    if last_drilled(ctx, path, ev).as_str() >= day.format("%Y-%m-%d").to_string().as_str() {
        return None;
    }
    match anki_due(ctx, path, ev) {
        None => Some((
            1,
            NaiveDate::MIN,
            depth,
            ctx.drill_after(path).len(),
            path.to_path_buf(),
        )),
        Some((due, _)) => {
            if due > day {
                None
            } else {
                Some((0, due, 0, 0, path.to_path_buf()))
            }
        }
    }
}

/// kg_lib.anki_frontier: every bank file due on its own clock, as (path,
/// node): reviews most overdue first, then files never done, atoms
/// first; a due drill's due predecessors come before it.
/// kg_lib.anki_rank of every bank file for (day, assisted) at depth 0,
/// computed once per evidence version; a file the assisted filter drops
/// is absent.
fn anki_table(
    ctx: &Ctx,
    ev: &Evidence,
    day: NaiveDate,
    assisted: bool,
) -> Rc<HashMap<PathBuf, Option<AnkiKey>>> {
    let key = (day, assisted);
    if let Some(t) = ev.cold_cache().anki.get(&key) {
        return t.clone();
    }
    let mut table = HashMap::new();
    for node in ctx.nodes.keys() {
        for path in ctx.bank_paths(node).iter() {
            if assisted && !drill_assisted(ctx, path, ev) {
                continue;
            }
            let r = anki_rank(ctx, path, ev, day, 0);
            table.insert(path.clone(), r);
        }
    }
    let table = Rc::new(table);
    ev.cold_cache().anki.insert(key, table.clone());
    table
}

pub fn anki_frontier(
    ctx: &Ctx,
    ev: &Evidence,
    day: NaiveDate,
    nodes: Option<&crate::data::Nodes>,
    node_ids: Option<&[String]>,
    assisted: bool,
) -> Vec<(PathBuf, String)> {
    let table = anki_table(ctx, ev, day, assisted);
    let nodes = nodes.unwrap_or(&ctx.nodes);
    let mut ids: Vec<String> = match node_ids {
        Some(ids) => ids.to_vec(),
        None => nodes.keys().cloned().collect(),
    };
    ids.sort();
    let mut ranked: Vec<(AnkiKey, PathBuf, String)> = Vec::new();
    for node in &ids {
        let depth = if nodes.contains_key(node) {
            input_tree(std::slice::from_ref(node), nodes).len()
        } else {
            0
        };
        for path in ctx.bank_paths(node).iter() {
            // the table holds the rank at depth 0 for the files the
            // assisted filter keeps; a never-done file's key carries the
            // depth, filled in here
            let hit = match table.get(path) {
                Some(r) => r.clone(),
                None if assisted => continue,
                None => anki_rank(ctx, path, ev, day, depth),
            };
            if let Some(mut key) = hit {
                if key.0 == 1 {
                    key.2 = depth;
                }
                ranked.push((key, path.clone(), node.clone()));
            }
        }
    }
    ranked.sort_by(|a, b| a.0.cmp(&b.0));
    let due: HashMap<PathBuf, String> = ranked
        .iter()
        .map(|(_, p, n)| (p.clone(), n.clone()))
        .collect();
    let mut out: Vec<(PathBuf, String)> = Vec::new();
    let mut seen: HashSet<PathBuf> = HashSet::new();
    fn emit(
        ctx: &Ctx,
        path: Option<PathBuf>,
        due: &HashMap<PathBuf, String>,
        seen: &mut HashSet<PathBuf>,
        out: &mut Vec<(PathBuf, String)>,
    ) {
        // drill_path(a) may be None (a predecessor with no bank file):
        // Python then recurses with path None and stops there
        let Some(path) = path else { return };
        if seen.contains(&path) {
            return;
        }
        seen.insert(path.clone());
        for a in ctx.drill_after(&path) {
            emit(ctx, ctx.drill_path(&a), due, seen, out);
        }
        if let Some(n) = due.get(&path) {
            out.push((path, n.clone()));
        }
    }
    for (_, path, _) in &ranked {
        emit(ctx, Some(path.clone()), &due, &mut seen, &mut out);
    }
    out
}

/// kg_lib.due_drill: the bank file to serve a node today, or None.
pub fn due_drill(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    day: NaiveDate,
    early: bool,
    assisted: bool,
) -> Option<PathBuf> {
    sync_caches(ctx, ev);
    if !early && !assisted {
        // a wanted file outranks the node's own clock; the answer depends
        // on every node's status, so it is never memoised per node
        if let Some(p) = wanted_drill(ctx, node, ev, day) {
            return Some(p);
        }
    }
    let key = (node.to_string(), day, early, assisted);
    if let Some(d) = ev.cold_cache().due_drill.get(&key) {
        return d.clone();
    }
    let d = due_drill_uncached(ctx, node, ev, day, early, assisted);
    ev.cold_cache().due_drill.insert(key, d.clone());
    d
}

fn due_drill_uncached(
    ctx: &Ctx,
    node: &str,
    ev: &Evidence,
    day: NaiveDate,
    early: bool,
    assisted: bool,
) -> Option<PathBuf> {
    let (status, _) = node_status(ctx, node, ev, day);
    if anki() {
        let empty = crate::data::Nodes::new();
        let ranked = anki_frontier(
            ctx,
            ev,
            day,
            Some(&empty),
            Some(&[node.to_string()]),
            assisted,
        );
        if let Some((p, _)) = ranked.first() {
            return Some(p.clone());
        }
    }
    let carriers = ctx.ro.carrier_counts(ctx).get(node).copied().unwrap_or(0);
    let g = graduation_due(ev, node, carriers);
    let at_floor = g.is_some_and(|(d, _)| d <= day);
    let holds = status == SOLID
        && owned(ev, node)
        && !early
        && !assisted
        && !drills_left(ctx, node, ev, false)
        && !at_floor;
    let today = day.format("%Y-%m-%d").to_string();
    let mut candidates: Vec<PathBuf> = ctx.bank_paths(node).as_ref().clone();
    if assisted || holds {
        candidates.retain(|p| drill_assisted(ctx, p, ev));
    }
    if candidates.is_empty() {
        return None;
    }
    let pool = if assisted {
        candidates
    } else {
        servable_drills(ctx, &candidates, ev, Some(node), early)
    };
    if pool.is_empty() {
        return None;
    }
    let path = pool
        .iter()
        .min_by_key(|p| last_drilled(ctx, p, ev))
        .cloned()
        .unwrap();
    if last_drilled(ctx, &path, ev) >= today {
        None
    } else {
        Some(path)
    }
}

// ---- the budgets --------------------------------------------------------

/// kg_lib.group_caps: KG_GROUP_CAP, "sql=3,graphs=2".
pub fn group_caps() -> Vec<(String, i64)> {
    let raw = env_str("KG_GROUP_CAP");
    let mut out: Vec<(String, i64)> = Vec::new();
    for part in raw.split(',') {
        let (name, count) = part.split_once('=').unwrap_or((part, ""));
        let name = name.trim();
        let count = count.trim();
        if !name.is_empty() && !count.is_empty() && count.chars().all(|c| c.is_ascii_digit()) {
            let v: i64 = count.parse().unwrap_or(0);
            match out.iter_mut().find(|(n, _)| n == name) {
                Some(slot) => slot.1 = v,
                None => out.push((name.to_string(), v)),
            }
        }
    }
    out
}

fn env_int(name: &str) -> Option<i64> {
    let raw = env_str(name);
    let raw = raw.trim();
    if !raw.is_empty() && raw.chars().all(|c| c.is_ascii_digit()) {
        raw.parse().ok()
    } else {
        None
    }
}

pub fn new_drill_cap() -> Option<i64> {
    env_int("MAX_NEW_DRILLS")
}

pub fn drill_review_cap() -> Option<i64> {
    env_int("MAX_DRILL_REVIEWS")
}

/// kg_lib.reviews_first: REVIEWS_FIRST set to anything but "" or "0".
pub fn reviews_first() -> bool {
    let raw = env_str("REVIEWS_FIRST");
    let raw = raw.trim();
    !(raw.is_empty() || raw == "0")
}

pub fn new_drills_today(ev: &Evidence, day: NaiveDate) -> i64 {
    let d = day.format("%Y-%m-%d").to_string();
    ev.date_recs(&d)
        .iter()
        .filter(|i| ev.first_reps.contains(i))
        .count() as i64
}

pub fn drill_reviews_today(ev: &Evidence, day: NaiveDate) -> i64 {
    let d = day.format("%Y-%m-%d").to_string();
    ev.date_recs(&d)
        .iter()
        .filter(|&&i| drill_key(ev.fname(i)).is_some() && !ev.first_reps.contains(&i))
        .count() as i64
}

pub fn new_drills_left(ev: &Evidence, day: NaiveDate) -> Option<i64> {
    new_drill_cap().map(|c| c - new_drills_today(ev, day))
}

pub fn drill_reviews_left(ev: &Evidence, day: NaiveDate) -> Option<i64> {
    drill_review_cap().map(|c| c - drill_reviews_today(ev, day))
}

/// kg_lib.drill_capped: the day's budget for this file is spent.
pub fn drill_capped(ctx: &Ctx, path: &Path, ev: &Evidence, day: NaiveDate) -> bool {
    let left = if !last_drilled(ctx, path, ev).is_empty() {
        drill_reviews_left(ev, day)
    } else {
        new_drills_left(ev, day)
    };
    left.is_some_and(|l| l <= 0)
}

/// kg_lib.group_reps: reps dated `day` whose walk touches the group.
pub fn group_reps(ctx: &Ctx, group: &str, ev: &Evidence, day: NaiveDate) -> i64 {
    let d = day.format("%Y-%m-%d").to_string();
    ev.date_recs(&d)
        .iter()
        .filter(|&&i| {
            ev.rec(i)
                .moves
                .keys()
                .any(|m| ctx.group_of(m) == Some(group))
        })
        .count() as i64
}

/// kg_lib.drill_recall: (recall, clean days, gap, copies) for one file.
pub fn drill_recall(
    ctx: &Ctx,
    path: &Path,
    ev: &Evidence,
    today: NaiveDate,
) -> Option<(Option<f64>, i64, i64, i64)> {
    let cv = ctx.curve.as_ref()?;
    let key = ctx.drill_evidence_key(path);
    let mut reps: Vec<usize> = ev.drill_reps(&key).to_vec();
    reps.sort_by(|&a, &b| {
        let (da, ba, _) = &ev.drills[a];
        let (db, bb, _) = &ev.drills[b];
        (da, ba).cmp(&(db, bb))
    });
    if reps.is_empty() {
        return None;
    }
    let mut by_day: Vec<(String, usize)> = Vec::new();
    for i in &reps {
        let (d, _, ri) = &ev.drills[*i];
        match by_day.iter_mut().find(|(day, _)| day == d) {
            Some(slot) => slot.1 = *ri,
            None => by_day.push((d.clone(), *ri)),
        }
    }
    let mut clean_days: Vec<String> = Vec::new();
    let mut struggles = 0.0;
    for (d, ri) in &by_day {
        let rec = ev.rec(*ri);
        if rec.moves.is_empty() {
            continue;
        }
        if rec.moves.values().all(|v| v == "clean") {
            if rec.assist_any() != "learning" {
                clean_days.push(d.clone());
            }
        } else {
            struggles += 1.0;
        }
    }
    let copies = by_day
        .iter()
        .filter(|(_, ri)| ev.rec(*ri).assist_any() == "learning")
        .count() as i64;
    if clean_days.is_empty() {
        let latest = by_day.iter().map(|(d, _)| d.as_str()).max().unwrap();
        let gap = (today - parse_date(latest)).num_days().max(0);
        return Some((None, 0, gap, copies));
    }
    let mut assisted = 0.0;
    for i in &reps {
        assisted += assist_weight(ev.rec(ev.drills[*i].2).assist_any());
    }
    let cn = ctx
        .drill_trains(path)
        .iter()
        .filter_map(|n| cv.conn.get(n).copied())
        .fold(None, |m: Option<f64>, x| Some(m.map_or(x, |m| m.max(x))))
        .unwrap_or(cv.conn_mean);
    let stability =
        (cv.a + cv.b * (clean_days.len() as f64).ln_1p() - cv.c * struggles - cv.d * assisted
            + cv.e * (cn - cv.conn_mean))
            .exp()
            .clamp(7.0, 3650.0);
    let latest_clean = clean_days.iter().max().unwrap();
    let gap = (today - parse_date(latest_clean)).num_days().max(0);
    let memory = (1.0 + gap as f64 / stability).powf(-cv.beta);
    Some((
        Some((1.0 - cv.slip) * memory),
        clean_days.len() as i64,
        gap,
        copies,
    ))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::data::Assist;
    use indexmap::IndexMap;

    fn rec(date: &str) -> Rec {
        let mut moves = IndexMap::new();
        moves.insert("grid-neighbors".to_string(), "clean".to_string());
        Rec {
            date: date.to_string(),
            problem: Some("drill".to_string()),
            moves,
            assist: Assist::None,
            followup: None,
            pending: None,
            note: None,
            judge: None,
            seconds: None,
        }
    }

    /// 2026-09-13: `make drill grid-neighbors` served Count Cells four
    /// times in a row. Every file of the node had a rep that day, the
    /// picker keyed on the date alone, and min_by_key kept the first of
    /// the tie: the bank's first file, however recently it was solved.
    #[test]
    fn same_day_reps_order_by_time_not_bank_order() {
        let ev = Evidence::new(vec![
            (
                "solved/d_Count_Cells_2026_09_13T07_04_17Z.py".to_string(),
                rec("2026-09-13"),
            ),
            (
                "solved/d_Neighbour_Values_2026_09_13T07_08_33Z.py".to_string(),
                rec("2026-09-13"),
            ),
            (
                "solved/d_Neighbour_Counts_2026_09_13T07_14_11Z.py".to_string(),
                rec("2026-09-13"),
            ),
            (
                "solved/d_Count_Cells_2026_09_13T07_15_31Z.py".to_string(),
                rec("2026-09-13"),
            ),
        ]);
        let keys = [
            "d_count_cells_",
            "d_neighbour_values_",
            "d_neighbour_counts_",
        ];
        let next = keys.iter().min_by_key(|k| drill_queue_key(k, &ev)).unwrap();
        assert_eq!(*next, "d_neighbour_values_");
        // the file just solved is at the back
        let last = keys.iter().max_by_key(|k| drill_queue_key(k, &ev)).unwrap();
        assert_eq!(*last, "d_count_cells_");
        // a file never drilled outranks every drilled one
        assert!(drill_queue_key("d_nearest_one_", &ev) < drill_queue_key(next, &ev));
    }

    #[test]
    fn due_date_outranks_last_rep_time() {
        let ev = Evidence::new(vec![
            // drilled twice: interval 1 then 3, due 09-15
            (
                "solved/d_A_2026_09_11T01_00_00Z.py".to_string(),
                rec("2026-09-11"),
            ),
            (
                "solved/d_A_2026_09_12T01_00_00Z.py".to_string(),
                rec("2026-09-12"),
            ),
            // drilled once, later in the day, due 09-14
            (
                "solved/d_B_2026_09_13T09_00_00Z.py".to_string(),
                rec("2026-09-13"),
            ),
        ]);
        assert!(drill_queue_key("d_b_", &ev) < drill_queue_key("d_a_", &ev));
    }
}
