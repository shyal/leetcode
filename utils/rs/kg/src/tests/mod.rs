// The picker is the one piece of tooling that decides what gets solved,
// and these tests pin its rules down. Every regression it has shipped was
// a sort key quietly outranking a more important one, or a frontier node
// that fell through every branch and left `make next` saying nothing.
//
// They run pick() against synthetic graphs (a handful of nodes and
// problems built in the test) so each rule is asserted in isolation, with
// no dependency on the real graph/*.json. The graph is pure input; the
// disk reads (the drill bank, the acceptance metadata) and the tables
// months of evidence derive (the unlock counts, the immature set) are
// stood in for through ctx::Stubs, which the Fx fixture fills. A test
// that wants the real function writes a bank under Fx::dir and leaves the
// stubs unset.
//
// They were utils/tests/test_kg_next.py until the Python picker they ran
// against was deleted (2026-09-14); the test names and their notes are
// kept, one section per rule.

mod bank;
mod clock;
mod frontier;
mod reach;
mod rules;

use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};

use chrono::{Duration, NaiveDate};
use indexmap::IndexMap;

use crate::ctx::{Ctx, PView, Stubs};
use crate::data::{
    load_curve, real_today, reset_test_env, Assist, Curve, DrillEntry, DrillMap, Metadata, Node,
    Nodes, Problem, Problems, Rec, Walk,
};
use crate::evidence::Evidence;
use crate::pick::{blocked_frontier, pick, ready_hards, Choice, PickArgs};
use crate::status::{Status, Statuses};

pub use crate::status::{FRAGILE, MISSING, SOLID, STALE};

pub fn today() -> NaiveDate {
    real_today()
}

pub fn ago(days: i64) -> NaiveDate {
    today() - Duration::days(days)
}

pub fn iso(days: i64) -> String {
    ago(days).format("%Y-%m-%d").to_string()
}

/// The repo root, for the fitted curve the Python tests loaded through
/// kg_lib._load_curve.
pub fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../..")
        .canonicalize()
        .unwrap()
}

static DIRS: AtomicU64 = AtomicU64::new(0);

/// A directory of the test's own (pytest's tmp_path), removed on drop.
pub struct TempDir(pub PathBuf);

impl TempDir {
    pub fn new() -> TempDir {
        let n = DIRS.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kg-tests-{}-{n}", std::process::id()));
        std::fs::create_dir_all(p.join("drills")).unwrap();
        TempDir(p)
    }
}

impl Drop for TempDir {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

pub fn node(id: &str) -> Node {
    Node {
        id: id.to_string(),
        name: id.to_string(),
        group: None,
        prereqs: vec![],
        desc: String::new(),
        drill: None,
    }
}

pub fn strs(v: &[&str]) -> Vec<String> {
    v.iter().map(|s| s.to_string()).collect()
}

pub fn set(v: &[&str]) -> HashSet<String> {
    strs(v).into_iter().collect()
}

/// A synthetic problem: Medium unless told otherwise.
pub fn problem(moves: &[&str]) -> Problem {
    Problem {
        title: "synthetic Medium".to_string(),
        difficulty: Some("Medium".to_string()),
        moves: strs(moves),
        ..Default::default()
    }
}

pub fn easy(moves: &[&str]) -> Problem {
    problem(moves).difficulty("Easy")
}

pub fn hard(moves: &[&str]) -> Problem {
    problem(moves).difficulty("Hard")
}

/// A drafted problems.json entry with one drafted walk.
pub fn drafted(moves: &[&str]) -> Problem {
    Problem {
        title: "synthetic draft".to_string(),
        walks: vec![Walk {
            moves: strs(moves),
            missing: false,
            missing_names: vec![],
        }],
        ..Default::default()
    }
}

pub fn drafted_missing(moves: &[&str], missing: &[&str]) -> Problem {
    let mut p = drafted(moves);
    p.walks[0].missing = true;
    p.walks[0].missing_names = strs(missing);
    p
}

pub trait ProblemExt {
    fn difficulty(self, d: &str) -> Problem;
    fn after(self, ids: &[&str]) -> Problem;
    fn banned(self) -> Problem;
    fn alt_walks(self, walks: &[&[&str]]) -> Problem;
    fn unmapped(self, moves: &[&str]) -> Problem;
    fn title(self, t: &str) -> Problem;
}

impl ProblemExt for Problem {
    fn difficulty(mut self, d: &str) -> Problem {
        self.difficulty = Some(d.to_string());
        self.title = format!("synthetic {d}");
        self
    }
    fn after(mut self, ids: &[&str]) -> Problem {
        self.after = strs(ids);
        self
    }
    fn banned(mut self) -> Problem {
        self.banned = true;
        self
    }
    fn alt_walks(mut self, walks: &[&[&str]]) -> Problem {
        self.alt_walks = walks.iter().map(|w| strs(w)).collect();
        self
    }
    fn unmapped(mut self, moves: &[&str]) -> Problem {
        self.unmapped = strs(moves);
        self
    }
    fn title(mut self, t: &str) -> Problem {
        self.title = t.to_string();
        self
    }
}

pub fn assist_map(pairs: &[(&str, &str)]) -> Assist {
    Assist::Map(
        pairs
            .iter()
            .map(|(k, v)| (k.to_string(), v.to_string()))
            .collect(),
    )
}

pub fn level(l: &str) -> Assist {
    Assist::Level(l.to_string())
}

fn rec(date: String, problem: &str, moves: &[(&str, &str)], assist: Assist) -> Rec {
    Rec {
        date,
        problem: Some(problem.to_string()),
        moves: moves
            .iter()
            .map(|(k, v)| (k.to_string(), v.to_string()))
            .collect::<IndexMap<_, _>>(),
        assist,
        followup: None,
        pending: None,
        note: None,
        judge: None,
    }
}

/// One evidence record. `moves` maps node -> clean/struggled/avoided.
pub fn solve(pnum: &str, moves: &[(&str, &str)], days_ago: i64) -> (String, Rec) {
    solve_a(pnum, moves, days_ago, Assist::None)
}

pub fn solve_a(pnum: &str, moves: &[(&str, &str)], days_ago: i64, assist: Assist) -> (String, Rec) {
    (
        format!("solved/p{pnum}_{days_ago}.py"),
        rec(iso(days_ago), pnum, moves, assist),
    )
}

/// A rep of a bank drill, filed under its DRILL title as make solved does.
pub fn drill_rep(title: &str, node: &str, days_ago: i64) -> (String, Rec) {
    drill_rep_v(title, node, days_ago, "clean", Assist::None)
}

pub fn drill_rep_a(title: &str, node: &str, days_ago: i64, assist: Assist) -> (String, Rec) {
    drill_rep_v(title, node, days_ago, "clean", assist)
}

pub fn drill_rep_v(
    title: &str,
    node: &str,
    days_ago: i64,
    verdict: &str,
    assist: Assist,
) -> (String, Rec) {
    let stem = title.replace(' ', "_");
    (
        format!("solved/d_{stem}_{days_ago}.py"),
        rec(iso(days_ago), "drill", &[(node, verdict)], assist),
    )
}

/// A drill rep under a solved/ name of the test's own choosing.
pub fn drill_file(fname: &str, node: &str, days_ago: i64, assist: Assist) -> (String, Rec) {
    (
        fname.to_string(),
        rec(iso(days_ago), "drill", &[(node, "clean")], assist),
    )
}

pub fn evidence(records: Vec<(String, Rec)>) -> Evidence {
    // a dict: a later record under the same name replaces the earlier
    let mut merged: IndexMap<String, Rec> = IndexMap::new();
    for (f, r) in records {
        merged.insert(f, r);
    }
    Evidence::new(merged.into_iter().collect())
}

pub fn no_evidence() -> Evidence {
    Evidence::new(vec![])
}

/// {node: (status, last)}; None is the MISSING node's date.
pub fn statuses(specs: &[(&str, Status, Option<i64>)]) -> Statuses {
    specs
        .iter()
        .map(|(n, s, d)| (n.to_string(), (*s, d.map(ago))))
        .collect()
}

pub trait ArgsExt {
    fn exclude(self, ids: &[&str]) -> PickArgs;
    fn asleep(self, ids: &[&str]) -> PickArgs;
    fn woken(self, ids: &[&str]) -> PickArgs;
    fn group(self, g: &str) -> PickArgs;
    fn cram(self) -> PickArgs;
    fn early(self) -> PickArgs;
    fn assisted(self) -> PickArgs;
    fn session_start(self) -> PickArgs;
}

impl ArgsExt for PickArgs {
    fn exclude(mut self, ids: &[&str]) -> PickArgs {
        self.exclude = set(ids);
        self
    }
    fn asleep(mut self, ids: &[&str]) -> PickArgs {
        self.asleep = strs(ids);
        self
    }
    fn woken(mut self, ids: &[&str]) -> PickArgs {
        self.woken = strs(ids);
        self
    }
    fn group(mut self, g: &str) -> PickArgs {
        self.group = Some(g.to_string());
        self
    }
    fn cram(mut self) -> PickArgs {
        self.cram = true;
        self
    }
    fn early(mut self) -> PickArgs {
        self.early = true;
        self
    }
    fn assisted(mut self) -> PickArgs {
        self.assisted = true;
        self
    }
    fn session_start(mut self) -> PickArgs {
        self.session_start = true;
        self
    }
}

pub fn args() -> PickArgs {
    PickArgs::default()
}

/// (target, status, pnum) of a pick, the Python test's `[:3]`.
pub fn t3(c: &Option<Choice>) -> (String, Status, String) {
    let c = c.as_ref().expect("a pick");
    (c.target.clone(), c.status, c.pnum.clone())
}

pub fn target(c: &Option<Choice>) -> String {
    c.as_ref().expect("a pick").target.clone()
}

pub fn pnum(c: &Option<Choice>) -> String {
    c.as_ref().expect("a pick").pnum.clone()
}

pub fn reason(c: &Option<Choice>) -> String {
    c.as_ref().expect("a pick").reason.clone()
}

pub fn tup(target: &str, status: Status, pnum: &str) -> (String, Status, String) {
    (target.to_string(), status, pnum.to_string())
}

/// The synthetic graph and the stubs, built into a fresh Ctx per call:
/// what the `picker` fixture held. `Fx::picker()` stubs the disk reads
/// (no drill bank anywhere, neutral acceptance, every node mature);
/// `Fx::new()` leaves every function real, over a bank under `dir`.
pub struct Fx {
    pub dir: TempDir,
    pub nodes: Nodes,
    pub problems: Problems,
    pub predicted: Problems,
    pub meta: Metadata,
    pub drills: DrillMap,
    pub curve: Option<Curve>,
    pub stubs: Option<Stubs>,
    pub git: Option<crate::git::GitState>,
}

impl Fx {
    pub fn new() -> Fx {
        reset_test_env();
        Fx {
            dir: TempDir::new(),
            nodes: Nodes::new(),
            problems: Problems::new(),
            predicted: Problems::new(),
            meta: Metadata::new(),
            drills: DrillMap::new(),
            curve: load_curve(&repo_root()),
            stubs: None,
            git: None,
        }
    }

    pub fn picker() -> Fx {
        let mut fx = Fx::new();
        fx.stubs = Some(Stubs::default());
        fx
    }

    pub fn stubs(&mut self) -> &mut Stubs {
        self.stubs.get_or_insert_with(Stubs::default)
    }

    /// No fitted curve: SOLID for SOLID_WINDOW_DAYS after a clean rep,
    /// then STALE (kg_lib._load_curve -> None).
    pub fn flat_window(&mut self) -> &mut Fx {
        self.curve = None;
        self
    }

    pub fn nodes(&mut self, ids: &[&str]) -> &mut Fx {
        for id in ids {
            self.nodes.insert(id.to_string(), node(id));
        }
        self
    }

    pub fn prereqs(&mut self, id: &str, prereqs: &[&str]) -> &mut Fx {
        self.nodes.entry(id.to_string()).or_insert_with(|| node(id));
        self.nodes[id].prereqs = strs(prereqs);
        self
    }

    pub fn group(&mut self, ids: &[&str], group: &str) -> &mut Fx {
        for id in ids {
            self.nodes[*id].group = Some(group.to_string());
        }
        self
    }

    pub fn problems(&mut self, ps: Vec<(&str, Problem)>) -> &mut Fx {
        for (k, p) in ps {
            self.problems.insert(k.to_string(), p);
        }
        self
    }

    pub fn problem(&mut self, k: &str, p: Problem) -> &mut Fx {
        self.problems.insert(k.to_string(), p);
        self
    }

    /// A drafted entry in the predicted tier with its metadata difficulty.
    pub fn draft(&mut self, k: &str, p: Problem, difficulty: &str) -> &mut Fx {
        self.predicted.insert(k.to_string(), p);
        self.meta.entry(k.to_string()).or_default().difficulty = Some(difficulty.to_string());
        self
    }

    pub fn acceptance(&mut self, k: &str, pct: f64) -> &mut Fx {
        self.meta.entry(k.to_string()).or_default().acceptance = Some(pct);
        self
    }

    pub fn premium(&mut self, k: &str) -> &mut Fx {
        self.meta.entry(k.to_string()).or_default().paid_only = true;
        self
    }

    /// One bank file under drills/<node>, registered in drills.json as
    /// `did` with its "after" ids (the drill_bank helper).
    pub fn bank(
        &mut self,
        node: &str,
        title: &str,
        fname: &str,
        did: &str,
        after: &[&str],
    ) -> PathBuf {
        let d = self.dir.0.join("drills").join(node);
        std::fs::create_dir_all(&d).unwrap();
        let path = d.join(fname);
        std::fs::write(
            &path,
            format!("\"\"\"\nDRILL: {title}\nTRAINS: {node}\n\"\"\"\n"),
        )
        .unwrap();
        self.drills.insert(
            did.to_string(),
            DrillEntry {
                title: title.to_string(),
                after: strs(after),
                trains: None,
            },
        );
        path
    }

    /// A bank file written by hand, no registry entry.
    pub fn bank_file(&self, node: &str, fname: &str, text: &str) -> PathBuf {
        let d = self.dir.0.join("drills").join(node);
        std::fs::create_dir_all(&d).unwrap();
        let path = d.join(fname);
        std::fs::write(&path, text).unwrap();
        path
    }

    /// drills.json for a bank written by hand: register(d1 = "Lower",
    /// d2 = ("Upper", ["d1"])).
    pub fn register(&mut self, specs: &[(&str, &str, &[&str])]) -> &mut Fx {
        for (did, title, after) in specs {
            self.drills.insert(
                did.to_string(),
                DrillEntry {
                    title: title.to_string(),
                    after: strs(after),
                    trains: None,
                },
            );
        }
        self
    }

    pub fn path(&self, node: &str, fname: &str) -> PathBuf {
        self.dir.0.join("drills").join(node).join(fname)
    }

    pub fn ctx(&self) -> Ctx {
        let ctx = Ctx::synthetic(
            self.dir.0.clone(),
            self.nodes.clone(),
            self.problems.clone(),
            self.predicted.clone(),
            self.drills.clone(),
            self.meta.clone(),
            self.curve.clone(),
        );
        *ctx.stubs.borrow_mut() = self.stubs.clone();
        if let Some(g) = &self.git {
            *ctx.git.borrow_mut() = Some(std::rc::Rc::new(g.clone()));
        }
        ctx
    }

    pub fn pv(&self) -> PView {
        PView::new(self.problems.clone())
    }

    pub fn run(&self, ev: &Evidence, st: &Statuses, args: PickArgs) -> Option<Choice> {
        self.run_pv(ev, st, args).0
    }

    /// pick() and the problem table after it (promotions land there).
    pub fn run_pv(&self, ev: &Evidence, st: &Statuses, args: PickArgs) -> (Option<Choice>, PView) {
        let ctx = self.ctx();
        let pv = RefCell::new(self.pv());
        let c = pick(&ctx, &pv, ev, st, &args);
        (c, pv.into_inner())
    }

    pub fn blocked(
        &self,
        ev: &Evidence,
        st: &Statuses,
        asleep: &[&str],
        exclude: &[&str],
    ) -> Vec<(String, Status, String, bool)> {
        let ctx = self.ctx();
        blocked_frontier(
            &ctx,
            &self.pv(),
            ev,
            st,
            &strs(asleep),
            &set(exclude),
            today(),
        )
    }

    pub fn summits(&self, ev: &Evidence, st: &Statuses) -> Vec<String> {
        let ctx = self.ctx();
        ready_hards(&ctx, &self.pv(), ev, st, None, None, today())
    }
}

pub fn map(pairs: &[(&str, i64)]) -> HashMap<String, i64> {
    pairs.iter().map(|(k, v)| (k.to_string(), *v)).collect()
}

pub fn fmap(pairs: &[(&str, f64)]) -> HashMap<String, f64> {
    pairs.iter().map(|(k, v)| (k.to_string(), *v)).collect()
}
