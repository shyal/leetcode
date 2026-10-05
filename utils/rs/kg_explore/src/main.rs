// kg_explore - the graph as JSON, for the VS Code explorer (misc/vscode-graph).
//
//   kg_explore graph          # every node, drill and problem, and the id in current.py
//   kg_explore show d10       # one vertex: its files, its reps, what it waits on
//   kg_explore disable d10    # "disabled": true on the drill's drills.json entry
//   kg_explore enable d10     # the flag removed
//
// The explorer computes nothing: status, due dates and holds are read here
// from the same functions the picker uses. A disabled drill is left out of
// every bank listing (Ctx::bank_files); `make drill d10` still serves it.
// A drill that a problem's "after" names cannot be disabled before it has
// cleared the gate (kg::drills::disable_refused_by).

use std::path::Path;

use kg::bank::held_behind;
use kg::clock::{attempt_label, problem_due};
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root};
use kg::drills::{anki_due, disable_refused_by, drill_clean, last_drilled, set_disabled};
use kg::evidence::Evidence;
use kg::status::node_axes;
use serde_json::{json, Value};

fn rel(path: &Path, root: &Path) -> String {
    path.strip_prefix(root)
        .unwrap_or(path)
        .to_string_lossy()
        .into_owned()
}

/// The id of the drill or problem in current.py.
fn current(ctx: &Ctx) -> Option<String> {
    let (_, _, id, title, _) = kg::lang::current_subject(&ctx.root)?;
    if id == "drill" {
        ctx.drill_path(&title).and_then(|p| ctx.drill_id(&p))
    } else {
        Some(id)
    }
}

/// One rep: its date, its solved file, how it went, the help taken, the
/// minutes on the clock when a record carries them.
fn rep(ev: &Evidence, idx: usize) -> Value {
    let (fname, rec) = &ev.recs[idx];
    let verdict = if rec.moves.is_empty() {
        attempt_label(fname, rec)
    } else {
        rec.moves
            .iter()
            .map(|(m, v)| format!("{m}={v}"))
            .collect::<Vec<_>>()
            .join(", ")
    };
    json!({
        "date": rec.date,
        "file": fname,
        "verdict": verdict,
        "assist": rec.assist_any(),
        "minutes": rec.seconds.map(|s| (s as f64 / 60.0 * 10.0).round() / 10.0),
        "note": rec.note,
    })
}

fn drill_reps(ctx: &Ctx, path: &Path, ev: &Evidence) -> Vec<usize> {
    let key = ctx.drill_evidence_key(path);
    let mut reps: Vec<(&str, &str, usize)> = ev
        .drill_reps(&key)
        .iter()
        .map(|&i| {
            let (d, base, ri) = &ev.drills[i];
            (d.as_str(), base.as_str(), *ri)
        })
        .collect();
    reps.sort();
    reps.into_iter().map(|r| r.2).collect()
}

fn problem_reps(pnum: &str, ev: &Evidence) -> Vec<usize> {
    let mut reps = ev.problem_recs(pnum);
    reps.sort();
    reps.into_iter().map(|r| r.2).collect()
}

/// graph/node_notes/<node>/<drill file stem>.*: the drill's reference.
fn reference(ctx: &Ctx, path: &Path) -> Option<String> {
    let stem = path.file_stem()?.to_str()?;
    let node = path.parent()?.file_name()?;
    let dir = ctx.root.join("graph/node_notes").join(node);
    let mut hits: Vec<_> = std::fs::read_dir(dir)
        .ok()?
        .filter_map(Result::ok)
        .map(|e| e.path())
        .filter(|p| p.file_stem().and_then(|s| s.to_str()) == Some(stem))
        .collect();
    hits.sort();
    hits.first().map(|p| rel(p, &ctx.root))
}

fn graph(ctx: &Ctx, ev: &Evidence, pv: &PView) -> Value {
    let today = ctx.today();
    let nodes: Vec<Value> = ctx
        .nodes
        .values()
        .map(|n| {
            let a = node_axes(ctx, &n.id, ev, pv, today);
            json!({
                "id": n.id,
                "name": n.name,
                "group": n.group,
                "status": a.status.to_string(),
                "degree": (a.degree * 100.0).round() / 100.0,
                "prereqs": n.prereqs,
            })
        })
        .collect();
    let drills: Vec<Value> = ctx
        .drills
        .iter()
        .filter_map(|(id, d)| {
            let path = ctx.drill_path(id)?;
            Some(json!({
                "id": id,
                "title": d.title,
                "trains": ctx.drill_trains(&path),
                "after": d.after,
                "disabled": d.disabled,
                "reps": drill_reps(ctx, &path, ev).len(),
                "last": last_drilled(ctx, &path, ev),
                "clean": drill_clean(ctx, &path, ev),
                "due": anki_due(ctx, &path, ev).map(|(d, _)| d.to_string()),
            }))
        })
        .collect();
    let problems: Vec<Value> = ctx
        .ro
        .map
        .iter()
        .map(|(id, p)| {
            json!({
                "id": id,
                "title": p.title,
                "moves": p.moves,
                "after": p.after,
                "reps": ev.problem_recs(id).len(),
            })
        })
        .collect();
    json!({
        "current": current(ctx),
        "today": today.to_string(),
        "nodes": nodes,
        "drills": drills,
        "problems": problems,
    })
}

fn show(ctx: &Ctx, ev: &Evidence, pv: &PView, id: &str) -> Option<Value> {
    let today = ctx.today();
    if let Some(d) = ctx.drills.get(id) {
        let path = ctx.drill_path(id)?;
        let reps: Vec<Value> = drill_reps(ctx, &path, ev)
            .into_iter()
            .map(|i| rep(ev, i))
            .collect();
        let refused: Vec<Value> = disable_refused_by(ctx, id, ev)
            .into_iter()
            .map(|p| {
                let title = ctx.ro.map.get(&p).map(|x| x.title.clone());
                json!({"id": p, "title": title})
            })
            .collect();
        return Some(json!({
            "kind": "drill",
            "id": id,
            "title": d.title,
            "disabled": d.disabled,
            "file": rel(&path, &ctx.root),
            "reference": reference(ctx, &path),
            "trains": ctx.drill_trains(&path),
            "after": d.after,
            "due": anki_due(ctx, &path, ev).map(|(d, _)| d.to_string()),
            "refused_by": refused,
            "reps": reps,
        }));
    }
    if let Some(p) = ctx.ro.map.get(id) {
        let cache = ctx.root.join(".prepare_cache").join(format!("{id}.json"));
        let reps: Vec<Value> = problem_reps(id, ev)
            .into_iter()
            .map(|i| rep(ev, i))
            .collect();
        return Some(json!({
            "kind": "problem",
            "id": id,
            "title": p.title,
            "moves": p.moves,
            "after": p.after,
            "held_behind": held_behind(ctx, id, pv, ev, today),
            "due": problem_due(ev, id).map(|(d, _)| d.to_string()),
            "cache": cache.is_file().then(|| rel(&cache, &ctx.root)),
            "reps": reps,
        }));
    }
    let n = ctx.nodes.get(id)?;
    let a = node_axes(ctx, id, ev, pv, today);
    let bank: Vec<String> = ctx
        .drills
        .keys()
        .filter(|d| {
            ctx.drill_path(d)
                .is_some_and(|p| ctx.drill_trains(&p).iter().any(|t| t == id))
        })
        .cloned()
        .collect();
    Some(json!({
        "kind": "node",
        "id": id,
        "name": n.name,
        "group": n.group,
        "desc": n.desc,
        "status": a.status.to_string(),
        "degree": (a.degree * 100.0).round() / 100.0,
        "carriers": a.carriers,
        "last": a.last.map(|d| d.to_string()),
        "prereqs": n.prereqs,
        "drills": bank,
    }))
}

/// Set or clear the flag; the refusal is one sentence per waiting problem.
fn flag(ctx: &Ctx, ev: &Evidence, id: &str, on: bool) -> Result<(), String> {
    if on {
        let waiting = disable_refused_by(ctx, id, ev);
        if !waiting.is_empty() {
            let names: Vec<String> = waiting
                .iter()
                .map(|p| {
                    let title = ctx.ro.map.get(p).map(|x| x.title.as_str()).unwrap_or("");
                    format!("{p}. {title}")
                })
                .collect();
            return Err(format!(
                "{id} cannot be disabled: {} waits on it, and its reps have not cleared the gate yet.",
                names.join(", ")
            ));
        }
    }
    set_disabled(&ctx.root, id, on)
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let usage = "usage: kg_explore graph | show <id> | disable <drill id> | enable <drill id>";
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let pv = PView::new(ctx.evidenced());
    let ev = Evidence::new(recs);
    let strs: Vec<&str> = args.iter().map(String::as_str).collect();
    match strs.as_slice() {
        ["graph"] => println!("{}", graph(&ctx, &ev, &pv)),
        ["show", id] => match show(&ctx, &ev, &pv, id) {
            Some(v) => println!("{v}"),
            None => {
                eprintln!("{id} is not a node, a drill or a problem.");
                std::process::exit(1);
            }
        },
        [verb @ ("disable" | "enable"), id] => {
            if let Err(e) = flag(&ctx, &ev, id, *verb == "disable") {
                eprintln!("{e}");
                std::process::exit(1);
            }
        }
        _ => {
            eprintln!("{usage}");
            std::process::exit(2);
        }
    }
}
