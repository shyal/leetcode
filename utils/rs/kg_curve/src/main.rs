// kg_curve - fit a personal forgetting curve from evidence.json and write
// graph/curve.json, which node_status uses instead of the flat 42-day
// window (delete curve.json to fall back).
//
//   make curve                 # refit from current evidence + report
//   kg_curve --if-stale        # refit only when evidence.json (or a knob) is newer
//   kg_curve --solve-report    # held-out comparison of the cold-solve model
//   kg_curve --solve-rows-json # the per-game feature rows (kg_progress_svg)
//
// Fit knobs, for experimenting with what the trial pool should say (CLI
// flag or env var; .envrc carries them, and --if-stale treats a knob change
// as stale):
//   --since YYYY-MM-DD / CURVE_SINCE       era boundary: older trials dropped
//   --half-life DAYS   / CURVE_HALF_LIFE   recency weight 0.5^(age/half-life)
//
// Model: power-law forgetting with a slip rate.
//   P(recall after gap D) = (1-slip) * (1 + D/s)^(-beta)
//   s = exp(a + b*log1p(cleans) - c*struggles - d*assist + e*(conn - conn_mean))
// Fit by maximum likelihood on recall trials: a trial is the FIRST solve of
// a node on a day, when the node had at least one prior unaided clean;
// success if clean and unaided, failure if struggled or helped; a learning
// solve is censored. Same-day reps count as one clean rep.
//
// The cold-solve model (curve.json "solve"): one logistic on the games
// kg::model::scored_games scores, features forward-selected on held-out
// expanding-window folds.
//
// Ported from utils/kg/kg_curve (Python) on 2026-09-12. The sums follow
// numpy's pairwise order so the gradient descent lands on the same digits.
// Not ported: the matplotlib report picture (matplotlib was never
// installed, so the Python skipped it too). The --solve-report bootstrap
// uses its own RNG; its confidence intervals are not numpy's.

use std::collections::{HashMap, HashSet};

use chrono::NaiveDate;
use indexmap::IndexMap;
use kg::bank::carrier_counts;
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{assist_weight, load_envrc, parse_date, repo_root};
use kg::evidence::Evidence;
use kg::linalg::{inverse, np_sum, round_to, solve, xtwx};
use kg::model::{elo_drift, elo_games, elo_now, solve_ratings, walk_mass};
use kg::pyjson::{self, dumps, float_repr, g as py_g};
use kg::status::node_conn;
use regex::Regex;
use serde_json::{json, Map, Value};

const TARGET_RETENTION: f64 = 0.9;
const GAP_BUCKETS: [(i64, i64); 6] = [(1, 7), (8, 21), (22, 42), (43, 90), (91, 180), (181, 400)];
const SOLVE_FEATURES: [&str; 7] = [
    "gap",
    "rating",
    "recall",
    "unseen",
    "experience",
    "mass",
    "length",
];
const SOLVE_FOLDS: usize = 5;
const SOLVE_LAMBDAS: [f64; 6] = [0.0, 0.1, 0.3, 1.0, 3.0, 10.0];

/// (date, ts, verdict, assist, node_assist) of one move on one record
type Event = (String, String, String, String, String);

/// (gap, success, cleans, struggles, assist, conn, date)
#[derive(Clone, Debug, PartialEq)]
pub struct Trial {
    pub gap: i64,
    pub success: i64,
    pub cleans: i64,
    pub struggles: i64,
    pub assist: f64,
    pub conn: f64,
    pub date: NaiveDate,
}

/// kg_curve.extract_trials(with_date=True, with_conn=True).
fn extract_trials(ctx: &Ctx, ev: &Evidence, pv: &PView) -> Vec<Trial> {
    let ts_re = Regex::new(r"\d{4}_\d{2}_\d{2}T[\d_]+").unwrap();
    // (date, ts, verdict, assist, node_assist): assist is the help actually
    // taken; node_assist is what node_eval charges the node for, "none" on
    // the first rep of a drill
    let mut events: IndexMap<String, Vec<Event>> = IndexMap::new();
    for (idx, (fname, rec)) in ev.recs.iter().enumerate() {
        let ts = ts_re
            .find(fname)
            .map(|m| m.as_str().to_string())
            .unwrap_or_default();
        let first = ev.first_reps.contains(&idx);
        for (node, verdict) in &rec.moves {
            let a = rec.assist_for(node).to_string();
            let na = if first { "none".to_string() } else { a.clone() };
            events.entry(node.clone()).or_default().push((
                rec.date.clone(),
                ts.clone(),
                verdict.clone(),
                a,
                na,
            ));
        }
    }
    let conn = node_conn(pv, ctx);
    let mut trials = Vec::new();
    for (node, evs) in events.iter_mut() {
        evs.sort();
        let mut days: IndexMap<String, Vec<(String, String, String)>> = IndexMap::new();
        for (d, _, v, a, na) in evs.iter() {
            days.entry(d.clone())
                .or_default()
                .push((v.clone(), a.clone(), na.clone()));
        }
        days.sort_keys();
        let (mut last_clean, mut cleans, mut struggles, mut assisted) =
            (None::<NaiveDate>, 0i64, 0i64, 0.0f64);
        let mut retrieved = false;
        for (d, reps) in &days {
            let (verdict, assist, _) = &reps[0];
            if retrieved && (verdict == "clean" || verdict == "struggled") && assist != "learning" {
                let gap = (parse_date(d) - last_clean.unwrap()).num_days();
                if gap >= 1 {
                    trials.push(Trial {
                        gap,
                        success: i64::from(verdict == "clean" && assist == "none"),
                        cleans,
                        struggles,
                        assist: assisted,
                        conn: *conn.get(node).unwrap_or(&0.0),
                        date: parse_date(d),
                    });
                }
            }
            let mut day_clean = 0;
            for (v, a, na) in reps {
                if v == "clean" && na != "learning" {
                    day_clean = 1;
                    last_clean = Some(parse_date(d));
                    retrieved = retrieved || a == "none";
                } else if v == "struggled" {
                    struggles += 1;
                }
                assisted += assist_weight(na);
            }
            cleans += day_clean;
        }
    }
    trials
}

/// kg_curve.select_trials: (trials, weights or None).
pub fn select_trials(
    trials: &[Trial],
    since: Option<NaiveDate>,
    half_life: Option<f64>,
) -> (Vec<Trial>, Option<Vec<f64>>) {
    let kept: Vec<Trial> = trials
        .iter()
        .filter(|t| since.is_none_or(|s| t.date >= s))
        .cloned()
        .collect();
    if kept.is_empty() {
        return (vec![], None);
    }
    let weights = half_life.map(|h| {
        let newest = kept.iter().map(|t| t.date).max().unwrap();
        kept.iter()
            .map(|t| 0.5f64.powf((newest - t.date).num_days() as f64 / h))
            .collect()
    });
    (kept, weights)
}

#[derive(Clone, Copy, Debug)]
pub struct Params {
    pub a: f64,
    pub b: f64,
    pub c: f64,
    pub d: f64,
    pub e: f64,
    pub conn_mean: f64,
    pub beta: f64,
    pub slip: f64,
}

/// kg_curve.fit (the numpy path): MLE by gradient descent, 8000 steps,
/// every sum in numpy's pairwise order.
pub fn fit(trials: &[Trial], weights: Option<&[f64]>) -> Params {
    let n = trials.len();
    let iters = 8000;
    let lr = 0.05;
    let gap: Vec<f64> = trials.iter().map(|t| t.gap as f64).collect();
    let sf: Vec<f64> = trials.iter().map(|t| t.success as f64).collect();
    let k: Vec<f64> = trials.iter().map(|t| (t.cleans as f64).ln_1p()).collect();
    let m: Vec<f64> = trials.iter().map(|t| t.struggles as f64).collect();
    let x: Vec<f64> = trials.iter().map(|t| t.assist).collect();
    let cn: Vec<f64> = trials.iter().map(|t| t.conn).collect();
    let w: Vec<f64> = match weights {
        Some(ws) => ws.to_vec(),
        None => vec![1.0; n],
    };
    let wsum = np_sum(&w);
    let wcn: Vec<f64> = w.iter().zip(&cn).map(|(a, b)| a * b).collect();
    let conn_mean = np_sum(&wcn) / wsum;
    let cnc: Vec<f64> = cn.iter().map(|c| c - conn_mean).collect();
    let (mut a, mut b, mut c, mut d, mut e, mut beta, mut slip) =
        (60f64.ln(), 0.05, 0.05, 0.05, 0.0, 0.5, 0.05);
    let mut u = vec![0.0; n];
    let mut dlns = vec![0.0; n];
    let mut ee = vec![0.0; n];
    let mut tmp = vec![0.0; n];
    for it in 0..iters {
        for i in 0..n {
            u[i] = gap[i] / (a + b * k[i] - c * m[i] - d * x[i] + e * cnc[i]).exp();
            let mem = (1.0 + u[i]).powf(-beta);
            let p = ((1.0 - slip) * mem).clamp(1e-9, 1.0 - 1e-9);
            ee[i] = w[i] * (sf[i] - (1.0 - sf[i]) * p / (1.0 - p));
            dlns[i] = ee[i] * beta * u[i] / (1.0 + u[i]);
        }
        let step = lr / (1.0 + it as f64 / 2000.0) / wsum;
        a += step * np_sum(&dlns);
        for i in 0..n {
            tmp[i] = dlns[i] * k[i];
        }
        b = (b + step * np_sum(&tmp)).max(0.0);
        for i in 0..n {
            tmp[i] = -dlns[i] * m[i];
        }
        c = (c + step * np_sum(&tmp)).max(0.0);
        for i in 0..n {
            tmp[i] = -dlns[i] * x[i];
        }
        d = (d + step * np_sum(&tmp)).max(0.0);
        for i in 0..n {
            tmp[i] = dlns[i] * cnc[i];
        }
        e += step * np_sum(&tmp);
        for i in 0..n {
            tmp[i] = -ee[i] * u[i].ln_1p();
        }
        beta = (beta + step * np_sum(&tmp)).clamp(0.02, 5.0);
        for i in 0..n {
            tmp[i] = -ee[i] / (1.0 - slip);
        }
        slip = (slip + step * np_sum(&tmp)).clamp(0.0, 0.25);
    }
    Params {
        a,
        b,
        c,
        d,
        e,
        conn_mean,
        beta,
        slip,
    }
}

impl Params {
    fn stab(&self, k: i64, m: i64, x: f64, cn: Option<f64>) -> f64 {
        let cn = cn.unwrap_or(self.conn_mean);
        (self.a + self.b * (k as f64).ln_1p() - self.c * m as f64 - self.d * x
            + self.e * (cn - self.conn_mean))
            .exp()
    }

    fn pred(&self, gap: i64, k: i64, m: i64, x: f64, cn: Option<f64>) -> f64 {
        (1.0 - self.slip) * (1.0 + gap as f64 / self.stab(k, m, x, cn)).powf(-self.beta)
    }
}

/// kg_curve.loglik: the weighted mean log-likelihood (Python's sequential sums).
fn loglik(trials: &[Trial], p: &Params, weights: Option<&[f64]>) -> f64 {
    let mut num = 0.0;
    let mut den = 0.0;
    for (i, t) in trials.iter().enumerate() {
        let w = weights.map_or(1.0, |ws| ws[i]);
        let pr = p.pred(t.gap, t.cleans, t.struggles, t.assist, Some(t.conn));
        let v = if t.success == 1 {
            pr
        } else {
            1.0 - pr.min(1.0 - 1e-9)
        };
        num += w * v.max(1e-9).ln();
        den += w;
    }
    num / den
}

fn sigmoid(z: f64) -> f64 {
    1.0 / (1.0 + (-z).exp())
}

fn matvec(x: &[Vec<f64>], w: &[f64]) -> Vec<f64> {
    x.iter()
        .map(|row| row.iter().zip(w).map(|(a, b)| a * b).sum())
        .collect()
}

/// Newton's method on the (ridge-penalised) log-likelihood; the intercept
/// (column 0) is never penalised. kg_curve._logistic (and fit_mass's loop
/// with lam = 0, iters = 25, tol 1e-8).
fn logistic(x: &[Vec<f64>], y: &[f64], lam: f64, iters: usize, tol: f64) -> Vec<f64> {
    let p = x[0].len();
    let mut w = vec![0.0; p];
    for _ in 0..iters {
        let pr: Vec<f64> = matvec(x, &w).into_iter().map(sigmoid).collect();
        let mut grad = vec![0.0; p];
        for (row, (yi, pi)) in x.iter().zip(y.iter().zip(&pr)) {
            for j in 0..p {
                grad[j] += row[j] * (yi - pi);
            }
        }
        for j in 1..p {
            grad[j] -= lam * w[j];
        }
        let wts: Vec<f64> = pr.iter().map(|q| q * (1.0 - q)).collect();
        let hess = xtwx(x, &wts, lam, true, 1e-6);
        let step = solve(&hess, &grad).expect("hessian");
        for j in 0..p {
            w[j] += step[j];
        }
        if step.iter().map(|s| s.abs()).fold(0.0, f64::max) < tol {
            break;
        }
    }
    w
}

fn mean_loglik(x: &[Vec<f64>], y: &[f64], w: &[f64]) -> f64 {
    let terms: Vec<f64> = matvec(x, w)
        .into_iter()
        .zip(y)
        .map(|(z, yi)| {
            let pr = sigmoid(z).clamp(1e-9, 1.0 - 1e-9);
            yi * pr.ln() + (1.0 - yi) * (1.0 - pr).ln()
        })
        .collect();
    np_sum(&terms) / terms.len() as f64
}

/// kg_curve.fit_mass: rehearsal mass as a predictor of a clean cold first
/// attempt, one intercept per difficulty.
fn fit_mass(ctx: &Ctx, ev: &Evidence, pv: &PView) -> Value {
    let counts = carrier_counts(&pv.map);
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| {
        (ev.rec(a).date.as_str(), ev.fname(a)).cmp(&(ev.rec(b).date.as_str(), ev.fname(b)))
    });
    let mut seen: HashSet<String> = HashSet::new();
    let mut rows: Vec<(String, f64, bool)> = Vec::new();
    for i in order {
        let rec = ev.rec(i);
        let pnum = rec.problem.clone().unwrap_or_default();
        if !pnum.chars().next().is_some_and(|c| c.is_ascii_digit())
            || seen.contains(&pnum)
            || rec.moves.is_empty()
        {
            continue;
        }
        seen.insert(pnum.clone());
        let dif = ctx.problem_difficulty(&pnum, &pv.map);
        if !matches!(dif.as_str(), "Easy" | "Medium" | "Hard") {
            continue;
        }
        let clean = rec.moves.values().all(|v| v == "clean") && rec.assist_any() == "none";
        let moves: Vec<String> = rec.moves.keys().cloned().collect();
        rows.push((dif, walk_mass(&moves, &counts), clean));
    }
    if rows.len() < 30 {
        return json!({"beta": 0.0, "se": 0.0, "n": rows.len(), "by_difficulty": {}});
    }
    let difs = ["Easy", "Medium", "Hard"];
    let x: Vec<Vec<f64>> = rows
        .iter()
        .map(|(d, m, _)| {
            let mut r: Vec<f64> = difs
                .iter()
                .map(|dd| if d == dd { 1.0 } else { 0.0 })
                .collect();
            r.push(*m);
            r
        })
        .collect();
    let y: Vec<f64> = rows
        .iter()
        .map(|(_, _, c)| if *c { 1.0 } else { 0.0 })
        .collect();
    let w = logistic(&x, &y, 0.0, 25, 1e-8);
    let pr: Vec<f64> = matvec(&x, &w).into_iter().map(sigmoid).collect();
    let wts: Vec<f64> = pr.iter().map(|q| q * (1.0 - q)).collect();
    let cov = inverse(&xtwx(&x, &wts, 0.0, true, 1e-6)).expect("covariance");
    let mut by = Map::new();
    for (i, d) in difs.iter().enumerate() {
        by.insert(d.to_string(), json!(round_to(w[i], 4)));
    }
    json!({
        "beta": round_to(w[3], 4),
        "se": round_to(cov[3][3].sqrt(), 4),
        "n": rows.len(),
        "by_difficulty": Value::Object(by),
    })
}

/// One scored game's features, its outcome and its date (kg_curve.solve_rows).
struct Row {
    features: IndexMap<&'static str, f64>,
    /// the recall sum had no terms: Python's sum() of nothing is the int 0
    recall_empty: bool,
    y: f64,
    date: String,
}

fn solve_rows(
    ctx: &Ctx,
    ev: &Evidence,
    pv: &PView,
    p: &Params,
    ratings: &HashMap<String, f64>,
) -> Vec<Row> {
    let mut cleans: HashMap<&str, Vec<&str>> = HashMap::new();
    for (_, rec) in &ev.recs {
        for (mv, verdict) in &rec.moves {
            if verdict == "clean" {
                cleans
                    .entry(mv.as_str())
                    .or_default()
                    .push(rec.date.as_str());
            }
        }
    }
    for v in cleans.values_mut() {
        v.sort();
    }
    let recall = |mv: &str, day: &str| -> Option<f64> {
        let seen = cleans.get(mv)?;
        let i = seen.partition_point(|d| *d < day);
        if i == 0 {
            return None;
        }
        let prior = &seen[..i];
        let distinct: HashSet<&&str> = prior.iter().collect();
        let s = (p.a + p.b * (distinct.len() as f64).ln_1p())
            .exp()
            .clamp(7.0, 3650.0);
        let gap = (parse_date(day) - parse_date(prior[prior.len() - 1])).num_days();
        Some((1.0 + gap as f64 / s).powf(-p.beta))
    };
    let counts = carrier_counts(&pv.map);
    let mut rows: Vec<Row> = Vec::new();
    for (g, rating, elo_before) in elo_games(ctx, ev, ratings) {
        let rs: Vec<Option<f64>> = g.moves.iter().map(|m| recall(m, &g.date)).collect();
        let present: Vec<f64> = rs.iter().flatten().map(|r| r.max(1e-3).ln()).collect();
        let mut f = IndexMap::new();
        f.insert("gap", (elo_before - rating) / 400.0);
        f.insert("rating", (rating - 1500.0) / 400.0);
        f.insert("recall", present.iter().sum::<f64>());
        f.insert("unseen", rs.iter().filter(|r| r.is_none()).count() as f64);
        f.insert("experience", (rows.len() as f64).ln_1p());
        f.insert("mass", walk_mass(&g.moves, &counts));
        f.insert("length", (g.moves.len().max(1) as f64).ln());
        rows.push(Row {
            features: f,
            recall_empty: present.is_empty(),
            y: g.score,
            date: g.date.clone(),
        });
    }
    rows
}

fn design(rows: &[Row], features: &[&str]) -> (Vec<Vec<f64>>, Vec<f64>) {
    let x = rows
        .iter()
        .map(|r| {
            let mut v = vec![1.0];
            v.extend(features.iter().map(|f| r.features[*f]));
            v
        })
        .collect();
    (x, rows.iter().map(|r| r.y).collect())
}

fn fold_edges(n: usize) -> Vec<usize> {
    (0..=SOLVE_FOLDS)
        .map(|i| (n as f64 * (i + 1) as f64 / (SOLVE_FOLDS + 1) as f64).round_ties_even() as usize)
        .collect()
}

/// Mean held-out log-likelihood over expanding-window folds.
fn cv_loglik(rows: &[Row], features: &[&str], lam: f64) -> f64 {
    let (x, y) = design(rows, features);
    let edges = fold_edges(y.len());
    let (mut lls, mut sizes) = (0.0, 0usize);
    for w in edges.windows(2) {
        let (lo, hi) = (w[0], w[1]);
        if hi <= lo {
            continue;
        }
        let coef = logistic(&x[..lo], &y[..lo], lam, 60, 1e-9);
        lls += mean_loglik(&x[lo..hi], &y[lo..hi], &coef) * (hi - lo) as f64;
        sizes += hi - lo;
    }
    if sizes == 0 {
        f64::NEG_INFINITY
    } else {
        lls / sizes as f64
    }
}

/// kg_curve.fit_solve: forward-select the features that earn their place on
/// held-out games, refit on everything, report the alternatives.
fn fit_solve(
    ctx: &Ctx,
    ev: &Evidence,
    pv: &PView,
    p: &Params,
    ratings: &HashMap<String, f64>,
) -> Value {
    let rows = solve_rows(ctx, ev, pv, p, ratings);
    if rows.len() < 100 {
        return json!({"games": rows.len(), "features": {}, "note": "too few games"});
    }
    let mut chosen: Vec<&str> = Vec::new();
    let mut best = SOLVE_LAMBDAS
        .iter()
        .map(|l| cv_loglik(&rows, &[], *l))
        .fold(f64::NEG_INFINITY, f64::max);
    let base_cv = best;
    let mut best_lam = 0.0;
    loop {
        // max over (cv, feature, lam) tuples, compared the way Python does
        let mut top: Option<(f64, &str, f64)> = None;
        for f in SOLVE_FEATURES {
            if chosen.contains(&f) {
                continue;
            }
            for lam in SOLVE_LAMBDAS {
                let mut with = chosen.clone();
                with.push(f);
                let cv = cv_loglik(&rows, &with, lam);
                let cand = (cv, f, lam);
                top = Some(match top {
                    None => cand,
                    Some(t) => {
                        let ord = cand
                            .0
                            .partial_cmp(&t.0)
                            .unwrap()
                            .then(cand.1.cmp(t.1))
                            .then(cand.2.partial_cmp(&t.2).unwrap());
                        if ord == std::cmp::Ordering::Greater {
                            cand
                        } else {
                            t
                        }
                    }
                });
            }
        }
        let Some((cv, feature, lam)) = top else { break };
        if cv <= best + 1e-4 {
            break;
        }
        chosen.push(feature);
        best = cv;
        best_lam = lam;
    }
    let (x, y) = design(&rows, &chosen);
    let w = logistic(&x, &y, best_lam, 60, 1e-9);
    let games = elo_games(ctx, ev, ratings);
    let (drift, drift_se) = elo_drift(&games);
    let pr: Vec<f64> = matvec(&x, &w).into_iter().map(sigmoid).collect();
    let wts: Vec<f64> = pr.iter().map(|q| q * (1.0 - q)).collect();
    let cov = inverse(&xtwx(&x, &wts, 0.0, true, 1e-6)).expect("covariance");
    let names: Vec<&str> = std::iter::once("intercept")
        .chain(chosen.iter().copied())
        .collect();
    let mut features = Map::new();
    let mut se = Map::new();
    for (i, n) in names.iter().enumerate() {
        features.insert(n.to_string(), json!(round_to(w[i], 4)));
        se.insert(n.to_string(), json!(round_to(cov[i][i].sqrt(), 4)));
    }
    json!({
        "games": rows.len(),
        "features": Value::Object(features),
        "se": Value::Object(se),
        "intercept_se": round_to(cov[0][0].sqrt(), 4),
        "elo": {
            "now": round_to(elo_now(ctx, ev), 1),
            "drift_per_day": round_to(drift, 5),
            "drift_se": round_to(drift_se, 5),
        },
        "lambda": best_lam,
        "cv_loglik": round_to(best, 4),
        "baseline_cv_loglik": round_to(base_cv, 4),
        "rejected": SOLVE_FEATURES.iter().filter(|f| !chosen.contains(f)).collect::<Vec<_>>(),
    })
}

/// A small xorshift for the bootstrap; not numpy's PCG64, so the intervals
/// differ from the Python report's.
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
}

fn percentile(sorted: &[f64], q: f64) -> f64 {
    let pos = q / 100.0 * (sorted.len() - 1) as f64;
    let lo = pos.floor() as usize;
    let hi = pos.ceil() as usize;
    sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo as f64)
}

/// kg_curve.solve_report: the cold-solve model against the alternatives on
/// the same expanding-window folds.
fn solve_report(ctx: &Ctx, ev: &Evidence, pv: &PView, p: &Params, ratings: &HashMap<String, f64>) {
    let rows = solve_rows(ctx, ev, pv, p, ratings);
    let games: Vec<_> = kg::model::scored_games(ctx, ev)
        .into_iter()
        .filter(|g| ratings.contains_key(&g.problem))
        .collect();
    let y: Vec<f64> = rows.iter().map(|r| r.y).collect();
    let n = y.len();
    let edges = fold_edges(n);
    let out_of_fold = |x: &[Vec<f64>], lam: f64| -> Vec<Option<f64>> {
        let mut pred = vec![None; n];
        for w in edges.windows(2) {
            let (lo, hi) = (w[0], w[1]);
            let coef = logistic(&x[..lo], &y[..lo], lam, 60, 1e-9);
            for (i, z) in matvec(&x[lo..hi], &coef).into_iter().enumerate() {
                pred[lo + i] = Some(sigmoid(z));
            }
        }
        pred
    };
    let fitted = fit_solve(ctx, ev, pv, p, ratings);
    let chosen: Vec<&str> = fitted["features"]
        .as_object()
        .map(|m| {
            m.keys()
                .filter(|k| *k != "intercept")
                .map(|k| SOLVE_FEATURES.iter().copied().find(|f| f == k).unwrap())
                .collect()
        })
        .unwrap_or_default();
    let lam = fitted["lambda"].as_f64().unwrap_or(0.0);
    let label: Vec<Vec<f64>> = games
        .iter()
        .map(|g| {
            vec![
                1.0,
                f64::from(g.difficulty == "Medium"),
                f64::from(g.difficulty == "Hard"),
            ]
        })
        .collect();
    let ones: Vec<Vec<f64>> = vec![vec![1.0]; n];
    let models: Vec<(String, Vec<Option<f64>>)> = vec![
        ("base rate".to_string(), out_of_fold(&ones, 0.0)),
        (
            "Easy/Medium/Hard label".to_string(),
            out_of_fold(&label, 0.0),
        ),
        (
            "rating alone".to_string(),
            out_of_fold(&design(&rows, &["rating"]).0, lam),
        ),
        (
            format!("fitted: {}", chosen.join(" + ")),
            out_of_fold(&design(&rows, &chosen).0, lam),
        ),
    ];
    let scored: Vec<usize> = (0..n).filter(|i| models[0].1[*i].is_some()).collect();
    println!(
        "{n} games, {} scored out of fold ({SOLVE_FOLDS} expanding-window blocks)",
        scored.len()
    );
    println!(
        "  {:34}{:>13}{:>9}{:>9}{:>9}",
        "model", "loglik/game", "Brier", "mean p", "actual"
    );
    let mut lls: Vec<Vec<f64>> = Vec::new();
    for (name, pred) in &models {
        let ps: Vec<f64> = scored
            .iter()
            .map(|i| pred[*i].unwrap().clamp(1e-9, 1.0 - 1e-9))
            .collect();
        let ts: Vec<f64> = scored.iter().map(|i| y[*i]).collect();
        let ll: Vec<f64> = ps
            .iter()
            .zip(&ts)
            .map(|(p, t)| t * p.ln() + (1.0 - t) * (1.0 - p).ln())
            .collect();
        let mean = |v: &[f64]| np_sum(v) / v.len() as f64;
        let brier: Vec<f64> = ps.iter().zip(&ts).map(|(p, t)| (p - t) * (p - t)).collect();
        println!(
            "  {name:34}{:13.4}{:9.4}{:9.3}{:9.3}",
            mean(&ll),
            mean(&brier),
            mean(&ps),
            mean(&ts)
        );
        lls.push(ll);
    }
    let mut rng = Rng(0x9e3779b97f4a7c15);
    for (other, idx) in [("base rate", 0usize), ("Easy/Medium/Hard label", 1)] {
        let d: Vec<f64> = lls[3].iter().zip(&lls[idx]).map(|(a, b)| a - b).collect();
        let mut boot: Vec<f64> = (0..4000)
            .map(|_| {
                let s: f64 = (0..d.len())
                    .map(|_| d[(rng.next() % d.len() as u64) as usize])
                    .sum();
                s / d.len() as f64
            })
            .collect();
        boot.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let better = boot.iter().filter(|b| **b > 0.0).count() as f64 / boot.len() as f64;
        println!(
            "  fitted - {other}: {:+.4}/game, 95% CI [{:+.4}, {:+.4}], P(better) {better:.3}",
            np_sum(&d) / d.len() as f64,
            percentile(&boot, 2.5),
            percentile(&boot, 97.5)
        );
    }
}

/// clist.write_ratings: graph/ratings.json, problem number -> rating.
fn write_ratings(ctx: &Ctx, ratings: &HashMap<String, f64>) {
    let mut keys: Vec<&String> = ratings.keys().collect();
    keys.sort_by_key(|k| k.parse::<i64>().unwrap_or(i64::MAX));
    let mut table = Map::new();
    for k in keys {
        table.insert(k.clone(), json!(round_to(ratings[k], 1)));
    }
    pyjson::save(
        &ctx.graph_dir().join("ratings.json"),
        &Value::Object(table),
        Some(1),
    )
    .expect("write graph/ratings.json");
}

fn pct(x: f64) -> String {
    format!("{:.0}%", x * 100.0)
}

fn mtime(p: &std::path::Path) -> Option<std::time::SystemTime> {
    std::fs::metadata(p).and_then(|m| m.modified()).ok()
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_curve [--if-stale] [--since YYYY-MM-DD] [--half-life DAYS] [--solve-report] [--solve-rows-json]");
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let flag = |name: &str| -> Option<String> {
        args.iter()
            .position(|a| a == name)
            .and_then(|i| args.get(i + 1).cloned())
    };
    let since_s: Option<String> =
        flag("--since").or_else(|| std::env::var("CURVE_SINCE").ok().filter(|s| !s.is_empty()));
    let half_life: f64 = flag("--half-life")
        .or_else(|| {
            std::env::var("CURVE_HALF_LIFE")
                .ok()
                .filter(|s| !s.is_empty())
        })
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.0);
    let if_stale = args.iter().any(|a| a == "--if-stale");
    let rows_json = args.iter().any(|a| a == "--solve-rows-json");
    let report = args.iter().any(|a| a == "--solve-report");
    // knobs["half_life"]: `args.half_life or 0`, the int 0 when off
    let knob_half = if half_life == 0.0 {
        json!(0)
    } else {
        json!(half_life)
    };
    let knob_since = since_s.clone().map(Value::String).unwrap_or(Value::Null);

    let curve_path = root.join("graph/curve.json");
    let evidence_path = root.join("graph/evidence.json");
    if if_stale && curve_path.exists() && mtime(&curve_path) >= mtime(&evidence_path) {
        // a knob change makes the file stale even with no new evidence
        let prev = pyjson::load(&curve_path)
            .and_then(|v| v.get("fit").cloned())
            .unwrap_or_else(|| json!({}));
        let prev_half = prev.get("half_life").cloned().unwrap_or(json!(0));
        let same_half = prev_half.as_f64() == knob_half.as_f64();
        if prev.get("since").cloned().unwrap_or(Value::Null) == knob_since && same_half {
            return;
        }
    }

    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());

    if rows_json {
        // the bridge for kg_progress_svg: the feature rows under the fitted curve
        let curve = ctx.curve.as_ref().expect("graph/curve.json");
        let p = Params {
            a: curve.a,
            b: curve.b,
            c: 0.0,
            d: 0.0,
            e: 0.0,
            conn_mean: 0.0,
            beta: curve.beta,
            slip: 0.0,
        };
        let ratings = solve_ratings(&ctx);
        let rows = solve_rows(&ctx, &ev, &pv, &p, &ratings);
        let mut items = Vec::new();
        for r in rows {
            let mut f = Map::new();
            for (k, v) in &r.features {
                if *k == "recall" && r.recall_empty {
                    f.insert(k.to_string(), json!(0));
                } else {
                    f.insert(k.to_string(), json!(*v));
                }
            }
            items.push(json!([Value::Object(f), r.y, r.date]));
        }
        println!("{}", dumps(&Value::Array(items), None));
        return;
    }

    let dated = extract_trials(&ctx, &ev, &pv);
    let since = since_s.as_deref().map(parse_date);
    let (trials, weights) = select_trials(
        &dated,
        since,
        if half_life > 0.0 {
            Some(half_life)
        } else {
            None
        },
    );
    if trials.is_empty() {
        eprintln!(
            "no trials on or after {}; curve.json left as is",
            since_s.unwrap_or_default()
        );
        std::process::exit(1);
    }
    let p = fit(&trials, weights.as_deref());
    let conn = node_conn(&pv, &ctx);
    let mass = fit_mass(&ctx, &ev, &pv);
    let ratings = solve_ratings(&ctx);
    if !ratings.is_empty() {
        write_ratings(&ctx, &ratings); // graph/ratings.json, read by kg_mock
    }
    let solve = fit_solve(&ctx, &ev, &pv, &p, &ratings);

    let ws: Vec<f64> = weights.clone().unwrap_or_else(|| vec![1.0; trials.len()]);
    let wsum: f64 = ws.iter().sum();
    let base_rate: f64 = ws
        .iter()
        .zip(&trials)
        .map(|(w, t)| w * t.success as f64)
        .sum::<f64>()
        / wsum;
    let ll_model = loglik(&trials, &p, weights.as_deref());
    let ll_base: f64 = ws
        .iter()
        .zip(&trials)
        .map(|(w, t)| {
            w * (if t.success == 1 {
                base_rate
            } else {
                1.0 - base_rate
            })
            .ln()
        })
        .sum::<f64>()
        / wsum;

    let mut conn_sorted: Vec<(&String, &f64)> = conn.iter().collect();
    conn_sorted.sort_by(|a, b| a.0.cmp(b.0));
    let mut conn_map = Map::new();
    for (n, v) in conn_sorted {
        conn_map.insert(n.clone(), json!(round_to(*v, 3)));
    }
    let curve = json!({
        "_comment": "Personal forgetting curve fitted by utils/kg/kg_curve. P(recall) = (1-slip)*(1 + gap/s)^(-beta), s = exp(a + b*log1p(cleans) - c*struggles - d*assist + e*(conn - conn_mean)); cleans counts distinct clean days, same-day reps are one rep. conn is the node's log2 carrier count, frozen below at fit time; consumers that ignore e are assuming average connectivity. \"solve\" is the cold-solve model fitted by fit_solve: logit P(solve cold, unaided, inside the clock) = the listed coefficients over (rating - 1500)/400, the walk's summed log recall, and its count of never-met moves; features not listed did not earn their place on held-out games. node_status() calls a node SOLID while the memory component (1 + gap/s)^(-beta) >= target_retention; delete this file to fall back to the flat 42-day window.",
        "model": "power-law-slip",
        "params": {
            "a": round_to(p.a, 4),
            "b": round_to(p.b, 4),
            "c": round_to(p.c, 4),
            "d": round_to(p.d, 4),
            "e": round_to(p.e, 4),
            "conn_mean": round_to(p.conn_mean, 4),
            "beta": round_to(p.beta, 4),
            "slip": round_to(p.slip, 4),
        },
        "conn": Value::Object(conn_map),
        "target_retention": TARGET_RETENTION,
        "mass": mass,
        "solve": solve,
        "fit": {
            "trials": trials.len(),
            "loglik": round_to(ll_model, 4),
            "baseline_loglik": round_to(ll_base, 4),
            "since": knob_since,
            "half_life": knob_half,
            "effective_trials": round_to(wsum, 1),
        },
    });
    pyjson::save(&curve_path, &curve, Some(2)).expect("write graph/curve.json");

    let console = Console::full_width();
    let say = |line: &str| {
        let markup = if line.starts_with("fitted") || line.starts_with("wrote") {
            format!("[bold]{line}[/bold]")
        } else if line.starts_with("  ") {
            format!("[dim]{line}[/dim]")
        } else {
            format!("[cyan]{line}[/cyan]")
        };
        console.print(&markup);
    };
    if since_s.is_some() || half_life > 0.0 {
        let mut parts = Vec::new();
        if let Some(s) = &since_s {
            parts.push(format!("era boundary {s}"));
        }
        if half_life > 0.0 {
            parts.push(format!(
                "recency half-life {}d (effective n {:.0})",
                py_g(half_life),
                wsum
            ));
        }
        say(&format!("knobs: {}", parts.join(", ")));
    }
    say(&format!(
        "fitted on {} trials: P = {:.2}·(1 + Δ/s)^(−{:.2}), s = exp({:.2} + {:.3}·log1p(cleans) − {:.3}·struggles − {:.3}·assist + {:.3}·conn)",
        trials.len(),
        1.0 - p.slip,
        p.beta,
        p.a,
        p.b,
        p.c,
        p.d,
        p.e
    ));
    say(&format!(
        "loglik/trial {ll_model:.4} vs always-{} baseline {ll_base:.4}",
        pct(base_rate)
    ));
    say(&format!(
        "{}-retention window by clean reps (no struggles, unaided):",
        pct(TARGET_RETENTION)
    ));
    let factor = TARGET_RETENTION.powf(-1.0 / p.beta) - 1.0;
    for k in [1, 2, 3, 5, 10, 20] {
        let s = p.stab(k, 0, 0.0, None);
        say(&format!(
            "  {k:2} reps: stability {s:5.0}d -> window ≈ {:5.0}d",
            s * factor
        ));
    }
    say("cost of assistance (5 clean reps, no struggles):");
    for (label, x) in [
        ("unaided", 0.0),
        ("one hint", 0.5),
        ("walkthrough", 1.0),
        ("learning", 2.0),
    ] {
        say(&format!(
            "  {label:<12}: window ≈ {:5.0}d",
            p.stab(5, 0, x, None) * factor
        ));
    }
    say("calibration (model mean vs observed unaided-recall rate):");
    for (lo, hi) in GAP_BUCKETS {
        let rows: Vec<&Trial> = trials
            .iter()
            .filter(|t| lo <= t.gap && t.gap <= hi)
            .collect();
        if rows.is_empty() {
            continue;
        }
        let obs = rows.iter().map(|t| t.success as f64).sum::<f64>() / rows.len() as f64;
        let model = rows
            .iter()
            .map(|t| p.pred(t.gap, t.cleans, t.struggles, t.assist, Some(t.conn)))
            .sum::<f64>()
            / rows.len() as f64;
        say(&format!(
            "  gap {lo:3}-{hi:3}d: model {:>4}  observed {:>4}  (n={})",
            pct(model),
            pct(obs),
            rows.len()
        ));
    }
    if let Some(feats) = solve
        .get("features")
        .and_then(Value::as_object)
        .filter(|m| !m.is_empty())
    {
        let terms: Vec<String> = feats
            .iter()
            .filter(|(f, _)| *f != "intercept")
            .map(|(f, c)| format!("{:+.3}·{f}", c.as_f64().unwrap_or(0.0)))
            .collect();
        say(&format!(
            "cold solve, fitted on {} timed games: logit P = {:.3} {}",
            solve["games"],
            feats["intercept"].as_f64().unwrap_or(0.0),
            terms.join(" ")
        ));
        let rejected: Vec<&str> = solve["rejected"]
            .as_array()
            .map(|a| a.iter().filter_map(Value::as_str).collect())
            .unwrap_or_default();
        say(&format!(
            "  held-out loglik/game {:.4} vs base rate {:.4}{}",
            solve["cv_loglik"].as_f64().unwrap_or(0.0),
            solve["baseline_cv_loglik"].as_f64().unwrap_or(0.0),
            if rejected.is_empty() {
                String::new()
            } else {
                format!("; earned no place: {}", rejected.join(", "))
            }
        ));
    }
    if report {
        solve_report(&ctx, &ev, &pv, &p, &ratings);
    }
    say(&format!("wrote {}", curve_path.display()));
    let _ = float_repr;
}

#[cfg(test)]
mod tests {
    use super::*;

    fn dated(gap: i64, success: i64, day: NaiveDate) -> Trial {
        Trial {
            gap,
            success,
            cleans: 1,
            struggles: 0,
            assist: 0.0,
            conn: 4.0,
            date: day,
        }
    }

    fn day(y: i32, m: u32, d: u32) -> NaiveDate {
        NaiveDate::from_ymd_opt(y, m, d).unwrap()
    }

    /// utils/tests/test_kg_curve.py, moved here with the fitter.
    #[test]
    fn no_knobs_returns_all_trials_unweighted() {
        let rows = vec![
            dated(30, 1, day(2025, 11, 1)),
            dated(30, 0, day(2026, 8, 20)),
        ];
        let (t, w) = select_trials(&rows, None, None);
        assert_eq!(t, rows);
        assert!(w.is_none());
    }

    #[test]
    fn era_boundary_drops_older_trials() {
        let rows = vec![
            dated(30, 1, day(2025, 11, 1)),
            dated(30, 0, day(2026, 8, 20)),
        ];
        let (t, _) = select_trials(&rows, Some(day(2026, 1, 1)), None);
        assert_eq!(t, vec![rows[1].clone()]);
        assert_eq!(
            select_trials(&rows[..1], Some(day(2026, 1, 1)), None),
            (vec![], None)
        );
    }

    #[test]
    fn half_life_discounts_by_age_from_newest() {
        let rows = vec![
            dated(30, 1, day(2026, 8, 1)),
            dated(30, 1, day(2026, 7, 2)),
            dated(30, 1, day(2026, 8, 31)),
        ];
        let (_, w) = select_trials(&rows, None, Some(30.0));
        assert_eq!(w.unwrap(), vec![0.5, 0.25, 1.0]);
    }

    #[test]
    fn recency_weighted_fit_follows_the_recent_era() {
        // one era says gap-30 recall holds, a later era says it fails
        let mut rows = vec![dated(30, 1, day(2025, 11, 1)); 40];
        rows.extend(vec![dated(30, 0, day(2026, 8, 20)); 40]);
        let pred_at_30 =
            |p: Params| (1.0 - p.slip) * (1.0 + 30.0 / (p.a + p.b * 2f64.ln()).exp()).powf(-p.beta);
        let (t, w) = select_trials(&rows, None, None);
        let plain = pred_at_30(fit(&t, w.as_deref()));
        let (t, w) = select_trials(&rows, None, Some(30.0));
        let weighted = pred_at_30(fit(&t, w.as_deref()));
        assert!(0.3 < plain && plain < 0.7, "{plain}");
        assert!(weighted < 0.25, "{weighted}");
        assert!(weighted < plain - 0.2);
    }
}
