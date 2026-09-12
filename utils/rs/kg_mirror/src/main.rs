// kg_mirror - mirror the graph JSON into graph/leet.db (sqlite) for ad-hoc SQL.
//
// Read-only, rebuilt from scratch on every run - nothing reads it back.
// The JSON stays the source of truth; this is a playground.
//
//     make mirror
//     sqlite3 graph/leet.db
//
// Tables
//     nodes(id, name, "group", added, desc, hint, drill)
//     prereqs(node_id, prereq_id)               node_id needs prereq_id first
//     node_refs(node_id, path)                  dsa/ files the node points at
//     problems(num, title, difficulty, source, note, banned)
//     steps(num, pos, node_id)                  the nodes a problem uses, in order
//     alt_steps(num, walk, pos, node_id)        alternative orderings, walk = which one
//     problem_after(num, after_id)              serve `after_id` before `num`
//     drills(id, title, path, node)             one bank drill (drills/<node>/*.py), id = d14
//     drill_trains(id, node_id)                 the nodes a drill evidences (drills.json "trains")
//     drill_after(id, after_id)                 serve `after_id` before the drill
//     problem_unmapped(num, text)               moves no node names yet
//     solves(file, date, problem, assist, note, followup)
//                                               one solve or drill file (evidence.json)
//     verdicts(file, node_id, verdict)          one node's verdict inside one solve
//     solve_unmapped(file, text)
//
// `assist` is always filled: 'none' when the record has no assist field.
// `problem` is 'drill' for drill files, else the LeetCode number as text.
// `followup` is 'solved' or 'not solved' when the statement asked one, else NULL.
// An `after_id` is a problem number, a drill id, or a node id (one relation,
// kg::bank::warm decides when it is met).
//
// Ported from utils/kg/kg_mirror (Python) on 2026-09-12. The Python read
// an "alt_steps" key the problems never carried (they say "alt_walks"), so
// alt_steps stayed empty; kept as it was.

use kg::ctx::Ctx;
use kg::data::{assist_weight, load_envrc, repo_root, value_str};
use kg::pyjson;
use rusqlite::{params, Connection};
use serde_json::Value;

const SCHEMA: &str = r#"
CREATE TABLE nodes (
    id TEXT PRIMARY KEY, name TEXT, "group" TEXT, added TEXT,
    desc TEXT, hint TEXT, drill TEXT);
CREATE TABLE prereqs (node_id TEXT, prereq_id TEXT, PRIMARY KEY (node_id, prereq_id));
CREATE TABLE node_refs (node_id TEXT, path TEXT);
CREATE TABLE problems (
    num TEXT PRIMARY KEY, title TEXT, difficulty TEXT, source TEXT,
    note TEXT, banned INTEGER NOT NULL DEFAULT 0);
CREATE TABLE steps (num TEXT, pos INTEGER, node_id TEXT, PRIMARY KEY (num, pos));
CREATE TABLE alt_steps (num TEXT, walk INTEGER, pos INTEGER, node_id TEXT, PRIMARY KEY (num, walk, pos));
CREATE TABLE problem_after (num TEXT, after_id TEXT, PRIMARY KEY (num, after_id));
CREATE TABLE drills (id TEXT PRIMARY KEY, title TEXT, path TEXT, node TEXT);
CREATE TABLE drill_trains (id TEXT, node_id TEXT, PRIMARY KEY (id, node_id));
CREATE TABLE drill_after (id TEXT, after_id TEXT, PRIMARY KEY (id, after_id));
CREATE TABLE problem_unmapped (num TEXT, text TEXT);
CREATE TABLE solves (file TEXT PRIMARY KEY, date TEXT, problem TEXT, assist TEXT, note TEXT, followup TEXT);
CREATE TABLE verdicts (file TEXT, node_id TEXT, verdict TEXT, PRIMARY KEY (file, node_id));
CREATE TABLE solve_unmapped (file TEXT, text TEXT);
CREATE INDEX verdicts_node ON verdicts (node_id);
CREATE INDEX solves_date ON solves (date);
CREATE INDEX steps_node ON steps (node_id);
"#;

/// A JSON field as sqlite text, NULL when absent or null.
fn text(v: &Value, key: &str) -> Option<String> {
    match v.get(key) {
        None | Some(Value::Null) => None,
        Some(x) => Some(value_str(x)),
    }
}

fn list<'a>(v: &'a Value, key: &str) -> Vec<&'a Value> {
    v.get(key)
        .and_then(Value::as_array)
        .map(|a| a.iter().collect())
        .unwrap_or_default()
}

/// kg_lib.assist_of(rec): the solve's heaviest assist level, 'none' when
/// the field is absent.
fn assist_of(rec: &Value) -> String {
    match rec.get("assist") {
        Some(Value::Object(o)) => o
            .values()
            .filter_map(Value::as_str)
            .filter(|l| matches!(*l, "none" | "hint" | "walkthrough" | "learning"))
            .max_by(|a, b| assist_weight(a).partial_cmp(&assist_weight(b)).unwrap())
            .unwrap_or("none")
            .to_string(),
        Some(Value::String(s))
            if matches!(s.as_str(), "none" | "hint" | "walkthrough" | "learning") =>
        {
            s.clone()
        }
        _ => "none".to_string(),
    }
}

fn main() -> rusqlite::Result<()> {
    let root = repo_root();
    load_envrc(&root);
    let (ctx, _) = Ctx::load(root);
    let graph = ctx.graph_dir();
    let nodes = pyjson::load(&graph.join("nodes.json")).expect("nodes.json");
    let problems = pyjson::load(&graph.join("problems.json")).expect("problems.json");
    let evidence = pyjson::load(&graph.join("evidence.json")).expect("evidence.json");
    let db = graph.join("leet.db");
    let _ = std::fs::remove_file(&db);
    let con = Connection::open(&db)?;
    con.execute_batch(SCHEMA)?;

    for n in list(&nodes, "nodes") {
        let nid = value_str(&n["id"]);
        con.execute(
            "INSERT INTO nodes VALUES (?,?,?,?,?,?,?)",
            params![
                nid,
                text(n, "name"),
                text(n, "group"),
                text(n, "added"),
                text(n, "desc"),
                text(n, "hint"),
                text(n, "drill")
            ],
        )?;
        for p in list(n, "prereqs") {
            con.execute(
                "INSERT INTO prereqs VALUES (?,?)",
                params![nid, value_str(p)],
            )?;
        }
        for r in list(n, "refs") {
            con.execute(
                "INSERT INTO node_refs VALUES (?,?)",
                params![nid, value_str(r)],
            )?;
        }
    }

    // the evidenced view (kg_lib.load_problems): entries without the draft flag
    for (num, p) in problems["problems"].as_object().expect("problems{}") {
        if p.get("draft").is_some_and(kg::data::truthy) {
            continue;
        }
        con.execute(
            "INSERT INTO problems VALUES (?,?,?,?,?,?)",
            params![
                num,
                text(p, "title"),
                text(p, "difficulty"),
                text(p, "source"),
                text(p, "note"),
                i64::from(p.get("banned").is_some_and(kg::data::truthy))
            ],
        )?;
        for (i, m) in list(p, "moves").iter().enumerate() {
            con.execute(
                "INSERT INTO steps VALUES (?,?,?)",
                params![num, i as i64, value_str(m)],
            )?;
        }
        for (w, walk) in list(p, "alt_steps").iter().enumerate() {
            for (i, m) in walk
                .as_array()
                .map(|a| a.iter().collect::<Vec<_>>())
                .unwrap_or_default()
                .iter()
                .enumerate()
            {
                con.execute(
                    "INSERT INTO alt_steps VALUES (?,?,?,?)",
                    params![num, w as i64, i as i64, value_str(m)],
                )?;
            }
        }
        for a in list(p, "after") {
            con.execute(
                "INSERT INTO problem_after VALUES (?,?)",
                params![num, value_str(a)],
            )?;
        }
        for t in list(p, "unmapped") {
            con.execute(
                "INSERT INTO problem_unmapped VALUES (?,?)",
                params![num, value_str(t)],
            )?;
        }
    }

    for path in ctx.every_bank_path().iter() {
        let Some(title) = ctx.drill_title(path) else {
            continue;
        };
        let Some(did) = ctx.drill_id(path) else {
            continue;
        };
        let rel = path
            .strip_prefix(&ctx.root)
            .unwrap_or(path)
            .to_string_lossy()
            .into_owned();
        let node = path
            .parent()
            .and_then(|d| d.file_name())
            .map(|s| s.to_string_lossy().into_owned())
            .unwrap_or_default();
        con.execute(
            "INSERT OR IGNORE INTO drills VALUES (?,?,?,?)",
            params![did, title, rel, node],
        )?;
        for n in ctx.drill_trains(path) {
            con.execute(
                "INSERT OR IGNORE INTO drill_trains VALUES (?,?)",
                params![did, n],
            )?;
        }
        if let Some(d) = ctx.drills.get(&did) {
            for a in &d.after {
                con.execute(
                    "INSERT OR IGNORE INTO drill_after VALUES (?,?)",
                    params![did, a],
                )?;
            }
        }
    }

    for (fname, rec) in evidence["evidence"].as_object().expect("evidence{}") {
        con.execute(
            "INSERT INTO solves VALUES (?,?,?,?,?,?)",
            params![
                fname,
                text(rec, "date"),
                text(rec, "problem"),
                assist_of(rec),
                text(rec, "note"),
                text(rec, "followup")
            ],
        )?;
        if let Some(moves) = rec.get("moves").and_then(Value::as_object) {
            for (m, v) in moves {
                con.execute(
                    "INSERT INTO verdicts VALUES (?,?,?)",
                    params![fname, m, value_str(v)],
                )?;
            }
        }
        for t in list(rec, "unmapped") {
            con.execute(
                "INSERT INTO solve_unmapped VALUES (?,?)",
                params![fname, value_str(t)],
            )?;
        }
    }

    let mut counts = Vec::new();
    for t in [
        "nodes", "prereqs", "problems", "steps", "solves", "verdicts",
    ] {
        let n: i64 = con.query_row(&format!("SELECT count(*) FROM \"{t}\""), [], |r| r.get(0))?;
        counts.push(format!("{n} {t}"));
    }
    drop(con);
    let rel = db
        .strip_prefix(std::env::current_dir().unwrap_or_default())
        .unwrap_or(&db)
        .to_string_lossy()
        .into_owned();
    println!("{rel}: {}", counts.join(", "));
    println!("sqlite3 {rel}");
    Ok(())
}
