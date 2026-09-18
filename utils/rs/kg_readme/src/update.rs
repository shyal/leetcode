// Upload the charts to S3 and rewrite the README's generated regions.
//
// README.md is the single source of truth: prose is edited there, and each
// generated block lives between <!-- NAME --> ... <!-- /NAME --> markers.
// It is also where the previous run's S3 keys live: every timestamped key
// it links is HEADed first, so an unchanged chart keeps its link instead
// of landing on S3 again as a duplicate. Charts go up gzipped with a
// Content-Encoding header, mtime 0 and no filename, so the gzip bytes are
// a pure function of the SVG and the dedupe (md5 against the ETag of a
// single-part upload) can see through the compression. S3 is reached
// through the aws CLI, with the profile the makefile sets.
//
// Ported from utils/readme/update_readme.py (Python) on 2026-09-13.

use std::io::Write;
use std::path::Path;
use std::process::Command;

use flate2::write::GzEncoder;
use flate2::{Compression, GzBuilder};
use kg::ctx::Ctx;
use kg::evidence::Evidence;
use regex::Regex;
use serde_json::Value;

use crate::common::f0;
use crate::{elo, hours, onsite};

const BUCKET: &str = "shyal";

// (graph file, s3 prefix, README region, alt text, inline region?)
const CHARTS: [(&str, &str, &str, &str, bool); 12] = [
    (
        "graph/problem_rating.svg",
        "problem_rating",
        "PROBLEM_RATING_CHART",
        "Rating of the problems attempted",
        false,
    ),
    (
        "graph/problem_rating_month.svg",
        "problem_rating_month",
        "PROBLEM_RATING_MONTH_CHART",
        "Rating of the problems attempted in the last 30 days",
        false,
    ),
    (
        "graph/hours.svg",
        "hours",
        "HOURS_CHART",
        "Elo against hours of recorded solving, with the Carnegie Mellon rate",
        false,
    ),
    (
        "graph/onsite.svg",
        "onsite",
        "ONSITE_CHART",
        "Elo history and its projection to the onsite line, on dates",
        false,
    ),
    (
        "graph/backlog.svg",
        "backlog",
        "BACKLOG_CHART",
        "Backlog and forecast: review cards, solves by kind, STALE and FRAGILE nodes",
        false,
    ),
    (
        "graph/progress.svg",
        "progress",
        "PROGRESS_CHART",
        "Actual minus model on the last 30 first sights",
        false,
    ),
    ("graph/elo_badge.svg", "elo_badge", "ELO_BADGE", "Elo", true),
    (
        "graph/streak_badge.svg",
        "streak_badge",
        "STREAK_BADGE",
        "Streak",
        true,
    ),
    (
        "graph/rank_all_badge.svg",
        "rank_all_badge",
        "RANK_ALL_BADGE",
        "Elo against all rated LeetCode users",
        true,
    ),
    (
        "graph/rank_regulars_badge.svg",
        "rank_regulars_badge",
        "RANK_REGULARS_BADGE",
        "Elo against users with 20 or more contests",
        true,
    ),
    (
        "graph/rate_badge.svg",
        "rate_badge",
        "RATE_BADGE",
        "First-sight Elo per 100 hours",
        true,
    ),
    (
        "graph/rate_gauge.svg",
        "rate_gauge",
        "RATE_GAUGE",
        "Elo per 100 hours on problems seen for the first time",
        false,
    ),
];

fn aws(args: &[&str]) -> Option<Vec<u8>> {
    let out = Command::new("aws").args(args).output().ok()?;
    if out.status.success() {
        Some(out.stdout)
    } else {
        None
    }
}

/// The ETag of an object, or None when it is not there.
fn etag_of(key: &str) -> Option<String> {
    let out = aws(&[
        "s3api",
        "head-object",
        "--bucket",
        BUCKET,
        "--key",
        key,
        "--output",
        "json",
    ])?;
    let v: Value = serde_json::from_slice(&out).ok()?;
    Some(v.get("ETag")?.as_str()?.trim_matches('"').to_string())
}

fn upload(local: &Path, key: &str) -> Result<(), String> {
    let out = Command::new("aws")
        .args([
            "s3api",
            "put-object",
            "--bucket",
            BUCKET,
            "--key",
            key,
            "--body",
            local.to_str().unwrap(),
            "--content-type",
            "image/svg+xml",
            "--content-encoding",
            "gzip",
        ])
        .output()
        .map_err(|e| e.to_string())?;
    if out.status.success() {
        Ok(())
    } else {
        Err(format!(
            "put-object {key}: {}",
            String::from_utf8_lossy(&out.stderr).trim()
        ))
    }
}

/// The SVG gzipped as a pure function of its bytes: no name, mtime 0.
fn gzip_to(path: &Path, local: &Path) {
    let raw = std::fs::read(path).expect("read svg");
    let f = std::fs::File::create(local).expect("create gz");
    let mut g: GzEncoder<_> = GzBuilder::new()
        .mtime(0)
        .operating_system(255)
        .write(f, Compression::best());
    g.write_all(&raw).unwrap();
    g.finish().unwrap();
}

/// Rewrite only the inside of a block region, keeping its whitespace
/// padding. Empty content leaves the region as-is.
pub fn fill(text: &str, name: &str, content: &str) -> String {
    if content.is_empty() {
        return text.to_string();
    }
    let pat = Regex::new(&format!(
        r"(?s)<!-- {name} -->(\s*).*?(\s*)<!-- /{name} -->"
    ))
    .unwrap();
    if !pat.is_match(text) {
        println!("WARNING: no <!-- {name} --> region in README.md, skipped");
        return text.to_string();
    }
    pat.replace_all(text, |c: &regex::Captures| {
        let lead = if c[1].contains('\n') {
            c[1].to_string()
        } else {
            "\n".to_string()
        };
        let trail = if c[2].contains('\n') {
            c[2].to_string()
        } else {
            "\n".to_string()
        };
        format!("<!-- {name} -->{lead}{content}{trail}<!-- /{name} -->")
    })
    .to_string()
}

/// Same markers inside a sentence: every occurrence gets the value.
pub fn fill_inline(text: &str, name: &str, value: &str) -> String {
    let pat = Regex::new(&format!(r"(?s)<!-- {name} -->.*?<!-- /{name} -->")).unwrap();
    if !pat.is_match(text) {
        println!("WARNING: no <!-- {name} --> region in README.md, skipped");
        return text.to_string();
    }
    pat.replace_all(text, |_: &regex::Captures| {
        format!("<!-- {name} -->{value}<!-- /{name} -->")
    })
    .to_string()
}

pub fn run(ctx: &Ctx, ev: &Evidence) {
    let readme_path = ctx.root.join("README.md");
    let mut readme = std::fs::read_to_string(&readme_path).expect("README.md");
    let key_re =
        Regex::new(r"https://shyal\.s3\.amazonaws\.com/([a-z_]+_\d{14}\.(?:svg|png))").unwrap();
    // prefix -> key currently linked from README.md
    let mut existing: Vec<(String, String)> = Vec::new();
    for c in key_re.captures_iter(&readme) {
        let key = c[1].to_string();
        let prefix = key.rsplit_once('_').unwrap().0.to_string();
        match existing.iter_mut().find(|(p, _)| *p == prefix) {
            Some(slot) => slot.1 = key,
            None => existing.push((prefix, key)),
        }
    }
    let etags: Vec<(String, Option<String>)> = std::thread::scope(|sc| {
        let hs: Vec<_> = existing
            .iter()
            .map(|(p, k)| {
                let (p, k) = (p.clone(), k.clone());
                sc.spawn(move || (p, etag_of(&k)))
            })
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).collect()
    });
    let timestamp = chrono::Local::now().format("%Y%m%d%H%M%S").to_string();

    let mut upload_jobs: Vec<(std::path::PathBuf, String)> = Vec::new();
    let mut unchanged = 0;
    let mut images: Vec<(&str, String, bool)> = Vec::new();
    for (path, prefix, region, alt, inline) in CHARTS {
        let path = ctx.root.join(path);
        if !path.exists() {
            continue;
        }
        let local = std::env::temp_dir().join(format!("{prefix}.svg.gz"));
        gzip_to(&path, &local);
        let md5 = format!("{:x}", md5::compute(std::fs::read(&local).unwrap()));
        let linked = existing
            .iter()
            .find(|(p, _)| p == prefix)
            .map(|(_, k)| k.clone());
        let etag = etags
            .iter()
            .find(|(p, _)| p == prefix)
            .and_then(|(_, e)| e.clone());
        let key = match linked {
            Some(k) if etag.as_deref() == Some(md5.as_str()) => {
                unchanged += 1;
                k
            }
            _ => {
                let k = format!("{prefix}_{timestamp}.svg");
                upload_jobs.push((local, k.clone()));
                k
            }
        };
        images.push((
            region,
            format!("![{alt}](https://shyal.s3.amazonaws.com/{key})"),
            inline,
        ));
    }
    // push everything queued concurrently; any failure stops here, before
    // the README is touched
    let results: Vec<Result<(), String>> = std::thread::scope(|sc| {
        let hs: Vec<_> = upload_jobs
            .iter()
            .map(|(l, k)| sc.spawn(move || upload(l, k)))
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).collect()
    });
    for r in results {
        if let Err(e) = r {
            eprintln!("{e}");
            std::process::exit(1);
        }
    }
    println!("uploaded {}, unchanged {unchanged}", upload_jobs.len());

    // inline numbers the prose claims, so they can never go stale
    readme = fill_inline(&readme, "N_NODES", &ctx.nodes.len().to_string());
    if let Some(r) = kg::data::read_json(&ctx.graph_dir().join("reach.json")) {
        readme = fill_inline(&readme, "N_BANK", &kg::data::value_str(&r["catalog"]));
        let reach = r["predicted_reach"].as_f64().unwrap_or(0.0);
        readme = fill_inline(
            &readme,
            "N_REACH_TODAY",
            &format!("~{}", f0((reach / 100.0).round_ties_even() * 100.0)),
        );
    }
    // the Elo figures the prose quotes, from the chart code so the text
    // and the charts never disagree
    let gs = elo::games(ctx, ev);
    let ma = elo::elo_ma(&gs, elo::START, &[]);
    let (fs_rate, fs_early, fs_late) = onsite::first_sight_rate(&gs, &hours::hours_by_day(ctx));
    readme = fill_inline(&readme, "FS_RATE", &format!("{:+.0}", fs_rate * 100.0));
    readme = fill_inline(&readme, "FS_EARLY", &f0(fs_early));
    readme = fill_inline(&readme, "FS_LATE", &f0(fs_late));
    readme = fill_inline(&readme, "FS_WINDOW", &onsite::FS_WINDOW.to_string());
    readme = fill_inline(
        &readme,
        "SERVED_MEDIAN",
        &f0(onsite::served(&gs).last().unwrap().1),
    );
    readme = fill_inline(&readme, "ELO_MA", &f0(ma.last().unwrap().1));
    readme = fill_inline(&readme, "ELO_MA_WINDOW", &elo::MA.to_string());
    for (region, markdown, inline) in images {
        readme = if inline {
            fill_inline(&readme, region, &markdown)
        } else {
            fill(&readme, region, &markdown)
        };
    }
    std::fs::write(&readme_path, readme).expect("write README.md");
    println!("README updated with S3 image links!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fill_keeps_the_padding_and_replaces_every_occurrence() {
        let t = "a <!-- X -->\n\nold\n\n<!-- /X --> b <!-- X -->old<!-- /X -->";
        assert_eq!(
            fill(t, "X", "new"),
            "a <!-- X -->\n\nnew\n\n<!-- /X --> b <!-- X -->\nnew\n<!-- /X -->"
        );
        assert_eq!(fill(t, "X", ""), t);
        assert_eq!(
            fill_inline(t, "X", "5"),
            "a <!-- X -->5<!-- /X --> b <!-- X -->5<!-- /X -->"
        );
    }
}
