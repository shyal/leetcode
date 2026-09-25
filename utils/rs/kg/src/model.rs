// The fitted models the pick panel prices with: the contest ratings
// (utils/kg/clist.py's combined table), his Elo over the scored games, the
// cold-solve odds (curve.json "solve"), and the pacing forecast from the
// mined solve times (kg_lib.solve_forecast / drill_forecast).

use std::collections::{HashMap, HashSet};
use std::path::Path;

use chrono::{Duration, NaiveDate};

use crate::ctx::{Ctx, PView};
use crate::data::{env_str, is_numeric_id, read_json, rejected_by_leetcode};
use crate::evidence::Evidence;
use crate::git::mined_solve_times;
use crate::status::node_conn;

pub const ELO_K: f64 = 32.0;
pub const ELO_START: f64 = 1200.0;
pub const FORECAST_WARM_DAYS: i64 = 30;

pub fn budget_min(d: &str) -> Option<i64> {
    match d {
        "Easy" => Some(10),
        "Medium" => Some(30),
        "Hard" => Some(45),
        _ => None,
    }
}

pub fn next_tier(d: &str) -> &str {
    match d {
        "Easy" => "Medium",
        _ => "Hard",
    }
}

/// kg_lib.solve_model: the fitted coefficients, or None.
pub fn solve_model(ctx: &Ctx) -> Option<HashMap<String, f64>> {
    #[cfg(test)]
    if let Some(m) = ctx.stub(|s| s.solve_model.clone()).flatten() {
        return Some(m);
    }
    let cv = ctx.curve.as_ref()?;
    let f = cv.raw.get("solve")?.get("features")?.as_object()?;
    if f.is_empty() {
        return None;
    }
    Some(
        f.iter()
            .filter_map(|(k, v)| v.as_f64().map(|x| (k.clone(), x)))
            .collect(),
    )
}

/// The features of the cold-solve model in graph/curve.json "solve" that
/// solve_logit can price at pick time. kg_curve offers the fitter exactly
/// these, so a fitted coefficient is never silently dropped here (the
/// `length` term was, from its fit on 2026-09-16 until this list existed).
pub const PRICED_FEATURES: [&str; 6] =
    ["intercept", "rating", "recall", "unseen", "length", "mass"];

/// The walk's side of the cold-solve model: kg_curve.solve_rows' per-walk
/// features, computed the same way at pick time.
pub struct WalkTerms {
    /// the summed log recall of the moves met before
    pub ln_recall: f64,
    /// the moves never met
    pub unseen: i64,
    /// ln(moves), at least ln(1)
    pub length: f64,
    /// walk_mass: log(1 + carriers of the rarest move)
    pub mass: f64,
}

pub fn solve_logit(coef: &HashMap<String, f64>, rating: f64, t: &WalkTerms) -> f64 {
    let g = |k: &str| coef.get(k).copied().unwrap_or(0.0);
    g("intercept")
        + g("rating") * (rating - 1500.0) / 400.0
        + g("recall") * t.ln_recall
        + g("unseen") * t.unseen as f64
        + g("length") * t.length
        + g("mass") * t.mass
}

pub fn walk_terms(
    walk: &[String],
    recall: &HashMap<String, f64>,
    counts: &HashMap<String, i64>,
) -> WalkTerms {
    let (mut ln_recall, mut unseen) = (0.0, 0);
    for mv in walk {
        match recall.get(mv) {
            None => unseen += 1,
            Some(r) => ln_recall += r.max(1e-3).ln(),
        }
    }
    WalkTerms {
        ln_recall,
        unseen,
        length: (walk.len().max(1) as f64).ln(),
        mass: walk_mass(walk, counts),
    }
}

/// kg_lib.problem_solve_p: the cold-solve odds on one problem, or None.
pub fn problem_solve_p(
    pnum: &str,
    pv: &PView,
    recall: &HashMap<String, f64>,
    coef: Option<&HashMap<String, f64>>,
    ratings: &HashMap<String, f64>,
    counts: &HashMap<String, i64>,
) -> Option<f64> {
    let coef = coef?;
    let rating = *ratings.get(pnum)?;
    let walk = &pv.get(pnum)?.moves;
    if walk.is_empty() {
        return None;
    }
    let t = walk_terms(walk, recall, counts);
    Some(1.0 / (1.0 + (-solve_logit(coef, rating, &t)).exp()))
}

/// kg_lib.target_pass_rate: TARGET_PASS_RATE in (0, 1), else 0.5.
/// kg_next.solve_state: (node recall today, the fitted cold-solve
/// coefficients, problem ratings, carrier counts) - what prices a walk.
/// Computed once per pick and handed to every rating-aware sort.
pub type SolveState = (
    HashMap<String, f64>,
    Option<HashMap<String, f64>>,
    HashMap<String, f64>,
    HashMap<String, i64>,
);

/// kg_lib.predicted_carrier.informative: (unpriced, distance of the walk's
/// cold-solve odds from the target pass rate). Unpriced walks sort last.
pub fn walk_informative(
    pnum: &str,
    walk: &[String],
    state: Option<&SolveState>,
    aim: f64,
) -> (bool, f64) {
    let Some((recall, Some(coef), ratings, counts)) = state else {
        return (true, 0.0);
    };
    let Some(&rating) = ratings.get(pnum) else {
        return (true, 0.0);
    };
    let t = walk_terms(walk, recall, counts);
    let odds = 1.0 / (1.0 + (-solve_logit(coef, rating, &t)).exp());
    (false, (odds - aim).abs())
}

/// kg_lib.skill_shift: the logit shift `days` of projected practice buys,
/// from the measured Elo drift: a gain of D points is every problem being D
/// points easier, so the shift is -k_rating * D / 400. `z` walks the
/// drift's standard error. Zero drift, zero shift.
pub fn skill_shift(ctx: &Ctx, days: i64, z: f64) -> f64 {
    let solve = ctx.curve.as_ref().and_then(|cv| cv.raw.get("solve"));
    let num = |v: Option<&serde_json::Value>| v.and_then(|x| x.as_f64()).unwrap_or(0.0);
    let elo = solve.and_then(|s| s.get("elo"));
    let k_rating = num(solve
        .and_then(|s| s.get("features"))
        .and_then(|f| f.get("rating")));
    let drift = num(elo.and_then(|e| e.get("drift_per_day")))
        + z * num(elo.and_then(|e| e.get("drift_se")));
    -k_rating * drift * days as f64 / 400.0
}

/// kg_lib.solve_scenarios: (cautious, central, optimistic) logit shifts
/// `days` out - the fitted intercept's standard error plus the drift's,
/// compounded over the horizon.
pub fn solve_scenarios(ctx: &Ctx, days: i64) -> (f64, f64, f64) {
    let se = ctx
        .curve
        .as_ref()
        .and_then(|cv| cv.raw.get("solve"))
        .and_then(|s| s.get("intercept_se"))
        .and_then(|x| x.as_f64())
        .unwrap_or(0.0);
    (
        -1.96 * se + skill_shift(ctx, days, -1.96),
        skill_shift(ctx, days, 0.0),
        1.96 * se + skill_shift(ctx, days, 1.96),
    )
}

/// kg_lib.retention_cycle: the median retention window over the graph,
/// in days - how long the typical move holds before the curve calls it
/// due.
pub fn retention_cycle(ctx: &Ctx, ev: &Evidence) -> i64 {
    let Some(cv) = &ctx.curve else {
        return crate::data::SOLID_WINDOW_DAYS;
    };
    let mut windows: Vec<f64> = ctx
        .nodes
        .keys()
        .map(|nid| {
            let cleans = ev
                .node_entries(nid)
                .iter()
                .filter(|e| e.verdict == "clean")
                .map(|e| e.date)
                .collect::<std::collections::HashSet<_>>()
                .len() as f64;
            let s = (cv.a + cv.b * cleans.ln_1p()).exp().clamp(7.0, 3650.0);
            s * (cv.target_retention.powf(-1.0 / cv.beta) - 1.0)
        })
        .collect();
    if windows.is_empty() {
        return crate::data::SOLID_WINDOW_DAYS;
    }
    windows.sort_by(|a, b| a.partial_cmp(b).unwrap());
    windows[windows.len() / 2] as i64
}

pub fn target_pass_rate() -> f64 {
    let raw = env_str("TARGET_PASS_RATE");
    if raw.is_empty() {
        return 0.5;
    }
    match raw.trim().parse::<f64>() {
        Ok(v) if v > 0.0 && v < 1.0 => v,
        _ => 0.5,
    }
}

// ---- ratings (utils/kg/clist.py) ------------------------------------------

/// statistics.mean over floats: the exact rational mean, converted once.
/// A rating is a float between 1 and 4096, so a multiple of 2^-42: the
/// exact sum fits fixed point at 2^-60 in an i128 (4096 * 2^60 per term,
/// a few thousand terms); the quotient is rounded to a float once, half
/// to even, as Fraction.__float__ rounds it.
fn exact_mean(xs: &[f64]) -> f64 {
    const SHIFT: f64 = 1152921504606846976.0; // 2^60
    let total: i128 = xs.iter().map(|x| (x * SHIFT).round() as i128).sum();
    let d = xs.len() as i128 * (1i128 << 60);
    let neg = total < 0;
    let mut num = total.abs();
    // scale the quotient to 55 bits: 53 of mantissa and two to round on
    let mut k = 0i32;
    while num / d < (1i128 << 54) && k < 100 {
        num <<= 1;
        k += 1;
    }
    let (mut q, r) = (num / d, num % d);
    if r != 0 {
        q |= 1; // the sticky bit: below a tie, the round goes down
    }
    let v = (q as f64) * 2f64.powi(-k);
    if neg {
        -v
    } else {
        v
    }
}

fn clist_ratings(root: &Path) -> HashMap<String, f64> {
    // leetcode number -> CLIST rating, through the slug of the metadata
    let mut out = HashMap::new();
    let Some(table) = read_json(&root.join("data/clist_problems.json")) else {
        return out;
    };
    let mut by_slug: HashMap<String, f64> = HashMap::new();
    for row in table.as_array().into_iter().flatten() {
        if let (Some(slug), Some(r)) = (row.get("slug").and_then(|s| s.as_str()), row.get("rating"))
        {
            if let Some(r) = r.as_f64() {
                if r != 0.0 {
                    by_slug.insert(slug.to_string(), r);
                }
            }
        }
    }
    let Some(meta) = read_json(&root.join("data/problems_metadata.json")) else {
        return out;
    };
    for (num, m) in meta.as_object().into_iter().flatten() {
        if let Some(slug) = m.get("slug").and_then(|s| s.as_str()) {
            if slug.is_empty() {
                continue;
            }
            if let Some(r) = by_slug.get(slug) {
                out.insert(num.clone(), *r);
            }
        }
    }
    out
}

fn zerotrac_ratings(root: &Path) -> HashMap<String, f64> {
    let mut out = HashMap::new();
    let Ok(text) = std::fs::read_to_string(root.join("data/leetcode_ratings.tsv")) else {
        return out;
    };
    let mut lines = text.lines();
    let Some(header) = lines.next() else {
        return out;
    };
    let cols: Vec<&str> = header.split('\t').collect();
    let (Some(ri), Some(ii)) = (
        cols.iter().position(|c| *c == "rating"),
        cols.iter().position(|c| *c == "id"),
    ) else {
        return out;
    };
    for line in lines {
        let f: Vec<&str> = line.split('\t').collect();
        if let (Some(r), Some(id)) = (f.get(ri), f.get(ii)) {
            if let Ok(r) = r.parse::<f64>() {
                out.insert(id.to_string(), r);
            }
        }
    }
    out
}

/// clist.combined_ratings: zerotrac where it rates, rescaled CLIST elsewhere.
pub fn solve_ratings(ctx: &Ctx) -> HashMap<String, f64> {
    #[cfg(test)]
    if let Some(r) = ctx.stub(|s| s.solve_ratings.clone()).flatten() {
        return r;
    }
    if let Some(r) = ctx.ratings.borrow().as_ref() {
        return r.clone();
    }
    let root = &ctx.root;
    let clist = clist_ratings(root);
    let zt = zerotrac_ratings(root);
    let mut out: HashMap<String, f64> = HashMap::new();
    if !clist.is_empty() && !zt.is_empty() {
        let mut both: Vec<&String> = clist.keys().filter(|n| zt.contains_key(*n)).collect();
        both.sort();
        let xs: Vec<f64> = both.iter().map(|n| clist[*n]).collect();
        let ys: Vec<f64> = both.iter().map(|n| zt[*n]).collect();
        if !xs.is_empty() {
            let (mx, my) = (exact_mean(&xs), exact_mean(&ys));
            let mut var = 0.0;
            for x in &xs {
                var += (x - mx) * (x - mx);
            }
            let mut cov = 0.0;
            for (x, y) in xs.iter().zip(&ys) {
                cov += (x - mx) * (y - my);
            }
            let slope = cov / var;
            let a = my - slope * mx;
            for (n, r) in &clist {
                out.insert(n.clone(), a + slope * r);
            }
        }
    }
    for (n, r) in zt {
        out.insert(n, r);
    }
    *ctx.ratings.borrow_mut() = Some(out.clone());
    out
}

// ---- scored games and Elo -----------------------------------------------

#[derive(Clone, Debug)]
pub struct Game {
    pub date: String,
    pub problem: String,
    pub difficulty: String,
    pub score: f64,
    pub moves: Vec<String>,
    pub fname: String,
    /// first sight: on the day of the problem's first evidenced attempt,
    /// with no studied file before it. Every first-sight measure reads it:
    /// make stats, the Elo, the proven rating.
    pub first: bool,
    /// a FAILED file, or a submission leetcode rejected
    pub failed: bool,
    pub seconds: Option<i64>,
    /// a pass that ran past its tier's clock (budget_min)
    pub over: bool,
    /// the heaviest assist level on the solve, or "chain" for an unaided
    /// solve served from a combos chain
    pub assist: String,
}

impl Game {
    /// Served from a combos chain: the technique was named before the
    /// problem was opened. It proves the technique can be carried out,
    /// not that it would be recognised cold, so it is kept out of every
    /// first-sight measure.
    pub fn chain(&self) -> bool {
        self.assist == "chain"
    }
}

/// The totals `make stats` prints and `make elo` shows under its gauges:
/// the games since a date, counted the way they were scored.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Summary {
    pub solves: usize,
    pub fails: usize,
    /// passes inside the clock
    pub inside: usize,
    /// passes over the clock
    pub over: usize,
    /// first sights, chain solves left out
    pub first: usize,
    pub first_fails: usize,
    /// solves served from a combos chain, first sight or not
    pub chain: usize,
    pub chain_fails: usize,
    pub chain_inside: usize,
    /// the sum of the scores: what the Elo saw
    pub won: f64,
}

impl Summary {
    pub fn of<'a>(games: impl IntoIterator<Item = &'a Game>) -> Summary {
        let mut s = Summary::default();
        for g in games {
            s.solves += 1;
            s.fails += usize::from(g.failed);
            s.inside += usize::from(!g.failed && !g.over);
            s.over += usize::from(g.over);
            if g.chain() {
                s.chain += 1;
                s.chain_fails += usize::from(g.failed);
                s.chain_inside += usize::from(!g.failed && !g.over);
            } else {
                s.first += usize::from(g.first);
                s.first_fails += usize::from(g.first && g.failed);
            }
            s.won += g.score;
        }
        s
    }

    pub fn passes(&self) -> usize {
        self.solves - self.fails
    }

    /// The lines as (before, ratio, after): the ratio is the part a
    /// caller colours. `lines()` joins them.
    pub fn rows(&self) -> Vec<(String, String, String)> {
        let pct = |a: usize, b: usize| {
            if b == 0 {
                "-".to_string()
            } else {
                format!("{:.0}%", 100.0 * a as f64 / b as f64)
            }
        };
        let repeats = self.solves - self.first - self.chain;
        let repeat_fails = self.fails - self.first_fails - self.chain_fails;
        let mut rows = vec![
            (
                format!(
                    "{} solves: {} pass / {} fail (",
                    self.solves,
                    self.passes(),
                    self.fails
                ),
                pct(self.passes(), self.solves),
                ")".to_string(),
            ),
            (
                format!("inside the clock: {} of {} (", self.inside, self.solves),
                pct(self.inside, self.solves),
                format!(", {} passes over time)", self.over),
            ),
            (
                format!(
                    "first sight: {} ({} pass / {} fail, ",
                    self.first,
                    self.first - self.first_fails,
                    self.first_fails
                ),
                pct(self.first - self.first_fails, self.first),
                ")".to_string(),
            ),
            (
                format!(
                    "repeat: {} ({} pass / {} fail, ",
                    repeats,
                    repeats - repeat_fails,
                    repeat_fails
                ),
                pct(repeats - repeat_fails, repeats),
                ")".to_string(),
            ),
            (
                format!(
                    "games won: {} of {} (",
                    crate::pyjson::g(self.won),
                    self.solves
                ),
                pct((self.won * 2.0).round() as usize, self.solves * 2),
                ", repeats included: the picker's Elo)".to_string(),
            ),
        ];
        if self.chain > 0 {
            rows.insert(
                4,
                (
                    format!(
                        "chain: {} ({} pass / {} fail, ",
                        self.chain,
                        self.chain - self.chain_fails,
                        self.chain_fails
                    ),
                    pct(self.chain - self.chain_fails, self.chain),
                    format!(", {} inside the clock)", self.chain_inside),
                ),
            );
        }
        rows
    }

    /// The lines, plain text.
    pub fn lines(&self) -> Vec<String> {
        self.rows()
            .into_iter()
            .map(|(a, b, c)| format!("{a}{b}{c}"))
            .collect()
    }
}

/// The games on or after `since`, in place.
pub fn games_since(games: &[Game], since: NaiveDate) -> Vec<&Game> {
    games
        .iter()
        .filter(|g| crate::data::parse_date(&g.date) >= since)
        .collect()
}

/// kg_lib.scored_games over the evidence, oldest first.
pub fn scored_games(ctx: &Ctx, ev: &Evidence) -> Vec<Game> {
    let problems = ctx.evidenced();
    let secs: HashMap<String, i64> = mined_solve_times(ctx)
        .into_iter()
        .map(|(_, _, s, f)| (f, s))
        .collect();
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| {
        (ev.rec(a).date.as_str(), ev.fname(a)).cmp(&(ev.rec(b).date.as_str(), ev.fname(b)))
    });
    let mut out = Vec::new();
    let first_day = first_dates(ev);
    let mut studied: HashSet<String> = HashSet::new();
    for i in order {
        let rec = ev.rec(i);
        let fname = ev.fname(i);
        let pnum = rec.problem.clone().unwrap_or_default();
        let diff = ctx.problem_difficulty(&pnum, &problems);
        if !is_numeric_id(&pnum) || budget_min(&diff).is_none() {
            continue;
        }
        // a studied file is no game, but the problem has been seen: no
        // later rep of it is a first sight
        if crate::clock::is_studied(fname) {
            studied.insert(pnum);
            continue;
        }
        let level = match rec.assist_any() {
            "none" if crate::data::served_by_combos(&ctx.root, fname) => "chain",
            l => l,
        };
        // a walk-away, or a submission leetcode rejected (TLE, WA, RE)
        let failed = fname.contains("FAILED") || rejected_by_leetcode(&ctx.root, fname);
        // the record's own clock; a record older than the field
        // (2026-09-16) falls back to the time mined from its commit
        let seconds = rec.seconds.or_else(|| secs.get(fname).copied());
        let tier = if rec.followup.as_deref() == Some("solved") {
            next_tier(&diff).to_string()
        } else {
            diff.clone()
        };
        let over = !failed && seconds.is_some_and(|s| s > budget_min(&tier).unwrap() * 60);
        let score = if failed || level == "walkthrough" || level == "learning" {
            0.0
        } else {
            if seconds.is_none() {
                continue;
            }
            if over {
                0.0
            } else if level == "hint" || level == "chain" {
                0.5
            } else {
                1.0
            }
        };
        out.push(Game {
            date: rec.date.clone(),
            problem: pnum.clone(),
            difficulty: diff,
            score,
            moves: rec.moves.keys().cloned().collect(),
            fname: fname.to_string(),
            first: first_day.get(&pnum) == Some(&rec.date) && !studied.contains(&pnum),
            failed,
            seconds,
            over,
            assist: level.to_string(),
        });
    }
    out
}

/// kg_lib.elo_games: every scored game with the Elo he carried INTO it and
/// the rating of the problem (a missing rating takes its difficulty's
/// median), oldest first: (game, rating, elo_before).
pub fn elo_games(
    ctx: &Ctx,
    ev: &Evidence,
    ratings: &HashMap<String, f64>,
) -> Vec<(Game, f64, f64)> {
    let games = scored_games(ctx, ev);
    let mut by_dif: HashMap<String, Vec<f64>> = HashMap::new();
    for g in &games {
        if let Some(r) = ratings.get(&g.problem) {
            by_dif.entry(g.difficulty.clone()).or_default().push(*r);
        }
    }
    let median: HashMap<String, f64> = by_dif
        .into_iter()
        .map(|(d, mut v)| {
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let m = v[v.len() / 2];
            (d, m)
        })
        .collect();
    let mut elo = ELO_START;
    let mut out = Vec::new();
    for g in games {
        let Some(r) = ratings
            .get(&g.problem)
            .or_else(|| median.get(&g.difficulty))
            .copied()
        else {
            continue;
        };
        let before = elo;
        elo += ELO_K * (g.score - 1.0 / (1.0 + 10f64.powf((r - elo) / 400.0)));
        out.push((g, r, before));
    }
    out
}

/// How far the Elo you carried into a game may sit above the problem for
/// the problem to count as at your level.
pub const AT_RATING_BAND: f64 = 100.0;

/// The two counts that answer "progressing or grinding" (2026-09-20):
/// gain, first-sight games on problems at your level (rating within
/// AT_RATING_BAND under the Elo carried into the game) and how many were
/// won cold; and retention, problems recovered (a lost game - a fail, a
/// copy or a walkthrough - then an unaided pass) that were retested and
/// passed unaided again, over the clock or not. The window applies to the first
/// sight and to the retest; `pending` counts every recovery still waiting
/// for its retest, whatever the window. `make stats` prints both under
/// the totals, and the note of 2026-09-20 fixes the baseline: 5 cold of
/// 14 tried in September, 1 held of 11 retests since August.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Ground {
    pub tried: usize,
    pub cold: usize,
    pub retested: usize,
    pub held: usize,
    pub pending: usize,
}

impl Ground {
    /// Over elo_games, oldest first; `since` limits the first sights and
    /// the retests to a window.
    pub fn of(games: &[(Game, f64, f64)], since: Option<NaiveDate>) -> Ground {
        let inside = |g: &Game| since.is_none_or(|s| crate::data::parse_date(&g.date) >= s);
        let lost = |g: &Game| g.failed || g.assist == "learning" || g.assist == "walkthrough";
        let mut out = Ground::default();
        // per problem: (last game lost, the game before that was a recovery)
        let mut state: HashMap<&str, (bool, bool)> = HashMap::new();
        for (g, rating, before) in games {
            if g.first && !g.chain() && *rating >= before - AT_RATING_BAND && inside(g) {
                out.tried += 1;
                out.cold += usize::from(g.score == 1.0);
            }
            // an unaided pass, over the clock or not: the retest asks
            // whether the memory held, not whether it was fast
            let won = !g.failed && g.assist == "none";
            let (was_lost, recovered) = state
                .get(g.problem.as_str())
                .copied()
                .unwrap_or((false, false));
            if recovered && inside(g) {
                out.retested += 1;
                out.held += usize::from(won);
            }
            let now_recovered = was_lost && won;
            state.insert(g.problem.as_str(), (lost(g), now_recovered));
        }
        out.pending = state.values().filter(|(_, r)| *r).count();
        out
    }

    /// Two sentences; `window` is "the last 7 days" or "all time".
    pub fn rows(&self, window: &str) -> Vec<(String, String, String)> {
        let pct = |a: usize, b: usize| {
            if b == 0 {
                "-".to_string()
            } else {
                format!("{:.0}%", 100.0 * a as f64 / b as f64)
            }
        };
        vec![
            (
                format!(
                    "In {window} you tried {} problems at your level for the first time and solved {} of them with no help and within the time limit (",
                    self.tried, self.cold
                ),
                pct(self.cold, self.tried),
                ").".to_string(),
            ),
            (
                format!(
                    "{} problems you had failed and later solved were given to you again; you solved {} of them again with no help (",
                    self.retested, self.held
                ),
                pct(self.held, self.retested),
                format!("). {} more have not been given again yet.", self.pending),
            ),
        ]
    }
}

/// Transfer: whether what was practiced carries over to problems never
/// seen. Every first sight in the window (a chain solve left out) is split
/// by whether each move its problem needs (problems.json) was in some
/// record, a drill or another problem, dated before the game. A move
/// practiced elsewhere cannot hand over this problem's answer, so a cold
/// win in the first group is the technique carrying over, not a memory of
/// the problem. All time on 2026-09-25: 280 cold of 388 with every move
/// practiced (72%), 21 of 41 with a move new (51%).
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Transfer {
    pub practiced: usize,
    pub practiced_cold: usize,
    pub new: usize,
    pub new_cold: usize,
}

impl Transfer {
    pub fn of(
        games: &[Game],
        ev: &Evidence,
        problems: &crate::data::Problems,
        since: Option<NaiveDate>,
    ) -> Transfer {
        let mut out = Transfer::default();
        for g in games {
            let day = crate::data::parse_date(&g.date);
            if !g.first || g.chain() || since.is_some_and(|s| day < s) {
                continue;
            }
            let Some(p) = problems.get(&g.problem).filter(|p| !p.moves.is_empty()) else {
                continue;
            };
            let cold = usize::from(g.score == 1.0);
            if p.moves
                .iter()
                .all(|m| ev.node_entries(m).iter().any(|e| e.date < day))
            {
                out.practiced += 1;
                out.practiced_cold += cold;
            } else {
                out.new += 1;
                out.new_cold += cold;
            }
        }
        out
    }

    /// One sentence; `window` is "the last 7 days" or "all time".
    pub fn rows(&self, window: &str) -> Vec<(String, String, String)> {
        let pct = |a: usize, b: usize| {
            if b == 0 {
                "-".to_string()
            } else {
                format!("{:.0}%", 100.0 * a as f64 / b as f64)
            }
        };
        vec![
            (
                format!(
                    "In {window}, of {} new problems whose techniques you had all practiced on other problems or drills, you solved {} with no help and within the time limit (",
                    self.practiced, self.practiced_cold
                ),
                pct(self.practiced_cold, self.practiced),
                ");".to_string(),
            ),
            (
                format!(
                    "of {} new problems that needed a technique you had not practiced, you solved {} (",
                    self.new, self.new_cold
                ),
                pct(self.new_cold, self.new),
                ").".to_string(),
            ),
        ]
    }
}

// ---- first-sight Elo -------------------------------------------------------

// The one first-sight Elo: the number on `make elo` and the README badge.
// Problem ratings are zerotrac's (data/leetcode_ratings.tsv); a problem
// that never ran in a contest gets the median contest rating of its
// difficulty. Only first sights are games (Game::first), a chain solve
// left out. Standard Elo, ELO_K from ELO_START. The picker keeps its own
// over every timed attempt (elo_games, settled 2026-09-12).

/// (date, problem rating, score): one scored first-sight game.
pub type FirstSight = (NaiveDate, f64, f64);

/// data/leetcode_ratings.tsv in file order: (problem, rating).
pub fn load_ratings(ctx: &Ctx) -> Vec<(String, f64)> {
    let text = std::fs::read_to_string(ctx.root.join("data/leetcode_ratings.tsv"))
        .expect("data/leetcode_ratings.tsv");
    text.lines()
        .skip(1)
        .map(|l| {
            let mut f = l.split('\t');
            let r: f64 = f.next().unwrap().parse().unwrap();
            (f.next().unwrap().to_string(), r)
        })
        .collect()
}

/// problem -> date of its first evidenced attempt, timed or not.
pub fn first_dates(ev: &Evidence) -> HashMap<String, String> {
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| (&ev.rec(a).date, ev.fname(a)).cmp(&(&ev.rec(b).date, ev.fname(b))));
    let mut first = HashMap::new();
    for i in order {
        let rec = ev.rec(i);
        first
            .entry(rec.problem.clone().unwrap_or_default())
            .or_insert_with(|| rec.date.clone());
    }
    first
}

/// (problem -> contest rating, difficulty -> the median rating of its
/// rated problems): what a game is priced at.
pub fn pricing(ctx: &Ctx) -> (HashMap<String, f64>, HashMap<String, f64>) {
    let ratings = load_ratings(ctx);
    let mut by_diff: HashMap<String, Vec<f64>> = HashMap::new();
    for (pid, rt) in &ratings {
        if let Some(d) = ctx.meta.get(pid).and_then(|m| m.difficulty.clone()) {
            by_diff.entry(d).or_default().push(*rt);
        }
    }
    (
        ratings.into_iter().collect(),
        by_diff.into_iter().map(|(d, v)| (d, median(&v))).collect(),
    )
}

pub fn price(
    ratings: &HashMap<String, f64>,
    imputed: &HashMap<String, f64>,
    problem: &str,
    difficulty: &str,
) -> f64 {
    match ratings.get(problem) {
        Some(r) => *r,
        None => *imputed
            .get(difficulty)
            .unwrap_or_else(|| panic!("no median rating for {difficulty}")),
    }
}

/// The scored first-sight attempts oldest first, each game's score
/// read through `score`; a chain solve is no first sight (Game::chain).
fn first_sights(ctx: &Ctx, ev: &Evidence, score: fn(&Game) -> f64) -> Vec<FirstSight> {
    let (ratings, imputed) = pricing(ctx);
    scored_games(ctx, ev)
        .into_iter()
        .filter(|g| g.first && !g.chain())
        .map(|g| {
            (
                crate::data::parse_date(&g.date),
                price(&ratings, &imputed, &g.problem, &g.difficulty),
                score(&g),
            )
        })
        .collect()
}

/// [(date, problem rating, Elo score)]: the games of the first-sight Elo.
pub fn first_sight_elo_games(ctx: &Ctx, ev: &Evidence) -> Vec<FirstSight> {
    first_sights(ctx, ev, |g| g.score)
}

/// [(date, problem rating, proven score)]: the same games, scored for
/// the proven rating (proven_game_score).
pub fn proven_games(ctx: &Ctx, ev: &Evidence) -> Vec<FirstSight> {
    first_sights(ctx, ev, proven_game_score)
}

/// [(date, rating after the game)] one per game, from `start`.
pub fn elo_after(gs: &[FirstSight], start: f64) -> Vec<(NaiveDate, f64)> {
    let mut r = start;
    gs.iter()
        .map(|(d, rp, s)| {
            r += ELO_K * (s - 1.0 / (1.0 + 10f64.powf((rp - r) / 400.0)));
            (*d, r)
        })
        .collect()
}

// ---- proven rating ---------------------------------------------------------

/// The window of the proven rating: the last PROVEN_WINDOW first sights.
pub const PROVEN_WINDOW: usize = 30;

/// What one first-sight game proves (settled 2026-09-20): an unaided win
/// inside the clock proves the problem's rating, a pass that fell short
/// of that (a hint, or over the clock) the rating less 200, a fail or a
/// copy the rating less 400. A win proves nothing beyond the problem:
/// three hundred wins on 1250s prove 1250, where Elo read them as 1900
/// (a 1250 problem cannot tell a 1700 from a 1900, so Elo climbs until
/// the slip rate matches its expectation). `score` is the proven score
/// of proven_games, not the Elo score: a slow pass is 0 to the Elo
/// and 0.5 here, since the solution was found, only late.
pub fn proven_score(rating: f64, score: f64) -> f64 {
    if score >= 1.0 {
        rating
    } else if score >= 0.5 {
        rating - 200.0
    } else {
        rating - 400.0
    }
}

/// [(date, proven rating)] one per first-sight game from the
/// PROVEN_WINDOW-th on: the mean of the last PROVEN_WINDOW scores.
pub fn proven_series(games: &[(NaiveDate, f64, f64)]) -> Vec<(NaiveDate, f64)> {
    let scores: Vec<f64> = games.iter().map(|(_, r, s)| proven_score(*r, *s)).collect();
    let n = PROVEN_WINDOW;
    if scores.len() < n {
        return vec![];
    }
    (n - 1..scores.len())
        .map(|i| {
            let mean = scores[i + 1 - n..=i].iter().sum::<f64>() / n as f64;
            (games[i].0, mean)
        })
        .collect()
}

/// The median problem rating over the same windows as proven_series,
/// one per point.
pub fn served_series(games: &[(NaiveDate, f64, f64)]) -> Vec<f64> {
    let n = PROVEN_WINDOW;
    if games.len() < n {
        return vec![];
    }
    (n - 1..games.len())
        .map(|i| {
            let rs: Vec<f64> = games[i + 1 - n..=i].iter().map(|(_, r, _)| *r).collect();
            median(&rs)
        })
        .collect()
}

/// A first-sight game's proven score: the Elo score except for a pass
/// over the clock, which the Elo scores 0 and the proven rating 0.5: it
/// was solved, late.
pub fn proven_game_score(g: &Game) -> f64 {
    let passed = !g.failed && (g.assist == "none" || g.assist == "hint");
    if passed {
        g.score.max(0.5)
    } else {
        g.score
    }
}

// ---- make progress -------------------------------------------------------

/// The Elo has to move this much over PROGRESS_LEVEL_DAYS to count as a
/// move at all; under it the level is called flat.
pub const PROGRESS_LEVEL_POINTS: f64 = 50.0;
pub const PROGRESS_LEVEL_DAYS: i64 = 90;
pub const PROGRESS_WINDOW_DAYS: i64 = 30;
/// A drill holds once this many unaided clean reps in a row end its history.
pub const PROGRESS_HOLD_REPS: usize = 3;
/// An unaided solve counts as the drill's once a clean rep on one of its
/// moves fell inside this many days before it.
pub const PROGRESS_TURNED_DAYS: i64 = 21;

fn month_name(d: NaiveDate) -> &'static str {
    use chrono::Datelike;
    [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ][d.month0() as usize]
}

fn plain(node: &str, ctx: &Ctx) -> String {
    ctx.nodes
        .get(node)
        .map(|n| n.name.to_lowercase())
        .unwrap_or_else(|| node.replace('-', " "))
}

fn number(n: usize) -> String {
    match n {
        0 => "none".into(),
        1 => "one".into(),
        2 => "two".into(),
        3 => "three".into(),
        4 => "four".into(),
        5 => "five".into(),
        6 => "six".into(),
        7 => "seven".into(),
        8 => "eight".into(),
        9 => "nine".into(),
        _ => n.to_string(),
    }
}

/// The numbers behind `make progress` and the `make prog` panel
/// (2026-09-20). One load, two readers: the prose in `progress` and the
/// panel in kg_readme read the same struct.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Progress {
    /// scored games in the last PROGRESS_WINDOW_DAYS, repeats included
    pub recent: usize,
    /// of those, lost: a fail, a copy or a walkthrough
    pub lost: usize,
    /// (date, proven rating) one per first sight from the PROVEN_WINDOW-th on
    pub proven: Vec<(NaiveDate, f64)>,
    /// the proven rating now, once PROVEN_WINDOW first sights exist
    pub now: Option<f64>,
    /// the proven rating PROGRESS_LEVEL_DAYS ago (the first point on or after)
    pub then: Option<f64>,
    /// the best proven rating before now, over the whole series
    pub best: Option<f64>,
    /// the median rating of the last PROVEN_WINDOW first sights served
    pub served: Option<f64>,
    /// the same median at the point `then` was read
    pub served_then: Option<f64>,
    /// gain and retention over the last PROGRESS_WINDOW_DAYS
    pub ground: Ground,
    /// drills whose last PROGRESS_HOLD_REPS days of reps were all clean,
    /// the last inside the window
    pub holding: usize,
    /// (move, problem titles) unaided solves at level this month with a
    /// clean drill rep on the move in the three weeks before, oldest first
    pub turned: Vec<(String, Vec<String>)>,
}

impl Progress {
    /// The proven rating less the median rating served, now and then.
    /// A fail still proves its rating less 400, so the proven rating
    /// rises with the serving level on its own; only this gap says
    /// whether he did better on what he was given (2026-09-25).
    pub fn gap(&self) -> Option<f64> {
        Some(self.now? - self.served?)
    }

    pub fn gap_then(&self) -> Option<f64> {
        Some(self.then? - self.served_then?)
    }

    /// the gap now less the gap then, 0 without both
    pub fn delta(&self) -> f64 {
        match (self.gap(), self.gap_then()) {
            (Some(n), Some(t)) => n - t,
            _ => 0.0,
        }
    }

    /// The one-word verdict of `make progress`, lower case: progressing,
    /// slipping, stalled, grinding, rebuilding, gaining; "not training"
    /// under five games in the window.
    pub fn verdict(&self) -> &'static str {
        let g = &self.ground;
        if self.recent < 5 {
            "not training"
        } else if self.delta() >= PROGRESS_LEVEL_POINTS {
            "progressing"
        } else if self.delta() <= -PROGRESS_LEVEL_POINTS {
            "slipping"
        } else if g.cold == 0 {
            "stalled"
        } else if g.retested >= 3 && g.held * 2 < g.retested {
            "grinding"
        } else if self.lost * 2 > self.recent {
            "rebuilding"
        } else {
            "gaining"
        }
    }

    /// whether now is the highest the proven rating has been
    pub fn at_best(&self) -> bool {
        match (self.now, self.best) {
            (Some(n), Some(b)) => n > b,
            _ => false,
        }
    }
}

/// The reps of one drill folded to one answer per day, oldest first: the
/// day's last answer stands.
fn drill_days(ev: &Evidence, key: &str) -> Vec<(String, &'static str)> {
    let mut by_day: Vec<(String, &'static str)> = Vec::new();
    for &i in ev.drill_reps(key).iter() {
        let (d, base, ri) = &ev.drills[i];
        let a = crate::drills::anki_answer(base, ev.rec(*ri));
        match by_day.iter_mut().find(|(day, _)| day == d) {
            Some(slot) => slot.1 = a,
            None => by_day.push((d.clone(), a)),
        }
    }
    by_day.sort();
    by_day
}

/// The numbers as of `today`: games and drill reps after it are left out,
/// so KG_TODAY gives the panel as it stood on a past day.
pub fn progress_numbers(ctx: &Ctx, ev: &Evidence, today: NaiveDate) -> Progress {
    let ratings = solve_ratings(ctx);
    let mut games = elo_games(ctx, ev, &ratings);
    games.retain(|(g, _, _)| crate::data::parse_date(&g.date) <= today);
    let since = today - Duration::days(PROGRESS_WINDOW_DAYS);
    let lost_game = |g: &Game| g.failed || g.assist == "learning" || g.assist == "walkthrough";
    let recent: Vec<&Game> = games
        .iter()
        .map(|(g, _, _)| g)
        .filter(|g| crate::data::parse_date(&g.date) >= since)
        .collect();
    let mut out = Progress {
        recent: recent.len(),
        lost: recent.iter().filter(|g| lost_game(g)).count(),
        ..Progress::default()
    };
    // the level: the proven rating (proven_series) now against 90 days
    // ago. Elo, every-game or first-sight, was inflated by the 2025 easies
    // (settled 2026-09-20); a peak built on them is never a level to beat.
    let mut fs = proven_games(ctx, ev);
    fs.retain(|(d, _, _)| *d <= today);
    out.proven = proven_series(&fs);
    let level_since = today - Duration::days(PROGRESS_LEVEL_DAYS);
    out.now = out.proven.last().map(|(_, e)| *e);
    // the level rises with the serving level on its own, so the median
    // served is read at the same points: a rise on a steady serving level
    // is his, a rise that only tracks the serving level is the picker's
    let served = served_series(&fs);
    let then_at = out.proven.iter().position(|(d, _)| *d >= level_since);
    out.then = then_at.map(|i| out.proven[i].1);
    out.served_then = then_at.map(|i| served[i]);
    out.served = served.last().copied();
    let before_now = &out.proven[..out.proven.len().saturating_sub(1)];
    out.best = before_now
        .iter()
        .map(|(_, e)| *e)
        .fold(None::<f64>, |b, e| Some(b.map_or(e, |b| b.max(e))));
    out.ground = Ground::of(&games, Some(since));

    // the drills: holding, and which turned into unaided solves this month
    let mut held_nodes: HashMap<String, Vec<NaiveDate>> = HashMap::new();
    for path in ctx.every_bank_path() {
        let mut by_day = drill_days(ev, &ctx.drill_evidence_key(&path));
        by_day.retain(|(d, _)| crate::data::parse_date(d) <= today);
        let n = by_day.len();
        if n >= PROGRESS_HOLD_REPS
            && by_day[n - PROGRESS_HOLD_REPS..]
                .iter()
                .all(|(_, a)| *a == "good")
            && crate::data::parse_date(&by_day[n - 1].0) >= since
        {
            out.holding += 1;
        }
        if let Some(node) = crate::drills::drill_node(&path) {
            let goods = by_day
                .iter()
                .filter(|(_, a)| *a == "good")
                .map(|(d, _)| crate::data::parse_date(d));
            held_nodes.entry(node).or_default().extend(goods);
        }
    }
    // an unaided solve at level this month, first sight or won back, with a
    // clean drill rep on one of its moves in the three weeks before
    for (g, rating, before) in &games {
        let d = crate::data::parse_date(&g.date);
        if d < since || g.failed || g.assist != "none" || *rating < before - AT_RATING_BAND {
            continue;
        }
        let mv = g.moves.iter().find(|m| {
            held_nodes.get(*m).is_some_and(|ds| {
                ds.iter()
                    .any(|x| *x < d && d - *x <= Duration::days(PROGRESS_TURNED_DAYS))
            })
        });
        let Some(m) = mv else {
            continue;
        };
        let title = ctx
            .meta_title(&g.problem)
            .unwrap_or_else(|| g.problem.clone());
        let m = plain(m, ctx);
        match out.turned.iter_mut().find(|(k, _)| *k == m) {
            Some(slot) if slot.1.contains(&title) => {}
            Some(slot) => slot.1.push(title),
            None => out.turned.push((m, vec![title])),
        }
    }
    out
}

/// `make progress`: three paragraphs. The verdict on whether the level is
/// moving and why; whether the drills hold and which turned into unaided
/// solves this month; what is queued. Plain words: no rate,
/// no repo idiom (2026-09-20, the day the two `make stats` sentences took
/// six rewrites to read).
pub fn progress(ctx: &Ctx, ev: &Evidence, today: NaiveDate) -> Vec<String> {
    progress_text(&progress_numbers(ctx, ev, today), today)
}

/// The two gaps in words: "It was 260 under the median rating of the
/// problems you were given in June (1550 against 1290) and is 180 under
/// it now (1650 against 1470)".
fn against(p: &Progress, ten: impl Fn(f64) -> i64) -> String {
    let side = |g: f64| match ten(g) {
        0 => "level with".to_string(),
        x if x < 0 => format!("{} under", -x),
        x => format!("{x} over"),
    };
    format!(
        "It was {} the median rating of the problems you were given then ({} against {}) and is {} it now ({} against {})",
        side(p.gap_then().unwrap_or(0.0)),
        ten(p.then.unwrap_or(0.0)),
        ten(p.served_then.unwrap_or(0.0)),
        side(p.gap().unwrap_or(0.0)),
        ten(p.now.unwrap_or(0.0)),
        ten(p.served.unwrap_or(0.0)),
    )
}

pub fn progress_text(p: &Progress, today: NaiveDate) -> Vec<String> {
    let mut out = Vec::new();
    if p.verdict() == "not training" {
        out.push("You're not training.".to_string());
        out.push(format!(
            "{} problems in the last {} days. Nothing can be said about the level on that.",
            number(p.recent).to_uppercase_first(),
            PROGRESS_WINDOW_DAYS
        ));
        return out;
    }
    let level_since = today - Duration::days(PROGRESS_LEVEL_DAYS);
    let ten = |x: f64| (x / 10.0).round() as i64 * 10;
    let level = match (p.now, p.best) {
        (Some(n), Some(b)) if n > b => format!(
            "The rating you have proven on problems never seen before is about {}, the highest it has been.",
            ten(n)
        ),
        (Some(n), Some(b)) if b - n >= PROGRESS_LEVEL_POINTS => format!(
            "The rating you have proven on problems never seen before is about {}, {} under its best.",
            ten(n),
            ten(b - n)
        ),
        (Some(n), _) => format!(
            "The rating you have proven on problems never seen before is about {}.",
            ten(n)
        ),
        _ => String::new(),
    };
    let delta = p.delta();
    let moved = matches!(p.verdict(), "progressing" | "slipping");
    match p.verdict() {
        "progressing" => {
            out.push("You're progressing.".to_string());
            out.push(format!(
                "Against the problems you were given, the rating you have proven on problems never seen before is up about {} points since {}. {}{}.",
                ten(delta),
                month_name(level_since),
                against(p, ten),
                if p.at_best() {
                    " It is the highest it has been"
                } else {
                    ""
                }
            ));
        }
        "slipping" => {
            out.push("You're slipping.".to_string());
            out.push(format!(
                "Against the problems you were given, the rating you have proven on problems never seen before is down about {} points since {}. {}.",
                ten(-delta),
                month_name(level_since),
                against(p, ten)
            ));
        }
        "stalled" => {
            out.push("You're stalled.".to_string());
            out.push(format!(
                "No new problem at your level was solved without help in the last {} days, and the level cannot move on reviews and drills alone. {level}",
                PROGRESS_WINDOW_DAYS
            ));
        }
        "grinding" => {
            out.push("You're grinding.".to_string());
            out.push(format!(
                "You solve new problems at your level and lose them within weeks, so the level does not move. {level}"
            ));
        }
        "rebuilding" => {
            out.push("You're rebuilding.".to_string());
            out.push(format!(
                "Most of the last {} days went to problems you had failed or copied, and new problems at your level are getting solved. {level} It moves once the rebuilt ones stay solved.",
                PROGRESS_WINDOW_DAYS
            ));
        }
        _ => {
            out.push("You're gaining, and whether it stays is not known yet.".to_string());
            out.push(format!(
                "New problems at your level are being solved without help. Too few have been asked a second time to say whether they stay solved. {level}"
            ));
        }
    }
    if let (Some(served), false) = (p.served, moved) {
        out[1].push_str(&format!(
            " The median rating of those {} problems was about {}; the proven rating can only rise when that does.",
            PROVEN_WINDOW,
            ten(served)
        ));
    }

    if p.holding == 0 {
        out.push(
            "Your drills are not holding yet: none has three clean runs in a row this month."
                .to_string(),
        );
    } else {
        let mut para = format!(
            "Your drills are holding: {} of them have stayed clean for three runs or more.",
            number(p.holding)
        );
        if p.turned.is_empty() {
            para.push_str(" None of them turned into a solved problem this month.");
        } else {
            // the three most recent moves, the rest a count
            let total = p.turned.len();
            let list: Vec<String> = p
                .turned
                .iter()
                .rev()
                .take(3)
                .map(|(m, ts)| format!("{m} ({})", ts.join(", ")))
                .collect();
            let more = if total > 3 {
                format!(", and {} more", number(total - 3))
            } else {
                String::new()
            };
            para.push_str(&format!(
                " {} turned into problems solved without help this month: {}{more}.",
                number(total).to_uppercase_first(),
                list.join("; ")
            ));
        }
        out.push(para);
    }

    // what is queued
    if p.ground.pending > 0 {
        out.push(format!(
            "{} problems you had failed and later solved are waiting to be asked again, each after a drill on its move. That is where the level moves or does not.",
            number(p.ground.pending).to_uppercase_first()
        ));
    }
    out
}

trait UpperFirst {
    fn to_uppercase_first(&self) -> String;
}

impl UpperFirst for String {
    fn to_uppercase_first(&self) -> String {
        let mut c = self.chars();
        match c.next() {
            Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
            None => String::new(),
        }
    }
}

/// kg_lib.elo_drift: (points per day, its standard error), least squares of
/// Elo on calendar day over all the games; (0, 0) under 30 games.
pub fn elo_drift(games: &[(Game, f64, f64)]) -> (f64, f64) {
    if games.len() < 30 {
        return (0.0, 0.0);
    }
    let d0 = crate::data::parse_date(&games[0].0.date);
    let x: Vec<f64> = games
        .iter()
        .map(|(g, _, _)| (crate::data::parse_date(&g.date) - d0).num_days() as f64)
        .collect();
    let y: Vec<f64> = games.iter().map(|(_, _, e)| *e).collect();
    let n = x.len() as f64;
    let mx = x.iter().sum::<f64>() / n;
    let my = y.iter().sum::<f64>() / n;
    let sxx: f64 = x.iter().map(|a| (a - mx) * (a - mx)).sum();
    if sxx == 0.0 {
        return (0.0, 0.0);
    }
    let slope: f64 = x
        .iter()
        .zip(&y)
        .map(|(a, b)| (a - mx) * (b - my))
        .sum::<f64>()
        / sxx;
    let s2: f64 = x
        .iter()
        .zip(&y)
        .map(|(a, b)| {
            let r = b - (my + slope * (a - mx));
            r * r
        })
        .sum::<f64>()
        / (n - 2.0).max(1.0);
    (slope, (s2 / sxx).sqrt())
}

/// kg_lib.walk_mass: log(1 + carriers of the walk's rarest move).
pub fn walk_mass(walk: &[String], counts: &HashMap<String, i64>) -> f64 {
    let m = walk
        .iter()
        .map(|m| *counts.get(m).unwrap_or(&0))
        .min()
        .unwrap_or(0);
    (m as f64).ln_1p()
}

/// kg_lib.elo_now: his Elo after the last scored game.
pub fn elo_now(ctx: &Ctx, ev: &Evidence) -> f64 {
    let games = scored_games(ctx, ev);
    let ratings = solve_ratings(ctx);
    let mut by_dif: HashMap<String, Vec<f64>> = HashMap::new();
    for g in &games {
        if let Some(r) = ratings.get(&g.problem) {
            by_dif.entry(g.difficulty.clone()).or_default().push(*r);
        }
    }
    let median: HashMap<String, f64> = by_dif
        .into_iter()
        .map(|(d, mut v)| {
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let m = v[v.len() / 2];
            (d, m)
        })
        .collect();
    let mut elo = ELO_START;
    for g in &games {
        let r = match ratings
            .get(&g.problem)
            .or_else(|| median.get(&g.difficulty))
        {
            Some(r) => *r,
            None => continue,
        };
        elo += ELO_K * (g.score - 1.0 / (1.0 + 10f64.powf((r - elo) / 400.0)));
    }
    elo
}

// ---- pacing forecasts -----------------------------------------------------

/// statistics.median
pub fn median(v: &[f64]) -> f64 {
    let mut s = v.to_vec();
    s.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = s.len();
    if n % 2 == 1 {
        s[n / 2]
    } else {
        (s[n / 2 - 1] + s[n / 2]) / 2.0
    }
}

fn by_key(reps: &[(String, NaiveDate, i64, String)]) -> Vec<(String, Vec<(NaiveDate, i64)>)> {
    let mut out: Vec<(String, Vec<(NaiveDate, i64)>)> = Vec::new();
    for (k, d, s, _) in reps {
        match out.iter_mut().find(|(key, _)| key == k) {
            Some(slot) => slot.1.push((*d, *s)),
            None => out.push((k.clone(), vec![(*d, *s)])),
        }
    }
    out
}

fn warm_ratio(
    groups: &[(String, Vec<(NaiveDate, i64)>)],
    mine: &[(NaiveDate, i64)],
    today: NaiveDate,
) -> f64 {
    let (mut warm_r, mut cold_r): (Vec<f64>, Vec<f64>) = (vec![], vec![]);
    for (_, rs) in groups {
        for w in rs.windows(2) {
            let ((d0, s0), (d1, s1)) = (w[0], w[1]);
            let r = (s1 as f64 / s0 as f64).log2();
            if (d1 - d0).num_days() <= FORECAST_WARM_DAYS {
                warm_r.push(r);
            } else {
                cold_r.push(r);
            }
        }
    }
    let (d0, s0) = mine[mine.len() - 1];
    let warm = (today - d0).num_days() <= FORECAST_WARM_DAYS;
    let pool = if warm { &warm_r } else { &cold_r };
    let r = if pool.is_empty() { 0.0 } else { median(pool) };
    s0 as f64 / 60.0 * 2f64.powf(r)
}

/// kg_lib.drill_forecast: (expect, hint, bail) minutes for a bank file.
pub fn drill_forecast(ctx: &Ctx, path: &Path, today: NaiveDate) -> Option<(f64, f64, f64)> {
    let reps = mined_solve_times(ctx);
    if reps.is_empty() {
        return None;
    }
    let key = format!("d:{}", ctx.drill_solved_stem(path));
    let groups = by_key(&reps);
    let base = match groups.iter().find(|(k, _)| *k == key) {
        Some((_, mine)) => warm_ratio(&groups, mine, today),
        None => {
            let firsts: Vec<f64> = groups
                .iter()
                .filter(|(k, _)| k.starts_with("d:"))
                .map(|(_, rs)| rs[0].1 as f64 / 60.0)
                .collect();
            if firsts.len() < 8 {
                return None;
            }
            median(&firsts)
        }
    };
    let base = base.max(1.0);
    Some((base, base * 2.0, base * 4.0))
}

/// kg_lib.solve_forecast: (expect, hint, bail) minutes for a problem.
pub fn solve_forecast(
    ctx: &Ctx,
    pnum: &str,
    pv: &PView,
    today: NaiveDate,
) -> Option<(f64, f64, f64)> {
    let reps = mined_solve_times(ctx);
    if reps.is_empty() {
        return None;
    }
    let groups = by_key(&reps);
    let base = match groups.iter().find(|(k, _)| k == pnum) {
        Some((_, mine)) => warm_ratio(&groups, mine, today),
        None => {
            let conn = node_conn(pv, ctx);
            let my = pv.get(pnum)?;
            if my.moves.is_empty() {
                return None;
            }
            let mean_conn = |p: &crate::data::Problem| -> f64 {
                if p.moves.is_empty() {
                    0.0
                } else {
                    let mut s = 0.0;
                    for m in &p.moves {
                        s += conn.get(m).copied().unwrap_or(0.0);
                    }
                    s / p.moves.len() as f64
                }
            };
            let firsts: Vec<(f64, f64)> = groups
                .iter()
                .filter_map(|(k, rs)| {
                    let p = pv.get(k)?;
                    if p.difficulty() == my.difficulty() && !p.moves.is_empty() {
                        Some((mean_conn(p), rs[0].1 as f64 / 60.0))
                    } else {
                        None
                    }
                })
                .collect();
            if firsts.len() < 8 {
                return None;
            }
            let mut cs: Vec<f64> = firsts.iter().map(|(c, _)| *c).collect();
            cs.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let (t1, t2) = (cs[cs.len() / 3], cs[2 * cs.len() / 3]);
            let tier = |c: f64| {
                if c <= t1 {
                    0
                } else if c <= t2 {
                    1
                } else {
                    2
                }
            };
            let mine_tier = tier(mean_conn(my));
            let pool: Vec<f64> = firsts
                .iter()
                .filter(|(c, _)| tier(*c) == mine_tier)
                .map(|(_, t)| *t)
                .collect();
            if pool.len() >= 8 {
                median(&pool)
            } else {
                median(&firsts.iter().map(|(_, t)| *t).collect::<Vec<_>>())
            }
        }
    };
    let base = base.max(1.0);
    Some((base, base * 2.0, base * 4.0))
}
