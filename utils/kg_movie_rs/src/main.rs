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
// evidence recorded up to that date. Screen time is paced by solves, not by
// the calendar (--pace calendar for the old behaviour): marathon days stretch
// out enough to read, a 100-day dry spell still dims but takes a moment
// rather than half the film. The tail dissolves into the background so the
// loop has no dead frames at the seam. Label placement is chosen at spawn
// from ~20 candidate spots around the node, overlapping nothing graphviz
// drew — nodes, edges, cluster borders and titles — nor any still-fading
// label; the spot is pinned for the label's lifetime.

use std::collections::HashMap;
use std::fmt::Write as _;
use std::path::PathBuf;
use std::process::{Command, Stdio};

use chrono::{Duration, NaiveDate};
use serde_json::Value;

const DEFAULT_SECONDS: f64 = 50.0;
const END_FADE_S: f64 = 1.2; // loop-closing dissolve, capped by FADE_FRACTION
const FADE_FRACTION: f64 = 0.08; // dissolve shrinks with short movies
const LABEL_LIFE_FRACTION: f64 = 0.04; // label fade as a share of runtime
const LULL_WEIGHT: f64 = 0.25; // screen time a solve-less day gets, in solves

const HEADER_H: f64 = 30.0;
const BG: &str = "#0d1117";
const GOLD: &str = "#ffd75f";
const INK: &str = "#c9d1d9";
const STROKE_DEF: &str = "#30363d";
const LABEL_PT: f64 = 13.0; // the mp4's 19px at 144dpi, in 96dpi svg units
const LABEL_GAP: f64 = 4.0; // px between a node box and its label
const MAX_PROBS: usize = 3; // live labels per node; the oldest gets evicted

const SOLID_WINDOW_DAYS: i64 = 42; // flat fallback when curve.json is absent

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

fn animate(attr_name: &str, calc: &str, values: &[String], key_times: &[f64], dur: f64) -> String {
    let kt: Vec<String> = key_times.iter().map(|t| format!("{t:.5}")).collect();
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
    let mut pace_calendar = false;
    let mut args = std::env::args().skip(1);
    while let Some(a) = args.next() {
        match a.as_str() {
            "--open" => open_after = true,
            "--pace" => {
                pace_calendar = matches!(args.next().as_deref(), Some("calendar"));
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

    // gold solve labels, inside the graph transform so they share node coords
    for l in &labels {
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
        writeln!(
            out_svg,
            "<text x=\"{:.1}\" y=\"{:.1}\" font-family=\"Menlo,monospace\" font-size=\"{LABEL_PT:.2}\" fill=\"{GOLD}\" opacity=\"0\">{}{}</text>",
            l.rect.0,
            l.rect.3 - 3.0,
            l.text,
            animate("opacity", "linear", &values, &times, dur)
        )
        .unwrap();
    }
    out_svg.push_str("</g>\n");

    // header: the date and status counts, one flashcard per tick like the mp4's
    // title line — outside the graph transform, in plain canvas coordinates
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
            "<text x=\"{:.1}\" y=\"20\" text-anchor=\"middle\" font-family=\"Helvetica,sans-serif\" font-size=\"15\" fill=\"{INK}\" opacity=\"0\">{title_text}{}</text>",
            width / 2.0,
            animate("opacity", "discrete", &values, &times, dur)
        )
        .unwrap();
    }
    let _ = hidden_counts;

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
}
