// kg_drill - record a micro-drill result as evidence in the technique graph.
//
//   kg_drill solve-pair-condition clean --note "caught own sign slip via plug-in check"
//   kg_drill derived-key-lookup struggled
//
// Drills are the freshest evidence about the weakest nodes; a drill that
// isn't recorded didn't happen, as far as the graph is concerned.
//
// Ported from utils/kg/kg_drill (Python) on 2026-09-12.

use kg::console::Console;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root, Rec};
use kg::evidence::Evidence;
use kg::pyjson;
use kg::status::node_status;
use serde_json::{json, Value};

const USAGE: &str = "usage: kg_drill [-h] [--note NOTE] [--date DATE] node {clean,struggled}";

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("{USAGE}\n\nRecord a micro-drill result.\n\n  node         node id from graph/nodes.json\n  verdict      how it went: clean or struggled\n  --note NOTE  one-line context\n  --date DATE  YYYY-MM-DD (default today)");
        return;
    }
    let (mut node, mut verdict, mut note, mut date) = (None, None, String::new(), None);
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--note" => {
                i += 1;
                note = args.get(i).cloned().unwrap_or_default();
            }
            "--date" => {
                i += 1;
                date = args.get(i).cloned();
            }
            a if node.is_none() => node = Some(a.to_string()),
            a if verdict.is_none() => verdict = Some(a.to_string()),
            _ => {
                eprintln!("{USAGE}");
                std::process::exit(2);
            }
        }
        i += 1;
    }
    let (Some(node), Some(verdict)) = (node, verdict) else {
        eprintln!("{USAGE}");
        std::process::exit(2);
    };
    if verdict != "clean" && verdict != "struggled" {
        eprintln!("{USAGE}\nkg_drill: error: argument verdict: invalid choice: '{verdict}' (choose from 'clean', 'struggled')");
        std::process::exit(2);
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let console = Console::full_width();
    let date = date.unwrap_or_else(|| ctx.today().format("%Y-%m-%d").to_string());

    if !ctx.nodes.contains_key(&node) {
        console.print(&format!("[red]Unknown node id: {node}[/red]"));
        let head = node.split('-').next().unwrap_or("");
        let near: Vec<&String> = ctx.nodes.keys().filter(|n| n.contains(head)).collect();
        if !near.is_empty() {
            let near: Vec<&str> = near.iter().map(|s| s.as_str()).collect();
            console.print(&format!("[dim]Did you mean: {}[/dim]", near.join(", ")));
        }
        std::process::exit(1);
    }

    // the file as it is now: one entry added, the rest untouched
    let path = ctx.graph_dir().join("evidence.json");
    let mut data: Value = pyjson::load(&path).expect("graph/evidence.json");
    let evidence = data["evidence"].as_object_mut().expect("evidence{}");
    let mut key = format!("drill@{date}-{node}");
    let mut n = 2;
    while evidence.contains_key(&key) {
        key = format!("drill@{date}-{node}-{n}");
        n += 1;
    }
    let mut entry =
        json!({"date": date, "problem": "drill", "moves": {node.clone(): verdict.clone()}});
    if !note.is_empty() {
        entry["note"] = Value::String(note);
    }
    evidence.insert(key.clone(), entry.clone());
    pyjson::save(&path, &data, Some(2)).expect("write graph/evidence.json");

    let mut ev = Evidence::new(recs);
    ev.push(key.clone(), Rec::parse(&entry));
    let (status, _) = node_status(&ctx, &node, &ev, ctx.today());
    console.print(&format!("Recorded [bold]{node}[/bold] = {verdict} ({key})"));
    console.print(&format!("Node status is now: [bold]{status}[/bold]"));
}
