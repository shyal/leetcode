// kg_today - freeze today's study plan into data/study_plan/<date>.json.
//
//   make today            # build the plan if today's file does not exist
//   make today rebuild    # regenerate deliberately, e.g. after a bad draft
//   kg_today --no-analysis --plan-dir DIR   # the tests: no model call, a scratch dir
//
// The plan file is the determinism boundary: judgment (one claude call that
// reads the recent FAILED solves and turns them into consolidation work) runs
// ONCE per day and is frozen here; from that moment `make today` is idempotent
// and `make next` is a pure function of (plan, evidence). Gitignored - the
// plan is derived state.
//
// Sections, in serve order (the operator's spec):
//   warmup       2 mega-easies, straight from kg_next's session-start rule
//   review       FRAGILE/STALE targets with their carriers (rules 1-2)
//   consolidate  re-attempts / drills the failure analysis prescribes -
//                failures must account for something, not get hopped over
//   create-drill a drill the bank lacks; `make next` just SAYS to create it
//   new          rule 3/4 material, only when nothing above needs the day
//
// Ported from utils/kg/kg_today (Python) on 2026-09-12.

use std::cell::RefCell;
use std::collections::HashSet;

use kg::bank::{carriers_for, unlocks};
use kg::console::Console;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, parse_date, pnum_key, repo_root};
use kg::drills::{drill_gated, drill_held};
use kg::evidence::Evidence;
use kg::git::{is_session_start, sleep_state};
use kg::llm::claude_json;
use kg::pick::{pick, trivial_easies, PickArgs};
use kg::pyjson;
use kg::status::{
    all_statuses, cooled, gentleness, last_solved, owned, Statuses, FRAGILE, SOLID, STALE,
};
use serde_json::{json, Map, Value};

const FAILURE_LOOKBACK_DAYS: i64 = 7;
const MAX_REVIEWS: usize = 2;

/// FAILED solve files from the lookback window, with their code (head for
/// the attempt, tail for the operator's own verdict notes).
fn recent_failures(ctx: &Ctx, ev: &Evidence) -> Vec<(usize, String, String)> {
    let today = ctx.today();
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|a, b| ev.rec(*a).date.cmp(&ev.rec(*b).date)); // stable, as sorted() on the date
    let mut out = Vec::new();
    for i in order {
        let fname = ev.fname(i);
        if !fname.contains("FAILED") {
            continue;
        }
        if (today - parse_date(&ev.rec(i).date)).num_days() > FAILURE_LOOKBACK_DAYS {
            continue;
        }
        let mut code = std::fs::read_to_string(ctx.root.join(fname)).unwrap_or_default();
        let chars: Vec<char> = code.chars().collect();
        if chars.len() > 4500 {
            let head: String = chars[..2500].iter().collect();
            let tail: String = chars[chars.len() - 2000..].iter().collect();
            code = format!("{head}\n# ... (elided) ...\n{tail}");
        }
        out.push((i, fname.to_string(), code));
    }
    out
}

/// The once-a-day judgment call: turn recent failures into consolidation
/// items.
fn failure_analysis(
    ctx: &Ctx,
    ev: &Evidence,
    pv: &PView,
    failures: &[(usize, String, String)],
) -> Result<Value, String> {
    let digests: Vec<String> = failures
        .iter()
        .map(|(i, _, code)| {
            let rec = ev.rec(*i);
            let pnum = rec.problem.clone().unwrap_or_else(|| "?".to_string());
            let title = pv
                .map
                .get(&pnum)
                .map(|p| p.title.clone())
                .unwrap_or_default();
            let moves: Map<String, Value> = rec
                .moves
                .iter()
                .map(|(k, v)| (k.clone(), json!(v)))
                .collect();
            format!(
                "--- FAILED {}: {pnum}. {title}\nevidenced moves: {}\n{code}",
                rec.date,
                pyjson::dumps(&Value::Object(moves), None)
            )
        })
        .collect();
    let mut banked: Vec<&String> = ctx.nodes.keys().filter(|n| ctx.has_drill_bank(n)).collect();
    banked.sort();
    let banked: Vec<&str> = banked.iter().map(|s| s.as_str()).collect();
    let system = format!(
        "You are a training coach turning a leetcode learner's recent FAILED attempts into a short consolidation plan.\n\nTaxonomy of technique moves (use ONLY these ids):\n{}\n\nNodes that already have a drill bank: {}\n\nFor each failure decide what converts it into a wired skill:\n- a re-attempt of the same problem, unaided, once enough days passed (\"consolidate\")\n- reps on an EXISTING drill bank (\"drill\")\n- a NEW drill worth creating because the bank lacks the drill (\"create_drill\") — say exactly what the new drill trains, in 1-2 sentences\n\nRules:\n- Diagnose from the code: recognition (did not see the technique), mechanics (saw it, could not execute), or endurance. A blank file is recognition; near-working code is mechanics.\n- Do NOT prescribe a fresh new Hard.\n- In every \"note\"/\"spec\"/\"why\" text: never reveal a technique the operator's own failed code or notes did not already use or name. Recognizing the move is his rep. Drill node ids are overt (drills are named by what they train) — but a note attached to a PROBLEM re-attempt must not name the move unless his own file already names it.\n- At most 4 items total. Deduplicate: one item per wound.\n\nOutput STRICT JSON, nothing else:\n{{\"consolidate\": [{{\"problem\": \"<num>\", \"note\": \"<one-liner that gives nothing away>\", \"why\": \"<diagnosis>\"}}],\n \"drills\": [{{\"node\": \"<node-id>\", \"why\": \"<diagnosis>\"}}],\n \"create_drills\": [{{\"node\": \"<node-id>\", \"spec\": \"<what the new drill trains>\", \"why\": \"<diagnosis>\"}}]}}",
        ctx.taxonomy_summary(),
        banked.join(", ")
    );
    claude_json(
        &format!("Recent failures:\n\n{}", digests.join("\n\n")),
        &system,
        "sonnet",
        2,
    )
    .map_err(|e| e.to_string())
}

/// Rules 1-2 targets with their carriers, capped - the plan's spaced-review
/// slice, not the whole frontier.
fn review_items(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    taken: &mut HashSet<String>,
) -> Vec<Value> {
    let today = ctx.today();
    let unl = unlocks(ctx, statuses, pv, &HashSet::new());
    let mut rusty: Vec<&String> = ctx
        .nodes
        .keys()
        .filter(|n| matches!(statuses[*n].0, FRAGILE | STALE))
        .collect();
    rusty.sort_by_key(|n| (-unl.get(*n).copied().unwrap_or(0), statuses[*n].1));
    let mut items = Vec::new();
    for target in rusty {
        if items.len() >= MAX_REVIEWS {
            break;
        }
        let (status, last) = statuses[target];
        if drill_gated(ctx, target, status, last, today) {
            if !drill_held(ctx, target, statuses, ev, &HashSet::new()) {
                items.push(json!({"kind": "drill", "node": target, "why": "rusty move with a drill bank — drill until clean"}));
            }
            continue;
        }
        let mut cands: Vec<String> = carriers_for(ctx, target, pv, statuses, ev, today)
            .into_iter()
            .filter(|c| !taken.contains(c) && cooled(ev, c, today))
            .collect();
        if cands.is_empty() {
            continue;
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
        items.push(json!({"kind": "review", "problem": cands[0], "target": target, "why": "spaced review of a rusty move"}));
        taken.insert(cands[0].clone());
    }
    items
}

fn main() {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    if raw.iter().any(|a| a == "-h" || a == "--help") {
        println!("usage: kg_today [--force] [--no-analysis] [--plan-dir DIR]\n\nFreeze today's study plan.\n\n  --force  rebuild even if today's plan exists");
        return;
    }
    let force = raw.iter().any(|a| a == "--force");
    let no_analysis = raw.iter().any(|a| a == "--no-analysis");
    let plan_dir_flag = raw
        .iter()
        .position(|a| a == "--plan-dir")
        .and_then(|i| raw.get(i + 1).cloned());
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let console = Console::full_width();
    let today = ctx.today();
    let plan_dir = plan_dir_flag
        .map(std::path::PathBuf::from)
        .unwrap_or_else(|| ctx.root.join("data/study_plan"));
    let path = plan_dir.join(format!("{}.json", today.format("%Y-%m-%d")));
    if path.exists() && !force {
        let plan = pyjson::load(&path).unwrap_or_else(|| json!({}));
        console.print(&format!(
            "[dim]plan for {} already exists ({} items) — `make next` serves it; `make today rebuild` to regenerate[/dim]",
            plan["date"].as_str().unwrap_or(""),
            plan["items"].as_array().map(Vec::len).unwrap_or(0)
        ));
        return;
    }

    let ev = Evidence::new(recs);
    let pv = PView::new(ctx.evidenced());
    let statuses = all_statuses(&ctx, &ev, today);
    let asleep = sleep_state(&ctx, &pv, &ev);
    let mut items: Vec<Value> = Vec::new();
    let mut taken: HashSet<String> = asleep.iter().cloned().collect();

    // warmups - the same two the session-start rule would serve, and only
    // when that rule would actually fire
    if is_session_start(&ctx) {
        for pnum in trivial_easies(&ctx, &pv, &ev, &statuses, today)
            .into_iter()
            .take(2)
        {
            items.push(json!({"kind": "warmup", "problem": pnum, "why": "session start — juice, not training"}));
            taken.insert(pnum);
        }
    }
    // reviews - capped slice of the rusty frontier
    items.extend(review_items(&ctx, &pv, &ev, &statuses, &mut taken));

    // failure consolidation - the one claude call, frozen into the file
    let failures = recent_failures(&ctx, &ev);
    let mut analysis = json!({});
    if !failures.is_empty() {
        console.print(&format!(
            "[dim]Reading {} recent failure(s) — one claude call, frozen into the plan...[/dim]",
            failures.len()
        ));
        if !no_analysis {
            match failure_analysis(&ctx, &ev, &pv, &failures) {
                Ok(v) => analysis = v,
                Err(e) => console.print(&format!(
                    "[red]failure analysis unavailable ({e}); plan proceeds without consolidation items[/red]"
                )),
            }
        }
    }
    for it in analysis["consolidate"].as_array().into_iter().flatten() {
        let pnum = kg::data::value_str(&it["problem"]);
        if !taken.contains(&pnum) {
            items.push(json!({
                "kind": "consolidate",
                "problem": pnum,
                "note": it.get("note").and_then(Value::as_str).unwrap_or(""),
                "why": it.get("why").and_then(Value::as_str).unwrap_or(""),
            }));
            taken.insert(pnum);
        }
    }
    for it in analysis["drills"].as_array().into_iter().flatten() {
        let nid = it["node"].as_str().unwrap_or("");
        // judgment names the gap, the curve schedules the rep: no drill item
        // for a node that is SOLID on an unaided clean, and the cross-bank
        // hold applies here as it does in review_items
        if ctx.nodes.contains_key(nid)
            && !(statuses[nid].0 == SOLID && owned(&ev, nid))
            && !drill_held(&ctx, nid, &statuses, &ev, &HashSet::new())
        {
            items.push(json!({"kind": "drill", "node": nid, "why": it.get("why").and_then(Value::as_str).unwrap_or("")}));
        }
    }
    for it in analysis["create_drills"].as_array().into_iter().flatten() {
        let nid = it["node"].as_str().unwrap_or("");
        if ctx.nodes.contains_key(nid) {
            items.push(json!({
                "kind": "create-drill",
                "node": nid,
                "spec": it.get("spec").and_then(Value::as_str).unwrap_or(""),
                "why": it.get("why").and_then(Value::as_str).unwrap_or(""),
            }));
        }
    }
    // new ground - only when the day is not already spoken for
    if !items.iter().any(|i| {
        matches!(
            i["kind"].as_str(),
            Some("consolidate") | Some("create-drill")
        )
    }) {
        let pvc = RefCell::new(pv);
        let args = PickArgs {
            asleep: asleep.clone(),
            woken: vec![],
            exclude: taken.clone(),
            session_start: false,
            group: None,
            cram: false,
            early: false,
            assisted: false,
        };
        if let Some(choice) = pick(&ctx, &pvc, &ev, &statuses, &args) {
            if !choice.is_drill()
                && (choice.reason.contains("new") || choice.reason.contains("summit"))
            {
                items.push(json!({"kind": "new", "problem": choice.pnum, "why": choice.reason}));
            }
        }
    }

    let _ = std::fs::create_dir_all(&plan_dir);
    let plan = json!({
        "date": today.format("%Y-%m-%d").to_string(),
        "generated": chrono::Utc::now().with_timezone(&kg::data::manila()).format("%Y-%m-%dT%H:%M:%S").to_string(),
        "items": items,
    });
    pyjson::save(&path, &plan, Some(2)).expect("write the plan");
    let mut counts: Vec<(String, usize)> = Vec::new();
    for it in plan["items"].as_array().into_iter().flatten() {
        let k = it["kind"].as_str().unwrap_or("").to_string();
        match counts.iter_mut().find(|(kk, _)| *kk == k) {
            Some((_, c)) => *c += 1,
            None => counts.push((k, 1)),
        }
    }
    let summary = if counts.is_empty() {
        "empty".to_string()
    } else {
        counts
            .iter()
            .map(|(k, v)| format!("{v} {k}"))
            .collect::<Vec<_>>()
            .join(", ")
    };
    console.print(&format!(
        "[bold]plan for {}[/bold]: {summary}",
        plan["date"].as_str().unwrap_or("")
    ));
    console.print("[dim]`make next` now serves it, in order.[/dim]");
}
