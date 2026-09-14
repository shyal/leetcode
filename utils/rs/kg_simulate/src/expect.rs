// The pass model of kg_lib.pass_rates in closed form. A set draws each
// problem uniformly from its difficulty pool and solves it with the fitted
// cold-solve model - logit p = intercept + k_rating*(rating-1500)/400
// + k_recall*(summed log recall of the walk) + k_unseen*(its never-met
// moves), best walk winning - draws independent, so P(both Easies) is the
// pool mean of p squared, and P(onsite) = E^2 * M^2 * (1 - (1 - H)^2).
// Walks are flattened into index arrays once; a day's rates are two
// segmented reductions per pool, the pool mean summed as numpy sums it
// (kg::linalg::np_sum).

use std::collections::HashMap;

use indexmap::IndexMap;
use kg::ctx::Ctx;
use kg::data::{Problems, Walk};
use kg::linalg::np_sum;
use kg::model::solve_ratings;

/// One difficulty's pool: every walk's move indices end to end, where each
/// walk and each problem starts, and the rating behind each walk.
struct Pool {
    idx: Vec<usize>,
    walk_starts: Vec<usize>,
    prob_starts: Vec<usize>,
    n: usize,
    rating: Vec<f64>,
}

pub struct PassExpectation {
    index: HashMap<String, usize>,
    unseen_slot: usize,
    coef: HashMap<String, f64>,
    pools: IndexMap<String, Pool>,
}

pub type Pools = IndexMap<String, Vec<Vec<Vec<String>>>>;
pub type Ratings = IndexMap<String, Vec<f64>>;

/// The moves of a walk, the missing-move names folded in as off-taxonomy
/// moves (kg_mock_rs Bank::build).
fn walk_of(moves: &[String], missing: &[String]) -> Vec<String> {
    let mut w: Vec<String> = moves.to_vec();
    for m in missing {
        let name = m.trim().to_lowercase().replace(' ', "-");
        if !name.is_empty() && !name.starts_with("brute-force") {
            w.push(name);
        }
    }
    w
}

fn dif_of(ctx: &Ctx, num: &str, difficulty: Option<&str>) -> Option<&'static str> {
    let d = match difficulty {
        Some(d) if !d.is_empty() => d.to_string(),
        _ => ctx.meta_difficulty(num),
    };
    match d.as_str() {
        "Easy" => Some("E"),
        "Medium" => Some("M"),
        "Hard" => Some("H"),
        _ => None,
    }
}

/// kg_simulate.build_pools: ({"E"/"M"/"H": [problem, ...]}, the same shape
/// of contest ratings), each problem a list of walks: evidenced walks plus
/// drafted ones. A problem no contest rated takes the median rating of its
/// difficulty, the fallback kg_readme elo uses.
pub fn build_pools(ctx: &Ctx, problems: &Problems, predicted: &Problems) -> (Pools, Ratings) {
    let rated = solve_ratings(ctx);
    let mut raw: IndexMap<String, (&'static str, Vec<Vec<String>>)> = IndexMap::new();
    for (num, p) in problems {
        let d = dif_of(ctx, num, p.difficulty.as_deref());
        let w = walk_of(&p.moves, &[]);
        if let (Some(d), false) = (d, w.is_empty()) {
            raw.entry(num.clone()).or_insert((d, Vec::new())).1.push(w);
        }
    }
    for (num, p) in predicted {
        let Some(d) = dif_of(ctx, num, p.difficulty.as_deref()) else {
            continue;
        };
        for Walk {
            moves,
            missing_names,
            ..
        } in &p.walks
        {
            let w = walk_of(moves, missing_names);
            if !w.is_empty() {
                raw.entry(num.clone()).or_insert((d, Vec::new())).1.push(w);
            }
        }
    }
    let mut pools: Pools = IndexMap::new();
    let mut ratings: Ratings = IndexMap::new();
    let mut fallback: HashMap<&str, f64> = HashMap::new();
    for d in ["E", "M", "H"] {
        pools.insert(d.to_string(), Vec::new());
        ratings.insert(d.to_string(), Vec::new());
        let mut seen: Vec<f64> = raw
            .iter()
            .filter(|(n, (dd, _))| *dd == d && rated.contains_key(*n))
            .map(|(n, _)| rated[n])
            .collect();
        seen.sort_by(|a, b| a.partial_cmp(b).unwrap());
        fallback.insert(
            d,
            if seen.is_empty() {
                1500.0
            } else {
                seen[seen.len() / 2]
            },
        );
    }
    for (num, (d, walks)) in raw {
        pools[d].push(walks);
        ratings[d].push(rated.get(&num).copied().unwrap_or(fallback[d]));
    }
    (pools, ratings)
}

impl PassExpectation {
    pub fn new(
        pools: &Pools,
        ratings: &Ratings,
        node_order: &[String],
        coef: HashMap<String, f64>,
    ) -> Self {
        let index: HashMap<String, usize> = node_order
            .iter()
            .enumerate()
            .map(|(i, n)| (n.clone(), i))
            .collect();
        let unseen_slot = node_order.len();
        let mut out = IndexMap::new();
        for (dif, probs) in pools {
            let mut pool = Pool {
                idx: Vec::new(),
                walk_starts: Vec::new(),
                prob_starts: Vec::new(),
                n: probs.len(),
                rating: Vec::new(),
            };
            let mut pos = 0;
            for (pi, walks) in probs.iter().enumerate() {
                pool.prob_starts.push(pool.walk_starts.len());
                for w in walks {
                    pool.walk_starts.push(pos);
                    pool.rating.push(ratings[dif][pi]);
                    for m in w {
                        pool.idx.push(index.get(m).copied().unwrap_or(unseen_slot));
                    }
                    pos += w.len();
                }
            }
            out.insert(dif.clone(), pool);
        }
        PassExpectation {
            index,
            unseen_slot,
            coef,
            pools: out,
        }
    }

    /// The rates a perfect graph would produce: every move recalled, none
    /// never-met. Nothing the simulation can do beats this, so a target
    /// above it is unreachable however long the run goes on.
    pub fn ceiling(&self, shift: f64) -> (f64, f64, f64, f64) {
        let recall: HashMap<String, f64> = self.index.keys().map(|n| (n.clone(), 1.0)).collect();
        self.rates_(&recall, shift, true)
    }

    /// (full, onsite, screen, single-hard) as pass_rates returns.
    pub fn rates(&self, recall: &HashMap<String, f64>, shift: f64) -> (f64, f64, f64, f64) {
        self.rates_(recall, shift, false)
    }

    fn rates_(
        &self,
        recall: &HashMap<String, f64>,
        shift: f64,
        perfect: bool,
    ) -> (f64, f64, f64, f64) {
        let c = |k: &str| self.coef.get(k).copied().unwrap_or(0.0);
        let (k_rec, k_uns) = (c("recall"), c("unseen"));
        // per move: its contribution to a walk's linear predictor. A move he
        // has not met contributes the unseen coefficient instead of a recall.
        let mut term = vec![0.0f64; self.unseen_slot + 1];
        for (n, &i) in &self.index {
            term[i] = match recall.get(n) {
                None => k_uns,
                Some(r) => k_rec * r.max(1e-3).ln(),
            };
        }
        term[self.unseen_slot] = if perfect { 0.0 } else { k_uns };
        let mut p: HashMap<&str, f64> = HashMap::new();
        for (dif, pool) in &self.pools {
            if pool.n == 0 {
                p.insert(dif, 0.0);
                continue;
            }
            // np.add.reduceat over the walks: a plain left-to-right sum per
            // segment
            let nw = pool.walk_starts.len();
            let mut z = vec![0.0f64; nw];
            for (wi, &ws) in pool.walk_starts.iter().enumerate() {
                let end = if wi + 1 < nw {
                    pool.walk_starts[wi + 1]
                } else {
                    pool.idx.len()
                };
                let mut s = term[pool.idx[ws]];
                for &m in &pool.idx[ws + 1..end] {
                    s += term[m];
                }
                z[wi] =
                    c("intercept") + shift + c("rating") * (pool.rating[wi] - 1500.0) / 400.0 + s;
            }
            let mut best = Vec::with_capacity(pool.n);
            for (pi, &ps) in pool.prob_starts.iter().enumerate() {
                let end = if pi + 1 < pool.n {
                    pool.prob_starts[pi + 1]
                } else {
                    nw
                };
                let mut b = z[ps];
                for &v in &z[ps + 1..end] {
                    b = b.max(v);
                }
                best.push(1.0 / (1.0 + (-b).exp()));
            }
            p.insert(dif, np_sum(&best) / pool.n as f64);
        }
        let (e, m, h) = (p["E"], p["M"], p["H"]);
        let (e2, m2) = (e * e, m * m);
        let h1 = 1.0 - (1.0 - h) * (1.0 - h);
        (e2 * m2 * h * h, e2 * m2 * h1, m2, h)
    }
}
