// kg_mock — the Monte-Carlo pass-rate model behind `make mock`: today's cold
// mock estimate plus the forward practice simulation.
//
// Ported from (and replacing) the retired Python utils/kg_mock. The core model
// math (pass_rates / current_recall) is shared with utils/kg_lib.py, which the
// README's P(pass) history chart uses — change the two together. PyRandom
// reproduces CPython's random.Random exactly so results stay comparable with
// the Python era. utils/test_mock.py guards output shape and speed.

use std::collections::HashMap;
use std::io::IsTerminal;
use std::path::PathBuf;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};

use chrono::{Datelike, Duration, NaiveDate};
use serde_json::Value;

// ---------------------------------------------------------------- PyRandom --
// CPython's random.Random: MT19937 seeded via init_by_array, with random(),
// getrandbits() and randint() reproduced exactly.

struct PyRandom {
    mt: [u32; 624],
    mti: usize,
}

impl PyRandom {
    fn new(seed: u32) -> Self {
        let mut r = PyRandom { mt: [0; 624], mti: 624 };
        r.init_by_array(&[seed]);
        r
    }

    fn init_genrand(&mut self, s: u32) {
        self.mt[0] = s;
        for i in 1..624usize {
            self.mt[i] = 1812433253u32
                .wrapping_mul(self.mt[i - 1] ^ (self.mt[i - 1] >> 30))
                .wrapping_add(i as u32);
        }
        self.mti = 624;
    }

    fn init_by_array(&mut self, key: &[u32]) {
        self.init_genrand(19650218);
        let (mut i, mut j) = (1usize, 0usize);
        for _ in 0..std::cmp::max(624, key.len()) {
            self.mt[i] = (self.mt[i]
                ^ (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)).wrapping_mul(1664525))
            .wrapping_add(key[j])
            .wrapping_add(j as u32);
            i += 1;
            j += 1;
            if i >= 624 {
                self.mt[0] = self.mt[623];
                i = 1;
            }
            if j >= key.len() {
                j = 0;
            }
        }
        for _ in 0..623 {
            self.mt[i] = (self.mt[i]
                ^ (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)).wrapping_mul(1566083941))
            .wrapping_sub(i as u32);
            i += 1;
            if i >= 624 {
                self.mt[0] = self.mt[623];
                i = 1;
            }
        }
        self.mt[0] = 0x80000000;
        self.mti = 624;
    }

    fn genrand(&mut self) -> u32 {
        const M: usize = 397;
        const MATRIX_A: u32 = 0x9908b0df;
        const UPPER: u32 = 0x80000000;
        const LOWER: u32 = 0x7fffffff;
        if self.mti >= 624 {
            let mt = &mut self.mt;
            for kk in 0..624 - M {
                let y = (mt[kk] & UPPER) | (mt[kk + 1] & LOWER);
                mt[kk] = mt[kk + M] ^ (y >> 1) ^ if y & 1 != 0 { MATRIX_A } else { 0 };
            }
            for kk in 624 - M..623 {
                let y = (mt[kk] & UPPER) | (mt[kk + 1] & LOWER);
                mt[kk] = mt[kk + M - 624] ^ (y >> 1) ^ if y & 1 != 0 { MATRIX_A } else { 0 };
            }
            let y = (mt[623] & UPPER) | (mt[0] & LOWER);
            mt[623] = mt[M - 1] ^ (y >> 1) ^ if y & 1 != 0 { MATRIX_A } else { 0 };
            self.mti = 0;
        }
        let mut y = self.mt[self.mti];
        self.mti += 1;
        y ^= y >> 11;
        y ^= (y << 7) & 0x9d2c5680;
        y ^= (y << 15) & 0xefc60000;
        y ^= y >> 18;
        y
    }

    fn random(&mut self) -> f64 {
        let a = (self.genrand() >> 5) as f64;
        let b = (self.genrand() >> 6) as f64;
        (a * 67108864.0 + b) * (1.0 / 9007199254740992.0)
    }

    fn getrandbits(&mut self, k: u32) -> u32 {
        self.genrand() >> (32 - k)
    }

    fn randbelow(&mut self, n: u32) -> u32 {
        let k = 32 - n.leading_zeros();
        let mut r = self.getrandbits(k);
        while r >= n {
            r = self.getrandbits(k);
        }
        r
    }

    fn randint(&mut self, a: u32, b: u32) -> u32 {
        a + self.randbelow(b - a + 1)
    }
}

// ------------------------------------------------------------- data model --

struct EvRec {
    fname: String,
    date: String,
    moves: HashMap<String, String>,
    assist: String,
}

struct Curve {
    a: f64,
    b: f64,
    c: f64,
    d: f64,
    beta: f64,
    target: f64,
}

const SOLID: u8 = 0;
const STALE: u8 = 1;
const FRAGILE: u8 = 2;
const MISSING: u8 = 3;

fn assist_weight(a: &str) -> f64 {
    match a {
        "hint" => 0.5,
        "walkthrough" => 1.0,
        "spoiled" => 2.0,
        _ => 0.0,
    }
}

fn parse_date(s: &str) -> NaiveDate {
    NaiveDate::parse_from_str(s, "%Y-%m-%d").expect("bad date in evidence")
}

fn node_status(node: &str, evidence: &[EvRec], today: NaiveDate, cv: &Curve) -> (u8, Option<NaiveDate>) {
    let mut entries: Vec<(&str, &str, &str)> = Vec::new();
    for rec in evidence {
        if let Some(v) = rec.moves.get(node) {
            if !v.is_empty() {
                entries.push((rec.date.as_str(), v.as_str(), rec.assist.as_str()));
            }
        }
    }
    if entries.is_empty() {
        return (MISSING, None);
    }
    entries.sort();
    let (last_date, last_verdict, _) = *entries.last().unwrap();
    let clean_dates: Vec<&str> = entries
        .iter()
        .filter(|(_, v, a)| *v == "clean" && *a != "spoiled")
        .map(|(d, _, _)| *d)
        .collect();
    if (last_verdict == "struggled" || last_verdict == "avoided")
        && !clean_dates.last().map_or(false, |c| *c >= last_date)
    {
        return (FRAGILE, Some(parse_date(last_date)));
    }
    if clean_dates.is_empty() {
        return (FRAGILE, Some(parse_date(last_date)));
    }
    let cleans = clean_dates.len() as f64;
    let struggles = entries.iter().filter(|(_, v, _)| *v == "struggled").count() as f64;
    let mut assisted = 0.0;
    for (_, _, a) in &entries {
        assisted += assist_weight(a);
    }
    let stability = (cv.a + cv.b * cleans - cv.c * struggles - cv.d * assisted)
        .exp()
        .max(7.0)
        .min(3650.0);
    let clean_last = parse_date(clean_dates.last().unwrap());
    let gap = (today - clean_last).num_days() as f64;
    if (1.0 + gap / stability).powf(-cv.beta) >= cv.target {
        (SOLID, Some(clean_last))
    } else {
        (STALE, Some(clean_last))
    }
}

fn current_recall(node_ids: &[String], evidence: &[EvRec], cv: &Curve, today: NaiveDate) -> Vec<f64> {
    node_ids
        .iter()
        .map(|nid| {
            let (status, last) = node_status(nid, evidence, today, cv);
            let cleans = evidence
                .iter()
                .filter(|r| r.moves.get(nid.as_str()).map(String::as_str) == Some("clean"))
                .count() as f64;
            if status == MISSING || last.is_none() {
                return 0.25;
            }
            let s = (cv.a + cv.b * cleans).exp().max(7.0).min(3650.0);
            let rec = (1.0 + (today - last.unwrap()).num_days() as f64 / s).powf(-cv.beta);
            if status == FRAGILE {
                rec * 0.5
            } else {
                rec
            }
        })
        .collect()
}

// First match of r"\d{4}_\d{2}_\d{2}T[\d_]+" in s, or "".
fn ts_match(s: &str) -> String {
    let b = s.as_bytes();
    let n = b.len();
    for i in 0..n {
        if i + 11 < n
            && b[i..i + 4].iter().all(u8::is_ascii_digit)
            && b[i + 4] == b'_'
            && b[i + 5].is_ascii_digit()
            && b[i + 6].is_ascii_digit()
            && b[i + 7] == b'_'
            && b[i + 8].is_ascii_digit()
            && b[i + 9].is_ascii_digit()
            && b[i + 10] == b'T'
            && (b[i + 11].is_ascii_digit() || b[i + 11] == b'_')
        {
            let mut j = i + 11;
            while j < n && (b[j].is_ascii_digit() || b[j] == b'_') {
                j += 1;
            }
            return s[i..j].to_string();
        }
    }
    String::new()
}

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

// Mirrors kg_mock's measured_week_pace: average hours/day over the last 7
// calendar days from `solve time: Xm Ys` trailers in git commits, rounded to
// 0.1h; None when the week has no timed solves.
fn measured_week_pace(repo_root: &PathBuf, today: NaiveDate) -> Option<f64> {
    let out = std::process::Command::new("git")
        .args(["log", "--format=%ad|%B~~~", "--date=short"])
        .current_dir(repo_root)
        .output()
        .ok()?;
    let log = String::from_utf8_lossy(&out.stdout).into_owned();
    let start = today - Duration::days(6);
    let mut minutes = 0.0f64;
    for block in log.split("~~~") {
        let block = block.trim();
        let Some(head) = block.get(..10) else { continue };
        let Ok(when) = NaiveDate::parse_from_str(head, "%Y-%m-%d") else { continue };
        if !(start <= when && when <= today) {
            continue;
        }
        let mut rest = block;
        while let Some(pos) = rest.find("solve time: ") {
            rest = &rest[pos + 12..];
            if let Some((m, s, consumed)) = parse_solve_trailer(rest) {
                minutes += m as f64 + s as f64 / 60.0;
                rest = &rest[consumed..];
            }
        }
    }
    let h: f64 = format!("{:.1}", minutes / 7.0 / 60.0).parse().unwrap();
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

const WALK_LEN: [(u32, u32); 3] = [(1, 2), (2, 4), (4, 6)];
const OFF_GRAPH0: [f64; 3] = [0.02, 0.10, 0.45];
const OFF_FLOOR: [f64; 3] = [0.01, 0.04, 0.15];
const UNKNOWN_POOL_M: f64 = 12.0;
const UNKNOWN_POOL_H: f64 = 35.0;
const REC_POWER: [f64; 3] = [0.5, 1.0, 1.6];
const SCENARIOS: [(&str, f64); 3] = [("cautious", 0.75), ("central", 0.85), ("optimistic", 0.95)];
const HARDS_START: i64 = 45;
const MOCKS_START: i64 = 90;
const MOCKS_PER_WEEK: f64 = 2.0;
const HARDS_PER_WEEK: f64 = 3.0;
const N_MC: usize = 20000;

// mv_recall: per move (in Counter order) the node's recall, or None -> derive.
fn pass_rates(
    mv_recall: &[Option<f64>],
    weights: &[f64],
    off: &[f64; 3],
    r_base: f64,
    practice: (i64, i64, i64),
    rng: &mut PyRandom,
    n_mc: usize,
) -> (f64, f64, f64, f64) {
    let (mediums, mocks, hards) = practice;
    let grow = 1.0 - (-(mediums as f64) / 120.0).exp();
    let time_f = [
        0.88 + 0.07 * grow,
        0.87 + 0.07 * grow,
        0.40 + 0.42 * (1.0 - (-(hards as f64) / 15.0).exp()),
    ];
    let derive = 0.25 + 0.20 * (1.0 - (-((mocks + hards) as f64) / 30.0).exp());
    let rec = r_base + (0.98 - r_base) * (1.0 - (-(mocks as f64) / 8.0).exp());
    let base_p = [
        time_f[0] * rec.powf(REC_POWER[0]),
        time_f[1] * rec.powf(REC_POWER[1]),
        time_f[2] * rec.powf(REC_POWER[2]),
    ];
    let mv_val: Vec<f64> = mv_recall.iter().map(|o| o.unwrap_or(derive)).collect();
    let mut cum = Vec::with_capacity(weights.len());
    let mut acc = 0.0;
    for w in weights {
        acc += w;
        cum.push(acc);
    }
    let total = cum[cum.len() - 1] + 0.0;
    let hi_idx = cum.len() - 1;

    let (mut full, mut onsite, mut screen, mut h_solved) = (0i64, 0i64, 0i64, 0i64);
    for _ in 0..n_mc {
        let mut solved = [0i32; 3];
        for &dif in &[0usize, 0, 1, 1, 2, 2] {
            let mut p = base_p[dif];
            if rng.random() < off[dif] {
                p *= derive;
            }
            let k = rng.randint(WALK_LEN[dif].0, WALK_LEN[dif].1);
            for _ in 0..k {
                let x = rng.random() * total;
                let (mut lo, mut hi) = (0usize, hi_idx);
                while lo < hi {
                    let mid = (lo + hi) / 2;
                    if x < cum[mid] {
                        hi = mid;
                    } else {
                        lo = mid + 1;
                    }
                }
                p *= mv_val[lo];
            }
            if rng.random() < p {
                solved[dif] += 1;
            }
        }
        full += (solved[0] == 2 && solved[1] == 2 && solved[2] == 2) as i64;
        onsite += (solved[0] == 2 && solved[1] == 2 && solved[2] >= 1) as i64;
        screen += (solved[1] == 2) as i64;
        h_solved += solved[2] as i64;
    }
    (
        full as f64 / n_mc as f64,
        onsite as f64 / n_mc as f64,
        screen as f64 / n_mc as f64,
        h_solved as f64 / (2 * n_mc) as f64,
    )
}

// Every pass_rates call is independent (fresh seeded RNG), so the whole
// Monte-Carlo load fans out over a thread pool; results land by task index.
struct Task {
    mv_recall: Arc<Vec<Option<f64>>>,
    weights: Arc<Vec<f64>>,
    off: [f64; 3],
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
                    &t.weights,
                    &t.off,
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
    let (hours, source): (f64, &str) = match std::env::args().nth(1) {
        Some(s) => (
            s.parse().unwrap_or_else(|_| {
                eprintln!("could not convert string to float: '{}'", s);
                std::process::exit(1);
            }),
            "",
        ),
        None => match measured_week_pace(&repo_root, today) {
            Some(p) => (p, "avg of last 7 days; "),
            None => (2.0, ""),
        },
    };

    let nodes_v = load_json(&graph.join("nodes.json"));
    let node_ids: Vec<String> = nodes_v["nodes"]
        .as_array()
        .expect("nodes.json: nodes[]")
        .iter()
        .map(|n| n["id"].as_str().unwrap().to_string())
        .collect();

    let problems_v = load_json(&graph.join("problems.json"));
    let problems = problems_v["problems"].as_object().expect("problems.json: problems{}");

    let evidence_v = load_json(&graph.join("evidence.json"));
    let evidence: Vec<EvRec> = evidence_v["evidence"]
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

    let curve_v = load_json(&graph.join("curve.json"));
    let p = &curve_v["params"];
    let cv = Curve {
        a: p["a"].as_f64().unwrap(),
        b: p["b"].as_f64().unwrap(),
        c: p["c"].as_f64().unwrap(),
        d: p.get("d").and_then(Value::as_f64).unwrap_or(0.0),
        beta: p["beta"].as_f64().unwrap(),
        target: curve_v["target_retention"].as_f64().unwrap(),
    };

    // move_freq: Counter over every problem walk, first-appearance order
    let mut freq_names: Vec<String> = Vec::new();
    let mut freq_weights: Vec<f64> = Vec::new();
    let mut freq_index: HashMap<String, usize> = HashMap::new();
    for (_pnum, v) in problems {
        let Some(obj) = v.as_object() else { continue };
        let Some(mvs) = obj.get("moves").and_then(Value::as_array) else { continue };
        for mv in mvs {
            let name = mv.as_str().unwrap();
            match freq_index.get(name) {
                Some(&i) => freq_weights[i] += 1.0,
                None => {
                    freq_index.insert(name.to_string(), freq_names.len());
                    freq_names.push(name.to_string());
                    freq_weights.push(1.0);
                }
            }
        }
    }
    let median_w = {
        let mut v = freq_weights.clone();
        v.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let n = v.len();
        if n % 2 == 1 {
            v[n / 2]
        } else {
            (v[n / 2 - 1] + v[n / 2]) / 2.0
        }
    };

    let node_index: HashMap<&str, usize> =
        node_ids.iter().enumerate().map(|(i, n)| (n.as_str(), i)).collect();
    let recall_today = current_recall(&node_ids, &evidence, &cv, today);
    let mfc = measured_first_contact(&evidence);
    let teach = (mfc * 0.8).min(0.85);

    let mv_recall_today: Arc<Vec<Option<f64>>> = Arc::new(
        freq_names
            .iter()
            .map(|n| node_index.get(n.as_str()).map(|&i| recall_today[i]))
            .collect(),
    );
    let freq_weights_arc = Arc::new(freq_weights.clone());
    let mut tasks: Vec<Task> = SCENARIOS
        .iter()
        .map(|&(_, r)| Task {
            mv_recall: mv_recall_today.clone(),
            weights: freq_weights_arc.clone(),
            off: OFF_GRAPH0,
            r,
            practice: (0, 0, 0),
            n_mc: N_MC,
        })
        .collect();

    // forward: practice within the graph AND growth of the graph itself
    let mut reps: Vec<i64> = node_ids
        .iter()
        .map(|nid| {
            let c = evidence
                .iter()
                .filter(|r| r.moves.get(nid.as_str()).map(String::as_str) == Some("clean"))
                .count() as i64;
            c.max(1)
        })
        .collect();
    let mut gaps: Vec<i64> = node_ids
        .iter()
        .map(|nid| {
            let (_, last) = node_status(nid, &evidence, today, &cv);
            last.map_or(0, |l| (today - l).num_days())
        })
        .collect();
    let mut off = OFF_GRAPH0;
    let (mut unknown_m, mut unknown_h) = (UNKNOWN_POOL_M, UNKNOWN_POOL_H);
    let mut freq_now = freq_weights.clone();
    let mut freq_node_idx: Vec<Option<usize>> = freq_names
        .iter()
        .map(|n| node_index.get(n.as_str()).copied())
        .collect();
    let (mut mediums_done, mut mocks_done, mut hards_done) = (0i64, 0i64, 0i64);
    let mut syn = 0i64;
    let mut snaps: Vec<(i64, (i64, i64, i64), usize, f64)> = Vec::new();
    let mut day = 0i64;
    let hards_per_week = (HARDS_PER_WEEK * hours / 2.0).min(6.0);

    macro_rules! learn_ideas {
        ($dif:expr, $encounters:expr) => {{
            let dif: usize = $dif;
            let learned = teach * off[dif] * $encounters as f64;
            let (unknown, pool) = if dif == 1 {
                unknown_m = (unknown_m - learned).max(0.0);
                (unknown_m, UNKNOWN_POOL_M)
            } else {
                unknown_h = (unknown_h - learned).max(0.0);
                (unknown_h, UNKNOWN_POOL_H)
            };
            off[dif] = OFF_FLOOR[dif] + (OFF_GRAPH0[dif] - OFF_FLOOR[dif]) * unknown / pool;
            while (syn as f64)
                < UNKNOWN_POOL_M + UNKNOWN_POOL_H - unknown_m - unknown_h - 0.5
            {
                syn += 1;
                reps.push(1);
                gaps.push(0);
                freq_now.push(median_w);
                freq_node_idx.push(Some(reps.len() - 1));
            }
        }};
    }

    while day < 540 {
        day += 1;
        let mut budget = hours * 60.0;
        for g in gaps.iter_mut() {
            *g += 1;
        }
        let mut order: Vec<usize> = (0..gaps.len()).collect();
        order.sort_by(|&x, &y| gaps[y].cmp(&gaps[x]));
        for &n in &order {
            let s = (cv.a + cv.b * reps[n] as f64).exp().max(7.0).min(3650.0);
            if (1.0 + gaps[n] as f64 / s).powf(-cv.beta) < cv.target && budget >= 10.0 {
                budget -= 10.0;
                gaps[n] = 0;
                reps[n] += 1;
            }
        }
        while budget >= 23.0 {
            if day > HARDS_START
                && (hards_done as f64) < (day - HARDS_START) as f64 / 7.0 * hards_per_week
            {
                budget -= 40.0;
                hards_done += 1;
                learn_ideas!(2, 1i64);
            } else if day > MOCKS_START
                && (mocks_done as f64) < (day - MOCKS_START) as f64 / 7.0 * MOCKS_PER_WEEK
            {
                budget -= 90.0;
                mocks_done += 1;
            } else {
                budget -= 23.0;
                mediums_done += 1;
                learn_ideas!(1, 1i64);
            }
            let mut ord2: Vec<usize> = (0..gaps.len()).collect();
            ord2.sort_by_key(|&n| (reps[n], -gaps[n]));
            for &n in ord2.iter().take(3) {
                gaps[n] = 0;
                reps[n] += 1;
            }
        }
        if day % 30 == 0 {
            let rec_now: Vec<f64> = (0..gaps.len())
                .map(|n| {
                    let s = (cv.a + cv.b * reps[n] as f64).exp().max(7.0).min(3650.0);
                    (1.0 + gaps[n] as f64 / s).powf(-cv.beta)
                })
                .collect();
            let practice = (mediums_done, mocks_done, hards_done);
            let mv_recall: Arc<Vec<Option<f64>>> =
                Arc::new(freq_node_idx.iter().map(|o| o.map(|i| rec_now[i])).collect());
            let weights = Arc::new(freq_now.clone());
            for &(_, r) in &SCENARIOS {
                tasks.push(Task {
                    mv_recall: mv_recall.clone(),
                    weights: weights.clone(),
                    off,
                    r,
                    practice,
                    n_mc: 6000,
                });
            }
            snaps.push((day, practice, gaps.len(), off[2]));
        }
    }

    let results = run_all(&tasks);

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

    let mut rows: Vec<(i64, (i64, i64, i64), usize, f64, Vec<(f64, f64, f64, f64)>)> = Vec::new();
    // workable, competent, onsite-ready (the faang-readiness line)
    let mut milestones: [Option<i64>; 3] = [None, None, None];
    for (i, &(day, practice, n_nodes, offh)) in snaps.iter().enumerate() {
        let spread: Vec<(f64, f64, f64, f64)> = results[3 + 3 * i..6 + 3 * i].to_vec();
        let ph_c = spread[1].3;
        let onsite_c = spread[1].1;
        rows.push((day, practice, n_nodes, offh, spread));
        for (slot, lvl) in [(0usize, 0.25), (1, 0.5)] {
            if ph_c >= lvl && milestones[slot].is_none() {
                milestones[slot] = Some(day);
            }
        }
        if onsite_c >= 0.5 && milestones[2].is_none() {
            milestones[2] = Some(day);
        }
    }

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
        if let Some(d) = milestones[slot] {
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
        "measured: solve times, forgetting curve, 84% first-contact absorption. assumed: \
         unknown-idea pools (M 12, H 35), off-graph floors, recognition scenarios, mock \
         start day. The band collapses as real data arrives.",
        "dim",
        color,
        80,
    );
}
