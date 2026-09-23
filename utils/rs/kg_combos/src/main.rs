// kg_combos - serve a chain of problems in order, in one sitting.
//
//   kg_combos                          # list the chains in graph/chains/
//   kg_combos two-sequence-align       # the chain, with what is done this lap
//   kg_combos two-sequence-align prepare   # `make prepare` its next problem
//
// A chain file lists problems that fill the same table, ordered so each one
// is one change from an earlier one. The chain loops. A lap is done when
// every problem in it has been solved from the chain since the last lap
// ended; then the next lap starts from the first problem. Only solves whose
// file starts with the chain's note count. A problem's "change" line is
// printed only once it is done this lap: before the solve it would give away
// the move. `prepare` puts a comment at the top of current.py naming the
// chain and where it is saved.

use kg::console::Console;
use kg::ctx::Ctx;
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::table::{print_table, Table};
use serde_json::Value;
use std::collections::HashSet;
use std::path::Path;

const USAGE: &str = "usage: kg_combos [-h] [chain] [{prepare}]";

struct Step {
    id: String,
    title: String,
    from: Option<String>,
    change: Option<String>,
}

fn chain_names(dir: &Path) -> Vec<String> {
    let mut names: Vec<String> = std::fs::read_dir(dir)
        .map(|rd| {
            rd.filter_map(|e| e.ok())
                .filter_map(|e| {
                    let p = e.path();
                    (p.extension()? == "json").then(|| p.file_stem()?.to_str().map(String::from))?
                })
                .collect()
        })
        .unwrap_or_default();
    names.sort();
    names
}

fn load_chain(path: &Path) -> Vec<Step> {
    let text = std::fs::read_to_string(path).unwrap_or_else(|e| {
        eprintln!("cannot read {}: {e}", path.display());
        std::process::exit(1);
    });
    let v: Value = serde_json::from_str(&text).unwrap_or_else(|e| {
        eprintln!("{} is not valid json: {e}", path.display());
        std::process::exit(1);
    });
    let s = |x: &Value| x.as_str().map(String::from);
    v["order"]
        .as_array()
        .into_iter()
        .flatten()
        .filter_map(|id| {
            let id = id.as_str()?.to_string();
            let p = &v["problems"][&id];
            Some(Step {
                title: s(&p["title"]).unwrap_or_default(),
                from: s(&p["from"]),
                change: s(&p["change"]),
                id,
            })
        })
        .collect()
}

/// The solve's timestamp, from the tail of its file name
/// (`..._2026_09_23T01_23_26_945067_00_00Z.py`); it sorts as text.
fn stamp(fname: &str) -> &str {
    fname
        .rsplitn(9, '_')
        .last()
        .map_or(fname, |head| &fname[head.len()..])
}

/// Walk the chain's solves in time order. Each solve adds its problem to the
/// current lap; when the lap holds every problem, it counts as finished and
/// empties. Returns the finished laps and the problems in the current one.
fn laps(root: &Path, ev: &Evidence, name: &str, steps: &[Step]) -> (usize, HashSet<String>) {
    let note = format!("{}{name},", kg::data::COMBO_NOTE_PREFIX);
    let mut solves: Vec<(&str, &str)> = steps
        .iter()
        .flat_map(|st| {
            ev.problem_recs(&st.id)
                .into_iter()
                .map(move |(_, f, _)| (f, st.id.as_str()))
        })
        .filter(|(f, _)| std::fs::read_to_string(root.join(f)).is_ok_and(|t| t.starts_with(&note)))
        .collect();
    solves.sort_by_key(|(f, _)| stamp(f));
    let (mut finished, mut lap) = (0, HashSet::new());
    for (_, id) in solves {
        lap.insert(id.to_string());
        if lap.len() == steps.len() {
            finished += 1;
            lap.clear();
        }
    }
    (finished, lap)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("{USAGE}\n\nServe a chain of closely related problems in order.\n\n  chain     a file name in graph/chains/ (optional when there is only one)\n  prepare   `make prepare` the first problem in the chain not done this lap");
        return;
    }
    let prepare = args.iter().any(|a| a == "prepare");
    let rest: Vec<&String> = args.iter().filter(|a| *a != "prepare").collect();
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let console = Console::full_width();
    let dir = ctx.graph_dir().join("chains");
    let names = chain_names(&dir);

    let name = match rest.as_slice() {
        [n] => (*n).clone(),
        [] if names.len() == 1 => names[0].clone(),
        [] => {
            console.print("[bold]The chains in graph/chains/:[/bold]");
            for n in &names {
                console.print(&format!("  make combos {n}"));
            }
            return;
        }
        _ => {
            eprintln!("{USAGE}");
            std::process::exit(2);
        }
    };
    let path = dir.join(format!("{name}.json"));
    if !path.exists() {
        console.print(&format!(
            "[red]There is no chain called {name}. The chains are: {}.[/red]",
            names.join(", ")
        ));
        std::process::exit(1);
    }
    let steps = load_chain(&path);
    let ev = Evidence::new(recs);
    let (laps, lap) = laps(&ctx.root, &ev, &name, &steps);
    let done = |id: &str| lap.contains(id);

    let mut table = Table::bare(&["#", "problem", "this lap", "change"], true, 2);
    for (i, st) in steps.iter().enumerate() {
        let (mark, change) = if done(&st.id) {
            let change = match (&st.from, &st.change) {
                (Some(f), Some(c)) => format!("{f} + {c}"),
                _ => "the base".to_string(),
            };
            ("[green]done[/green]".to_string(), change)
        } else {
            (String::new(), String::new())
        };
        table.add_row(&[
            (i + 1).to_string(),
            format!("{}. {}", st.id, st.title),
            mark,
            change,
        ]);
    }
    console.print(&format!(
        "[bold]The {name} chain, lap {}[/bold]. You have finished it {laps} {}.",
        laps + 1,
        if laps == 1 { "time" } else { "times" }
    ));
    print_table(&console, &table);

    // laps() empties the lap as soon as it is full, so there is always a next
    let Some(next) = steps.iter().find(|st| !done(&st.id)) else {
        return;
    };
    if !prepare {
        console.print(&format!(
            "The next problem is {}. {}. Run `make combos {name} prepare` to start it.",
            next.id, next.title
        ));
        return;
    }
    console.print(&format!("[bold]make prepare {}[/bold]", next.id));
    let pos = steps.iter().position(|st| st.id == next.id).unwrap_or(0) + 1;
    let note = format!(
        "{prefix}{name}, problem {pos} of {total}. Run `make combos {name}` to see\n\
         # the chain and what is done this lap; the chain is saved in graph/chains/{name}.json.",
        prefix = kg::data::COMBO_NOTE_PREFIX,
        total = steps.len()
    );
    let status = std::process::Command::new(kg::data::rs_bin(&ctx.root, "prepare"))
        .arg(&next.id)
        .env("KG_COMBO_NOTE", note)
        .current_dir(&ctx.root)
        .status();
    std::process::exit(status.ok().and_then(|s| s.code()).unwrap_or(1));
}
