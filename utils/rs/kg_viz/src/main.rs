// kg_viz - draw the whole technique graph as an actual graph.
//
//   kg_viz               # render + show inline in the terminal (iTerm2)
//   kg_viz --open        # render + open the SVG in the browser (hover tooltips)
//   kg_viz --no-show     # render only
//   kg_viz --source      # print the DOT source instead of rendering
//
// Nodes are colored by degree of ownership (kg::status::node_degree), edges
// are prerequisites from nodes.json, families are drawn as clusters.
//
// Ported from utils/kg/kg_viz (Python) on 2026-09-12.

use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::render::{display, render, Dot};
use kg::status::{node_degree, node_status};

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_viz [--open] [--no-show] [--source]\n\nRender the technique graph.\n\n  --open     open the SVG in the browser instead\n  --no-show  render only, display nothing (also --no-open)\n  --source   print the DOT source, render nothing");
        return;
    }
    let open = args.iter().any(|a| a == "--open");
    let no_show = args.iter().any(|a| a == "--no-show" || a == "--no-open");
    let source_only = args.iter().any(|a| a == "--source");

    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let pv = PView::new(ctx.evidenced());
    let ev = Evidence::new(recs);
    let console = Console::full_width();

    let mut dot = Dot::new("technique-graph");
    let mut groups: Vec<(String, Vec<&String>)> = Vec::new();
    for (id, node) in &ctx.nodes {
        let group = node.group.clone().unwrap_or_else(|| "None".to_string());
        match groups.iter_mut().find(|(g, _)| *g == group) {
            Some((_, m)) => m.push(id),
            None => groups.push((group, vec![id])),
        }
    }
    for (group, members) in &groups {
        dot.begin_subgraph(
            &format!("cluster_{group}"),
            &[
                ("label", group.as_str()),
                ("fontcolor", "#8b949e"),
                ("color", "#30363d"),
                ("style", "rounded"),
                ("fontname", "Helvetica"),
            ],
        );
        for id in members {
            let (status, when) = node_status(&ctx, id, &ev, today);
            let when = when.map(|d| d.format("%Y-%m-%d").to_string());
            let label = id.replacen('-', "-\n", 1);
            dot.status_node(
                id,
                &ctx.nodes[*id].name,
                status,
                when.as_deref(),
                false,
                &label,
                node_degree(&ctx, id, &ev, &pv, today),
            );
        }
        dot.end_subgraph();
    }
    for (id, node) in &ctx.nodes {
        for prereq in &node.prereqs {
            if ctx.nodes.contains_key(prereq) {
                dot.edge(prereq, id, &[]);
            }
        }
    }
    dot.legend();
    if source_only {
        print!("{}", dot.source());
        return;
    }
    let graph_dir = ctx.graph_dir();
    let width = match render(&graph_dir, dot.source(), "kg") {
        Ok(w) => w,
        Err(e) => {
            eprintln!("kg_viz: {e}");
            std::process::exit(1);
        }
    };
    console.print(&format!(
        "Rendered [bold]{}/kg.svg[/bold] and kg.png",
        graph_dir.display()
    ));
    if no_show {
        return;
    }
    if open {
        let _ = std::process::Command::new("open")
            .arg(graph_dir.join("kg.svg"))
            .status();
    } else {
        display(&console, &graph_dir, "kg", width);
    }
}
