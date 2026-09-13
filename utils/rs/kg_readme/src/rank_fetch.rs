// A snapshot of where LeetCode contest ratings sit in the rated
// population, written to data/leetcode_rank_table.json for rank.rs. Run
// by hand (make rank-table); the badge reads the file.
//
// Two populations. "all" is every rated user: LeetCode's global ranking
// lists them by rating, 25 to a page, so the number of users at or above
// a rating is found by binary search over the pages. The table holds that
// count for every 25 points from 1200 to 3000. "regulars" are users with
// at least REGULAR_MIN attended contests: PAGES pages are drawn at random
// and each user's count is fetched in batches of 25; the ratings of the
// regulars found are kept, sorted. Users answering null are dropped;
// "answered" records how many did not.
//
// Ported from utils/readme/kg_rank_fetch (Python) on 2026-09-13.

use std::collections::{HashMap, HashSet};

use kg::ctx::Ctx;
use kg::mock::PyRandom;
use serde_json::{json, Value};

const URL: &str = "https://leetcode.com/graphql";
const REGULAR_MIN: i64 = 20;
const PAGES: usize = 120;
const SEED: u32 = 20260912;

fn gql(query: &str) -> Value {
    for _ in 0..4 {
        let r = ureq::post(URL)
            .header("content-type", "application/json")
            .header("referer", "https://leetcode.com/contest/globalranking/")
            .header("user-agent", "Mozilla/5.0")
            .send_json(json!({"query": query}));
        if let Ok(mut resp) = r {
            if let Ok(v) = resp.body_mut().read_json::<Value>() {
                if let Some(d) = v.get("data") {
                    return d.clone();
                }
            }
        }
        std::thread::sleep(std::time::Duration::from_secs(3));
    }
    eprintln!("leetcode did not answer");
    std::process::exit(1);
}

type Node = (f64, i64, String);

fn page(p: usize) -> (i64, i64, Vec<Node>) {
    let d = gql(&format!(
        "query {{ globalRanking(page: {p}) {{ totalUsers userPerPage rankingNodes {{ currentRating currentGlobalRanking user {{ username }} }} }} }}"
    ));
    let d = &d["globalRanking"];
    let nodes = d["rankingNodes"]
        .as_array()
        .unwrap()
        .iter()
        .map(|n| {
            (
                kg::data::value_str(&n["currentRating"]).parse().unwrap(),
                n["currentGlobalRanking"].as_i64().unwrap(),
                n["user"]["username"].as_str().unwrap().to_string(),
            )
        })
        .collect();
    (
        d["totalUsers"].as_i64().unwrap(),
        d["userPerPage"].as_i64().unwrap(),
        nodes,
    )
}

struct Ranking {
    total: i64,
    pages: usize,
    cache: HashMap<usize, Vec<Node>>,
}

impl Ranking {
    fn new() -> Ranking {
        let (total, per, _) = page(1);
        Ranking {
            total,
            pages: ((total + per - 1) / per) as usize,
            cache: HashMap::new(),
        }
    }

    fn nodes(&mut self, p: usize) -> &Vec<Node> {
        self.cache.entry(p).or_insert_with(|| page(p).2)
    }

    /// Number of users with rating >= r.
    fn at_or_above(&mut self, r: f64) -> i64 {
        let (mut lo, mut hi) = (1, self.pages);
        while lo < hi {
            let mid = (lo + hi) / 2;
            if self.nodes(mid).last().unwrap().0 >= r {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        let nodes = self.nodes(lo);
        for (rt, rank, _) in nodes {
            if *rt < r {
                return rank - 1;
            }
        }
        nodes.last().unwrap().1
    }
}

/// {username: attended contests} for the users that answer.
fn contest_counts(usernames: &[String]) -> HashMap<String, i64> {
    let q: Vec<String> = usernames
        .iter()
        .enumerate()
        .map(|(i, u)| {
            format!("u{i}: userContestRanking(username: \"{u}\") {{ attendedContestsCount }}")
        })
        .collect();
    let d = gql(&format!("query {{ {} }}", q.join(" ")));
    usernames
        .iter()
        .enumerate()
        .filter_map(|(i, u)| {
            let e = d.get(format!("u{i}"))?;
            if e.is_null() {
                return None;
            }
            Some((u.clone(), e["attendedContestsCount"].as_i64().unwrap_or(0)))
        })
        .collect()
}

/// random.Random(SEED).sample(range(1, n + 1), k) for a large population:
/// CPython's set-based draw.
fn sample_pages(n: usize, k: usize) -> Vec<usize> {
    let mut rng = PyRandom::new(SEED);
    let mut selected = HashSet::new();
    let mut out = Vec::new();
    for _ in 0..k {
        let mut j = rng.randbelow(n as u32) as usize;
        while selected.contains(&j) {
            j = rng.randbelow(n as u32) as usize;
        }
        selected.insert(j);
        out.push(j + 1);
    }
    out
}

fn sample_regulars(ranking: &mut Ranking) -> Value {
    let (mut sampled, mut answered, mut ratings) = (0, 0, Vec::new());
    for p in sample_pages(ranking.pages, PAGES) {
        let nodes = ranking.nodes(p).clone();
        let counts = contest_counts(&nodes.iter().map(|n| n.2.clone()).collect::<Vec<_>>());
        sampled += nodes.len();
        answered += counts.len();
        ratings.extend(
            nodes
                .iter()
                .filter(|n| counts.get(&n.2).copied().unwrap_or(0) >= REGULAR_MIN)
                .map(|n| n.0),
        );
        println!("page {p}: {}/{} answered", counts.len(), nodes.len());
    }
    ratings.sort_by(|a, b| a.partial_cmp(b).unwrap());
    json!({"min_contests": REGULAR_MIN, "sampled": sampled, "answered": answered, "ratings": ratings})
}

pub fn run(ctx: &Ctx) {
    let out = ctx.root.join("data/leetcode_rank_table.json");
    let mut ranking = Ranking::new();
    let mut rows = Vec::new();
    let mut r = 1200;
    while r <= 3000 {
        let n = ranking.at_or_above(r as f64);
        rows.push(json!([r, n]));
        println!(
            "{r}: {n} at or above ({:.2}%)",
            100.0 * n as f64 / ranking.total as f64
        );
        r += 25;
    }
    let table = json!({
        "date": ctx.today().format("%Y-%m-%d").to_string(),
        "all": {"total": ranking.total, "rows": rows},
        "regulars": sample_regulars(&mut ranking),
    });
    std::fs::write(&out, serde_json::to_string_pretty(&table).unwrap()).expect("write table");
    println!("wrote {}", out.display());
}
