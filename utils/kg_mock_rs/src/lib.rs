// kg_mock library: the shared cold-mock model — CPython-exact PyRandom,
// node_status / current_recall (kept in lockstep with utils/kg_lib.py), and
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
        let mut r = PyRandom { mt: [0; 624], mti: 624 };
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
    pub assist: String,
}

pub struct Curve {
    pub a: f64,
    pub b: f64,
    pub c: f64,
    pub d: f64,
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
        "spoiled" => 2.0,
        _ => 0.0,
    }
}

pub fn parse_date(s: &str) -> NaiveDate {
    NaiveDate::parse_from_str(s, "%Y-%m-%d").expect("bad date in evidence")
}

pub fn node_status(node: &str, evidence: &[EvRec], today: NaiveDate, cv: &Curve) -> (u8, Option<NaiveDate>) {
    let mut entries: Vec<(&str, &str, &str)> = Vec::new();
    for rec in evidence {
        if let Some(v) = rec.moves.get(node) {
            if !v.is_empty() {
                entries.push((rec.date.as_str(), v.as_str(), rec.assist.as_str()));
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
        .filter(|(_, v, a)| *v == "clean" && *a != "spoiled")
        .map(|(d, _, _)| *d)
        .collect();
    if (last_verdict == "struggled" || last_verdict == "avoided")
        && !clean_dates.last().map_or(false, |c| *c >= last_date)
    {
        return (FRAGILE, Some(parse_date(last_date)));
    }
    if clean_dates.is_empty() {
        return (FRAGILE, Some(parse_date(last_date)));
    }
    let cleans = clean_dates.len() as f64;
    let struggles = entries.iter().filter(|(_, v, _)| *v == "struggled").count() as f64;
    let mut assisted = 0.0;
    for (_, _, a) in &entries {
        assisted += assist_weight(a);
    }
    let stability = (cv.a + cv.b * cleans - cv.c * struggles - cv.d * assisted)
        .exp()
        .max(7.0)
        .min(3650.0);
    let clean_last = parse_date(clean_dates.last().unwrap());
    let gap = (today - clean_last).num_days() as f64;
    if (1.0 + gap / stability).powf(-cv.beta) >= cv.target {
        (SOLID, Some(clean_last))
    } else {
        (STALE, Some(clean_last))
    }
}

pub fn current_recall(node_ids: &[String], evidence: &[EvRec], cv: &Curve, today: NaiveDate) -> Vec<f64> {
    node_ids
        .iter()
        .map(|nid| {
            let (status, last) = node_status(nid, evidence, today, cv);
            let cleans = evidence
                .iter()
                .filter(|r| r.moves.get(nid.as_str()).map(String::as_str) == Some("clean"))
                .count() as f64;
            if status == MISSING || last.is_none() {
                return 0.25;
            }
            let s = (cv.a + cv.b * cleans).exp().max(7.0).min(3650.0);
            let rec = (1.0 + (today - last.unwrap()).num_days() as f64 / s).powf(-cv.beta);
            if status == FRAGILE {
                rec * 0.5
            } else {
                rec
            }
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

pub const WALK_LEN: [(u32, u32); 3] = [(1, 2), (2, 4), (4, 6)];
pub const OFF_GRAPH0: [f64; 3] = [0.02, 0.10, 0.45];
pub const REC_POWER: [f64; 3] = [0.5, 1.0, 1.6];
pub const SCENARIOS: [(&str, f64); 3] = [("cautious", 0.75), ("central", 0.85), ("optimistic", 0.95)];

// The simulation loop itself: n_mc mock interviews on a random 2E+2M+2H set,
// each problem's walk multiplying move recalls; on_sim sees every simulated
// mock's per-difficulty solved counts plus, per problem of the set, the
// weakest move in its walk (index into mv_recall; usize::MAX when the
// weakest link was an off-graph move at the derive rate) and whether the
// problem failed. pass_rates and outcome_hist are thin tallies over this —
// the RNG stream is identical for identical inputs.
pub fn run_mocks(
    mv_recall: &[Option<f64>],
    weights: &[f64],
    off: &[f64; 3],
    r_base: f64,
    practice: (i64, i64, i64),
    rng: &mut PyRandom,
    n_mc: usize,
    mut on_sim: impl FnMut(&[i32; 3], &[(usize, bool); 6]),
) {
    let (mediums, mocks, hards) = practice;
    let grow = 1.0 - (-(mediums as f64) / 120.0).exp();
    let time_f = [
        0.88 + 0.07 * grow,
        0.87 + 0.07 * grow,
        0.40 + 0.42 * (1.0 - (-(hards as f64) / 15.0).exp()),
    ];
    let derive = 0.25 + 0.20 * (1.0 - (-((mocks + hards) as f64) / 30.0).exp());
    let rec = r_base + (0.98 - r_base) * (1.0 - (-(mocks as f64) / 8.0).exp());
    let base_p = [
        time_f[0] * rec.powf(REC_POWER[0]),
        time_f[1] * rec.powf(REC_POWER[1]),
        time_f[2] * rec.powf(REC_POWER[2]),
    ];
    let mv_val: Vec<f64> = mv_recall.iter().map(|o| o.unwrap_or(derive)).collect();
    let mut cum = Vec::with_capacity(weights.len());
    let mut acc = 0.0;
    for w in weights {
        acc += w;
        cum.push(acc);
    }
    let total = cum[cum.len() - 1] + 0.0;
    let hi_idx = cum.len() - 1;

    for _ in 0..n_mc {
        let mut solved = [0i32; 3];
        let mut probs = [(usize::MAX, false); 6];
        for (pi, &dif) in [0usize, 0, 1, 1, 2, 2].iter().enumerate() {
            let mut p = base_p[dif];
            if rng.random() < off[dif] {
                p *= derive;
            }
            let k = rng.randint(WALK_LEN[dif].0, WALK_LEN[dif].1);
            let (mut min_v, mut min_i) = (f64::INFINITY, usize::MAX);
            for _ in 0..k {
                let x = rng.random() * total;
                let (mut lo, mut hi) = (0usize, hi_idx);
                while lo < hi {
                    let mid = (lo + hi) / 2;
                    if x < cum[mid] {
                        hi = mid;
                    } else {
                        lo = mid + 1;
                    }
                }
                if mv_val[lo] < min_v {
                    min_v = mv_val[lo];
                    min_i = if mv_recall[lo].is_some() { lo } else { usize::MAX };
                }
                p *= mv_val[lo];
            }
            let ok = rng.random() < p;
            solved[dif] += ok as i32;
            probs[pi] = (min_i, !ok);
        }
        on_sim(&solved, &probs);
    }
}

pub fn pass_rates(
    mv_recall: &[Option<f64>],
    weights: &[f64],
    off: &[f64; 3],
    r_base: f64,
    practice: (i64, i64, i64),
    rng: &mut PyRandom,
    n_mc: usize,
) -> (f64, f64, f64, f64) {
    let (mut full, mut onsite, mut screen, mut h_solved) = (0i64, 0i64, 0i64, 0i64);
    run_mocks(mv_recall, weights, off, r_base, practice, rng, n_mc, |solved, _| {
        full += (solved[0] == 2 && solved[1] == 2 && solved[2] == 2) as i64;
        onsite += (solved[0] == 2 && solved[1] == 2 && solved[2] >= 1) as i64;
        screen += (solved[1] == 2) as i64;
        h_solved += solved[2] as i64;
    });
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
    weights: &[f64],
    off: &[f64; 3],
    r_base: f64,
    practice: (i64, i64, i64),
    rng: &mut PyRandom,
    n_mc: usize,
) -> ([f64; 7], [f64; 7]) {
    let (mut hist, mut onsite_hist) = ([0i64; 7], [0i64; 7]);
    run_mocks(mv_recall, weights, off, r_base, practice, rng, n_mc, |solved, _| {
        let t = (solved[0] + solved[1] + solved[2]) as usize;
        hist[t] += 1;
        onsite_hist[t] += (solved[0] == 2 && solved[1] == 2 && solved[2] >= 1) as i64;
    });
    let norm = |a: [i64; 7]| a.map(|v| v as f64 / n_mc as f64);
    (norm(hist), norm(onsite_hist))
}
