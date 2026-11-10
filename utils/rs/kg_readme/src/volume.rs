// The volume charts, read from the git history of the repository:
//
//   graph/commits.svg  cumulative tooling commits against solve commits,
//                      one point per day
//   graph/rates.svg    solves and drills per day (top), and the distinct
//                      problems and drills per day (bottom), each with a
//                      MA_DAYS-day average of the total
//
// A solve commit adds a solved/ file that is not a FAILED record (problems
// and drills alike). A tooling commit is any other commit that touches
// code: utils/, the makefile, dsa/, drills/, stubs/, misc/, .github/,
// conftest.py, requirements.txt, or any .py/.rs file outside solved/.
// Commits that only regenerate the README, edit graph json or record a
// fail or a sleep are neither and are not drawn.
//
// In rates.svg a solve is a solved/p<num>_* file added by a commit and a
// drill is a solved/d_<name>_* file. A commit that adds more than
// IMPORT_CAP solve files is an import of older work and is skipped.
//
// Days are Manila days, and both charts end on the day of the run.
//
// Ported from utils/readme/kg_commits_svg and kg_rates_svg (Python, deleted
// on 2026-09-20) on 2026-11-10.

use std::collections::{BTreeMap, BTreeSet};
use std::process::{Command, Stdio};

use chrono::{Datelike, Duration, NaiveDate};
use kg::ctx::Ctx;
use kg::data::parse_date;
use regex::Regex;

use crate::common::*;

const TOOL_PREFIXES: [&str; 10] = [
    "utils/",
    "makefile",
    "Makefile",
    "dsa/",
    "drills/",
    "stubs/",
    "misc/",
    ".github/",
    "conftest.py",
    "requirements.txt",
];
pub const IMPORT_CAP: usize = 5;
pub const MA_DAYS: usize = 7;

const W: i64 = 1200;
const SOLVE: &str = BLUE;
const TOOL: &str = GOLD;
const DRILL: &str = GREEN;
const MA: &str = "#f0f6fc";
const ML: i64 = 62;
const MR: i64 = 24;

/// [(Manila day, files named by the commit)], newest first.
fn commits(ctx: &Ctx, extra: &[&str]) -> Vec<(NaiveDate, Vec<String>)> {
    let mut args = vec![
        "log",
        "--name-only",
        "--format=%x01%ad",
        "--date=short-local",
    ];
    args.extend_from_slice(extra);
    let out = Command::new("git")
        .args(&args)
        .current_dir(&ctx.root)
        .env("TZ", "Asia/Manila")
        .stderr(Stdio::null())
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
        .unwrap_or_default();
    out.split('\x01')
        .skip(1)
        .filter_map(|block| {
            let mut lines = block.trim().lines();
            let day = lines.next()?.get(..10)?.to_string();
            Some((
                parse_date(&day),
                lines
                    .filter(|l| !l.is_empty())
                    .map(str::to_string)
                    .collect(),
            ))
        })
        .collect()
}

pub fn is_solve(files: &[String]) -> bool {
    files
        .iter()
        .any(|f| f.starts_with("solved/") && !f.contains("FAILED"))
}

pub fn is_tool(files: &[String]) -> bool {
    files.iter().any(|f| {
        TOOL_PREFIXES.iter().any(|p| f.starts_with(p))
            || ((f.ends_with(".py") || f.ends_with(".rs"))
                && !f.starts_with("solved/")
                && f != "current.py")
    })
}

/// Every day from the first key to `end`, with the day's value or the
/// default.
fn daily<T: Clone + Default>(
    by_day: &BTreeMap<NaiveDate, T>,
    end: NaiveDate,
) -> Vec<(NaiveDate, T)> {
    let Some(&first) = by_day.keys().next() else {
        return Vec::new();
    };
    let mut out = Vec::new();
    let mut d = first;
    while d <= end {
        out.push((d, by_day.get(&d).cloned().unwrap_or_default()));
        d += Duration::days(1);
    }
    out
}

fn head(title: &str, h: i64) -> Vec<String> {
    vec![
        format!("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {W} {h}\" font-family=\"Helvetica,sans-serif\">"),
        format!("<rect width=\"{W}\" height=\"{h}\" fill=\"{BG}\"/>"),
        format!(
            "<text x=\"{}\" y=\"24\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">{title}</text>",
            W / 2
        ),
    ]
}

fn x_at(i: usize, n: usize) -> f64 {
    ML as f64 + i as f64 / (n.max(2) - 1) as f64 * (W - ML - MR) as f64
}

/// A grid line and a label every `step` from 0 to ymax.
fn value_grid(svg: &mut Vec<String>, ymax: f64, step: i64, y_of: &dyn Fn(f64) -> f64) {
    let mut g = 0;
    while g as f64 <= ymax {
        let y = y_of(g as f64);
        svg.push(format!(
            "<line x1=\"{ML}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" stroke=\"{GRID}\" stroke-width=\"1\"/>",
            f1(y),
            W - MR,
            f1(y)
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{g}</text>",
            ML - 8,
            f1(y + 4.0)
        ));
        g += step;
    }
}

/// A vertical line on the first day of each month across each lane, and
/// the month under the last lane.
fn month_grid(svg: &mut Vec<String>, days: &[NaiveDate], lanes: &[(i64, i64)]) {
    for (i, d) in days.iter().enumerate() {
        if d.day() != 1 {
            continue;
        }
        let x = f1(x_at(i, days.len()));
        for (top, bottom) in lanes {
            svg.push(format!(
                "<line x1=\"{x}\" y1=\"{top}\" x2=\"{x}\" y2=\"{bottom}\" stroke=\"{GRID}\" stroke-width=\"1\"/>"
            ));
        }
        svg.push(format!(
            "<text x=\"{x}\" y=\"{}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{}</text>",
            lanes[lanes.len() - 1].1 + 18,
            d.format("%b %y")
        ));
    }
}

fn key(svg: &mut Vec<String>, x: i64, y: i64, color: &str, label: &str) {
    svg.push(format!(
        "<rect x=\"{x}\" y=\"{y}\" width=\"12\" height=\"12\" rx=\"3\" fill=\"{color}\"/>"
    ));
    svg.push(format!(
        "<text x=\"{}\" y=\"{}\" font-size=\"11\" fill=\"{INK}\">{label}</text>",
        x + 18,
        y + 10
    ));
}

pub fn render_commits(ctx: &Ctx) {
    const H: i64 = 400;
    const MT: i64 = 62;
    const MB: i64 = 60;
    let out = ctx.graph_dir().join("commits.svg");
    // day -> (tooling commits, solve commits)
    let mut by_day: BTreeMap<NaiveDate, (i64, i64)> = BTreeMap::new();
    for (d, files) in commits(ctx, &[]) {
        if is_solve(&files) {
            by_day.entry(d).or_default().1 += 1;
        } else if is_tool(&files) {
            by_day.entry(d).or_default().0 += 1;
        }
    }
    let per_day = daily(&by_day, ctx.today());
    if per_day.is_empty() {
        println!("no commits found");
        return;
    }
    let (mut tools, mut solves) = (0, 0);
    let rows: Vec<(NaiveDate, [i64; 2])> = per_day
        .into_iter()
        .map(|(d, (t, s))| {
            tools += t;
            solves += s;
            (d, [tools, solves])
        })
        .collect();
    let n = rows.len();
    let last = rows[n - 1].1;
    let (top, bottom) = (MT, H - MB);
    let ymax = last[0].max(last[1]).max(1) as f64 * 1.08;
    let y_of = |v: f64| bottom as f64 - v / ymax * (bottom - top) as f64;

    let mut svg = head(
        "Cumulative commits: tooling (yellow) versus solves (blue), full repo history",
        H,
    );
    let step = if ymax > 2000.0 {
        500
    } else if ymax > 800.0 {
        200
    } else if ymax > 400.0 {
        100
    } else if ymax > 150.0 {
        50
    } else if ymax > 60.0 {
        20
    } else {
        10
    };
    value_grid(&mut svg, ymax, step, &y_of);
    let days: Vec<NaiveDate> = rows.iter().map(|r| r.0).collect();
    month_grid(&mut svg, &days, &[(top, bottom)]);
    for (col, color) in [(0, TOOL), (1, SOLVE)] {
        let pts: Vec<String> = rows
            .iter()
            .enumerate()
            .map(|(i, r)| format!("{},{}", f1(x_at(i, n)), f1(y_of(r.1[col] as f64))))
            .collect();
        svg.push(format!(
            "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\"/>",
            pts.join(" ")
        ));
        svg.push(format!(
            "<text x=\"{}\" y=\"{}\" text-anchor=\"end\" font-size=\"11\" fill=\"{color}\">{}</text>",
            W - MR - 4,
            f1(y_of(last[col] as f64) - 6.0),
            last[col]
        ));
    }
    key(&mut svg, ML, bottom + 30, TOOL, "tooling commits");
    key(&mut svg, ML + 130, bottom + 30, SOLVE, "solve commits");
    svg.push("</svg>".to_string());
    write(&out, &svg);
    println!(
        "wrote {} ({n} days: {} tooling commits, {} solve commits)",
        out.display(),
        last[0],
        last[1]
    );
}

#[derive(Clone, Default)]
struct Day {
    solves: i64,
    drills: i64,
    problems: BTreeSet<String>,
    names: BTreeSet<String>,
}

fn moving_average(xs: &[i64]) -> Vec<f64> {
    (0..xs.len())
        .map(|i| {
            let lo = (i + 1).saturating_sub(MA_DAYS);
            xs[lo..=i].iter().sum::<i64>() as f64 / (i + 1 - lo) as f64
        })
        .collect()
}

/// Stacked areas of series a (bottom) and b (on top), and the average of
/// a + b.
fn panel(svg: &mut Vec<String>, a: &[i64], b: &[i64], lane: (i64, i64), title: &str) {
    let (top, bottom) = lane;
    let n = a.len();
    let total: Vec<i64> = a.iter().zip(b).map(|(p, q)| p + q).collect();
    let ymax = total.iter().copied().max().unwrap_or(0).max(1) as f64 * 1.08;
    let y_of = |v: f64| bottom as f64 - v / ymax * (bottom - top) as f64;
    svg.push(format!(
        "<text x=\"{ML}\" y=\"{}\" font-size=\"12\" fill=\"{INK}\">{title}</text>",
        top - 10
    ));
    let step = if ymax > 60.0 {
        20
    } else if ymax > 30.0 {
        10
    } else if ymax > 12.0 {
        5
    } else if ymax > 5.0 {
        2
    } else {
        1
    };
    value_grid(svg, ymax, step, &y_of);
    let mut area = |lower: &[i64], upper: &[i64], color: &str| {
        let mut pts: Vec<String> = (0..n)
            .map(|i| format!("{},{}", f1(x_at(i, n)), f1(y_of(upper[i] as f64))))
            .collect();
        pts.extend(
            (0..n)
                .rev()
                .map(|i| format!("{},{}", f1(x_at(i, n)), f1(y_of(lower[i] as f64)))),
        );
        svg.push(format!(
            "<polygon points=\"{}\" fill=\"{color}\" fill-opacity=\"0.75\"/>",
            pts.join(" ")
        ));
    };
    area(&vec![0; n], a, SOLVE);
    area(a, &total, DRILL);
    let ma: Vec<String> = moving_average(&total)
        .iter()
        .enumerate()
        .map(|(i, v)| format!("{},{}", f1(x_at(i, n)), f1(y_of(*v))))
        .collect();
    svg.push(format!(
        "<polyline points=\"{}\" fill=\"none\" stroke=\"{MA}\" stroke-width=\"1.6\" stroke-dasharray=\"6 4\"/>",
        ma.join(" ")
    ));
}

pub fn render_rates(ctx: &Ctx) {
    const H: i64 = 560;
    const LANES: [(i64, i64); 2] = [(62, 270), (322, 500)];
    let out = ctx.graph_dir().join("rates.svg");
    let problem = Regex::new(r"^p(\d+)_").unwrap();
    let drill = Regex::new(r"^d_(.+?)_\d{4}_").unwrap();
    let mut by_day: BTreeMap<NaiveDate, Day> = BTreeMap::new();
    for (d, files) in commits(ctx, &["--diff-filter=A", "--", "solved/"]) {
        let names: Vec<&str> = files
            .iter()
            .filter(|f| !f.contains("FAILED"))
            .filter_map(|f| f.strip_prefix("solved/"))
            .collect();
        if names.len() > IMPORT_CAP {
            continue;
        }
        for name in names {
            let day = by_day.entry(d).or_default();
            if let Some(m) = problem.captures(name) {
                day.solves += 1;
                day.problems.insert(m[1].to_string());
            } else if let Some(m) = drill.captures(name) {
                day.drills += 1;
                day.names.insert(m[1].to_string());
            }
        }
    }
    let rows = daily(&by_day, ctx.today());
    if rows.is_empty() {
        println!("no solves found");
        return;
    }
    let col = |f: &dyn Fn(&Day) -> i64| -> Vec<i64> { rows.iter().map(|(_, d)| f(d)).collect() };
    let series = [
        col(&|d| d.solves),
        col(&|d| d.drills),
        col(&|d| d.problems.len() as i64),
        col(&|d| d.names.len() as i64),
    ];
    let mut svg = head("Solves and drills per day, full repo history", H);
    panel(
        &mut svg,
        &series[0],
        &series[1],
        LANES[0],
        &format!("per day: solves (blue) + drills (green), stacked; dashed = {MA_DAYS}-day average of the total"),
    );
    panel(
        &mut svg,
        &series[2],
        &series[3],
        LANES[1],
        &format!("distinct per day: problems (blue) + drills (green), stacked; dashed = {MA_DAYS}-day average"),
    );
    let days: Vec<NaiveDate> = rows.iter().map(|r| r.0).collect();
    month_grid(&mut svg, &days, &LANES);
    key(&mut svg, W - MR - 170, LANES[1].1 + 30, SOLVE, "solves");
    key(&mut svg, W - MR - 85, LANES[1].1 + 30, DRILL, "drills");
    svg.push("</svg>".to_string());
    write(&out, &svg);
    let tot: Vec<i64> = series.iter().map(|s| s.iter().sum()).collect();
    println!(
        "wrote {} ({} days: {} solves, {} drills, {} distinct problem-days, {} distinct drill-days)",
        out.display(),
        rows.len(),
        tot[0],
        tot[1],
        tot[2],
        tot[3]
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    fn files(v: &[&str]) -> Vec<String> {
        v.iter().map(|s| s.to_string()).collect()
    }

    #[test]
    fn a_commit_is_a_solve_before_it_is_tooling() {
        assert!(is_solve(&files(&[
            "solved/p1_Two_Sum_2026.mu",
            "utils/x.py"
        ])));
        assert!(!is_solve(&files(&["solved/p1_Two_Sum_FAILED_2026.mu"])));
        assert!(is_tool(&files(&["utils/rs/kg/src/pick.rs"])));
        assert!(is_tool(&files(&["mu/leetmu.py"])));
        assert!(!is_tool(&files(&[
            "README.md",
            "graph/evidence.json",
            "current.py"
        ])));
    }

    #[test]
    fn the_average_covers_the_days_that_exist() {
        let xs = [7, 0, 0, 0, 0, 0, 0, 14];
        let ma = moving_average(&xs);
        assert_eq!(ma[0], 7.0);
        assert_eq!(ma[6], 1.0);
        assert_eq!(ma[7], 2.0);
    }
}
