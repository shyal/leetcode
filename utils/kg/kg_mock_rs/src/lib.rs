// kg_mock library: the shared cold-mock model — CPython-exact PyRandom,
// node_status / current_recall (kept in lockstep with utils/kg/kg_lib.py —
// utils/tests/test_golden.py diffs the two over the real graph/ data), and
// the pass_rates Monte Carlo. Used by the kg_mock binary (`make mock`) and by
// kg_movie_rs for the README's animated P(pass) history chart — the same
// math kg_lib.py runs for that chart's Python era; change them together.

use std::collections::HashMap;

use chrono::NaiveDate;

// ---------------------------------------------------------------- PyRandom --
// CPython's random.Random: MT19937 seeded via init_by_array, with random(),
// getrandbits() and randint() reproduced exactly.

pub struct PyRandom {
    mt: [u32; 624],
    mti: usize,
}

impl PyRandom {
    pub fn new(seed: u32) -> Self {
        let mut r = PyRandom {
            mt: [0; 624],
            mti: 624,
        };
        r.init_by_array(&[seed]);
        r
    }

    pub fn init_genrand(&mut self, s: u32) {
        self.mt[0] = s;
        for i in 1..624usize {
            self.mt[i] = 1812433253u32
                .wrapping_mul(self.mt[i - 1] ^ (self.mt[i - 1] >> 30))
                .wrapping_add(i as u32);
        }
        self.mti = 624;
    }

    pub fn init_by_array(&mut self, key: &[u32]) {
        self.init_genrand(19650218);
        let (mut i, mut j) = (1usize, 0usize);
        for _ in 0..std::cmp::max(624, key.len()) {
            self.mt[i] = (self.mt[i]
                ^ (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)).wrapping_mul(1664525))
            .wrapping_add(key[j])
            .wrapping_add(j as u32);
            i += 1;
            j += 1;
            if i >= 624 {
                self.mt[0] = self.mt[623];
                i = 1;
            }
            if j >= key.len() {
                j = 0;
            }
        }
        for _ in 0..623 {
            self.mt[i] = (self.mt[i]
                ^ (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)).wrapping_mul(1566083941))
            .wrapping_sub(i as u32);
            i += 1;
            if i >= 624 {
                self.mt[0] = self.mt[623];
                i = 1;
            }
        }
        self.mt[0] = 0x80000000;
        self.mti = 624;
    }

    pub fn genrand(&mut self) -> u32 {
        const M: usize = 397;
        const MATRIX_A: u32 = 0x9908b0df;
        const UPPER: u32 = 0x80000000;
        const LOWER: u32 = 0x7fffffff;
        if self.mti >= 624 {
            let mt = &mut self.mt;
            for kk in 0..624 - M {
                let y = (mt[kk] & UPPER) | (mt[kk + 1] & LOWER);
                mt[kk] = mt[kk + M] ^ (y >> 1) ^ if y & 1 != 0 { MATRIX_A } else { 0 };
            }
            for kk in 624 - M..623 {
                let y = (mt[kk] & UPPER) | (mt[kk + 1] & LOWER);
                mt[kk] = mt[kk + M - 624] ^ (y >> 1) ^ if y & 1 != 0 { MATRIX_A } else { 0 };
            }
            let y = (mt[623] & UPPER) | (mt[0] & LOWER);
            mt[623] = mt[M - 1] ^ (y >> 1) ^ if y & 1 != 0 { MATRIX_A } else { 0 };
            self.mti = 0;
        }
        let mut y = self.mt[self.mti];
        self.mti += 1;
        y ^= y >> 11;
        y ^= (y << 7) & 0x9d2c5680;
        y ^= (y << 15) & 0xefc60000;
        y ^= y >> 18;
        y
    }

    pub fn random(&mut self) -> f64 {
        let a = (self.genrand() >> 5) as f64;
        let b = (self.genrand() >> 6) as f64;
        (a * 67108864.0 + b) * (1.0 / 9007199254740992.0)
    }

    pub fn getrandbits(&mut self, k: u32) -> u32 {
        self.genrand() >> (32 - k)
    }

    pub fn randbelow(&mut self, n: u32) -> u32 {
        let k = 32 - n.leading_zeros();
        let mut r = self.getrandbits(k);
        while r >= n {
            r = self.getrandbits(k);
        }
        r
    }

    pub fn randint(&mut self, a: u32, b: u32) -> u32 {
        a + self.randbelow(b - a + 1)
    }
}

// ------------------------------------------------------------- data model --

pub struct EvRec {
    pub fname: String,
    pub date: String,
    pub moves: HashMap<String, String>,
    /// per-move assist level, "none" when absent (kg_lib.assist_of(rec, node))
    pub assist: HashMap<String, String>,
}

impl EvRec {
    pub fn assist_for(&self, node: &str) -> &str {
        self.assist.get(node).map(String::as_str).unwrap_or("none")
    }
}

/// Mirror of kg_lib.drill_key: the drill a d_ solved file is a rep of, its
/// lowercase basename with the `make solved` timestamp (_YYYY_MM_DDT...)
/// stripped, or the last _token when there is none. None for a problem solve.
pub fn drill_key(fname: &str) -> Option<String> {
    let base = fname.rsplit('/').next().unwrap_or(fname).to_lowercase();
    let stem = base.strip_suffix(".py").unwrap_or(&base);
    if !stem.starts_with("d_") {
        return None;
    }
    let b = stem.as_bytes();
    for (i, &c) in b.iter().enumerate() {
        // "_YYYY_MM_DDt": 4 digits, '_', 2 digits, '_', 2 digits, 't'
        if c == b'_' && i + 12 <= b.len() {
            let t = &b[i + 1..i + 12];
            let digits = |r: std::ops::Range<usize>| t[r].iter().all(u8::is_ascii_digit);
            if digits(0..4)
                && t[4] == b'_'
                && digits(5..7)
                && t[7] == b'_'
                && digits(8..10)
                && t[10] == b't'
            {
                return Some(stem[..i].to_string());
            }
        }
    }
    Some(stem.rsplit_once('_').map_or(stem, |(a, _)| a).to_string())
}

/// The indices of each drill's first rep (earliest date, then filename):
/// first exposure to the drill, scored as unaided at the node level
/// (kg_lib.ev_index, 2026-09-01). `fname_date` yields (fname, date) per rec.
pub fn first_drill_reps<'a, I>(recs: I) -> Vec<usize>
where
    I: IntoIterator<Item = (&'a str, &'a str)>,
{
    let mut firsts: HashMap<String, (String, String, usize)> = HashMap::new();
    for (i, (fname, date)) in recs.into_iter().enumerate() {
        let Some(key) = drill_key(fname) else {
            continue;
        };
        let base = fname.rsplit('/').next().unwrap_or(fname).to_lowercase();
        let better = match firsts.get(&key) {
            Some((d, b, _)) => (date, base.as_str()) < (d.as_str(), b.as_str()),
            None => true,
        };
        if better {
            firsts.insert(key, (date.to_string(), base, i));
        }
    }
    firsts.into_values().map(|(_, _, i)| i).collect()
}

/// Mirror of kg_lib.assist_of's two shapes: a bare string taints every move
/// in the walk, a {move: level} dict names the moves the help touched.
pub fn assist_map(rec: &serde_json::Value) -> HashMap<String, String> {
    let valid = |a: &str| ["hint", "walkthrough", "learning"].contains(&a);
    let mut out = HashMap::new();
    match rec.get("assist") {
        Some(serde_json::Value::String(a)) if valid(a) => {
            if let Some(m) = rec.get("moves").and_then(serde_json::Value::as_object) {
                for k in m.keys() {
                    out.insert(k.clone(), a.clone());
                }
            }
        }
        Some(serde_json::Value::Object(d)) => {
            for (k, v) in d {
                if let Some(a) = v.as_str().filter(|a| valid(a)) {
                    out.insert(k.clone(), a.to_string());
                }
            }
        }
        _ => {}
    }
    out
}

pub struct Curve {
    pub a: f64,
    pub b: f64,
    pub c: f64,
    pub d: f64,
    // connectivity covariate: stability picks up e*(conn - conn_mean), where
    // conn is the node's log2 carrier count frozen into curve.json at fit
    // time. A node absent from the map gets conn_mean (zero effect), so old
    // curve files and simulated nodes behave as before.
    pub e: f64,
    pub conn_mean: f64,
    pub conn: HashMap<String, f64>,
    pub beta: f64,
    pub target: f64,
}

pub const SOLID: u8 = 0;
pub const STALE: u8 = 1;
pub const FRAGILE: u8 = 2;
pub const MISSING: u8 = 3;

pub fn assist_weight(a: &str) -> f64 {
    match a {
        "hint" => 0.5,
        "walkthrough" => 1.0,
        "learning" => 2.0,
        _ => 0.0,
    }
}

pub fn parse_date(s: &str) -> NaiveDate {
    NaiveDate::parse_from_str(s, "%Y-%m-%d").expect("bad date in evidence")
}

pub fn node_status(
    node: &str,
    evidence: &[EvRec],
    today: NaiveDate,
    cv: &Curve,
) -> (u8, Option<NaiveDate>) {
    let mut entries: Vec<(&str, &str, &str)> = Vec::new();
    for rec in evidence {
        if let Some(v) = rec.moves.get(node) {
            if !v.is_empty() {
                entries.push((rec.date.as_str(), v.as_str(), rec.assist_for(node)));
            }
        }
    }
    if entries.is_empty() {
        return (MISSING, None);
    }
    entries.sort();
    let (last_date, last_verdict, _) = *entries.last().unwrap();
    let clean_dates: Vec<&str> = entries
        .iter()
        .filter(|(_, v, a)| *v == "clean" && *a != "learning")
        .map(|(d, _, _)| *d)
        .collect();
    if (last_verdict == "struggled" || last_verdict == "avoided")
        && clean_dates.last().is_none_or(|c| *c < last_date)
    {
        return (FRAGILE, Some(parse_date(last_date)));
    }
    if clean_dates.is_empty() {
        return (FRAGILE, Some(parse_date(last_date)));
    }
    // distinct days, not entries: same-day reps are one rep (kept in
    // lockstep with kg_lib.node_eval)
    let cleans = {
        let mut uniq = clean_dates.clone();
        uniq.dedup();
        uniq.len() as f64
    };
    let struggles = entries.iter().filter(|(_, v, _)| *v == "struggled").count() as f64;
    let mut assisted = 0.0;
    for (_, _, a) in &entries {
        assisted += assist_weight(a);
    }
    let cn = cv.conn.get(node).copied().unwrap_or(cv.conn_mean);
    let stability = (cv.a + cv.b * (1.0 + cleans).ln() - cv.c * struggles - cv.d * assisted
        + cv.e * (cn - cv.conn_mean))
        .exp()
        .clamp(7.0, 3650.0);
    let clean_last = parse_date(clean_dates.last().unwrap());
    let gap = (today - clean_last).num_days() as f64;
    if (1.0 + gap / stability).powf(-cv.beta) >= cv.target {
        (SOLID, Some(clean_last))
    } else {
        (STALE, Some(clean_last))
    }
}

pub fn current_recall(
    node_ids: &[String],
    evidence: &[EvRec],
    cv: &Curve,
    today: NaiveDate,
) -> Vec<Option<f64>> {
    node_ids
        .iter()
        .map(|nid| {
            let (status, last) = node_status(nid, evidence, today, cv);
            // distinct clean days, as in kg_lib.node_curve_recall
            let cleans = {
                let mut days: Vec<&str> = evidence
                    .iter()
                    .filter(|r| r.moves.get(nid.as_str()).map(String::as_str) == Some("clean"))
                    .map(|r| r.date.as_str())
                    .collect();
                days.sort();
                days.dedup();
                days.len() as f64
            };
            // a move he has never had clean has no recall at all: the
            // cold-solve model charges it the fitted unseen term instead of
            // an assumed number
            if status == MISSING || last.is_none() || cleans == 0.0 {
                return None;
            }
            let s = (cv.a + cv.b * (1.0 + cleans).ln()).exp().clamp(7.0, 3650.0);
            Some((1.0 + (today - last.unwrap()).num_days() as f64 / s).powf(-cv.beta))
        })
        .collect()
}

// First match of r"\d{4}_\d{2}_\d{2}T[\d_]+" in s, or "".
pub fn ts_match(s: &str) -> String {
    let b = s.as_bytes();
    let n = b.len();
    for i in 0..n {
        if i + 11 < n
            && b[i..i + 4].iter().all(u8::is_ascii_digit)
            && b[i + 4] == b'_'
            && b[i + 5].is_ascii_digit()
            && b[i + 6].is_ascii_digit()
            && b[i + 7] == b'_'
            && b[i + 8].is_ascii_digit()
            && b[i + 9].is_ascii_digit()
            && b[i + 10] == b'T'
            && (b[i + 11].is_ascii_digit() || b[i + 11] == b'_')
        {
            let mut j = i + 11;
            while j < n && (b[j].is_ascii_digit() || b[j] == b'_') {
                j += 1;
            }
            return s[i..j].to_string();
        }
    }
    String::new()
}

// The cold-solve model fitted by utils/kg/kg_curve (curve.json "solve"):
// logit P(solve a problem cold, unaided, inside the clock) = intercept
// + rating*(contest rating - 1500)/400 + recall*(the walk's summed log
// recall) + unseen*(its count of never-met moves). Nothing here is
// per-difficulty: the label only says which pool a problem is drawn from.
#[derive(Clone, Copy, Default)]
pub struct SolveModel {
    pub intercept: f64,
    pub rating: f64,
    pub recall: f64,
    pub unseen: f64,
    pub intercept_se: f64,
    /// the skill channel: measured Elo drift in points per day, and its
    /// standard error. `gap` (elo - rating) is offered to the fit as a
    /// feature and loses to plain rating, because his skill has not
    /// measurably moved; the drift is what a PROJECTION advances by, so the
    /// forecast can rise without anyone assuming that it will.
    pub drift: f64,
    pub drift_se: f64,
}

impl SolveModel {
    pub fn load(v: &serde_json::Value) -> Option<SolveModel> {
        let f = v.get("solve")?.get("features")?;
        Some(SolveModel {
            intercept: f.get("intercept").and_then(serde_json::Value::as_f64)?,
            rating: f
                .get("rating")
                .and_then(serde_json::Value::as_f64)
                .unwrap_or(0.0),
            recall: f
                .get("recall")
                .and_then(serde_json::Value::as_f64)
                .unwrap_or(0.0),
            unseen: f
                .get("unseen")
                .and_then(serde_json::Value::as_f64)
                .unwrap_or(0.0),
            intercept_se: v["solve"]["intercept_se"].as_f64().unwrap_or(0.0),
            drift: v["solve"]["elo"]["drift_per_day"].as_f64().unwrap_or(0.0),
            drift_se: v["solve"]["elo"]["drift_se"].as_f64().unwrap_or(0.0),
        })
    }

    /// The logit shift `days` of projected practice buys: a skill gain of D
    /// Elo points is the same as every problem being D points easier, so the
    /// shift is -k_rating * D / 400. `z` walks the drift's standard error.
    /// Zero drift, zero shift.
    pub fn skill_shift(&self, days: i64, z: f64) -> f64 {
        -self.rating * (self.drift + z * self.drift_se) * days as f64 / 400.0
    }

    /// The scenario band at `days` into a projection: the fitted intercept's
    /// own standard error (today's uncertainty) plus the drift's, compounded
    /// over the horizon. Tight today, widening with the projection - and the
    /// central line moves only by the drift his games actually show.
    pub fn scenarios(&self, days: i64) -> [(&'static str, f64); 3] {
        let z = 1.96 * self.intercept_se;
        [
            ("cautious", -z + self.skill_shift(days, -1.96)),
            ("central", self.skill_shift(days, 0.0)),
            ("optimistic", z + self.skill_shift(days, 1.96)),
        ]
    }

    /// One walk's linear predictor.
    pub fn logit(&self, rating: f64, ln_recall: f64, unseen: f64) -> f64 {
        self.intercept
            + self.rating * (rating - 1500.0) / 400.0
            + self.recall * ln_recall
            + self.unseen * unseen
    }
}

pub fn sigmoid(z: f64) -> f64 {
    1.0 / (1.0 + (-z).exp())
}

// ---------------------------------------------------------------- the bank --
// Real problems replace the old fabricated walks (guessed WALK_LEN /
// OFF_GRAPH0 / i.i.d. move-frequency draws): every problem with a walk —
// evidenced or LLM-drafted, both in problems.json — sits in a
// per-difficulty pool, its walks stored as indices into one move-name
// universe. Universe layout: [0, n_known) are nodes.json ids (recall comes
// from evidence); [n_known, ..) are "extras" — moves the taxonomy lacks
// (missing: suggestions, ranked by how many walks want them, plus stray
// evidenced move names) — recall None until the forward sim learns them.
// brute-force* suggestions are dropped: they mean "no technique needed".
// Per-node refresh price from graph/solvecost.json (utils/kg/kg_solvecost):
// ln minutes = a + g_reps*ln(1+reps) + g_conn*(conn-conn_mean) + kind + eff,
// clamped to [min, max]. Exposure (reps) is what the forward sim grows, so a
// node gets cheaper to maintain the more the sim has met it, at the rate the
// timed solves actually show. None -> the flat 10-minute refresh.
pub struct SolveCost {
    pub a: f64,
    pub g_reps: f64,
    pub g_conn: f64,
    pub g_len: f64,
    pub conn_mean: f64,
    pub min: f64,
    pub max: f64,
    /// per difficulty, the fitted kind intercept (Easy is the baseline, 0)
    pub kind: [f64; 3],
    pub nodes: Vec<Option<(f64, f64, f64)>>, // node index -> (eff, conn, kind intercept)
}

impl SolveCost {
    pub fn load(v: &serde_json::Value, node_ids: &[String]) -> Option<SolveCost> {
        let p = v.get("params")?;
        let f = |k: &str| p.get(k).and_then(serde_json::Value::as_f64);
        let nodes_v = v.get("nodes")?.as_object()?;
        let nodes = node_ids
            .iter()
            .map(|nid| {
                let n = nodes_v.get(nid)?;
                let kind = n.get("kind")?.as_str()?;
                Some((
                    n.get("eff")?.as_f64()?,
                    n.get("conn")?.as_f64()?,
                    f(&format!("kind_{kind}"))?,
                ))
            })
            .collect();
        Some(SolveCost {
            a: f("a")?,
            g_reps: f("g_reps")?,
            g_conn: f("g_conn")?,
            g_len: f("g_len").unwrap_or(0.0),
            kind: [
                f("kind_Easy").unwrap_or(0.0),
                f("kind_Medium").unwrap_or(0.0),
                f("kind_Hard").unwrap_or(0.0),
            ],
            conn_mean: f("conn_mean")?,
            min: f("min_cost").unwrap_or(1.0),
            max: f("max_cost").unwrap_or(40.0),
            nodes,
        })
    }

    /// Minutes one fresh solve of a difficulty-`dif` problem costs, from the
    /// same fitted model: no prior reps, average connectivity, a walk of
    /// `walk_len` moves. Replaces the flat 23/40/90-minute budgets.
    pub fn solve_minutes(&self, dif: usize, walk_len: f64) -> f64 {
        (self.a + self.g_len * walk_len.max(1.0).ln() + self.kind[dif])
            .exp()
            .max(self.min)
            .min(self.max)
    }

    pub fn minutes(&self, n: usize, reps: i64) -> f64 {
        match self.nodes.get(n).copied().flatten() {
            Some((eff, conn, kind)) => (self.a
                + self.g_reps * (1.0 + reps.max(0) as f64).ln()
                + self.g_conn * (conn - self.conn_mean)
                + kind
                + eff)
                .exp()
                .max(self.min)
                .min(self.max),
            None => 10.0,
        }
    }
}

pub struct Bank {
    pub cost: Option<SolveCost>,
    pub move_names: Vec<String>,
    pub n_known: usize,
    // pools[dif][prob] = walks; a walk = move indices (known + extras mixed)
    pub pools: [Vec<Vec<Vec<usize>>>; 3],
    // ratings[dif][prob] = the problem's contest rating (graph/ratings.json;
    // a problem no contest rated takes its difficulty's median)
    pub ratings: [Vec<f64>; 3],
    // flat walk table for the forward sim's learning bookkeeping
    pub walk_prob: Vec<(usize, usize)>, // walk gid -> (dif, prob index)
    pub walk_extras: Vec<Vec<usize>>,   // walk gid -> extra ids (0-based past n_known)
    pub extra_walks: Vec<Vec<usize>>,   // extra id -> walk gids that want it
}

impl Bank {
    /// Minutes one refresh of node `n` costs after `reps` clean reps.
    pub fn refresh_cost(&self, n: usize, reps: i64) -> f64 {
        self.cost.as_ref().map_or(10.0, |c| c.minutes(n, reps))
    }

    pub fn n_extras(&self) -> usize {
        self.move_names.len() - self.n_known
    }
}

// The simulation loop itself: n_mc mock interviews on a random 2E+2M+2H set,
// each problem drawn uniformly from its difficulty pool and scored by its
// BEST real walk under the fitted cold-solve model — the problem's contest
// rating, the walk's summed log recall, and its count of never-met moves.
// on_sim sees every simulated mock's per-difficulty solved counts plus, per
// problem of the set, the weakest move in the walk that was used (index into
// mv_recall; usize::MAX when the weakest link was a move he has never met)
// and whether the problem failed. pass_rates and outcome_hist are thin
// tallies over this — the RNG stream is identical for identical inputs.
#[allow(clippy::too_many_arguments)]
pub fn run_mocks(
    mv_recall: &[Option<f64>],
    pools: &[Vec<Vec<Vec<usize>>>; 3],
    ratings: &[Vec<f64>; 3],
    coef: &SolveModel,
    shift: f64,
    rng: &mut PyRandom,
    n_mc: usize,
    mut on_sim: impl FnMut(&[i32; 3], &[(usize, bool); 6]),
) {
    // per move, its contribution to a walk's linear predictor: the recall
    // term for a move he has met, the unseen term for one he has not
    let term: Vec<f64> = mv_recall
        .iter()
        .map(|o| match o {
            Some(r) => coef.recall * r.max(1e-3).ln(),
            None => coef.unseen,
        })
        .collect();

    for _ in 0..n_mc {
        let mut solved = [0i32; 3];
        let mut probs = [(usize::MAX, false); 6];
        for (pi, &dif) in [0usize, 0, 1, 1, 2, 2].iter().enumerate() {
            let pool = &pools[dif];
            let prob_i = rng.randbelow(pool.len() as u32) as usize;
            let prob = &pool[prob_i];
            // best walk: highest linear predictor; its weakest move is blame
            let (mut best_z, mut best_min_i) = (f64::NEG_INFINITY, usize::MAX);
            for walk in prob.iter() {
                let mut z = 0.0;
                let (mut min_v, mut min_i) = (f64::INFINITY, usize::MAX);
                for &mv in walk {
                    let v = term[mv];
                    if v < min_v {
                        min_v = v;
                        min_i = if mv_recall[mv].is_some() {
                            mv
                        } else {
                            usize::MAX
                        };
                    }
                    z += v;
                }
                if z > best_z {
                    best_z = z;
                    best_min_i = min_i;
                }
            }
            // logit(rating, 0, 0) is the intercept plus the rating term;
            // best_z already carries the walk's recall and unseen terms
            let p = sigmoid(coef.logit(ratings[dif][prob_i], 0.0, 0.0) + best_z + shift);
            let ok = rng.random() < p;
            solved[dif] += ok as i32;
            probs[pi] = (best_min_i, !ok);
        }
        on_sim(&solved, &probs);
    }
}

impl Bank {
    // problems.json (one table: an evidenced entry has "moves" and a
    // difficulty, a drafted one "walks" + missing: suggestions),
    // problems_metadata.json (difficulty for problems only the drafts know).
    pub fn build(
        problems: &serde_json::Value,
        metadata: &serde_json::Value,
        node_ids: &[String],
        ratings: &serde_json::Value,
    ) -> Bank {
        use serde_json::Value;
        let norm = |s: &str| s.trim().to_lowercase().replace(' ', "-");
        let dif_of = |num: &str, obj: &serde_json::Map<String, Value>| -> Option<usize> {
            let d = obj
                .get("difficulty")
                .and_then(Value::as_str)
                .or_else(|| metadata.get(num).and_then(|m| m["difficulty"].as_str()))?;
            match d {
                "Easy" => Some(0),
                "Medium" => Some(1),
                "Hard" => Some(2),
                _ => None,
            }
        };
        let probs = problems["problems"]
            .as_object()
            .expect("problems.json: problems{}");

        // universe: node ids first, then extras ranked by walk mentions
        let mut index: HashMap<String, usize> = HashMap::new();
        let mut move_names: Vec<String> = node_ids.to_vec();
        for (i, n) in node_ids.iter().enumerate() {
            index.insert(n.clone(), i);
        }
        let n_known = move_names.len();
        let mut mention: HashMap<String, f64> = HashMap::new();
        let walk_of = |v: &Value, mention: &mut HashMap<String, f64>| -> Vec<String> {
            let mut w: Vec<String> = v["moves"]
                .as_array()
                .map(|a| {
                    a.iter()
                        .filter_map(Value::as_str)
                        .map(String::from)
                        .collect()
                })
                .unwrap_or_default();
            for m in v
                .get("missing")
                .and_then(Value::as_array)
                .unwrap_or(&vec![])
            {
                let name = norm(m.as_str().unwrap_or(""));
                if name.is_empty() || name.starts_with("brute-force") {
                    continue;
                }
                w.push(name);
            }
            for m in &w {
                if !index.contains_key(m.as_str()) {
                    *mention.entry(m.clone()).or_insert(0.0) += 1.0;
                }
            }
            w
        };
        // collect raw walks per problem first, so extras can be ranked before
        // indices are assigned
        let mut raw: HashMap<String, (usize, Vec<Vec<String>>)> = HashMap::new();
        for (num, v) in probs {
            let Some(obj) = v.as_object() else { continue };
            let Some(dif) = dif_of(num, obj) else {
                continue;
            };
            let w = walk_of(v, &mut mention); // the evidenced walk, if any
            if !w.is_empty() {
                raw.entry(num.clone()).or_insert((dif, vec![])).1.push(w);
            }
            for wv in v["walks"].as_array().unwrap_or(&vec![]) {
                let w = walk_of(wv, &mut mention);
                if !w.is_empty() {
                    raw.entry(num.clone()).or_insert((dif, vec![])).1.push(w);
                }
            }
        }
        let mut extras: Vec<(String, f64)> = mention.into_iter().collect();
        extras.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap().then(a.0.cmp(&b.0)));
        for (name, _) in &extras {
            index.insert(name.clone(), move_names.len());
            move_names.push(name.clone());
        }

        let mut bank = Bank {
            cost: None,
            move_names,
            n_known,
            pools: [vec![], vec![], vec![]],
            ratings: [vec![], vec![], vec![]],
            walk_prob: vec![],
            walk_extras: vec![],
            extra_walks: vec![Vec::new(); extras.len()],
        };
        let mut nums: Vec<&String> = raw.keys().collect();
        nums.sort(); // deterministic pool order -> deterministic RNG stream
        let rating_of = |num: &str| ratings.get(num).and_then(Value::as_f64);
        let median_rating: [f64; 3] = [0, 1, 2].map(|d| {
            let mut seen: Vec<f64> = nums
                .iter()
                .filter(|n| raw[**n].0 == d)
                .filter_map(|n| rating_of(n))
                .collect();
            seen.sort_by(|a, b| a.partial_cmp(b).unwrap());
            if seen.is_empty() {
                1500.0
            } else {
                seen[seen.len() / 2]
            }
        });
        for num in nums {
            let (dif, walks) = &raw[num];
            let pi = bank.pools[*dif].len();
            let mut iw: Vec<Vec<usize>> = vec![];
            for w in walks {
                let gid = bank.walk_prob.len();
                let ids: Vec<usize> = w.iter().map(|m| index[m.as_str()]).collect();
                let ex: Vec<usize> = ids
                    .iter()
                    .filter(|&&i| i >= n_known)
                    .map(|&i| i - n_known)
                    .collect();
                for &e in &ex {
                    bank.extra_walks[e].push(gid);
                }
                bank.walk_prob.push((*dif, pi));
                bank.walk_extras.push(ex);
                iw.push(ids);
            }
            bank.pools[*dif].push(iw);
            bank.ratings[*dif].push(rating_of(num).unwrap_or(median_rating[*dif]));
        }
        bank
    }
}

pub fn pass_rates(
    mv_recall: &[Option<f64>],
    pools: &[Vec<Vec<Vec<usize>>>; 3],
    ratings: &[Vec<f64>; 3],
    coef: &SolveModel,
    shift: f64,
    rng: &mut PyRandom,
    n_mc: usize,
) -> (f64, f64, f64, f64) {
    let (mut full, mut onsite, mut screen, mut h_solved) = (0i64, 0i64, 0i64, 0i64);
    run_mocks(
        mv_recall,
        pools,
        ratings,
        coef,
        shift,
        rng,
        n_mc,
        |solved, _| {
            full += (solved[0] == 2 && solved[1] == 2 && solved[2] == 2) as i64;
            onsite += (solved[0] == 2 && solved[1] == 2 && solved[2] >= 1) as i64;
            screen += (solved[1] == 2) as i64;
            h_solved += solved[2] as i64;
        },
    );
    (
        full as f64 / n_mc as f64,
        onsite as f64 / n_mc as f64,
        screen as f64 / n_mc as f64,
        h_solved as f64 / (2 * n_mc) as f64,
    )
}

// Per-mock outcome distribution behind pass_rates' aggregates: share of the
// n_mc simulated mocks that solved 0..=6 problems, plus the share of each bin
// that clears the onsite bar (2E + 2M + >=1 hard — only 5s and 6s can).
pub fn outcome_hist(
    mv_recall: &[Option<f64>],
    pools: &[Vec<Vec<Vec<usize>>>; 3],
    ratings: &[Vec<f64>; 3],
    coef: &SolveModel,
    shift: f64,
    rng: &mut PyRandom,
    n_mc: usize,
) -> ([f64; 7], [f64; 7]) {
    let (mut hist, mut onsite_hist) = ([0i64; 7], [0i64; 7]);
    run_mocks(
        mv_recall,
        pools,
        ratings,
        coef,
        shift,
        rng,
        n_mc,
        |solved, _| {
            let t = (solved[0] + solved[1] + solved[2]) as usize;
            hist[t] += 1;
            onsite_hist[t] += (solved[0] == 2 && solved[1] == 2 && solved[2] >= 1) as i64;
        },
    );
    let norm = |a: [i64; 7]| a.map(|v| v as f64 / n_mc as f64);
    (norm(hist), norm(onsite_hist))
}
