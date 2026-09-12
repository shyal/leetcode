// kg_residuals - residual diagnostic for the global forgetting curve.
//
//   make residuals             # observed - predicted, grouped by wing and node
//
// For every recall trial (same construction as kg_curve.extract_trials, but
// keeping the node), compute observed - predicted under graph/curve.json.
// If the one-global-law assumption is right, every wing hovers near zero.
// A wing significantly negative at long gaps decays faster than the global
// curve says; a NODE significantly negative while its wing is fine is a
// fission or interference suspect, not a curve problem (README rule 4).
// z per group is sum(obs - p) / sqrt(sum p(1-p)).
//
// Ported from utils/kg/kg_residuals (Python) on 2026-09-12.

use chrono::NaiveDate;
use indexmap::IndexMap;
use kg::ctx::Ctx;
use kg::data::{assist_weight, load_envrc, parse_date, repo_root, Rec};
use regex::Regex;

const NODE_Z_FLAG: f64 = 1.5; // per-node report threshold
const NODE_N_MIN: usize = 5;
const GAP_SPLIT: i64 = 21; // days: short vs long bucket

/// (node, gap_days, success, prior_cleans, prior_struggles, prior_assist)
type Trial = (String, i64, i64, i64, i64, f64);

fn trials_by_node(recs: &[(String, Rec)]) -> Vec<Trial> {
    let ts_re = Regex::new(r"\d{4}_\d{2}_\d{2}T[\d_]+").unwrap();
    let mut events: IndexMap<String, Vec<(String, String, String, String)>> = IndexMap::new();
    for (fname, rec) in recs {
        let ts = ts_re
            .find(fname)
            .map(|m| m.as_str().to_string())
            .unwrap_or_default();
        for (node, verdict) in &rec.moves {
            events.entry(node.clone()).or_default().push((
                rec.date.clone(),
                ts.clone(),
                verdict.clone(),
                rec.assist_for(node).to_string(),
            ));
        }
    }
    let mut out = Vec::new();
    for (node, evs) in events.iter_mut() {
        evs.sort();
        let mut days: IndexMap<String, Vec<(String, String)>> = IndexMap::new();
        for (d, _, v, a) in evs.iter() {
            days.entry(d.clone())
                .or_default()
                .push((v.clone(), a.clone()));
        }
        days.sort_keys();
        let (mut last_clean, mut cleans, mut struggles, mut assisted) =
            (None::<NaiveDate>, 0i64, 0i64, 0.0f64);
        let mut retrieved = false; // an unaided clean so far: the memory exists to test
        for (d, reps) in &days {
            let (verdict, assist) = &reps[0];
            // a trial needs a prior UNAIDED clean: after only walked-through
            // or hinted cleans nothing was retrieved yet, so the next attempt
            // is a first attempt, not a recall
            if retrieved && (verdict == "clean" || verdict == "struggled") && assist != "learning" {
                let gap = (parse_date(d) - last_clean.unwrap()).num_days();
                if gap >= 1 {
                    let success = i64::from(verdict == "clean" && assist == "none");
                    out.push((node.clone(), gap, success, cleans, struggles, assisted));
                }
            }
            for (v, a) in reps {
                if v == "clean" && a != "learning" {
                    cleans += 1;
                    last_clean = Some(parse_date(d));
                    retrieved = retrieved || a == "none";
                } else if v == "struggled" {
                    struggles += 1;
                }
                assisted += assist_weight(a);
            }
        }
    }
    out
}

fn bucket(gap: i64) -> String {
    if gap <= GAP_SPLIT {
        format!("short (<={GAP_SPLIT}d)")
    } else {
        format!("long (>{GAP_SPLIT}d)")
    }
}

/// (n, observed rate, model rate, z)
type Stat = (usize, f64, f64, f64);

fn stats(pairs: &[(f64, f64)]) -> Stat {
    let n = pairs.len();
    let obs = pairs.iter().map(|(s, _)| s).sum::<f64>() / n as f64;
    let exp = pairs.iter().map(|(_, p)| p).sum::<f64>() / n as f64;
    let var: f64 = pairs.iter().map(|(_, p)| p * (1.0 - p)).sum();
    let z = if var > 0.0 {
        pairs.iter().map(|(s, p)| s - p).sum::<f64>() / var.sqrt()
    } else {
        0.0
    };
    (n, obs, exp, z)
}

fn pct(x: f64) -> String {
    format!("{:.0}%", x * 100.0)
}

fn main() {
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let Some(curve) = &ctx.curve else {
        eprintln!("graph/curve.json missing");
        std::process::exit(1);
    };
    let wing = |node: &str| {
        ctx.nodes
            .get(node)
            .and_then(|n| n.group.clone())
            .unwrap_or_else(|| "?".to_string())
    };
    let trials = trials_by_node(&recs);
    let predict = |gap: i64, k: i64, m: i64, x: f64| {
        let s = (curve.a + curve.b * (k as f64).ln_1p() - curve.c * m as f64 - curve.d * x).exp();
        (1.0 - curve.slip) * (1.0 + gap as f64 / s).powf(-curve.beta)
    };

    // wing -> bucket -> [(obs, p)], in first-seen order like the Python dicts
    let mut agg: IndexMap<String, IndexMap<String, Vec<(f64, f64)>>> = IndexMap::new();
    let mut per_node: IndexMap<String, Vec<(f64, f64)>> = IndexMap::new();
    for (node, gap, sf, k, m, x) in &trials {
        let p = predict(*gap, *k, *m, *x);
        agg.entry(wing(node))
            .or_default()
            .entry(bucket(*gap))
            .or_default()
            .push((*sf as f64, p));
        per_node
            .entry(node.clone())
            .or_default()
            .push((*sf as f64, p));
    }

    println!("{} trials against curve.json\n", trials.len());
    println!(
        "{:<18}{:<15}{:>4}{:>7}{:>7}{:>7}",
        "wing", "bucket", "n", "obs", "model", "z"
    );
    let buckets = [bucket(0), bucket(GAP_SPLIT + 1)];
    let mut wings: Vec<&String> = agg.keys().collect();
    let min_z = |w: &String| {
        agg[w]
            .values()
            .map(|ps| stats(ps).3)
            .fold(f64::INFINITY, f64::min)
    };
    wings.sort_by(|a, b| min_z(a).partial_cmp(&min_z(b)).unwrap());
    for w in wings {
        for b in &buckets {
            if let Some(ps) = agg[w].get(b).filter(|ps| !ps.is_empty()) {
                let (n, obs, exp, z) = stats(ps);
                let flag = if z.abs() >= 2.0 { "  <--" } else { "" };
                println!(
                    "{w:<18}{b:<15}{n:>4}{:>7}{:>7}{z:>7.2}{flag}",
                    pct(obs),
                    pct(exp)
                );
            }
        }
    }

    let mut flagged: Vec<(&String, Stat)> = per_node
        .iter()
        .filter(|(_, pairs)| pairs.len() >= NODE_N_MIN && stats(pairs).3.abs() >= NODE_Z_FLAG)
        .map(|(node, pairs)| (node, stats(pairs)))
        .collect();
    if !flagged.is_empty() {
        println!("\nnodes with |z| >= {NODE_Z_FLAG} and n >= {NODE_N_MIN} (fission / interference suspects):");
        flagged.sort_by(|a, b| a.1 .3.partial_cmp(&b.1 .3).unwrap());
        for (node, (n, obs, exp, z)) in flagged {
            println!(
                "  {node:<28}{:<17}n={n:<4}obs={:<5}model={:<5}z={z:+.2}",
                wing(node),
                pct(obs),
                pct(exp)
            );
        }
    }
}
