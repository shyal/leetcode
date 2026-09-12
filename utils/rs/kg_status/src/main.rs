// kg_status - graph health report.
//
//   kg_status            # counts, then the named grid by group
//   kg_status --summary  # counts only (what `make` on master prints)
//
// Days-to-all-green is remaining non-SOLID / nodes-turned-SOLID per day
// over the last 7 calendar days (including today).
//
// Colors: green = SOLID, yellow = STALE, red = FRAGILE, dim = MISSING.
// Derivation lives in kg::status::node_status; nothing is stored.
//
// Ownership is the graded axis under the labels (kg::status::node_axes):
// the weaker of the curve's memory and breadth, distinct real problems the
// move was executed on unaided. The report prints its mean and a
// four-bucket histogram; the grid prints each node's degree after its id.
// A graph that is all green with a mean of 0.6 is remembered, not yet
// owned.
//
// Ported from utils/kg/kg_status (Python) on 2026-09-12.

use std::collections::HashMap;

use chrono::{Duration, NaiveDate};
use kg::console::{Console, Style};
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::status::{
    input_tree, node_axes, node_status, node_status_cut, Status, FRAGILE, MISSING, SOLID, STALE,
};
use kg::table::{print_table, Column, Justify, Table};

const ORDER: [Status; 4] = [SOLID, STALE, FRAGILE, MISSING];

fn style(s: Status) -> &'static str {
    match s {
        SOLID => "green",
        STALE => "yellow",
        FRAGILE => "red",
        MISSING => "dim",
    }
}

fn fading_count(ctx: &Ctx, ev: &Evidence, today: NaiveDate) -> usize {
    let soon = today + Duration::days(7);
    ctx.nodes
        .keys()
        .filter(|n| {
            node_status(ctx, n, ev, today).0 == SOLID && node_status(ctx, n, ev, soon).0 != SOLID
        })
        .count()
}

/// Mean nodes that flipped to SOLID per calendar day over the last `days`.
fn greened_per_day(ctx: &Ctx, ev: &Evidence, days: i64, today: NaiveDate) -> f64 {
    let mut greened = 0;
    for i in (0..days).rev() {
        let day = today - Duration::days(i);
        let before = (day - Duration::days(1)).format("%Y-%m-%d").to_string();
        let after = day.format("%Y-%m-%d").to_string();
        for n in ctx.nodes.keys() {
            if node_status_cut(ctx, n, ev, &before, day).0 != SOLID
                && node_status_cut(ctx, n, ev, &after, day).0 == SOLID
            {
                greened += 1;
            }
        }
    }
    greened as f64 / days as f64
}

/// Human line for days-to-all-green at the trailing pace.
fn eta_line(remaining: usize, pace: f64) -> String {
    if remaining == 0 {
        return "all nodes green".to_string();
    }
    if pace <= 0.0 {
        return format!("{remaining} to green · no greening in the last 7 days");
    }
    let days = (remaining as f64 / pace).ceil() as i64;
    let pace_txt = format!("{pace:.1} greened/day (last 7 days)");
    if days <= 1 {
        return format!("all green later today · {pace_txt}");
    }
    format!("~{days} days to all green · {pace_txt}")
}

const DEGREE_BUCKETS: [&str; 4] = ["0-.25", ".25-.5", ".5-.75", ".75-1"];

/// Index into DEGREE_BUCKETS; 1.0 lands in the top bucket.
fn degree_bucket(degree: f64) -> usize {
    ((degree * 4.0) as i64).clamp(0, 3) as usize
}

/// A node's degree beside its id in the grid: 1 when owned in full, else
/// the fraction without its leading zero (.50).
fn degree_label(degree: f64) -> String {
    if kg::table::py_round(degree * 100.0) / 100.0 >= 1.0 {
        return "1".to_string();
    }
    format!("{degree:.2}")[1..].to_string()
}

/// Two lines: mean degree with the count below 0.5, then the histogram.
fn ownership_lines(degrees: &[f64]) -> Vec<String> {
    if degrees.is_empty() {
        return vec![];
    }
    let mean = degrees.iter().sum::<f64>() / degrees.len() as f64;
    let low = degrees.iter().filter(|v| **v < 0.5).count();
    let mut hist = [0usize; 4];
    for v in degrees {
        hist[degree_bucket(*v)] += 1;
    }
    let cells: Vec<String> = (0..4)
        .map(|i| format!("{}: {}", DEGREE_BUCKETS[i], hist[i]))
        .collect();
    vec![
        format!("ownership: mean {mean:.2} · {low} below 0.5"),
        format!("[dim]{}[/dim]", cells.join("  ")),
    ]
}

fn print_report(
    console: &Console,
    counts: &HashMap<Status, usize>,
    n_problems: usize,
    n_fading: usize,
    remaining: usize,
    pace: f64,
    degrees: &[f64],
) {
    let total: usize = counts.values().sum();
    console.print(&format!("\n[bold]Technique graph[/bold] · {total} nodes"));
    let mut table = Table::bare(&["swatch", "status", "n", "pct"], false, 2);
    table.column(
        2,
        Column {
            justify: Justify::Right,
            ..Column::default()
        },
    );
    table.column(
        3,
        Column {
            justify: Justify::Right,
            style: Style::parse("dim"),
            ..Column::default()
        },
    );
    for status in ORDER {
        let n = *counts.get(&status).unwrap_or(&0);
        let pct = if total > 0 {
            format!(
                "{}%",
                kg::table::py_round(100.0 * n as f64 / total as f64) as i64
            )
        } else {
            "-".to_string()
        };
        let st = style(status);
        table.add_row(&[
            format!("[{st}]■[/{st}]"),
            format!("[{st}]{status}[/{st}]"),
            n.to_string(),
            pct,
        ]);
    }
    print_table(console, &table);
    let mut extras = vec![format!("{n_problems} problems mapped")];
    if n_fading > 0 {
        extras.push(format!("{n_fading} fade within 7 days"));
    }
    console.print(&format!("[dim]{}[/dim]", extras.join(" · ")));
    console.print(&eta_line(remaining, pace));
    for line in ownership_lines(degrees) {
        console.print(&line);
    }
}

fn print_grid(
    console: &Console,
    groups: &[(String, Vec<(String, Status)>)],
    degrees: &HashMap<String, f64>,
) {
    let mut table = Table::bare(&["group", "nodes"], false, 1);
    table.title = Some("by group".to_string());
    table.title_style = Style::parse("dim");
    table.column(
        0,
        Column {
            style: Style::parse("bold"),
            no_wrap: true,
            ..Column::default()
        },
    );
    for (group, members) in groups {
        let line: Vec<String> = members
            .iter()
            .map(|(id, status)| {
                let st = style(*status);
                format!("[{st}]{id}[/{st}][dim]:{}[/dim]", degree_label(degrees[id]))
            })
            .collect();
        table.add_row(&[group.clone(), line.join("  ")]);
    }
    console.blank();
    print_table(console, &table);
}

fn print_sleep(console: &Console, ctx: &Ctx, pv: &PView, ev: &Evidence, today: NaiveDate) {
    let recs = kg::git::sleep_records(ctx, pv, ev);
    if recs.is_empty() {
        return;
    }
    let by_pnum: HashMap<&str, &kg::git::SleepRec> =
        recs.iter().map(|r| (r.pnum.as_str(), r)).collect();
    for p in kg::git::sleep_state(ctx, pv, ev) {
        let rec = by_pnum[p.as_str()];
        let moves = pv.map.get(&p).map(|x| x.moves.clone()).unwrap_or_default();
        let mut rusty: Vec<String> = input_tree(&moves, &ctx.nodes)
            .into_iter()
            .filter(|n| node_status(ctx, n, ev, today).0 != SOLID)
            .collect();
        rusty.sort();
        let cycles = if rec.cycles > 1 {
            format!(" (slept x{})", rec.cycles)
        } else {
            String::new()
        };
        let ground = if rusty.is_empty() {
            "ground solid, simmering".to_string()
        } else {
            format!("kg_next is warming: {}", rusty.join(", "))
        };
        console.print(&format!(
            "💤 [bold]{p}. {}[/bold]{cycles} parked - {ground} - make wake {p} when you choose",
            rec.title
        ));
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let summary = args.iter().any(|a| a == "--summary");
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_status [--summary]\n\nGraph health report.\n\n  --summary  counts only, no named grid");
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let pv = PView::new(ctx.evidenced());
    let ev = Evidence::new(recs);
    let console = Console::full_width();

    let mut groups: Vec<(String, Vec<(String, Status)>)> = Vec::new();
    let mut counts: HashMap<Status, usize> = HashMap::new();
    let mut degrees: HashMap<String, f64> = HashMap::new();
    let mut degree_list: Vec<f64> = Vec::new();
    for (id, node) in &ctx.nodes {
        let ax = node_axes(&ctx, id, &ev, &pv, today);
        let group = node.group.clone().unwrap_or_else(|| "None".to_string());
        match groups.iter_mut().find(|(g, _)| *g == group) {
            Some((_, members)) => members.push((id.clone(), ax.status)),
            None => groups.push((group, vec![(id.clone(), ax.status)])),
        }
        *counts.entry(ax.status).or_insert(0) += 1;
        degrees.insert(id.clone(), ax.degree);
        degree_list.push(ax.degree);
    }
    let remaining = [STALE, FRAGILE, MISSING]
        .iter()
        .map(|s| counts.get(s).unwrap_or(&0))
        .sum();
    let pace = greened_per_day(&ctx, &ev, 7, today);
    print_report(
        &console,
        &counts,
        pv.map.len(),
        fading_count(&ctx, &ev, today),
        remaining,
        pace,
        &degree_list,
    );
    if !summary {
        print_grid(&console, &groups, &degrees);
    }
    print_sleep(&console, &ctx, &pv, &ev, today);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn labels_and_buckets() {
        assert_eq!(degree_label(1.0), "1");
        assert_eq!(degree_label(0.996), "1");
        assert_eq!(degree_label(0.5), ".50");
        assert_eq!(degree_label(0.0), ".00");
        assert_eq!(degree_bucket(1.0), 3);
        assert_eq!(degree_bucket(0.24), 0);
        assert_eq!(degree_bucket(0.25), 1);
    }

    #[test]
    fn eta_lines() {
        assert_eq!(eta_line(0, 1.0), "all nodes green");
        assert_eq!(
            eta_line(3, 0.0),
            "3 to green · no greening in the last 7 days"
        );
        assert_eq!(
            eta_line(1, 2.0),
            "all green later today · 2.0 greened/day (last 7 days)"
        );
        assert_eq!(
            eta_line(4, 0.3),
            "~14 days to all green · 0.3 greened/day (last 7 days)"
        );
    }
}
