// kg_predict - simulate the road to interview-ready under the fitted curve.
//
//   make predict 2             # 2 hours/day; any hours value works (e.g. 1.5)
//   kg_predict --json          # the headline dates as one JSON object
//   kg_predict --history-json  # the projection replayed for every day so far
//
// Day-by-day simulation of how the picker would spend your hours:
// consolidate fragile moves, acquire missing ones, re-solve whatever the
// personal forgetting curve (graph/curve.json) says is about to go stale,
// and spend the rest on new mediums (which refresh the least-repped moves
// they walk). The taxonomy grows by fission as mediums accumulate. Ready =
// the graph fully solid + MEDIUM_TARGET distinct mediums banked, then
// POLISH_DAYS of timed sets and mocks on top. Solve costs are measured from
// your own git history, not assumed.
//
// What this does NOT model: system design or behavioral prep, and - the
// dominant real-world variable - whether the hours actually happen daily.
// The two long ambers in your history moved dates more than any parameter
// here. Constants below are editable and printed with the result.
//
// Ported from utils/kg/kg_predict (Python) on 2026-09-12.

use std::collections::HashSet;

use chrono::{Duration, NaiveDate};
use kg::ctx::Ctx;
use kg::data::{load_envrc, parse_date, read_json, repo_root};
use kg::evidence::Evidence;
use kg::mock::SolveCost;
use kg::pyjson::{dumps, g};
use kg::status::{node_status_cut, FRAGILE, MISSING};
use regex::Regex;
use serde_json::json;

const MEDIUM_TARGET: usize = 220; // distinct mediums banked = broad interview coverage
const POLISH_DAYS: i64 = 35; // timed sets, hards, mocks after the grind
const MAINT_COST: f64 = 10.0; // minutes to re-solve a known carrier, when
                              // graph/solvecost.json has no per-node price
const CONSOLIDATE_COST: f64 = 18.0; // minutes to fix a fragile move on a fresh carrier
const ACQUIRE_COST: f64 = 30.0; // minutes to learn a missing move (drill + carrier)
const MEDIUM_OVERHEAD: f64 = 1.3; // review/struggle amortization on top of median time
const MEDIUM_FLOOR: f64 = 15.0; // minutes a practiced medium converges toward
const NODES_PER_MEDIUM: usize = 3; // moves a medium's walk refreshes
const FISSION_EVERY: usize = 8; // mediums per newly split node, up to NODE_CAP
const NODE_CAP: usize = 95;

/// Every timed Medium solve in the git log, as (commit date, number,
/// minutes). Parsed once so banked counts can be asked for any as-of date.
fn medium_log(ctx: &Ctx) -> Vec<(String, String, f64)> {
    let log = std::process::Command::new("git")
        .args(["log", "--format=%ad|%s|%b~~~", "--date=short"])
        .current_dir(&ctx.root)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).into_owned())
        .unwrap_or_default();
    let re = Regex::new(r"(?s)\|(\d+)\. .*?solve time: (\d+)m (\d+)s").unwrap();
    let mut entries = Vec::new();
    for block in log.split("~~~") {
        let block = block.trim();
        let Some(m) = re.captures(block) else {
            continue;
        };
        let num = m[1].to_string();
        let mins: f64 = m[2].parse::<f64>().unwrap() + m[3].parse::<f64>().unwrap() / 60.0;
        if ctx.meta_difficulty(&num) == "Medium" {
            let when: String = block.chars().take(10).collect();
            entries.push((when, num, mins));
        }
    }
    entries
}

/// statistics.median
fn median(v: &mut [f64]) -> f64 {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = v.len();
    if n % 2 == 1 {
        v[n / 2]
    } else {
        (v[n / 2 - 1] + v[n / 2]) / 2.0
    }
}

fn measured_times(entries: &[(String, String, f64)], as_of: &str) -> (usize, f64) {
    let mut mediums: HashSet<&str> = HashSet::new();
    let mut times = Vec::new();
    for (when, num, mins) in entries {
        if when.as_str() > as_of {
            continue;
        }
        mediums.insert(num);
        if *mins < 120.0 {
            times.push(*mins);
        }
    }
    let med = if times.len() >= 5 {
        median(&mut times)
    } else {
        25.0
    };
    (mediums.len(), med)
}

#[derive(Clone)]
struct NodeSim {
    /// the node index in the cost model; None for a node born by fission
    id: Option<usize>,
    reps: i64,
    gap: i64,
    pending: f64,
}

struct Params {
    a: f64,
    b: f64,
    beta: f64,
}

fn recall(p: &Params, n: &NodeSim) -> f64 {
    let s = (p.a + p.b * (n.reps as f64).ln_1p())
        .exp()
        .clamp(7.0, 3650.0);
    (1.0 + n.gap as f64 / s).powf(-p.beta)
}

/// Per-node refresh price from graph/solvecost.json (kg_solvecost), which
/// falls with the node's simulated rep count; flat MAINT_COST without it.
fn maint_cost(cost: Option<&SolveCost>, n: &NodeSim) -> f64 {
    match (cost, n.id) {
        (Some(c), Some(i)) => c.minutes(i, n.reps),
        (Some(_), None) => 10.0,
        (None, _) => MAINT_COST,
    }
}

/// (days, day the graph lit, maintenance minutes per day)
fn simulate(
    state: &mut Vec<NodeSim>,
    mediums_needed: usize,
    medium_median: f64,
    hours: f64,
    p: &Params,
    target: f64,
    cost: Option<&SolveCost>,
) -> (i64, Option<i64>, Vec<f64>) {
    let (mut day, mut done_mediums, mut lit_day) = (0i64, 0usize, None);
    let mut maint_minutes = Vec::new();
    while day < 3650 {
        day += 1;
        let mut budget = hours * 60.0;
        for n in state.iter_mut() {
            n.gap += 1;
        }
        let mut spent_maint = 0.0;
        // 1. one-off repairs: fragile consolidations, then missing acquisitions
        let mut order: Vec<usize> = (0..state.len()).collect();
        order.sort_by(|a, b| state[*a].pending.partial_cmp(&state[*b].pending).unwrap());
        for i in order {
            let n = &mut state[i];
            if n.pending > 0.0 && budget >= n.pending {
                budget -= n.pending;
                spent_maint += n.pending;
                n.pending = 0.0;
                n.gap = 0;
                n.reps += 1;
            }
        }
        // 2. curve-driven maintenance, most-faded first
        let mut order: Vec<usize> = (0..state.len())
            .filter(|i| state[*i].reps != 0 && state[*i].pending == 0.0)
            .collect();
        order.sort_by(|a, b| {
            recall(p, &state[*a])
                .partial_cmp(&recall(p, &state[*b]))
                .unwrap()
        });
        for i in order {
            let c = maint_cost(cost, &state[i]);
            if recall(p, &state[i]) >= target || budget < c {
                break;
            }
            budget -= c;
            spent_maint += c;
            state[i].gap = 0;
            state[i].reps += 1;
        }
        maint_minutes.push(spent_maint);
        // 3. new mediums with whatever remains
        let mut c =
            MEDIUM_FLOOR.max(medium_median * MEDIUM_OVERHEAD * 0.995f64.powi(done_mediums as i32));
        while budget >= c && done_mediums < mediums_needed {
            budget -= c;
            done_mediums += 1;
            let mut order: Vec<usize> = (0..state.len())
                .filter(|i| state[*i].pending == 0.0)
                .collect();
            order.sort_by_key(|i| (state[*i].reps, -state[*i].gap));
            for i in order.into_iter().take(NODES_PER_MEDIUM) {
                state[i].gap = 0;
                state[i].reps += 1;
            }
            if done_mediums % FISSION_EVERY == 0 && state.len() < NODE_CAP {
                state.push(NodeSim {
                    id: None,
                    reps: 1,
                    gap: 0,
                    pending: 0.0,
                });
            }
            // the Python recomputes the cost only per day; keep that
            let _ = &mut c;
        }
        let graph_lit = state
            .iter()
            .all(|n| n.pending == 0.0 && n.reps != 0 && recall(p, n) >= target);
        if graph_lit && lit_day.is_none() {
            lit_day = Some(day);
        }
        if graph_lit && done_mediums >= mediums_needed {
            break;
        }
    }
    (day, lit_day, maint_minutes)
}

/// Node state as of a day: reps, days-since-clean, pending one-off cost
/// (fragile/missing), from the evidence dated on or before it.
fn node_state(ctx: &Ctx, ev: &Evidence, as_of: NaiveDate) -> Vec<NodeSim> {
    let cut = as_of.format("%Y-%m-%d").to_string();
    ctx.nodes
        .keys()
        .enumerate()
        .map(|(i, nid)| {
            let (status, last) = node_status_cut(ctx, nid, ev, &cut, as_of);
            let cleans = ev
                .node_entries(nid)
                .iter()
                .filter(|e| e.verdict == "clean" && ev.rec(e.idx).date.as_str() <= cut.as_str())
                .count() as i64;
            let gap = last.map(|l| (as_of - l).num_days()).unwrap_or(0);
            let pending = if status == FRAGILE {
                CONSOLIDATE_COST
            } else if status == MISSING {
                ACQUIRE_COST
            } else {
                0.0
            };
            NodeSim {
                id: Some(i),
                reps: cleans.max(0),
                gap,
                pending,
            }
        })
        .collect()
}

fn projection(
    run_date: NaiveDate,
    hours: f64,
    day: i64,
    lit_day: Option<i64>,
) -> serde_json::Value {
    json!({
        "run_date": run_date.format("%Y-%m-%d").to_string(),
        "hours": hours,
        "ready": (run_date + Duration::days(day + POLISH_DAYS)).format("%Y-%m-%d").to_string(),
        "days": day + POLISH_DAYS,
        "graph_lit": (run_date + Duration::days(lit_day.unwrap_or(day))).format("%Y-%m-%d").to_string(),
    })
}

fn main() {
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let json_mode = argv.iter().any(|a| a == "--json");
    let history_mode = argv.iter().any(|a| a == "--history-json");
    let hours: f64 = argv
        .iter()
        .find(|a| !a.starts_with("--"))
        .map(|a| a.parse().expect("hours"))
        .unwrap_or(2.0);
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let today = ctx.today();
    let curve = ctx.curve.as_ref().expect("graph/curve.json");
    let p = Params {
        a: curve.a,
        b: curve.b,
        beta: curve.beta,
    };
    let target = curve.target_retention;
    let node_ids: Vec<String> = ctx.nodes.keys().cloned().collect();
    let cost = read_json(&ctx.graph_dir().join("solvecost.json"))
        .and_then(|v| SolveCost::load(&v, &node_ids));
    let mediums = medium_log(&ctx);

    // --history-json: replay the projection for every day since the first
    // evidence record, from the evidence and git log visible on that day.
    // Feeds the README's "Projected Ready Dates Over Time" chart.
    if history_mode {
        let Some(first) = ev.recs.iter().map(|(_, r)| r.date.as_str()).min() else {
            println!("[]");
            return;
        };
        let mut out = Vec::new();
        let mut d = parse_date(first);
        while d <= today {
            let d_iso = d.format("%Y-%m-%d").to_string();
            let (banked, med) = measured_times(&mediums, &d_iso);
            let needed = MEDIUM_TARGET.saturating_sub(banked);
            let mut state = node_state(&ctx, &ev, d);
            let (day, lit_day, _) =
                simulate(&mut state, needed, med, hours, &p, target, cost.as_ref());
            out.push(projection(d, hours, day, lit_day));
            d += Duration::days(1);
        }
        println!("{}", dumps(&serde_json::Value::Array(out), None));
        return;
    }

    let today_iso = today.format("%Y-%m-%d").to_string();
    let (mediums_banked, medium_median) = measured_times(&mediums, &today_iso);
    let mediums_needed = MEDIUM_TARGET.saturating_sub(mediums_banked);
    let mut state = node_state(&ctx, &ev, today);
    let (day, lit_day, maint_minutes) = simulate(
        &mut state,
        mediums_needed,
        medium_median,
        hours,
        &p,
        target,
        cost.as_ref(),
    );
    let ready = today + Duration::days(day + POLISH_DAYS);
    if json_mode {
        println!("{}", dumps(&projection(today, hours, day, lit_day), None));
        return;
    }
    println!("at {}h/day, every day:", g(hours));
    println!(
        "  graph fully lit          ~ {}",
        today + Duration::days(lit_day.unwrap_or(day))
    );
    println!(
        "  {mediums_needed} new mediums banked   ~ {}   (credit for {mediums_banked} already solved, median {medium_median:.0}m)",
        today + Duration::days(day)
    );
    println!(
        "  + {POLISH_DAYS}d timed sets/mocks -> interview-ready ≈ {}  ({} days)",
        ready.format("%-d %b %Y"),
        day + POLISH_DAYS
    );
    let mean = |v: &[f64]| v.iter().sum::<f64>() / v.len() as f64;
    let early = mean(&maint_minutes[..maint_minutes.len().min(14)]);
    let late = mean(&maint_minutes[maint_minutes.len().saturating_sub(14)..]);
    println!(
        "  maintenance load: {early:.0}m/day first fortnight -> {late:.0}m/day last (the curve compounds; upkeep shrinks as reps stack)"
    );
    println!(
        "  taxonomy grows {} -> {} nodes by fission along the way",
        ctx.nodes.len(),
        state.len()
    );
    println!(
        "assumes: coding rounds only (no system design), and the hours actually happen — history says lapses, not pace, move this date."
    );
}
