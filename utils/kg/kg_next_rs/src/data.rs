// The graph files as typed tables: graph/nodes.json, graph/problems.json,
// graph/evidence.json, graph/drills.json, graph/curve.json,
// data/problems_metadata.json, and the .envrc knobs. Mirrors the loaders at
// the top of utils/kg/kg_lib.py; every table keeps its file order, since
// the picker's tie-breaks are the order the Python dicts iterate in.

use std::collections::HashMap;
use std::path::{Path, PathBuf};

use chrono::{FixedOffset, NaiveDate, Utc};
use indexmap::IndexMap;
use serde_json::Value;

pub const SOLID_WINDOW_DAYS: i64 = 42;
pub const PENDING_STALE_SECONDS: f64 = 600.0;

/// kg_lib.MAX_ASLEEP: parked problems at once (env, default 3).
pub fn max_asleep() -> i64 {
    env_str("MAX_ASLEEP").trim().parse().unwrap_or(3)
}

/// Manila is UTC+8: "today" everywhere in the toolchain is the Manila day.
pub fn manila() -> FixedOffset {
    FixedOffset::east_opt(8 * 3600).unwrap()
}

pub fn real_today() -> NaiveDate {
    Utc::now().with_timezone(&manila()).date_naive()
}

pub fn parse_date(s: &str) -> NaiveDate {
    NaiveDate::parse_from_str(s, "%Y-%m-%d").unwrap_or_else(|_| panic!("bad date {s:?}"))
}

/// The repo root: the directory holding graph/nodes.json, found from
/// KG_ROOT, the binary's own location (utils/kg/kg_next_rs/target/...), or
/// the working directory.
pub fn repo_root() -> PathBuf {
    if let Ok(r) = std::env::var("KG_ROOT") {
        return PathBuf::from(r);
    }
    let mut candidates: Vec<PathBuf> = Vec::new();
    if let Ok(exe) = std::env::current_exe() {
        let mut p = exe.as_path();
        while let Some(parent) = p.parent() {
            candidates.push(parent.to_path_buf());
            p = parent;
        }
    }
    if let Ok(cwd) = std::env::current_dir() {
        candidates.push(cwd);
    }
    for c in candidates {
        if c.join("graph").join("nodes.json").exists() {
            return c;
        }
    }
    PathBuf::from(".")
}

/// kg_lib.load_envrc: `export NAME=VALUE` lines of .envrc set in this
/// process's environment unless already set; a `$` value is left to the
/// shell.
pub fn load_envrc(root: &Path) {
    let Ok(text) = std::fs::read_to_string(root.join(".envrc")) else {
        return;
    };
    for raw in text.lines() {
        let mut line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some(rest) = line.strip_prefix("export ") {
            line = rest.trim();
        }
        let Some((name, value)) = line.split_once('=') else {
            continue;
        };
        let name = name.trim();
        let ok = !name.is_empty()
            && name
                .chars()
                .next()
                .is_some_and(|c| c.is_ascii_alphabetic() || c == '_')
            && name.chars().all(|c| c.is_ascii_alphanumeric() || c == '_');
        if !ok {
            continue;
        }
        let mut value = value.trim().to_string();
        let quoted = value.len() >= 2
            && value.starts_with(value.chars().last().unwrap())
            && (value.starts_with('"') || value.starts_with('\''));
        if quoted {
            value = value[1..value.len() - 1].to_string();
        } else if value.contains('$') {
            continue;
        }
        if std::env::var_os(name).is_none() {
            std::env::set_var(name, value);
        }
    }
}

pub fn env_str(name: &str) -> String {
    std::env::var(name).unwrap_or_default()
}

#[derive(Clone, Debug, Default)]
pub struct Node {
    pub id: String,
    pub name: String,
    pub group: Option<String>,
    pub prereqs: Vec<String>,
}

pub type Nodes = IndexMap<String, Node>;

#[derive(Clone, Debug, Default)]
pub struct Walk {
    pub moves: Vec<String>,
    pub missing: bool,
}

#[derive(Clone, Debug, Default)]
pub struct Problem {
    pub title: String,
    pub difficulty: Option<String>,
    pub moves: Vec<String>,
    pub alt_walks: Vec<Vec<String>>,
    pub after: Vec<String>,
    pub banned: bool,
    pub note: Option<String>,
    pub unmapped: Vec<String>,
    pub walks: Vec<Walk>,
    pub draft: bool,
    pub predicted: bool,
}

impl Problem {
    pub fn difficulty(&self) -> &str {
        self.difficulty.as_deref().unwrap_or("")
    }

    pub fn is_hard(&self) -> bool {
        self.difficulty() == "Hard"
    }
}

pub type Problems = IndexMap<String, Problem>;

fn str_list(v: Option<&Value>) -> Vec<String> {
    v.and_then(Value::as_array)
        .map(|a| a.iter().map(value_str).collect())
        .unwrap_or_default()
}

/// str(v) for the ids an "after" list or a "problem" field may hold as
/// numbers.
pub fn value_str(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Number(n) => n.to_string(),
        Value::Bool(b) => (if *b { "True" } else { "False" }).to_string(),
        Value::Null => "None".to_string(),
        other => other.to_string(),
    }
}

pub fn parse_problem(v: &Value) -> Problem {
    Problem {
        title: v
            .get("title")
            .and_then(Value::as_str)
            .unwrap_or("")
            .to_string(),
        difficulty: v
            .get("difficulty")
            .and_then(Value::as_str)
            .map(String::from),
        moves: str_list(v.get("moves")),
        alt_walks: v
            .get("alt_walks")
            .and_then(Value::as_array)
            .map(|a| a.iter().map(|w| str_list(Some(w))).collect())
            .unwrap_or_default(),
        after: str_list(v.get("after")),
        banned: v.get("banned").is_some_and(truthy),
        note: v.get("note").and_then(Value::as_str).map(String::from),
        unmapped: str_list(v.get("unmapped")),
        walks: v
            .get("walks")
            .and_then(Value::as_array)
            .map(|a| {
                a.iter()
                    .map(|w| Walk {
                        moves: str_list(w.get("moves")),
                        missing: w.get("missing").is_some_and(truthy),
                    })
                    .collect()
            })
            .unwrap_or_default(),
        draft: v.get("draft").is_some_and(truthy),
        predicted: v.get("predicted").is_some_and(truthy),
    }
}

/// Python truthiness of a JSON value.
pub fn truthy(v: &Value) -> bool {
    match v {
        Value::Null => false,
        Value::Bool(b) => *b,
        Value::Number(n) => n.as_f64().is_some_and(|x| x != 0.0),
        Value::String(s) => !s.is_empty(),
        Value::Array(a) => !a.is_empty(),
        Value::Object(o) => !o.is_empty(),
    }
}

#[derive(Clone, Debug)]
pub enum Assist {
    None,
    Level(String),
    Map(IndexMap<String, String>),
}

#[derive(Clone, Debug)]
pub struct Rec {
    pub date: String,
    pub problem: Option<String>,
    pub moves: IndexMap<String, String>,
    pub assist: Assist,
    pub followup: Option<String>,
    pub pending: Option<String>,
}

pub const ASSIST_LEVELS: [&str; 4] = ["none", "hint", "walkthrough", "learning"];

pub fn assist_weight(a: &str) -> f64 {
    match a {
        "hint" => 0.5,
        "walkthrough" => 1.0,
        "learning" => 2.0,
        _ => 0.0,
    }
}

impl Rec {
    pub fn parse(v: &Value) -> Rec {
        let assist = match v.get("assist") {
            Some(Value::String(s)) => Assist::Level(s.clone()),
            Some(Value::Object(o)) => {
                Assist::Map(o.iter().map(|(k, v)| (k.clone(), value_str(v))).collect())
            }
            _ => Assist::None,
        };
        Rec {
            date: v
                .get("date")
                .and_then(Value::as_str)
                .unwrap_or("")
                .to_string(),
            problem: v.get("problem").map(value_str),
            moves: v
                .get("moves")
                .and_then(Value::as_object)
                .map(|o| o.iter().map(|(k, v)| (k.clone(), value_str(v))).collect())
                .unwrap_or_default(),
            assist,
            followup: v.get("followup").and_then(Value::as_str).map(String::from),
            pending: v.get("pending").and_then(Value::as_str).map(String::from),
        }
    }

    /// kg_lib.assist_of(rec, node): the level on one move.
    pub fn assist_for(&self, node: &str) -> &str {
        match &self.assist {
            Assist::None => "none",
            Assist::Level(s) => {
                if ASSIST_LEVELS.contains(&s.as_str()) {
                    s
                } else {
                    "none"
                }
            }
            Assist::Map(m) => match m.get(node) {
                Some(v) if ASSIST_LEVELS.contains(&v.as_str()) => v,
                _ => "none",
            },
        }
    }

    /// kg_lib.assist_of(rec): the heaviest level on the solve.
    pub fn assist_any(&self) -> &str {
        match &self.assist {
            Assist::None => "none",
            Assist::Level(s) => {
                if ASSIST_LEVELS.contains(&s.as_str()) {
                    s
                } else {
                    "none"
                }
            }
            Assist::Map(m) => {
                let mut best: Option<&str> = None;
                for v in m.values() {
                    if ASSIST_LEVELS.contains(&v.as_str())
                        && best.is_none_or(|b| assist_weight(v) > assist_weight(b))
                    {
                        best = Some(v);
                    }
                }
                best.unwrap_or("none")
            }
        }
    }

    pub fn problem_str(&self) -> String {
        self.problem.clone().unwrap_or_else(|| "None".to_string())
    }

    pub fn all_clean(&self) -> bool {
        !self.moves.is_empty() && self.moves.values().all(|v| v == "clean")
    }
}

#[derive(Clone, Debug, Default)]
pub struct DrillEntry {
    pub title: String,
    pub after: Vec<String>,
    pub trains: Option<Vec<String>>,
}

pub type DrillMap = IndexMap<String, DrillEntry>;

#[derive(Clone, Debug, Default)]
pub struct Meta {
    pub title: Option<String>,
    pub slug: Option<String>,
    pub difficulty: Option<String>,
    pub paid_only: bool,
    pub acceptance: Option<f64>,
}

pub type Metadata = HashMap<String, Meta>;

#[derive(Clone, Debug)]
pub struct Curve {
    pub a: f64,
    pub b: f64,
    pub c: f64,
    pub d: f64,
    pub e: f64,
    pub conn_mean: f64,
    pub beta: f64,
    pub slip: f64,
    pub conn: HashMap<String, f64>,
    pub target_retention: f64,
    pub raw: Value,
}

pub fn read_json(path: &Path) -> Option<Value> {
    let text = std::fs::read_to_string(path).ok()?;
    serde_json::from_str(&text).ok()
}

pub fn load_nodes(root: &Path) -> Nodes {
    let v = read_json(&root.join("graph/nodes.json")).expect("graph/nodes.json");
    let mut out = Nodes::new();
    for n in v["nodes"].as_array().expect("nodes[]") {
        let id = n["id"].as_str().unwrap_or("").to_string();
        out.insert(
            id.clone(),
            Node {
                id,
                name: n
                    .get("name")
                    .and_then(Value::as_str)
                    .unwrap_or("")
                    .to_string(),
                group: n.get("group").and_then(Value::as_str).map(String::from),
                prereqs: str_list(n.get("prereqs")),
            },
        );
    }
    out
}

/// graph/problems.json, every entry (kg_lib.load_all_problems).
pub fn load_all_problems(root: &Path) -> Problems {
    let v = read_json(&root.join("graph/problems.json")).expect("graph/problems.json");
    let mut out = Problems::new();
    for (k, p) in v["problems"].as_object().expect("problems{}") {
        out.insert(k.clone(), parse_problem(p));
    }
    out
}

/// The evidenced view: entries without the draft flag (kg_lib.load_problems).
pub fn evidenced_view(all: &Problems) -> Problems {
    all.iter()
        .filter(|(_, p)| !p.draft)
        .map(|(k, p)| (k.clone(), p.clone()))
        .collect()
}

/// The drafted walks: entries carrying "walks" (kg_lib.load_predicted).
pub fn predicted_view(all: &Problems) -> Problems {
    all.iter()
        .filter(|(_, p)| !p.walks.is_empty())
        .map(|(k, p)| (k.clone(), p.clone()))
        .collect()
}

pub fn load_evidence_recs(root: &Path) -> Vec<(String, Rec)> {
    let v = read_json(&root.join("graph/evidence.json")).expect("graph/evidence.json");
    v["evidence"]
        .as_object()
        .expect("evidence{}")
        .iter()
        .map(|(k, r)| (k.clone(), Rec::parse(r)))
        .collect()
}

pub fn load_drills(root: &Path) -> DrillMap {
    let mut out = DrillMap::new();
    let Some(v) = read_json(&root.join("graph/drills.json")) else {
        return out;
    };
    for (k, d) in v["drills"].as_object().into_iter().flatten() {
        out.insert(
            k.clone(),
            DrillEntry {
                title: d
                    .get("title")
                    .and_then(Value::as_str)
                    .unwrap_or("")
                    .to_string(),
                after: str_list(d.get("after")),
                trains: d.get("trains").map(|t| str_list(Some(t))),
            },
        );
    }
    out
}

pub fn load_metadata(root: &Path) -> Metadata {
    let mut out = Metadata::new();
    let Some(v) = read_json(&root.join("data/problems_metadata.json")) else {
        return out;
    };
    for (k, m) in v.as_object().into_iter().flatten() {
        out.insert(
            k.clone(),
            Meta {
                title: m.get("title").and_then(Value::as_str).map(String::from),
                slug: m.get("slug").and_then(Value::as_str).map(String::from),
                difficulty: m
                    .get("difficulty")
                    .and_then(Value::as_str)
                    .map(String::from),
                paid_only: m.get("paid_only").is_some_and(truthy),
                acceptance: m.get("acceptance").and_then(Value::as_f64),
            },
        );
    }
    out
}

pub fn load_curve(root: &Path) -> Option<Curve> {
    let v = read_json(&root.join("graph/curve.json"))?;
    if !truthy(&v) {
        return None;
    }
    let p = v.get("params")?;
    let f = |k: &str| p.get(k).and_then(Value::as_f64);
    let conn = v
        .get("conn")
        .and_then(Value::as_object)
        .map(|o| {
            o.iter()
                .filter_map(|(k, x)| x.as_f64().map(|x| (k.clone(), x)))
                .collect()
        })
        .unwrap_or_default();
    Some(Curve {
        a: f("a")?,
        b: f("b")?,
        c: f("c")?,
        d: f("d").unwrap_or(0.0),
        e: f("e").unwrap_or(0.0),
        conn_mean: f("conn_mean").unwrap_or(0.0),
        beta: f("beta")?,
        slip: f("slip").unwrap_or(0.0),
        conn,
        target_retention: v.get("target_retention")?.as_f64()?,
        raw: v.clone(),
    })
}

/// kg_lib.pnum_key: numeric sort that tolerates ids like '2167B'.
pub fn pnum_key(pnum: &str) -> (i64, String) {
    let digits: String = pnum.chars().filter(|c| c.is_ascii_digit()).collect();
    (digits.parse().unwrap_or(0), pnum.to_string())
}

pub fn is_numeric_id(s: &str) -> bool {
    s.chars().next().is_some_and(|c| c.is_ascii_digit())
}
