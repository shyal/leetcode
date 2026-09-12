// kg_solvecost - how long does one rep on a move cost me, and how does that
// fall as i meet the move again? Fits a solve-time model on every timed
// solve and writes graph/solvecost.json, which kg_mock and kg_predict read
// to price each simulated refresh instead of charging a flat 10 minutes.
//
//   kg_solvecost              # refit and print the fit
//   kg_solvecost --if-stale   # refit only when evidence.json is newer
//
// Model, per timed successful solve (minutes from the solve-time trailer,
// kg::git::mined_solve_times):
//
//   ln minutes = a
//              + g_reps  * ln(1 + prior clean reps, averaged over the walk)
//              + g_conn  * (conn - conn_mean)         log2 carriers, averaged
//              + g_len   * ln(walk length)
//              + g_assist * assist weight
//              + kind[Easy | Medium | Hard | drill]
//              + node effect
//
// Exposure (g_reps) and connectivity (g_conn) are the two drivers the README
// regression found; the rest are controls so those two are not credited
// with the difficulty or the drill format. The node effect is the node's
// mean residual shrunk toward zero (k = 3 pseudo-solves).
//
// The consumer (kg::mock::SolveCost) prices a refresh of node n after r
// simulated clean reps as
//   exp(a + g_reps * ln(1 + r) + g_conn * (conn_n - conn_mean) + kind_n + eff_n)
// with kind_n = drill when the node has a bank, else Easy, clamped to
// [MIN_COST, MAX_COST] minutes.
//
// Ported from utils/kg/kg_solvecost (Python) on 2026-09-12.

use std::collections::HashMap;

use indexmap::IndexMap;
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{assist_weight, load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::git::mined_solve_times;
use kg::linalg::{lstsq, round_to};
use kg::mock::SolveCost;
use kg::pyjson;
use kg::status::node_conn;
use serde_json::{json, Map, Value};

const SHRINK: f64 = 3.0;
const MIN_COST: f64 = 1.0;
const MAX_COST: f64 = 40.0;
const KINDS: [&str; 4] = ["Easy", "Medium", "Hard", "drill"];

/// One feature row per timed solve that has an evidence record:
/// (features, ln minutes, moves).
fn rows(
    ctx: &Ctx,
    ev: &Evidence,
    pv: &PView,
    conn: &HashMap<String, f64>,
    conn_mean: f64,
) -> Vec<(Vec<f64>, f64, Vec<String>)> {
    let mut prior_clean: HashMap<String, i64> = HashMap::new();
    let mut out = Vec::new();
    for (key, _d, secs, fname) in mined_solve_times(ctx) {
        let Some(&idx) = ev.by_fname.get(&fname) else {
            continue;
        };
        let rec = ev.rec(idx);
        let moves: Vec<String> = rec.moves.keys().cloned().collect();
        if moves.is_empty() {
            continue;
        }
        let kind = if key.starts_with("d:") {
            "drill".to_string()
        } else {
            pv.map
                .get(&key)
                .and_then(|p| p.difficulty.clone())
                .unwrap_or_default()
        };
        if !KINDS.contains(&kind.as_str()) {
            continue;
        }
        let n = moves.len() as f64;
        let reps = moves
            .iter()
            .map(|m| *prior_clean.get(m).unwrap_or(&0) as f64)
            .sum::<f64>()
            / n;
        let cn = moves
            .iter()
            .map(|m| *conn.get(m).unwrap_or(&0.0))
            .sum::<f64>()
            / n
            - conn_mean;
        let mut x = vec![
            1.0,
            reps.ln_1p(),
            cn,
            n.ln(),
            assist_weight(rec.assist_any()),
        ];
        x.extend(
            KINDS[1..]
                .iter()
                .map(|k| if *k == kind { 1.0 } else { 0.0 }),
        );
        out.push((x, (secs as f64 / 60.0).ln(), moves));
        let level = rec.assist_any().to_string();
        for (m, v) in &rec.moves {
            if v == "clean" && level != "learning" {
                *prior_clean.entry(m.clone()).or_insert(0) += 1;
            }
        }
    }
    out
}

fn fit(ctx: &Ctx, ev: &Evidence) -> Value {
    let pv = PView::new(ctx.evidenced());
    let conn = node_conn(&pv, ctx);
    let conn_mean = if conn.is_empty() {
        0.0
    } else {
        conn.values().sum::<f64>() / conn.len() as f64
    };
    let data = rows(ctx, ev, &pv, &conn, conn_mean);
    if data.len() < 30 {
        eprintln!(
            "only {} timed solves with evidence; not fitting",
            data.len()
        );
        std::process::exit(1);
    }
    let x: Vec<Vec<f64>> = data.iter().map(|(x, _, _)| x.clone()).collect();
    let y: Vec<f64> = data.iter().map(|(_, y, _)| *y).collect();
    let beta = lstsq(&x, &y);
    let resid: Vec<f64> = x
        .iter()
        .zip(&y)
        .map(|(row, yi)| yi - row.iter().zip(&beta).map(|(a, b)| a * b).sum::<f64>())
        .collect();
    let ymean = y.iter().sum::<f64>() / y.len() as f64;
    let ss_res: f64 = resid.iter().map(|r| r * r).sum();
    let ss_tot: f64 = y.iter().map(|v| (v - ymean) * (v - ymean)).sum();
    let r2 = 1.0 - ss_res / ss_tot;

    let names = [
        "a",
        "g_reps",
        "g_conn",
        "g_len",
        "g_assist",
        "kind_Medium",
        "kind_Hard",
        "kind_drill",
    ];
    let mut params = Map::new();
    for (n, b) in names.iter().zip(&beta) {
        params.insert(n.to_string(), json!(round_to(*b, 4)));
    }
    params.insert("kind_Easy".into(), json!(0.0));
    params.insert("conn_mean".into(), json!(round_to(conn_mean, 4)));
    params.insert("min_cost".into(), json!(MIN_COST));
    params.insert("max_cost".into(), json!(MAX_COST));

    let mut per_node: HashMap<&str, Vec<f64>> = HashMap::new();
    for ((_, _, moves), r) in data.iter().zip(&resid) {
        for m in moves {
            per_node.entry(m.as_str()).or_default().push(*r);
        }
    }
    let mut nodes = Map::new();
    for n in ctx.nodes.keys() {
        let rs = per_node.get(n.as_str()).cloned().unwrap_or_default();
        let eff = if rs.is_empty() {
            0.0
        } else {
            rs.iter().sum::<f64>() / (rs.len() as f64 + SHRINK)
        };
        nodes.insert(
            n.clone(),
            json!({
                "eff": round_to(eff, 4),
                "conn": round_to(*conn.get(n).unwrap_or(&0.0), 3),
                "kind": if ctx.has_drill_bank(n) { "drill" } else { "Easy" },
                "n": rs.len(),
            }),
        );
    }
    json!({
        "_comment": "Solve-time model fitted by utils/kg/kg_solvecost. ln minutes = a + g_reps*ln(1+reps) + g_conn*(conn-conn_mean) + g_len*ln(walk) + g_assist*assist + kind + node eff. A refresh of node n after r clean reps costs exp(a + g_reps*ln(1+r) + g_conn*(conn_n-conn_mean) + kind_n + eff_n) minutes, clamped to [min_cost, max_cost]. Delete this file to fall back to the flat 10-minute refresh.",
        "fit": {"n": data.len(), "r2": round_to(r2, 4), "date": ctx.today().format("%Y-%m-%d").to_string()},
        "params": Value::Object(params),
        "nodes": Value::Object(nodes),
    })
}

fn mtime(p: &std::path::Path) -> Option<std::time::SystemTime> {
    std::fs::metadata(p).and_then(|m| m.modified()).ok()
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_solvecost [--if-stale]\n\n  --if-stale  refit only when evidence.json is newer than solvecost.json");
        return;
    }
    let root = repo_root();
    load_envrc(&root);
    let out_path = root.join("graph/solvecost.json");
    let ev_path = root.join("graph/evidence.json");
    if args.iter().any(|a| a == "--if-stale")
        && out_path.exists()
        && mtime(&out_path) >= mtime(&ev_path)
    {
        return;
    }
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let model = fit(&ctx, &ev);
    pyjson::save(&out_path, &model, Some(2)).expect("write graph/solvecost.json");

    let console = Console::full_width();
    let say = |line: &str| {
        let markup = if line.starts_with("fitted") || line.starts_with("wrote") {
            format!("[bold]{line}[/bold]")
        } else if line.starts_with("  ") {
            format!("[dim]{line}[/dim]")
        } else {
            format!("[cyan]{line}[/cyan]")
        };
        console.print(&markup);
    };
    let p = &model["params"];
    let f = |k: &str| p[k].as_f64().unwrap_or(0.0);
    say(&format!(
        "fitted on {} timed solves, r2 {:.3}",
        model["fit"]["n"],
        model["fit"]["r2"].as_f64().unwrap_or(0.0)
    ));
    say(&format!(
        "  exposure  g_reps  {:+.3}  (x{:.2} per doubling of reps)",
        f("g_reps"),
        (f("g_reps") * 2f64.ln()).exp()
    ));
    say(&format!(
        "  connect.  g_conn  {:+.3}  per log2 carrier",
        f("g_conn")
    ));
    say(&format!(
        "  assist    g_assist {:+.3}   walk len g_len {:+.3}",
        f("g_assist"),
        f("g_len")
    ));
    say(&format!(
        "  kind      Medium {:+.2}  Hard {:+.2}  drill {:+.2}  (vs Easy)",
        f("kind_Medium"),
        f("kind_Hard"),
        f("kind_drill")
    ));
    say("refresh cost, minutes, at 0 / 3 / 10 / 30 clean reps:");
    let node_ids: Vec<String> = ctx.nodes.keys().cloned().collect();
    let cost = SolveCost::load(&model, &node_ids).expect("the model just written");
    let index: IndexMap<&str, usize> = node_ids
        .iter()
        .enumerate()
        .map(|(i, n)| (n.as_str(), i))
        .collect();
    for n in [
        "two-pointers",
        "monotonic-stack",
        "sql-window-rank",
        "dp-2d-grid",
        "counter-build",
    ] {
        let Some(&i) = index.get(n) else { continue };
        let cells: Vec<String> = [0, 3, 10, 30]
            .iter()
            .map(|r| format!("{:5.1}", cost.minutes(i, *r)))
            .collect();
        say(&format!("  {n:20} {}", cells.join("  ")));
    }
    say(&format!("wrote {}", out_path.display()));
}
