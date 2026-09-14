// The simulation: the real picker (kg::pick::pick) run forward one day at
// a time on simulated evidence. Ported from utils/kg/kg_simulate (Python);
// the header of main.rs says what is modelled.

use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::process::Command;

use chrono::{Duration, NaiveDate};
use indexmap::IndexMap;
use kg::ctx::{Ctx, PView};
use kg::data::{Assist, Rec};
use kg::drills::{bank_authored, due_drill};
use kg::evidence::Evidence;
use kg::git::{mined_solve_times, sleep_state};
use kg::mock::PyRandom;
use kg::model::{
    median, retention_cycle, solve_logit, solve_model, solve_ratings, solve_scenarios, walk_terms,
};
use kg::pick::{due_on, pick, PickArgs};
use kg::status::{
    all_statuses, current_recall, immature_nodes, node_curve_recall, node_status, Statuses,
    FRAGILE, MISSING, SOLID, STALE, STARVED_DAYS,
};

pub const MAX_DAYS: i64 = 730;
/// calendar days the pace is averaged over (kg_mock_rs week_pace)
pub const PACE_WINDOW: i64 = 28;
/// calendar days the authoring rate is averaged over
pub const AUTHOR_WINDOW: i64 = PACE_WINDOW;
pub const KINDS: [&str; 4] = ["Easy", "Medium", "Hard", "drill"];

/// One timed attempt in the git log: (date, minutes, kind, verdict).
pub type Attempt = (NaiveDate, f64, String, &'static str);

/// kg_simulate.timed_attempts: kind Easy/Medium/Hard/drill, verdict clean
/// (every move clean, no assist) or struggled. The same trailers make mock
/// paces itself by.
pub fn timed_attempts(ctx: &Ctx, ev: &Evidence, problems: &kg::data::Problems) -> Vec<Attempt> {
    let mut out = Vec::new();
    for (key, d, secs, fname) in mined_solve_times(ctx) {
        let Some(&i) = ev.by_fname.get(&fname) else {
            continue;
        };
        let rec = ev.rec(i);
        let kind = if key.starts_with("d:") {
            "drill".to_string()
        } else {
            ctx.problem_difficulty(&key, problems)
        };
        if !KINDS.contains(&kind.as_str()) {
            continue;
        }
        let clean = rec.moves.values().all(|v| v == "clean") && rec.assist_any() == "none";
        out.push((
            d,
            secs as f64 / 60.0,
            kind,
            if clean { "clean" } else { "struggled" },
        ));
    }
    out
}

/// Python's round(x, 1): the shortest decimal, ties to even on the exact
/// binary value.
fn round1(x: f64) -> f64 {
    format!("{x:.1}").parse().unwrap()
}

fn round2(x: f64) -> f64 {
    format!("{x:.2}").parse().unwrap()
}

/// kg_simulate.week_pace: hours per calendar day over the last PACE_WINDOW
/// days, cut at the first dead week walking back from today.
pub fn week_pace(attempts: &[Attempt], today: NaiveDate) -> f64 {
    let mut mins = vec![0.0f64; PACE_WINDOW as usize];
    for (d, m, _, _) in attempts {
        let i = (today - *d).num_days();
        if (0..PACE_WINDOW).contains(&i) {
            mins[i as usize] += m;
        }
    }
    let (mut window, mut run) = (PACE_WINDOW as usize, 0usize);
    for (i, &m) in mins.iter().enumerate() {
        run = if m == 0.0 { run + 1 } else { 0 };
        if run == 7 {
            window = i + 1 - run;
            break;
        }
    }
    let window = window.max(7);
    let mut total = 0.0;
    for m in &mins[..window] {
        total += m;
    }
    round1(total / window as f64 / 60.0)
}

/// kg_simulate.price_table: (kind, verdict) -> median minutes, the kind's
/// median as the fallback for a verdict never timed, the overall median
/// for a kind never timed.
pub fn price_table(attempts: &[Attempt]) -> HashMap<(String, &'static str), f64> {
    let mut by: HashMap<(String, &str), Vec<f64>> = HashMap::new();
    let mut by_kind: HashMap<String, Vec<f64>> = HashMap::new();
    for (_, m, kind, verdict) in attempts {
        by.entry((kind.clone(), verdict)).or_default().push(*m);
        by_kind.entry(kind.clone()).or_default().push(*m);
    }
    let overall = if attempts.is_empty() {
        15.0
    } else {
        median(&attempts.iter().map(|a| a.1).collect::<Vec<_>>())
    };
    let mut table = HashMap::new();
    for kind in KINDS {
        for verdict in ["clean", "struggled"] {
            let pool = by
                .get(&(kind.to_string(), verdict))
                .filter(|v| !v.is_empty())
                .or_else(|| by_kind.get(kind).filter(|v| !v.is_empty()))
                .cloned()
                .unwrap_or_else(|| vec![overall]);
            table.insert((kind.to_string(), verdict), median(&pool));
        }
    }
    table
}

/// kg_simulate.bank_history: ({node: date its first bank file landed},
/// {node: files on disk}) from the git log of drills/. Only files still on
/// disk count; an untracked file counts as landed today.
pub fn bank_history(
    root: &Path,
    drills_dir: &Path,
    today: NaiveDate,
) -> (HashMap<String, NaiveDate>, HashMap<String, i64>) {
    let out = Command::new("git")
        .args([
            "log",
            "--diff-filter=A",
            "--format=%x00%ad",
            "--date=short",
            "--name-only",
            "--",
            "drills/*/*.py",
        ])
        .current_dir(root)
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).to_string())
        .unwrap_or_default();
    let mut first: IndexMap<String, NaiveDate> = IndexMap::new();
    let mut d: Option<NaiveDate> = None;
    for line in out.lines() {
        if let Some(rest) = line.strip_prefix('\0') {
            d = Some(kg::data::parse_date(rest));
        } else if line.starts_with("drills/") && root.join(line).exists() {
            let d = d.expect("git log prints the date line before its files");
            let e = first.entry(line.to_string()).or_insert(d);
            *e = (*e).min(d);
        }
    }
    let mut on_disk: Vec<PathBuf> = Vec::new();
    // glob("*/*.py"): dot-directories and dot-files excluded
    let hidden = |p: &Path| {
        p.file_name()
            .and_then(|n| n.to_str())
            .is_some_and(|n| n.starts_with('.'))
    };
    if let Ok(rd) = std::fs::read_dir(drills_dir) {
        for e in rd.filter_map(Result::ok) {
            if !e.path().is_dir() || hidden(&e.path()) {
                continue;
            }
            if let Ok(files) = std::fs::read_dir(e.path()) {
                on_disk.extend(
                    files
                        .filter_map(Result::ok)
                        .map(|f| f.path())
                        .filter(|p| p.extension().is_some_and(|x| x == "py") && !hidden(p)),
                );
            }
        }
    }
    on_disk.sort();
    for path in on_disk {
        let rel = format!(
            "drills/{}/{}",
            path.parent()
                .and_then(|p| p.file_name())
                .and_then(|s| s.to_str())
                .unwrap_or(""),
            path.file_name().and_then(|s| s.to_str()).unwrap_or("")
        );
        first.entry(rel).or_insert(today);
    }
    let mut banked: HashMap<String, NaiveDate> = HashMap::new();
    let mut sizes: HashMap<String, i64> = HashMap::new();
    for (rel, d) in first {
        let node = rel.split('/').nth(1).unwrap_or("").to_string();
        let e = banked.entry(node.clone()).or_insert(d);
        *e = (*e).min(d);
        *sizes.entry(node).or_insert(0) += 1;
    }
    (banked, sizes)
}

fn banked_recently(banked: &HashMap<String, NaiveDate>, today: NaiveDate) -> i64 {
    banked
        .values()
        .filter(|d| (0..AUTHOR_WINDOW).contains(&(today - **d).num_days()))
        .count() as i64
}

/// kg_simulate.measured_bank_rate: new banks per calendar day over the last
/// AUTHOR_WINDOW days.
pub fn measured_bank_rate(banked: &HashMap<String, NaiveDate>, today: NaiveDate) -> f64 {
    round2(banked_recently(banked, today) as f64 / AUTHOR_WINDOW as f64)
}

/// A scratch copy of drills/ the run authors into: every real bank file
/// linked in, virtual files written beside them. Ctx reads its drills
/// directory at call time, so the run points it at the copy.
pub struct ScratchBank {
    pub real: PathBuf,
    pub root: PathBuf,
    /// node -> virtual files written
    pub authored: IndexMap<String, i64>,
}

impl ScratchBank {
    pub fn new(real: PathBuf) -> ScratchBank {
        let root = std::env::temp_dir().join(format!(
            "kg_simulate_bank_{}_{}",
            std::process::id(),
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .map(|d| d.as_nanos())
                .unwrap_or(0)
        ));
        std::fs::create_dir_all(&root).expect("scratch bank");
        if let Ok(rd) = std::fs::read_dir(&real) {
            for e in rd.filter_map(Result::ok) {
                if !e.path().is_dir() {
                    continue;
                }
                let node = e.file_name();
                let Ok(files) = std::fs::read_dir(e.path()) else {
                    continue;
                };
                for f in files.filter_map(Result::ok) {
                    let path = f.path();
                    if path.extension().is_none_or(|x| x != "py") {
                        continue;
                    }
                    let dir = root.join(&node);
                    let _ = std::fs::create_dir_all(&dir);
                    let _ = std::os::unix::fs::symlink(&path, dir.join(f.file_name()));
                }
            }
        }
        ScratchBank {
            real,
            root,
            authored: IndexMap::new(),
        }
    }

    /// Write `files` virtual bank files for node: a DRILL title and a
    /// TRAINS line, nothing else. No drills.json entry, so the file comes
    /// after nothing; TRAINS only its node, so it holds on no other.
    pub fn author(&mut self, node: &str, files: i64) {
        let d = self.root.join(node);
        let _ = std::fs::create_dir_all(&d);
        for _ in 0..files {
            let k = self.authored.get(node).copied().unwrap_or(0) + 1;
            self.authored.insert(node.to_string(), k);
            let _ = std::fs::write(
                d.join(format!("sim_{k}.py")),
                format!("\"\"\"\nDRILL: Sim {node} {k}\nTRAINS: {node}\n\"\"\"\n"),
            );
        }
    }
}

impl Drop for ScratchBank {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

/// kg_simulate.first_contact: the share of nodes whose first ever rep was
/// clean (kg_mock_rs measured_first_contact).
pub fn first_contact(ev: &Evidence) -> f64 {
    let mut order: Vec<usize> = (0..ev.len()).collect();
    order.sort_by(|&a, &b| ev.fname(a).cmp(ev.fname(b)));
    let mut first: HashMap<&str, ((&str, &str), &str)> = HashMap::new();
    for i in order {
        let rec = ev.rec(i);
        let key = (rec.date.as_str(), ev.fname(i));
        for (node, v) in &rec.moves {
            match first.get(node.as_str()) {
                Some((k0, _)) if key >= *k0 => {}
                _ => {
                    first.insert(node, (key, v));
                }
            }
        }
    }
    if first.is_empty() {
        return 0.7;
    }
    first.values().filter(|(_, v)| *v == "clean").count() as f64 / first.len() as f64
}

#[derive(Clone, Debug)]
pub struct SimAttempt {
    pub date: NaiveDate,
    pub problem: String,
    pub difficulty: String,
    pub rating: f64,
    pub first: bool,
    /// the Elo game a first sight played: 1.0 won, 0.0 lost, None a repeat
    pub score: Option<f64>,
}

#[derive(Clone, Debug)]
pub struct DayRow {
    pub day: NaiveDate,
    pub solves: IndexMap<String, i64>,
    pub stale: i64,
    pub fragile: i64,
    pub missing: i64,
    pub onsite: f64,
    pub screen: f64,
    pub hard: f64,
}

pub struct Authored {
    pub nodes: usize,
    pub files: i64,
    pub rate: f64,
    pub source: String,
}

pub struct RunResult {
    /// the last day run
    pub day: i64,
    pub start: NaiveDate,
    pub onsite: f64,
    pub hours: f64,
    pub source: String,
    pub per_kind: IndexMap<String, i64>,
    /// days the picker served nothing at all
    pub dry_days: i64,
    /// days it ran out before half the hours were used
    pub short_days: i64,
    /// (day_no, stale, fragile, missing) at the first pick of the day
    pub rusty: Vec<(i64, i64, i64, i64)>,
    /// node -> the longest run of due days with no pick aimed at it, for
    /// every run of STARVED_DAYS or more
    pub starved: IndexMap<String, i64>,
    pub series: Vec<DayRow>,
    pub attempts: Vec<SimAttempt>,
    pub authored: Authored,
    /// the closed-form (onsite, screen, hard) on the real evidence today
    pub today_rates: (f64, f64, f64),
}

pub struct RunArgs {
    pub hours: Option<f64>,
    pub seed: i64,
    pub days: i64,
    pub every: i64,
    pub draft_error: f64,
    pub bank_rate: Option<f64>,
}

/// Least recalled first; a node with no recall reads as 0.
fn by_recall(recall: &HashMap<String, f64>, a: &str, b: &str) -> std::cmp::Ordering {
    let r = |n: &str| recall.get(n).copied().unwrap_or(0.0);
    r(a).partial_cmp(&r(b)).unwrap()
}

fn pct0(x: f64) -> String {
    format!("{:.0}%", x * 100.0)
}

/// The .envrc knobs leave the environment for the run (conftest does the
/// same for the suite): the run is the picker on its own rules, not the
/// .envrc of the day. TARGET_PASS_RATE says what "ready" means and is read
/// before this. Returns what was dropped, for the caller to put back.
pub fn drop_knobs(root: &Path) -> Vec<(String, String)> {
    let mut saved = Vec::new();
    for (name, _) in kg::data::envrc_pairs(root) {
        if let Ok(v) = std::env::var(&name) {
            saved.push((name.clone(), v));
            std::env::remove_var(&name);
        }
    }
    saved
}

pub fn restore_knobs(saved: Vec<(String, String)>) {
    for (name, v) in saved {
        std::env::set_var(name, v);
    }
}

/// kg_simulate.run. Prints the rows through `log` (None for a silent run).
/// The .envrc knobs are out of the environment for the run and back
/// after; Ctx's clock is frozen day by day and restored.
pub fn run(
    ctx: &Ctx,
    recs: Vec<(String, Rec)>,
    args: &RunArgs,
    log: Option<&dyn Fn(&str)>,
) -> RunResult {
    let target = kg::model::target_pass_rate();
    let knobs = drop_knobs(&ctx.root);
    let real = ctx.drills_dir();
    let bank = ScratchBank::new(real.clone());
    ctx.set_drills_dir(bank.root.clone());
    let start = ctx.today();
    let out = run_(ctx, recs, args, log, target, bank);
    ctx.set_drills_dir(real);
    ctx.freeze(start);
    restore_knobs(knobs);
    out
}

fn run_(
    ctx: &Ctx,
    recs: Vec<(String, Rec)>,
    args: &RunArgs,
    log: Option<&dyn Fn(&str)>,
    target: f64,
    mut bank: ScratchBank,
) -> RunResult {
    let log = |s: String| {
        if let Some(f) = log {
            f(&s);
        }
    };
    let mut rng = PyRandom::new(args.seed.unsigned_abs() as u32);
    let mut days = args.days;
    let pv = RefCell::new(PView::new(ctx.evidenced()));
    let predicted = &ctx.predicted;
    let mut ev = Evidence::new(recs);
    let Some(cv) = &ctx.curve else {
        eprintln!("graph/curve.json missing - run make curve first");
        std::process::exit(1);
    };
    let mined_problems = pv.borrow().map.clone();

    let (pools, ratings) = crate::expect::build_pools(ctx, &mined_problems, predicted);
    let Some(coef) = solve_model(ctx) else {
        eprintln!("graph/curve.json has no fitted cold-solve model - run make curve");
        std::process::exit(1);
    };
    let node_order: Vec<String> = ctx.nodes.keys().cloned().collect();
    let expect = crate::expect::PassExpectation::new(&pools, &ratings, &node_order, coef.clone());
    // Is the target even reachable? The ceiling is what a perfect graph
    // scores - every move recalled, none never-met - at the optimistic end
    // of the band on the last projected day. Nothing the simulation does
    // beats it, so a target above it is never crossed however long the run
    // goes on. Then the run has only its picker diagnostics left to earn,
    // and one retention cycle (the median node's window, so the typical
    // move comes due and is repaired once) is as far as those need.
    let ceiling = expect.ceiling(solve_scenarios(ctx, days).2).1;
    if ceiling < target {
        let cycle = retention_cycle(ctx, &ev);
        if cycle < days {
            log(format!(
                "target P(onsite) {} is above the model's ceiling of {} (a perfect graph, \
                 optimistic band, day {days}): no run can cross it. Stopping at one retention \
                 cycle ({cycle}d) instead of {days}d - the diagnostics are what is left to learn.",
                pct0(target),
                pct0(ceiling)
            ));
            days = cycle;
        }
    }
    let ratings_of = solve_ratings(ctx);
    let median_rating: HashMap<String, f64> = ratings
        .iter()
        .map(|(d, v)| {
            let mut s = v.clone();
            s.sort_by(|a, b| a.partial_cmp(b).unwrap());
            (
                d.clone(),
                if s.is_empty() { 1500.0 } else { s[s.len() / 2] },
            )
        })
        .collect();
    let teach = (first_contact(&ev) * 0.8).min(0.85);
    let asleep = sleep_state(ctx, &pv.borrow(), &ev);

    // the central line moves with the measured Elo drift, so a projected
    // day is priced at the skill the evidence says he will have then
    let shift_on = |day_no: i64| solve_scenarios(ctx, day_no).1;
    let shift = shift_on(0);
    let start = ctx.today();
    let attempts = timed_attempts(ctx, &ev, &mined_problems);
    let prices = price_table(&attempts);
    let measured = week_pace(&attempts, start);
    let given = args.hours.is_some();
    let hours = args.hours.unwrap_or(measured);
    if hours <= 0.0 {
        eprintln!("measured pace is 0h/day - pass hours explicitly");
        std::process::exit(1);
    }
    let (banked, sizes) = bank_history(&ctx.root, &bank.real, start);
    let measured_rate = measured_bank_rate(&banked, start);
    let rate = args.bank_rate.unwrap_or(measured_rate);
    let mut size_pool: Vec<i64> = sizes.values().copied().collect();
    size_pool.sort();
    if size_pool.is_empty() {
        size_pool.push(1);
    }
    let mut author_budget = 0.0;
    let mut authored_files = 0i64;
    let rate_src = if args.bank_rate.is_some() {
        "given".to_string()
    } else {
        format!(
            "measured: {} nodes banked in the last {AUTHOR_WINDOW} days",
            banked_recently(&banked, start)
        )
    };

    let price = |kind: &str, clean: bool| -> f64 {
        prices[&(kind.to_string(), if clean { "clean" } else { "struggled" })]
    };

    let mut seen: HashSet<String> = ev.recs.iter().map(|(_, r)| r.problem_str()).collect();
    let mut per_kind: IndexMap<String, i64> = KINDS.iter().map(|k| (k.to_string(), 0)).collect();
    let mut seq = 0i64;
    let mut dry_days = 0i64;
    let mut short_days = 0i64;
    let mut rusty: Vec<(i64, i64, i64, i64)> = Vec::new();
    // consecutive due days, no pick aimed
    let mut streak: HashMap<String, i64> = ctx.nodes.keys().map(|n| (n.clone(), 0)).collect();
    let mut starved: IndexMap<String, i64> = IndexMap::new();
    let mut series: Vec<DayRow> = Vec::new();
    let mut attempts_log: Vec<SimAttempt> = Vec::new();
    let src = if given {
        "given".to_string()
    } else {
        format!(
            "measured: avg of the current streak, {}h",
            kg::pyjson::g(measured)
        )
    };
    if args.draft_error != 0.0 {
        log(format!(
            "model knobs off their defaults: draft-error {}",
            kg::pyjson::g(args.draft_error)
        ));
    }
    log(format!(
        "policy: kg_next.pick at {}h/day ({src}), seed {}; teach {teach:.2}, curve graph/curve.json",
        kg::pyjson::g(hours),
        args.seed
    ));
    let features: Vec<String> = cv
        .raw
        .get("solve")
        .and_then(|s| s.get("features"))
        .and_then(|f| f.as_object())
        .map(|o| {
            o.iter()
                .map(|(f, c)| format!("{:+.3}·{f}", c.as_f64().unwrap_or(0.0)))
                .collect()
        })
        .unwrap_or_default();
    let games = cv
        .raw
        .get("solve")
        .and_then(|s| s.get("games"))
        .map(kg::data::value_str)
        .unwrap_or_default();
    log(format!(
        "cold-solve model: logit P = {} (curve.json, fitted on {games} timed games)",
        features.join(" ")
    ));
    log(format!(
        "drill authoring: {} new banks/day ({rate_src}), size drawn from the {} banks on disk \
         (median {} files); {} of {} nodes bankless today",
        kg::pyjson::g(rate),
        size_pool.len(),
        kg::pyjson::g(median(
            &size_pool.iter().map(|&x| x as f64).collect::<Vec<_>>()
        )),
        ctx.nodes
            .keys()
            .filter(|n| !banked.contains_key(*n))
            .count(),
        ctx.nodes.len()
    ));
    log(format!(
        "price per attempt, measured medians (clean / struggled): {}",
        KINDS
            .iter()
            .map(|k| format!("{k} {:.0}/{:.0}m", price(k, true), price(k, false)))
            .collect::<Vec<_>>()
            .join(", ")
    ));
    log(format!(
        "{:>4}  {:10}  {:>6}  {:>5}  {:>5}  {:>9}  {:>7}  {:>9}  {:>9}",
        "day", "date", "solves", "solid", "young", "reach", "P(hard)", "P(screen)", "P(onsite)"
    ));

    let rates =
        |ev: &Evidence, day: NaiveDate, recall: Option<&HashMap<String, f64>>, day_no: i64| {
            match recall {
                Some(r) => expect.rates(r, shift_on(day_no)),
                None => expect.rates(&current_recall(ctx, ev, day), shift_on(day_no)),
            }
        };
    let today_rates = {
        let (_, o, s, h) = rates(&ev, start, None, 0);
        (o, s, h)
    };

    let report = |ev: &Evidence,
                  day_no: i64,
                  day: NaiveDate,
                  solves_today: i64,
                  statuses: Option<&Statuses>,
                  recall: Option<&HashMap<String, f64>>|
     -> f64 {
        let owned;
        let statuses = match statuses {
            Some(s) => s,
            None => {
                owned = all_statuses(ctx, ev, day);
                &owned
            }
        };
        let imm = immature_nodes(ctx, ev, &pv.borrow());
        let pvb = pv.borrow();
        let blocked = predicted
            .iter()
            .filter(|(p, _)| !pvb.contains(p))
            .filter(|(_, entry)| {
                !entry.walks.iter().any(|w| {
                    w.moves
                        .iter()
                        .filter(|m| ctx.nodes.contains_key(*m))
                        .all(|m| kg::status::st(statuses, m).0 == SOLID && !imm.contains(m))
                        && w.moves.iter().all(|m| ctx.nodes.contains_key(m))
                        && !w.missing
                })
            })
            .count();
        let (_, onsite, screen, phard) = rates(ev, day, recall, day_no);
        let solid = statuses.values().filter(|s| s.0 == SOLID).count();
        log(format!(
            "{day_no:>4}  {:10}  {solves_today:>6}  {solid:>5}  {:>5}  {:>4}/{:<4}  {:>6}  {:>8}  {:>8}",
            day.format("%Y-%m-%d"),
            imm.len(),
            predicted.len() - blocked,
            predicted.len(),
            pct0(phard),
            pct0(screen),
            pct0(onsite)
        ));
        onsite
    };

    let close_streak =
        |n: &str, streak: &mut HashMap<String, i64>, starved: &mut IndexMap<String, i64>| {
            let s = streak[n];
            if s >= STARVED_DAYS && s > starved.get(n).copied().unwrap_or(0) {
                starved.insert(n.to_string(), s);
            }
            streak.insert(n.to_string(), 0);
        };

    let mut onsite = report(&ev, 0, start, 0, None, None);
    let mut day_no = 0;
    let mut reached = false;
    while day_no < days {
        day_no += 1;
        let day = start + Duration::days(day_no);
        ctx.freeze(day);
        let mut budget = hours * 60.0;
        let mut exclude: HashSet<String> = HashSet::new();
        let mut solves_today = 0i64;
        // node -> (target?, struggled?) over the day's picks
        let mut touched: IndexMap<String, (bool, bool)> = IndexMap::new();
        let mut today_kind: IndexMap<String, i64> =
            KINDS.iter().map(|k| (k.to_string(), 0)).collect();
        // statuses and recall once per day; after a solve only its moves change
        let mut statuses = all_statuses(ctx, &ev, day);
        let mut recall = current_recall(ctx, &ev, day);
        let mut counts: HashMap<kg::status::Status, i64> = HashMap::new();
        let carr = pv.borrow().carrier_counts(ctx);
        let mut cache = HashMap::new();
        for n in ctx.nodes.keys() {
            *counts.entry(statuses[n].0).or_insert(0) += 1;
            // due by the picker's own test (kg_next.due_on): rusty, SOLID
            // at its floor, or MISSING with every prereq SOLID
            if due_on(ctx, n, &ev, &carr, day, &mut cache) {
                *streak.get_mut(n).unwrap() += 1;
            } else {
                close_streak(n, &mut streak, &mut starved);
            }
        }
        let count = |s| counts.get(&s).copied().unwrap_or(0);
        rusty.push((day_no, count(STALE), count(FRAGILE), count(MISSING)));
        while budget > 0.0 {
            let pa = PickArgs {
                asleep: asleep.clone(),
                exclude: exclude.clone(),
                ..PickArgs::default()
            };
            let Some(choice) = pick(ctx, &pv, &ev, &statuses, &pa) else {
                break;
            };
            let target_node = choice.target.clone();
            let pnum = choice.pnum.clone();
            close_streak(&target_node, &mut streak, &mut starved);
            seq += 1;
            // the exact shape `make solved` writes (kg_lib.FNAME_TS_RE,
            // drill_key): a hyphenated date made every simulated drill rep
            // a first rep, so no floor ever advanced (2026-09-06)
            let (h, rem) = (seq / 3600, seq % 3600);
            let stamp = format!(
                "{}T{h:02}_{:02}_{:02}_000000_00_00Z",
                day.format("%Y_%m_%d"),
                rem / 60,
                rem % 60
            );
            let (kind, moves, fname, problem): (String, Vec<String>, String, String);
            if pnum.starts_with("drill:") {
                let Some(path) = due_drill(ctx, &target_node, &ev, day, false, false) else {
                    break;
                };
                kind = "drill".to_string();
                let t = ctx.drill_trains(&path);
                moves = if t.is_empty() {
                    vec![target_node.clone()]
                } else {
                    t
                };
                let stem = ctx.drill_solved_stem(&path);
                fname = format!("solved/d_{stem}_{stamp}.py");
                problem = "drill".to_string();
                exclude.insert(pnum.clone());
            } else {
                let pvb = pv.borrow();
                let p = pvb.get(&pnum).expect("picked problem");
                kind = match p.difficulty.as_deref() {
                    Some(d) if !d.is_empty() => d.to_string(),
                    _ => ctx.problem_difficulty(&pnum, &pvb.map),
                };
                moves = p.moves.clone();
                fname = format!("solved/p{pnum}_sim_{stamp}.py");
                problem = pnum.clone();
                exclude.insert(pnum.clone());
            }
            let mut verdict: IndexMap<String, String> = IndexMap::new();
            for m in &moves {
                if !ctx.nodes.contains_key(m) {
                    continue;
                }
                // a node met but never clean has no curve recall: it is
                // still being taught, so the teach rate applies
                let p_clean = match recall.get(m) {
                    Some(&r) if statuses[m].0 != MISSING => r,
                    _ => teach,
                };
                let v = if rng.random() < p_clean {
                    "clean"
                } else {
                    "struggled"
                };
                verdict.insert(m.clone(), v.to_string());
            }
            let dif = match kind.as_str() {
                "Easy" => "E",
                "Hard" => "H",
                _ => "M",
            };
            let rating = ratings_of
                .get(&problem)
                .copied()
                .unwrap_or(median_rating[dif]);
            let first = problem != "drill" && !seen.contains(&problem);
            let mut score = None; // the Elo game a first sight plays; a repeat plays none
            if first && !verdict.is_empty() {
                // a cold problem: the pass model's own odds on top of recall.
                // The model is fitted on scored games, so this draw is the
                // game: won cold and inside the clock, or not
                let mut walk = moves.clone();
                if rng.random() < args.draft_error {
                    walk.push("off-taxonomy".to_string()); // the draft missed a move
                }
                let (ln_recall, unseen) = walk_terms(&walk, &recall);
                let p_cold =
                    1.0 / (1.0 + (-(solve_logit(&coef, rating, ln_recall, unseen) + shift)).exp());
                score = Some(1.0);
                if rng.random() >= p_cold {
                    score = Some(0.0);
                    let weakest = verdict
                        .keys()
                        .min_by(|a, b| by_recall(&recall, a, b))
                        .cloned()
                        .unwrap();
                    verdict.insert(weakest, "struggled".to_string());
                }
            }
            let clean = verdict.values().all(|v| v == "clean");
            for (m, v) in &verdict {
                let was = touched.get(m).copied().unwrap_or((false, false));
                touched.insert(
                    m.clone(),
                    (was.0 || *m == target_node, was.1 || v == "struggled"),
                );
            }
            let kind_key = if KINDS.contains(&kind.as_str()) {
                kind.clone()
            } else {
                "Medium".to_string()
            };
            budget -= price(&kind_key, clean);
            ev.push(
                fname,
                Rec {
                    date: day.format("%Y-%m-%d").to_string(),
                    problem: Some(problem.clone()),
                    moves: verdict.clone(),
                    assist: Assist::None,
                    followup: None,
                    pending: None,
                    note: None,
                    judge: None,
                },
            );
            if problem != "drill" {
                attempts_log.push(SimAttempt {
                    date: day,
                    problem: problem.clone(),
                    difficulty: kind.clone(),
                    rating,
                    first,
                    score,
                });
            }
            for m in verdict.keys() {
                statuses.insert(m.clone(), node_status(ctx, m, &ev, day));
                match node_curve_recall(ctx, m, &ev, day) {
                    None => {
                        recall.remove(m);
                    }
                    Some(r) => {
                        recall.insert(m.clone(), r);
                    }
                }
            }
            solves_today += 1;
            *per_kind.get_mut(&kind_key).unwrap() += 1;
            *today_kind.get_mut(&kind_key).unwrap() += 1;
            seen.insert(problem);
        }
        dry_days += (solves_today == 0) as i64;
        short_days += (budget > hours * 30.0) as i64;
        author_budget += rate;
        while author_budget >= 1.0 {
            let mut cands: Vec<String> = touched
                .keys()
                .filter(|n| !ctx.has_drill_bank(n))
                .cloned()
                .collect();
            cands.sort_by(|a, b| {
                let ka = (!touched[a].0, !touched[a].1);
                let kb = (!touched[b].0, !touched[b].1);
                ka.cmp(&kb).then_with(|| by_recall(&recall, a, b))
            });
            if cands.is_empty() {
                cands = ctx
                    .nodes
                    .keys()
                    .filter(|n| !ctx.has_drill_bank(n))
                    .cloned()
                    .collect();
                cands.sort_by(|a, b| by_recall(&recall, a, b));
            }
            if cands.is_empty() {
                break; // every node has a bank
            }
            let files = size_pool[rng.randbelow(size_pool.len() as u32) as usize];
            bank.author(&cands[0], files);
            bank_authored(ctx, &ev, &cands[0]);
            authored_files += files;
            author_budget -= 1.0;
        }
        let (_, o, screen, phard) = rates(&ev, day, Some(&recall), day_no);
        onsite = o;
        let mut end: HashMap<kg::status::Status, i64> = HashMap::new();
        for s in statuses.values() {
            *end.entry(s.0).or_insert(0) += 1;
        }
        let end = |s| end.get(&s).copied().unwrap_or(0);
        series.push(DayRow {
            day,
            solves: today_kind,
            stale: end(STALE),
            fragile: end(FRAGILE),
            missing: end(MISSING),
            onsite,
            screen,
            hard: phard,
        });
        if day_no % args.every == 0 || day_no == days || onsite >= target {
            onsite = report(
                &ev,
                day_no,
                day,
                solves_today,
                Some(&statuses),
                Some(&recall),
            );
            if onsite >= target {
                reached = true;
                break;
            }
        }
    }
    if !reached {
        day_no = days;
    }
    for n in ctx.nodes.keys() {
        close_streak(n, &mut streak, &mut starved);
    }
    RunResult {
        day: day_no,
        start,
        onsite,
        hours,
        source: src,
        per_kind,
        dry_days,
        short_days,
        rusty,
        starved,
        series,
        attempts: attempts_log,
        authored: Authored {
            nodes: bank.authored.len(),
            files: authored_files,
            rate,
            source: rate_src,
        },
        today_rates,
    }
}
