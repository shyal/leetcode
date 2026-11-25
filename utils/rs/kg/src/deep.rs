// The deep dive (KG_DEEP, 2026-11-11): one technique a day, its problems
// easy to hard, the memory work after.
//
// Every other rule of the picker picks one problem at a time, and each
// pick can be a different technique. A book does the opposite: EPI and the
// NeetCode roadmap give every problem of one topic, easy to hard, and then
// the next topic. The report of 2026-11-11 found the cost of the first
// way: a technique passes in the form its drill has and fails in a
// changed form (plain Dijkstra against Dijkstra with a second record per
// city, on one day).
//
// KG_DEEP=N (.envrc) switches the mode on, N the new problems of the day's
// technique; unset or 0 is off and the picker is what it was. With it on,
// a day is (2026-11-13; before that the technique's one drill came first
// and never did, and three days had 8 problems and no drill):
//   1. the language drills due on the clock (sql, ts, python, rust,
//      design), within their caps: syntax memory, and the clock is the
//      tool for it;
//   2. the drills of the day's technique that are due on the clock, and
//      those of its direct prerequisites and of the techniques built
//      directly on it (linked, 2026-11-26: "Formulate DP state" has no
//      drill of its own, and 309 came before three due DP drills);
//   2b. the drills never done of the other algorithm techniques, a set
//      file apart (2026-11-20, pick::pick): a technique gets a day only
//      after a first sight needed it, so the drills of a new technique
//      were never served. MAX_NEW_DRILLS is the limit;
//   3. the problems of the technique, in turns: a problem he has never
//      met, then a repeat, until N never-met problems are done; then
//      repeats only. The never-met problems go easy to hard. The repeats
//      are the due ones, easy to hard, then the ones that are not due,
//      the one he did longest ago first. A repeat that is not due is
//      served only clock::PROBLEM_GRADUATING_DAYS days or more after its
//      last record (2026-11-20; before that it came back the next day).
// A day is one topic (his word, 2026-11-16): no problem of another
// technique is served, due or not. Before that date the due repeats of
// every other technique came after step 3, and on 2026-11-16 the queue
// was three problems of the technique and then seven of other topics.
// A drill of the day's technique holds none of its problems (2026-11-14,
// bank::held_behind_past): step 2 serves it first, and while it was cold
// it held every problem of steps 3 and 4.
// The drills of every other algorithm technique that he has done are not
// served that day, due or not: depth comes before the memory curves (his thesis,
// 2026-11-13), and a technique's drills come back on its own day. Steps 1
// and 2 are in pick::pick, step 3 in pick() here.
// A named group, cram, early, assisted and a woken problem are his own
// call and go past the mode, as they go past the caps.
//
// The technique of the day is the weakest one (weakness): of the problems
// met for the first time in the last DEEP_WINDOW_DAYS days that needed
// it, the share solved alone. Drills and repeats do not count: a clean
// drill says the code can be written again, not that the technique is
// seen in a new problem (156 of 176 nodes were SOLID on 2026-11-11 while
// 1D bottom-up DP failed two first sights in a month). The share is read
// at the upper end of its confidence interval (DEEP_Z), so one fail on a
// technique met once does not put it first. Records of today are left
// out, so the technique does not change during the day.
//
// A problem needs a technique when his own record of it names the move,
// or when a walk of the problem in graph/problems.json does (the drafted
// walks of kg_draft: for a fail the record holds what his code did, the
// walk what the solution needed).
//
// The new problems of step 3 are the never-met problems whose walk names the
// technique. A technique with none takes the never-met problems of its
// group. They are served by rating: the first of the day at or below the
// median rating of his alone first sights on the technique
// (DEEP_START_QUANTILE), after a pass the next one above it, after a
// fail the nearest at or below it. With FIRST_SIGHT_WITHIN_BAND set, a
// problem rated more than the band below his first-sight elo is not a
// candidate (2026-11-14: a day of 1301 to 1474 at elo 1609). Nor is one
// rated more than the band above it (2026-11-24: 1806 at elo 1609); when
// no candidate is in the band, the one nearest to his elo is served.
//
// A problem of the day that something holds is not passed over: what holds
// it is served first (pick::open), a drill of another technique included
// (2026-11-24). One whose holder cannot be served today is passed over.

use std::cell::RefCell;
use std::collections::{HashMap, HashSet};

use chrono::{Duration, NaiveDate};

use crate::clock::{attempt_label, is_studied, PROBLEM_GRADUATING_DAYS};
use crate::ctx::{Ctx, PView};
use crate::data::{env_str, filed_at, is_numeric_id, parse_date, pnum_key, Problem};
use crate::drills::{first_sight_range, in_group, ALGORITHMS};
use crate::evidence::Evidence;
use crate::model::solve_ratings;
use crate::pick::{clock_servable, open, reviews_due, Choice, Open, PickArgs};
use crate::status::{st, Statuses};

/// How wide the confidence interval of a technique's alone share is, in
/// standard errors (1.645: one side at 95%). The technique is ranked on
/// the upper end.
pub const DEEP_Z: f64 = 1.645;
/// The first sights that count toward a technique's weakness.
pub const DEEP_WINDOW_DAYS: i64 = 60;
/// Where the first new problem of the day sits among the ratings of the
/// first sights he solved alone on the technique.
pub const DEEP_START_QUANTILE: f64 = 0.5;

/// KG_DEEP: the new problems of the day's technique; 0 is off.
pub fn budget() -> i64 {
    env_str("KG_DEEP").trim().parse::<i64>().unwrap_or(0).max(0)
}

/// The first record of one problem.
#[derive(Clone, Debug)]
pub struct Sight {
    pub pnum: String,
    pub date: NaiveDate,
    /// no FAILED file, every move clean, no help
    pub alone: bool,
    /// the moves his record names
    pub moves: Vec<String>,
    filed: String,
}

/// Every problem's first record, oldest first. A problem whose first
/// record is a `make studied` file was read, not tried, and has none.
pub fn first_sights(ev: &Evidence) -> Vec<Sight> {
    let mut first: HashMap<String, (String, usize)> = HashMap::new();
    for (i, (fname, r)) in ev.recs.iter().enumerate() {
        let Some(p) = r.problem.as_deref().filter(|p| is_numeric_id(p)) else {
            continue;
        };
        if ev.is_drill(i) {
            continue;
        }
        let key = (filed_at(fname, &r.date), i);
        match first.get(p) {
            Some(k) if *k <= key => {}
            _ => {
                first.insert(p.to_string(), key);
            }
        }
    }
    let mut out: Vec<Sight> = first
        .into_iter()
        .filter(|(_, (_, i))| !is_studied(ev.fname(*i)))
        .map(|(pnum, (filed, i))| {
            let r = ev.rec(i);
            Sight {
                pnum,
                date: parse_date(&r.date),
                alone: attempt_label(ev.fname(i), r) == "clean",
                moves: r.moves.keys().cloned().collect(),
                filed,
            }
        })
        .collect();
    out.sort_by(|a, b| (&a.filed, pnum_key(&a.pnum)).cmp(&(&b.filed, pnum_key(&b.pnum))));
    out
}

/// The problems table entry of a problem, evidenced or drafted.
fn entry<'a>(ctx: &'a Ctx, pnum: &str) -> Option<&'a Problem> {
    ctx.all_problems()
        .get(pnum)
        .or_else(|| ctx.predicted.get(pnum))
}

/// The moves a problem needs: its own and those of its walks.
fn needs(p: &Problem) -> impl Iterator<Item = &String> {
    p.moves
        .iter()
        .chain(p.walks.iter().flat_map(|w| w.moves.iter()))
}

/// The technique, or its whole group when the technique has no problem
/// left that he has never met.
#[derive(Clone, Debug, PartialEq)]
pub enum Scope {
    Node(String),
    Group(String),
}

impl Scope {
    fn covers(&self, ctx: &Ctx, p: &Problem) -> bool {
        match self {
            Scope::Node(n) => needs(p).any(|m| m == n),
            Scope::Group(g) => needs(p).any(|m| ctx.group_of(m) == Some(g.as_str())),
        }
    }
}

/// One technique's first sights in the window.
#[derive(Clone, Debug)]
pub struct Weak {
    pub node: String,
    pub met: i64,
    pub alone: i64,
    /// the alone share at the upper end of its interval
    pub bound: f64,
}

/// Wilson's upper bound on k of n at z standard errors.
fn upper(k: i64, n: i64, z: f64) -> f64 {
    if n == 0 {
        return 1.0;
    }
    let (k, n) = (k as f64, n as f64);
    let p = k / n;
    let z2 = z * z;
    (p + z2 / (2.0 * n) + z * (p * (1.0 - p) / n + z2 / (4.0 * n * n)).sqrt()) / (1.0 + z2 / n)
}

/// The algorithm techniques met on a first sight in the window before
/// `today`, weakest first.
pub fn weakness(ctx: &Ctx, ev: &Evidence, today: NaiveDate) -> Vec<Weak> {
    let since = today - Duration::days(DEEP_WINDOW_DAYS);
    let mut tally: HashMap<String, (i64, i64)> = HashMap::new();
    for s in first_sights(ev) {
        if s.date < since || s.date >= today {
            continue;
        }
        let mut nodes: HashSet<&String> = s.moves.iter().collect();
        if let Some(p) = entry(ctx, &s.pnum) {
            nodes.extend(needs(p));
        }
        for n in nodes {
            if !ctx.nodes.contains_key(n) || !in_group(ctx, n, ALGORITHMS) {
                continue;
            }
            let t = tally.entry(n.clone()).or_insert((0, 0));
            t.0 += 1;
            t.1 += s.alone as i64;
        }
    }
    let mut out: Vec<Weak> = tally
        .into_iter()
        .map(|(node, (met, alone))| Weak {
            bound: upper(alone, met, DEEP_Z),
            node,
            met,
            alone,
        })
        .collect();
    out.sort_by(|a, b| {
        a.bound
            .partial_cmp(&b.bound)
            .unwrap()
            .then_with(|| b.met.cmp(&a.met))
            .then_with(|| a.node.cmp(&b.node))
    });
    out
}

/// The rated, servable problems in scope with no record before `day`,
/// easiest first. `day` None: with no record at all.
pub fn cluster(
    ctx: &Ctx,
    ev: &Evidence,
    scope: &Scope,
    day: Option<NaiveDate>,
    ratings: &HashMap<String, f64>,
) -> Vec<(String, f64)> {
    let mut seen: HashSet<&String> = HashSet::new();
    let mut out: Vec<(String, f64)> = Vec::new();
    for (num, p) in ctx.all_problems().iter().chain(ctx.predicted.iter()) {
        if !seen.insert(num) || !is_numeric_id(num) || !scope.covers(ctx, p) {
            continue;
        }
        let Some(r) = ratings.get(num) else { continue };
        if ctx.unservable(num, p) {
            continue;
        }
        let met = ev
            .problem_recs(num)
            .iter()
            .any(|(date, _, _)| day.is_none_or(|d| parse_date(date) < d));
        if !met {
            out.push((num.clone(), *r));
        }
    }
    out.sort_by(|a, b| {
        a.1.partial_cmp(&b.1)
            .unwrap()
            .then_with(|| pnum_key(&a.0).cmp(&pnum_key(&b.0)))
    });
    out
}

/// The technique of the day and where its new problems come from: the
/// weakest technique that had a never-met problem when the day began.
pub fn technique(
    ctx: &Ctx,
    ev: &Evidence,
    today: NaiveDate,
    ratings: &HashMap<String, f64>,
) -> Option<(Weak, Scope)> {
    for w in weakness(ctx, ev, today) {
        let node = Scope::Node(w.node.clone());
        if !cluster(ctx, ev, &node, Some(today), ratings).is_empty() {
            return Some((w, node));
        }
        if let Some(g) = ctx.group_of(&w.node) {
            let group = Scope::Group(g.to_string());
            if !cluster(ctx, ev, &group, Some(today), ratings).is_empty() {
                return Some((w, group));
            }
        }
    }
    None
}

/// The rating the first new problem of the day starts at: the
/// DEEP_START_QUANTILE of the ratings of the first sights he solved alone
/// on the technique, in the window when it has any, else ever.
fn start_level(
    ctx: &Ctx,
    sights: &[Sight],
    node: &str,
    today: NaiveDate,
    ratings: &HashMap<String, f64>,
) -> Option<f64> {
    let scope = Scope::Node(node.to_string());
    let since = today - Duration::days(DEEP_WINDOW_DAYS);
    let rated = |recent: bool| -> Vec<f64> {
        let mut v: Vec<f64> = sights
            .iter()
            .filter(|s| s.alone && s.date < today && (!recent || s.date >= since))
            .filter(|s| {
                s.moves.iter().any(|m| m == node)
                    || entry(ctx, &s.pnum).is_some_and(|p| scope.covers(ctx, p))
            })
            .filter_map(|s| ratings.get(&s.pnum).copied())
            .collect();
        v.sort_by(|a, b| a.partial_cmp(b).unwrap());
        v
    };
    let mut v = rated(true);
    if v.is_empty() {
        v = rated(false);
    }
    if v.is_empty() {
        return None;
    }
    let i = ((v.len() - 1) as f64 * DEEP_START_QUANTILE).round() as usize;
    Some(v[i])
}

/// The hardest candidate at or below `anchor`, else the easiest above.
fn at_or_below(cands: &[(String, f64)], anchor: f64) -> Option<&(String, f64)> {
    cands
        .iter()
        .rfind(|(_, r)| *r <= anchor)
        .or_else(|| cands.first())
}

/// The easiest candidate above `anchor`, else the hardest below.
fn above(cands: &[(String, f64)], anchor: f64) -> Option<&(String, f64)> {
    cands
        .iter()
        .find(|(_, r)| *r > anchor)
        .or_else(|| cands.last())
}

/// The candidates rated in `range` (drills::first_sight_range). When there
/// is none, the candidate nearest to the middle of it, his elo, so the day
/// still has a problem.
fn in_range(cands: Vec<(String, f64)>, range: Option<(f64, f64)>) -> Vec<(String, f64)> {
    let Some((lo, hi)) = range else { return cands };
    let elo = (lo + hi) / 2.0;
    let nearest = cands
        .iter()
        .min_by(|a, b| (a.1 - elo).abs().total_cmp(&(b.1 - elo).abs()))
        .cloned();
    let kept: Vec<(String, f64)> = cands
        .into_iter()
        .filter(|(_, r)| (lo..=hi).contains(r))
        .collect();
    if kept.is_empty() {
        nearest.into_iter().collect()
    } else {
        kept
    }
}

/// The technique of the day, where its new problems come from, and the
/// ratings they are served by.
pub struct Day {
    pub weak: Weak,
    pub scope: Scope,
    ratings: HashMap<String, f64>,
}

/// Whether the mode has a say in this pick: KG_DEEP is set and the pick is
/// not one of his own calls.
pub fn on(args: &PickArgs) -> bool {
    budget() > 0
        && args.group.is_none()
        && !args.cram
        && !args.early
        && !args.assisted
        && args.woken.is_empty()
}

/// The day of the mode; None when the mode is off or no technique has a
/// problem left, and the ordinary picker runs.
pub fn day(ctx: &Ctx, ev: &Evidence, args: &PickArgs) -> Option<Day> {
    if !on(args) {
        return None;
    }
    let today = ctx.today();
    let ratings = solve_ratings(ctx);
    let (weak, scope) = technique(ctx, ev, today, &ratings)?;
    if std::env::var("KG_TRACE").is_ok() {
        eprintln!(
            "deep dive: {} ({} of {} first sights alone, bound {:.2}), problems from {scope:?}",
            weak.node, weak.alone, weak.met, weak.bound
        );
    }
    if std::env::var("KG_TRACE").as_deref() == Ok("deep") {
        for w in weakness(ctx, ev, today).iter().take(25) {
            eprintln!(
                "  {:32} {} of {} alone, bound {:.2}",
                w.node, w.alone, w.met, w.bound
            );
        }
    }
    Some(Day {
        weak,
        scope,
        ratings,
    })
}

/// The algorithm techniques next to `node`: its direct prerequisites and
/// the techniques that name it as one.
pub fn linked(ctx: &Ctx, node: &str) -> HashSet<String> {
    let built_on_it = ctx
        .nodes
        .keys()
        .filter(|n| ctx.prereqs(n).iter().any(|p| p == node));
    ctx.prereqs(node)
        .iter()
        .chain(built_on_it)
        .filter(|n| in_group(ctx, n, ALGORITHMS))
        .cloned()
        .collect()
}

/// The drill id of every algorithm technique: what the mode holds, the
/// day's technique and the ones next to it (linked) apart.
pub fn algorithm_drills(ctx: &Ctx) -> HashSet<String> {
    ctx.nodes
        .keys()
        .filter(|n| in_group(ctx, n, ALGORITHMS))
        .map(|n| format!("drill:{n}"))
        .collect()
}

/// The repeats of the day's technique, held or not (pick::open): the due
/// ones, easy to hard, then the ones that are not due, the one he did
/// longest ago first. A problem that is not due and has a record in the
/// last PROBLEM_GRADUATING_DAYS days is not in it.
fn repeats(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    args: &PickArgs,
    day: &Day,
) -> Vec<(String, bool)> {
    let today = ctx.today();
    let node = day.weak.node.as_str();
    let scope = Scope::Node(node.to_string());
    let skip = |p: &str| args.asleep.iter().any(|a| a == p) || args.exclude.contains(p);
    let uses = |num: &str| pv.get(num).is_some_and(|q| scope.covers(ctx, q));
    let mut due: Vec<String> = reviews_due(ctx, ev, pv, today, true)
        .into_iter()
        .map(|(num, _, _)| num)
        .filter(|num| !skip(num) && uses(num))
        .collect();
    due.sort_by(|a, b| {
        let ra = day.ratings.get(a).copied().unwrap_or(f64::INFINITY);
        let rb = day.ratings.get(b).copied().unwrap_or(f64::INFINITY);
        ra.partial_cmp(&rb)
            .unwrap()
            .then_with(|| pnum_key(a).cmp(&pnum_key(b)))
    });
    // the repeats that are not due: the band of the due ones holds them too
    let band = crate::drills::reviews_band().map(|b| {
        let elo = crate::model::first_sight_elo_now(ctx, ev);
        let floor = if crate::learning::enabled() {
            elo - b
        } else {
            f64::NEG_INFINITY
        };
        (floor, elo + b)
    });
    let in_band = |num: &str| match (band, day.ratings.get(num)) {
        (Some((lo, hi)), Some(r)) => *r >= lo && *r <= hi,
        _ => true,
    };
    let mut early: Vec<(NaiveDate, String)> = ev
        .by_problem
        .keys()
        .filter(|num| is_numeric_id(num) && !due.contains(num) && !skip(num) && uses(num))
        .filter(|num| !ctx.unservable(num, pv.get(num).unwrap()) && in_band(num))
        .filter_map(|num| {
            let recs = ev.problem_recs(num);
            if recs.iter().all(|(_, f, _)| is_studied(f)) {
                return None;
            }
            let last = recs.iter().map(|(d, _, _)| parse_date(d)).max()?;
            // a repeat that is not due waits the days the clock gives a
            // fail (2026-11-20: 3021 came back the day after a clean solve)
            (last + Duration::days(PROBLEM_GRADUATING_DAYS) <= today).then(|| (last, num.clone()))
        })
        .collect();
    early.sort_by(|a, b| {
        a.0.cmp(&b.0)
            .then_with(|| pnum_key(&a.1).cmp(&pnum_key(&b.1)))
    });
    due.into_iter()
        .map(|num| (num, true))
        .chain(early.into_iter().map(|(_, num)| (num, false)))
        .collect()
}

/// The repeats of the technique done today: the problems with a record of
/// today and a record before it.
fn repeats_today(ctx: &Ctx, ev: &Evidence, scope: &Scope, today: NaiveDate) -> i64 {
    let d = today.format("%Y-%m-%d").to_string();
    let done: HashSet<String> = ev
        .date_recs(&d)
        .iter()
        .filter(|&&i| !ev.is_drill(i) && !is_studied(ev.fname(i)))
        .map(|&i| ev.rec(i).problem_str())
        .filter(|p| {
            ev.problem_recs(p)
                .iter()
                .any(|(date, f, _)| parse_date(date) < today && !is_studied(f))
        })
        .filter(|p| entry(ctx, p).is_some_and(|q| scope.covers(ctx, q)))
        .collect();
    done.len() as i64
}

/// The technique's problems, in turns: a new problem, then a repeat, until
/// the day's new problems are done, then repeats only. None when the
/// technique has neither left.
pub fn pick(
    ctx: &Ctx,
    pv: &RefCell<PView>,
    ev: &Evidence,
    statuses: &Statuses,
    args: &PickArgs,
    day: &Day,
) -> Option<Choice> {
    let n = budget();
    let today = ctx.today();
    let (weak, scope, ratings) = (&day.weak, &day.scope, &day.ratings);
    let node = weak.node.as_str();
    let name = ctx
        .nodes
        .get(node)
        .map(|x| x.name.clone())
        .filter(|x| !x.is_empty())
        .unwrap_or_else(|| node.to_string());
    let status = st(statuses, node).0;
    // the day's problems are spent: the bank is what is left
    if crate::drills::problems_left(ev, today).is_some_and(|l| l <= 0) {
        return None;
    }
    let skip = |p: &str| args.asleep.iter().any(|a| a == p) || args.exclude.contains(p);

    let drills = clock_servable(ctx, ev, statuses, args);

    let repeat =
        || -> Option<Choice> {
            if crate::drills::no_reviews() {
                return None;
            }
            let view = pv.borrow();
            let (num, due) = repeats(ctx, &view, ev, args, day).into_iter().find_map(
                |(num, due)| match open(ctx, &view, ev, statuses, args, &drills, node, &num) {
                    Open::Itself => Some((Ok(num), due)),
                    Open::First(c) => Some((Err(c), due)),
                    Open::Shut => None,
                },
            )?;
            let num = match num {
                Ok(num) => num,
                Err(first) => return Some(first),
            };
            let what = if due {
                "a due repeat that uses it"
            } else {
                "a repeat that uses it, not due, the oldest first"
            };
            Some(Choice::new(
                node,
                status,
                &num,
                format!("deep dive on {name}: {what}"),
            ))
        };

    // N problems never met, easy to hard
    let sights = first_sights(ev);
    let met_today: Vec<&Sight> = sights
        .iter()
        .filter(|s| s.date == today)
        .filter(|s| {
            s.moves.iter().any(|m| m == node)
                || entry(ctx, &s.pnum).is_some_and(|p| scope.covers(ctx, p))
        })
        .collect();
    let met = met_today.len() as i64;
    let done = repeats_today(ctx, ev, &Scope::Node(node.to_string()), today);
    // the turn: a new problem when as many repeats as new problems are done
    let new_first = met < n && met <= done;
    if !new_first {
        if let Some(c) = repeat() {
            return Some(c);
        }
    }
    if met >= n {
        return None;
    }
    let way = |num: &str| {
        let view = &ctx.predicted_view;
        open(ctx, view, ev, statuses, args, &drills, node, num)
    };
    let cands: Vec<(String, f64)> = cluster(ctx, ev, scope, None, ratings)
        .into_iter()
        .filter(|(num, _)| !skip(num))
        .filter(|(num, _)| !matches!(way(num), Open::Shut))
        .collect();
    let cands = in_range(cands, first_sight_range(ctx, ev));
    let next = match met_today.last() {
        Some(last) => {
            let anchor = ratings.get(&last.pnum).copied();
            match (last.alone, anchor) {
                (true, Some(a)) => above(&cands, a),
                (false, Some(a)) => at_or_below(&cands, a),
                (_, None) => cands.first(),
            }
        }
        None => match start_level(ctx, &sights, node, today, ratings) {
            Some(level) => at_or_below(&cands, level),
            None => cands.first(),
        },
    };
    let Some((num, _)) = next else {
        return repeat();
    };
    if let Open::First(c) = way(num) {
        return Some(c);
    }
    if pv.borrow().get(num).is_none() {
        let p = entry(ctx, num).expect("a cluster problem is in the table");
        let moves = p
            .walks
            .iter()
            .find(|w| w.moves.iter().any(|m| m == node))
            .or(p.walks.first())
            .map(|w| w.moves.clone())
            .unwrap_or_else(|| p.moves.clone());
        let title = Some(p.title.clone())
            .filter(|x| !x.is_empty())
            .or_else(|| ctx.meta_title(num))
            .unwrap_or_else(|| format!("problem {num}"));
        pv.borrow_mut().insert(
            num.clone(),
            Problem {
                title,
                difficulty: Some(ctx.problem_difficulty(num, ctx.all_problems())),
                moves,
                predicted: true,
                ..Default::default()
            },
        );
    }
    Some(Choice::new(
        node,
        status,
        num,
        format!(
            "deep dive on {name}: new problem {} of {n}, easy to hard",
            met_today.len() + 1
        ),
    ))
}

/// Every problem with no record.
pub fn never_met(ctx: &Ctx, ev: &Evidence) -> HashSet<String> {
    ctx.all_problems()
        .keys()
        .chain(ctx.predicted.keys())
        .filter(|p| ev.problem_recs(p).is_empty())
        .cloned()
        .collect()
}
