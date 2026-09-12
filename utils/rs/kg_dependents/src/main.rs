// kg_dependents - what an id gates, to act on right after finishing it.
//
//   kg_dependents d26            # a drill
//   kg_dependents 46             # a problem
//   kg_dependents d26 prepare    # cut a branch for each open one, easiest first
//
// One row per problem or drill whose "after" list names the id: its id and
// title, its kind, its status today, and what else still holds it. A row
// with nothing else holding it is servable the moment the id is warm:
// `make prepare <id>`.
//
// Ported from utils/kg/kg_dependents (Python) on 2026-09-12.

use kg::bank::{dependents, easiest_first, vertex_status};
use kg::console::Console;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::status::{Status, FRAGILE, MISSING, SOLID, STALE};
use kg::table::{print_table, Table};

fn style(s: Status) -> &'static str {
    match s {
        SOLID => "green",
        STALE => "yellow",
        FRAGILE => "red",
        MISSING => "dim",
    }
}

const USAGE: &str = "usage: kg_dependents [-h] id [{prepare}]";

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("{USAGE}\n\nList what a problem or drill gates.\n\n  id        a drill id (d26), a problem number (46), or a node id\n  prepare   `make prepare` every dependent nothing else holds, easiest first (drills, Easy, Medium, Hard)");
        return;
    }
    let (vid, action) = match args.as_slice() {
        [vid] => (vid.clone(), None),
        [vid, action] if action == "prepare" => (vid.clone(), Some(action.clone())),
        _ => {
            eprintln!("{USAGE}");
            std::process::exit(2);
        }
    };
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let ev = Evidence::new(recs);
    let console = Console::full_width();
    let problems = &ctx.ro;

    let Some(kind) = ctx.vertex_kind(&vid, &problems.map) else {
        console.print(&format!("[red]nothing in the graph is called {vid}[/red]"));
        std::process::exit(1);
    };
    let mut head = match kind {
        "problem" => format!("{vid}. {}", problems.map[&vid].title),
        "drill" => format!("{vid}. {}", ctx.drills[&vid].title),
        _ => vid.clone(),
    };
    let st = if kind != "node" {
        let st = vertex_status(&ctx, &vid, problems, &ev, today);
        head.push_str(&format!("  [{0}]{st}[/{0}]", style(st)));
        Some(st)
    } else {
        None
    };
    console.print(&format!("[bold]{head}[/bold]"));
    if st.is_some_and(|s| s != SOLID) {
        console.print(&format!(
            "[dim]{vid} is not warm yet; these open once it is[/dim]"
        ));
    }

    let rows = dependents(&ctx, &vid, problems, &ev, today);
    if rows.is_empty() {
        console.print("[dim]gates nothing[/dim]");
        return;
    }
    let mut table = Table::bare(&["id", "title", "kind", "status", "then"], true, 2);
    for r in &rows {
        let then = if r.held_by.is_empty() {
            format!("make prepare {}", r.id)
        } else {
            format!("held by {}", r.held_by.join(", "))
        };
        table.add_row(&[
            r.id.clone(),
            r.title.clone(),
            r.kind.clone(),
            format!("[{0}]{1}[/{0}]", style(r.status), r.status),
            then,
        ]);
    }
    print_table(&console, &table);

    if action.is_some() {
        let order: Vec<_> = easiest_first(&ctx, &rows)
            .into_iter()
            .filter(|r| r.held_by.is_empty())
            .collect();
        let skipped: Vec<&str> = rows
            .iter()
            .filter(|r| !r.held_by.is_empty())
            .map(|r| r.id.as_str())
            .collect();
        if !skipped.is_empty() {
            console.print(&format!(
                "[dim]skipped, held by something else: {}[/dim]",
                skipped.join(", ")
            ));
        }
        if order.is_empty() {
            console.print("[dim]nothing to prepare[/dim]");
            return;
        }
        let ids: Vec<&str> = order.iter().map(|r| r.id.as_str()).collect();
        console.print(&format!("[bold]make prepare {}[/bold]", ids.join(" ")));
        // one at a time: prepare's workers would otherwise cut the branches in
        // whatever order the cache answers, and the last one cut is the one
        // left checked out
        let pythonpath = match std::env::var("PYTHONPATH") {
            Ok(p) => format!("utils:{p}"),
            Err(_) => "utils:".to_string(),
        };
        let status = std::process::Command::new(ctx.root.join(".venv/bin/python3"))
            .arg(ctx.root.join("utils/kg/prepare"))
            .args(["--jobs", "1"])
            .args(&ids)
            .env("PYTHONPATH", pythonpath)
            .current_dir(&ctx.root)
            .status();
        std::process::exit(status.ok().and_then(|s| s.code()).unwrap_or(1));
    }
}
