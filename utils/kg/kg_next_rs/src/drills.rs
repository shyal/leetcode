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
use crate::data::{assist_weight, env_str, parse_date, Rec, SOLID_WINDOW_DAYS};
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
    best.map(|i| ev.rec(ev.drills[i].2))
}

pub fn drill_clean(ctx: &Ctx, path: &Path, ev: &Evidence) -> bool {
    latest_drill_rep(ctx, path, ev).is_some_and(Rec::all_clean)
}

pub fn drill_assisted(ctx: &Ctx, path: &Path, ev: &Evidence) -> bool {
    match latest_drill_rep(ctx, path, ev) {
        None => false,
        Some(rec) => !(rec.all_clean() && rec.assist_any() == "none"),
    }
}

pub fn drill_warm(ctx: &Ctx, path: &Path, ev: &Evidence, today: NaiveDate) -> bool {
    match latest_drill_rep(ctx, path, ev) {
        None => false,
        Some(rec) => {
            rec.all_clean()
                && rec.assist_any() == "none"
                && (today - parse_date(&rec.date)).num_days() <= SOLID_WINDOW_DAYS
        }
    }
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
        if ctx.has_drill_bank(p)
            && statuses.contains_key(p)
            && (statuses[p].0 != SOLID || !owned(ev, p) || drills_left(ctx, p, ev, false))
        {
            return true;
        }
    }
    false
}

/// kg_lib.drills_left: a drill of this node is never done and reachable.
pub fn drills_left(ctx: &Ctx, node: &str, ev: &Evidence, early: bool) -> bool {
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

pub fn anki_answer(rec: &Rec) -> &'static str {
    if rec.all_clean() {
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
    for i in reps {
        let (d, _, ri) = &ev.drills[i];
        match by_day.iter_mut().find(|(day, _)| day == d) {
            Some(slot) => slot.1 = *ri,
            None => by_day.push((d.clone(), *ri)),
        }
    }
    by_day.sort_by(|a, b| a.0.cmp(&b.0));
    let (mut interval, mut ease) = (0i64, ANKI_EASE);
    let mut last = String::new();
    for (d, ri) in by_day {
        match anki_answer(ev.rec(ri)) {
            "good" => {
                interval = if interval == 0 {
                    ANKI_GRADUATING_DAYS
                } else {
                    (interval + 1).max((interval as f64 * ease + 0.5) as i64)
                };
            }
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
        interval = interval.min(ANKI_MAX_INTERVAL);
        last = d;
    }
    Some((parse_date(&last) + Duration::days(interval), interval))
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
