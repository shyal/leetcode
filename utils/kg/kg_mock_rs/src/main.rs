// kg_mock — the Monte-Carlo pass-rate model behind `make mock`: today's cold
// mock estimate plus the forward practice simulation.
//
// Ported from (and replacing) the retired Python utils/kg_mock. The core model
// math (pass_rates / current_recall) is shared with utils/kg/kg_lib.py, which the
// README's P(pass) history chart uses — change the two together. PyRandom
// reproduces CPython's random.Random exactly so results stay comparable with
// the Python era. utils/tests/test_mock.py guards output shape and speed.

use std::collections::HashMap;
use std::io::IsTerminal;
use std::path::PathBuf;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};

use chrono::{Datelike, Duration, NaiveDate};
use serde_json::Value;

use kg_mock::*;

fn measured_first_contact(evidence: &[EvRec]) -> f64 {
    let mut order: Vec<usize> = (0..evidence.len()).collect();
    order.sort_by(|&x, &y| evidence[x].fname.cmp(&evidence[y].fname));
    let mut first: HashMap<&str, ((&str, String), &str)> = HashMap::new();
    for &i in &order {
        let rec = &evidence[i];
        let key = (rec.date.as_str(), ts_match(&rec.fname));
        for (node, v) in &rec.moves {
            match first.get(node.as_str()) {
                Some((k0, _)) if !(key < *k0) => {}
                _ => {
                    first.insert(node.as_str(), (key.clone(), v.as_str()));
                }
            }
        }
    }
    if first.is_empty() {
        return 0.7;
    }
    let clean = first.values().filter(|(_, v)| *v == "clean").count();
    clean as f64 / first.len() as f64
}

// Every `solve time: Xm Ys` trailer in the git log, as (commit date, minutes).
// Parsed once so pace can be asked for any as-of date without re-running git.
fn solve_log(repo_root: &PathBuf) -> Vec<(NaiveDate, f64)> {
    let Ok(out) = std::process::Command::new("git")
        .args(["log", "--format=%ad|%B~~~", "--date=short"])
        .current_dir(repo_root)
        .output()
    else {
        return Vec::new();
    };
    let log = String::from_utf8_lossy(&out.stdout).into_owned();
    let mut entries = Vec::new();
    for block in log.split("~~~") {
        let block = block.trim();
        let Some(head) = block.get(..10) else { continue };
        let Ok(when) = NaiveDate::parse_from_str(head, "%Y-%m-%d") else { continue };
        let mut rest = block;
        while let Some(pos) = rest.find("solve time: ") {
            rest = &rest[pos + 12..];
            if let Some((m, s, consumed)) = parse_solve_trailer(rest) {
                entries.push((when, m as f64 + s as f64 / 60.0));
                rest = &rest[consumed..];
            }
        }
    }
    entries
}

// Current-streak pace: average hours/day since the current practice streak
// began (a streak is broken by 7+ consecutive zero days), with the averaging
// window clamped to [7, 28] days ending at `today`. Rounded to 0.1h; None
// when the window has no timed solves. The forward sim extrapolates this
// number forever and the projected dates are ~(work left)/hours, so the old
// 7-day average let one heavy day entering or leaving the window whiplash the
// projections by months — while a flat 28-day average made a fresh streak
// drag a dead month behind it. Streak-aware clamping avoids both.
fn week_pace(log: &[(NaiveDate, f64)], today: NaiveDate) -> Option<f64> {
    let mut mins = [0.0f64; 28]; // mins[i] = minutes solved on `today - i`
    for (when, m) in log {
        let i = (today - *when).num_days();
        if (0..28).contains(&i) {
            mins[i as usize] += m;
        }
    }
    // walk back until a full dead week; the streak is the days before it
    let mut window = 28usize;
    let mut run = 0usize;
    for (i, &m) in mins.iter().enumerate() {
        if m == 0.0 {
            run += 1;
            if run == 7 {
                window = i + 1 - run;
                break;
            }
        } else {
            run = 0;
        }
    }
    // the floor only ever adds days inside the dead week, which are zero
    let window = window.max(7);
    let minutes: f64 = mins[..window].iter().sum();
    let h: f64 = format!("{:.1}", minutes / window as f64 / 60.0).parse().unwrap();
    if h == 0.0 {
        None
    } else {
        Some(h)
    }
}

// Parses the r"(\d+)m (\d+)s" tail of a solve-time trailer.
fn parse_solve_trailer(s: &str) -> Option<(u64, u64, usize)> {
    let b = s.as_bytes();
    let mut i = 0;
    while i < b.len() && b[i].is_ascii_digit() {
        i += 1;
    }
    if i == 0 || i + 1 >= b.len() || b[i] != b'm' || b[i + 1] != b' ' {
        return None;
    }
    let m: u64 = s[..i].parse().ok()?;
    let mut j = i + 2;
    while j < b.len() && b[j].is_ascii_digit() {
        j += 1;
    }
    if j == i + 2 || j >= b.len() || b[j] != b's' {
        return None;
    }
    let sec: u64 = s[i + 2..j].parse().ok()?;
    Some((m, sec, j + 1))
}

// ------------------------------------------------------------- pass_rates --

const HARDS_START: i64 = 45;
const MOCKS_START: i64 = 90;
const MOCKS_PER_WEEK: f64 = 2.0;
const HARDS_PER_WEEK: f64 = 3.0;
const N_MC: usize = 20000;

// mv_recall: per move of the bank universe the recall, or None -> derive.

// Every pass_rates call is independent (fresh seeded RNG), so the whole
// Monte-Carlo load fans out over a thread pool; results land by task index.
struct Task {
    mv_recall: Arc<Vec<Option<f64>>>,
    bank: Arc<Bank>,
    r: f64,
    practice: (i64, i64, i64),
    n_mc: usize,
}

fn run_all(tasks: &[Task]) -> Vec<(f64, f64, f64, f64)> {
    let n = tasks.len();
    let cursor = AtomicUsize::new(0);
    let results = Mutex::new(vec![(0.0, 0.0, 0.0, 0.0); n]);
    let workers = std::thread::available_parallelism()
        .map(|c| c.get())
        .unwrap_or(4)
        .min(n.max(1));
    std::thread::scope(|s| {
        for _ in 0..workers {
            s.spawn(|| loop {
                let i = cursor.fetch_add(1, Ordering::Relaxed);
                if i >= n {
                    break;
                }
                let t = &tasks[i];
                let r = pass_rates(
                    &t.mv_recall,
                    &t.bank.pools,
                    t.r,
                    t.practice,
                    &mut PyRandom::new(42),
                    t.n_mc,
                );
                results.lock().unwrap()[i] = r;
            });
        }
    });
    results.into_inner().unwrap()
}

// One monthly snapshot of the forward simulation; its pass_rates tasks sit at
// tasks[task_start..task_start + scenarios.len()], in SCENARIOS order.
struct Snap {
    day: i64,
    practice: (i64, i64, i64),
    n_nodes: usize,
    offh: f64,
    task_start: usize,
}

// The forward practice simulation as a steppable state machine, so a
// pass-rate check can be taken at ANY simulated day: the monthly scan and the
// milestone bisection both drive it.
//
// The taxonomy's growth is no longer an abstract unknown-idea pool: the bank
// knows exactly which extra moves the drafted walks want and which problems
// each one blocks. Learning absorbs them in mention-rank order (the order
// drilling would prioritize); each learned extra becomes a real node in the
// spaced-repetition loop and unblocks its specific problems.
struct SimState<'a> {
    cv: &'a Curve,
    teach: f64,
    hours: f64,
    hards_per_week: f64,
    bank: Arc<Bank>,
    reps: Vec<i64>,
    gaps: Vec<i64>,
    learned: Vec<Option<usize>>, // extra id -> reps/gaps index once learned
    walk_unlearned: Vec<u32>,    // per walk gid: extras still unlearned
    clean_walks: [Vec<u32>; 3],  // per (dif, prob): walks with 0 unlearned
    blocked: [usize; 3],         // per dif: problems with no clean walk
    learn_ptr: usize,
    learn_credit: f64,
    mediums_done: i64,
    mocks_done: i64,
    hards_done: i64,
    day: i64,
}

impl<'a> SimState<'a> {
    fn new(
        hours: f64,
        teach: f64,
        reps: Vec<i64>,
        gaps: Vec<i64>,
        cv: &'a Curve,
        bank: Arc<Bank>,
    ) -> Self {
        let walk_unlearned: Vec<u32> =
            bank.walk_extras.iter().map(|e| e.len() as u32).collect();
        let mut clean_walks: [Vec<u32>; 3] =
            [0, 1, 2].map(|d| vec![0u32; bank.pools[d].len()]);
        for (gid, &(dif, pi)) in bank.walk_prob.iter().enumerate() {
            if walk_unlearned[gid] == 0 {
                clean_walks[dif][pi] += 1;
            }
        }
        let blocked =
            [0, 1, 2].map(|d| clean_walks[d].iter().filter(|&&c| c == 0).count());
        SimState {
            cv,
            teach,
            hours,
            hards_per_week: (HARDS_PER_WEEK * hours / 2.0).min(6.0),
            learned: vec![None; bank.n_extras()],
            walk_unlearned,
            clean_walks,
            blocked,
            bank,
            reps,
            gaps,
            learn_ptr: 0,
            learn_credit: 0.0,
            mediums_done: 0,
            mocks_done: 0,
            hards_done: 0,
            day: 0,
        }
    }

    // share of difficulty-dif problems whose every walk still needs an
    // unlearned extra move — the measured replacement for the old off dial
    fn off_now(&self, dif: usize) -> f64 {
        self.blocked[dif] as f64 / self.bank.pools[dif].len().max(1) as f64
    }

    fn learn_ideas(&mut self, dif: usize, encounters: i64) {
        self.learn_credit += self.teach * self.off_now(dif) * encounters as f64;
        while self.learn_credit >= 1.0 && self.learn_ptr < self.bank.n_extras() {
            self.learn_credit -= 1.0;
            let e = self.learn_ptr;
            self.learn_ptr += 1;
            self.learned[e] = Some(self.reps.len());
            self.reps.push(1);
            self.gaps.push(0);
            for gi in 0..self.bank.extra_walks[e].len() {
                let gid = self.bank.extra_walks[e][gi];
                self.walk_unlearned[gid] -= 1;
                if self.walk_unlearned[gid] == 0 {
                    let (d, pi) = self.bank.walk_prob[gid];
                    self.clean_walks[d][pi] += 1;
                    if self.clean_walks[d][pi] == 1 {
                        self.blocked[d] -= 1;
                    }
                }
            }
        }
    }

    // one simulated day of practice
    fn step(&mut self) {
        self.day += 1;
        let mut budget = self.hours * 60.0;
        for g in self.gaps.iter_mut() {
            *g += 1;
        }
        let mut order: Vec<usize> = (0..self.gaps.len()).collect();
        order.sort_by(|&x, &y| self.gaps[y].cmp(&self.gaps[x]));
        for &n in &order {
            let s = (self.cv.a + self.cv.b * self.reps[n] as f64)
                .exp()
                .max(7.0)
                .min(3650.0);
            if (1.0 + self.gaps[n] as f64 / s).powf(-self.cv.beta) < self.cv.target
                && budget >= 10.0
            {
                budget -= 10.0;
                self.gaps[n] = 0;
                self.reps[n] += 1;
            }
        }
        while budget >= 23.0 {
            if self.day > HARDS_START
                && (self.hards_done as f64)
                    < (self.day - HARDS_START) as f64 / 7.0 * self.hards_per_week
            {
                budget -= 40.0;
                self.hards_done += 1;
                self.learn_ideas(2, 1);
            } else if self.day > MOCKS_START
                && (self.mocks_done as f64)
                    < (self.day - MOCKS_START) as f64 / 7.0 * MOCKS_PER_WEEK
            {
                budget -= 90.0;
                self.mocks_done += 1;
            } else {
                budget -= 23.0;
                self.mediums_done += 1;
                self.learn_ideas(1, 1);
            }
            let mut ord2: Vec<usize> = (0..self.gaps.len()).collect();
            ord2.sort_by_key(|&n| (self.reps[n], -self.gaps[n]));
            for &n in ord2.iter().take(3) {
                self.gaps[n] = 0;
                self.reps[n] += 1;
            }
        }
    }

    fn practice(&self) -> (i64, i64, i64) {
        (self.mediums_done, self.mocks_done, self.hards_done)
    }

    fn mv_recall(&self) -> Vec<Option<f64>> {
        let rec_now: Vec<f64> = (0..self.gaps.len())
            .map(|n| {
                let s = (self.cv.a + self.cv.b * self.reps[n] as f64)
                    .exp()
                    .max(7.0)
                    .min(3650.0);
                (1.0 + self.gaps[n] as f64 / s).powf(-self.cv.beta)
            })
            .collect();
        (0..self.bank.move_names.len())
            .map(|i| {
                if i < self.bank.n_known {
                    Some(rec_now[i])
                } else {
                    self.learned[i - self.bank.n_known].map(|j| rec_now[j])
                }
            })
            .collect()
    }

    fn task(&self, r: f64, n_mc: usize) -> Task {
        Task {
            mv_recall: Arc::new(self.mv_recall()),
            bank: self.bank.clone(),
            r,
            practice: self.practice(),
            n_mc,
        }
    }

    // pass_rates at the current simulated day — bit-identical to running the
    // equivalent Task through run_all (same params, same fresh seed)
    fn rates(&self, r: f64, n_mc: usize) -> (f64, f64, f64, f64) {
        pass_rates(
            &self.mv_recall(),
            &self.bank.pools,
            r,
            self.practice(),
            &mut PyRandom::new(42),
            n_mc,
        )
    }
}

// Forward practice simulation from a given start state (reps/gaps as of the
// run date): day-by-day budget spending, a snapshot every 30 days fanning one
// pass_rates task per scenario into `tasks`.
#[allow(clippy::too_many_arguments)]
fn forward_sim(
    hours: f64,
    teach: f64,
    reps: Vec<i64>,
    gaps: Vec<i64>,
    cv: &Curve,
    bank: Arc<Bank>,
    scenarios: &[f64],
    n_mc: usize,
    tasks: &mut Vec<Task>,
) -> Vec<Snap> {
    let mut st = SimState::new(hours, teach, reps, gaps, cv, bank);
    let mut snaps: Vec<Snap> = Vec::new();
    while st.day < 540 {
        st.step();
        if st.day % 30 == 0 {
            let task_start = tasks.len();
            for &r in scenarios {
                tasks.push(st.task(r, n_mc));
            }
            snaps.push(Snap {
                day: st.day,
                practice: st.practice(),
                n_nodes: st.gaps.len(),
                offh: st.off_now(2),
                task_start,
            });
        }
    }
    snaps
}

// Exact crossing day for a milestone the monthly scan bracketed at checkpoint
// `hi0`: bisect (hi0 - 30, hi0], replaying the deterministic sim to each probe
// day and running the same central check (6000 sims, seed 42) the checkpoints
// use. The metric only rises with simulated practice, so ~5 probes pin the
// crossing to the day instead of the month. `use_onsite` picks the metric.
fn refine_day<'a, F: Fn() -> SimState<'a>>(
    mk_state: &F,
    r: f64,
    thr: f64,
    use_onsite: bool,
    hi0: i64,
) -> i64 {
    let (mut lo, mut hi) = ((hi0 - 30).max(0), hi0);
    while hi - lo > 1 {
        let mid = (lo + hi) / 2;
        let mut st = mk_state();
        while st.day < mid {
            st.step();
        }
        let (_, onsite, _, ph) = st.rates(r, 6000);
        let v = if use_onsite { onsite } else { ph };
        if v >= thr {
            hi = mid;
        } else {
            lo = mid;
        }
    }
    hi
}

// reps (clean-rep counts) and gaps (days since last evidence) per node, from
// the evidence visible as of `as_of`.
fn init_state(
    node_ids: &[String],
    evidence: &[EvRec],
    as_of: NaiveDate,
    cv: &Curve,
) -> (Vec<i64>, Vec<i64>) {
    let reps = node_ids
        .iter()
        .map(|nid| {
            let c = evidence
                .iter()
                .filter(|r| r.moves.get(nid.as_str()).map(String::as_str) == Some("clean"))
                .count() as i64;
            c.max(1)
        })
        .collect();
    let gaps = node_ids
        .iter()
        .map(|nid| {
            let (_, last) = node_status(nid, evidence, as_of, cv);
            last.map_or(0, |l| (as_of - l).num_days())
        })
        .collect();
    (reps, gaps)
}

// -------------------------------------------------------------- rendering --

fn styled(text: &str, style: &str, color: bool) -> String {
    if !color {
        return text.to_string();
    }
    let code = match style {
        "bold" => "1",
        "dim" => "2",
        "red" => "31",
        "yellow" => "33",
        "green" => "32",
        "bold green" => "1;32",
        "cyan" => "36",
        _ => "0",
    };
    format!("\x1b[{}m{}\x1b[0m", code, text)
}

fn prob_style(v: f64) -> &'static str {
    if v < 0.25 {
        "red"
    } else if v < 0.5 {
        "yellow"
    } else if v < 0.75 {
        "green"
    } else {
        "bold green"
    }
}

fn risk_style(v: f64) -> &'static str {
    if v <= 0.20 {
        "green"
    } else if v <= 0.35 {
        "yellow"
    } else {
        "red"
    }
}

fn pct(v: f64, width: usize, prec: usize) -> String {
    format!("{:>w$}", format!("{:.p$}%", v * 100.0, p = prec), w = width)
}

struct Cell {
    text: String,
    style: Option<&'static str>,
}

impl Cell {
    fn new(text: String, style: Option<&'static str>) -> Self {
        Cell { text, style }
    }
}

// tabulate-style rendering: column widths fit the widest of header and cells,
// numbers right-aligned under their header, two-space gutters.
fn print_table(
    headers: &[(&str, bool)], // (label, left_align)
    header_style: Option<&'static str>,
    rows: &[Vec<Cell>],
    color: bool,
) {
    let width = |s: &str| s.chars().count();
    let mut widths: Vec<usize> = headers.iter().map(|(h, _)| width(h)).collect();
    for row in rows {
        for (i, c) in row.iter().enumerate() {
            widths[i] = widths[i].max(width(&c.text));
        }
    }
    let pad = |s: &str, w: usize, left: bool| {
        let fill = " ".repeat(w - width(s));
        if left {
            format!("{}{}", s, fill)
        } else {
            format!("{}{}", fill, s)
        }
    };
    let head: Vec<String> = headers
        .iter()
        .enumerate()
        .map(|(i, (h, left))| {
            let padded = pad(h, widths[i], *left);
            match header_style {
                Some(st) => styled(&padded, st, color),
                None => padded,
            }
        })
        .collect();
    println!("  {}", head.join("  "));
    for row in rows {
        let cells: Vec<String> = row
            .iter()
            .enumerate()
            .map(|(i, c)| {
                let padded = pad(&c.text, widths[i], headers[i].1);
                match c.style {
                    Some(st) => styled(&padded, st, color),
                    None => padded,
                }
            })
            .collect();
        println!("  {}", cells.join("  "));
    }
}

const MONTHS: [&str; 12] = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

fn fmt_date_short(d: NaiveDate) -> String {
    format!("{} {} {:02}", d.day(), MONTHS[d.month0() as usize], d.year() % 100)
}

fn fmt_date_long(d: NaiveDate) -> String {
    format!("{} {} {}", d.day(), MONTHS[d.month0() as usize], d.year())
}

// Python's "{:g}" for the values this CLI sees (finite, moderate magnitude).
fn fmt_g(x: f64) -> String {
    if x == 0.0 {
        return "0".to_string();
    }
    let exp = x.abs().log10().floor() as i32;
    if !(-4..6).contains(&exp) {
        let mantissa = x / 10f64.powi(exp);
        let mut m = format!("{:.5}", mantissa);
        while m.ends_with('0') {
            m.pop();
        }
        if m.ends_with('.') {
            m.pop();
        }
        return format!("{}e{}{:02}", m, if exp < 0 { "-" } else { "+" }, exp.abs());
    }
    let prec = (5 - exp).max(0) as usize;
    let mut s = format!("{:.p$}", x, p = prec);
    if s.contains('.') {
        while s.ends_with('0') {
            s.pop();
        }
        if s.ends_with('.') {
            s.pop();
        }
    }
    s
}

fn print_wrapped(text: &str, style: &str, color: bool, width: usize) {
    let mut line = String::new();
    for word in text.split(' ') {
        if line.is_empty() {
            line = word.to_string();
        } else if line.chars().count() + 1 + word.chars().count() <= width {
            line.push(' ');
            line.push_str(word);
        } else {
            println!("{}", styled(&line, style, color));
            line = word.to_string();
        }
    }
    if !line.is_empty() {
        println!("{}", styled(&line, style, color));
    }
}

// ---------------------------------------------------------------- loading --

fn find_graph_dir() -> PathBuf {
    let local = PathBuf::from("graph");
    if local.join("curve.json").exists() {
        return local;
    }
    let mut dir = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .unwrap_or_default();
    loop {
        let g = dir.join("graph");
        if g.join("curve.json").exists() {
            return g;
        }
        if !dir.pop() {
            panic!("graph/ directory not found");
        }
    }
}

fn load_json(path: &PathBuf) -> Value {
    let text = std::fs::read_to_string(path).unwrap_or_else(|e| panic!("{}: {}", path.display(), e));
    serde_json::from_str(&text).unwrap_or_else(|e| panic!("{}: {}", path.display(), e))
}

// ------------------------------------------------------------------- main --

fn main() {
    unsafe {
        libc::signal(libc::SIGPIPE, libc::SIG_DFL);
    }
    let graph = find_graph_dir();
    let color = std::io::stdout().is_terminal();
    let today = chrono::Local::now().date_naive();
    let repo_root = match graph.parent() {
        Some(p) if p.as_os_str().is_empty() => PathBuf::from("."),
        Some(p) => p.to_path_buf(),
        None => PathBuf::from("."),
    };
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let json_mode = argv.iter().any(|a| a == "--json");
    let history_mode = argv.iter().any(|a| a == "--history-json");
    let hours_arg: Option<f64> = argv.iter().find(|a| !a.starts_with("--")).map(|s| {
        s.parse().unwrap_or_else(|_| {
            eprintln!("could not convert string to float: '{}'", s);
            std::process::exit(1);
        })
    });

    let nodes_v = load_json(&graph.join("nodes.json"));
    let node_ids: Vec<String> = nodes_v["nodes"]
        .as_array()
        .expect("nodes.json: nodes[]")
        .iter()
        .map(|n| n["id"].as_str().unwrap().to_string())
        .collect();

    let problems_v = load_json(&graph.join("problems.json"));

    let evidence_v = load_json(&graph.join("evidence.json"));
    let mut evidence: Vec<EvRec> = evidence_v["evidence"]
        .as_object()
        .expect("evidence.json: evidence{}")
        .iter()
        .map(|(fname, rec)| {
            let assist = match rec.get("assist").and_then(Value::as_str) {
                Some(a) if ["none", "hint", "walkthrough", "spoiled"].contains(&a) => a,
                _ => "none",
            };
            EvRec {
                fname: fname.clone(),
                date: rec["date"].as_str().expect("evidence date").to_string(),
                moves: rec
                    .get("moves")
                    .and_then(Value::as_object)
                    .map(|m| {
                        m.iter()
                            .map(|(k, v)| (k.clone(), v.as_str().unwrap_or("").to_string()))
                            .collect()
                    })
                    .unwrap_or_default(),
                assist: assist.to_string(),
            }
        })
        .collect();
    // chronological, so a historical replay date is just a prefix slice; every
    // downstream computation is order-independent
    evidence.sort_by(|a, b| a.date.cmp(&b.date));

    let curve_v = load_json(&graph.join("curve.json"));
    let p = &curve_v["params"];
    let cv = Curve {
        a: p["a"].as_f64().unwrap(),
        b: p["b"].as_f64().unwrap(),
        c: p["c"].as_f64().unwrap(),
        d: p.get("d").and_then(Value::as_f64).unwrap_or(0.0),
        e: p.get("e").and_then(Value::as_f64).unwrap_or(0.0),
        conn_mean: p.get("conn_mean").and_then(Value::as_f64).unwrap_or(0.0),
        conn: curve_v
            .get("conn")
            .and_then(Value::as_object)
            .map(|m| {
                m.iter()
                    .filter_map(|(k, v)| v.as_f64().map(|f| (k.clone(), f)))
                    .collect()
            })
            .unwrap_or_default(),
        beta: p["beta"].as_f64().unwrap(),
        target: curve_v["target_retention"].as_f64().unwrap(),
    };

    // --golden-json: the lockstep contract with utils/kg/kg_lib.py — node_status
    // over the real evidence for every node id (plus every move name evidence
    // mentions) and PyRandom sample streams, diffed bit-for-bit against the
    // Python side by utils/tests/test_golden.py. Not a user-facing mode.
    if argv.iter().any(|a| a == "--golden-json") {
        let status_name = |s: u8| match s {
            SOLID => "SOLID",
            STALE => "STALE",
            FRAGILE => "FRAGILE",
            _ => "MISSING",
        };
        let mut ids = node_ids.clone();
        let known: std::collections::HashSet<&String> = node_ids.iter().collect();
        let mut extra: Vec<String> = evidence
            .iter()
            .flat_map(|r| r.moves.keys())
            .filter(|k| !known.contains(k))
            .cloned()
            .collect();
        extra.sort();
        extra.dedup();
        ids.extend(extra);
        let mut nodes = serde_json::Map::new();
        for nid in &ids {
            let (st, last) = node_status(nid, &evidence, today, &cv);
            nodes.insert(
                nid.clone(),
                serde_json::json!({
                    "status": status_name(st),
                    "last": last.map(|d| d.format("%Y-%m-%d").to_string()),
                }),
            );
        }
        let mut rng = PyRandom::new(42);
        let randoms: Vec<f64> = (0..20).map(|_| rng.random()).collect();
        let mut rng = PyRandom::new(42);
        let randints: Vec<u32> = (0..20).map(|_| rng.randint(1, 1000)).collect();
        println!(
            "{}",
            serde_json::json!({
                "today": today.format("%Y-%m-%d").to_string(),
                "nodes": nodes,
                "random": randoms,
                "randint": randints,
            })
        );
        return;
    }

    // the bank: real per-difficulty problem pools from evidenced + drafted
    // walks, one move universe (nodes first, then off-taxonomy extras)
    let predicted_v = load_json(&graph.join("predicted.json"));
    let metadata_v = load_json(&repo_root.join("data/problems_metadata.json"));
    let bank = Arc::new(Bank::build(&problems_v, &predicted_v, &metadata_v, &node_ids));

    let mv_recall_of = |recall: &[f64]| -> Arc<Vec<Option<f64>>> {
        Arc::new(
            (0..bank.move_names.len())
                .map(|i| if i < bank.n_known { Some(recall[i]) } else { None })
                .collect(),
        )
    };

    // --history-json: replay the whole history — for every day since the
    // first evidence record, recompute that day's central rates and milestone
    // projection from the evidence visible on that day (same math and seeds,
    // central scenario only). Feeds the README's "Projected Ready Dates Over
    // Time" chart; the last element agrees with --json.
    if history_mode {
        if evidence.is_empty() {
            println!("[]");
            return;
        }
        let pace_log = solve_log(&repo_root);
        let central_r = SCENARIOS[1].1;
        let first = parse_date(&evidence[0].date);
        let n_days = ((today - first).num_days() + 1).max(0) as usize;
        // per-date evidence prefix lengths, precomputed once
        let mut prefix_len = vec![0usize; n_days];
        {
            let mut k = 0usize;
            for (i, p) in prefix_len.iter_mut().enumerate() {
                let d = first + Duration::days(i as i64);
                while k < evidence.len() && parse_date(&evidence[k].date) <= d {
                    k += 1;
                }
                *p = k;
            }
        }
        // Each date's whole pipeline (today's rates, monthly scan, milestone
        // bisection) runs synchronously in one worker; dates fan out across
        // cores. The checks are bit-identical to the single-run path (same
        // params, same fresh seeds), so the last element agrees with --json.
        let cursor = AtomicUsize::new(0);
        let out = Mutex::new(vec![Value::Null; n_days]);
        let workers = std::thread::available_parallelism()
            .map(|c| c.get())
            .unwrap_or(4)
            .min(n_days.max(1));
        std::thread::scope(|s| {
            for _ in 0..workers {
                s.spawn(|| loop {
                    let i = cursor.fetch_add(1, Ordering::Relaxed);
                    if i >= n_days {
                        break;
                    }
                    let d = first + Duration::days(i as i64);
                    let ev = &evidence[..prefix_len[i]];
                    let hours_d = hours_arg.or_else(|| week_pace(&pace_log, d)).unwrap_or(2.0);
                    let teach_d = (measured_first_contact(ev) * 0.8).min(0.85);
                    let recall_d = current_recall(&node_ids, ev, &cv, d);
                    let (_, onsite_t, screen_t, ph_t) = pass_rates(
                        &mv_recall_of(&recall_d),
                        &bank.pools,
                        central_r,
                        (0, 0, 0),
                        &mut PyRandom::new(42),
                        N_MC,
                    );
                    let (reps0, gaps0) = init_state(&node_ids, ev, d, &cv);
                    let mk_state = || {
                        SimState::new(
                            hours_d,
                            teach_d,
                            reps0.clone(),
                            gaps0.clone(),
                            &cv,
                            bank.clone(),
                        )
                    };
                    // monthly scan for crossing brackets, then bisect each to
                    // its exact day
                    let mut checkpoints: [Option<i64>; 3] = [None, None, None];
                    let mut st = mk_state();
                    while st.day < 540 {
                        st.step();
                        if st.day % 30 == 0 {
                            let (_, onsite_c, _, ph_c) = st.rates(central_r, 6000);
                            for (slot, lvl) in [(0usize, 0.25), (1, 0.5)] {
                                if ph_c >= lvl && checkpoints[slot].is_none() {
                                    checkpoints[slot] = Some(st.day);
                                }
                            }
                            if onsite_c >= 0.5 && checkpoints[2].is_none() {
                                checkpoints[2] = Some(st.day);
                            }
                            if checkpoints.iter().all(Option::is_some) {
                                break;
                            }
                        }
                    }
                    let refine = |slot: usize, thr: f64, use_onsite: bool| {
                        checkpoints[slot]
                            .map(|hi| refine_day(&mk_state, central_r, thr, use_onsite, hi))
                            .map(|dd| Value::String((d + Duration::days(dd)).to_string()))
                            .unwrap_or(Value::Null)
                    };
                    let entry = serde_json::json!({
                        "run_date": d.to_string(),
                        "hours": hours_d,
                        "screen": screen_t,
                        "onsite": onsite_t,
                        "hard": ph_t,
                        "hards_workable": refine(0, 0.25, false),
                        "hard_competent": refine(1, 0.5, false),
                        "onsite_ready": refine(2, 0.5, true),
                    });
                    out.lock().unwrap()[i] = entry;
                });
            }
        });
        println!("{}", Value::Array(out.into_inner().unwrap()));
        return;
    }

    let (hours, source): (f64, &str) = match hours_arg {
        Some(h) => (h, ""),
        None => match week_pace(&solve_log(&repo_root), today) {
            Some(p) => (p, "avg of the current streak; "),
            None => (2.0, ""),
        },
    };

    let recall_today = current_recall(&node_ids, &evidence, &cv, today);
    let mfc = measured_first_contact(&evidence);
    let teach = (mfc * 0.8).min(0.85);

    let mv_recall_today = mv_recall_of(&recall_today);
    let mut tasks: Vec<Task> = SCENARIOS
        .iter()
        .map(|&(_, r)| Task {
            mv_recall: mv_recall_today.clone(),
            bank: bank.clone(),
            r,
            practice: (0, 0, 0),
            n_mc: N_MC,
        })
        .collect();

    // forward: practice within the graph AND growth of the graph itself
    let scenario_rs: Vec<f64> = SCENARIOS.iter().map(|&(_, r)| r).collect();
    let (reps0, gaps0) = init_state(&node_ids, &evidence, today, &cv);
    let snaps = forward_sim(
        hours,
        teach,
        reps0.clone(),
        gaps0.clone(),
        &cv,
        bank.clone(),
        &scenario_rs,
        6000,
        &mut tasks,
    );

    let results = run_all(&tasks);

    let mut rows: Vec<(i64, (i64, i64, i64), usize, f64, Vec<(f64, f64, f64, f64)>)> = Vec::new();
    // workable, competent, onsite-ready (the faang-readiness line)
    let mut milestones: [Option<i64>; 3] = [None, None, None];
    for s in &snaps {
        let spread: Vec<(f64, f64, f64, f64)> =
            results[s.task_start..s.task_start + SCENARIOS.len()].to_vec();
        let ph_c = spread[1].3;
        let onsite_c = spread[1].1;
        rows.push((s.day, s.practice, s.n_nodes, s.offh, spread));
        for (slot, lvl) in [(0usize, 0.25), (1, 0.5)] {
            if ph_c >= lvl && milestones[slot].is_none() {
                milestones[slot] = Some(s.day);
            }
        }
        if onsite_c >= 0.5 && milestones[2].is_none() {
            milestones[2] = Some(s.day);
        }
    }

    // exact-day refine: bisect within each crossed checkpoint's month, so the
    // reported dates (and the README replay chart) move daily instead of in
    // 30-day steps. The forward table stays monthly; its highlight marks the
    // crossing checkpoint row (`milestones`), while the printed milestone
    // lines and --json use the refined days.
    let central_r = SCENARIOS[1].1;
    let mk_state = || {
        SimState::new(
            hours,
            teach,
            reps0.clone(),
            gaps0.clone(),
            &cv,
            bank.clone(),
        )
    };
    let milestone_days: [Option<i64>; 3] = [
        milestones[0].map(|hi| refine_day(&mk_state, central_r, 0.25, false, hi)),
        milestones[1].map(|hi| refine_day(&mk_state, central_r, 0.5, false, hi)),
        milestones[2].map(|hi| refine_day(&mk_state, central_r, 0.5, true, hi)),
    ];

    // --json: today's central rates + the milestone dates, consumed live by
    // utils/kg/estimate and the dashboard (same contract as kg_predict --json)
    if json_mode {
        let (_, onsite_t, screen_t, ph_t) = results[1];
        let m_date = |slot: usize| {
            milestone_days[slot]
                .map(|d| Value::String((today + Duration::days(d)).to_string()))
                .unwrap_or(Value::Null)
        };
        let obj = serde_json::json!({
            "hours": hours,
            "screen": screen_t,
            "onsite": onsite_t,
            "hard": ph_t,
            "hards_workable": m_date(0),
            "hard_competent": m_date(1),
            "onsite_ready": m_date(2),
        });
        println!("{}", obj);
        return;
    }

    println!("{}", styled("today, cold, on a random 2E+2M+2H set:", "bold", color));
    let today_rows: Vec<Vec<Cell>> = SCENARIOS
        .iter()
        .enumerate()
        .map(|(i, (name, _))| {
            let (_, onsite, screen, ph) = results[i];
            vec![
                Cell::new(name.to_string(), None),
                Cell::new(pct(screen, 0, 1), Some(prob_style(screen))),
                Cell::new(pct(onsite, 0, 1), Some(prob_style(onsite))),
                Cell::new(pct(ph, 0, 1), Some(prob_style(ph))),
            ]
        })
        .collect();
    print_table(
        &[
            ("scenario", true),
            ("screen (both M)", false),
            ("onsite (2E+2M+>=1H)", false),
            ("P(one hard)", false),
        ],
        None,
        &today_rows,
        color,
    );
    println!(
        "{}",
        styled(
            &format!(
                "  measured: first-contact absorption {} -> miss-to-node conversion {}",
                pct(teach / 0.8, 0, 0),
                pct(teach, 0, 0)
            ),
            "dim",
            color
        )
    );

    println!();
    println!(
        "{} {}",
        styled(&format!("forward at {}h/day", fmt_g(hours)), "bold", color),
        styled(
            &format!(
                "({}hards from day {}, mocks deferred to day {})",
                source, HARDS_START, MOCKS_START
            ),
            "dim",
            color
        )
    );
    let forward_rows: Vec<Vec<Cell>> = rows
        .iter()
        .map(|(day, (md, mk, hd), n_nodes, offh, spread)| {
            let mut scr: Vec<f64> = spread.iter().map(|s| s.2).collect();
            scr.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let mut ons: Vec<f64> = spread.iter().map(|s| s.1).collect();
            ons.sort_by(|a, b| a.partial_cmp(b).unwrap());
            let ph = spread[1].3;
            let when = fmt_date_short(today + Duration::days(*day));
            let mut cells = vec![
                Cell::new(when, Some("bold")),
                Cell::new(format!("{:4}/{:3}/{:4}", md, mk, hd), Some("dim")),
                Cell::new(n_nodes.to_string(), Some("cyan")),
                Cell::new(pct(*offh, 0, 0), Some(risk_style(*offh))),
                Cell::new(pct(ph, 0, 0), Some(prob_style(ph))),
                Cell::new(
                    format!("{}\u{2013}{}", pct(scr[0], 3, 0), pct(scr[2], 3, 0)),
                    Some(prob_style((scr[0] + scr[2]) / 2.0)),
                ),
                Cell::new(
                    format!(
                        "{}\u{2013}{}\u{2013}{}",
                        pct(ons[0], 3, 0),
                        pct(ons[1], 3, 0),
                        pct(ons[2], 3, 0)
                    ),
                    Some(prob_style(ons[1])),
                ),
            ];
            if milestones[2] == Some(*day) {
                for c in &mut cells {
                    c.style = Some("bold green");
                }
            }
            cells
        })
        .collect();
    print_table(
        &[
            ("month", true),
            ("practice (M/mk/H)", false),
            ("nodes", false),
            ("offH", false),
            ("P(hard)", false),
            ("P(screen)", false),
            ("P(onsite)", false),
        ],
        Some("bold"),
        &forward_rows,
        color,
    );
    for (slot, tag, lvl) in [
        (0usize, "hards workable", "P >=25%"),
        (1, "hard-competent", "P >=50%"),
        (2, "onsite-ready", "central P(onsite) >=50%"),
    ] {
        if let Some(d) = milestone_days[slot] {
            let when = fmt_date_long(today + Duration::days(d));
            println!(
                "  {} ({}) ~ {}",
                styled(tag, "bold green", color),
                lvl,
                styled(&when, "bold", color)
            );
        }
    }
    print_wrapped(
        "measured: solve times, forgetting curve, first-contact absorption, and the \
         problem bank itself (real walks, LLM-drafted for unsolved problems; drafts \
         score P 0.80 / R 0.75 vs 50 evidenced walks). assumed: recognition scenarios, \
         mock start day, derive rate. The band collapses as real data arrives.",
        "dim",
        color,
        80,
    );
}
