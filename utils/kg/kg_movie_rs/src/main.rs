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
// date is just node_status() (kept in lockstep with utils/kg/kg_lib.py) over the
// evidence recorded up to that date. Screen time is event-rate paced: each
// day earns its solve count plus LULL_WEIGHT, so long solve-less stretches
// fast-forward (--pace calendar for constant-speed calendar time instead).
// The P(pass) chart's reveal follows the same tick clock over its linear
// x-axis, so the two stay in step; kg_lib.py's MovieClock mirrors this exact
// pacing for the Python-rendered SVGs — change them together. The tail dissolves into the background so
// the loop has no dead frames at the seam. Label placement is chosen at spawn
// from ~20 candidate spots around the node, overlapping nothing graphviz
// drew — nodes, edges, cluster borders and titles — nor any still-fading
// label; the spot is pinned for the label's lifetime.

use std::collections::HashMap;
use std::fmt::Write as _;
use std::path::PathBuf;
use std::process::{Command, Stdio};

use chrono::{Datelike, Duration, NaiveDate};
use serde_json::Value;

use kg_mock::{current_recall, pass_rates, run_mocks, Bank, EvRec, PyRandom, SCENARIOS};

const DEFAULT_SECONDS: f64 = 10.0;
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
// the tooling landed 2026-07-05, but the july solves were building/testing
// it; sustained picker-driven solving starts here
const ERA_SWITCH: &str = "2026-08-07";
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
    // connectivity covariate (see kg_mock lib.rs): per-node conn lives on
    // NodeReplay, frozen from curve.json's "conn" map at load time
    e: f64,
    conn_mean: f64,
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
// Kept in lockstep with utils/kg/kg_lib.py node_status(): entries sorted by
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
    conn: Option<f64>, // log2 carriers from curve.json, None = use conn_mean
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
                    - p.d * self.assisted
                    + p.e * (self.conn.unwrap_or(p.conn_mean) - p.conn_mean))
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

// The era banner every chart carries: big bold label flipping from the grey
// pre-graph era to the blue graph-scheduling era on the switch date's tick.
// era_frac None = the whole replay is one era (static label). halo draws a
// background-colored outline for banners placed over chart ink.
fn era_banner(x: f64, y: f64, size: f64, anchor: &str, era_frac: Option<f64>, switch_exists: bool, halo: &str, dur: f64) -> String {
    let halo_attr = if halo.is_empty() {
        String::new()
    } else {
        format!(" stroke=\"{halo}\" stroke-width=\"{:.0}\" paint-order=\"stroke\" stroke-linejoin=\"round\"", (size / 7.0).max(3.0))
    };
    let mut s = String::new();
    for (label, ink, show, is_pre) in [
        (ERA_PRE, ERA_PRE_INK, era_frac != Some(0.0), true),
        (ERA_GRAPH, ERA_GRAPH_INK, switch_exists, false),
    ] {
        if !show {
            continue;
        }
        let track = match era_frac {
            Some(f) if f > 0.0 => {
                let mut times = vec![0.0];
                push_key(&mut times, f);
                let values = if is_pre {
                    vec!["1".to_string(), "0".to_string()]
                } else {
                    vec!["0".to_string(), "1".to_string()]
                };
                animate("opacity", "discrete", &values, &times, dur)
            }
            _ => String::new(),
        };
        s.push_str(&format!(
            "<text x=\"{x:.0}\" y=\"{y:.0}\" text-anchor=\"{anchor}\" font-family=\"Helvetica,sans-serif\" font-size=\"{size:.0}\" font-weight=\"bold\" fill=\"{ink}\"{halo_attr} opacity=\"{}\">{label}{track}</text>\n",
            if is_pre && era_frac.is_some() { 0 } else { 1 }
        ));
    }
    s
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
    let conn_map: std::collections::HashMap<String, f64> = {
        let path = graph.join("curve.json");
        if path.exists() {
            load_json(&path)
                .get("conn")
                .and_then(Value::as_object)
                .map(|m| {
                    m.iter()
                        .filter_map(|(k, v)| v.as_f64().map(|f| (k.clone(), f)))
                        .collect()
                })
                .unwrap_or_default()
        } else {
            Default::default()
        }
    };
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
                e: p.get("e").and_then(Value::as_f64).unwrap_or(0.0),
                conn_mean: p.get("conn_mean").and_then(Value::as_f64).unwrap_or(0.0),
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
            NodeReplay { entries, idx: 0, cleans: 0, struggles: 0, assisted: 0.0,
                         conn: conn_map.get(&n.id).copied(), last_clean: None, last: None }
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
    dot.push_str(" graph [rankdir=LR, bgcolor=\"#0d1117\", fontname=\"Helvetica\", compound=true, ranksep=\"0.6\", nodesep=\"0.25\"];\n");
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
    out_svg.push_str("</g>\n");

    // ---- the avatar: gource-style, one sprite gravitating to whatever is
    // being solved and firing a laser at every move the solve exercised.
    // Off by default (AVATAR): the beams pull the eye away from the graph.
    // A shot = one solve (same birth), its targets the centers of the node
    // boxes it touched. The sprite hovers above the targets' centroid and
    // eases there from the previous shot (spline keySplines), so between
    // solves it is visibly travelling; the laser group flashes for LASER_S
    // (or until the next shot, whichever is sooner) and shares the label
    // clock exactly, keyTimes over the same loop.
    const AVATAR: bool = false;
    const HOVER_DY: f64 = -34.0;
    struct Shot {
        born: f64,
        hover: (f64, f64),
        targets: Vec<(f64, f64)>,
    }
    let mut shots: Vec<Shot> = vec![];
    let mut li = 0;
    while li < labels.len() {
        let l = &labels[li];
        let mut lj = li + 1;
        while lj < labels.len() && labels[lj].born == l.born && labels[lj].text == l.text {
            lj += 1;
        }
        let targets: Vec<(f64, f64)> = labels[li..lj]
            .iter()
            .filter_map(|l| boxes.get(&l.node))
            .map(|b| ((b.0 + b.2) / 2.0, (b.1 + b.3) / 2.0))
            .collect();
        if !targets.is_empty() {
            let n = targets.len() as f64;
            let cx = targets.iter().map(|t| t.0).sum::<f64>() / n;
            let cy = targets.iter().map(|t| t.1).sum::<f64>() / n;
            shots.push(Shot { born: l.born, hover: (cx, cy + HOVER_DY), targets });
        }
        li = lj;
    }
    if AVATAR && !shots.is_empty() {
        // the sprite's path, simulated at a fixed step: the target is a
        // heavily averaged trail of the solve positions (an exponential
        // average, so a burst of solves in one cluster pulls it there and a
        // stray one barely nudges it), and the sprite chases the target at a
        // speed proportional to the distance, capped at SPRITE_VMAX, so it
        // drifts rather than teleports. Beams fire from wherever the sprite
        // is at the moment of the solve.
        const STEP_S: f64 = 0.02;
        const TARGET_ALPHA: f64 = 0.12; // per shot, share of the way toward it
        const SPRITE_GAIN: f64 = 2.5; // per second: speed = gain * distance
        const SPRITE_VMAX: f64 = 320.0; // px per second in graph units
        let n_steps = (dur / STEP_S).ceil() as usize + 1;
        let mut path: Vec<(f64, f64)> = Vec::with_capacity(n_steps);
        let mut target = shots[0].hover;
        let mut pos = shots[0].hover;
        let mut si = 0;
        for k in 0..n_steps {
            let t = k as f64 * STEP_S;
            while si < shots.len() && shots[si].born <= t {
                target.0 += TARGET_ALPHA * (shots[si].hover.0 - target.0);
                target.1 += TARGET_ALPHA * (shots[si].hover.1 - target.1);
                si += 1;
            }
            let (dx, dy) = (target.0 - pos.0, target.1 - pos.1);
            let dist = (dx * dx + dy * dy).sqrt();
            if dist > 0.5 {
                let step = (SPRITE_GAIN * dist).min(SPRITE_VMAX) * STEP_S;
                let f = (step / dist).min(1.0);
                pos.0 += dx * f;
                pos.1 += dy * f;
            }
            path.push(pos);
        }
        let pos_at = |t: f64| path[((t / STEP_S).round() as usize).min(path.len() - 1)];

        // beams: one group per shot, lines from the sprite to each hit, lit
        // at the solve and fading out over BEAM_FADE_S so the eye can catch
        // them; overlapping beams simply coexist
        const BEAM_FADE_S: f64 = 0.7;
        writeln!(out_svg, "<g stroke=\"#ff7b72\" stroke-width=\"2\" stroke-linecap=\"round\">").unwrap();
        for sh in &shots {
            let tb = sh.born / dur;
            let te = (tb + BEAM_FADE_S / dur).min(1.0);
            let from = pos_at(sh.born);
            let mut times = vec![0.0];
            let mut values = vec!["0".to_string()];
            if tb > 0.0004 {
                push_key(&mut times, tb - 0.0002);
                values.push("0".to_string());
            }
            push_key(&mut times, tb.max(0.0));
            values.push("1".to_string());
            if te < 1.0 {
                push_key(&mut times, te);
                values.push("0".to_string());
            }
            push_key(&mut times, 1.0);
            values.push("0".to_string());
            write!(out_svg, "<g opacity=\"0\">{}", animate("opacity", "linear", &values, &times, dur)).unwrap();
            for t in &sh.targets {
                write!(
                    out_svg,
                    "<line x1=\"{:.0}\" y1=\"{:.0}\" x2=\"{:.0}\" y2=\"{:.0}\"/><circle cx=\"{:.0}\" cy=\"{:.0}\" r=\"5\" fill=\"#ff7b72\" stroke=\"none\"/>",
                    from.0, from.1, t.0, t.1, t.0, t.1
                )
                .unwrap();
            }
            out_svg.push_str("</g>\n");
        }
        out_svg.push_str("</g>\n");

        // the sprite itself, riding the simulated path (linear between steps)
        let times: Vec<f64> = (0..path.len()).map(|k| (k as f64 * STEP_S / dur).min(1.0)).collect();
        let values: Vec<String> = path.iter().map(|p| format!("{:.0},{:.0}", p.0, p.1)).collect();
        let kt: Vec<String> = times.iter().map(|t| fmt_frac(*t)).collect();
        writeln!(
            out_svg,
            "<g><animateTransform attributeName=\"transform\" type=\"translate\" calcMode=\"linear\" values=\"{}\" keyTimes=\"{}\" dur=\"{dur}s\" repeatCount=\"indefinite\"/>\
<circle r=\"15\" fill=\"{GOLD}\" opacity=\"0.22\"/><circle r=\"8\" fill=\"{GOLD}\" stroke=\"{BG}\" stroke-width=\"2\"/><circle cx=\"3\" cy=\"-2\" r=\"2.2\" fill=\"{BG}\"/></g>",
            values.join(";"),
            kt.join(";")
        )
        .unwrap();
    }
    out_svg.push_str("</g>\n");

    // header: the date and status counts, one flashcard per tick like the mp4's
    // title line — outside the graph transform, in plain canvas coordinates
    writeln!(
        out_svg,
        "<g text-anchor=\"end\" font-family=\"Helvetica,sans-serif\" font-size=\"20\" fill=\"{INK}\">"
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
            width - 20.0,
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
    out_svg.push_str(&era_banner(20.0, 48.0, 36.0, "start", era_frac, switch.is_some(), "", dur));

    // era strip: the history's calendar along the top edge — grey for the
    // hand-scheduled stretch, blue once the graph picker takes over, a
    // playhead sweeping across so the switch reads at any thumbnail size.
    // Both the split and the playhead are date-true (the playhead rides the
    // warped tick clock), so the strip stays in step with the P(pass)
    // chart's playhead and positions.svg under event-rate pacing.
    let cal_x = |i: usize| i as f64 / (n_ticks - 1).max(1) as f64 * width;
    let split_x = switch.map_or(width, &cal_x);
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
    let mut head_x: Vec<String> = (0..n_ticks).map(|i| format!("{:.1}", cal_x(i) - 2.0)).collect();
    let mut head_t = tick_frac.clone();
    head_x.push(head_x.last().unwrap().clone());
    push_key(&mut head_t, 1.0);
    writeln!(
        out_svg,
        "<rect x=\"-2\" y=\"0\" width=\"4\" height=\"{:.0}\" fill=\"{INK}\">{}</rect>",
        ERA_STRIP_H + 8.0,
        animate("x", "linear", &head_x, &head_t, dur)
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
        "wrote {} — {} ticks, {} solve labels, {} shots, {:.1}s loop ({:.1}s dissolve), {:.0}KB",
        out_path.display(),
        n_ticks,
        labels.len(),
        shots.len(),
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
    let mcurve = kg_mock::Curve { a: cv.a, b: cv.b, c: cv.c, d: cv.d, e: cv.e,
        conn_mean: cv.conn_mean, conn: conn_map.clone(), beta: cv.beta, target: cv.target };
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

    // the bank: real per-difficulty problem pools (evidenced + drafted
    // walks), shared with kg_mock so the charts and `make mock` agree
    let node_ids: Vec<String> = nodes.iter().map(|n| n.id.clone()).collect();
    let problems_v = load_json(&graph.join("problems.json"));
    let predicted_v = load_json(&graph.join("predicted.json"));
    let repo_root = graph.parent().map(|p| p.to_path_buf()).unwrap_or_else(|| PathBuf::from("."));
    let metadata_v = load_json(&repo_root.join("data/problems_metadata.json"));
    let bank = Bank::build(&problems_v, &predicted_v, &metadata_v, &node_ids);

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
    // the shelf line: same evidence prefix, recall evaluated 90 days LATER —
    // P(pass) if practice stopped that week, i.e. the durable floor under
    // the line. (The fitted curve is flat enough that the gap stays a fairly
    // steady ~15-20% relative — the plateau-vs-consolidation contrast lives
    // in the volume-bar tinting below, not here.) Central scenario only.
    const SHELF_DAYS: i64 = 90;
    let mut shelf: Vec<(f64, f64)> = vec![];
    let mut week_counts: Vec<usize> = vec![];
    for (i, wd) in weeks.iter().enumerate() {
        let wd_s = wd.to_string();
        let k = ev_recs.partition_point(|r| r.date.as_str() <= wd_s.as_str());
        let recall = current_recall(&node_ids, &ev_recs[..k], &mcurve, *wd);
        let mv_recall: Vec<Option<f64>> = (0..bank.move_names.len())
            .map(|i| if i < bank.n_known { Some(recall[i]) } else { None })
            .collect();
        let mut row = [(0.0, 0.0); 3];
        for (si, (_name, r_base)) in SCENARIOS.iter().enumerate() {
            let (_full, onsite, screen, _h) = pass_rates(
                &mv_recall, &bank.pools, *r_base, (0, 0, 0),
                &mut PyRandom::new(42), 4000,
            );
            row[si] = (screen * 100.0, onsite * 100.0);
        }
        series.push(row);
        let recall_s = current_recall(&node_ids, &ev_recs[..k], &mcurve, *wd + Duration::days(SHELF_DAYS));
        let mv_recall_s: Vec<Option<f64>> = (0..bank.move_names.len())
            .map(|i| if i < bank.n_known { Some(recall_s[i]) } else { None })
            .collect();
        let (_full, onsite_s, screen_s, _h) = pass_rates(
            &mv_recall_s, &bank.pools, SCENARIOS[1].1, (0, 0, 0),
            &mut PyRandom::new(42), 4000,
        );
        shelf.push((screen_s * 100.0, onsite_s * 100.0));
        let lo = if i == 0 { String::new() } else { weeks[i - 1].to_string() };
        week_counts.push(
            ev_recs.iter().filter(|r| lo.as_str() < r.date.as_str() && r.date.as_str() <= wd_s.as_str()).count(),
        );
    }
    // each week's volume split by problem NOVELTY — new problems vs
    // re-solves — feeds the yield chart (kg_yield.svg below): new problems
    // under a flat line mean grinding through what is already known (the
    // oct/nov '25 plateau: ~100 new problems/week, line going nowhere);
    // re-solves under a rising line are consolidation paying out.
    // Model-free: only problem numbers and dates.
    let mut week_new = vec![0usize; weeks.len()];
    let mut week_re = vec![0usize; weeks.len()];
    // drill work per week: reviews (evidence records with problem="drill")
    // plus bank files created (first git add under drills/) — the foundation
    // being poured during consolidation
    let mut week_drill = vec![0usize; weeks.len()];
    {
        let mut by_date: Vec<(&str, &str)> = evidence
            .iter()
            .filter_map(|(_, r)| {
                Some((r["date"].as_str()?, r.get("problem").and_then(Value::as_str)?))
            })
            .collect();
        by_date.sort();
        let mut seen: std::collections::HashSet<&str> = std::collections::HashSet::new();
        for (ds, pnum) in by_date {
            let d = NaiveDate::parse_from_str(ds, "%Y-%m-%d").unwrap();
            let wi = ((((d - first).num_days() + 6) / 7).max(0) as usize).min(weeks.len() - 1);
            if pnum == "drill" {
                week_drill[wi] += 1;
            }
            if seen.insert(pnum) {
                week_new[wi] += 1;
            } else {
                week_re[wi] += 1;
            }
        }
        if let Ok(out) = Command::new("git")
            .args(["log", "--diff-filter=A", "--date=short", "--format=C %ad", "--name-only", "--", "drills/"])
            .current_dir(&repo_root)
            .output()
        {
            let mut cur: Option<NaiveDate> = None;
            for line in String::from_utf8_lossy(&out.stdout).lines() {
                if let Some(ds) = line.strip_prefix("C ") {
                    cur = NaiveDate::parse_from_str(ds, "%Y-%m-%d").ok();
                } else if line.starts_with("drills/") {
                    if let Some(d) = cur {
                        if d >= first {
                            let wi = ((((d - first).num_days() + 6) / 7) as usize).min(weeks.len() - 1);
                            week_drill[wi] += 1;
                        }
                    }
                }
            }
        }
    }
    if std::env::var("KG_MOVIE_DEBUG").is_ok() {
        for (((wd, row), sh), (nn, nr)) in weeks
            .iter()
            .zip(&series)
            .zip(&shelf)
            .zip(week_new.iter().zip(&week_re))
        {
            eprintln!(
                "{wd} central screen={:.4} onsite={:.4} shelf screen={:.4} onsite={:.4} new={nn} re={nr}",
                row[1].0, row[1].1, sh.0, sh.1
            );
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

    // era banner strip + swapping era label, same split tick as the movie's;
    // date-true split so the two strips mirror each other
    let split_x = switch.map_or(CW, |i| i as f64 / (n_ticks - 1).max(1) as f64 * CW);
    if split_x > 0.0 {
        writeln!(c, "<rect x=\"0\" y=\"0\" width=\"{split_x:.1}\" height=\"3\" fill=\"{ERA_PRE_INK}\" opacity=\"0.55\"/>").unwrap();
    }
    if switch.is_some() && split_x < CW {
        writeln!(c, "<rect x=\"{split_x:.1}\" y=\"0\" width=\"{:.1}\" height=\"3\" fill=\"{ERA_GRAPH_INK}\" opacity=\"0.9\"/>", CW - split_x).unwrap();
    }
    c.push_str(&era_banner(12.0, 26.0, 24.0, "start", era_frac, switch.is_some(), "", dur));
    writeln!(
        c,
        "<text x=\"{:.0}\" y=\"19\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">P(pass a mock, cold) — weekly replay of the technique graph (band = recognition scenarios)</text>",
        CW / 2.0 + 100.0
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
    for (i, (color, label, dash)) in [
        (SCREEN_C, "phone screen (both mediums)", ""),
        (ONSITE_C, "onsite (2E + 2M + ≥1 hard)", ""),
        (MUTED, "dashed: after a 90-day break — the durable floor under each line", " stroke-dasharray=\"5 4\""),
    ]
    .iter()
    .enumerate()
    {
        let y = CPT + 14.0 + i as f64 * 18.0;
        writeln!(c, "<line x1=\"{:.0}\" y1=\"{y:.1}\" x2=\"{:.0}\" y2=\"{y:.1}\" stroke=\"{color}\" stroke-width=\"2.5\"{dash}/>", CML + 10.0, CML + 32.0).unwrap();
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
    // the complement: everything RIGHT of the playhead, so the not-yet-swept
    // data can sit dimmed underneath — same animation values, so the two
    // clips tile exactly at the playhead
    let rest_anim = animate("x", "linear", &reveal_x, &reveal_t, dur);
    writeln!(c, "<clipPath id=\"rest\"><rect x=\"{:.1}\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{rest_anim}</rect></clipPath>", CW - CMR).unwrap();
    let mut dg = String::new();

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
        writeln!(dg, "<polygon points=\"{}\" fill=\"{color}\" opacity=\"0.15\"/>", band.trim_end()).unwrap();
        let line: Vec<String> = weeks
            .iter()
            .enumerate()
            .map(|(i, wd)| format!("{:.1},{:.1}", x_of(*wd), y_of(get(1, i))))
            .collect();
        writeln!(dg, "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\"/>", line.join(" ")).unwrap();
        // the shelf: central P(pass) 90 days after stopping — dashed, under
        // its solid line; the gap is what a break would cost
        let sline: Vec<String> = weeks
            .iter()
            .enumerate()
            .map(|(i, wd)| {
                let v = if kind == 0 { shelf[i].0 } else { shelf[i].1 };
                format!("{:.1},{:.1}", x_of(*wd), y_of(v))
            })
            .collect();
        writeln!(dg, "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"1.4\" stroke-dasharray=\"5 4\" opacity=\"0.8\"/>", sline.join(" ")).unwrap();
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
        writeln!(dg, "<line x1=\"{:.1}\" y1=\"{py:.1}\" x2=\"{:.1}\" y2=\"{py:.1}\" stroke=\"{SCREEN_C}\" stroke-width=\"1\" stroke-dasharray=\"6 4\" opacity=\"0.55\"/>", x_of(NaiveDate::from_ymd_opt(2025, 10, 1).unwrap()), CW - CMR).unwrap();
        writeln!(dg, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"11\" fill=\"{SCREEN_C}\" opacity=\"0.8\">oct/nov '25 plateau</text>", x_of(NaiveDate::from_ymd_opt(2025, 12, 20).unwrap()), py - 5.0).unwrap();
    }

    // weekly solve volume, its own little axis under the main panel
    let vmax = week_counts.iter().copied().max().unwrap_or(1).max(1) as f64;
    for (wd, n) in weeks.iter().zip(&week_counts) {
        if *n == 0 {
            continue;
        }
        let x1 = x_of(*wd - Duration::days(6));
        let h = *n as f64 / vmax * (CVB - CVT - 6.0);
        writeln!(dg, "<rect x=\"{x1:.1}\" y=\"{:.1}\" width=\"{:.1}\" height=\"{h:.1}\" fill=\"#484f58\"/>", CVB - h, (x_of(*wd) - x1).max(1.0)).unwrap();
    }
    // dimmed ahead of the playhead, full strength behind it
    writeln!(c, "<g clip-path=\"url(#rest)\" opacity=\"0.5\">\n{dg}</g>").unwrap();
    writeln!(c, "<g clip-path=\"url(#reveal)\">\n{dg}</g>").unwrap();

    // end-of-line labels sit to the RIGHT of the finished reveal, so they get
    // their own entrance: pop in on the movie's final tick, when the sweep
    // reaches today — not clipped (never uncovered), not static (spoilers)
    let mut finale_times = vec![0.0];
    push_key(&mut finale_times, *tick_frac.last().unwrap());
    let finale = animate("opacity", "discrete", &["0".into(), "1".into()], &finale_times, dur);
    let lx = x_of(*weeks.last().unwrap());
    for (color, v, sv) in [
        (SCREEN_C, series.last().unwrap()[1].0, shelf.last().unwrap().0),
        (ONSITE_C, series.last().unwrap()[1].1, shelf.last().unwrap().1),
    ] {
        writeln!(c, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"12\" font-weight=\"bold\" fill=\"{color}\" opacity=\"1\">{v:.0}%{finale}</text>", lx + 8.0, y_of(v) + 4.0).unwrap();
        // shelf end label, skipped when it would sit on top of the main one
        if (y_of(sv) - y_of(v)).abs() >= 14.0 {
            writeln!(c, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"11\" fill=\"{color}\" opacity=\"0.8\">{sv:.0}%{finale}</text>", lx + 8.0, y_of(sv) + 4.0).unwrap();
        }
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

    // ---- yield chart: graph/kg_yield.svg ---------------------------------
    // P(pass) against CUMULATIVE SOLVES instead of time: effort is the
    // x-axis, so a plateau is a long flat slog to the right - hundreds of
    // solves buying nothing, and extending that slope it never breaks -
    // while consolidation is a near-vertical climb: few solves, mostly
    // re-solves, big lift. Segment color = the week's re-solve share (gray
    // new-problem churn, green re-solves). Same weekly replay and reveal
    // clock as kg_pass.svg.
    {
        let cum: Vec<f64> = weeks
            .iter()
            .map(|wd| {
                let s = wd.to_string();
                ev_recs.partition_point(|r| r.date.as_str() <= s.as_str()) as f64
            })
            .collect();
        let scr: Vec<f64> = series.iter().map(|r| r[1].0).collect();
        let cum_total = cum.last().unwrap().max(1.0);
        let ymax = (scr.iter().fold(0.0f64, |a, &b| a.max(b)) * 1.2 / 5.0).ceil() * 5.0;
        const YML: f64 = 52.0;
        const YMR: f64 = 46.0;
        const YPT: f64 = 58.0;
        const YPB: f64 = 386.0;
        let yx = |s: f64| YML + s / cum_total * (CW - YML - YMR);
        let yy = |p: f64| YPB - p / ymax * (YPB - YPT);
        let px_per_solve = (CW - YML - YMR) / cum_total;

        let mut y = String::with_capacity(32 * 1024);
        writeln!(y, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
        writeln!(
            y,
            "<svg width=\"{CW:.0}pt\" height=\"{CH:.0}pt\" viewBox=\"0 0 {CW:.0} {CH:.0}\" xmlns=\"http://www.w3.org/2000/svg\" font-family=\"Helvetica,sans-serif\">"
        )
        .unwrap();
        writeln!(y, "<rect width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\"/>").unwrap();
        if split_x > 0.0 {
            writeln!(y, "<rect x=\"0\" y=\"0\" width=\"{split_x:.1}\" height=\"3\" fill=\"{ERA_PRE_INK}\" opacity=\"0.55\"/>").unwrap();
        }
        if switch.is_some() && split_x < CW {
            writeln!(y, "<rect x=\"{split_x:.1}\" y=\"0\" width=\"{:.1}\" height=\"3\" fill=\"{ERA_GRAPH_INK}\" opacity=\"0.9\"/>", CW - split_x).unwrap();
        }
        y.push_str(&era_banner(12.0, 26.0, 24.0, "start", era_frac, switch.is_some(), "", dur));
        writeln!(
            y,
            "<text x=\"{:.0}\" y=\"19\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">what does a solve buy? - P(pass a phone screen) vs total solves</text>",
            CW / 2.0 + 100.0
        )
        .unwrap();
        writeln!(
            y,
            "<text x=\"{:.0}\" y=\"36\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">flat = a plateau more grinding will not break; vertical = consolidation paying out</text>",
            CW / 2.0 + 100.0
        )
        .unwrap();

        // furniture: y grid every 10 pts, x grid every 100 solves
        let mut p = 0.0;
        while p <= ymax {
            let gy = yy(p);
            writeln!(y, "<line x1=\"{YML}\" y1=\"{gy:.1}\" x2=\"{:.1}\" y2=\"{gy:.1}\" stroke=\"{GRID}\" stroke-width=\"1\"/>", CW - YMR).unwrap();
            writeln!(y, "<text x=\"{:.0}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{p:.0}%</text>", YML - 6.0, gy + 4.0).unwrap();
            p += 10.0;
        }
        let mut s = 0.0;
        while s <= cum_total {
            let gx = yx(s);
            writeln!(y, "<line x1=\"{gx:.1}\" y1=\"{YPB}\" x2=\"{gx:.1}\" y2=\"{:.0}\" stroke=\"{MUTED}\" stroke-width=\"1\"/>", YPB + 4.0).unwrap();
            if s as i64 % 200 == 0 {
                writeln!(y, "<text x=\"{gx:.1}\" y=\"{:.0}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{s:.0}</text>", YPB + 17.0).unwrap();
            }
            s += 100.0;
        }
        writeln!(y, "<text x=\"{:.1}\" y=\"{:.0}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">total solves</text>", CW - YMR, YPB + 32.0).unwrap();

        // era switch on the solve axis
        if let Ok(sw) = NaiveDate::parse_from_str(ERA_SWITCH, "%Y-%m-%d") {
            let sw_s = sw.to_string();
            let cx = yx(ev_recs.partition_point(|r| r.date.as_str() <= sw_s.as_str()) as f64);
            writeln!(y, "<line x1=\"{cx:.1}\" y1=\"{YPT}\" x2=\"{cx:.1}\" y2=\"{YPB}\" stroke=\"{ERA_GRAPH_INK}\" stroke-width=\"1.2\" stroke-dasharray=\"5 4\" opacity=\"0.6\"/>").unwrap();
        }

        let mut dy = String::new();
        // the path, one thick segment per week, colored by re-solve share
        for i in 1..weeks.len() {
            let (x1, y1, x2, y2) = (yx(cum[i - 1]), yy(scr[i - 1]), yx(cum[i]), yy(scr[i]));
            let (nn, nr) = (week_new[i], week_re[i]);
            if nn + nr == 0 {
                // a resting week: no x movement, the line just drips down
                writeln!(dy, "<line x1=\"{x1:.1}\" y1=\"{y1:.1}\" x2=\"{x2:.1}\" y2=\"{y2:.1}\" stroke=\"{MUTED}\" stroke-width=\"1.5\" stroke-dasharray=\"2 3\"/>").unwrap();
                continue;
            }
            let t = nr as f64 / (nn + nr) as f64;
            let lerp = |a: f64, b: f64| (a + t * (b - a)) as u8;
            let color = format!("#{:02x}{:02x}{:02x}", lerp(110.0, 63.0), lerp(118.0, 185.0), lerp(129.0, 80.0));
            writeln!(dy, "<line x1=\"{x1:.1}\" y1=\"{y1:.1}\" x2=\"{x2:.1}\" y2=\"{y2:.1}\" stroke=\"{color}\" stroke-width=\"4\" stroke-linecap=\"round\"/>").unwrap();
        }

        // the three phases, measured from the replay itself
        let widx = |d: NaiveDate| weeks.partition_point(|w| *w <= d).saturating_sub(1);
        let a = widx(NaiveDate::from_ymd_opt(2025, 10, 6).unwrap());
        let b = widx(NaiveDate::from_ymd_opt(2025, 11, 30).unwrap());
        let pz = widx(NaiveDate::from_ymd_opt(2026, 7, 31).unwrap());
        let last = weeks.len() - 1;
        if a < b && b < pz && pz < last {
            // the plateau: hundreds of solves after the first read, no lift
            let (dn, dp) = (cum[b] - cum[a], scr[b] - scr[a]);
            let ptop = scr[a..=b].iter().fold(0.0f64, |m, &v| m.max(v));
            let xm = (yx(cum[a]) + yx(cum[b])) / 2.0;
            writeln!(dy, "<text x=\"{xm:.1}\" y=\"{:.1}\" text-anchor=\"middle\" font-size=\"13\" font-weight=\"bold\" fill=\"{INK}\">the plateau: {dn:.0} more solves → {dp:+.0} pts</text>", yy(ptop) - 30.0).unwrap();
            writeln!(dy, "<text x=\"{xm:.1}\" y=\"{:.1}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">nearly all new problems, exercising ground already held</text>", yy(ptop) - 14.0).unwrap();
            // extend the plateau's slope: at that rate it never breaks
            let slope = dp / dn.max(1.0);
            let (ex1, ey1) = (yx(cum[b]), yy(scr[b]));
            let ex2 = CW - 8.0;
            let ey2 = yy((scr[b] + slope * (ex2 - ex1) / px_per_solve).max(0.0));
            writeln!(dy, "<line x1=\"{ex1:.1}\" y1=\"{ey1:.1}\" x2=\"{ex2:.1}\" y2=\"{ey2:.1}\" stroke=\"{MUTED}\" stroke-width=\"1.2\" stroke-dasharray=\"2 5\" opacity=\"0.8\"/>").unwrap();
            writeln!(dy, "<text x=\"{ex2:.1}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">grinding on at that rate: never</text>", ey2 - 7.0).unwrap();
            // the rest: no solves, the line drips in place
            let dp2 = scr[pz] - scr[b];
            writeln!(dy, "<text x=\"{:.1}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">8 months of rest: {dp2:+.0} pts</text>", yx(cum[b]) - 8.0, yy((scr[b] + scr[pz]) / 2.0) + 26.0).unwrap();
            // the consolidation: few solves, mostly re-solves, big lift
            let dn3 = cum[last] - cum[pz];
            let dp3 = scr[last] - scr[pz];
            let (n3, r3) = week_new[pz + 1..].iter().zip(&week_re[pz + 1..]).fold((0usize, 0usize), |(an, ar), (n, r)| (an + n, ar + r));
            let share = if n3 + r3 > 0 { 100.0 * r3 as f64 / (n3 + r3) as f64 } else { 0.0 };
            let cx = yx(cum[last]) + 6.0;
            let cy = yy(ymax * 0.32);
            writeln!(dy, "<text x=\"{cx:.1}\" y=\"{cy:.1}\" text-anchor=\"end\" font-size=\"13\" font-weight=\"bold\" fill=\"#3fb950\">the consolidation: {dn3:.0} solves → {dp3:+.0} pts</text>").unwrap();
            writeln!(dy, "<text x=\"{cx:.1}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"#3fb950\" opacity=\"0.85\">{share:.0}% re-solves, repairing stale ground</text>", cy + 16.0).unwrap();
        }

        // reveal on the movie clock: x = cumulative solves at the tick date,
        // monotone because solves only accumulate
        let mut ry: Vec<String> = days
            .iter()
            .map(|d| {
                let ds = d.to_string();
                let cx = yx(ev_recs.partition_point(|r| r.date.as_str() <= ds.as_str()) as f64);
                format!("{:.1}", cx.clamp(YML, CW - 2.0))
            })
            .collect();
        let mut rt: Vec<f64> = tick_frac.clone();
        ry.push(ry.last().unwrap().clone());
        push_key(&mut rt, 1.0);
        let ranim = animate("width", "linear", &ry, &rt, dur);
        writeln!(y, "<clipPath id=\"yreveal\"><rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{ranim}</rect></clipPath>").unwrap();
        let rrest = animate("x", "linear", &ry, &rt, dur);
        writeln!(y, "<clipPath id=\"yrest\"><rect x=\"{:.1}\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{rrest}</rect></clipPath>", CW - 2.0).unwrap();
        writeln!(y, "<g clip-path=\"url(#yrest)\" opacity=\"0.35\">\n{dy}</g>").unwrap();
        writeln!(y, "<g clip-path=\"url(#yreveal)\">\n{dy}</g>").unwrap();

        // end-of-path marker + label, popping in on the final tick
        let mut ft = vec![0.0];
        push_key(&mut ft, *tick_frac.last().unwrap());
        let yfinale = animate("opacity", "discrete", &["0".into(), "1".into()], &ft, dur);
        let (ex, ey) = (yx(cum[last]), yy(scr[last]));
        writeln!(y, "<circle cx=\"{ex:.1}\" cy=\"{ey:.1}\" r=\"4\" fill=\"{SCREEN_C}\" opacity=\"1\">{yfinale}</circle>").unwrap();
        writeln!(y, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"13\" font-weight=\"bold\" fill=\"{SCREEN_C}\" opacity=\"1\">{:.0}%{yfinale}</text>", ex + 8.0, ey - 8.0, scr[last]).unwrap();

        writeln!(
            y,
            "<rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
            animate("opacity", "linear", &["0".into(), "0".into(), "1".into()], &[0.0, fade_from, 1.0], dur)
        )
        .unwrap();
        writeln!(y, "</svg>").unwrap();

        let yield_path = graph.join("kg_yield.svg");
        std::fs::write(&yield_path, &y).unwrap();
        println!(
            "wrote {} — {:.0} solves along the x axis, synced to the {:.0}s loop, {:.0}KB",
            yield_path.display(),
            cum_total,
            seconds,
            y.len() as f64 / 1024.0
        );
    }

    // ---- two kinds of sideways: graph/kg_yield_time.svg ------------------
    // The P(pass) lines over what each week was MADE OF, on the calendar
    // axis shared with the other charts. Bar height = solves that week, bar
    // color = composition: green re-solves stacked under gray new problems.
    // A week is a regime, not a scorecard: flat P over tall gray bars is
    // the plateau (tons of new questions, nothing landing — more of the
    // same never breaks it); flat or slightly dipping P over green bars is
    // consolidation (revisits repairing ground, loading the next leg up).
    {
        const TPT: f64 = 64.0;
        const TPB: f64 = 368.0;

        let mut t = String::with_capacity(32 * 1024);
        writeln!(t, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
        writeln!(
            t,
            "<svg width=\"{CW:.0}pt\" height=\"{CH:.0}pt\" viewBox=\"0 0 {CW:.0} {CH:.0}\" xmlns=\"http://www.w3.org/2000/svg\" font-family=\"Helvetica,sans-serif\">"
        )
        .unwrap();
        writeln!(t, "<rect width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\"/>").unwrap();
        if split_x > 0.0 {
            writeln!(t, "<rect x=\"0\" y=\"0\" width=\"{split_x:.1}\" height=\"3\" fill=\"{ERA_PRE_INK}\" opacity=\"0.55\"/>").unwrap();
        }
        if switch.is_some() && split_x < CW {
            writeln!(t, "<rect x=\"{split_x:.1}\" y=\"0\" width=\"{:.1}\" height=\"3\" fill=\"{ERA_GRAPH_INK}\" opacity=\"0.9\"/>", CW - split_x).unwrap();
        }
        t.push_str(&era_banner(12.0, 26.0, 24.0, "start", era_frac, switch.is_some(), "", dur));
        writeln!(
            t,
            "<text x=\"{:.0}\" y=\"19\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">two kinds of sideways - P(pass) over what each week was made of</text>",
            CW / 2.0 + 100.0
        )
        .unwrap();
        writeln!(
            t,
            "<text x=\"{:.0}\" y=\"33\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">bars: re-solve share × slope × drill work ÷ √volume (<tspan fill=\"#3fb950\">green = re-solves</tspan>, gray = new problems) - tall = P held on few revisits; damped where P is climbing. lines: central P(pass) - <tspan fill=\"{SCREEN_C}\">phone screen</tspan> and <tspan fill=\"{ONSITE_C}\">onsite</tspan></text>",
            CW / 2.0 + 100.0
        )
        .unwrap();
        writeln!(
            t,
            "<text x=\"{:.0}\" y=\"48\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">flat P over gray = a plateau more new questions will not break; flat P over green = consolidation loading the next leg up</text>",
            CW / 2.0 + 100.0
        )
        .unwrap();

        // furniture: P% gridlines on the left, month ticks below
        const PMAX: f64 = 60.0;
        let py = |p: f64| TPB - p / PMAX * (TPB - TPT);
        for p in [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0] {
            let gy = py(p);
            writeln!(t, "<line x1=\"{CML}\" y1=\"{gy:.1}\" x2=\"{:.1}\" y2=\"{gy:.1}\" stroke=\"{GRID}\" stroke-width=\"1\"/>", CW - CMR).unwrap();
            writeln!(t, "<text x=\"{:.0}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{p:.0}%</text>", CML - 6.0, gy + 4.0).unwrap();
        }
        let mut m = NaiveDate::from_ymd_opt(x0.year(), x0.month(), 1).unwrap();
        while m <= xend {
            let nxt = NaiveDate::from_ymd_opt(m.year() + (m.month() == 12) as i32, m.month() % 12 + 1, 1).unwrap();
            if m >= x0 {
                let x = x_of(m);
                writeln!(t, "<line x1=\"{x:.1}\" y1=\"{TPB}\" x2=\"{x:.1}\" y2=\"{:.0}\" stroke=\"{MUTED}\" stroke-width=\"1\"/>", TPB + 4.0).unwrap();
                if x_of(nxt.min(xend)) - x >= 34.0 {
                    let lab = if m.month() == 1 {
                        format!("jan '{:02}", m.year() % 100)
                    } else {
                        MONTHS[m.month0() as usize].to_string()
                    };
                    writeln!(t, "<text x=\"{x:.1}\" y=\"{:.0}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{lab}</text>", TPB + 17.0).unwrap();
                }
            }
            m = nxt;
        }
        if let Ok(sw) = NaiveDate::parse_from_str(ERA_SWITCH, "%Y-%m-%d") {
            if sw > x0 && sw < xend {
                let x = x_of(sw);
                writeln!(t, "<line x1=\"{x:.1}\" y1=\"{TPT}\" x2=\"{x:.1}\" y2=\"{TPB}\" stroke=\"{ERA_GRAPH_INK}\" stroke-width=\"1.2\" stroke-dasharray=\"5 4\" opacity=\"0.6\"/>").unwrap();
            }
        }

        let mut dt = String::new();
        // stacked novelty bars from the baseline: green re-solves under gray
        // new problems. Height = re-solve share × slope weight ÷ volume —
        // smart-consolidation intensity. The slope weight keeps a bar tall
        // while the screen line is flat, wobbling, or dipping, and damps it
        // while the line climbs (there the line already tells the story);
        // dividing by √volume makes tall mean CHEAP, much held with little
        // solving (√ not raw, or near-empty weeks own the scale and real
        // work vanishes); the re-solve share gate means only revisit work
        // counts — a lone new-problem week can't fake it. So a tall green
        // bar is P held on a handful of revisits, while the plateau's flood
        // of new questions flattens to stubs.
        // flat or dipping keeps full weight (dips boost a little); any real
        // climb decays exponentially — a +1 pt/week wobble keeps a third,
        // +3 or more is effectively gone. Gentler damping let small-volume
        // weeks with mildly RISING P top the chart, which is neither kind
        // of sideways.
        let slope_w = |i: usize| {
            let s = if i == 0 { 0.0 } else { series[i][1].0 - series[i - 1][1].0 };
            if s <= 0.0 { 1.0 + (s.abs() / 4.0).min(0.6) } else { (-s).exp() }
        };
        let weighted: Vec<f64> = week_new
            .iter()
            .zip(&week_re)
            .enumerate()
            .map(|(i, (n, r))| {
                let tot = n + r;
                let share = *r as f64 / tot.max(1) as f64;
                // drill factor: 1 + 3× the drill share of the week's work,
                // capped at 4× — drills are the foundation consolidation
                // pours, so a week half-spent on drill building and review
                // more than doubles, and a drill-dominated week maxes out
                let dfac = 1.0 + (3.0 * week_drill[i] as f64 / (tot as f64).max(1.0)).min(3.0);
                slope_w(i) * share * dfac / (tot as f64).max(8.0).sqrt()
            })
            .collect();
        let vmax2 = weighted.iter().fold(0.0f64, |a, &b| a.max(b)).max(1e-9);
        let unit = 0.6 * (TPB - TPT) / vmax2;
        for (i, ((wd, nn), nr)) in weeks.iter().zip(&week_new).zip(&week_re).enumerate() {
            if *nn + *nr == 0 {
                continue;
            }
            let x1 = x_of(*wd - Duration::days(6));
            let w = (x_of(*wd) - x1).max(1.5);
            let h = weighted[i] * unit;
            let h_re = h * *nr as f64 / (*nn + *nr) as f64;
            let h_new = h - h_re;
            if *nr > 0 {
                writeln!(dt, "<rect x=\"{x1:.1}\" y=\"{:.1}\" width=\"{w:.1}\" height=\"{:.1}\" fill=\"#3fb950\"/>", TPB - h_re, h_re.max(1.0)).unwrap();
            }
            if *nn > 0 {
                writeln!(dt, "<rect x=\"{x1:.1}\" y=\"{:.1}\" width=\"{w:.1}\" height=\"{:.1}\" fill=\"#57606a\"/>", TPB - h_re - h_new, h_new.max(1.0)).unwrap();
            }
        }

        // the P(pass) lines on top of the bars, right-axis scale — the same
        // central lines as kg_pass.svg, here to show the two kinds of
        // sideways: flat over gray/red noise goes nowhere, flat-then-up over
        // green was being loaded
        for (kind, color) in [(0usize, SCREEN_C), (1usize, ONSITE_C)] {
            let line: Vec<String> = weeks
                .iter()
                .enumerate()
                .map(|(i, wd)| {
                    let v = if kind == 0 { series[i][1].0 } else { series[i][1].1 };
                    format!("{:.1},{:.1}", x_of(*wd), py(v.min(PMAX)))
                })
                .collect();
            writeln!(dt, "<polyline points=\"{}\" fill=\"none\" stroke=\"{color}\" stroke-width=\"2\"/>", line.join(" ")).unwrap();
        }

        // era callouts, computed from the replay
        let widx = |d: NaiveDate| weeks.partition_point(|w| *w <= d).saturating_sub(1);
        let a = widx(NaiveDate::from_ymd_opt(2025, 10, 6).unwrap());
        let b = widx(NaiveDate::from_ymd_opt(2025, 11, 30).unwrap());
        let pz = widx(NaiveDate::from_ymd_opt(2026, 7, 31).unwrap());
        let last = weeks.len() - 1;
        if a < b && b < pz && pz < last {
            let comp = |lo: usize, hi: usize| {
                let (n, r) = week_new[lo..=hi].iter().zip(&week_re[lo..=hi]).fold((0usize, 0usize), |(an, ar), (n, r)| (an + n, ar + r));
                (n + r, 100.0 * n as f64 / (n + r).max(1) as f64)
            };
            let (gn, gnew) = comp(a + 1, b);
            let gp = series[b][1].0 - series[a][1].0;
            let xm = ((x_of(weeks[a]) + x_of(weeks[b])) / 2.0).max(CML + 260.0);
            writeln!(dt, "<text x=\"{xm:.1}\" y=\"{:.1}\" text-anchor=\"middle\" font-size=\"13\" font-weight=\"bold\" fill=\"{INK}\">sideways going nowhere: {gn} solves, {gnew:.0}% new → {gp:+.0} pts</text>", TPT + 16.0).unwrap();
            writeln!(dt, "<text x=\"{xm:.1}\" y=\"{:.1}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">tons of new questions over ground already held - more of them will not break it</text>", TPT + 32.0).unwrap();
            let (cn, cnew) = comp(pz + 1, last);
            let cp = series[last][1].0 - series[pz][1].0;
            let xc = x_of(weeks[pz]) - 10.0;
            writeln!(dt, "<text x=\"{xc:.1}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"13\" font-weight=\"bold\" fill=\"#3fb950\">loading the next leg: {cn} solves, {:.0}% revisits → {cp:+.0} pts</text>", TPT + 16.0, 100.0 - cnew).unwrap();
            writeln!(dt, "<text x=\"{xc:.1}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"#3fb950\" opacity=\"0.85\">a third of the volume, repairing stale ground - a dip here still preps the climb</text>", TPT + 32.0).unwrap();
        }

        // reveal + playhead on the shared calendar clock
        let tanim = animate("width", "linear", &reveal_x, &reveal_t, dur);
        writeln!(t, "<clipPath id=\"treveal\"><rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{tanim}</rect></clipPath>").unwrap();
        let trest = animate("x", "linear", &reveal_x, &reveal_t, dur);
        writeln!(t, "<clipPath id=\"trest\"><rect x=\"{:.1}\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{trest}</rect></clipPath>", CW - CMR).unwrap();
        writeln!(t, "<g clip-path=\"url(#trest)\" opacity=\"0.35\">\n{dt}</g>").unwrap();
        writeln!(t, "<g clip-path=\"url(#treveal)\">\n{dt}</g>").unwrap();
        let thead = animate("x", "linear", &reveal_x, &reveal_t, dur);
        writeln!(t, "<rect x=\"{:.1}\" y=\"{TPT}\" width=\"1.5\" height=\"{:.0}\" fill=\"{INK}\" opacity=\"0.75\">{thead}</rect>", CW - CMR, TPB - TPT).unwrap();
        // line end labels pop in on the final tick, kg_pass style
        let mut tft = vec![0.0];
        push_key(&mut tft, *tick_frac.last().unwrap());
        let tfinale = animate("opacity", "discrete", &["0".into(), "1".into()], &tft, dur);
        let lx = x_of(*weeks.last().unwrap());
        for (color, v) in [(SCREEN_C, series.last().unwrap()[1].0), (ONSITE_C, series.last().unwrap()[1].1)] {
            writeln!(t, "<text x=\"{:.1}\" y=\"{:.1}\" font-size=\"12\" font-weight=\"bold\" fill=\"{color}\" opacity=\"1\">{v:.0}%{tfinale}</text>", lx + 8.0, py(v.min(PMAX)) + 4.0).unwrap();
        }
        writeln!(
            t,
            "<rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
            animate("opacity", "linear", &["0".into(), "0".into(), "1".into()], &[0.0, fade_from, 1.0], dur)
        )
        .unwrap();
        writeln!(t, "</svg>").unwrap();

        let tp = graph.join("kg_yield_time.svg");
        std::fs::write(&tp, &t).unwrap();
        println!(
            "wrote {} — {} weeks of yield, synced to the {:.0}s loop, {:.0}KB",
            tp.display(),
            weeks.len(),
            seconds,
            t.len() as f64 / 1024.0
        );
    }

    // ---- mock outcome distribution: graph/kg_dist.svg --------------------
    // The mass behind the P(pass) central line: per DAY (weekly steps read as
    // jitter), how the 4000 simulated mocks distribute over problems solved
    // (0..=6 of the 2E+2M+2H set), stepping tick for tick on the shared
    // clock. The slice of each bin that clears the onsite bar (2E+2M+>=1
    // hard — only 5s and 6s can) is lit in the onsite color, so the pass
    // rate reads as the lit mass. Same seed and inputs as the central
    // pass_rates call, so on kg_pass's weekly stations they agree exactly.
    // The swarm chart tracks the first SWARM_N of those sims individually.
    // Every day re-runs seed 42, so sim i rolls the SAME dice each day
    // (common random numbers): its dot moves only when the day's improved
    // recall actually flips one of its problems.
    const SWARM_N: usize = 150;
    // blame: failed problems attributed to the weakest move in their walk,
    // rolled up by technique group; last band = off-graph moves
    let n_groups = groups.len();
    let mf_group: Vec<usize> = bank
        .move_names
        .iter()
        .map(|key| {
            node_index
                .get(key.as_str())
                .and_then(|&ni| groups.iter().position(|(g, _)| *g == nodes[ni].group))
                .unwrap_or(n_groups)
        })
        .collect();
    let mut dists: Vec<([f64; 7], [f64; 7])> = Vec::with_capacity(n_ticks);
    let mut swarm: Vec<Vec<(usize, bool)>> = Vec::with_capacity(n_ticks); // (solved, onsite) per sim
    let mut blame_days: Vec<Vec<u32>> = Vec::with_capacity(n_ticks);
    for day in &days {
        let d_s = day.to_string();
        let k = ev_recs.partition_point(|r| r.date.as_str() <= d_s.as_str());
        let recall = current_recall(&node_ids, &ev_recs[..k], &mcurve, *day);
        let mv_recall: Vec<Option<f64>> = (0..bank.move_names.len())
            .map(|i| if i < bank.n_known { Some(recall[i]) } else { None })
            .collect();
        let (mut hist, mut onsite_hist) = ([0i64; 7], [0i64; 7]);
        let mut sims = Vec::with_capacity(SWARM_N);
        let mut blame = vec![0u32; n_groups + 1];
        run_mocks(
            &mv_recall, &bank.pools, SCENARIOS[1].1, (0, 0, 0),
            &mut PyRandom::new(42), 4000,
            |solved, probs| {
                let t = (solved[0] + solved[1] + solved[2]) as usize;
                let onsite = solved[0] == 2 && solved[1] == 2 && solved[2] >= 1;
                hist[t] += 1;
                onsite_hist[t] += onsite as i64;
                if sims.len() < SWARM_N {
                    sims.push((t, onsite));
                }
                for &(wi, failed) in probs {
                    if failed {
                        blame[if wi == usize::MAX { n_groups } else { mf_group[wi] }] += 1;
                    }
                }
            },
        );
        dists.push((hist.map(|v| v as f64 / 4000.0), onsite_hist.map(|v| v as f64 / 4000.0)));
        swarm.push(sims);
        blame_days.push(blame);
    }
    const DH: f64 = 430.0;
    const DML: f64 = 48.0;
    const DMR: f64 = 24.0;
    const DPT: f64 = 56.0;
    const DPB: f64 = 360.0;
    let y_max = dists
        .iter()
        .flat_map(|(h, _)| h.iter().copied())
        .fold(0.0f64, f64::max)
        .mul_add(10.0, 0.999)
        .floor()
        / 10.0;
    let dy_of = |share: f64| DPB - share / y_max * (DPB - DPT);
    let collapse = |vals: &[String], attr: &str| -> String {
        discrete_track(vals, &tick_frac, attr, dur).unwrap_or_default()
    };

    let mut ds = String::with_capacity(32 * 1024);
    writeln!(ds, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
    writeln!(ds, "<svg width=\"{CW:.0}pt\" height=\"{DH:.0}pt\" viewBox=\"0 0 {CW:.0} {DH:.0}\" xmlns=\"http://www.w3.org/2000/svg\" font-family=\"Helvetica,sans-serif\">").unwrap();
    writeln!(ds, "<rect width=\"{CW:.0}\" height=\"{DH:.0}\" fill=\"{BG}\"/>").unwrap();
    writeln!(ds, "<text x=\"{:.0}\" y=\"24\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">The Monte Carlo mass behind P(pass) — 4000 simulated mocks/week by problems solved, central scenario</text>", CW / 2.0).unwrap();
    ds.push_str(&era_banner(DML, 48.0, 26.0, "start", era_frac, switch.is_some(), "", dur));

    for p in [0.0, 0.25, 0.5, 0.75, 1.0] {
        let share = p * y_max;
        let y = dy_of(share);
        writeln!(ds, "<line x1=\"{DML}\" y1=\"{y:.1}\" x2=\"{:.1}\" y2=\"{y:.1}\" stroke=\"{GRID}\" stroke-width=\"1\"/>", CW - DMR).unwrap();
        writeln!(ds, "<text x=\"{:.0}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{:.0}%</text>", DML - 6.0, y + 4.0, share * 100.0).unwrap();
    }

    let group_w = (CW - DML - DMR) / 7.0;
    let bar_w = group_w * 0.5;
    for bin in 0..7usize {
        let bx = DML + bin as f64 * group_w + (group_w - bar_w) / 2.0;
        let (fin_h, fin_o) = (dists.last().unwrap().0[bin], dists.last().unwrap().1[bin]);
        // rest of the bin above, onsite-clearing slice grounded at the axis
        let rest_y: Vec<String> = dists.iter().map(|(h, _)| format!("{:.1}", dy_of(h[bin]))).collect();
        let rest_h: Vec<String> =
            dists.iter().map(|(h, o)| format!("{:.1}", (h[bin] - o[bin]) / y_max * (DPB - DPT))).collect();
        let pass_y: Vec<String> = dists.iter().map(|(_, o)| format!("{:.1}", dy_of(o[bin]))).collect();
        let pass_h: Vec<String> =
            dists.iter().map(|(_, o)| format!("{:.1}", o[bin] / y_max * (DPB - DPT))).collect();
        writeln!(
            ds,
            "<rect x=\"{bx:.1}\" y=\"{:.1}\" width=\"{bar_w:.1}\" height=\"{:.1}\" fill=\"{SCREEN_C}\" opacity=\"0.85\">{}{}</rect>",
            dy_of(fin_h),
            (fin_h - fin_o) / y_max * (DPB - DPT),
            collapse(&rest_y, "y"),
            collapse(&rest_h, "height")
        )
        .unwrap();
        writeln!(
            ds,
            "<rect x=\"{bx:.1}\" y=\"{:.1}\" width=\"{bar_w:.1}\" height=\"{:.1}\" fill=\"{ONSITE_C}\">{}{}</rect>",
            dy_of(fin_o),
            fin_o / y_max * (DPB - DPT),
            collapse(&pass_y, "y"),
            collapse(&pass_h, "height")
        )
        .unwrap();
        writeln!(
            ds,
            "<text x=\"{:.1}\" y=\"{:.0}\" text-anchor=\"middle\" font-size=\"12\" fill=\"{MUTED}\">{bin} solved</text>",
            bx + bar_w / 2.0,
            DPB + 18.0
        )
        .unwrap();
    }

    // legend + threshold note, top right where the low bins live early on
    for (i, (color, label)) in [
        (SCREEN_C, "share of simulated mocks"),
        (ONSITE_C, "clears the onsite bar (2E+2M+\u{2265}1H)"),
    ]
    .iter()
    .enumerate()
    {
        let y = DPT + 4.0 + i as f64 * 18.0;
        writeln!(ds, "<rect x=\"{:.0}\" y=\"{:.1}\" width=\"14\" height=\"10\" fill=\"{color}\"/>", CW - DMR - 260.0, y - 9.0).unwrap();
        writeln!(ds, "<text x=\"{:.0}\" y=\"{y:.1}\" font-size=\"12\" fill=\"{INK}\">{label}</text>", CW - DMR - 240.0).unwrap();
    }

    // month ticker on the movie's tick, like the python-rendered charts
    let mut m = NaiveDate::from_ymd_opt(days[0].year(), days[0].month(), 1).unwrap();
    let mut month_starts = vec![];
    while m <= today {
        month_starts.push(m);
        m = NaiveDate::from_ymd_opt(m.year() + (m.month() == 12) as i32, m.month() % 12 + 1, 1).unwrap();
    }
    for (i, m) in month_starts.iter().enumerate() {
        let fs = tick_frac[((*m - days[0]).num_days().max(0) as usize).min(n_ticks - 1)];
        let fe = month_starts
            .get(i + 1)
            .map_or(1.0, |n| tick_frac[((*n - days[0]).num_days() as usize).min(n_ticks - 1)]);
        let lab = format!("{} '{:02}", MONTHS[m.month0() as usize], m.year() % 100);
        let (values, times) = if fs > 0.0 {
            if i + 1 < month_starts.len() {
                (vec!["0".to_string(), "1".into(), "0".into()], vec![0.0, fs, fe])
            } else {
                (vec!["0".to_string(), "1".into()], vec![0.0, fs])
            }
        } else {
            (vec!["1".to_string(), "0".into()], vec![0.0, fe])
        };
        writeln!(
            ds,
            "<text x=\"{:.0}\" y=\"24\" text-anchor=\"end\" font-size=\"14\" fill=\"{INK}\" opacity=\"0\">{lab}{}</text>",
            CW - DMR,
            animate("opacity", "discrete", &values, &times, dur)
        )
        .unwrap();
    }

    writeln!(
        ds,
        "<rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{DH:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
        animate("opacity", "linear", &["0".into(), "0".into(), "1".into()], &[0.0, fade_from, 1.0], dur)
    )
    .unwrap();
    writeln!(ds, "</svg>").unwrap();

    let dist_path = graph.join("kg_dist.svg");
    std::fs::write(&dist_path, &ds).unwrap();
    println!(
        "wrote {} — {} daily distributions, synced to the {:.0}s loop, {:.0}KB",
        dist_path.display(),
        dists.len(),
        seconds,
        ds.len() as f64 / 1024.0
    );

    // ---- swarm: graph/kg_swarm.svg ---------------------------------------
    // The same simulation, dot by dot: SWARM_N individual mocks re-taken
    // daily with the same dice, packing into their solved-count bins. A dot
    // lights up in the onsite color the day its fixed luck plus current
    // skill clears the onsite bar. Companion to kg_dist.svg: that chart is
    // the mass, this one is the dice.
    const SH: f64 = 340.0;
    const SPB: f64 = 270.0;
    let sgroup = (CW - DML - DMR) / 7.0;
    let per_row = 10usize;
    let dot_step = 13.0;
    let n_dots = swarm[0].len();
    let mut dot_x: Vec<Vec<String>> = vec![Vec::with_capacity(n_ticks); n_dots];
    let mut dot_y: Vec<Vec<String>> = vec![Vec::with_capacity(n_ticks); n_dots];
    let mut dot_c: Vec<Vec<String>> = vec![Vec::with_capacity(n_ticks); n_dots];
    for sims in &swarm {
        let mut counts = [0usize; 7];
        for (i, &(bin, onsite)) in sims.iter().enumerate() {
            let slot = counts[bin];
            counts[bin] += 1;
            let (row, col) = (slot / per_row, slot % per_row);
            let x = DML
                + bin as f64 * sgroup
                + (sgroup - per_row as f64 * dot_step) / 2.0
                + col as f64 * dot_step
                + dot_step / 2.0;
            let y = SPB - 7.0 - row as f64 * dot_step;
            dot_x[i].push(format!("{x:.0}"));
            dot_y[i].push(format!("{y:.0}"));
            dot_c[i].push((if onsite { ONSITE_C } else { SCREEN_C }).to_string());
        }
    }

    let mut sw = String::with_capacity(64 * 1024);
    writeln!(sw, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
    writeln!(sw, "<svg width=\"{CW:.0}pt\" height=\"{SH:.0}pt\" viewBox=\"0 0 {CW:.0} {SH:.0}\" xmlns=\"http://www.w3.org/2000/svg\" font-family=\"Helvetica,sans-serif\">").unwrap();
    writeln!(sw, "<rect width=\"{CW:.0}\" height=\"{SH:.0}\" fill=\"{BG}\"/>").unwrap();
    writeln!(sw, "<text x=\"{:.0}\" y=\"24\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">The dice themselves — {n_dots} of the simulated mocks, same rolls every day: a dot hops bins only when skill flips one of its problems</text>", CW / 2.0).unwrap();
    sw.push_str(&era_banner(DML, 60.0, 26.0, "start", era_frac, switch.is_some(), "", dur));

    writeln!(sw, "<line x1=\"{DML}\" y1=\"{SPB}\" x2=\"{:.1}\" y2=\"{SPB}\" stroke=\"{GRID}\" stroke-width=\"1\"/>", CW - DMR).unwrap();
    for bin in 0..7usize {
        writeln!(
            sw,
            "<text x=\"{:.1}\" y=\"{:.0}\" text-anchor=\"middle\" font-size=\"12\" fill=\"{MUTED}\">{bin} solved</text>",
            DML + (bin as f64 + 0.5) * sgroup,
            SPB + 18.0
        )
        .unwrap();
    }
    for (i, (color, label)) in
        [(SCREEN_C, "one simulated mock"), (ONSITE_C, "clears the onsite bar (2E+2M+\u{2265}1H)")]
            .iter()
            .enumerate()
    {
        let y = 52.0 + i as f64 * 18.0;
        writeln!(sw, "<circle cx=\"{:.0}\" cy=\"{:.1}\" r=\"5\" fill=\"{color}\"/>", CW - DMR - 254.0, y - 4.0).unwrap();
        writeln!(sw, "<text x=\"{:.0}\" y=\"{y:.1}\" font-size=\"12\" fill=\"{INK}\">{label}</text>", CW - DMR - 240.0).unwrap();
    }

    for i in 0..n_dots {
        writeln!(
            sw,
            "<circle cx=\"{}\" cy=\"{}\" r=\"5\" fill=\"{}\">{}{}{}</circle>",
            dot_x[i].last().unwrap(),
            dot_y[i].last().unwrap(),
            dot_c[i].last().unwrap(),
            discrete_track(&dot_x[i], &tick_frac, "cx", dur).unwrap_or_default(),
            discrete_track(&dot_y[i], &tick_frac, "cy", dur).unwrap_or_default(),
            discrete_track(&dot_c[i], &tick_frac, "fill", dur).unwrap_or_default()
        )
        .unwrap();
    }

    for (i, m) in month_starts.iter().enumerate() {
        let fs = tick_frac[((*m - days[0]).num_days().max(0) as usize).min(n_ticks - 1)];
        let fe = month_starts
            .get(i + 1)
            .map_or(1.0, |n| tick_frac[((*n - days[0]).num_days() as usize).min(n_ticks - 1)]);
        let lab = format!("{} '{:02}", MONTHS[m.month0() as usize], m.year() % 100);
        let (values, times) = if fs > 0.0 {
            if i + 1 < month_starts.len() {
                (vec!["0".to_string(), "1".into(), "0".into()], vec![0.0, fs, fe])
            } else {
                (vec!["0".to_string(), "1".into()], vec![0.0, fs])
            }
        } else {
            (vec!["1".to_string(), "0".into()], vec![0.0, fe])
        };
        writeln!(
            sw,
            "<text x=\"{:.0}\" y=\"24\" text-anchor=\"end\" font-size=\"14\" fill=\"{INK}\" opacity=\"0\">{lab}{}</text>",
            CW - DMR,
            animate("opacity", "discrete", &values, &times, dur)
        )
        .unwrap();
    }

    writeln!(
        sw,
        "<rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{SH:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
        animate("opacity", "linear", &["0".into(), "0".into(), "1".into()], &[0.0, fade_from, 1.0], dur)
    )
    .unwrap();
    writeln!(sw, "</svg>").unwrap();

    let swarm_path = graph.join("kg_swarm.svg");
    std::fs::write(&swarm_path, &sw).unwrap();
    println!(
        "wrote {} — {} dots over {} days, synced to the {:.0}s loop, {:.0}KB",
        swarm_path.display(),
        n_dots,
        n_ticks,
        seconds,
        sw.len() as f64 / 1024.0
    );

    // ---- blame: graph/kg_blame.svg ---------------------------------------
    // WHY the simulated mocks fail: every failed problem blamed on the
    // weakest move in its walk, rolled up by technique group, stacked over
    // the calendar and revealed on the movie's clock (same axis, reveal and
    // playhead as kg_pass.svg). The y axis is the ABSOLUTE share of all
    // simulated problems failing — not normalized to 100% — so the whole
    // mountain sinking IS the improvement, and the bands are who's to blame
    // for what remains. Top groups get their own band; the rest pool into
    // "other"; moves not on the graph yet are the off-graph band on top.
    const BPT: f64 = 66.0;
    const BPB: f64 = 380.0;
    const N_TOP: usize = 7;
    let mut totals = vec![0u64; n_groups + 1];
    for day in &blame_days {
        for (b, v) in day.iter().enumerate() {
            totals[b] += *v as u64;
        }
    }
    let mut top: Vec<usize> = (0..n_groups).collect();
    top.sort_by_key(|&g| std::cmp::Reverse(totals[g]));
    top.truncate(N_TOP);
    // bands, bottom to top: top groups by total blame, other, off-graph
    let mut bands: Vec<(String, Vec<usize>)> =
        top.iter().map(|&g| (groups[g].0.to_string(), vec![g])).collect();
    let rest: Vec<usize> = (0..n_groups).filter(|g| !top.contains(g)).collect();
    if !rest.is_empty() {
        bands.push(("other groups".into(), rest));
    }
    bands.push(("off-graph moves".into(), vec![n_groups]));
    const BAND_C: [&str; 9] =
        ["#f85149", "#ff7f0e", "#e3b341", "#3fb950", "#1f77b4", "#a371f7", "#58a6ff", "#8b949e", "#484f58"];
    let n_bands = bands.len();
    let band_color = |bi: usize| {
        if bi + 2 == n_bands && n_bands == 9 { BAND_C[7] }        // other
        else if bi + 1 == n_bands { BAND_C[8] }                    // off-graph
        else { BAND_C[bi.min(6)] }
    };

    // per day: cumulative failure-rate boundaries (share of ALL simulated
    // problems, 6 per mock), bottom band first
    let n_problems = 4000.0 * 6.0;
    let mut cum_shares: Vec<Vec<f64>> = Vec::with_capacity(n_ticks); // per day, len n_bands+1
    for day in &blame_days {
        let mut cum = vec![0.0];
        for (_, members) in &bands {
            let s: f64 = members.iter().map(|&b| day[b] as f64).sum::<f64>() / n_problems;
            cum.push(cum.last().unwrap() + s);
        }
        cum_shares.push(cum);
    }
    let by_max = cum_shares
        .iter()
        .map(|c| *c.last().unwrap())
        .fold(0.0f64, f64::max)
        .mul_add(20.0, 0.999)
        .floor()
        / 20.0;
    let by_of = |share: f64| BPB - share / by_max * (BPB - BPT);

    let mut bl = String::with_capacity(128 * 1024);
    writeln!(bl, "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>").unwrap();
    writeln!(bl, "<svg width=\"{CW:.0}pt\" height=\"{CH:.0}pt\" viewBox=\"0 0 {CW:.0} {CH:.0}\" xmlns=\"http://www.w3.org/2000/svg\" font-family=\"Helvetica,sans-serif\">").unwrap();
    writeln!(bl, "<rect width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\"/>").unwrap();
    writeln!(bl, "<text x=\"{:.0}\" y=\"19\" text-anchor=\"middle\" font-size=\"13\" fill=\"{INK}\">Why the simulated mocks fail — share of all simulated problems failing, blamed on the weakest move in the walk: down = fewer fails</text>", CW / 2.0).unwrap();
    bl.push_str(&era_banner(CML + 10.0, BPT + 34.0, 30.0, "start", era_frac, switch.is_some(), BG, dur));

    // legend: one row of swatches under the title
    let mut lx = CML;
    for (bi, (name, _)) in bands.iter().enumerate() {
        writeln!(bl, "<rect x=\"{lx:.0}\" y=\"30\" width=\"12\" height=\"12\" fill=\"{}\"/>", band_color(bi)).unwrap();
        writeln!(bl, "<text x=\"{:.0}\" y=\"40\" font-size=\"12\" fill=\"{INK}\">{name}</text>", lx + 16.0).unwrap();
        lx += 16.0 + 8.0 + 7.2 * name.len() as f64 + 14.0;
    }

    for p in [0.0, 0.25, 0.5, 0.75, 1.0] {
        let share = p * by_max;
        let y = by_of(share);
        writeln!(bl, "<line x1=\"{CML}\" y1=\"{y:.1}\" x2=\"{:.1}\" y2=\"{y:.1}\" stroke=\"{GRID}\" stroke-width=\"1\"/>", CW - CMR).unwrap();
        writeln!(bl, "<text x=\"{:.0}\" y=\"{:.1}\" text-anchor=\"end\" font-size=\"11\" fill=\"{MUTED}\">{:.0}%</text>", CML - 6.0, y + 4.0, share * 100.0).unwrap();
    }
    let mut m = NaiveDate::from_ymd_opt(x0.year(), x0.month(), 1).unwrap();
    while m <= xend {
        let nxt = NaiveDate::from_ymd_opt(m.year() + (m.month() == 12) as i32, m.month() % 12 + 1, 1).unwrap();
        if m >= x0 {
            let x = x_of(m);
            writeln!(bl, "<line x1=\"{x:.1}\" y1=\"{BPB}\" x2=\"{x:.1}\" y2=\"{:.0}\" stroke=\"{MUTED}\" stroke-width=\"1\"/>", BPB + 4.0).unwrap();
            if x_of(nxt.min(xend)) - x >= 34.0 {
                let lab = if m.month() == 1 {
                    format!("jan '{:02}", m.year() % 100)
                } else {
                    MONTHS[m.month0() as usize].to_string()
                };
                writeln!(bl, "<text x=\"{x:.1}\" y=\"{:.0}\" text-anchor=\"middle\" font-size=\"11\" fill=\"{MUTED}\">{lab}</text>", BPB + 17.0).unwrap();
            }
        }
        m = nxt;
    }

    let breveal_anim = animate("width", "linear", &reveal_x, &reveal_t, dur);
    writeln!(bl, "<clipPath id=\"breveal\"><rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{breveal_anim}</rect></clipPath>").unwrap();
    let brest_anim = animate("x", "linear", &reveal_x, &reveal_t, dur);
    writeln!(bl, "<clipPath id=\"brest\"><rect x=\"{:.1}\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\">{brest_anim}</rect></clipPath>", CW - CMR).unwrap();
    let mut bd = String::new();
    for bi in 0..n_bands {
        let mut pts = String::new();
        for (di, day) in days.iter().enumerate() {
            write!(pts, "{:.1},{:.1} ", x_of(*day).clamp(CML, CW - CMR), by_of(cum_shares[di][bi + 1])).unwrap();
        }
        for (di, day) in days.iter().enumerate().rev() {
            write!(pts, "{:.1},{:.1} ", x_of(*day).clamp(CML, CW - CMR), by_of(cum_shares[di][bi])).unwrap();
        }
        writeln!(bd, "<polygon points=\"{}\" fill=\"{}\" opacity=\"0.9\"/>", pts.trim_end(), band_color(bi)).unwrap();
    }
    // dimmed ahead of the playhead, full strength behind it
    writeln!(bl, "<g clip-path=\"url(#brest)\" opacity=\"0.5\">\n{bd}</g>").unwrap();
    writeln!(bl, "<g clip-path=\"url(#breveal)\">\n{bd}</g>").unwrap();

    if let Ok(sw_d) = NaiveDate::parse_from_str(ERA_SWITCH, "%Y-%m-%d") {
        if sw_d > x0 && sw_d < xend {
            let x = x_of(sw_d);
            writeln!(bl, "<line x1=\"{x:.1}\" y1=\"{BPT}\" x2=\"{x:.1}\" y2=\"{BPB}\" stroke=\"{ERA_GRAPH_INK}\" stroke-width=\"1.2\" stroke-dasharray=\"5 4\" opacity=\"0.6\"/>").unwrap();
        }
    }
    let bhead_anim = animate("x", "linear", &reveal_x, &reveal_t, dur);
    writeln!(bl, "<rect x=\"{:.1}\" y=\"{BPT}\" width=\"1.5\" height=\"{:.0}\" fill=\"{INK}\" opacity=\"0.75\">{bhead_anim}</rect>", CW - CMR, BPB - BPT).unwrap();

    writeln!(
        bl,
        "<rect x=\"0\" y=\"0\" width=\"{CW:.0}\" height=\"{CH:.0}\" fill=\"{BG}\" opacity=\"0\" pointer-events=\"none\">{}</rect>",
        animate("opacity", "linear", &["0".into(), "0".into(), "1".into()], &[0.0, fade_from, 1.0], dur)
    )
    .unwrap();
    writeln!(bl, "</svg>").unwrap();

    let blame_path = graph.join("kg_blame.svg");
    std::fs::write(&blame_path, &bl).unwrap();
    println!(
        "wrote {} — {} bands over {} days, synced to the {:.0}s loop, {:.0}KB",
        blame_path.display(),
        n_bands,
        n_ticks,
        seconds,
        bl.len() as f64 / 1024.0
    );
}
