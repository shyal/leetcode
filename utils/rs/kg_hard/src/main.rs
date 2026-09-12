// kg_hard - pick a summit Hard and plan the route of base camps to reach it.
//
//   make hard          # pick a summit, verdict only, status+emoji tree
//   make hard 42       # same, for a specific problem
//   make hard graph    # label the tree with move names
//   make hard route    # named route + labeled tree (the map)
//
// kg_next and kg_dive work the rusty frontier bottom-up; kg_hard works
// top-down from a summit: take a Hard problem's full input tree (walk +
// transitive prereqs), find every non-SOLID node in it, and schedule one
// base camp per gap - a carrier problem (chosen the way kg_dive chooses,
// Hard carriers last) or a drill when no carrier is READY. Prereqs are
// scheduled before dependents and each camp is simulated as a clean solve.
//
// Summit picking (no argument): a curated shortlist of interview-classic
// Hards is scored by route length. Unmapped candidates cost ONE claude call
// for the whole batch; mappings are cached into problems.json.
//
// Ported from utils/kg/kg_hard (Python) on 2026-09-12.

use std::collections::{HashMap, HashSet};

use chrono::NaiveDate;
use kg::bank::{carriers_for, dodgeable, proving_carriers};
use kg::console::{Console, Text};
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, pnum_key, repo_root};
use kg::drills::drill_gated;
use kg::evidence::Evidence;
use kg::git::sleep_state;
use kg::llm::claude_json;
use kg::mock::PyRandom;
use kg::pick::CLASSICS;
use kg::render::{animate_with, display, faces, render, Dot};
use kg::status::{
    all_statuses, gentleness, immature_nodes, input_tree, last_solved, latest_carrier, node_degree,
    rank_summits, tree_size, Status, Statuses, DEEP_STALE_DAYS, FRAGILE, MISSING, SOLID, STALE,
};
use kg::table::{print_table, Table};
use serde_json::{json, Value};

/// kg_lib.CLASSICS: the blurb of each interview classic, in shortlist order.
const BLURBS: [(&str, &str); 23] = [
    ("4", "binary-search partitioning at its purest"),
    ("23", "the canonical heap hard — k-way merge"),
    ("25", "pointer surgery mastery — reverse in k-groups"),
    ("32", "stack meets DP on parentheses"),
    ("41", "in-place index cycling, O(1) space"),
    ("42", "the most famous hard — prefix-max / two-pointer"),
    ("76", "sliding window with need/have counters"),
    ("84", "monotonic stack at full power"),
    ("85", "84 lifted into 2-D"),
    ("124", "global-vs-path tree DP"),
    ("127", "implicit-graph BFS"),
    ("212", "trie + backtracking"),
    ("224", "expression parsing with a stack"),
    ("239", "monotonic deque"),
    ("295", "two-heap running median"),
    ("297", "tree serialization round-trip"),
    ("460", "layered data-structure design (LFU)"),
    ("502", "greedy + heap"),
    ("815", "BFS where routes are the nodes"),
    ("895", "stacked frequency stacks"),
    ("968", "greedy tree DP"),
    ("1235", "sort + binary search + DP"),
    ("2402", "two-heap simulation"),
];

fn style(s: Status) -> &'static str {
    match s {
        SOLID => "green",
        STALE => "yellow",
        FRAGILE => "red",
        MISSING => "dim",
    }
}

fn problem_url(ctx: &Ctx, pnum: &str) -> String {
    match ctx.meta.get(pnum).and_then(|m| m.slug.clone()) {
        Some(slug) => format!("https://leetcode.com/problems/{slug}/"),
        None => format!("https://leetcode.com/problemset/?search={pnum}"),
    }
}

fn taxonomy_summary(ctx: &Ctx) -> String {
    ctx.nodes
        .values()
        .map(|n| format!("- {}: {}", n.id, n.desc))
        .collect::<Vec<_>>()
        .join("\n")
}

/// One claude call mapping a batch of problems onto the taxonomy; results
/// cached into problems.json (same convention as preflight). Returns the
/// subset of `unmapped` that came back mapped, and reloads the view.
fn map_with_claude(
    console: &Console,
    ctx: &Ctx,
    pv: &mut PView,
    unmapped: &[String],
) -> Vec<String> {
    let listing: Vec<String> = unmapped
        .iter()
        .map(|n| {
            format!(
                "- {n}. {}",
                ctx.meta_title(n).unwrap_or_else(|| "?".to_string())
            )
        })
        .collect();
    let system = format!(
        "You are mapping LeetCode problems onto a fixed taxonomy of atomic technique moves.\n\nTaxonomy (use ONLY these ids):\n{}\n\nFor EACH problem below, determine the canonical clean solution and list every move a candidate must execute, including foundational micro-moves. Hard problems almost always hinge on a signature trick; if that trick has no matching node id, it MUST appear in \"unmapped\" — never paper over it with the nearest broader node. Output STRICT JSON, nothing else:\n{{\"problems\": [{{\"num\": \"<number>\", \"title\": \"<full title>\", \"moves\": [\"<node-id>\", ...], \"unmapped\": [\"<short description of any required move with no matching node>\"]}}, ...]}}\n\nDo not explain the solutions.",
        taxonomy_summary(ctx)
    );
    let result = match claude_json(
        &format!("LeetCode problems:\n{}", listing.join("\n")),
        &system,
        "sonnet",
        2,
    ) {
        Ok(v) => v,
        Err(e) => {
            console.print(&format!("[red]{e}[/red]"));
            return vec![];
        }
    };
    let mut mapped = Vec::new();
    for entry in result["problems"].as_array().into_iter().flatten() {
        let num = kg::data::value_str(&entry["num"]);
        let moves: Vec<String> = entry["moves"]
            .as_array()
            .map(|a| a.iter().map(kg::data::value_str).collect())
            .unwrap_or_default();
        if !unmapped.contains(&num) || moves.is_empty() {
            continue;
        }
        let mut e = json!({
            "title": entry.get("title").and_then(Value::as_str).map(String::from).or_else(|| ctx.meta_title(&num)).unwrap_or_else(|| num.clone()),
            "difficulty": ctx.meta.get(&num).and_then(|m| m.difficulty.clone()).unwrap_or_else(|| "Hard".to_string()),
            "moves": moves,
        });
        if let Some(un) = entry
            .get("unmapped")
            .and_then(Value::as_array)
            .filter(|a| !a.is_empty())
        {
            e["unmapped"] = Value::Array(un.clone());
            console.print(&format!(
                "[orange3]{num}: proposed new nodes (review!): {}[/orange3]",
                kg::pyjson::dumps(&Value::Array(un.clone()), None).replace('"', "'")
            ));
        }
        kg::pyjson::save_problem_entry(&ctx.root, &num, &e).expect("write graph/problems.json");
        mapped.push(num);
    }
    if !mapped.is_empty() {
        *pv = PView::new(kg::data::evidenced_view(&kg::data::load_all_problems(
            &ctx.root,
        )));
    }
    mapped
}

/// Most reachable valuable classic: fewest gaps, consolidation breaks ties.
fn pick_summit(
    console: &Console,
    ctx: &Ctx,
    pv: &mut PView,
    statuses: &Statuses,
    ev: &Evidence,
) -> Option<String> {
    let candidates: Vec<String> = CLASSICS
        .iter()
        .filter(|n| ctx.meta_difficulty(n) == "Hard" && last_solved(ev, n).is_empty())
        .map(|n| n.to_string())
        .collect();
    let unmapped: Vec<String> = candidates
        .iter()
        .filter(|n| !pv.map.contains_key(*n))
        .cloned()
        .collect();
    let mut mapped: Vec<String> = candidates
        .iter()
        .filter(|n| pv.map.contains_key(*n))
        .cloned()
        .collect();
    if mapped.len() < 3 && !unmapped.is_empty() {
        console.print(&format!(
            "[dim]Mapping {} classic Hards onto the taxonomy — one claude call, cached after...[/dim]",
            unmapped.len()
        ));
        mapped.extend(map_with_claude(console, ctx, pv, &unmapped));
    }
    let immature = immature_nodes(ctx, ev, pv);
    rank_summits(ctx, &mapped, pv, statuses, &immature)
        .first()
        .cloned()
}

/// (pnum, reason) for the target under simulated statuses, or None. Mirrors
/// kg_dive with one twist: Hard carriers sort last.
#[allow(clippy::too_many_arguments)]
fn choose_carrier(
    ctx: &Ctx,
    target: &str,
    sim: &Statuses,
    pv: &PView,
    ev: &Evidence,
    dodged: &HashMap<String, String>,
    excluded: &HashSet<String>,
    today: NaiveDate,
) -> Option<(String, String)> {
    let is_hard = |p: &str| {
        pv.map
            .get(p)
            .is_some_and(|x| x.difficulty.as_deref() == Some("Hard"))
    };
    let (s, d) = sim[target];
    let gentle_key = |p: &String| {
        (
            is_hard(p),
            gentleness(ctx, p, pv),
            last_solved(ev, p),
            -ctx.acceptance(p),
            pnum_key(p),
        )
    };
    if s == SOLID {
        // a SOLID target on the route is there because it is immature: the
        // camp is a proving rep
        let mut cands: Vec<String> = proving_carriers(ctx, target, pv, sim, ev, today)
            .into_iter()
            .filter(|c| !excluded.contains(c))
            .collect();
        if cands.is_empty() {
            return None;
        }
        cands.sort_by(|a, b| {
            (
                gentleness(ctx, a, pv),
                last_solved(ev, a),
                -ctx.acceptance(a),
                pnum_key(a),
            )
                .partial_cmp(&(
                    gentleness(ctx, b, pv),
                    last_solved(ev, b),
                    -ctx.acceptance(b),
                    pnum_key(b),
                ))
                .unwrap()
        });
        return Some((
            cands[0].clone(),
            "young move — prove it: solve this one VIA the move".to_string(),
        ));
    }
    let mut cands: Vec<String> = carriers_for(ctx, target, pv, sim, ev, today)
        .into_iter()
        .filter(|c| !excluded.contains(c))
        .collect();
    if cands.is_empty() {
        return None;
    }
    if s == FRAGILE {
        if let Some(on) = dodged.get(target) {
            cands.sort_by(|a, b| {
                (
                    is_hard(a),
                    dodgeable(pv, a, target),
                    tree_size(ctx, a, pv),
                    last_solved(ev, a),
                    pnum_key(a),
                )
                    .cmp(&(
                        is_hard(b),
                        dodgeable(pv, b, target),
                        tree_size(ctx, b, pv),
                        last_solved(ev, b),
                        pnum_key(b),
                    ))
            });
            return Some((
                cands[0].clone(),
                format!("dodged on {on} — carrier resists the dodge"),
            ));
        }
    }
    if s == STALE {
        let age = (today - d.unwrap()).num_days();
        if age <= DEEP_STALE_DAYS {
            let pnum = match latest_carrier(ev, target)
                .and_then(|(_, _, p)| p)
                .filter(|p| cands.contains(p))
            {
                Some(p) => p,
                None => {
                    // sorted(key=(not is_hard, last_solved), reverse=True)[0]
                    let mut by = cands.clone();
                    by.sort_by(|a, b| {
                        (!is_hard(b), last_solved(ev, b)).cmp(&(!is_hard(a), last_solved(ev, a)))
                    });
                    by[0].clone()
                }
            };
            return Some((pnum, "spaced re-solve".to_string()));
        }
        cands.sort_by(|a, b| gentle_key(a).partial_cmp(&gentle_key(b)).unwrap());
        return Some((
            cands[0].clone(),
            format!("deep-stale ({age}d) — gentle fresh carrier"),
        ));
    }
    cands.sort_by(|a, b| gentle_key(a).partial_cmp(&gentle_key(b)).unwrap());
    let why = if s == FRAGILE {
        "consolidate on a fresh carrier"
    } else {
        "new move, prereqs solid"
    };
    Some((cands[0].clone(), why.to_string()))
}

/// One base camp per gap in the summit's input tree, prereqs before
/// dependents, each camp simulated as a clean solve.
fn plan_route(
    ctx: &Ctx,
    summit: &str,
    pv: &PView,
    statuses: &Statuses,
    ev: &Evidence,
    asleep: &[String],
    today: NaiveDate,
) -> Vec<(String, Status, Option<String>, String)> {
    let mut sim = statuses.clone();
    let dodged = ev.dodged_nodes();
    let immature = immature_nodes(ctx, ev, pv);
    let mut remaining: Vec<String> = input_tree(&pv.map[summit].moves, &ctx.nodes)
        .into_iter()
        .filter(|n| statuses[n].0 != SOLID || immature.contains(n))
        .collect();
    remaining.sort();
    let mut excluded: HashSet<String> = asleep.iter().cloned().collect();
    excluded.insert(summit.to_string());
    let mut steps = Vec::new();
    while !remaining.is_empty() {
        let ready: Vec<String> = remaining
            .iter()
            .filter(|x| !ctx.nodes[*x].prereqs.iter().any(|p| remaining.contains(p)))
            .cloned()
            .collect();
        let mut pool = if ready.is_empty() {
            remaining.clone()
        } else {
            ready
        };
        pool.sort_by_key(|x| {
            (
                statuses[x].1.is_none(),
                statuses[x].1.unwrap_or(NaiveDate::MAX),
                x.clone(),
            )
        });
        let target = pool[0].clone();
        let status = sim[&target].0;
        if drill_gated(ctx, &target, sim[&target].0, sim[&target].1, today) {
            steps.push((
                target.clone(),
                status,
                None,
                "drill until clean — carrier stays held".to_string(),
            ));
        } else {
            match choose_carrier(ctx, &target, &sim, pv, ev, &dodged, &excluded, today) {
                Some((pnum, reason)) => {
                    excluded.insert(pnum.clone());
                    steps.push((target.clone(), status, Some(pnum), reason));
                }
                None => steps.push((
                    target.clone(),
                    status,
                    None,
                    "no ready carrier — drill it".to_string(),
                )),
            }
        }
        sim.insert(target.clone(), (SOLID, Some(today)));
        remaining.retain(|x| *x != target);
    }
    steps
}

#[allow(clippy::too_many_arguments)]
fn draw_tree(
    ctx: &Ctx,
    console: &Console,
    summit: &str,
    pv: &PView,
    statuses: &Statuses,
    ev: &Evidence,
    labeled: bool,
    today: NaiveDate,
) {
    let p = &pv.map[summit];
    let mut tree: Vec<String> = input_tree(&p.moves, &ctx.nodes).into_iter().collect();
    tree.sort();
    let mut rng = PyRandom::new(0);
    let mut dot = Dot::new("kg_hard");
    for n in &tree {
        let (s, d) = statuses[n];
        let when = d.map(|d| d.format("%Y-%m-%d").to_string());
        let label = if labeled {
            n.replacen('-', "-\n", 1)
        } else {
            let pool = faces(s);
            format!("{s} {}", pool[rng.randbelow(pool.len() as u32) as usize])
        };
        dot.status_node(
            n,
            &ctx.nodes[n].name,
            s,
            when.as_deref(),
            p.moves.contains(n),
            &label,
            node_degree(ctx, n, ev, pv, today),
        );
    }
    for n in &tree {
        for pre in &ctx.nodes[n].prereqs {
            if tree.contains(pre) {
                dot.edge(pre, n, &[]);
            }
        }
    }
    let summit_node = format!("problem_{summit}");
    let label = format!("⛰ {summit}. {}", p.title);
    let url = problem_url(ctx, summit);
    dot.node(
        &summit_node,
        &[
            ("label", label.as_str()),
            ("shape", "box"),
            ("style", "filled"),
            ("fillcolor", "#1f6feb"),
            ("color", "#c9d1d9"),
            ("penwidth", "2"),
            ("fontsize", "13"),
            ("margin", "0.2,0.12"),
            ("tooltip", url.as_str()),
        ],
    );
    for m in &p.moves {
        if tree.contains(m) {
            dot.edge(m, &summit_node, &[("penwidth", "1.4")]);
        }
    }
    let graph_dir = ctx.graph_dir();
    if let Ok(w) = render(&graph_dir, dot.source(), "kg_hard") {
        display(console, &graph_dir, "kg_hard", w);
    }
}

fn main() {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    if raw.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_hard [--route] [--graph] [--no-show] [problem]\n\nPick a summit Hard and plan the route to it.");
        return;
    }
    // `make hard route` / `make hard graph` / `make hard 23 graph`: bare goal words
    let mut route = false;
    let mut graph = false;
    let mut no_show = false;
    let mut problem: Option<String> = None;
    for a in &raw {
        match a.as_str() {
            "route" | "--route" => route = true,
            "graph" | "--graph" => graph = true,
            "--no-show" => no_show = true,
            other => problem = Some(other.to_string()),
        }
    }
    let labeled = graph || route;
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let ev = Evidence::new(recs);
    let mut pv = PView::new(ctx.evidenced());
    let console = Console::new(); // kg_render.animation_console: 8 columns under the pane
    let statuses = all_statuses(&ctx, &ev, today);
    let asleep = sleep_state(&ctx, &pv, &ev);

    let summit = match &problem {
        Some(p) => {
            let summit = p.trim().trim_end_matches('.').to_string();
            if !pv.map.contains_key(&summit) {
                let Some(title) = ctx.meta_title(&summit) else {
                    console.print(&format!("[red]unknown problem '{summit}'[/red]"));
                    return;
                };
                console.print(&format!("[dim]Mapping {summit}. {title} onto the taxonomy — one claude call, cached after...[/dim]"));
                if !map_with_claude(&console, &ctx, &mut pv, std::slice::from_ref(&summit))
                    .contains(&summit)
                {
                    console.print(&format!(
                        "[red]claude returned no mapping for {summit}[/red]"
                    ));
                    return;
                }
            }
            summit
        }
        None => match pick_summit(&console, &ctx, &mut pv, &statuses, &ev) {
            Some(s) => s,
            None => {
                console.print(
                    "[yellow]No classic Hard could be mapped — try `make hard <num>`.[/yellow]",
                );
                return;
            }
        },
    };
    let p = pv.map[&summit].clone();
    let difficulty = p
        .difficulty
        .clone()
        .filter(|d| !d.is_empty())
        .unwrap_or_else(|| ctx.meta_difficulty(&summit));
    let steps = plan_route(&ctx, &summit, &pv, &statuses, &ev, &asleep, today);

    console.begin_capture();
    console.print(&format!(
        "\n[bold]⛰  {summit}. {}[/bold]{}",
        p.title,
        if difficulty.is_empty() {
            String::new()
        } else {
            format!(" — {difficulty}")
        }
    ));
    console.print(&problem_url(&ctx, &summit));
    if route {
        if let Some((_, blurb)) = BLURBS.iter().find(|(n, _)| *n == summit) {
            console.print(&format!("[dim]{blurb}[/dim]"));
        }
    }
    if !difficulty.is_empty() && difficulty != "Hard" {
        console.print(&format!(
            "[yellow]note: this is a {difficulty}, not a Hard — routing anyway[/yellow]"
        ));
    }

    // Blind mode: verdict only in the text. The tree is status+face unless
    // --graph / --route names the walk (same deal as kg_next).
    if !route {
        if steps.is_empty() {
            console.print(
                "\n[bold green]Your walk is ready for this one. Go claim the summit.[/bold green]",
            );
        } else {
            let camps = if steps.len() == 1 {
                "1 base camp".to_string()
            } else {
                format!("{} base camps", steps.len())
            };
            console.print(&format!(
                "\n[yellow]Not ready — {camps} to build first.[/yellow]"
            ));
            console.print(&format!(
                "[dim]`make hard {summit} route` to see the route (names the moves).[/dim]"
            ));
        }
        let out = console.end_capture();
        if !no_show {
            draw_tree(&ctx, &console, &summit, &pv, &statuses, &ev, labeled, today);
        }
        animate_with(&console, out, &["laseretch"]);
        return;
    }

    let unknown: Vec<&String> = p
        .moves
        .iter()
        .filter(|m| !ctx.nodes.contains_key(*m))
        .collect();
    let mut table = Table::bare(&["Move", "Status", "Last evidence"], true, 2);
    for m in &p.moves {
        if ctx.nodes.contains_key(m) {
            let (s, d) = statuses[m];
            table.add_row(&[
                m.clone(),
                format!("[{0}]{s}[/{0}]", style(s)),
                d.map(|d| d.format("%Y-%m-%d").to_string())
                    .unwrap_or_else(|| "—".to_string()),
            ]);
        } else {
            table.add_row(&[
                m.clone(),
                "[red]unknown node[/red]".to_string(),
                "—".to_string(),
            ]);
        }
    }
    print_table(&console, &table);
    if !unknown.is_empty() {
        let names: Vec<&str> = unknown.iter().map(|s| s.as_str()).collect();
        console.print(&format!(
            "[orange3]unmapped territory (not routable until curated into nodes.json): {}[/orange3]",
            names.join(", ")
        ));
    }
    for desc in &p.unmapped {
        console.print(&format!(
            "[orange3]new territory (proposed node, review!): {desc}[/orange3]"
        ));
    }
    if steps.is_empty() {
        console.print("\n[bold green]The whole input tree is SOLID — no camps needed. Go claim the summit.[/bold green]");
    } else {
        let camps = if steps.len() == 1 {
            "base camp".to_string()
        } else {
            format!("{} base camps", steps.len())
        };
        console.print(&format!("\n[bold]Route ({camps}):[/bold]"));
        let dodged = ev.dodged_nodes();
        for (i, (target, status, pnum, reason)) in steps.iter().enumerate() {
            let st = style(*status);
            match pnum {
                Some(q) => console.print(&format!(
                    "  {}. [bold]{q}. {}[/bold] — [{st}]{status}[/{st}] [bold]{target}[/bold] ({reason})",
                    i + 1,
                    pv.map.get(q).map(|x| x.title.as_str()).unwrap_or("")
                )),
                None => {
                    if ctx.drills_dir().join(target).is_dir() {
                        console.print(&format!(
                            "  {}. `make drill {target}` — [{st}]{status}[/{st}] [bold]{target}[/bold] ({reason})",
                            i + 1
                        ));
                    } else {
                        console.print(&format!(
                            "  {}. drill: {} — [{st}]{status}[/{st}] [bold]{target}[/bold]",
                            i + 1,
                            ctx.nodes[target].drill.clone().unwrap_or_else(|| "improvise a <5min drill".to_string())
                        ));
                    }
                }
            }
            if pnum.is_some()
                && dodged.contains_key(target)
                && ctx.drills_dir().join(target).is_dir()
            {
                console.print(&format!("     [yellow]drill FIRST — a drill can't be dodged: `make drill {target}`[/yellow]"));
            }
        }
        console.print(&format!(
            "  ⛰  [bold]{summit}. {}[/bold] — summit: walk all SOLID after the camps above, a pure combination rep",
            p.title
        ));
        console.print(&format!(
            "\n[dim]Work top-down; `make solved` after each camp, then re-run `make hard {summit}` — the route re-derives and shrinks as camps turn SOLID.[/dim]"
        ));
    }
    let out = console.end_capture();
    if !no_show {
        draw_tree(&ctx, &console, &summit, &pv, &statuses, &ev, labeled, today);
    }
    animate_with(&console, out, &["laseretch"]);
    let _ = Text::plain;
}
