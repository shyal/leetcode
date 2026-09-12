// kg_dive - cluster the rusty frontier and plan a themed deep-dive session.
//
//   make dive           # rank clusters, plan a 3-problem dive in the top one
//   make dive 5         # longer session
//   make dive graphs    # dive a specific cluster instead of the top-scored one
//
// kg_next is greedy and memoryless: each run picks the single globally-oldest
// rusty node, so consecutive sessions hop between unrelated topics. kg_dive
// answers the other question - "where should I spend a whole session?":
//
//   1. Take every non-SOLID node (MISSING only if its prereqs are all SOLID -
//      otherwise it isn't assignable yet and shouldn't attract the dive).
//   2. Join them into clusters: same curated `group`, or a direct prereq edge.
//   3. Score each cluster by urgency mass: FRAGILE 3, STALE 2, MISSING 1,
//      oldest evidence breaking ties. The heaviest cluster is the dive.
//   4. Plan up to N problems INSIDE that cluster, prereqs scheduled before
//      dependents, each pick simulated as a clean solve so later picks can
//      stand on earlier ones. Carrier choice per target mirrors kg_next.
//
// The plan is an ordering, not a contract: solve top-down, `make solved` after
// each, and re-run - the plan re-derives from fresh evidence every time.
//
// Ported from utils/kg/kg_dive (Python) on 2026-09-12.

use std::collections::{HashMap, HashSet};

use chrono::NaiveDate;
use kg::bank::{carriers_for, dodgeable};
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, pnum_key, repo_root};
use kg::drills::drill_gated;
use kg::evidence::Evidence;
use kg::git::sleep_state;
use kg::status::{
    all_statuses, gentleness, last_solved, latest_carrier, tree_size, Status, Statuses,
    DEEP_STALE_DAYS, FRAGILE, MISSING, SOLID, STALE,
};
use kg::table::{print_table, Column, Justify, Table};

fn style(s: Status) -> &'static str {
    match s {
        SOLID => "green",
        STALE => "yellow",
        FRAGILE => "red",
        MISSING => "dim",
    }
}

fn weight(s: Status) -> i64 {
    match s {
        FRAGILE => 3,
        STALE => 2,
        MISSING => 1,
        SOLID => 0,
    }
}

/// Non-SOLID nodes worth diving on. MISSING counts only when assignable
/// (all prereqs SOLID).
fn rusty_frontier(ctx: &Ctx, statuses: &Statuses) -> Vec<String> {
    ctx.nodes
        .iter()
        .filter(|(n, node)| {
            let s = statuses[*n].0;
            s == FRAGILE
                || s == STALE
                || (s == MISSING
                    && node
                        .prereqs
                        .iter()
                        .all(|p| statuses.get(p).is_some_and(|x| x.0 == SOLID)))
        })
        .map(|(n, _)| n.clone())
        .collect()
}

/// Connected components over rusty nodes: same group or direct prereq edge.
/// Components and their members follow nodes.json order; the Python walked
/// a set, so tied group names in a label could come out in another order.
fn clusters_of(ctx: &Ctx, rusty: &[String]) -> Vec<Vec<String>> {
    let set: HashSet<&str> = rusty.iter().map(String::as_str).collect();
    let mut parent: HashMap<&str, &str> = rusty.iter().map(|n| (n.as_str(), n.as_str())).collect();
    fn find<'a>(parent: &mut HashMap<&'a str, &'a str>, mut n: &'a str) -> &'a str {
        while parent[n] != n {
            let gp = parent[parent[n]];
            parent.insert(n, gp);
            n = parent[n];
        }
        n
    }
    let mut by_group: Vec<(Option<String>, Vec<&str>)> = Vec::new();
    for n in rusty {
        let g = ctx.nodes[n].group.clone();
        match by_group.iter_mut().find(|(k, _)| *k == g) {
            Some((_, m)) => m.push(n),
            None => by_group.push((g, vec![n])),
        }
    }
    for (_, members) in &by_group {
        for m in &members[1..] {
            let a = find(&mut parent, members[0]);
            let b = find(&mut parent, m);
            parent.insert(a, b);
        }
    }
    for n in rusty {
        for p in &ctx.nodes[n].prereqs {
            if set.contains(p.as_str()) {
                let a = find(&mut parent, p);
                let b = find(&mut parent, n);
                parent.insert(a, b);
            }
        }
    }
    let mut comps: Vec<(&str, Vec<String>)> = Vec::new();
    for n in rusty {
        let r = find(&mut parent, n);
        match comps.iter_mut().find(|(k, _)| *k == r) {
            Some((_, m)) => m.push(n.clone()),
            None => comps.push((r, vec![n.clone()])),
        }
    }
    comps.into_iter().map(|(_, m)| m).collect()
}

fn cluster_score(cluster: &[String], statuses: &Statuses) -> i64 {
    cluster.iter().map(|n| weight(statuses[n].0)).sum()
}

fn cluster_label(ctx: &Ctx, cluster: &[String]) -> String {
    let mut groups: Vec<(String, i64)> = Vec::new();
    for n in cluster {
        let g = ctx.nodes[n]
            .group
            .clone()
            .unwrap_or_else(|| "?".to_string());
        match groups.iter_mut().find(|(k, _)| *k == g) {
            Some((_, c)) => *c += 1,
            None => groups.push((g, 1)),
        }
    }
    groups.sort_by_key(|(_, c)| -c); // stable: first-seen order on ties
    groups
        .into_iter()
        .map(|(g, _)| g)
        .collect::<Vec<_>>()
        .join("+")
}

fn urgency_key(n: &str, statuses: &Statuses) -> (i64, NaiveDate, String) {
    let (s, d) = statuses[n];
    let order = match s {
        FRAGILE => 0,
        STALE => 1,
        _ => 2,
    };
    (order, d.unwrap_or(NaiveDate::MAX), n.to_string())
}

/// (pnum, reason) for the target under simulated statuses, or None.
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
    let mut cands: Vec<String> = carriers_for(ctx, target, pv, sim, ev, today)
        .into_iter()
        .filter(|c| !excluded.contains(c))
        .collect();
    if cands.is_empty() {
        return None;
    }
    let (s, d) = sim[target];
    let gentle = |cands: &mut Vec<String>| {
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
    };
    if s == FRAGILE {
        if let Some(on) = dodged.get(target) {
            cands.sort_by(|a, b| {
                (
                    dodgeable(pv, a, target),
                    tree_size(ctx, a, pv),
                    last_solved(ev, a),
                    pnum_key(a),
                )
                    .cmp(&(
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
            let carrier = latest_carrier(ev, target);
            let pnum = match carrier
                .and_then(|(_, _, p)| p)
                .filter(|p| cands.contains(p))
            {
                Some(p) => p,
                None => {
                    let mut by_recent = cands.clone();
                    by_recent.sort_by_key(|b| std::cmp::Reverse(last_solved(ev, b)));
                    by_recent[0].clone()
                }
            };
            return Some((pnum, "spaced re-solve".to_string()));
        }
        gentle(&mut cands);
        return Some((
            cands[0].clone(),
            format!("deep-stale ({age}d) — gentle fresh carrier"),
        ));
    }
    gentle(&mut cands);
    let why = if s == FRAGILE {
        "consolidate on a fresh carrier"
    } else {
        "new move, prereqs solid"
    };
    Some((cands[0].clone(), why.to_string()))
}

/// Up to n steps inside the cluster: (target, status, pnum, reason). Picks
/// simulate a clean solve so later carriers may stand on earlier targets.
#[allow(clippy::too_many_arguments)]
fn plan_dive(
    ctx: &Ctx,
    cluster: &[String],
    statuses: &Statuses,
    pv: &PView,
    ev: &Evidence,
    asleep: &[String],
    n: usize,
    today: NaiveDate,
) -> Vec<(String, Status, Option<String>, String)> {
    let mut sim = statuses.clone();
    let dodged = ev.dodged_nodes();
    let mut remaining: Vec<String> = cluster.to_vec();
    let mut excluded: HashSet<String> = asleep.iter().cloned().collect();
    let mut steps = Vec::new();
    while !remaining.is_empty() && steps.len() < n {
        // prereqs first: a node waits while a rusty prereq of it is still unscheduled
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
        pool.sort_by_key(|x| urgency_key(x, &sim));
        let Some(target) = pool.first().cloned() else {
            break;
        };
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
                // no READY carrier - a drill still trains the node and can't be dodged
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

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_dive [words ...]\n\nCluster the rusty frontier and plan a deep-dive session.\n\n  words  a number = session length (default 3), a word = cluster to dive");
        return;
    }
    let mut n = 3usize;
    let mut cluster_name: Option<String> = None;
    for w in &args {
        match w.parse::<usize>() {
            Ok(k) if w.chars().all(|c| c.is_ascii_digit()) => n = k,
            _ => cluster_name = Some(w.clone()),
        }
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());
    let console = Console::full_width();
    let statuses = all_statuses(&ctx, &ev, today);
    let asleep = sleep_state(&ctx, &pv, &ev); // woken is always empty: nothing auto-wakes

    let rusty = rusty_frontier(&ctx, &statuses);
    if rusty.is_empty() {
        console.print(
            "[green]Nothing rusty — the whole frontier is SOLID. Go learn a new move.[/green]",
        );
        return;
    }
    let mut ranked = clusters_of(&ctx, &rusty);
    ranked.sort_by_key(|c| {
        (
            -cluster_score(c, &statuses),
            c.iter()
                .map(|x| statuses[x].1.unwrap_or(NaiveDate::MAX))
                .min()
                .unwrap(),
            cluster_label(&ctx, c),
        )
    });

    let mut table = Table::bare(&["Cluster", "Score", "Rusty moves"], true, 2);
    table.column(
        1,
        Column {
            justify: Justify::Right,
            ..Column::default()
        },
    );
    for c in &ranked {
        let mut members = c.clone();
        members.sort_by_key(|x| urgency_key(x, &statuses));
        let parts: Vec<String> = members
            .iter()
            .map(|x| format!("[{0}]{x}[/{0}]", style(statuses[x].0)))
            .collect();
        table.add_row(&[
            cluster_label(&ctx, c),
            cluster_score(c, &statuses).to_string(),
            parts.join(" "),
        ]);
    }
    print_table(&console, &table);

    let mut chosen = &ranked[0];
    if let Some(name) = &cluster_name {
        match ranked
            .iter()
            .find(|c| cluster_label(&ctx, c).split('+').any(|g| g == name))
        {
            Some(c) => chosen = c,
            None => {
                console.print(&format!("[red]no rusty cluster named '{name}'[/red]"));
                return;
            }
        }
    }
    let label = cluster_label(&ctx, chosen);
    console.print(&format!(
        "\n[bold]Deep dive: {label}[/bold] — {} rusty moves, score {}",
        chosen.len(),
        cluster_score(chosen, &statuses)
    ));
    let steps = plan_dive(&ctx, chosen, &statuses, &pv, &ev, &asleep, n, today);
    let dodged = ev.dodged_nodes();
    for (i, (target, status, pnum, reason)) in steps.iter().enumerate() {
        let st = style(*status);
        match pnum {
            Some(p) => console.print(&format!(
                "  {}. [bold]{p}. {}[/bold] — [{st}]{status}[/{st}] [bold]{target}[/bold] ({reason})",
                i + 1,
                pv.map.get(p).map(|x| x.title.as_str()).unwrap_or("")
            )),
            None => console.print(&format!(
                "  {}. `make drill {target}` — [{st}]{status}[/{st}] [bold]{target}[/bold] ({reason})",
                i + 1
            )),
        }
        if pnum.is_some() && dodged.contains_key(target) && ctx.drills_dir().join(target).is_dir() {
            console.print(&format!("     [yellow]drill FIRST — a drill can't be dodged: `make drill {target}`[/yellow]"));
        }
    }
    console.print("\n[dim]Work top-down; `make solved` after each, then re-run `make dive` — the plan re-derives from fresh evidence.[/dim]");
}
