// kg_queue - the queue `make next` prints, on its own, and its gates.
//
//   kg_queue [--size N]            # the next N problems, rating against elo
//   kg_queue gate [--gap 50]       # ask the judge model which plainer
//                                  # problems should gate the ones rated
//                                  # GAP or more above his elo
//   kg_queue gate --apply          # write those gates into the "after"
//                                  # lists in graph/problems.json
//   kg_queue gate --context        # print the prompt, ask nothing
//
// A gate is a plainer problem that isolates one piece of a harder one, so
// a clean solve of it proves the piece before the harder one is served
// (215 gates 2542). The model reads the target's cached solution
// (.prepare_cache) and picks from every rated problem GATE_MARGIN or more
// below it, by number and title alone. Moves are not sent: the mapped
// moves of 2542 are the brute force, and a move filter never reaches 215
// (experiment of 2026-09-14: solution + all titles found 215, 84, 875
// and 1011; moves alone missed two of three). Its reasons name no
// technique.

use std::collections::HashSet;

use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::git::sleep_state;
use kg::llm::{claude_json, judge_model};
use kg::model::elo_now;
use kg::pyjson::{self, dumps};
use kg::queue::{gap_colour, queue_rows, queue_table, QueueRow, QUEUE_LEN};
use kg::table::{print_table, BoxKind, Table};
use serde_json::{json, Map, Value};

const DEFAULT_GAP: f64 = 50.0;
const GATE_MARGIN: f64 = 150.0;

const SYSTEM_PROMPT: &str = "You maintain the prerequisite edges of one operator's leetcode practice\ngraph. A gate is a plainer problem that isolates one piece of a harder\ntarget problem, so that a clean solve of the gate proves the piece before\nthe target is served. Each target comes with its solution; read it and\nname the pieces yourself.\n\nFor each target, name up to three gates, taken from the candidates only,\none per distinct piece, each isolating that piece as purely as possible.\nNever name a problem that is not in the candidates. Never repeat a problem\nalready in the target's after list.\n\nWriting rules for `why`: one short declarative sentence in plain English.\nRefer to problems by number and title only. Never name a technique, a\nmove, or a data structure.\n\nReply with one JSON object and nothing else:\n{\"gates\": [{\"problem\": \"<target number>\", \"gate\": \"<candidate number>\", \"why\": \"<one sentence>\"}]}\n";

struct Args {
    size: usize,
    gate: bool,
    gap: f64,
    apply: bool,
    context: bool,
    model: String,
}

fn parse_args() -> Args {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    let mut a = Args {
        size: QUEUE_LEN,
        gate: false,
        gap: DEFAULT_GAP,
        apply: false,
        context: false,
        model: judge_model("deepseek"),
    };
    let mut i = 0;
    while i < raw.len() {
        match raw[i].as_str() {
            "-h" | "--help" => {
                println!("usage: kg_queue [--size N] [gate] [--gap N] [--apply] [--context] [--model MODEL]");
                std::process::exit(0);
            }
            "gate" => a.gate = true,
            "--apply" => a.apply = true,
            "--context" => a.context = true,
            "--size" => {
                i += 1;
                a.size = raw
                    .get(i)
                    .and_then(|s| s.parse().ok())
                    .filter(|&n| n > 0)
                    .unwrap_or_else(|| usage("--size takes a positive integer"));
            }
            w if w.starts_with("--size=") => {
                a.size = w["--size=".len()..]
                    .parse()
                    .ok()
                    .filter(|&n| n > 0)
                    .unwrap_or_else(|| usage("--size takes a positive integer"));
            }
            "--gap" => {
                i += 1;
                a.gap = raw
                    .get(i)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or_else(|| usage("--gap takes a number"));
            }
            "--model" => {
                i += 1;
                a.model = raw
                    .get(i)
                    .cloned()
                    .unwrap_or_else(|| usage("--model takes a name"));
            }
            w if w.starts_with("--gap=") => {
                a.gap = w["--gap=".len()..]
                    .parse()
                    .unwrap_or_else(|_| usage("--gap takes a number"));
            }
            w => usage(&format!("unrecognized argument: {w}")),
        }
        i += 1;
    }
    a
}

fn usage(msg: &str) -> ! {
    eprintln!("usage: kg_queue [--size N] [gate] [--gap N] [--apply] [--context] [--model MODEL]");
    eprintln!("kg_queue: error: {msg}");
    std::process::exit(2);
}

fn round_i(x: f64) -> i64 {
    x.round_ties_even() as i64
}

/// The queue rows rated `gap` or more above his elo.
fn targets(rows: &[QueueRow], elo: f64, gap: f64) -> Vec<&QueueRow> {
    rows.iter()
        .filter(|r| r.rating.is_some_and(|x| x - elo >= gap))
        .collect()
}

/// Every rated problem at least GATE_MARGIN below the lowest target, by
/// number, with its title. Drafted and evidenced alike; nothing else
/// filters them.
fn candidates(
    ctx: &Ctx,
    targets: &[&QueueRow],
    ratings: &std::collections::HashMap<String, f64>,
) -> Vec<(String, String, f64)> {
    let ceiling = targets
        .iter()
        .filter_map(|t| t.rating)
        .fold(f64::INFINITY, f64::min)
        - GATE_MARGIN;
    let mut out: Vec<(String, String, f64)> = ratings
        .iter()
        .filter(|(k, r)| **r <= ceiling && !targets.iter().any(|t| &t.pnum == *k))
        .filter_map(|(k, r)| {
            let title = ctx
                .all_problems()
                .get(k)
                .map(|p| p.title.clone())
                .or_else(|| ctx.meta_title(k))?;
            let banned = ctx.all_problems().get(k).is_some_and(|p| p.banned);
            (!banned && !ctx.paid_only(k)).then(|| (k.clone(), title, *r))
        })
        .collect();
    out.sort_by_key(|(k, _, _)| kg::data::pnum_key(k));
    out
}

/// The target's cached solution file (.prepare_cache/<num>.json), or "".
fn solution(ctx: &Ctx, pnum: &str) -> String {
    pyjson::load(&ctx.root.join(".prepare_cache").join(format!("{pnum}.json")))
        .map(|v| kg::data::value_str(&v["solution"]))
        .unwrap_or_default()
}

fn build_context(ctx: &Ctx, rows: &[QueueRow], elo: f64, gap: f64) -> Value {
    let ratings = kg::model::solve_ratings(ctx);
    let ts = targets(rows, elo, gap);
    let target_json: Vec<Value> = ts
        .iter()
        .map(|t| {
            let p = ctx.all_problems().get(&t.pnum);
            json!({
                "problem": t.pnum,
                "title": t.title,
                "rating": t.rating.map(round_i),
                "after": p.map(|p| p.after.clone()).unwrap_or_default(),
                "solution": solution(ctx, &t.pnum),
            })
        })
        .collect();
    let cand_json: Vec<Value> = candidates(ctx, &ts, &ratings)
        .into_iter()
        .map(|(k, title, r)| json!({ "problem": k, "title": title, "rating": round_i(r) }))
        .collect();
    json!({
        "elo": round_i(elo),
        "targets": target_json,
        "candidates": cand_json,
    })
}

struct Gate {
    problem: String,
    gate: String,
    why: String,
}

/// The model's gates, kept only where the target is a target and the gate
/// a candidate it does not already come after.
fn valid_gates(reply: &Value, context: &Value) -> Vec<Gate> {
    let targets: Map<String, Value> = context["targets"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|t| (kg::data::value_str(&t["problem"]), t.clone()))
        .collect();
    let cands: HashSet<String> = context["candidates"]
        .as_array()
        .into_iter()
        .flatten()
        .map(|c| kg::data::value_str(&c["problem"]))
        .collect();
    let mut seen: HashSet<(String, String)> = HashSet::new();
    reply["gates"]
        .as_array()
        .into_iter()
        .flatten()
        .filter_map(|g| {
            let problem = kg::data::value_str(&g["problem"]);
            let gate = kg::data::value_str(&g["gate"]);
            let t = targets.get(&problem)?;
            let already = t["after"]
                .as_array()
                .into_iter()
                .flatten()
                .any(|a| kg::data::value_str(a) == gate);
            if !cands.contains(&gate) || already || !seen.insert((problem.clone(), gate.clone())) {
                return None;
            }
            Some(Gate {
                problem,
                gate,
                why: kg::data::value_str(&g["why"]),
            })
        })
        .collect()
}

/// Append each gate to its target's "after" list in graph/problems.json.
fn apply(ctx: &Ctx, gates: &[Gate]) -> std::io::Result<usize> {
    let mut written = 0;
    for g in gates {
        let after = ctx
            .all_problems()
            .get(&g.problem)
            .map(|p| p.after.clone())
            .unwrap_or_default();
        let mut merged: Vec<String> = after;
        if merged.contains(&g.gate) {
            continue;
        }
        merged.push(g.gate.clone());
        merged.sort_by_key(|p| kg::data::pnum_key(p));
        pyjson::save_problem_entry(&ctx.root, &g.problem, &json!({ "after": merged }))?;
        written += 1;
    }
    Ok(written)
}

fn gate_table(
    ctx: &Ctx,
    gates: &[Gate],
    ratings: &std::collections::HashMap<String, f64>,
    elo: f64,
) -> Table {
    let mut table = Table::plain(
        &["Target", "Gate", "Rating", "Why"],
        Some("gates"),
        BoxKind::Rounded,
    );
    let title = |p: &str| {
        ctx.all_problems()
            .get(p)
            .map(|x| x.title.clone())
            .unwrap_or_default()
    };
    for g in gates {
        let rating = ratings
            .get(&g.gate)
            .map(|r| {
                let c = gap_colour(r - elo);
                format!("[{c}]{:.0}[/{c}]", r)
            })
            .unwrap_or_else(|| "-".into());
        table.add_row(&[
            format!("{}. {}", g.problem, title(&g.problem)),
            format!("{}. {}", g.gate, title(&g.gate)),
            rating,
            g.why.clone(),
        ]);
    }
    table
}

fn main() {
    let args = parse_args();
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());
    let asleep = sleep_state(&ctx, &pv, &ev);
    let console = Console::full_width();

    if !args.gate {
        match queue_table(&ctx, &pv, &ev, &asleep, args.size) {
            Some(t) => print_table(&console, &t),
            None => console.print("[dim]the queue is empty[/dim]"),
        }
        return;
    }

    let elo = elo_now(&ctx, &ev);
    let rows = queue_rows(&ctx, &pv, &ev, &asleep, args.size);
    let context = build_context(&ctx, &rows, elo, args.gap);
    if args.context {
        println!("{}", dumps(&context, Some(1)));
        return;
    }
    let n_targets = context["targets"].as_array().map_or(0, Vec::len);
    if n_targets == 0 {
        console.print(&format!(
            "[dim]nothing in the queue is rated {:.0} or more above your elo ({:.0})[/dim]",
            args.gap, elo
        ));
        return;
    }
    console.print(&format!(
        "[dim]{n_targets} target{} rated {:.0}+ above elo {:.0}, {} candidate{} - asking {}[/dim]",
        if n_targets == 1 { "" } else { "s" },
        args.gap,
        elo,
        context["candidates"].as_array().map_or(0, Vec::len),
        if context["candidates"].as_array().map_or(0, Vec::len) == 1 {
            ""
        } else {
            "s"
        },
        args.model
    ));
    let reply = match claude_json(&dumps(&context, Some(1)), SYSTEM_PROMPT, &args.model, 2) {
        Ok(v) => v,
        Err(e) => {
            console.print(&format!("[red]{e}[/red]"));
            std::process::exit(1);
        }
    };
    let gates = valid_gates(&reply, &context);
    if gates.is_empty() {
        console.print("[yellow]the model named no usable gate[/yellow]");
        return;
    }
    let ratings = kg::model::solve_ratings(&ctx);
    print_table(&console, &gate_table(&ctx, &gates, &ratings, elo));
    if args.apply {
        match apply(&ctx, &gates) {
            Ok(n) => console.print(&format!(
                "[green]{n} gate{} written to graph/problems.json[/green]",
                if n == 1 { "" } else { "s" }
            )),
            Err(e) => {
                console.print(&format!("[red]{e}[/red]"));
                std::process::exit(1);
            }
        }
    } else {
        console.print("[dim]make queue gate -- --apply writes them into the after lists[/dim]");
    }
}
