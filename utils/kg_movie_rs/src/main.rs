// kg_movie — animate the technique graph's history into graph/kg_movie.svg.
//
//   make movie                 # render + report
//   make movie 10              # replay the whole history in a 10-second loop
//   kg_movie --open            # render + open the svg
//
// Ported from (and replacing) the retired Python utils/kg_movie, which
// rendered per-day PNG frames and encoded an mp4. This builds ONE pinned
// graphviz layout and replays the same history as pure SMIL animation:
// status fills stepping through daily date ticks, nodes materializing on
// their `added` dates, a bright border on every status change, and each
// solve flashing its problem number in gold next to every move its walk
// exercised, replayed in true within-day order. Pure SMIL (no CSS/JS), so
// it plays inside GitHub's camo/<img> pipeline and loops indefinitely.
// Viewers without SMIL see today's graph as a still.
//
// Statuses are derived, never stored, so the graph's state on any historical
// date is just node_status() (kept in lockstep with utils/kg_lib.py) over the
// evidence recorded up to that date. Screen time is linear calendar time
// (--pace solves for event-rate pacing instead), so the replay runs at the
// same constant speed as the P(pass) chart's linear x-axis and the two stay
// in step. The tail dissolves into the background so the loop has no dead
// frames at the seam. Label placement is chosen at spawn
// from ~20 candidate spots around the node, overlapping nothing graphviz
// drew — nodes, edges, cluster borders and titles — nor any still-fading
// label; the spot is pinned for the label's lifetime.

use std::collections::HashMap;
use std::fmt::Write as _;
use std::path::PathBuf;
use std::process::{Command, Stdio};

use chrono::{Datelike, Duration, NaiveDate};
use serde_json::Value;

use kg_mock::{current_recall, pass_rates, EvRec, PyRandom, OFF_GRAPH0, SCENARIOS};

const DEFAULT_SECONDS: f64 = 50.0;
const END_FADE_S: f64 = 1.2; // loop-closing dissolve, capped by FADE_FRACTION
const FADE_FRACTION: f64 = 0.08; // dissolve shrinks with short movies
const LABEL_LIFE_FRACTION: f64 = 0.04; // label fade as a share of runtime
const LULL_WEIGHT: f64 = 0.25; // screen time a solve-less day gets, in solves

const HEADER_H: f64 = 56.0;
const ERA_STRIP_H: f64 = 6.0; // era timeline along the very top edge
const BG: &str = "#0d1117";
const GOLD: &str = "#ffd75f";
const INK: &str = "#c9d1d9";
const STROKE_DEF: &str = "#30363d";
const LABEL_PT: f64 = 13.0; // the mp4's 19px at 144dpi, in 96dpi svg units
const LABEL_GAP: f64 = 4.0; // px between a node box and its label
const MAX_PROBS: usize = 3; // live labels per node; the oldest gets evicted

const SOLID_WINDOW_DAYS: i64 = 42; // flat fallback when curve.json is absent

// The day the technique graph took over problem picking (commit 54377d3,
// "Technique graph tooling: viz, deterministic picker, drill bank, honest
// readiness"). Everything before it was hand-scheduled; the header names
// the era so the switch reads as the story beat it was.
const ERA_SWITCH: &str = "2026-07-05";
const ERA_PRE: &str = "pre graph scheduling era";
const ERA_GRAPH: &str = "graph scheduling era";
const ERA_PRE_INK: &str = "#8b949e";
const ERA_GRAPH_INK: &str = "#58a6ff";

const SOLID: usize = 0;
const STALE: usize = 1;
const FRAGILE: usize = 2;
const MISSING: usize = 3;
const FILL: [&str; 4] = ["#238636", "#bb8009", "#da3633", "#6e7681"];
const STATUS_NAME: [&str; 4] = ["solid", "stale", "fragile", "missing"];

type Rect = (f64, f64, f64, f64);

// ------------------------------------------------------------------ data --

struct NodeDef {
    id: String,
    group: String,
    prereqs: Vec<String>,
    added: String, // "" = always there
}

struct Curve {
    a: f64,
    b: f64,
    c: f64,
    d: f64,
    beta: f64,
    target: f64,
}

fn find_graph_dir() -> PathBuf {
    let local = PathBuf::from("graph");
    if local.join("nodes.json").exists() {
        return local;
    }
    let mut dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default();
    loop {
        let g = dir.join("graph");
        if g.join("nodes.json").exists() {
            return g;
        }
        if !dir.pop() {
            panic!("graph/ directory not found");
        }
    }
}

fn load_json(path: &PathBuf) -> Value {
    let text = std::fs::read_to_string(path)
        .unwrap_or_else(|e| panic!("cannot read {}: {e}", path.display()));
    serde_json::from_str(&text).unwrap_or_else(|e| panic!("bad json {}: {e}", path.display()))
}

fn assist_weight(a: &str) -> f64 {
    match a {
        "hint" => 0.5,
        "walkthrough" => 1.0,
        "spoiled" => 2.0,
        _ => 0.0,
    }
}

fn assist_of(rec: &Value) -> &str {
    match rec.get("assist").and_then(Value::as_str) {
        Some(a @ ("none" | "hint" | "walkthrough" | "spoiled")) => a,
        _ => "none",
    }
}

// ---------------------------------------------------------- node_status --
// Kept in lockstep with utils/kg_lib.py node_status(): entries sorted by
// (date, verdict, assist); FRAGILE when the most recent evidence is
// struggled/avoided with no clean on or after it, or when no clean exists;
// otherwise the fitted forgetting curve (or the flat window) splits
// SOLID/STALE. A spoiled solve is not recall evidence.

struct NodeReplay {
    entries: Vec<(NaiveDate, String, String)>, // sorted (date, verdict, assist)
    idx: usize,
    cleans: usize,
    struggles: usize,
    assisted: f64,
    last_clean: Option<NaiveDate>,
    last: Option<(NaiveDate, String)>,
}

impl NodeReplay {
    fn advance_to(&mut self, day: NaiveDate) {
        while self.idx < self.entries.len() && self.entries[self.idx].0 <= day {
            let (d, v, a) = self.entries[self.idx].clone();
            self.assisted += assist_weight(&a);
            if v == "clean" && a != "spoiled" {
                self.cleans += 1;
                self.last_clean = Some(d);
            }
            if v == "struggled" {
                self.struggles += 1;
            }
            self.last = Some((d, v));
            self.idx += 1;
        }
    }

    fn status(&self, day: NaiveDate, curve: Option<&Curve>) -> usize {
        let Some((last_date, last_verdict)) = &self.last else {
            return MISSING;
        };
        let clean_covers = self.last_clean.is_some_and(|c| c >= *last_date);
        if (last_verdict == "struggled" || last_verdict == "avoided") && !clean_covers {
            return FRAGILE;
        }
        let Some(last_clean) = self.last_clean else {
            return FRAGILE;
        };
        let gap = (day - last_clean).num_days();
        match curve {
            Some(p) => {
                let s = (p.a + p.b * self.cleans as f64 - p.c * self.struggles as f64
                    - p.d * self.assisted)
                    .exp()
                    .clamp(7.0, 3650.0);
                if (1.0 + gap as f64 / s).powf(-p.beta) >= p.target {
                    SOLID
                } else {
                    STALE
                }
            }
            None => {
                if gap <= SOLID_WINDOW_DAYS {
                    SOLID
                } else {
                    STALE
                }
            }
        }
    }
}

// --------------------------------------------------------------- solves --

// The filename timestamp (second granularity), for true within-day order.
fn filename_ts(fname: &str) -> String {
    let b = fname.as_bytes();
    let digit = |i: usize| i < b.len() && b[i].is_ascii_digit();
    for i in 0..b.len().saturating_sub(11) {
        if digit(i) && digit(i + 1) && digit(i + 2) && digit(i + 3) && b[i + 4] == b'_'
            && digit(i + 5) && digit(i + 6) && b[i + 7] == b'_'
            && digit(i + 8) && digit(i + 9) && b[i + 10] == b'T'
        {
            let mut j = i + 11;
            while j < b.len() && (b[j].is_ascii_digit() || b[j] == b'_') {
                j += 1;
            }
            return fname[i..j].to_string();
        }
    }
    String::new()
}

// date -> [(problem, moves)] in true within-day solve order, first solve of a
// same-day re-solve only. Drills and misc entries carry no leetcode number.
fn solves_by_day(evidence: &serde_json::Map<String, Value>) -> HashMap<String, Vec<(String, Vec<String>)>> {
    let mut by_day: HashMap<String, Vec<(String, String, Vec<String>)>> = HashMap::new();
    for (fname, rec) in evidence {
        let p = rec.get("problem").and_then(Value::as_str).unwrap_or("");
        if !p.chars().next().is_some_and(|c| c.is_ascii_digit()) {
            continue;
        }
        let date = rec["date"].as_str().unwrap().to_string();
        let moves: Vec<String> = rec
            .get("moves")
            .and_then(Value::as_object)
            .map(|m| m.keys().cloned().collect())
            .unwrap_or_default();
        by_day
            .entry(date)
            .or_default()
            .push((filename_ts(fname), p.to_string(), moves));
    }
    let mut out = HashMap::new();
    for (day, mut rows) in by_day {
        rows.sort();
        let mut seen = std::collections::HashSet::new();
        let mut ordered = vec![];
        for (_, p, moves) in rows {
            if seen.insert(p.clone()) {
                ordered.push((p, moves));
            }
        }
        out.insert(day, ordered);
    }
    out
}

// ------------------------------------------------------------- geometry --

fn floats(s: &str) -> Vec<f64> {
    let cleaned: String = s
        .chars()
        .map(|c| if c.is_ascii_digit() || c == '.' || c == '-' || c == '+' { c } else { ' ' })
        .collect();
    cleaned.split_whitespace().filter_map(|t| t.parse().ok()).collect()
}

fn points_bbox(pts: &[f64]) -> Rect {
    let (mut x0, mut y0, mut x1, mut y1) = (f64::MAX, f64::MAX, f64::MIN, f64::MIN);
    for pair in pts.chunks_exact(2) {
        x0 = x0.min(pair[0]);
        x1 = x1.max(pair[0]);
        y0 = y0.min(pair[1]);
        y1 = y1.max(pair[1]);
    }
    (x0, y0, x1, y1)
}

fn overlaps(a: Rect, b: Rect) -> bool {
    a.0 < b.2 && b.0 < a.2 && a.1 < b.3 && b.1 < a.3
}

fn attr<'a>(tag: &'a str, name: &str) -> Option<&'a str> {
    let key = format!("{name}=\"");
    let i = tag.find(&key)? + key.len();
    let j = tag[i..].find('"')? + i;
    Some(&tag[i..j])
}

fn unescape(s: &str) -> String {
    s.replace("&#45;", "-")
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("&amp;", "&")
}

// Positions to try around a node: above > below > right > left, each with
// center/left/right (or top/bottom) alignments, then a farther second ring.
fn candidate_spots(node_box: Rect, w: f64, h: f64) -> Vec<(f64, f64)> {
    let (x0, y0, x1, y1) = node_box;
    let (cx, cy) = ((x0 + x1) / 2.0, (y0 + y1) / 2.0);
    let g = LABEL_GAP;
    let xs = [cx - w / 2.0, x0, x1 - w];
    let mut spots = vec![];
    for &x in &xs {
        spots.push((x, y0 - g - h));
    }
    for &x in &xs {
        spots.push((x, y1 + g));
    }
    for &y in &[cy - h / 2.0, y0, y1 - h] {
        spots.push((x1 + g, y));
    }
    for &y in &[cy - h / 2.0, y0, y1 - h] {
        spots.push((x0 - g - w, y));
    }
    for ring in [13.0, 27.0] {
        spots.push((cx - w / 2.0, y0 - g - h - ring));
        spots.push((cx - w / 2.0, y1 + g + ring));
        spots.push((x1 + g + ring, cy - h / 2.0));
        spots.push((x0 - g - w - ring, cy - h / 2.0));
    }
    spots
}

// Pick a spot touching nothing; least-weighted-overlap fallback. `taken` are
// rectangles of labels still fading: a dying label keeps its ground.
fn place_label(node_box: Rect, w: f64, h: f64, obstacles: &[(Rect, f64)], taken: &[Rect]) -> Rect {
    let vicinity = (node_box.0 - 180.0, node_box.1 - 180.0, node_box.2 + 180.0, node_box.3 + 180.0);
    let near: Vec<&(Rect, f64)> = obstacles.iter().filter(|(r, _)| overlaps(*r, vicinity)).collect();
    let near_taken: Vec<Rect> = taken.iter().copied().filter(|r| overlaps(*r, vicinity)).collect();
    let mut best = None;
    let mut best_bad = f64::MAX;
    for (lx, ly) in candidate_spots(node_box, w, h) {
        let rect = (lx, ly, lx + w, ly + h);
        let mut bad = 0.0;
        for (r, wt) in near.iter().map(|x| **x).chain(near_taken.iter().map(|r| (*r, 5.0))) {
            if overlaps(rect, r) {
                bad += (r.2.min(rect.2) - r.0.max(rect.0)) * (r.3.min(rect.3) - r.1.max(rect.1)) * wt;
            }
        }
        if bad == 0.0 {
            return rect;
        }
        if bad < best_bad {
            best = Some(rect);
            best_bad = bad;
        }
    }
    best.unwrap()
}

fn label_alpha(age_s: f64, life_s: f64) -> f64 {
    if age_s < 0.0 {
        return 0.0;
    }
    let t = age_s / life_s;
    if t >= 1.0 {
        0.0
    } else {
        (1.0 - t).powf(1.4)
    }
}

// ------------------------------------------------------------------ smil --

// Strictly increasing keyTimes or Chrome discards the whole animation.
fn push_key(times: &mut Vec<f64>, t: f64) {
    let t = match times.last() {
        Some(&p) if t <= p => p + 1e-5,
        _ => t,
    };
    times.push(t.min(1.0));
}

// 4 decimals (5ms at a 50s loop), trailing zeros trimmed: keyTimes are the
// bulk of the file, and the movie must stay small so it loads (and starts
// its SMIL clock) nearly in step with the chart svg beside it in the README.
fn fmt_frac(t: f64) -> String {
    let s = format!("{t:.4}");
    let s = s.trim_end_matches('0').trim_end_matches('.');
    if s.is_empty() { "0".to_string() } else { s.to_string() }
}

fn animate(attr_name: &str, calc: &str, values: &[String], key_times: &[f64], dur: f64) -> String {
    let kt: Vec<String> = key_times.iter().map(|t| fmt_frac(*t)).collect();
    format!(
        "<animate attributeName=\"{attr_name}\" calcMode=\"{calc}\" values=\"{}\" keyTimes=\"{}\" dur=\"{dur}s\" repeatCount=\"indefinite\"/>",
        values.join(";"),
        kt.join(";")
    )
}

// One discrete animation from a per-tick value sequence, compressed to its
// change points. None when the value never changes.
fn discrete_track(seq: &[String], tick_frac: &[f64], attr_name: &str, dur: f64) -> Option<String> {
    let mut values = vec![seq[0].clone()];
    let mut times = vec![0.0];
    for i in 1..seq.len() {
        if seq[i] != seq[i - 1] {
            values.push(seq[i].clone());
            push_key(&mut times, tick_frac[i]);
        }
    }
    (values.len() > 1).then(|| animate(attr_name, "discrete", &values, &times, dur))
}

// --------------------------------------------------------------- main --

fn main() {
    let mut seconds = DEFAULT_SECONDS;
    let mut open_after = false;
    let mut pace_calendar = true;
    let mut args = std::env::args().skip(1);
    while let Some(a) = args.next() {
        match a.as_str() {
            "--open" => open_after = true,
            "--pace" => {
                pace_calendar = !matches!(args.next().as_deref(), Some("solves"));
            }
            s => match s.parse::<f64>() {
                Ok(v) if v > 0.0 => seconds = v,
                _ => {
                    eprintln!("usage: kg_movie [seconds] [--pace solves|calendar] [--open]");
                    std::process::exit(2);
                }
            },
        }
    }
    let fade_s = END_FADE_S.min(seconds * FADE_FRACTION);
    let label_life = seconds * LABEL_LIFE_FRACTION;
    let ticks_s = seconds - fade_s;

    let graph = find_graph_dir();
    let nodes_v = load_json(&graph.join("nodes.json"));
    let evidence_v = load_json(&graph.join("evidence.json"));
    let curve = {
        let path = graph.join("curve.json");
        path.exists().then(|| {
            let v = load_json(&path);
            let p = &v["params"];
            Curve {
                a: p["a"].as_f64().unwrap(),
                b: p["b"].as_f64().unwrap(),
                c: p["c"].as_f64().unwrap(),
                d: p.get("d").and_then(Value::as_f64).unwrap_or(0.0),
                beta: p["beta"].as_f64().unwrap(),
                target: v["target_retention"].as_f64().unwrap(),
            }
        })
    };

    let nodes: Vec<NodeDef> = nodes_v["nodes"]
        .as_array()
        .unwrap()
        .iter()
        .map(|n| NodeDef {
            id: n["id"].as_str().unwrap().to_string(),
            group: n["group"].as_str().unwrap().to_string(),
            prereqs: n
                .get("prereqs")
                .and_then(Value::as_array)
                .map(|a| a.iter().filter_map(|v| v.as_str().map(String::from)).collect())
                .unwrap_or_default(),
            added: n.get("added").and_then(Value::as_str).unwrap_or("").to_string(),
        })
        .collect();
    let node_index: HashMap<&str, usize> =
        nodes.iter().enumerate().map(|(i, n)| (n.id.as_str(), i)).collect();
    let evidence = evidence_v["evidence"].as_object().unwrap();

    // ---- date ticks: opening dark frame + every day of the history --------
    let mut solve_days: Vec<&str> = evidence.values().map(|r| r["date"].as_str().unwrap()).collect();
    solve_days.sort_unstable();
    let first = NaiveDate::parse_from_str(solve_days[0], "%Y-%m-%d").unwrap();
    let last = NaiveDate::parse_from_str(solve_days[solve_days.len() - 1], "%Y-%m-%d").unwrap();
    let mut days = vec![];
    let mut d = first - Duration::days(1);
    while d <= last {
        days.push(d);
        d += Duration::days(1);
    }
    let n_ticks = days.len();

    // ---- per-node status/hidden timelines --------------------------------
    let mut replays: Vec<NodeReplay> = nodes
        .iter()
        .map(|n| {
            let mut entries = vec![];
            for rec in evidence.values() {
                if let Some(v) = rec.get("moves").and_then(|m| m.get(&n.id)).and_then(Value::as_str)
                {
                    let d = NaiveDate::parse_from_str(rec["date"].as_str().unwrap(), "%Y-%m-%d")
                        .unwrap();
                    entries.push((d, v.to_string(), assist_of(rec).to_string()));
                }
            }
            entries.sort();
            NodeReplay { entries, idx: 0, cleans: 0, struggles: 0, assisted: 0.0, last_clean: None, last: None }
        })
        .collect();

    let mut status_tl: Vec<Vec<usize>> = vec![Vec::with_capacity(n_ticks); nodes.len()];
    for &day in &days {
        for (ni, rep) in replays.iter_mut().enumerate() {
            rep.advance_to(day);
            status_tl[ni].push(rep.status(day, curve.as_ref()));
        }
    }
    // nodes appear when they were actually introduced; no field = always there
    let first_vis: Vec<usize> = nodes
        .iter()
        .map(|n| days.iter().position(|d| n.added.as_str() <= d.to_string().as_str()).unwrap_or(0))
        .collect();

    // ---- pacing: screen time per tick, in units of "one solve" -----------
    let by_day = solves_by_day(evidence);
    let weights: Vec<f64> = days
        .iter()
        .map(|d| {
            if pace_calendar {
                1.0
            } else {
                by_day.get(&d.to_string()).map_or(0.0, |s| s.len() as f64) + LULL_WEIGHT
            }
        })
        .collect();
    let total_w: f64 = weights.iter().sum();
    let mut tick_t = Vec::with_capacity(n_ticks); // start seconds per tick
    let mut cum = 0.0;
    for w in &weights {
        tick_t.push(cum / total_w * ticks_s);
        cum += w;
    }
    let tick_len: Vec<f64> = (0..n_ticks)
        .map(|i| if i + 1 < n_ticks { tick_t[i + 1] - tick_t[i] } else { ticks_s - tick_t[i] })
        .collect();
    let tick_frac: Vec<f64> = tick_t.iter().map(|t| t / seconds).collect();

    // ---- the pinned layout ------------------------------------------------
    let mut groups: Vec<(&str, Vec<usize>)> = vec![];
    for (i, n) in nodes.iter().enumerate() {
        match groups.iter_mut().find(|(g, _)| *g == n.group) {
            Some((_, m)) => m.push(i),
            None => groups.push((&n.group, vec![i])),
        }
    }
    let today_i = n_ticks - 1;
    let mut dot = String::new();
    dot.push_str("digraph kg {\n");
    dot.push_str(" graph [rankdir=TB, bgcolor=\"#0d1117\", fontname=\"Helvetica\", compound=true, ranksep=\"0.6\", nodesep=\"0.25\"];\n");
    dot.push_str(" node [shape=box, style=\"rounded,filled\", fontname=\"Helvetica\", fontsize=11, fontcolor=white, color=\"#30363d\", margin=\"0.12,0.06\", penwidth=2];\n");
    dot.push_str(" edge [color=\"#8b949e\", arrowsize=0.6];\n");
    for (group, members) in &groups {
        writeln!(dot, " subgraph \"cluster_{group}\" {{").unwrap();
        writeln!(dot, "  label=\"{group}\"; fontcolor=\"#8b949e\"; color=\"#30363d\"; style=rounded; fontname=\"Helvetica\";").unwrap();
        for &ni in members {
            // static fill = today's status: the still that non-SMIL viewers see
            writeln!(
                dot,
                "  \"{}\" [label=\"{}\", fillcolor=\"{}\"];",
                nodes[ni].id,
                nodes[ni].id.replacen('-', "-\\n", 1),
                FILL[status_tl[ni][today_i]]
            )
            .unwrap();
        }
        dot.push_str(" }\n");
    }
    for n in &nodes {
        for p in &n.prereqs {
            if node_index.contains_key(p.as_str()) {
                writeln!(dot, " \"{p}\" -> \"{}\";", n.id).unwrap();
            }
        }
    }
    dot.push_str(" subgraph cluster_legend {\n  label=\"legend\"; fontcolor=\"#8b949e\"; color=\"#30363d\"; style=rounded;\n");
    for s in [SOLID, STALE, FRAGILE, MISSING] {
        writeln!(dot, "  legend_{} [label=\"{}\", fillcolor=\"{}\"];", STATUS_NAME[s], STATUS_NAME[s], FILL[s]).unwrap();
    }
    dot.push_str(" }\n}\n");

    let child = Command::new("dot")
        .arg("-Tsvg")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("graphviz `dot` not found");
    use std::io::Write as _;
    child.stdin.as_ref().unwrap().write_all(dot.as_bytes()).unwrap();
    let out = child.wait_with_output().unwrap();
    assert!(out.status.success(), "dot failed");
    let svg = String::from_utf8(out.stdout).unwrap();

    // ---- pass 1: geometry from the svg itself ----------------------------
    // Obstacles cover everything graphviz drew: node boxes (legend included),
    // cluster borders and titles, and every edge spline marched into a
    // corridor of small rects. Weights let the fallback scoring prefer
    // grazing a thin edge over covering text if no spot is free.
    let mut boxes: HashMap<String, Rect> = HashMap::new();
    let mut obstacles: Vec<(Rect, f64)> = vec![];
    let mut pos = 0;
    while let Some(rel) = svg[pos..].find("<g id=\"") {
        let gstart = pos + rel;
        let tag_end = svg[gstart..].find('>').unwrap() + gstart + 1;
        let open_tag = &svg[gstart..tag_end];
        let class = attr(open_tag, "class").unwrap_or("");
        if class == "graph" {
            pos = tag_end;
            continue;
        }
        let gend = svg[tag_end..].find("</g>").unwrap() + tag_end + 4;
        let block = &svg[tag_end..gend];
        let title = block
            .find("<title>")
            .map(|i| {
                let j = block[i..].find("</title>").unwrap() + i;
                unescape(&block[i + 7..j])
            })
            .unwrap_or_default();
        match class {
            "node" => {
                if let Some(i) = block.find(" d=\"") {
                    let j = block[i + 4..].find('"').unwrap() + i + 4;
                    let bb = points_bbox(&floats(&block[i + 4..j]));
                    boxes.insert(title, bb);
                    obstacles.push((bb, 5.0));
                }
            }
            "cluster" => {
                if let Some(i) = block.find(" d=\"") {
                    let j = block[i + 4..].find('"').unwrap() + i + 4;
                    let (x0, y0, x1, y1) = points_bbox(&floats(&block[i + 4..j]));
                    for strip in [
                        (x0 - 2.0, y0 - 2.0, x1 + 2.0, y0 + 2.0),
                        (x0 - 2.0, y1 - 2.0, x1 + 2.0, y1 + 2.0),
                        (x0 - 2.0, y0 - 2.0, x0 + 2.0, y1 + 2.0),
                        (x1 - 2.0, y0 - 2.0, x1 + 2.0, y1 + 2.0),
                    ] {
                        obstacles.push((strip, 2.0));
                    }
                }
                if let Some(i) = block.find("<text") {
                    let te = block[i..].find('>').unwrap() + i;
                    let tag = &block[i..te];
                    let cj = block[te..].find("</text>").unwrap() + te;
                    let chars = unescape(&block[te + 1..cj]).chars().count() as f64;
                    let x: f64 = attr(tag, "x").and_then(|v| v.parse().ok()).unwrap_or(0.0);
                    let y: f64 = attr(tag, "y").and_then(|v| v.parse().ok()).unwrap_or(0.0);
                    let w = chars * 14.0 * 0.55;
                    obstacles.push(((x - w / 2.0, y - 12.0, x + w / 2.0, y + 3.0), 5.0));
                }
            }
            "edge" => {
                if let Some(i) = block.find(" d=\"") {
                    let j = block[i + 4..].find('"').unwrap() + i + 4;
                    let pts = floats(&block[i + 4..j]);
                    for pair in pts.windows(4).step_by(2) {
                        let (ax, ay, bx, by) = (pair[0], pair[1], pair[2], pair[3]);
                        let steps = (((bx - ax).powi(2) + (by - ay).powi(2)).sqrt() / 9.0).max(1.0) as usize;
                        for k in 0..=steps {
                            let mx = ax + (bx - ax) * k as f64 / steps as f64;
                            let my = ay + (by - ay) * k as f64 / steps as f64;
                            obstacles.push(((mx - 3.0, my - 3.0, mx + 3.0, my + 3.0), 1.0));
                        }
                    }
                }
            }
            _ => {}
        }
        pos = gend;
    }

    // ---- solve labels: spawn, evict, place -------------------------------
    struct Label {
        node: String,
        text: String,
        rect: Rect,
        born: f64,
    }
    let mut active: Vec<usize> = vec![]; // indices into labels still fading
    let mut labels: Vec<Label> = vec![];
    let line_h = LABEL_PT + 4.0;
    for (i, day) in days.iter().enumerate() {
        let t0 = tick_t[i];
        active.retain(|&li| label_alpha(t0 - labels[li].born, label_life) > 0.0);
        let Some(day_solves) = by_day.get(&day.to_string()) else { continue };
        for (k, (prob, moves)) in day_solves.iter().enumerate() {
            let born = t0 + k as f64 * tick_len[i] / day_solves.len() as f64;
            for node_id in moves {
                let Some(&node_box) = boxes.get(node_id) else { continue };
                let alive_here: Vec<usize> =
                    active.iter().copied().filter(|&li| &labels[li].node == node_id).collect();
                if alive_here.len() >= MAX_PROBS {
                    // evict the oldest on a hot node
                    let oldest = *alive_here
                        .iter()
                        .min_by(|&&a, &&b| labels[a].born.total_cmp(&labels[b].born))
                        .unwrap();
                    active.retain(|&li| li != oldest);
                }
                let w = prob.chars().count() as f64 * LABEL_PT * 0.61;
                let taken: Vec<Rect> = active.iter().map(|&li| labels[li].rect).collect();
                let rect = place_label(node_box, w, line_h, &obstacles, &taken);
                labels.push(Label { node: node_id.clone(), text: prob.clone(), rect, born });
                active.push(labels.len() - 1);
            }
        }
    }

    // ---- pass 2: rewrite the svg with the animation tracks ---------------
    let vb_i = svg.find("viewBox=\"").unwrap() + 9;
    let vb_j = svg[vb_i..].find('"').unwrap() + vb_i;
    let vb = floats(&svg[vb_i..vb_j]);
    let (width, height) = (vb[2], vb[3]);
    let new_h = height + HEADER_H;
    let dur = seconds;

    let mut out_svg = String::with_capacity(svg.len() * 2);
    let header_end = svg.find("<g id=\"graph0\"").unwrap();
    let mut head = svg[..header_end].to_string();
    head = head.replace(
        &format!("height=\"{}pt\"", height as i64),
        &format!("height=\"{}pt\"", new_h.ceil() as i64),
    );
    head = head.replace(
        &format!("viewBox=\"{}\"", &svg[vb_i..vb_j]),
        &format!("viewBox=\"0.00 0.00 {width:.2} {new_h:.2}\""),
    );
    out_svg.push_str(&head);
    // full-canvas background: the graph's own bg polygon doesn't cover the header
    writeln!(out_svg, "<rect x=\"0\" y=\"0\" width=\"{width:.0}\" height=\"{new_h:.0}\" fill=\"{BG}\"/>").unwrap();

    let g_tag_end = svg[header_end..].find('>').unwrap() + header_end + 1;
    let g_open = svg[header_end..g_tag_end]
        .replace(&format!("translate(4 {})", height - 4.0), &format!("translate(4 {})", height - 4.0 + HEADER_H));
    out_svg.push_str(&g_open);

    let body_end = svg.rfind("</g>").unwrap();
    let mut pos = g_tag_end;
    while let Some(rel) = svg[pos..body_end].find("<g id=\"") {
        let gstart = pos + rel;
        out_svg.push_str(&svg[pos..gstart]);
        let tag_end = svg[gstart..].find('>').unwrap() + gstart + 1;
        let open_tag = &svg[gstart..tag_end];
        let class = attr(open_tag, "class").unwrap_or("");
        let gend = svg[tag_end..].find("</g>").unwrap() + tag_end + 4;
        let block = &svg[tag_end..gend];
        let title = block
            .find("<title>")
            .map(|i| {
                let j = block[i..].find("</title>").unwrap() + i;
                unescape(&block[i + 7..j])
            })
            .unwrap_or_default();
        out_svg.push_str(open_tag);
        match class {
            "node" if node_index.contains_key(title.as_str()) => {
                let ni = node_index[title.as_str()];
                let mut tracks = String::new();
                // materialize on the `added` date
                if first_vis[ni] > 0 {
                    let mut times = vec![0.0];
                    push_key(&mut times, tick_frac[first_vis[ni]]);
                    tracks.push_str(&animate("opacity", "discrete", &["0".into(), "1".into()], &times, dur));
                }
                let fills: Vec<String> = status_tl[ni].iter().map(|&s| FILL[s].to_string()).collect();
                let fill_track = discrete_track(&fills, &tick_frac, "fill", dur);
                // bright border on the ticks where the status changed or the
                // node was just introduced
                let strokes: Vec<String> = (0..n_ticks)
                    .map(|t| {
                        let vis = t >= first_vis[ni];
                        let hot = t > 0
                            && vis
                            && (status_tl[ni][t] != status_tl[ni][t - 1] || first_vis[ni] == t);
                        (if hot { INK } else { STROKE_DEF }).to_string()
                    })
                    .collect();
                let stroke_track = discrete_track(&strokes, &tick_frac, "stroke", dur);
                let mut inner = block.to_string();
                if fill_track.is_some() || stroke_track.is_some() {
                    if let Some(i) = inner.find("<path ") {
                        let j = inner[i..].find("/>").unwrap() + i;
                        let mut kids = String::from(">");
                        if let Some(t) = fill_track {
                            kids.push_str(&t);
                        }
                        if let Some(t) = stroke_track {
                            kids.push_str(&t);
                        }
                        kids.push_str("</path>");
                        inner.replace_range(j..j + 2, &kids);
                    }
                }
                out_svg.push_str(&tracks);
                out_svg.push_str(&inner);
            }
            "edge" => {
                // an edge exists once both its endpoints do
                let vis = title
                    .split_once("->")
                    .map(|(a, b)| {
                        let fa = node_index.get(a.trim()).map_or(0, |&i| first_vis[i]);
                        let fb = node_index.get(b.trim()).map_or(0, |&i| first_vis[i]);
                        fa.max(fb)
                    })
                    .unwrap_or(0);
                if vis > 0 {
                    let mut times = vec![0.0];
                    push_key(&mut times, tick_frac[vis]);
                    out_svg.push_str(&animate("opacity", "discrete", &["0".into(), "1".into()], &times, dur));
                }
                out_svg.push_str(block);
            }
            _ => out_svg.push_str(block),
        }
        pos = gend;
    }
    out_svg.push_str(&svg[pos..body_end]);

    // gold solve labels, inside the graph transform so they share node coords.
    // Shared styling lives on the outer group, and every label of one solve
    // (same problem, same birth, one per exercised move) shares a single
    // fade animation on an inner group — 1000+ labels, every byte repeats.
    writeln!(out_svg, "<g font-family=\"Menlo,monospace\" font-size=\"{LABEL_PT:.0}\" fill=\"{GOLD}\">").unwrap();
    let mut li = 0;
    while li < labels.len() {
        let l = &labels[li];
        let mut lj = li + 1;
        while lj < labels.len() && labels[lj].born == l.born && labels[lj].text == l.text {
            lj += 1;
        }
        let lb = l.born / dur;
        let lf = label_life / dur;
        let mut times = vec![];
        let mut values = vec![];
        if lb > 0.0004 {
            times.push(0.0);
            values.push("0".to_string());
            push_key(&mut times, lb - 0.0002);
            values.push("0".to_string());
        }
        push_key(&mut times, lb.max(0.0));
        values.push("1".to_string());
        for (u, a) in [(0.25, 0.669), (0.5, 0.379), (0.75, 0.144), (1.0, 0.0)] {
            let t = lb + u * lf;
            if t >= 1.0 {
                break;
            }
            push_key(&mut times, t);
            values.push(format!("{a}"));
        }
        // linear keyTimes must end exactly at 1
        push_key(&mut times, 1.0);
        values.push(format!("{:.3}", label_alpha((1.0 - lb) * dur, label_life)));
        if times[0] != 0.0 {
            times.insert(0, 0.0);
            values.insert(0, "0".to_string());
        }
        write!(
            out_svg,
            "<g opacity=\"0\">{}",
            animate("opacity", "linear", &values, &times, dur)
        )
        .unwrap();
        for l in &labels[li..lj] {
            write!(out_svg, "<text x=\"{:.0}\" y=\"{:.0}\">{}</text>", l.rect.0, l.rect.3 - 3.0, l.text).unwrap();
        }
        out_svg.push_str("</g>\n");
        li = lj;
    }
    out_svg.push_str("</g>\n</g>\n");

    // header: the date and status counts, one flashcard per tick like the mp4's
    // title line — outside the graph transform, in plain canvas coordinates
    writeln!(
        out_svg,
        "<g text-anchor=\"middle\" font-family=\"Helvetica,sans-serif\" font-size=\"20\" fill=\"{INK}\">"
    )
    .unwrap();
    let mut hidden_counts = 0;
    for i in 0..n_ticks {
        let mut counts = [0usize; 4];
        for ni in 0..nodes.len() {
            if i >= first_vis[ni] {
                counts[status_tl[ni][i]] += 1;
            } else {
                hidden_counts += 1;
            }
        }
        let title_text = format!(
            "{}   ·   {} solid  {} stale  {} fragile  {} missing",
            days[i], counts[SOLID], counts[STALE], counts[FRAGILE], counts[MISSING]
        );
        let ts = tick_frac[i];
        let te = if i + 1 < n_ticks { tick_frac[i + 1] } else { 1.0 };
        let (values, times) = if ts <= 0.0 {
            (vec!["1".to_string(), "0".to_string()], vec![0.0, te])
        } else {
            let mut t = vec![0.0];
            push_key(&mut t, ts);
            if i + 1 < n_ticks {
                push_key(&mut t, te);
                (vec!["0".into(), "1".into(), "0".into()], t)
            } else {
                (vec!["0".into(), "1".into()], t)
            }
        };
        writeln!(
            out_svg,
            "<text x=\"{:.0}\" y=\"44\" opacity=\"0\">{title_text}{}</text>",
            width / 2.0,
            animate("opacity", "discrete", &values, &times, dur)
        )
        .unwrap();
    }
    out_svg.push_str("</g>\n");
    let _ = hidden_counts;

    // era label, top left: hand-scheduled until the graph tooling landed,
    // graph-scheduled after — one flip, pinned to the switch date's tick
    let switch = days.iter().position(|d| d.to_string().as_str() >= ERA_SWITCH);
    let era_frac = switch.map(|i| tick_frac[i]);
    for (label, ink, show) in [
        (ERA_PRE, ERA_PRE_INK, era_frac != Some(0.0)),
        (ERA_GRAPH, ERA_GRAPH_INK, switch.is_some()),
    ] {
        if !show {
            continue;
        }
        let track = match era_frac {
            Some(f) if f > 0.0 => {
                let mut times = vec![0.0];
                push_key(&mut times, f);
                let values = if label == ERA_PRE {
                    vec!["1".to_string(), "0".to_string()]
                } else {
                    vec!["0".to_string(), "1".to_string()]
                };
                animate("opacity", "discrete", &values, &times, dur)
            }
            _ => String::new(), // the whole movie is one era: static label
        };
        writeln!(
            out_svg,
            "<text x=\"20\" y=\"44\" font-family=\"Helvetica,sans-serif\" font-size=\"34\" font-weight=\"bold\" fill=\"{ink}\" opacity=\"{}\">{label}{track}</text>",
            if label == ERA_PRE && era_frac.is_some() { 0 } else { 1 }
        )
        .unwrap();
    }

    // era strip: the loop's own timeline along the top edge — grey for the
    // hand-scheduled stretch, blue once the graph picker takes over, a
    // playhead sweeping across so the switch reads at any thumbnail size
    let split_x = era_frac.map_or(width, |f| f * width);
    if split_x > 0.0 {
        writeln!(out_svg, "<rect x=\"0\" y=\"0\" width=\"{split_x:.1}\" height=\"{ERA_STRIP_H}\" fill=\"{ERA_PRE_INK}\" opacity=\"0.55\"/>").unwrap();
    }
    if switch.is_some() && split_x < width {
        writeln!(
            out_svg,
            "<rect x=\"{split_x:.1}\" y=\"0\" width=\"{:.1}\" height=\"{ERA_STRIP_H}\" fill=\"{ERA_GRAPH_INK}\" opacity=\"0.9\"/>",
            width - split_x
        )
        .unwrap();
    }
    writeln!(
        out_svg,
        "<rect x=\"-2\" y=\"0\" width=\"4\" height=\"{:.0}\" fill=\"{INK}\"><animate attributeName=\"x\" calcMode=\"linear\" values=\"-2;{:.1}\" keyTimes=\"0;1\" dur=\"{dur}s\" repeatCount=\"indefinite\"/></rect>",
        ERA_STRIP_H + 8.0,
        width - 2.0
    )
    .unwrap();

    // Close the loop by dissolving into the background rather than freezing:
    // dead frames are exactly what a looping animation makes you stare at, and
    // a hard cut from the fully lit graph to the dark opening is jarring. The
    // overlay ramps up over the fade window and snaps away at the seam, where
    // dark-to-dark has nothing to catch on.
    let fade_from = ticks_s / dur;
    writeln!(
        out_svg,
        "<rect x=\"0\" y=\"0\" width=\"{width:.0}\" height=\"{new_h:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
        animate(
            "opacity",
            "linear",
            &["0".into(), "0".into(), "1".into()],
            &[0.0, fade_from, 1.0],
            dur
        )
    )
    .unwrap();
    out_svg.push_str("</svg>\n");

    let out_path = graph.join("kg_movie.svg");
    std::fs::write(&out_path, &out_svg).unwrap();
    println!(
        "wrote {} — {} ticks, {} solve labels, {:.1}s loop ({:.1}s dissolve), {:.0}KB",
        out_path.display(),
        n_ticks,
        labels.len(),
        seconds,
        fade_s,
        out_svg.len() as f64 / 1024.0
    );
    if open_after {
        let _ = Command::new("open").arg(&out_path).status();
    }

    // ---- P(pass) history chart: graph/kg_pass.svg ------------------------
    // The README's "It seems to be working" chart, animated: the same weekly
    // replay update_readme.py used to render with matplotlib (kg_lib math,
    // Random(42), 4000 samples — reproduced bit-for-bit by the kg_mock lib),
    // drawn as SMIL that reveals left-to-right on the SAME clock as
    // kg_movie.svg, so the two loops tell one story in sync. A playhead
    // line sweeps the calendar axis at the movie's current date; the era
    // banner and label flip on the same tick as the movie's.
    let Some(cv) = curve.as_ref() else {
        println!("no graph/curve.json — kg_pass.svg skipped");
        return;
    };
    let mcurve = kg_mock::Curve { a: cv.a, b: cv.b, c: cv.c, d: cv.d, beta: cv.beta, target: cv.target };
    let mut ev_recs: Vec<EvRec> = evidence
        .iter()
        .map(|(f, r)| EvRec {
            fname: f.clone(),
            date: r["date"].as_str().unwrap().to_string(),
            moves: r
                .get("moves")
                .and_then(Value::as_object)
                .map(|m| {
                    m.iter()
                        .map(|(k, v)| (k.clone(), v.as_str().unwrap_or("").to_string()))
                        .collect()
                })
                .unwrap_or_default(),
            assist: assist_of(r).to_string(),
        })
        .collect();
    ev_recs.sort_by(|a, b| a.date.cmp(&b.date));

    // move frequency over problems.json walks, first-seen order — the same
    // Counter order the Python chart fed pass_rates, so the RNG stream matches
    let problems_v = load_json(&graph.join("problems.json"));
    let mut mf_keys: Vec<String> = vec![];
    let mut mf_count: HashMap<String, f64> = HashMap::new();
    for (_p, v) in problems_v["problems"].as_object().unwrap() {
        let Some(obj) = v.as_object() else { continue };
        let Some(mvs) = obj.get("moves").and_then(Value::as_array) else { continue };
        for m in mvs {
            let s = m.as_str().unwrap().to_string();
            if !mf_count.contains_key(&s) {
                mf_keys.push(s.clone());
            }
            *mf_count.entry(s).or_insert(0.0) += 1.0;
        }
    }
    let mf_weights: Vec<f64> = mf_keys.iter().map(|k| mf_count[k]).collect();
    let node_ids: Vec<String> = nodes.iter().map(|n| n.id.clone()).collect();

    // weekly replay: evidence filtered to each date, recall from the curve,
    // Monte Carlo per recognition scenario ("today" = last recorded evidence)
    let today = *days.last().unwrap();
    let mut weeks = vec![];
    let mut wd = first;
    while wd < today {
        weeks.push(wd);
        wd += Duration::days(7);
    }
    weeks.push(today);
    // per week, per scenario (cautious/central/optimistic): (screen%, onsite%)
    let mut series: Vec<[(f64, f64); 3]> = vec![];
    let mut week_counts: Vec<usize> = vec![];
    for (i, wd) in weeks.iter().enumerate() {
        let wd_s = wd.to_string();
        let k = ev_recs.partition_point(|r| r.date.as_str() <= wd_s.as_str());
        let recall = current_recall(&node_ids, &ev_recs[..k], &mcurve, *wd);
        let rmap: HashMap<&str, f64> =
            node_ids.iter().map(String::as_str).zip(recall.iter().copied()).collect();
        let mv_recall: Vec<Option<f64>> =
            mf_keys.iter().map(|k| rmap.get(k.as_str()).copied()).collect();
        let mut row = [(0.0, 0.0); 3];
        for (si, (_name, r_base)) in SCENARIOS.iter().enumerate() {
            let (_full, onsite, screen, _h) = pass_rates(
                &mv_recall, &mf_weights, &OFF_GRAPH0, *r_base, (0, 0, 0),
                &mut PyRandom::new(42), 4000,
            );
            row[si] = (screen * 100.0, onsite * 100.0);
        }
        series.push(row);
        let lo = if i == 0 { String::new() } else { weeks[i - 1].to_string() };
        week_counts.push(
            ev_recs.iter().filter(|r| lo.as_str() < r.date.as_str() && r.date.as_str() <= wd_s.as_str()).count(),
        );
    }
    if std::env::var("KG_MOVIE_DEBUG").is_ok() {
        for (wd, row) in weeks.iter().zip(&series) {
            eprintln!("{wd} central screen={:.4} onsite={:.4}", row[1].0, row[1].1);
        }
    }

    // ---- draw --------------------------------------------------------------
    const CW: f64 = 1200.0;
    const CH: f64 = 430.0;
    const CML: f64 = 48.0; // left margin
    const CMR: f64 = 56.0; // the axis's two-week tail hosts the end labels
    const CPT: f64 = 34.0; // main panel top
    const CPB: f64 = 334.0; // main panel bottom
    const CVT: f64 = 344.0; // volume panel top
    const CVB: f64 = 404.0; // volume panel bottom
    const GRID: &str = "#21262d";
    const MUTED: &str = "#8b949e";
    const SCREEN_C: &str = "#1f77b4";
    const ONSITE_C: &str = "#ff7f0e";
    let x0 = weeks[0];
    let xend = *weeks.last().unwrap() + Duration::days(14);
    let span = (xend - x0).num_days() as f64;
    let x_of = |d: NaiveDate| CML + (d - x0).num_days() as f64 / span * (CW - CML - CMR);
    let y_of = |p: f64| CPB - p / 100.0 * (CPB - CPT);

    let mut c = String::with_capacity(64 * 1024);
    writeln!(c, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
    writeln!(
        c,
        "<svg width=\"{CW:.0}pt\" height=\"{CH:.0}pt\" viewBox=\"0 0 {CW:.0} {CH:.0}\" xmlns=\"http://www.w3.org/2000/svg\" font-family=\"Helvetica,sans-serif\">"
    )
    .unwrap();
    writeln!(c, "<rect width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\"/>").unwrap();

    // era banner strip + swapping era label, same split tick as the movie's
    let split_x = era_frac.map_or(CW, |f| f * CW);
    if split_x > 0.0 {
        writeln!(c, "<rect x=\"0\" y=\"0\" width=\"{split_x:.1}\" height=\"3\" fill=\"{ERA_PRE_INK}\" opacity=\"0.55\"/>").unwrap();
    }
    if switch.is_some() && split_x < CW {
        writeln!(c, "<rect x=\"{split_x:.1}\" y=\"0\" width=\"{:.1}\" height=\"3\" fill=\"{ERA_GRAPH_INK}\" opacity=\"0.9\"/>", CW - split_x).unwrap();
    }
    for (label, ink, show) in [
        (ERA_PRE, ERA_PRE_INK, era_frac != Some(0.0)),
        (ERA_GRAPH, ERA_GRAPH_INK, switch.is_some()),
    ] {
        if !show {
            continue;
        }
        let track = match era_frac {
            Some(f) if f > 0.0 => {
                let mut times = vec![0.0];
                push_key(&mut times, f);
                let values = if label == ERA_PRE {
                    vec!["1".to_string(), "0".to_string()]
                } else {
                    vec!["0".to_string(), "1".to_string()]
                };
                animate("opacity", "discrete", &values, &times, dur)
            }
            _ => String::new(),
        };
        writeln!(
            c,
            "<text x=\"12\" y=\"19\" font-size=\"14\" font-weight=\"bold\" fill=\"{ink}\" opacity=\"{}\">{label}{track}</text>",
            if label == ERA_PRE && era_frac.is_some() { 0 } else { 1 }
        )
        .unwrap();
    }
    writeln!(
        c,
        "<text x=\"{:.0}\" y=\"19\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">P(pass a mock, cold) — weekly replay of the technique graph (band = recognition scenarios)</text>",
        CW / 2.0
    )
    .unwrap();

    // static furniture: grid, axes, month ticks
    for p in [0.0, 25.0, 50.0, 75.0, 100.0] {
        let y = y_of(p);
        let (stroke, dash) = if p == 50.0 { (MUTED, " stroke-dasharray=\"2 4\"") } else { (GRID, "") };
        writeln!(c, "<line x1=\"{CML}\" y1=\"{y:.1}\" x2=\"{:.1}\" y2=\"{y:.1}\" stroke=\"{stroke}\" stroke-width=\"1\"{dash}/>", CW - CMR).unwrap();
        writeln!(c, "<text x=\"{:.0}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{p:.0}%</text>", CML - 6.0, y + 4.0).unwrap();
    }
    let mut m = NaiveDate::from_ymd_opt(x0.year(), x0.month(), 1).unwrap();
    const MONTHS: [&str; 12] = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
    while m <= xend {
        let nxt = NaiveDate::from_ymd_opt(m.year() + (m.month() == 12) as i32, m.month() % 12 + 1, 1).unwrap();
        if m >= x0 {
            let x = x_of(m);
            writeln!(c, "<line x1=\"{x:.1}\" y1=\"{CVB}\" x2=\"{x:.1}\" y2=\"{:.0}\" stroke=\"{MUTED}\" stroke-width=\"1\"/>", CVB + 4.0).unwrap();
            // the warped axis crams quiet months together — a label only
            // where its month is wide enough to own it
            if x_of(nxt.min(xend)) - x >= 34.0 {
                let lab = if m.month() == 1 {
                    format!("jan '{:02}", m.year() % 100)
                } else {
                    MONTHS[m.month0() as usize].to_string()
                };
                writeln!(c, "<text x=\"{x:.1}\" y=\"{:.0}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{lab}</text>", CVB + 17.0).unwrap();
            }
        }
        m = nxt;
    }
    writeln!(c, "<text x=\"{:.0}\" y=\"{:.0}\" font-size=\"10\" fill=\"{MUTED}\">solves/wk</text>", CML + 4.0, CVT + 10.0).unwrap();

    // era switch on the calendar axis itself
    if let Ok(sw) = NaiveDate::parse_from_str(ERA_SWITCH, "%Y-%m-%d") {
        if sw > x0 && sw < xend {
            let x = x_of(sw);
            writeln!(c, "<line x1=\"{x:.1}\" y1=\"{CPT}\" x2=\"{x:.1}\" y2=\"{CVB}\" stroke=\"{ERA_GRAPH_INK}\" stroke-width=\"1.2\" stroke-dasharray=\"5 4\" opacity=\"0.6\"/>").unwrap();
        }
    }

    // legend
    for (i, (color, label)) in [
        (SCREEN_C, "phone screen (both mediums)"),
        (ONSITE_C, "onsite (2E + 2M + ≥1 hard)"),
    ]
    .iter()
    .enumerate()
    {
        let y = CPT + 14.0 + i as f64 * 18.0;
        writeln!(c, "<line x1=\"{:.0}\" y1=\"{y:.1}\" x2=\"{:.0}\" y2=\"{y:.1}\" stroke=\"{color}\" stroke-width=\"2.5\"/>", CML + 10.0, CML + 32.0).unwrap();
        writeln!(c, "<text x=\"{:.0}\" y=\"{:.1}\" font-size=\"12\" fill=\"{INK}\">{label}</text>", CML + 38.0, y + 4.0).unwrap();
    }

    // the reveal: everything data-driven clips to a rect whose right edge
    // tracks the movie's current date, tick for tick — under calendar pacing
    // that's one constant-speed sweep, and it stays date-true under --pace
    // solves too; it holds through the loop-closing fade
    let mut reveal_x: Vec<String> = days
        .iter()
        .map(|d| format!("{:.1}", x_of(*d).clamp(CML, CW - CMR)))
        .collect();
    let mut reveal_t: Vec<f64> = tick_frac.clone();
    reveal_x.push(reveal_x.last().unwrap().clone());
    push_key(&mut reveal_t, 1.0);
    let reveal_anim = animate("width", "linear", &reveal_x, &reveal_t, dur);
    writeln!(c, "<clipPath id=\"reveal\"><rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{reveal_anim}</rect></clipPath>").unwrap();
    writeln!(c, "<g clip-path=\"url(#reveal)\">").unwrap();

    // bands (cautious..optimistic) and central lines
    for (kind, color) in [(0usize, SCREEN_C), (1usize, ONSITE_C)] {
        let get = |si: usize, i: usize| if kind == 0 { series[i][si].0 } else { series[i][si].1 };
        let mut band = String::new();
        for (i, wd) in weeks.iter().enumerate() {
            write!(band, "{:.1},{:.1} ", x_of(*wd), y_of(get(0, i))).unwrap();
        }
        for (i, wd) in weeks.iter().enumerate().rev() {
            write!(band, "{:.1},{:.1} ", x_of(*wd), y_of(get(2, i))).unwrap();
        }
        writeln!(c, "<polygon points=\"{}\" fill=\"{color}\" opacity=\"0.15\"/>", band.trim_end()).unwrap();
        let line: Vec<String> = weeks
            .iter()
            .enumerate()
            .map(|(i, wd)| format!("{:.1},{:.1}", x_of(*wd), y_of(get(1, i))))
            .collect();
        writeln!(c, "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\"/>", line.join(" ")).unwrap();
    }

    // the oct/nov '25 plateau, and the note when the line breaks above it
    let central_screen: Vec<f64> = series.iter().map(|r| r[1].0).collect();
    let plateau = weeks
        .iter()
        .zip(&central_screen)
        .filter(|(wd, _)| {
            **wd >= NaiveDate::from_ymd_opt(2025, 10, 1).unwrap()
                && **wd <= NaiveDate::from_ymd_opt(2025, 11, 30).unwrap()
        })
        .map(|(_, v)| *v)
        .fold(f64::NAN, f64::max);
    if plateau.is_finite() {
        let py = y_of(plateau);
        writeln!(c, "<line x1=\"{:.1}\" y1=\"{py:.1}\" x2=\"{:.1}\" y2=\"{py:.1}\" stroke=\"{SCREEN_C}\" stroke-width=\"1\" stroke-dasharray=\"6 4\" opacity=\"0.55\"/>", x_of(NaiveDate::from_ymd_opt(2025, 10, 1).unwrap()), CW - CMR).unwrap();
        writeln!(c, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"11\" fill=\"{SCREEN_C}\" opacity=\"0.8\">oct/nov '25 plateau</text>", x_of(NaiveDate::from_ymd_opt(2025, 12, 20).unwrap()), py - 5.0).unwrap();
    }

    // weekly solve volume, its own little axis under the main panel
    let vmax = week_counts.iter().copied().max().unwrap_or(1).max(1) as f64;
    for (wd, n) in weeks.iter().zip(&week_counts) {
        if *n == 0 {
            continue;
        }
        let x1 = x_of(*wd - Duration::days(6));
        let h = *n as f64 / vmax * (CVB - CVT - 6.0);
        writeln!(c, "<rect x=\"{x1:.1}\" y=\"{:.1}\" width=\"{:.1}\" height=\"{h:.1}\" fill=\"#484f58\"/>", CVB - h, (x_of(*wd) - x1).max(1.0)).unwrap();
    }
    writeln!(c, "</g>").unwrap();

    // end-of-line labels sit to the RIGHT of the finished reveal, so they get
    // their own entrance: pop in on the movie's final tick, when the sweep
    // reaches today — not clipped (never uncovered), not static (spoilers)
    let mut finale_times = vec![0.0];
    push_key(&mut finale_times, *tick_frac.last().unwrap());
    let finale = animate("opacity", "discrete", &["0".into(), "1".into()], &finale_times, dur);
    let lx = x_of(*weeks.last().unwrap());
    for (color, v) in [(SCREEN_C, series.last().unwrap()[1].0), (ONSITE_C, series.last().unwrap()[1].1)] {
        writeln!(c, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"12\" font-weight=\"bold\" fill=\"{color}\" opacity=\"1\">{v:.0}%{finale}</text>", lx + 8.0, y_of(v) + 4.0).unwrap();
    }
    if plateau.is_finite() && *central_screen.last().unwrap() > plateau {
        writeln!(c, "<text x=\"{:.1}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"12\" font-weight=\"bold\" fill=\"#3fb950\" opacity=\"1\">breaking the plateau ↑{finale}</text>", CW - CMR - 4.0, y_of(*central_screen.last().unwrap()) - 24.0).unwrap();
    }

    // the playhead: the movie's current date swept across the calendar
    let head_anim = animate("x", "linear", &reveal_x, &reveal_t, dur);
    writeln!(c, "<rect x=\"{:.1}\" y=\"{CPT}\" width=\"1.5\" height=\"{:.0}\" fill=\"{INK}\" opacity=\"0.75\">{head_anim}</rect>", CW - CMR, CVB - CPT).unwrap();

    // same loop-closing dissolve window as the movie
    writeln!(
        c,
        "<rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
        animate("opacity", "linear", &["0".into(), "0".into(), "1".into()], &[0.0, fade_from, 1.0], dur)
    )
    .unwrap();
    writeln!(c, "</svg>").unwrap();

    let chart_path = graph.join("kg_pass.svg");
    std::fs::write(&chart_path, &c).unwrap();
    println!(
        "wrote {} — {} weeks replayed, synced to the {:.0}s loop, {:.0}KB",
        chart_path.display(),
        weeks.len(),
        seconds,
        c.len() as f64 / 1024.0
    );
}
