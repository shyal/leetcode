// The fitted models the pick panel prices with: the contest ratings
// (utils/kg/clist.py's combined table), his Elo over the scored games, the
// cold-solve odds (curve.json "solve"), and the pacing forecast from the
// mined solve times (kg_lib.solve_forecast / drill_forecast).

use std::collections::HashMap;
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
        "Medium" => Some(25),
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

pub fn solve_logit(coef: &HashMap<String, f64>, rating: f64, ln_recall: f64, unseen: i64) -> f64 {
    let g = |k: &str| coef.get(k).copied().unwrap_or(0.0);
    g("intercept")
        + g("rating") * (rating - 1500.0) / 400.0
        + g("recall") * ln_recall
        + g("unseen") * unseen as f64
}

pub fn walk_terms(walk: &[String], recall: &HashMap<String, f64>) -> (f64, i64) {
    let (mut ln_recall, mut unseen) = (0.0, 0);
    for mv in walk {
        match recall.get(mv) {
            None => unseen += 1,
            Some(r) => ln_recall += r.max(1e-3).ln(),
        }
    }
    (ln_recall, unseen)
}

/// kg_lib.problem_solve_p: the cold-solve odds on one problem, or None.
pub fn problem_solve_p(
    pnum: &str,
    pv: &PView,
    recall: &HashMap<String, f64>,
    coef: Option<&HashMap<String, f64>>,
    ratings: &HashMap<String, f64>,
) -> Option<f64> {
    let coef = coef?;
    let rating = *ratings.get(pnum)?;
    let walk = &pv.get(pnum)?.moves;
    if walk.is_empty() {
        return None;
    }
    let (ln_recall, unseen) = walk_terms(walk, recall);
    Some(1.0 / (1.0 + (-solve_logit(coef, rating, ln_recall, unseen)).exp()))
}

/// kg_lib.target_pass_rate: TARGET_PASS_RATE in (0, 1), else 0.5.
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
/// Every rating is an integer or a decimal with one digit, so the exact
/// sum fits fixed point at 2^-40.
fn exact_mean(xs: &[f64]) -> f64 {
    const SHIFT: f64 = 1099511627776.0; // 2^40
    let total: i128 = xs.iter().map(|x| (x * SHIFT).round() as i128).sum();
    (total as f64 / SHIFT) / xs.len() as f64
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
    for i in order {
        let rec = ev.rec(i);
        let fname = ev.fname(i);
        let pnum = rec.problem.clone().unwrap_or_default();
        let diff = ctx.problem_difficulty(&pnum, &problems);
        if !is_numeric_id(&pnum) || budget_min(&diff).is_none() {
            continue;
        }
        let level = rec.assist_any();
        let score = if fname.contains("FAILED") || level == "walkthrough" || level == "learning" {
            0.0
        } else {
            let Some(s) = secs.get(fname) else { continue };
            let tier = if rec.followup.as_deref() == Some("solved") {
                next_tier(&diff).to_string()
            } else {
                diff.clone()
            };
            if *s > budget_min(&tier).unwrap() * 60 {
                0.0
            } else if level == "hint" {
                0.5
            } else {
                1.0
            }
        };
        out.push(Game {
            date: rec.date.clone(),
            problem: pnum,
            difficulty: diff,
            score,
        });
    }
    out
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

fn median(v: &[f64]) -> f64 {
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
