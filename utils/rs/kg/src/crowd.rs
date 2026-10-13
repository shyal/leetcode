// The crowd's record of every problem: how many people have attempted it
// and how many liked and disliked it, from the question's own GraphQL
// query (no login). kg_crowd keeps data/crowd.json fresh (not checked in);
// the picker reads it in two places (ctx::disliked, ctx::crowd_key,
// pick.rs):
//
//   - "bad": the Wilson lower bound (95%) of dislikes / (likes + dislikes)
//     reaches BAD_AT. Such a problem is served after every other
//     candidate of its rule. The bound, not the share, so a problem with
//     a dozen votes cannot be "bad" on a handful of them.
//   - "obscure": in the bottom OBSCURE_QUANTILE of the file by
//     submissions. Served last the same way: almost nobody does it, so
//     almost nobody is asked it, whatever its voters think.
//   - the tiebreak: among candidates still tied on odds, gentleness and
//     freshness, the one more people have attempted comes first
//     (companies ask what everyone knows; half-decade buckets of
//     submissions, so 8M and 6M tie and go to the next key), then the one
//     with the smaller share of dislikes. Acceptance, the old friction
//     tiebreak, is behind both. A problem with no record sorts after one
//     with a record.
//
// CROWD_DOWNRANK=0 switches both off.
//
// Why the ratio and not the Discussion comments (kg_discuss): on 99
// problems judged by a model from their top comments (2026-10-13), the
// verdicts and the dislike share measured the same thing (median dislike
// share 44% under "bad", 6% under "good"), and where they differed the
// share was right. 56. Merge Intervals was "bad" on 1188 upvotes for "the
// list is not sorted, please clarify", a statement LeetCode rewrote years
// ago; 26060 voters since then give it 4% dislikes. The comments see the
// loudest moment in the past; the ratio sees the present crowd. The
// comment judge stays as the on-demand reader of why.

use std::cmp::Reverse;
use std::collections::HashMap;
use std::path::Path;

use serde_json::{json, Map, Value};

use crate::data::{env_str, read_json};

pub const FILE: &str = "data/crowd.json";
/// The lower bound of the dislike share at which a problem is "bad".
pub const BAD_AT: f64 = 0.5;
/// The Wilson interval's z: 95%.
pub const Z: f64 = 1.96;
/// A record older than this is synced again.
pub const STALE_DAYS: i64 = 7;

pub(crate) const UA: &str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36";
const STATS_QUERY: &str =
    "query q($slug: String!) { question(titleSlug: $slug) { likes dislikes stats } }";

/// What the crowd did with one problem.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Stats {
    pub submissions: i64,
    pub likes: i64,
    pub dislikes: i64,
}

impl Stats {
    pub fn votes(&self) -> i64 {
        self.likes + self.dislikes
    }

    /// Dislikes as a share of the votes, 0 when there are none.
    pub fn dislike_share(&self) -> f64 {
        if self.votes() <= 0 {
            0.0
        } else {
            self.dislikes as f64 / self.votes() as f64
        }
    }

    pub fn dislike_pct(&self) -> i64 {
        (100.0 * self.dislike_share()).round() as i64
    }

    /// The crowd dislikes it: the share's lower bound reaches BAD_AT.
    pub fn bad(&self) -> bool {
        wilson_lower(self.dislikes, self.votes()) >= BAD_AT
    }

    /// Popularity on a log scale: half-decades of submissions (50k -> 9,
    /// 114k -> 10, 8M -> 13, 41M -> 15), 0 when none.
    pub fn bucket(&self) -> i64 {
        if self.submissions <= 0 {
            0
        } else {
            (2.0 * (self.submissions as f64).log10()).floor() as i64
        }
    }
}

/// The Wilson score interval's lower bound on the share `k` of `n`.
pub fn wilson_lower(k: i64, n: i64) -> f64 {
    if n <= 0 {
        return 0.0;
    }
    let (k, n) = (k as f64, n as f64);
    let p = k / n;
    let z2 = Z * Z;
    let centre = p + z2 / (2.0 * n);
    let half = Z * (p * (1.0 - p) / n + z2 / (4.0 * n * n)).sqrt();
    ((centre - half) / (1.0 + z2 / n)).max(0.0)
}

/// The sort key the picker's carrier sorts use: most attempted first,
/// then fewest dislikes; a problem with no record after every problem
/// with one.
pub fn tiebreak(stats: Option<Stats>) -> (Reverse<Option<i64>>, i64) {
    match stats {
        Some(s) => (Reverse(Some(s.bucket())), s.dislike_pct()),
        None => (Reverse(None), 0),
    }
}

// ---- the transport ----------------------------------------------------

/// One request. Err(true, _) is a transport or status failure worth a
/// retry; Err(false, _) is an answer that carried `errors` (a premium
/// problem's topic does not exist), which asking again will not change.
fn graphql_once(query: &str, variables: &Value) -> Result<Value, (bool, String)> {
    let agent: ureq::Agent = ureq::Agent::config_builder()
        .timeout_global(Some(std::time::Duration::from_secs(60)))
        .build()
        .into();
    let mut resp = agent
        .post("https://leetcode.com/graphql/")
        .header("Content-Type", "application/json")
        .header("User-Agent", UA)
        .header("Referer", "https://leetcode.com/problems/")
        .send_json(json!({"query": query, "variables": variables}))
        .map_err(|e| (true, format!("graphql: {e}")))?;
    let v: Value = resp
        .body_mut()
        .read_json()
        .map_err(|e| (true, format!("graphql: {e}")))?;
    if let Some(errs) = v.get("errors").filter(|e| !e.is_null()) {
        let msg = errs[0]["message"].as_str().unwrap_or("").to_string();
        let msg = if msg.is_empty() {
            errs.to_string()
        } else {
            msg
        };
        return Err((false, format!("graphql: {msg}")));
    }
    Ok(v["data"].clone())
}

/// The waits before each retry of a failed request. LeetCode answers a
/// burst of requests with 404s, 503s and 504s for a minute or so and then
/// recovers (seven in a row on 2026-10-13); the job has an hour.
const RETRY_WAITS: [u64; 3] = [10, 30, 90];

/// One GraphQL query to leetcode.com, no login, retried on a transport
/// or status failure.
pub(crate) fn graphql(query: &str, variables: Value) -> Result<Value, String> {
    let mut last = String::new();
    for wait in RETRY_WAITS.iter().map(Some).chain([None]) {
        match graphql_once(query, &variables) {
            Ok(v) => return Ok(v),
            Err((false, e)) => return Err(e),
            Err((true, e)) => last = e,
        }
        match wait {
            Some(s) => std::thread::sleep(std::time::Duration::from_secs(*s)),
            None => break,
        }
    }
    Err(format!("{last} (after {} tries)", RETRY_WAITS.len() + 1))
}

/// The problem's counts. `stats` comes back as a JSON string inside the
/// JSON; totalSubmissionRaw is the attempt count.
pub fn fetch_stats(slug: &str) -> Result<Stats, String> {
    let q = graphql(STATS_QUERY, json!({"slug": slug}))?;
    let q = &q["question"];
    if q.is_null() {
        return Err(format!("{slug}: no such question"));
    }
    let stats: Value = q["stats"]
        .as_str()
        .and_then(|s| serde_json::from_str(s).ok())
        .unwrap_or(Value::Null);
    Ok(Stats {
        submissions: stats["totalSubmissionRaw"].as_i64().unwrap_or(0),
        likes: q["likes"].as_i64().unwrap_or(0),
        dislikes: q["dislikes"].as_i64().unwrap_or(0),
    })
}

// ---- the file -----------------------------------------------------------

/// data/crowd.json: problem number -> {slug, submissions, likes,
/// dislikes, synced}.
pub fn load(root: &Path) -> Map<String, Value> {
    read_json(&root.join(FILE))
        .and_then(|v| v.as_object().cloned())
        .unwrap_or_default()
}

pub fn save(root: &Path, crowd: &Map<String, Value>) -> std::io::Result<()> {
    crate::pyjson::save(&root.join(FILE), &Value::Object(crowd.clone()), Some(1))
}

pub fn entry(slug: &str, s: Stats, synced: &str) -> Value {
    json!({
        "slug": slug,
        "submissions": s.submissions,
        "likes": s.likes,
        "dislikes": s.dislikes,
        "synced": synced,
    })
}

pub fn stats_of(e: &Value) -> Option<Stats> {
    Some(Stats {
        submissions: e["submissions"].as_i64()?,
        likes: e["likes"].as_i64()?,
        dislikes: e["dislikes"].as_i64()?,
    })
}

/// CROWD_DOWNRANK=0 switches the picker's reads off; unset or anything
/// else leaves them on.
pub fn downrank_on() -> bool {
    env_str("CROWD_DOWNRANK").trim() != "0"
}

/// The share of the free problems, by submissions from the bottom, that
/// count as obscure: almost nobody does them, so almost nobody is asked
/// them. 1017. Convert to Base -2 had 67k attempts against a median of
/// 356k (2026-10-13) and 65% likes, so no dislike bound reaches it. The
/// cut is a quantile of the file, never a count, and moves as the file
/// does.
pub const OBSCURE_QUANTILE: f64 = 0.25;

/// Every problem's record, the empty table when the reads are off or the
/// file is missing.
#[derive(Debug, Default, Clone)]
pub struct Crowd {
    stats: HashMap<String, Stats>,
    /// Submissions below this are obscure: the OBSCURE_QUANTILE point of
    /// the records; 0 with no records, so nothing is obscure.
    obscure_below: i64,
}

/// The value at quantile `q` of the counts, 0 when there are none.
pub fn quantile(counts: &mut [i64], q: f64) -> i64 {
    if counts.is_empty() {
        return 0;
    }
    counts.sort_unstable();
    let i = ((counts.len() as f64 * q) as usize).min(counts.len() - 1);
    counts[i]
}

impl Crowd {
    pub fn read(root: &Path) -> Crowd {
        if !downrank_on() {
            return Crowd::default();
        }
        let stats: HashMap<String, Stats> = load(root)
            .iter()
            .filter_map(|(p, e)| stats_of(e).map(|s| (p.clone(), s)))
            .collect();
        let mut counts: Vec<i64> = stats.values().map(|s| s.submissions).collect();
        Crowd {
            obscure_below: quantile(&mut counts, OBSCURE_QUANTILE),
            stats,
        }
    }

    pub fn get(&self, pnum: &str) -> Option<Stats> {
        self.stats.get(pnum).copied()
    }

    /// The crowd dislikes it (Stats::bad).
    pub fn bad(&self, pnum: &str) -> bool {
        self.get(pnum).is_some_and(|s| s.bad())
    }

    /// Almost nobody does it: in the bottom OBSCURE_QUANTILE of the
    /// records by submissions.
    pub fn obscure(&self, pnum: &str) -> bool {
        self.get(pnum)
            .is_some_and(|s| s.submissions < self.obscure_below)
    }

    /// Served after every other candidate of its rule: disliked or
    /// obscure.
    pub fn downranked(&self, pnum: &str) -> bool {
        self.bad(pnum) || self.obscure(pnum)
    }
}

/// A count for a table cell: 41.0M, 318k, 67.
pub fn compact(n: i64) -> String {
    if n >= 1_000_000 {
        format!("{:.1}M", n as f64 / 1e6)
    } else if n >= 1_000 {
        format!("{}k", n / 1_000)
    } else {
        n.to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn s(submissions: i64, likes: i64, dislikes: i64) -> Stats {
        Stats {
            submissions,
            likes,
            dislikes,
        }
    }

    #[test]
    fn wilson_lower_narrows_with_the_sample() {
        assert_eq!(wilson_lower(0, 0), 0.0);
        assert!((wilson_lower(3, 5) - 0.231).abs() < 0.01);
        assert!((wilson_lower(600, 1000) - 0.569).abs() < 0.01);
        assert!(wilson_lower(5, 5) < 1.0);
    }

    #[test]
    fn bad_needs_a_crowd_behind_the_share() {
        // 481. Magical String: 394 likes, 1438 dislikes
        assert!(s(114_090, 394, 1438).bad());
        // 56. Merge Intervals: 25137 likes, 923 dislikes
        assert!(!s(8_308_689, 25137, 923).bad());
        // 3 of 5 is a share of 60 and a lower bound of 23
        assert!(!s(100, 2, 3).bad());
        assert_eq!(s(0, 0, 0).dislike_pct(), 0);
    }

    #[test]
    fn buckets_are_half_decades() {
        assert_eq!(s(50_000, 0, 0).bucket(), 9);
        assert_eq!(s(114_090, 0, 0).bucket(), 10);
        assert_eq!(s(8_308_689, 0, 0).bucket(), 13);
        assert_eq!(s(41_004_521, 0, 0).bucket(), 15);
        assert_eq!(s(0, 0, 0).bucket(), 0);
    }

    #[test]
    fn tiebreak_puts_popular_then_liked_then_unknown() {
        let popular = tiebreak(Some(s(8_000_000, 25000, 900)));
        let small = tiebreak(Some(s(50_000, 52, 52)));
        let small_liked = tiebreak(Some(s(60_000, 100, 2)));
        assert!(popular < small);
        assert!(small_liked < small);
        assert!(small < tiebreak(None));
    }

    #[test]
    fn crowd_reads_the_file_unless_switched_off() {
        let dir = std::env::temp_dir().join(format!("kg-crowd-{}", std::process::id()));
        std::fs::create_dir_all(dir.join("data")).unwrap();
        let mut m = Map::new();
        m.insert("1".into(), entry("x", s(100, 10, 90), "2026-10-13"));
        m.insert("2".into(), entry("y", s(100, 90, 10), "2026-10-13"));
        save(&dir, &m).unwrap();
        crate::data::test_env("CROWD_DOWNRANK", "");
        let c = Crowd::read(&dir);
        assert!(c.bad("1"));
        assert!(!c.bad("2"));
        assert!(!c.bad("3"));
        crate::data::test_env("CROWD_DOWNRANK", "0");
        assert!(!Crowd::read(&dir).bad("1"));
        crate::data::test_env("CROWD_DOWNRANK", "");
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn obscure_is_the_bottom_quarter_by_submissions() {
        let dir = std::env::temp_dir().join(format!("kg-crowd-q-{}", std::process::id()));
        std::fs::create_dir_all(dir.join("data")).unwrap();
        let mut m = Map::new();
        for (p, subs) in [
            ("1", 10_000),
            ("2", 200_000),
            ("3", 300_000),
            ("4", 400_000),
        ] {
            m.insert(p.into(), entry("x", s(subs, 900, 100), "2026-10-13"));
        }
        save(&dir, &m).unwrap();
        crate::data::test_env("CROWD_DOWNRANK", "");
        let c = Crowd::read(&dir);
        assert!(c.obscure("1"));
        assert!(!c.obscure("2"));
        assert!(!c.obscure("9"));
        assert!(c.downranked("1") && !c.downranked("2"));
        let _ = std::fs::remove_dir_all(&dir);
        assert_eq!(quantile(&mut [], 0.25), 0);
        assert_eq!(quantile(&mut [5, 1, 3], 0.25), 1);
    }

    #[test]
    fn compact_counts() {
        assert_eq!(compact(41_004_521), "41.0M");
        assert_eq!(compact(318_566), "318k");
        assert_eq!(compact(67), "67");
    }
}
