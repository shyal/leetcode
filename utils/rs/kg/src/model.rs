// The fitted models the pick panel prices with: the contest ratings
// (utils/kg/clist.py's combined table), his Elo over the scored games, the
// cold-solve odds (curve.json "solve"), and the pacing forecast from the
// mined solve times (kg_lib.solve_forecast / drill_forecast).

use std::collections::{HashMap, HashSet};
use std::path::Path;
use std::rc::Rc;

use chrono::{Duration, NaiveDate};

use crate::ctx::{Ctx, PView};
use crate::data::{env_str, is_numeric_id, read_json, rejected_by_leetcode};
use crate::evidence::Evidence;
use crate::git::mined_solve_times;
use crate::status::node_conn;

pub const ELO_K: f64 = 32.0;
pub const ELO_START: f64 = 1200.0;
pub const FORECAST_WARM_DAYS: i64 = 30;

/// The three LeetCode labels: a problem under any other label is no game.
pub fn is_tier(d: &str) -> bool {
    matches!(d, "Easy" | "Medium" | "Hard")
}

/// The most a first sight costs the contests it is drawn into as a
/// companion (contest_fit), by its label. These were the flat
/// per-problem clocks until 2026-10-08; as caps they keep a solve slept
/// through at the keyboard from sinking every contest it lands in. The
/// pass being timed is never capped: it took as long as it took.
pub fn companion_cap_min(d: &str) -> i64 {
    match d {
        "Easy" => 10,
        "Medium" => 30,
        _ => 45,
    }
}

// ---- the contest clock -----------------------------------------------------

// The clock is the contest's (settled 2026-10-08): four problems, 90
// minutes, scored by how many are solved, with time only a tiebreaker.
// No real format times a problem on its own, and the flat 10/30/45
// budgets this replaced had no source. A pass is timed against the
// contest it would sit in: its slot is read off its rating, the other
// three slots are filled by your own first sights from those slots, and
// the pass is inside the clock when it fits beside them (contest_fit).
// Solving an easy problem fast, or giving up on a problem early, leaves
// time for the others, and this is where that time is counted.

pub const CONTEST_MIN: i64 = 90;
pub const CONTEST_SLOTS: usize = 4;

/// The slot cut points, fitted 2026-10-08 on the 2603 problems in
/// zerotrac's ratings.txt that name their contest slot, the way
/// EASY_BELOW was: the rating at which the two adjacent slots are
/// mislabelled at the same rate. 17% of Q1s sit at or above 1365 and
/// 17% of Q2s below it; 21% either side of 1663 (Q2/Q3); 21% either
/// side of 2035 (Q3/Q4).
pub const SLOT_CUTS: [f64; 3] = [1365.0, 1663.0, 2035.0];

/// The contest slot (0 to 3, for Q1 to Q4) a rating sits in.
pub fn contest_slot(rating: f64) -> usize {
    SLOT_CUTS.iter().filter(|c| rating >= **c).count()
}

/// The slot of a problem no contest rated, from its LeetCode label.
pub fn label_slot(difficulty: &str) -> usize {
    match difficulty {
        "Easy" => 0,
        "Hard" => 2,
        _ => 1,
    }
}

/// How often a pass of `seconds` in `slot` fits a contest drawn around
/// it. `others[j]` holds your first sights in slot j as (seconds,
/// failed), the seconds capped at companion_cap_min; each other slot is
/// filled by one of them, drawn uniformly, and a slot with no games in
/// it stays empty. A fail sinks the time spent before giving up, up to
/// the cap. Passes are taken shortest first, so a pass
/// no longer than this one is taken before it and costs its time, and
/// a longer one is taken after it and costs nothing. The result is the
/// fraction of draws in which this pass is taken within CONTEST_MIN,
/// counting in whole minutes rounded up.
pub fn contest_fit(seconds: i64, slot: usize, others: &[Vec<(i64, bool)>]) -> f64 {
    let minutes = |s: i64| ((s + 59) / 60) as usize;
    let cap = CONTEST_MIN as usize;
    let mine = minutes(seconds);
    if mine > cap {
        return 0.0;
    }
    let left = cap - mine;
    // dist[k] = P(the slots so far cost k minutes), k <= left
    let mut dist = vec![0.0; left + 1];
    dist[0] = 1.0;
    for (j, games) in others.iter().enumerate() {
        if j == slot || games.is_empty() {
            continue;
        }
        let w = 1.0 / games.len() as f64;
        let mut next = vec![0.0; left + 1];
        for &(s, failed) in games {
            let cost = if failed || s <= seconds {
                minutes(s)
            } else {
                0
            };
            if cost > left {
                continue; // this draw never fits
            }
            for k in 0..=left - cost {
                next[k + cost] += dist[k] * w;
            }
        }
        dist = next;
    }
    dist.iter().sum()
}

// ---- the display label ---------------------------------------------------

/// The cut points of the display label, fitted 2026-10-01 on the 2572
/// problems zerotrac rates. Each is the rating at which the two LeetCode
/// labels are wrong at the same rate: 11% of Easies sit at or above
/// EASY_BELOW and 11% of Mediums below it, 12% of Mediums sit at or above
/// HARD_FROM and 12% of Hards below it.
pub const EASY_BELOW: f64 = 1379.0;
pub const HARD_FROM: f64 = 1969.0;

/// The label a contest rating earns. It is for display only: the time
/// picker's rules keep LeetCode's label; the clock reads the rating
/// (contest_slot).
pub fn rating_label(rating: f64) -> &'static str {
    if rating < EASY_BELOW {
        "Easy"
    } else if rating < HARD_FROM {
        "Medium"
    } else {
        "Hard"
    }
}

/// The label shown for a problem: the one its rating earns, or LeetCode's
/// when nothing rates it.
pub fn display_difficulty(ctx: &Ctx, pnum: &str, pv: &PView) -> String {
    match solve_ratings(ctx).get(pnum) {
        Some(r) => rating_label(*r).to_string(),
        None => ctx.problem_difficulty(pnum, &pv.map),
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

/// kg_lib.target_pass_rate: TARGET_PASS_RATE in (0, 1), else 0.5. What
/// "ready" means to the simulators; the picker aims at aim_pass_rate.
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

/// The window of the aim: the last AIM_WINDOW first sights.
pub const AIM_WINDOW: usize = 20;
/// Fewer first sights than this in the window and the aim is the target.
pub const AIM_MIN_GAMES: usize = 10;
/// The aim never leaves this range, whatever the window scored.
pub const AIM_BOUNDS: (f64, f64) = (0.1, 0.9);

/// What the picker aims the cold-solve odds at (settled 2026-09-29).
#[derive(Clone, Debug, PartialEq)]
pub struct Aim {
    /// TARGET_PASS_RATE
    pub target: f64,
    /// first sights in the window
    pub games: usize,
    /// the mean of their scores, the quantity the fit predicts; None
    /// under AIM_MIN_GAMES games
    pub scored: Option<f64>,
    /// the odds the fit should give a served problem
    pub aim: f64,
}

/// The picker prices a walk by the fit's odds and serves the one nearest
/// the target. A walk the fit puts at the target has not scored at the
/// target: the first sights of September 2026 scored well under it, and
/// the target in .envrc was raised by hand from 0.50 to 0.65 to make up
/// the shortfall. This is that hand rule made automatic. The aim is the
/// target plus the shortfall of the last AIM_WINDOW first sights, their
/// mean score (the quantity the fit predicts) against the target: scoring
/// 0.30 against a target of 0.50 aims at 0.70, scoring 0.60 aims at
/// 0.40. A window scoring at the target aims at the target. Under
/// AIM_MIN_GAMES games the aim is the target; it stays inside AIM_BOUNDS.
pub fn aim_pass_rate(ctx: &Ctx, ev: &Evidence) -> Aim {
    let target = target_pass_rate();
    let scores: Vec<f64> = scored_games(ctx, ev)
        .iter()
        .filter(|g| g.first)
        .map(|g| g.score)
        .collect();
    let recent = &scores[scores.len().saturating_sub(AIM_WINDOW)..];
    let games = recent.len();
    if games < AIM_MIN_GAMES {
        return Aim {
            target,
            games,
            scored: None,
            aim: target,
        };
    }
    let scored = recent.iter().sum::<f64>() / games as f64;
    let aim = (target + (target - scored)).clamp(AIM_BOUNDS.0, AIM_BOUNDS.1);
    Aim {
        target,
        games,
        scored: Some(scored),
        aim,
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
    /// with no studied file before it, and no accepted submission on the
    /// leetcode account before that day (account_first_dates, make
    /// lc-sync). Every first-sight measure reads it: make stats, the Elo,
    /// the proven rating.
    pub first: bool,
    /// a FAILED file, or a submission leetcode rejected
    pub failed: bool,
    pub seconds: Option<i64>,
    /// how often the pass fits a contest beside your other first sights
    /// (contest_fit); None for a fail
    pub fit: Option<f64>,
    /// a pass that fits fewer than half the contests drawn around it
    pub over: bool,
    /// the heaviest assist level on the solve; "chain" for an unaided
    /// solve served from a combos chain whose assist is "hint"
    /// (data::chain_assist), "none" for one from a chain whose assist
    /// is "none"
    pub assist: String,
    /// served from a combos chain, whatever the chain's assist
    pub chain: bool,
}

impl Game {
    /// Served from a combos chain. A chain says in its own file what a
    /// solve from it scores (data::chain_assist): a plain unaided solve,
    /// or a hinted one at 1/2 because the chain names the technique. It
    /// is a first sight either way (settled 2026-10-08; until then chain
    /// solves were kept out of every first-sight measure).
    pub fn chain(&self) -> bool {
        self.chain
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
    /// first sights, chain solves included
    pub first: usize,
    pub first_fails: usize,
    /// solves served from a combos chain, first sight or not
    pub chain: usize,
    pub chain_fails: usize,
    pub chain_inside: usize,
    /// the chain solves that were repeats, so the repeat line can leave
    /// them out
    pub chain_repeats: usize,
    pub chain_repeat_fails: usize,
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
                s.chain_repeats += usize::from(!g.first);
                s.chain_repeat_fails += usize::from(!g.first && g.failed);
            }
            s.first += usize::from(g.first);
            s.first_fails += usize::from(g.first && g.failed);
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
        let repeats = self.solves - self.first - self.chain_repeats;
        let repeat_fails = self.fails - self.first_fails - self.chain_repeat_fails;
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

/// kg_lib.scored_games over the evidence, oldest first. Memoized on the
/// evidence: a pick asks for it many times (the band, the queue, the
/// replay) and each build reads files for every record. The replay
/// appends records between the calls; those add no game, so the memo
/// stays.
pub fn scored_games(ctx: &Ctx, ev: &Evidence) -> Vec<Game> {
    let memo = ev.cold_cache().scored.clone();
    if let Some((n, games, mined)) = memo {
        if (n..ev.len()).all(|i| adds_no_game(ctx, ev, i, &mined)) {
            if n < ev.len() {
                ev.cold_cache().scored = Some((ev.len(), games.clone(), mined));
            }
            return games.as_ref().clone();
        }
    }
    let (out, mined) = build_scored_games(ctx, ev);
    ev.cold_cache().scored = Some((ev.len(), Rc::new(out.clone()), Rc::new(mined)));
    out
}

/// Record `i` is no game (no time, not failed, no file on disk) and
/// leaves the others as they are: not a studied file, and not before
/// its problem's first record (the date `first` is measured from).
fn adds_no_game(ctx: &Ctx, ev: &Evidence, i: usize, mined: &HashSet<String>) -> bool {
    let (fname, rec) = (ev.fname(i), ev.rec(i));
    let after_first = || {
        let Some(p) = &rec.problem else { return true };
        ev.problem_recs(p)
            .iter()
            .filter(|(_, _, j)| *j < i)
            .map(|(d, _, _)| *d)
            .min()
            .is_none_or(|d| d <= rec.date.as_str())
    };
    rec.seconds.is_none()
        && !rec.learning
        && !fname.contains("FAILED")
        && !crate::clock::is_studied(fname)
        && !mined.contains(fname)
        && !ctx.root.join(fname).exists()
        && after_first()
}

fn build_scored_games(ctx: &Ctx, ev: &Evidence) -> (Vec<Game>, HashSet<String>) {
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
    let account = account_first_dates(&ctx.root);
    let mut studied: HashSet<String> = HashSet::new();
    let mut chain_assists: HashMap<String, String> = HashMap::new();
    for i in order {
        let rec = ev.rec(i);
        let fname = ev.fname(i);
        let pnum = rec.problem.clone().unwrap_or_default();
        let diff = ctx.problem_difficulty(&pnum, &problems);
        if !is_numeric_id(&pnum) || !is_tier(&diff) {
            continue;
        }
        // a studied file is no game, but the problem has been seen: no
        // later rep of it is a first sight
        if crate::clock::is_studied(fname) {
            studied.insert(pnum);
            continue;
        }
        // a learning solve is no game either, and the problem has been
        // seen the same way (kg::learning)
        if rec.learning {
            studied.insert(pnum);
            continue;
        }
        let chain = crate::data::combo_chain_of(&ctx.root, fname);
        let level = match (rec.assist_any(), &chain) {
            ("none", Some(name)) => {
                let assist = chain_assists
                    .entry(name.clone())
                    .or_insert_with(|| crate::data::chain_assist(&ctx.root, name));
                if assist == "none" {
                    "none"
                } else {
                    "chain"
                }
            }
            (l, _) => l,
        };
        // a walk-away, or a submission leetcode rejected (TLE, WA, RE)
        let failed = fname.contains("FAILED") || rejected_by_leetcode(&ctx.root, fname);
        // the record's own clock; a record older than the field
        // (2026-09-16) falls back to the time mined from its commit
        let seconds = rec.seconds.or_else(|| secs.get(fname).copied());
        // a pass with no time on record is no game
        if !failed && seconds.is_none() {
            continue;
        }
        out.push(Game {
            date: rec.date.clone(),
            problem: pnum.clone(),
            difficulty: diff,
            score: 0.0,
            moves: rec.moves.keys().cloned().collect(),
            fname: fname.to_string(),
            first: first_day.get(&pnum) == Some(&rec.date)
                && !studied.contains(&pnum)
                && account.get(&pnum).is_none_or(|d| *d >= rec.date),
            failed,
            seconds,
            fit: None,
            over: false,
            assist: level.to_string(),
            chain: chain.is_some(),
        });
    }
    // the contest clock: every pass is timed beside your first sights
    // in the other slots, over the whole record
    let ratings = solve_ratings(ctx);
    let slot = |g: &Game| match ratings.get(&g.problem) {
        Some(r) => contest_slot(*r),
        None => label_slot(&g.difficulty),
    };
    let mut slots: Vec<Vec<(i64, bool)>> = vec![vec![]; CONTEST_SLOTS];
    for g in out.iter().filter(|g| g.first) {
        if let Some(s) = g.seconds {
            let cap = companion_cap_min(&g.difficulty) * 60;
            slots[slot(g)].push((s.min(cap), g.failed));
        }
    }
    for g in out.iter_mut() {
        if let Some(s) = g.seconds.filter(|_| !g.failed) {
            let fit = contest_fit(s, slot(g), &slots);
            g.fit = Some(fit);
            g.over = fit < 0.5;
        }
        g.score = if g.failed || g.over || g.assist == "walkthrough" || g.assist == "learning" {
            0.0
        } else if g.assist == "hint" || g.assist == "chain" {
            0.5
        } else {
            1.0
        };
    }
    (out, secs.into_keys().collect())
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
            if g.first && *rating >= before - AT_RATING_BAND && inside(g) {
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
            if !g.first || since.is_some_and(|s| day < s) {
                continue;
            }
            let Some(practiced) = moves_practiced(g, ev, problems) else {
                continue;
            };
            let cold = usize::from(g.score == 1.0);
            if practiced {
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

/// Whether every move the game's problem needs (problems.json) has a
/// record, a drill or another problem, dated before the game; None when
/// the problem lists no moves.
pub fn moves_practiced(g: &Game, ev: &Evidence, problems: &crate::data::Problems) -> Option<bool> {
    let day = crate::data::parse_date(&g.date);
    let p = problems.get(&g.problem).filter(|p| !p.moves.is_empty())?;
    Some(
        p.moves
            .iter()
            .all(|m| ev.node_entries(m).iter().any(|e| e.date < day)),
    )
}

/// Width of one band in the rating table of `make stats`.
pub const RATING_BAND: f64 = 100.0;

/// One rating band of the games in a window: the first sights, the first
/// sights whose moves were all practiced before (as Transfer counts
/// them), and the repeats, each with its cold wins (score 1). Asked on
/// 2026-10-16: Summary and Transfer put every rating together, so a fall
/// with the rating reads as a fall in transfer.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Band {
    /// the lowest rating in the band, a multiple of RATING_BAND
    pub low: i64,
    pub first: usize,
    pub first_cold: usize,
    pub practiced: usize,
    pub practiced_cold: usize,
    pub repeat: usize,
    pub repeat_cold: usize,
}

impl Band {
    /// The bands of `games`, lowest first; a game whose problem has no
    /// rating is left out.
    pub fn of(
        games: &[Game],
        ev: &Evidence,
        problems: &crate::data::Problems,
        rating: impl Fn(&str) -> Option<f64>,
    ) -> Vec<Band> {
        let mut bands: std::collections::BTreeMap<i64, Band> = Default::default();
        for g in games {
            let Some(r) = rating(&g.problem) else {
                continue;
            };
            let low = ((r / RATING_BAND).floor() * RATING_BAND) as i64;
            let b = bands.entry(low).or_insert_with(|| Band {
                low,
                ..Default::default()
            });
            let cold = usize::from(g.score == 1.0);
            if g.first {
                b.first += 1;
                b.first_cold += cold;
                if moves_practiced(g, ev, problems) == Some(true) {
                    b.practiced += 1;
                    b.practiced_cold += cold;
                }
            } else {
                b.repeat += 1;
                b.repeat_cold += cold;
            }
        }
        bands.into_values().collect()
    }
}

// ---- first-sight Elo -------------------------------------------------------

// The one first-sight Elo: the number on `make elo` and the README badge.
// Problem ratings are zerotrac's (data/leetcode_ratings.tsv); a problem
// that never ran in a contest gets the median contest rating of its
// difficulty. Only first sights are games (Game::first), chain solves
// among them since 2026-10-08, and only the easies within the contest's
// share (easy_share, 2026-10-11). Standard Elo, ELO_K from ELO_START. The
// picker keeps its own over every timed attempt (elo_games, settled
// 2026-09-12). The proven rating (below) reads every first sight: a win
// there proves only the problem's rating, so easies cannot inflate it.

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

/// problem -> the local day of the leetcode account's first accepted
/// submission of it (data/leetcode_submissions.json, written by make
/// lc-sync); empty with no file. A first sight (Game::first) has none
/// before its day: the account goes back to 2020, the evidence to
/// October 2025, and a problem solved in between is a repeat here
/// whatever solved/ holds (settled 2026-10-11).
pub fn account_first_dates(root: &std::path::Path) -> HashMap<String, String> {
    let mut out: HashMap<String, String> = HashMap::new();
    let Some(v) = crate::data::read_json(&root.join("data/leetcode_submissions.json")) else {
        return out;
    };
    for s in v["submissions"].as_array().into_iter().flatten() {
        let (Some(n), Some(d)) = (s["number"].as_str(), s["date"].as_str()) else {
            continue;
        };
        let e = out.entry(n.to_string()).or_insert_with(|| d.to_string());
        if d < e.as_str() {
            *e = d.to_string();
        }
    }
    out
}

/// The account's first acceptance of `pnum` when it came before `day`
/// (an ISO date): the problem is a repeat for the Elo and the proven
/// rating whatever the evidence holds (Game::first). None otherwise.
pub fn account_repeat(account: &HashMap<String, String>, pnum: &str, day: &str) -> Option<String> {
    account.get(pnum).filter(|d| d.as_str() < day).cloned()
}

/// Whether a solve of `pnum` on `day` would be a first sight: no record of
/// it in the evidence and no acceptance on the account before that day.
/// The serve reads this where it labels a pick a first sight (the queue,
/// `make rep`, the hook line, the Elo swing under `make next`), so the
/// label agrees with Game::first. Before 2026-10-13 those read the
/// evidence alone: 398 was served as a first sight and scored as a
/// repeat of 2020-08-25.
pub fn first_sight_open(
    ev: &Evidence,
    account: &HashMap<String, String>,
    pnum: &str,
    day: &str,
) -> bool {
    ev.problem_recs(pnum).is_empty() && account_repeat(account, pnum, day).is_none()
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

/// `games` priced (pricing), oldest first, each game's score read
/// through `score`.
fn priced(ctx: &Ctx, games: Vec<Game>, score: fn(&Game) -> f64) -> Vec<FirstSight> {
    let (ratings, imputed) = pricing(ctx);
    games
        .into_iter()
        .map(|g| {
            (
                crate::data::parse_date(&g.date),
                price(&ratings, &imputed, &g.problem, &g.difficulty),
                score(&g),
            )
        })
        .collect()
}

/// Every scored first-sight attempt, oldest first.
fn first_sights(ctx: &Ctx, ev: &Evidence) -> Vec<Game> {
    scored_games(ctx, ev)
        .into_iter()
        .filter(|g| g.first)
        .collect()
}

/// The contest's share of easies (settled 2026-10-11). A weekly contest
/// is four problems, one of them Easy; two easies, two mediums and a hard
/// is the generous reading, and that is the quota: of any EASY_WINDOW
/// games the Elo counts in a row, at most EASY_QUOTA are Easy. An Easy
/// past the quota is not a game. It is left out of the Elo, not scored
/// against it, because the solve was real; it just proves nothing a
/// contest would ask. Of the 466 first sights to 2026-10-11, 293 were
/// Easy, in runs of fifty through October and November 2025; the rule
/// leaves 237 of them out and takes that era's Elo from 1970 to 1890.
/// The rest of the 2000 was 65 mediums won of 92, which Elo at K=32
/// reads as it should.
pub const EASY_WINDOW: usize = 5;
pub const EASY_QUOTA: usize = 2;

/// Which of `difficulties`, oldest first, the Elo counts: every problem
/// that is not Easy, and an Easy only while fewer than EASY_QUOTA of the
/// EASY_WINDOW - 1 games counted before it are Easy. The window is over
/// the games counted, not the games played, so fifty easies in a row
/// count two, and the next Easy counts once three harder games have.
pub fn easy_share(difficulties: &[&str]) -> Vec<bool> {
    let mut counted: Vec<bool> = Vec::new(); // true for each Easy counted
    difficulties
        .iter()
        .map(|d| {
            let easy = *d == "Easy";
            let tail = counted.len().saturating_sub(EASY_WINDOW - 1);
            let keep = !easy || counted[tail..].iter().filter(|e| **e).count() < EASY_QUOTA;
            if keep {
                counted.push(easy);
            }
            keep
        })
        .collect()
}

/// The first-sight games the Elo counts (easy_share), oldest first.
fn counted_first_sights(ctx: &Ctx, ev: &Evidence) -> Vec<Game> {
    let games = first_sights(ctx, ev);
    let difficulties: Vec<&str> = games.iter().map(|g| g.difficulty.as_str()).collect();
    let keep = easy_share(&difficulties);
    games
        .into_iter()
        .zip(keep)
        .filter_map(|(g, k)| k.then_some(g))
        .collect()
}

/// [(date, problem rating, Elo score)]: the games of the first-sight Elo,
/// the first sights within the contest's share of easies.
pub fn first_sight_elo_games(ctx: &Ctx, ev: &Evidence) -> Vec<FirstSight> {
    priced(ctx, counted_first_sights(ctx, ev), |g| g.score)
}

/// How many first sights the Elo leaves out: the easies past the quota.
pub fn easies_left_out(ctx: &Ctx, ev: &Evidence) -> usize {
    first_sights(ctx, ev).len() - counted_first_sights(ctx, ev).len()
}

/// [(date, problem rating, proven score)]: every first sight, the easies
/// past the quota too, scored for the proven rating (proven_game_score).
pub fn proven_games(ctx: &Ctx, ev: &Evidence) -> Vec<FirstSight> {
    priced(ctx, first_sights(ctx, ev), proven_game_score)
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

/// The spread of the prior on the fitted rating, in rating points: the
/// prior sits on the window's median problem rating. It keeps a window of
/// wins only finite; on a window with losses in it the games outweigh it.
pub const PROVEN_PRIOR_SD: f64 = 200.0;

/// (rating, standard error) fitted to one window of first sights
/// (2026-10-18): the rating that makes the scores most likely under the
/// Elo curve, P(win) = 1 / (1 + 10^((problem - rating) / 400)), with a
/// pass short of a cold win scored 0.5 and a fail or a copy 0. A fail on
/// a 2000 costs less than a fail on a 1400, so the rating is not held
/// under the problems served. It replaces the mean of a per-game score
/// (2026-09-20: the rating, less 200 for a hint, less 400 for a fail),
/// which could never rise above the problems served. A win proves
/// nothing beyond the problem (a 1250 cannot tell a 1700 from a 1900),
/// so the fit is held to the median rating of the problems won cold in
/// the window. The hardest one won was tried first: one Hard among
/// twenty-nine easy wins let 2025 fit 1950.
pub fn proven_fit(games: &[(NaiveDate, f64, f64)]) -> (f64, f64) {
    let s = 400.0 / std::f64::consts::LN_10;
    let rs: Vec<f64> = games.iter().map(|(_, r, _)| *r).collect();
    let mu = median(&rs);
    let prior = 1.0 / (PROVEN_PRIOR_SD * PROVEN_PRIOR_SD);
    let mut t = mu;
    let mut info = prior;
    for _ in 0..50 {
        let mut grad = -(t - mu) * prior;
        info = prior;
        for (_, r, y) in games {
            let p = 1.0 / (1.0 + 10f64.powf((r - t) / 400.0));
            grad += (y.clamp(0.0, 1.0) - p) / s;
            info += p * (1.0 - p) / (s * s);
        }
        let step = grad / info;
        t += step;
        if step.abs() < 1e-6 {
            break;
        }
    }
    let won: Vec<f64> = games
        .iter()
        .filter(|(_, _, y)| *y >= 1.0)
        .map(|(_, r, _)| *r)
        .collect();
    if !won.is_empty() {
        t = t.min(median(&won));
    }
    (t, 1.0 / info.sqrt())
}

/// [(date, proven rating)] one per first-sight game from the
/// PROVEN_WINDOW-th on: proven_fit over the last PROVEN_WINDOW games.
pub fn proven_series(games: &[(NaiveDate, f64, f64)]) -> Vec<(NaiveDate, f64)> {
    proven_fits(games)
        .into_iter()
        .map(|(d, r, _)| (d, r))
        .collect()
}

/// proven_series with each point's standard error.
pub fn proven_fits(games: &[(NaiveDate, f64, f64)]) -> Vec<(NaiveDate, f64, f64)> {
    let n = PROVEN_WINDOW;
    if games.len() < n {
        return vec![];
    }
    (n - 1..games.len())
        .map(|i| {
            let (r, se) = proven_fit(&games[i + 1 - n..=i]);
            (games[i].0, r, se)
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

/// The best has to lead the rating now by this much to be named.
pub const PROGRESS_LEVEL_POINTS: f64 = 50.0;
/// The rating has to move this many standard errors of the difference
/// (proven_fit, now and PROGRESS_LEVEL_DAYS ago) to count as a move at
/// all; under it the level is called flat.
pub const PROGRESS_LEVEL_Z: f64 = 2.0;
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
    /// the standard error of `now`
    pub se_now: Option<f64>,
    /// the proven rating PROGRESS_LEVEL_DAYS ago (the first point on or after)
    pub then: Option<f64>,
    /// the standard error of `then`
    pub se_then: Option<f64>,
    /// the best proven rating before now, over the whole series
    pub best: Option<f64>,
    /// the median rating of the last PROVEN_WINDOW first sights served
    pub served: Option<f64>,
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
    /// The proven rating now less then, 0 without both. The fit credits
    /// a harder problem on its own, so the rating is read directly; the
    /// gap to the median served (2026-09-25) is gone: the mean it was
    /// read on could not rise above the problems served (2026-10-18).
    pub fn delta(&self) -> f64 {
        match (self.now, self.then) {
            (Some(n), Some(t)) => n - t,
            _ => 0.0,
        }
    }

    /// The smallest delta that counts as a move: PROGRESS_LEVEL_Z
    /// standard errors of the difference, infinite without both.
    pub fn level_bar(&self) -> f64 {
        match (self.se_now, self.se_then) {
            (Some(a), Some(b)) => PROGRESS_LEVEL_Z * (a * a + b * b).sqrt(),
            _ => f64::INFINITY,
        }
    }

    /// The one-word verdict of `make progress`, lower case: progressing,
    /// slipping, stalled, grinding, rebuilding, gaining; "not training"
    /// under five games in the window.
    pub fn verdict(&self) -> &'static str {
        let g = &self.ground;
        if self.recent < 5 {
            "not training"
        } else if self.delta() >= self.level_bar() {
            "progressing"
        } else if self.delta() <= -self.level_bar() {
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
    let fits = proven_fits(&fs);
    out.proven = fits.iter().map(|(d, r, _)| (*d, *r)).collect();
    let level_since = today - Duration::days(PROGRESS_LEVEL_DAYS);
    out.now = fits.last().map(|(_, r, _)| *r);
    out.se_now = fits.last().map(|(_, _, se)| *se);
    let then_at = fits.iter().position(|(d, _, _)| *d >= level_since);
    out.then = then_at.map(|i| fits[i].1);
    out.se_then = then_at.map(|i| fits[i].2);
    out.served = served_series(&fs).last().copied();
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

/// The two ratings in words: "It was about 1830 then and is about 1650
/// now, each correct to about 100".
fn against(p: &Progress, ten: impl Fn(f64) -> i64) -> String {
    let se = p.se_now.unwrap_or(0.0).max(p.se_then.unwrap_or(0.0));
    format!(
        "It was about {} then and is about {} now, each correct to about {}",
        ten(p.then.unwrap_or(0.0)),
        ten(p.now.unwrap_or(0.0)),
        ten(se),
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
                "The rating you have proven on problems never seen before is up about {} points since {}. {}{}.",
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
                "The rating you have proven on problems never seen before is down about {} points since {}. {}.",
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
    if let (Some(then), false) = (p.then, moved) {
        out[1].push_str(&format!(
            " It was about {} in {}; the change since is smaller than the error of the two ratings.",
            ten(then),
            month_name(level_since)
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

/// His first-sight Elo after the last first-sight game, or ELO_START with
/// none: the elo the picker, the queue and both bands rate a problem
/// against (2026-10-02). elo_now also scores repeats, which are easier to
/// win, so it runs higher.
pub fn first_sight_elo_now(ctx: &Ctx, ev: &Evidence) -> f64 {
    elo_after(&first_sight_elo_games(ctx, ev), ELO_START)
        .last()
        .map_or(ELO_START, |x| x.1)
}

/// kg_lib.elo_now: his Elo after the last scored game, repeats included.
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
