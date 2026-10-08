// kg_combos - serve a chain of problems in order, in one sitting.
//
//   kg_combos                          # list the chains in graph/chains/
//   kg_combos two-sequence-align       # the chain, with what is done this pass
//   kg_combos two-sequence-align prepare   # `make prepare` its next problem
//
// A chain file lists problems that fill the same table, ordered so each one
// is one change from an earlier one. The chain loops. A pass is done when
// every problem in it has been solved from the chain since the last pass
// ended; then the next pass starts from the first problem. Only solves whose
// file starts with the chain's note count. A problem's "state", "event",
// "invariant", "from" and "change" fields are notes in the json and are never
// printed: each is the solution. `prepare` puts a comment at the top of
// current.py naming the chain and where it is saved. A chain's "assist" field says what an
// unaided solve served from it scores (kg::data::chain_assist): "none",
// a plain unaided solve, or "hint" (the default), half a game, because
// the chain's name gives the technique away.

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
}

fn is_drill_id(id: &str) -> bool {
    id.len() > 1 && id.starts_with('d') && id[1..].chars().all(|c| c.is_ascii_digit())
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

/// A game's verdict as `make stats` words it, with the minutes on the
/// clock when they are on file: fail, pass, pass over the clock, or a
/// pass with the assist level that was used.
fn verdict(g: &kg::model::Game) -> String {
    let mins = g
        .seconds
        .map(|s| format!(" {}m", s / 60))
        .unwrap_or_default();
    if g.failed {
        "[red]fail[/red]".to_string()
    } else if g.over {
        format!("[yellow]over{mins}[/yellow]")
    } else if g.assist == "none" {
        format!("[green]pass{mins}[/green]")
    } else {
        format!("[cyan]{}{mins}[/cyan]", g.assist)
    }
}

/// Walk the chain's solves in time order. Each solve adds its problem to the
/// current pass; when the pass holds every problem, it counts as finished and
/// empties. Returns the finished passes and the problems in the current one.
fn chain_passes(ctx: &Ctx, ev: &Evidence, name: &str, steps: &[Step]) -> (usize, HashSet<String>) {
    let root = &ctx.root;
    let note = format!("{}{name},", kg::data::COMBO_NOTE_PREFIX);
    let mut solves: Vec<(&str, &str)> = steps
        .iter()
        .flat_map(|st| {
            // a drill id (d14) is keyed in the evidence by its bank file,
            // a problem by its number
            let files: Vec<&str> = if is_drill_id(&st.id) {
                ctx.drill_path(&st.id)
                    .map(|p| {
                        let key = ctx.drill_evidence_key(&p);
                        ev.drill_reps(&key)
                            .iter()
                            .map(|&i| ev.recs[ev.drills[i].2].0.as_str())
                            .collect()
                    })
                    .unwrap_or_default()
            } else {
                ev.problem_recs(&st.id)
                    .into_iter()
                    .map(|(_, f, _)| f)
                    .collect()
            };
            files.into_iter().map(move |f| (f, st.id.as_str()))
        })
        .filter(|(f, _)| std::fs::read_to_string(root.join(f)).is_ok_and(|t| t.starts_with(&note)))
        .collect();
    solves.sort_by_key(|(f, _)| stamp(f));
    let (mut finished, mut pass) = (0, HashSet::new());
    for (_, id) in solves {
        pass.insert(id.to_string());
        if pass.len() == steps.len() {
            finished += 1;
            pass.clear();
        }
    }
    (finished, pass)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("{USAGE}\n\nServe a chain of closely related problems in order.\n\n  chain     a file name in graph/chains/ (optional when there is only one)\n  prepare   `make prepare` the first problem in the chain not done this pass");
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
    let (finished, pass) = chain_passes(&ctx, &ev, &name, &steps);
    let done = |id: &str| pass.contains(id);

    // rating: the contest rating, coloured by its gap to his elo like the
    // queue (red 100 above, yellow inside 100, green below), and the label
    // it earns (kg::model::rating_label); leetcode: LeetCode's own label;
    // tries: every attempt on file, oldest first, worded like make stats
    let ratings = kg::model::solve_ratings(&ctx);
    let elo = kg::model::first_sight_elo_now(&ctx, &ev);
    let games = kg::model::scored_games(&ctx, &ev);
    let today = ctx.today();
    let painted = |d: &str| {
        let c = kg::queue::difficulty_colour(d);
        format!("[{c}]{d}[/{c}]")
    };
    let mut table = Table::bare(
        &[
            "#", "problem", "rating", "label", "leetcode", "tries", "verdicts", "last", "this pass",
        ],
        true,
        2,
    );
    for (i, st) in steps.iter().enumerate() {
        let (rating, label) = match ratings.get(&st.id) {
            Some(r) => {
                let c = kg::queue::gap_colour(*r - elo);
                (
                    format!("[{c}]{r:.0}[/{c}]"),
                    painted(kg::model::rating_label(*r)),
                )
            }
            None => (String::new(), String::new()),
        };
        let mine: Vec<&kg::model::Game> = games.iter().filter(|g| g.problem == st.id).collect();
        let verdicts: Vec<String> = mine.iter().map(|g| verdict(g)).collect();
        let last = mine
            .last()
            .map(|g| {
                let days = (today - kg::data::parse_date(&g.date)).num_days();
                match days {
                    0 => "today".to_string(),
                    1 => "yesterday".to_string(),
                    _ => format!("{days}d ago"),
                }
            })
            .unwrap_or_default();
        let mark = if done(&st.id) {
            "[green]done[/green]"
        } else {
            ""
        };
        table.add_row(&[
            (i + 1).to_string(),
            format!("{}. {}", st.id, st.title),
            rating,
            label,
            painted(&ctx.meta_difficulty(&st.id)),
            if mine.is_empty() {
                String::new()
            } else {
                mine.len().to_string()
            },
            verdicts.join(", "),
            last,
            mark.to_string(),
        ]);
    }
    console.print(&format!(
        "[bold]The {name} chain, pass {}[/bold]. You have finished it {finished} {}.",
        finished + 1,
        if finished == 1 { "time" } else { "times" }
    ));
    print_table(&console, &table);
    let on_chain: Vec<&kg::model::Game> = games
        .iter()
        .filter(|g| steps.iter().any(|st| st.id == g.problem))
        .collect();
    if !on_chain.is_empty() {
        let fails = on_chain.iter().filter(|g| g.failed).count();
        let helped = on_chain
            .iter()
            .filter(|g| !g.failed && g.assist != "none")
            .count();
        let passes = on_chain.len() - fails - helped;
        let secs: i64 = on_chain.iter().filter_map(|g| g.seconds).sum();
        console.print(&format!(
            "Across the chain: [green]{passes} unaided {}[/green], [cyan]{helped} with help[/cyan], [red]{fails} {}[/red], {}h {:02}m on the clock.",
            if passes == 1 { "pass" } else { "passes" },
            if fails == 1 { "fail" } else { "fails" },
            secs / 3600,
            secs % 3600 / 60
        ));
    }

    // chain_passes() empties the pass as soon as it is full, so there is always a next
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
         # the chain and what is done this pass; the chain is saved in graph/chains/{name}.json.",
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
