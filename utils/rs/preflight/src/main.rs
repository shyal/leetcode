// preflight v2 - prerequisite audit as a deterministic graph join.
//
// moves(problem) come from graph/problems.json; mastery status is derived
// from graph/evidence.json dates. No LLM call at all for known problems
// (milliseconds). Unknown problems trigger ONE small claude call (problem +
// taxonomy only, no solve history) and the result is cached back into
// problems.json.
//
// Verdict: READY when at most one move is non-SOLID (that move is the
// training target). Hards are summits: READY only when EVERY move in the
// walk is SOLID - rusty gear stays at basecamp. Otherwise PREP FIRST, with
// one prep step per weak move: STALE -> spaced re-solve of its most recent
// carrier; FRAGILE/MISSING -> the node's micro-drill.
//
// Ported from utils/kg/preflight (Python) on 2026-09-12.

use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root, Problem};
use kg::evidence::Evidence;
use kg::llm::claude_json;
use kg::pyjson;
use kg::status::{latest_carrier, node_status, Status, FRAGILE, MISSING, SOLID, STALE};
use kg::table::{print_table, Table};
use serde_json::{json, Map, Value};

fn style(s: Status) -> &'static str {
    match s {
        SOLID => "green",
        STALE => "yellow",
        FRAGILE => "orange3",
        MISSING => "red",
    }
}

/// kg_lib.taxonomy_summary: compact node list for prompts.
fn taxonomy_summary(ctx: &Ctx) -> String {
    ctx.nodes
        .values()
        .map(|n| format!("- {}: {}", n.id, n.desc))
        .collect::<Vec<_>>()
        .join("\n")
}

/// (moves, title, the entry's difficulty/banned/note) for the key: a mapped
/// problem, a title fragment, or one claude call cached into problems.json.
fn resolve_moves(
    console: &Console,
    ctx: &Ctx,
    pv: &PView,
    key: &str,
) -> (Vec<String>, String, Problem) {
    // an entry with an EMPTY walk is a withdrawn mapping, not a mapped
    // problem: a bad edge was pulled and the walk still has to be re-derived
    if let Some(p) = pv.map.get(key).filter(|p| !p.moves.is_empty()) {
        return (p.moves.clone(), p.title.clone(), p.clone());
    }
    let lower = key.to_lowercase();
    for p in pv.map.values() {
        if p.title.to_lowercase().contains(&lower) && !p.moves.is_empty() {
            return (p.moves.clone(), p.title.clone(), p.clone());
        }
    }
    console.print("[dim]Problem not in graph/problems.json — one claude call to map it (cached after)...[/dim]");
    let system = format!(
        "You are mapping a LeetCode problem onto a fixed taxonomy of atomic technique moves.\n\nTaxonomy (use ONLY these ids):\n{}\n\nDetermine the canonical clean solution for the problem, then output STRICT JSON, nothing else:\n{{\"title\": \"<full problem title>\", \"difficulty\": \"Easy|Medium|Hard\", \"moves\": [\"<node-id>\", ...], \"unmapped\": [\"<short description of any required move with no matching node>\"]}}\n\nList every move a candidate must execute, including foundational micro-moves (algebra steps, idioms). Do not explain the solution.",
        taxonomy_summary(ctx)
    );
    let result = match claude_json(&format!("LeetCode problem: {key}"), &system, "sonnet", 2) {
        Ok(v) => v,
        Err(e) => {
            console.print(&format!("[red]{e}[/red]"));
            std::process::exit(1);
        }
    };
    let moves: Vec<String> = result["moves"]
        .as_array()
        .map(|a| a.iter().map(kg::data::value_str).collect())
        .unwrap_or_default();
    let title = result
        .get("title")
        .and_then(Value::as_str)
        .unwrap_or(key)
        .to_string();
    let difficulty = result
        .get("difficulty")
        .and_then(Value::as_str)
        .unwrap_or("")
        .to_string();
    // merge over any withdrawn entry rather than replacing it: alt_walks
    // recorded against the old walk are evidence, and the re-derive must not
    // eat them
    let mut entry = Map::new();
    entry.insert("title".into(), json!(title));
    entry.insert("difficulty".into(), json!(difficulty));
    entry.insert("moves".into(), json!(moves));
    if let Some(un) = result
        .get("unmapped")
        .and_then(Value::as_array)
        .filter(|a| !a.is_empty())
    {
        entry.insert("unmapped".into(), Value::Array(un.clone()));
        console.print(&format!(
            "[orange3]Proposed new nodes (review!): {}[/orange3]",
            kg::pyjson::dumps(&Value::Array(un.clone()), None).replace('"', "'")
        ));
    }
    pyjson::save_problem_entry(&ctx.root, key, &Value::Object(entry))
        .expect("write graph/problems.json");
    let meta = Problem {
        title: title.clone(),
        difficulty: Some(difficulty),
        moves: moves.clone(),
        ..pv.map.get(key).cloned().unwrap_or_default()
    };
    (moves, title, meta)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.is_empty() || args.iter().any(|a| a == "-h" || a == "--help") {
        eprintln!("usage: preflight problem [problem ...]\n\n  problem  problem number or title, e.g. 1 or \"Two Sum\"");
        std::process::exit(if args.is_empty() { 2 } else { 0 });
    }
    let key = args.join(" ").trim().trim_end_matches('.').to_string();
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());
    let console = Console::full_width();

    let (moves, title, meta) = resolve_moves(&console, &ctx, &pv, &key);
    if meta.banned {
        console.print("[bold red]⛔ BANNED — never offered as a carrier (busywork/quality blacklist)[/bold red]");
    }
    if let Some(note) = meta.note.as_deref().filter(|n| !n.is_empty()) {
        console.print(&format!("[yellow]⚠ {note}[/yellow]"));
    }
    let mut table = Table::rich_default(
        &["Move", "Status", "Last evidence"],
        Some(&format!("Preflight: {key}. {title}")),
    );
    let mut weak: Vec<(String, Status)> = Vec::new();
    for mv in &moves {
        if !ctx.nodes.contains_key(mv) {
            console.print(&format!(
                "[red]Unknown node id in problems.json: {mv}[/red]"
            ));
            continue;
        }
        let (status, when) = node_status(&ctx, mv, &ev, today);
        if status != SOLID {
            weak.push((mv.clone(), status));
        }
        let carrier = latest_carrier(&ev, mv);
        let last = match (carrier, when) {
            (Some((_, fname, problem)), Some(w)) => format!("{} ({w})", problem.unwrap_or(fname)),
            _ => "—".to_string(),
        };
        table.add_row(&[
            mv.clone(),
            format!("[{0}]{status}[/{0}]", style(status)),
            last,
        ]);
    }
    print_table(&console, &table);

    let is_hard = meta.difficulty.as_deref() == Some("Hard");
    let tolerance = if is_hard { 0 } else { 1 };
    if weak.len() <= tolerance {
        console.print("\n[bold green]Verdict: READY[/bold green]");
        if let Some((m, s)) = weak.first() {
            console.print(&format!("Training target: [bold]{m}[/bold] ({s})"));
        } else if is_hard {
            console.print(
                "[dim]Walk is all green — summit is a pure combination rep at altitude.[/dim]",
            );
        } else {
            console
                .print("[dim]No new moves — this is a pure combination/consolidation rep.[/dim]");
        }
        return;
    }
    if is_hard {
        console.print(&format!(
            "\n[bold red]Verdict: PREP FIRST[/bold red] — summits demand an all-SOLID walk (rusty gear stays at basecamp; `make hard {key}` plans the route).\n"
        ));
    } else {
        console
            .print("\n[bold red]Verdict: PREP FIRST[/bold red] — more than one non-SOLID move.\n");
    }
    for (step, (mv, status)) in weak.iter().enumerate() {
        if *status == STALE {
            let src = match latest_carrier(&ev, mv) {
                Some((date, _, problem)) => format!(
                    "problem {} ({date})",
                    problem.unwrap_or_else(|| "None".to_string())
                ),
                None => "a past carrier problem".to_string(),
            };
            console.print(&format!(
                "{}. [yellow]{mv}[/yellow] is stale — spaced re-solve of {src}",
                step + 1
            ));
        } else {
            let drill = ctx.nodes[mv]
                .drill
                .clone()
                .unwrap_or_else(|| "improvise a <5min drill".to_string());
            console.print(&format!(
                "{}. [orange3]{mv}[/orange3] ({status}) — micro-drill: {drill}",
                step + 1
            ));
        }
    }
}
