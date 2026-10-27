// The three problem tables the picker and the README read, kept fresh
// by the hourly crowd job (kg_crowd) and by `make tables`:
//
//   data/problems_metadata.json  every problem LeetCode lists: number ->
//                                title, slug, difficulty, paid_only (only
//                                when true), acceptance. From
//                                leetcode.com/api/problems/all/, no login.
//   data/leetcode_ratings.tsv    zerotrac's contest ratings (rating, id,
//                                slug), from his GitHub ratings.txt.
//   data/clist_problems.json     CLIST's problem table for leetcode
//                                (rating, counts, contest time), paged
//                                from clist.by with the key in .envrc.
//
// A contest adds four problems a week and zerotrac rates them a few
// days later, so a table older than a week is stale (STALE_DAYS) and is
// fetched again; a fetch that fails leaves the file as it was and the
// next run tries again. Before this (2026-10-27) the tables were
// snapshots written by scripts since deleted (utils/history/metadata.py,
// utils/kg/clist.py), last run in September 2026, so Weekly Contest 525's
// problems were in none of them.

use std::path::{Path, PathBuf};

use serde_json::{Map, Value};

use crate::crowd::UA;
use crate::pyjson;

/// A table older than this many days is fetched again: the contest cadence.
pub const STALE_DAYS: i64 = 7;

pub const METADATA: &str = "data/problems_metadata.json";
pub const RATINGS: &str = "data/leetcode_ratings.tsv";
pub const CLIST: &str = "data/clist_problems.json";

const PROBLEMS_ALL: &str = "https://leetcode.com/api/problems/all/";
const ZEROTRAC: &str =
    "https://raw.githubusercontent.com/zerotrac/leetcode_problem_rating/main/ratings.txt";
const CLIST_API: &str = "https://clist.by/api/v4/problem/";
/// clist.by's resource id for leetcode.com.
const CLIST_RESOURCE: u32 = 102;
const CLIST_PAGE: usize = 1000;
/// CLIST allows 10 requests a minute.
const CLIST_PAUSE_MS: u64 = 6500;
/// The CLIST fields kept, in the order json.dump(sort_keys=True) wrote them.
const CLIST_FIELDS: [&str; 7] = [
    "kinds",
    "n_accepted",
    "n_total",
    "name",
    "rating",
    "slug",
    "time",
];

// ---- the transport ----------------------------------------------------

fn agent() -> ureq::Agent {
    ureq::Agent::config_builder()
        .timeout_global(Some(std::time::Duration::from_secs(120)))
        .build()
        .into()
}

fn get_text(url: &str, auth: Option<&str>) -> Result<String, String> {
    let mut req = agent().get(url).header("User-Agent", UA);
    if let Some(a) = auth {
        req = req.header("Authorization", a);
    }
    let mut resp = req.call().map_err(|e| format!("{url}: {e}"))?;
    resp.body_mut()
        .read_to_string()
        .map_err(|e| format!("{url}: {e}"))
}

fn get_json(url: &str, auth: Option<&str>) -> Result<Value, String> {
    serde_json::from_str(&get_text(url, auth)?).map_err(|e| format!("{url}: {e}"))
}

// ---- problems_metadata.json -------------------------------------------

/// The table utils/history/metadata.py wrote, from the problems/all
/// answer: number -> {title, slug, difficulty, [paid_only], [acceptance]},
/// in the API's order (newest first).
pub fn parse_metadata(all: &Value) -> Result<Map<String, Value>, String> {
    let pairs = all["stat_status_pairs"]
        .as_array()
        .ok_or("problems/all: no stat_status_pairs")?;
    let mut out = Map::new();
    for p in pairs {
        let s = &p["stat"];
        let num = s["frontend_question_id"]
            .as_i64()
            .map(|n| n.to_string())
            .or_else(|| s["frontend_question_id"].as_str().map(String::from))
            .ok_or("problems/all: a problem with no frontend_question_id")?;
        let mut m = Map::new();
        m.insert("title".into(), s["question__title"].clone());
        m.insert("slug".into(), s["question__title_slug"].clone());
        let level = match p["difficulty"]["level"].as_i64() {
            Some(1) => "Easy",
            Some(2) => "Medium",
            Some(3) => "Hard",
            other => return Err(format!("problems/all: {num}: difficulty level {other:?}")),
        };
        m.insert("difficulty".into(), Value::from(level));
        if p["paid_only"].as_bool() == Some(true) {
            m.insert("paid_only".into(), Value::Bool(true));
        }
        let (acs, sub) = (
            s["total_acs"].as_f64().unwrap_or(0.0),
            s["total_submitted"].as_f64().unwrap_or(0.0),
        );
        if sub > 0.0 {
            let pct = (1000.0 * acs / sub).round() / 10.0;
            m.insert("acceptance".into(), Value::from(pct));
        }
        out.insert(num, Value::Object(m));
    }
    Ok(out)
}

pub fn fetch_metadata() -> Result<Map<String, Value>, String> {
    parse_metadata(&get_json(PROBLEMS_ALL, None)?)
}

// ---- leetcode_ratings.tsv ---------------------------------------------

/// zerotrac's ratings.txt (Rating, ID, Title, Title ZH, Title Slug,
/// Contest Slug, Problem Index) as the three columns the repo keeps,
/// sorted by problem number, the rating to one decimal.
pub fn parse_zerotrac(text: &str) -> Result<String, String> {
    let mut rows: Vec<(i64, String, String)> = Vec::new();
    for (i, line) in text.lines().enumerate() {
        if i == 0 || line.trim().is_empty() {
            continue;
        }
        let f: Vec<&str> = line.split('\t').collect();
        if f.len() < 5 {
            return Err(format!("ratings.txt line {}: {} columns", i + 1, f.len()));
        }
        let rating: f64 = f[0]
            .parse()
            .map_err(|_| format!("ratings.txt line {}: rating {:?}", i + 1, f[0]))?;
        let id: i64 = f[1]
            .parse()
            .map_err(|_| format!("ratings.txt line {}: id {:?}", i + 1, f[1]))?;
        rows.push((id, format!("{rating:.1}"), f[4].to_string()));
    }
    if rows.is_empty() {
        return Err("ratings.txt: no rows".into());
    }
    rows.sort();
    let mut out = String::from("rating\tid\tslug\n");
    for (id, rating, slug) in rows {
        out.push_str(&format!("{rating}\t{id}\t{slug}\n"));
    }
    Ok(out)
}

pub fn fetch_zerotrac() -> Result<String, String> {
    parse_zerotrac(&get_text(ZEROTRAC, None)?)
}

// ---- clist_problems.json ----------------------------------------------

/// One CLIST page's objects as the rows the repo keeps: the fields of
/// CLIST_FIELDS, problems with a slug only.
pub fn clist_rows(objects: &Value) -> Vec<Value> {
    objects
        .as_array()
        .into_iter()
        .flatten()
        .filter(|o| o["slug"].as_str().is_some_and(|s| !s.is_empty()))
        .map(|o| {
            let mut m = Map::new();
            for f in CLIST_FIELDS {
                m.insert(f.to_string(), o.get(f).cloned().unwrap_or(Value::Null));
            }
            Value::Object(m)
        })
        .collect()
}

/// Every leetcode problem CLIST knows, sorted by slug. The API wants
/// CLIST_USERNAME and CLIST_API_KEY (.envrc); the pages are paced to its
/// limit, so this takes about a minute.
pub fn fetch_clist() -> Result<Vec<Value>, String> {
    let (Ok(user), Ok(key)) = (
        std::env::var("CLIST_USERNAME"),
        std::env::var("CLIST_API_KEY"),
    ) else {
        return Err("set CLIST_USERNAME and CLIST_API_KEY (see .envrc)".into());
    };
    let auth = format!("ApiKey {user}:{key}");
    let mut rows = Vec::new();
    let mut offset = 0;
    loop {
        if offset > 0 {
            std::thread::sleep(std::time::Duration::from_millis(CLIST_PAUSE_MS));
        }
        let url = format!(
            "{CLIST_API}?resource_id={CLIST_RESOURCE}&limit={CLIST_PAGE}&offset={offset}&order_by=id&format=json"
        );
        let page = get_json(&url, Some(&auth))?;
        let objects = page["objects"]
            .as_array()
            .ok_or_else(|| format!("{url}: no objects"))?;
        rows.extend(clist_rows(&page["objects"]));
        if objects.len() < CLIST_PAGE {
            break;
        }
        offset += CLIST_PAGE;
    }
    if rows.is_empty() {
        return Err("clist: no problems".into());
    }
    rows.sort_by(|a, b| a["slug"].as_str().cmp(&b["slug"].as_str()));
    Ok(rows)
}

// ---- the refresh --------------------------------------------------------

/// Days since the file was last written; None with no file.
pub fn age_days(path: &Path) -> Option<i64> {
    let modified = std::fs::metadata(path).ok()?.modified().ok()?;
    let age = std::time::SystemTime::now()
        .duration_since(modified)
        .unwrap_or_default();
    Some((age.as_secs() / 86_400) as i64)
}

/// A table with no file, or one older than `stale` days, is due.
pub fn is_due(age: Option<i64>, stale: i64) -> bool {
    age.is_none_or(|d| d >= stale)
}

fn write_text(path: &Path, text: &str) -> std::io::Result<()> {
    let name = path
        .file_name()
        .and_then(|n| n.to_str())
        .ok_or_else(|| std::io::Error::other("write: no file name"))?;
    let tmp = path.with_file_name(format!(".{name}.tmp"));
    std::fs::write(&tmp, text)?;
    std::fs::rename(&tmp, path)
}

/// Fetch and write every table that is due (every table, with `force`).
/// One line per table, fetched or not; a failed fetch is reported and the
/// file is left as it was.
pub fn refresh(root: &Path, stale: i64, force: bool) -> Vec<String> {
    let mut lines = Vec::new();
    let tables: [(&str, fn(&Path) -> Result<String, String>); 3] = [
        (METADATA, |p| {
            let m = fetch_metadata()?;
            let n = m.len();
            pyjson::save(p, &Value::Object(m), None).map_err(|e| e.to_string())?;
            Ok(format!("{n} problems"))
        }),
        (RATINGS, |p| {
            let tsv = fetch_zerotrac()?;
            let n = tsv.lines().count() - 1;
            write_text(p, &tsv).map_err(|e| e.to_string())?;
            Ok(format!("{n} rated"))
        }),
        (CLIST, |p| {
            let rows = fetch_clist()?;
            let rated = rows
                .iter()
                .filter(|r| r["rating"].as_f64().unwrap_or(0.0) != 0.0)
                .count();
            let n = rows.len();
            pyjson::save(p, &Value::Array(rows), Some(1)).map_err(|e| e.to_string())?;
            Ok(format!("{n} problems, {rated} rated"))
        }),
    ];
    for (file, fetch) in tables {
        let path: PathBuf = root.join(file);
        let age = age_days(&path);
        if !force && !is_due(age, stale) {
            lines.push(format!("{file}: {} days old, kept", age.unwrap_or(0)));
            continue;
        }
        match fetch(&path) {
            Ok(what) => lines.push(format!("{file}: fetched, {what}")),
            Err(e) => lines.push(format!("{file}: not fetched ({e}), kept")),
        }
    }
    lines
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn metadata_keeps_the_api_order_and_flags_paid_only_when_true() {
        let all = json!({"stat_status_pairs": [
            {"stat": {"frontend_question_id": 4095, "question__title": "Count Frequency Staircase Subarrays II",
                      "question__title_slug": "count-frequency-staircase-subarrays-ii",
                      "total_acs": 892, "total_submitted": 8400},
             "difficulty": {"level": 3}, "paid_only": false},
            {"stat": {"frontend_question_id": 261, "question__title": "Graph Valid Tree",
                      "question__title_slug": "graph-valid-tree", "total_acs": 0, "total_submitted": 0},
             "difficulty": {"level": 2}, "paid_only": true},
        ]});
        let m = parse_metadata(&all).unwrap();
        assert_eq!(m.keys().cloned().collect::<Vec<_>>(), ["4095", "261"]);
        assert_eq!(m["4095"]["difficulty"], "Hard");
        assert_eq!(m["4095"]["acceptance"], 10.6);
        assert!(m["4095"].get("paid_only").is_none());
        assert_eq!(m["261"]["paid_only"], true);
        assert!(m["261"].get("acceptance").is_none());
        assert_eq!(
            pyjson::dumps(&Value::Object(m), None),
            r#"{"4095": {"title": "Count Frequency Staircase Subarrays II", "slug": "count-frequency-staircase-subarrays-ii", "difficulty": "Hard", "acceptance": 10.6}, "261": {"title": "Graph Valid Tree", "slug": "graph-valid-tree", "difficulty": "Medium", "paid_only": true}}"#
        );
    }

    #[test]
    fn zerotrac_becomes_three_columns_sorted_by_number() {
        let text = "Rating\tID\tTitle\tTitle ZH\tTitle Slug\tContest Slug\tProblem Index\n\
                    3124.5016688063\t3743\tMaximize Cyclic Partition Score\t循环划分的最大得分\tmaximize-cyclic-partition-score\tweekly-contest-475\tQ4\n\
                    1358.4138240224\t746\tMin Cost Climbing Stairs\t使用最小花费爬楼梯\tmin-cost-climbing-stairs\tweekly-contest-63\tQ1\n";
        assert_eq!(
            parse_zerotrac(text).unwrap(),
            "rating\tid\tslug\n1358.4\t746\tmin-cost-climbing-stairs\n3124.5\t3743\tmaximize-cyclic-partition-score\n"
        );
        assert!(parse_zerotrac("Rating\tID\n").is_err());
        assert!(parse_zerotrac("Rating\tID\tT\tZ\tS\tC\tI\nx\t1\ta\tb\tc\td\te\n").is_err());
    }

    #[test]
    fn clist_rows_keep_the_sorted_fields_and_drop_slugless_rows() {
        let objects = json!([
            {"id": 1, "slug": "two-sum", "name": "Two Sum", "rating": 1100, "n_accepted": 5,
             "n_total": 9, "time": "2017-01-01T00:00:00", "kinds": [], "url": "x"},
            {"id": 2, "slug": "", "name": "Nameless"},
        ]);
        let rows = clist_rows(&objects);
        assert_eq!(rows.len(), 1);
        assert_eq!(
            rows[0]
                .as_object()
                .unwrap()
                .keys()
                .cloned()
                .collect::<Vec<_>>(),
            CLIST_FIELDS
        );
        assert_eq!(rows[0]["rating"], 1100);
    }

    #[test]
    fn a_table_is_due_without_a_file_or_after_the_cadence() {
        assert!(is_due(None, STALE_DAYS));
        assert!(is_due(Some(7), STALE_DAYS));
        assert!(!is_due(Some(6), STALE_DAYS));
        assert!(!is_due(Some(0), STALE_DAYS));
    }
}
