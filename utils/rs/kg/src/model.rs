// The fitted models the pick panel prices with: the contest ratings
// (utils/kg/clist.py's combined table), his Elo over the scored games, the
// cold-solve odds (curve.json "solve"), and the pacing forecast from the
// mined solve times (kg_lib.solve_forecast / drill_forecast).

use std::collections::{HashMap, HashSet};
use std::path::Path;

use chrono::NaiveDate;

use crate::ctx::{Ctx, PView};
use crate::data::{env_str, is_numeric_id, read_json};
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
    /// first sight: no earlier scored game on the problem
    pub first: bool,
    /// a FAILED file
    pub failed: bool,
    pub seconds: Option<i64>,
    /// a pass that ran past its tier's clock (budget_min)
    pub over: bool,
    /// the heaviest assist level on the solve
    pub assist: String,
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
    pub first: usize,
    pub first_fails: usize,
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
            s.first += usize::from(g.first);
            s.first_fails += usize::from(g.first && g.failed);
            s.won += g.score;
        }
        s
    }

    pub fn passes(&self) -> usize {
        self.solves - self.fails
    }

    /// The five lines as (before, ratio, after): the ratio is the part a
    /// caller colours. `lines()` joins them.
    pub fn rows(&self) -> Vec<(String, String, String)> {
        let pct = |a: usize, b: usize| {
            if b == 0 {
                "-".to_string()
            } else {
                format!("{:.0}%", 100.0 * a as f64 / b as f64)
            }
        };
        let repeats = self.solves - self.first;
        let repeat_fails = self.fails - self.first_fails;
        vec![
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
                ", what the Elo sees)".to_string(),
            ),
        ]
    }

    /// The five lines, plain text.
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
    let mut seen: HashSet<String> = HashSet::new();
    for i in order {
        let rec = ev.rec(i);
        let fname = ev.fname(i);
        let pnum = rec.problem.clone().unwrap_or_default();
        let diff = ctx.problem_difficulty(&pnum, &problems);
        if !is_numeric_id(&pnum) || budget_min(&diff).is_none() {
            continue;
        }
        let level = rec.assist_any();
        let failed = fname.contains("FAILED");
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
            } else if level == "hint" {
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
            first: seen.insert(pnum),
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
