// kg_draft - draft predicted walks for cached problems with an LLM.
//
//   kg_draft --pilot 50                 # label N evidenced problems, score vs truth
//   kg_draft --full                     # label every cached solution -> graph/problems.json
//
// Closed-vocabulary labeling: the model picks move ids from nodes.json, it
// never invents walk vocabulary. Few-shot examples come from evidenced walks
// in problems.json, always excluding the problem being labeled. Responses are
// cached per problem+model in .walk_cache/ so reruns are free.
//
// Predicted walks are a separate tier from evidence (see PLAN.md phase 2);
// --pilot writes nothing to problems.json, --full appends predicted walks.
//
// Ported from utils/kg/kg_draft (Python) on 2026-09-14.

use std::collections::{BTreeMap, HashMap, HashSet, VecDeque};
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};

use kg::data::repo_root;
use kg::mock::PyRandom;
use kg::pyjson;
use regex::Regex;
use serde_json::{json, Map, Value};

const PROMPT_VERSION: i64 = 3;

const SYSTEM_PROMPT: &str =
    "You label LeetCode solutions with the techniques they use, chosen from \
a fixed move list. Output ONLY the move ids, comma-separated, on one \
line. If the solution needs a technique that is not in the list, add \
extra lines of the form 'missing: short-kebab-name'. No other text.";

const USAGE: &str = "usage: kg_draft [-h] [--pilot PILOT] [--full] [--limit LIMIT] [--model MODEL]
                [--examples EXAMPLES] [--jobs JOBS] [--seed SEED]

options:
  -h, --help           show this help message and exit
  --pilot PILOT        Label N random evidenced problems and score vs truth.
  --full               Label every cached solution, write graph/problems.json.
  --limit LIMIT        With --full: stop after N problems.
  --model MODEL
  --examples EXAMPLES  Few-shot examples per prompt.
  --jobs JOBS
  --seed SEED";

struct Paths {
    graph: PathBuf,
    prepare_cache: PathBuf,
    solved: PathBuf,
    walk_cache: PathBuf,
}

impl Paths {
    fn new(root: &Path) -> Paths {
        Paths {
            graph: root.join("graph"),
            prepare_cache: root.join(".prepare_cache"),
            solved: root.join("solved"),
            walk_cache: root.join(".walk_cache"),
        }
    }
}

/// One move of the closed vocabulary, in nodes.json order.
struct Node {
    id: String,
    desc: String,
    hint: String,
}

/// An evidenced walk: the few-shot material.
struct Walk {
    title: String,
    moves: Vec<String>,
}

/// One labeled problem: the parsed reply and the reply itself.
#[derive(Clone)]
struct Entry {
    moves: Vec<String>,
    missing: Vec<String>,
    junk: Vec<String>,
    reply: String,
}

fn str_list(v: Option<&Value>) -> Vec<String> {
    v.and_then(Value::as_array)
        .map(|a| {
            a.iter()
                .filter_map(|x| x.as_str().map(String::from))
                .collect()
        })
        .unwrap_or_default()
}

fn load_nodes(p: &Paths) -> Vec<Node> {
    let doc = pyjson::load(&p.graph.join("nodes.json")).unwrap_or_else(|| {
        die("graph/nodes.json: unreadable");
    });
    doc["nodes"]
        .as_array()
        .map(|a| {
            a.iter()
                .map(|n| Node {
                    id: n["id"].as_str().unwrap_or("").to_string(),
                    desc: n["desc"].as_str().unwrap_or("").to_string(),
                    hint: n["hint"].as_str().unwrap_or("").to_string(),
                })
                .collect()
        })
        .unwrap_or_default()
}

/// The evidenced walks, for the few-shot examples: a drafted entry has no
/// "moves" of its own, only the walks this program writes. Keys in file
/// order, as the Python dict kept them.
fn load_walks(p: &Paths) -> Vec<(String, Walk)> {
    let doc = pyjson::load(&p.graph.join("problems.json")).unwrap_or_else(|| {
        die("graph/problems.json: unreadable");
    });
    let mut out = Vec::new();
    if let Some(probs) = doc["problems"].as_object() {
        for (k, v) in probs {
            if !k.is_empty() && k.bytes().all(|b| b.is_ascii_digit()) {
                let moves = str_list(v.get("moves"));
                if !moves.is_empty() {
                    let title = v["title"].as_str().unwrap_or("").to_string();
                    out.push((k.clone(), Walk { title, moves }));
                }
            }
        }
    }
    out
}

/// The solved/ listing, read once: load_solution asks it for every
/// example candidate.
struct Solutions {
    solved_files: Vec<String>,
    prepare_cache: PathBuf,
    solved: PathBuf,
}

impl Solutions {
    fn new(p: &Paths) -> Solutions {
        let mut solved_files: Vec<String> = std::fs::read_dir(&p.solved)
            .map(|rd| {
                rd.filter_map(|e| e.ok())
                    .map(|e| e.file_name().to_string_lossy().into_owned())
                    .collect()
            })
            .unwrap_or_default();
        solved_files.sort();
        Solutions {
            solved_files,
            prepare_cache: p.prepare_cache.clone(),
            solved: p.solved.clone(),
        }
    }

    /// The validated cache entry's (solution, title), None when there is
    /// no entry or it does not parse.
    fn cache_entry(&self, num: &str) -> (Option<String>, Option<String>) {
        let Some(entry) = pyjson::load(&self.prepare_cache.join(format!("{num}.json"))) else {
            return (None, None);
        };
        let s = |k: &str| entry.get(k).and_then(Value::as_str).map(String::from);
        (s("solution"), s("title"))
    }

    /// The operator's own latest solve if there is one (that is the code the
    /// evidenced walk describes), else the validated cache solution.
    fn load_solution(&self, num: &str) -> Option<String> {
        let re = Regex::new(&format!(r"^p{}_.*\.py$", regex::escape(num))).unwrap();
        let own = self.solved_files.iter().rfind(|f| re.is_match(f));
        if let Some(f) = own {
            return std::fs::read_to_string(self.solved.join(f)).ok();
        }
        self.cache_entry(num).0
    }
}

fn build_prompt(
    nodes: &[Node],
    walks: &HashMap<String, Walk>,
    sols: &Solutions,
    solution: &str,
    examples: &[String],
) -> String {
    let mut lines = vec!["MOVE LIST (pick only from these ids):".to_string()];
    for n in nodes {
        let hint = if n.hint.is_empty() {
            String::new()
        } else {
            format!(" {}", n.hint)
        };
        lines.push(format!("- {}: {}{}", n.id, n.desc, hint));
    }
    lines.push(String::new());
    lines.push("Examples of solutions and their move labels:".to_string());
    for ex_num in examples {
        let ex_sol = sols.load_solution(ex_num).unwrap_or_default();
        let w = &walks[ex_num];
        lines.push(format!("\n### {}. {}", ex_num, w.title));
        lines.push(ex_sol.trim().to_string());
        lines.push(format!("MOVES: {}", w.moves.join(", ")));
    }
    lines.push("\n### Now label this one:".to_string());
    lines.push(solution.trim().to_string());
    lines.push("MOVES:".to_string());
    lines.join("\n")
}

/// (moves, missing, junk): known ids, `missing:` suggestions, and anything
/// claimed as a move that is not in the taxonomy.
fn parse_reply(reply: &str, ids: &HashSet<&str>) -> (Vec<String>, Vec<String>, Vec<String>) {
    let missing_re = Regex::new(r"(?i)^missing:\s*(.+)").unwrap();
    let moves_re = Regex::new(r"(?i)^moves:\s*").unwrap();
    let (mut moves, mut missing, mut junk) = (Vec::new(), Vec::new(), Vec::new());
    for line in reply.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if let Some(m) = missing_re.captures(line) {
            missing.push(m[1].trim().to_string());
            continue;
        }
        let line = moves_re.replace(line, "");
        for tok in line.split(',') {
            let tok = tok.trim().trim_matches(|c| c == '`' || c == '.');
            if tok.is_empty() {
                continue;
            }
            if ids.contains(tok) {
                if !moves.iter().any(|m| m == tok) {
                    moves.push(tok.to_string());
                }
            } else {
                junk.push(tok.to_string());
            }
        }
    }
    (moves, missing, junk)
}

fn entry_json(e: &Entry) -> Value {
    json!({
        "moves": e.moves,
        "missing": e.missing,
        "junk": e.junk,
        "reply": e.reply,
    })
}

struct Drafter {
    nodes: Vec<Node>,
    ids: HashSet<String>,
    walks: HashMap<String, Walk>,
    sols: Solutions,
    walk_cache: PathBuf,
    model: String,
}

impl Drafter {
    fn id_set(&self) -> HashSet<&str> {
        self.ids.iter().map(String::as_str).collect()
    }

    /// The cached reply for this problem+model, re-parsed against today's
    /// taxonomy; else one LLM call, cached before it is returned.
    fn draft(
        &self,
        num: &str,
        solution: &str,
        examples: &[String],
        source: &str,
    ) -> Result<Entry, String> {
        std::fs::create_dir_all(&self.walk_cache).map_err(|e| e.to_string())?;
        let cache = self.walk_cache.join(format!(
            "{num}.{source}.{}.v{PROMPT_VERSION}.json",
            self.model
        ));
        let ids = self.id_set();
        if cache.exists() {
            let entry =
                pyjson::load(&cache).ok_or_else(|| format!("{}: unreadable", cache.display()))?;
            let reply = entry["reply"].as_str().unwrap_or("").to_string();
            let (moves, missing, junk) = parse_reply(&reply, &ids);
            return Ok(Entry {
                moves,
                missing,
                junk,
                reply,
            });
        }
        let prompt = build_prompt(&self.nodes, &self.walks, &self.sols, solution, examples);
        let reply =
            kg::llm::text(&prompt, SYSTEM_PROMPT, Some(&self.model)).map_err(|e| e.to_string())?;
        let (moves, missing, junk) = parse_reply(&reply, &ids);
        let entry = Entry {
            moves,
            missing,
            junk,
            reply,
        };
        pyjson::save(&cache, &entry_json(&entry), None).map_err(|e| e.to_string())?;
        Ok(entry)
    }

    /// k evidenced problems other than `exclude` that have a solution on
    /// disk, drawn with CPython's sample so the cache keys line up.
    fn pick_examples(&self, exclude: &str, k: usize, rng: &mut PyRandom) -> Vec<String> {
        let mut pool: Vec<String> = self
            .walks
            .keys()
            .filter(|n| n.as_str() != exclude && self.sols.load_solution(n).is_some())
            .cloned()
            .collect();
        pool.sort();
        rng.sample(&pool, k)
    }
}

/// graph/problems.json: "walks" is a LIST per problem, each walk stamped
/// with tier and source. Alt walks accumulate; nothing here is evidence, so
/// a problem the operator has never solved keeps its "draft": true until
/// kg_extract maps it from a real solve.
fn save_predicted(
    p: &Paths,
    drafts: &BTreeMap<i64, (String, String, Entry)>,
    model: &str,
) -> PathBuf {
    let path = p.graph.join("problems.json");
    let mut doc = pyjson::load(&path).unwrap_or_else(|| die("graph/problems.json: unreadable"));
    let probs = doc["problems"]
        .as_object_mut()
        .unwrap_or_else(|| die("problems.json: no problems"));
    for (num, title, entry) in drafts.values() {
        let prob = probs
            .entry(num.clone())
            .or_insert_with(|| json!({"title": title, "draft": true, "walks": []}));
        let prob = prob
            .as_object_mut()
            .unwrap_or_else(|| die(&format!("problems.json: {num} is not an object")));
        let walks = prob.entry("walks").or_insert_with(|| json!([]));
        if !walks.is_array() {
            *walks = json!([]);
        }
        let mut walk = Map::new();
        walk.insert("moves".into(), json!(entry.moves));
        walk.insert("tier".into(), json!("predicted"));
        walk.insert("source".into(), json!("cache-solution"));
        walk.insert("model".into(), json!(model));
        walk.insert("prompt_version".into(), json!(PROMPT_VERSION));
        if !entry.missing.is_empty() {
            walk.insert("missing".into(), json!(entry.missing));
        }
        let arr = walks.as_array_mut().unwrap();
        if !arr.iter().any(|w| w.get("moves") == Some(&walk["moves"])) {
            arr.push(Value::Object(walk));
        }
    }
    if let Err(e) = pyjson::save(&path, &doc, Some(1)) {
        die(&format!("{}: {e}", path.display()));
    }
    path
}

/// A shared queue of problem numbers, drained by `jobs` threads.
fn run_workers<F>(nums: &[String], jobs: usize, work: F)
where
    F: Fn(&str) + Sync,
{
    let q: Arc<Mutex<VecDeque<String>>> = Arc::new(Mutex::new(nums.iter().cloned().collect()));
    std::thread::scope(|s| {
        for _ in 0..jobs {
            let q = Arc::clone(&q);
            let work = &work;
            s.spawn(move || loop {
                let next = q.lock().unwrap().pop_front();
                let Some(num) = next else { return };
                work(&num);
            });
        }
    });
}

fn full(args: &Args, p: &Paths, d: &Drafter) {
    let mut nums: Vec<(i64, String)> = std::fs::read_dir(&p.prepare_cache)
        .map(|rd| {
            rd.filter_map(|e| e.ok())
                .map(|e| e.file_name().to_string_lossy().into_owned())
                .filter(|f| f.ends_with(".json"))
                .map(|f| f.split('.').next().unwrap_or("").to_string())
                .filter_map(|n| n.parse::<i64>().ok().map(|k| (k, n)))
                .collect()
        })
        .unwrap_or_default();
    nums.sort_by_key(|(k, _)| *k);
    let mut nums: Vec<String> = nums.into_iter().map(|(_, n)| n).collect();
    if let Some(limit) = args.limit {
        nums.truncate(limit);
    }
    let total = nums.len();
    let drafts: Mutex<BTreeMap<i64, (String, String, Entry)>> = Mutex::new(BTreeMap::new());
    let errors: Mutex<Vec<(String, String)>> = Mutex::new(Vec::new());
    run_workers(&nums, args.jobs, |num| {
        let (sol, title) = d.sols.cache_entry(num);
        let Some(sol) = sol.filter(|s| !s.is_empty()) else {
            return;
        };
        let mut rng = PyRandom::new((args.seed + num.parse::<i64>().unwrap_or(0)) as u32);
        let ex = d.pick_examples(num, args.examples, &mut rng);
        match d.draft(num, &sol, &ex, "cache") {
            Ok(entry) => {
                let mut drafts = drafts.lock().unwrap();
                drafts.insert(
                    num.parse().unwrap_or(0),
                    (num.to_string(), title.unwrap_or_default(), entry),
                );
                if drafts.len().is_multiple_of(50) {
                    eprintln!("{}/{}", drafts.len(), total);
                }
            }
            Err(e) => errors.lock().unwrap().push((num.to_string(), e)),
        }
    });
    let drafts = drafts.into_inner().unwrap();
    let errors = errors.into_inner().unwrap();
    let path = save_predicted(p, &drafts, &args.model);
    println!(
        "drafted {} problems -> {}   errors: {}",
        drafts.len(),
        path.display(),
        errors.len()
    );
    for (num, e) in errors.iter().take(10) {
        println!("  {num}: {e}");
    }
}

/// Python's repr of a str: single quotes unless the text has one and no
/// double quote; backslash, the quote, and the control characters escaped.
fn py_repr(s: &str) -> String {
    let q = if s.contains('\'') && !s.contains('"') {
        '"'
    } else {
        '\''
    };
    let mut out = String::new();
    out.push(q);
    for c in s.chars() {
        match c {
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if c == q => {
                out.push('\\');
                out.push(c);
            }
            c if (c as u32) < 0x20 || c as u32 == 0x7f => {
                out.push_str(&format!("\\x{:02x}", c as u32));
            }
            c => out.push(c),
        }
    }
    out.push(q);
    out
}

fn py_list(items: &[String]) -> String {
    format!(
        "[{}]",
        items
            .iter()
            .map(|s| py_repr(s))
            .collect::<Vec<_>>()
            .join(", ")
    )
}

fn pilot(args: &Args, d: &Drafter, n_pilot: usize) {
    let mut rng = PyRandom::new(args.seed as u32);
    let mut evidenced: Vec<String> = d
        .walks
        .keys()
        .filter(|n| d.sols.load_solution(n).is_some())
        .cloned()
        .collect();
    evidenced.sort();
    if n_pilot > evidenced.len() {
        die("Sample larger than population or is negative");
    }
    let targets = rng.sample(&evidenced, n_pilot);

    let results: Mutex<HashMap<String, Result<Entry, String>>> = Mutex::new(HashMap::new());
    run_workers(&targets, args.jobs.min(targets.len()), |num| {
        let mut rng = PyRandom::new((args.seed + num.parse::<i64>().unwrap_or(0)) as u32);
        let ex = d.pick_examples(num, args.examples, &mut rng);
        let sol = d.sols.load_solution(num).unwrap_or_default();
        let r = d.draft(num, &sol, &ex, "own");
        results.lock().unwrap().insert(num.to_string(), r);
    });
    let results = results.into_inner().unwrap();

    let (mut tp, mut fp, mut fn_, mut exact) = (0usize, 0usize, 0usize, 0usize);
    println!(
        "model={} examples={} seed={}\n",
        args.model, args.examples, args.seed
    );
    for num in &targets {
        let Some(r) = results.get(num) else { continue };
        let entry = match r {
            Err(e) => {
                println!("{num:>5} ERROR {e}");
                continue;
            }
            Ok(entry) => entry,
        };
        let truth: HashSet<&str> = d.walks[num].moves.iter().map(String::as_str).collect();
        let pred: HashSet<&str> = entry.moves.iter().map(String::as_str).collect();
        let sorted = |it: HashSet<&&str>| {
            let mut v: Vec<String> = it.into_iter().map(|s| s.to_string()).collect();
            v.sort();
            v
        };
        let hit = sorted(truth.intersection(&pred).collect());
        let extra = sorted(pred.difference(&truth).collect());
        let miss = sorted(truth.difference(&pred).collect());
        tp += hit.len();
        fp += extra.len();
        fn_ += miss.len();
        let same = truth == pred;
        exact += usize::from(same);
        let flag = if same { '=' } else { ' ' };
        let title: String = d.walks[num].title.chars().take(34).collect();
        let mut line = format!(
            "{num:>5} {flag} {title:<34} hit {}  extra {}  miss {}",
            py_list(&hit),
            py_list(&extra),
            py_list(&miss)
        );
        if !entry.missing.is_empty() {
            line.push_str(&format!("  missing? {}", py_list(&entry.missing)));
        }
        if !entry.junk.is_empty() {
            line.push_str(&format!("  junk {}", py_list(&entry.junk)));
        }
        println!("{line}");
    }
    let n = results.values().filter(|r| r.is_ok()).count();
    if tp + fp > 0 && tp + fn_ > 0 {
        println!(
            "\nexact {exact}/{n}   precision {:.2}   recall {:.2}",
            tp as f64 / (tp + fp) as f64,
            tp as f64 / (tp + fn_) as f64
        );
    }
}

struct Args {
    pilot: Option<usize>,
    full: bool,
    limit: Option<usize>,
    model: String,
    examples: usize,
    jobs: usize,
    seed: i64,
}

fn parse_args() -> Args {
    let mut a = Args {
        pilot: None,
        full: false,
        limit: None,
        model: "gpt-5-mini".to_string(),
        examples: 6,
        jobs: 4,
        seed: 1,
    };
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let mut i = 0;
    let value = |i: &mut usize, name: &str| -> String {
        *i += 1;
        argv.get(*i)
            .cloned()
            .unwrap_or_else(|| die(&format!("{name} needs a value")))
    };
    while i < argv.len() {
        let arg = argv[i].as_str();
        match arg {
            "--pilot" => a.pilot = Some(num(&value(&mut i, arg), arg)),
            "--full" => a.full = true,
            "--limit" => a.limit = Some(num(&value(&mut i, arg), arg)),
            "--model" => a.model = value(&mut i, arg),
            "--examples" => a.examples = num(&value(&mut i, arg), arg),
            "--jobs" => a.jobs = num(&value(&mut i, arg), arg),
            "--seed" => a.seed = num(&value(&mut i, arg), arg),
            "-h" | "--help" => {
                println!("{USAGE}");
                std::process::exit(0);
            }
            _ => die(&format!("unknown argument {arg}\n{USAGE}")),
        }
        i += 1;
    }
    a
}

fn num<T: std::str::FromStr>(s: &str, name: &str) -> T {
    s.parse()
        .unwrap_or_else(|_| die(&format!("{name}: not a number: {s}")))
}

fn die(msg: &str) -> ! {
    eprintln!("{msg}");
    std::process::exit(2)
}

fn main() {
    let args = parse_args();
    if !args.full && args.pilot.is_none() {
        println!("{USAGE}");
        return;
    }
    let p = Paths::new(&repo_root());
    let nodes = load_nodes(&p);
    let ids: HashSet<String> = nodes.iter().map(|n| n.id.clone()).collect();
    let walks: HashMap<String, Walk> = load_walks(&p).into_iter().collect();
    let d = Drafter {
        nodes,
        ids,
        walks,
        sols: Solutions::new(&p),
        walk_cache: p.walk_cache.clone(),
        model: args.model.clone(),
    };
    if args.full {
        full(&args, &p, &d);
    } else if let Some(n) = args.pilot {
        pilot(&args, &d, n);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn ids() -> HashSet<&'static str> {
        ["two-pointers", "prefix-sum", "dp-1d"]
            .into_iter()
            .collect()
    }

    #[test]
    fn parse_reply_splits_moves_missing_and_junk() {
        let reply = "MOVES: two-pointers, `prefix-sum`, two-pointers, sliding.\nmissing: bit-trick\n\nMissing:  other-thing\n";
        let (moves, missing, junk) = parse_reply(reply, &ids());
        assert_eq!(moves, ["two-pointers", "prefix-sum"]);
        assert_eq!(missing, ["bit-trick", "other-thing"]);
        assert_eq!(junk, ["sliding"]);
    }

    #[test]
    fn py_repr_picks_the_quote_like_python() {
        assert_eq!(py_repr("plain"), "'plain'");
        assert_eq!(py_repr("it's"), "\"it's\"");
        assert_eq!(py_repr("a'b\"c"), "'a\\'b\"c'");
        assert_eq!(py_list(&["a".into(), "b".into()]), "['a', 'b']");
        assert_eq!(py_list(&[]), "[]");
    }
}
