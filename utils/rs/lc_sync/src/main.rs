// lc_sync - pull every accepted submission on the leetcode account into
// data/leetcode_submissions.json. A first sight is then the account's first
// solve of the problem, not the first file in solved/: the chart starts in
// October 2025 and the account in 2020, and the study-list classics solved
// then came back in the Grok era as first sights (59 unrated mediums, 40
// won, 2026-10-11). kg::model::scored_games reads the file.
//
//   lc_sync          # pull what is newer than the file, write it, print the totals
//   lc_sync --all    # pull the whole account again
//   lc_sync --show   # the totals from the file, no network
//
// Transport: the browser at LC_CDP_ENDPOINT (kg::lc), the one that passes
// Cloudflare. The account's submissions come newest first in pages of 20
// (submissionList, every verdict: the schema has no status filter), the
// accepted ones are kept, and the pull stops at the first submission
// already in the file. A 429 is waited out.
//
// The file: {"_comment": ..., "submissions": [...]} oldest first, one
// record per accepted submission: id, number, slug, date, timestamp, lang.
// `date` is the local day of the submission, the day a solve's evidence
// carries. A slug data/problems_metadata.json does not know keeps
// "number": null and is named at the end.

use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::time::Duration;

use chrono::{Local, TimeZone};
use kg::ctx::Ctx;
use kg::data::read_json;
use kg::evidence::Evidence;
use kg::lc::{ensure_browser, graphql, no_browser};
use serde_json::{json, Value};

pub const FILE: &str = "data/leetcode_submissions.json";
const PAGE: usize = 20;
const COMMENT: &str = "Every accepted submission on the leetcode account, oldest first \
    (make lc-sync). A problem's first date here is the account's first solve of it; a \
    solve in solved/ dated after it is a repeat, not a first sight.";

const QUERY: &str = "query submissionList($offset: Int!, $limit: Int!, $lastKey: String) {
  submissionList(offset: $offset, limit: $limit, lastKey: $lastKey) {
    lastKey
    hasNext
    submissions { id title titleSlug statusDisplay lang timestamp }
  }
}";

fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(1)
}

/// The records in the file, oldest first; none without a file.
fn load(path: &Path) -> Vec<Value> {
    read_json(path)
        .and_then(|v| v.get("submissions").and_then(Value::as_array).cloned())
        .unwrap_or_default()
}

fn id_of(s: &Value) -> Option<u64> {
    match &s["id"] {
        Value::Number(n) => n.as_u64(),
        Value::String(t) => t.parse().ok(),
        _ => None,
    }
}

fn timestamp_of(s: &Value) -> Option<i64> {
    match &s["timestamp"] {
        Value::Number(n) => n.as_i64(),
        Value::String(t) => t.parse().ok(),
        _ => None,
    }
}

/// The local day of a unix timestamp, YYYY-MM-DD.
fn local_day(ts: i64) -> String {
    Local
        .timestamp_opt(ts, 0)
        .single()
        .map(|d| d.format("%Y-%m-%d").to_string())
        .unwrap_or_default()
}

/// slug -> problem number, from data/problems_metadata.json; the API's
/// own ids are internal, not the numbers the site shows.
fn numbers_by_slug(ctx: &Ctx) -> HashMap<String, String> {
    ctx.meta
        .iter()
        .filter_map(|(n, m)| m.slug.clone().map(|s| (s, n.clone())))
        .collect()
}

/// One page of the account's submissions, newest first, from `offset`:
/// (the submissions, hasNext, lastKey). A 429 is waited out, doubling from
/// five seconds.
fn page(offset: usize, last_key: &Value) -> Result<(Vec<Value>, bool, Value), String> {
    let mut wait = 5;
    loop {
        let vars = json!({"offset": offset, "limit": PAGE, "lastKey": last_key});
        match graphql(QUERY, vars)? {
            (200, data) => {
                let list = &data["submissionList"];
                let subs = list["submissions"].as_array().cloned().unwrap_or_default();
                let has_next = list["hasNext"].as_bool().unwrap_or(false);
                return Ok((subs, has_next, list["lastKey"].clone()));
            }
            (429, _) if wait <= 80 => {
                eprintln!("leetcode is rate limiting; retrying in {wait}s");
                std::thread::sleep(Duration::from_secs(wait));
                wait *= 2;
            }
            (403, _) => {
                return Err("leetcode refused the request (403): is the browser logged in?".into())
            }
            (status, body) => {
                let body = body
                    .as_str()
                    .unwrap_or("")
                    .chars()
                    .take(200)
                    .collect::<String>();
                return Err(format!("submissionList: http {status}: {body}"));
            }
        }
    }
}

/// The accepted submissions newer than `known`, newest first.
fn pull(known: &HashSet<u64>, numbers: &HashMap<String, String>) -> Result<Vec<Value>, String> {
    let mut out = Vec::new();
    let mut offset = 0;
    let mut last_key = Value::Null;
    loop {
        let (subs, has_next, key) = page(offset, &last_key)?;
        let mut hit_known = false;
        for s in &subs {
            let Some(id) = id_of(s) else {
                continue;
            };
            if known.contains(&id) {
                hit_known = true;
                continue;
            }
            if s["statusDisplay"].as_str() != Some("Accepted") {
                continue;
            }
            let slug = s["titleSlug"].as_str().unwrap_or("").to_string();
            let ts = timestamp_of(s).unwrap_or(0);
            out.push(json!({
                "id": id,
                "number": numbers.get(&slug).cloned(),
                "slug": slug,
                "date": local_day(ts),
                "timestamp": ts,
                "lang": s["lang"].as_str().unwrap_or(""),
            }));
        }
        if let Some(oldest) = out.last() {
            eprint!(
                "\r{} accepted submissions, back to {}        ",
                out.len(),
                oldest["date"].as_str().unwrap_or("")
            );
        }
        if hit_known || !has_next || subs.is_empty() {
            break;
        }
        offset += subs.len();
        last_key = key;
        std::thread::sleep(Duration::from_millis(300));
    }
    if !out.is_empty() {
        eprintln!();
    }
    Ok(out)
}

fn write(path: &Path, mut subs: Vec<Value>) {
    subs.sort_by_key(|s| (timestamp_of(s).unwrap_or(0), id_of(s).unwrap_or(0)));
    let doc = json!({"_comment": COMMENT, "submissions": subs});
    let text = serde_json::to_string_pretty(&doc).expect("json") + "\n";
    std::fs::write(path, text).unwrap_or_else(|e| die(&format!("{}: {e}", path.display())));
}

/// The totals, as sentences: what the account holds and how many of the
/// repo's first sights it predates.
fn show(ctx: &Ctx, ev: &Evidence, subs: &[Value]) {
    if subs.is_empty() {
        println!("The file has no submissions.");
        return;
    }
    let account = kg::model::account_first_dates(&ctx.root);
    let unknown: Vec<&str> = subs
        .iter()
        .filter(|s| s["number"].is_null())
        .filter_map(|s| s["slug"].as_str())
        .collect();
    println!(
        "The account holds {} accepted submissions on {} problems, from {} to {}.",
        subs.len(),
        account.len() + unknown.len(),
        subs[0]["date"].as_str().unwrap_or(""),
        subs[subs.len() - 1]["date"].as_str().unwrap_or("")
    );
    let repo_first = kg::model::first_dates(ev);
    let mut earlier: Vec<(&String, &String, &String)> = repo_first
        .iter()
        .filter_map(|(p, d)| account.get(p).filter(|a| *a < d).map(|a| (p, a, d)))
        .collect();
    earlier.sort_by(|a, b| (a.1, a.0).cmp(&(b.1, b.0)));
    let mut by_year: HashMap<&str, usize> = HashMap::new();
    for (_, a, _) in &earlier {
        *by_year.entry(&a[..4]).or_default() += 1;
    }
    let mut years: Vec<(&str, usize)> = by_year.into_iter().collect();
    years.sort();
    let years: Vec<String> = years.iter().map(|(y, n)| format!("{n} in {y}")).collect();
    println!(
        "{} of the {} problems in solved/ were accepted on the account before their first file here ({}), so those solves are repeats, not first sights.",
        earlier.len(),
        repo_first.len(),
        if years.is_empty() {
            "none".to_string()
        } else {
            years.join(", ")
        }
    );
    if !unknown.is_empty() {
        let mut u: Vec<&str> = unknown.clone();
        u.sort_unstable();
        u.dedup();
        println!(
            "{} slugs are not in data/problems_metadata.json, so they carry no number: {}.",
            u.len(),
            u.join(", ")
        );
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "--help" || a == "-h") {
        println!("usage: lc_sync [--all | --show]");
        return;
    }
    let root: PathBuf = kg::data::repo_root();
    let path = root.join(FILE);
    let (ctx, recs) = Ctx::load(root.clone());
    let ev = Evidence::new(recs);
    let have = load(&path);
    if args.iter().any(|a| a == "--show") {
        if have.is_empty() {
            println!("No {FILE} yet; run make lc-sync.");
        } else {
            show(&ctx, &ev, &have);
        }
        return;
    }
    if no_browser() {
        die("no browser: set LC_CDP_ENDPOINT to its devtools endpoint (lc_submit uses the same one)");
    }
    let all = args.iter().any(|a| a == "--all");
    let known: HashSet<u64> = if all {
        HashSet::new()
    } else {
        have.iter().filter_map(id_of).collect()
    };
    let numbers = numbers_by_slug(&ctx);
    let fresh = match ensure_browser().and_then(|()| pull(&known, &numbers)) {
        Ok(f) => f,
        Err(e) => die(&e),
    };
    let n = fresh.len();
    let mut subs = if all { Vec::new() } else { have };
    subs.extend(fresh);
    write(&path, subs);
    let subs = load(&path);
    println!("{n} new accepted submissions; {FILE} holds {}.", subs.len());
    show(&ctx, &ev, &subs);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ids_and_timestamps_read_as_strings_or_numbers() {
        assert_eq!(id_of(&json!({"id": "123"})), Some(123));
        assert_eq!(id_of(&json!({"id": 123})), Some(123));
        assert_eq!(
            timestamp_of(&json!({"timestamp": "1595469755"})),
            Some(1595469755)
        );
        assert_eq!(id_of(&json!({})), None);
    }
}
