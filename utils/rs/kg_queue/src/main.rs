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
// What a gate is, and how the model is asked: kg::queue.

use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::evidence::Evidence;
use kg::git::sleep_state;
use kg::llm::{claude_json, judge_model};
use kg::model::first_sight_elo_now;
use kg::pyjson::dumps;
use kg::queue::{
    apply_gates, gap_colour, gate_context, queue_rows, queue_table, valid_gates, Gate, QueueRow,
    GATE_SYSTEM_PROMPT, QUEUE_LEN,
};
use kg::table::{print_table, BoxKind, Table};

const DEFAULT_GAP: f64 = 50.0;

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

/// The queue rows rated `gap` or more above his elo.
fn targets(rows: &[QueueRow], elo: f64, gap: f64) -> Vec<&QueueRow> {
    rows.iter()
        .filter(|r| r.rating.is_some_and(|x| x - elo >= gap))
        .collect()
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

    let elo = first_sight_elo_now(&ctx, &ev);
    let rows = queue_rows(&ctx, &pv, &ev, &asleep, args.size);
    let context = gate_context(&ctx, &targets(&rows, elo, args.gap), elo, None);
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
    let reply = match claude_json(
        &dumps(&context, Some(1)),
        GATE_SYSTEM_PROMPT,
        &args.model,
        2,
    ) {
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
        match apply_gates(&ctx, &gates) {
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
