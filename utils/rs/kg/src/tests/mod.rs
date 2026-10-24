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
mod learning;
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

// The drill ids of the test's bank by title, as Fx registers them: a
// drill rep built by title (drill_rep) or by solved filename (drill_file)
// carries the id the registry gave that title. A title no Fx registered
// gets "t:<title>", the id Fx::bank_file gives a file it registers alone.
thread_local! {
    static TEST_IDS: RefCell<Vec<(String, String)>> = const { RefCell::new(Vec::new()) };
}

fn note_test_id(title: &str, id: &str) {
    TEST_IDS.with(|t| {
        let mut t = t.borrow_mut();
        t.retain(|(k, _)| k != title);
        t.push((title.to_string(), id.to_string()));
    });
}

/// The drill id of a title in the test's registry.
pub fn test_drill_id(title: &str) -> String {
    TEST_IDS.with(|t| {
        t.borrow()
            .iter()
            .find(|(k, _)| k == title)
            .map(|(_, v)| v.clone())
            .unwrap_or_else(|| format!("t:{title}"))
    })
}

/// The drill id of a solved filename: the registered title whose
/// `make solved` stem (d_<Title_With_Underscores>_) the basename starts
/// with, the longest one when two do; else the stem read as a title.
fn test_drill_id_of_fname(fname: &str) -> String {
    let base = fname.rsplit('/').next().unwrap_or(fname).to_lowercase();
    let hit = TEST_IDS.with(|t| {
        t.borrow()
            .iter()
            .filter(|(k, _)| {
                base.starts_with(&format!("d_{}_", crate::ctx::clean_title(k).to_lowercase()))
            })
            .max_by_key(|(k, _)| k.len())
            .map(|(_, v)| v.clone())
    });
    hit.unwrap_or_else(|| {
        let base = fname.rsplit('/').next().unwrap_or(fname);
        let stamp = crate::drills::solved_stamp(base);
        let stem = &base[..base.len() - stamp.len()];
        let stem = stem.trim_end_matches('_');
        let stem = stem.strip_prefix("d_").unwrap_or(stem);
        format!("t:{}", stem.replace('_', " "))
    })
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
        seconds: None,
        learning: false,
        drill: None,
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
    let mut r = rec(iso(days_ago), "drill", &[(node, verdict)], assist);
    r.drill = Some(test_drill_id(title));
    (format!("solved/d_{stem}_{days_ago}.py"), r)
}

/// A drill rep under a solved/ name of the test's own choosing.
pub fn drill_file(fname: &str, node: &str, days_ago: i64, assist: Assist) -> (String, Rec) {
    let mut r = rec(iso(days_ago), "drill", &[(node, "clean")], assist);
    r.drill = Some(test_drill_id_of_fname(fname));
    (fname.to_string(), r)
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
        TEST_IDS.with(|t| t.borrow_mut().clear());
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
        std::fs::write(&path, format!("\"\"\"\n{title}\n\"\"\"\n")).unwrap();
        self.drills.insert(
            did.to_string(),
            DrillEntry {
                title: title.to_string(),
                file: format!("{node}/{fname}"),
                after: strs(after),
                trains: Some(vec![node.to_string()]),
                disabled: false,
            },
        );
        note_test_id(title, did);
        path
    }

    /// A bank file written by hand. Its `DRILL: <title>` and
    /// `TRAINS: <ids>` lines are the fixture's shorthand for a registry
    /// entry: the file is registered as "t:<title>" until `register` gives
    /// the title an id. A text with no DRILL line gets no entry.
    pub fn bank_file(&mut self, node: &str, fname: &str, text: &str) -> PathBuf {
        let d = self.dir.0.join("drills").join(node);
        std::fs::create_dir_all(&d).unwrap();
        let path = d.join(fname);
        std::fs::write(&path, text).unwrap();
        let field = |key: &str| {
            text.lines().find_map(|l| {
                crate::lang::uncomment(l)
                    .strip_prefix(key)
                    .map(|r| r.trim().to_string())
                    .filter(|r| !r.is_empty())
            })
        };
        if let Some(title) = field("DRILL:") {
            let trains =
                field("TRAINS:").map(|t| t.split(',').map(|s| s.trim().to_string()).collect());
            let file = format!("{node}/{fname}");
            // a file written again under a title the registry has keeps
            // its id
            if let Some(e) = self.drills.values_mut().find(|e| e.title == title) {
                e.file = file;
                e.trains = trains;
                return path;
            }
            let id = format!("t:{title}");
            self.drills.insert(
                id.clone(),
                DrillEntry {
                    title: title.clone(),
                    file,
                    after: Vec::new(),
                    trains,
                    disabled: false,
                },
            );
            note_test_id(&title, &id);
        }
        path
    }

    /// Registry entries for bank files no test writes (a stubbed clock's
    /// paths): (file under drills/, title), each as "t:<title>".
    pub fn titled(&mut self, files: &[(&str, &str)]) -> &mut Fx {
        for (file, title) in files {
            let id = format!("t:{title}");
            self.drills.insert(
                id.clone(),
                DrillEntry {
                    title: title.to_string(),
                    file: file.to_string(),
                    after: Vec::new(),
                    trains: None,
                    disabled: false,
                },
            );
            note_test_id(title, &id);
        }
        self
    }

    /// drills.json for a bank written by hand: register(d1 = "Lower",
    /// d2 = ("Upper", ["d1"])).
    pub fn register(&mut self, specs: &[(&str, &str, &[&str])]) -> &mut Fx {
        for (did, title, after) in specs {
            // the file bank_file wrote for this title moves to the id
            let written = self.drills.shift_remove(&format!("t:{title}"));
            self.drills.insert(
                did.to_string(),
                DrillEntry {
                    title: title.to_string(),
                    file: written.as_ref().map(|w| w.file.clone()).unwrap_or_default(),
                    after: strs(after),
                    trains: written.and_then(|w| w.trains),
                    disabled: false,
                },
            );
            note_test_id(title, did);
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

/// Writes data/crowd.json, the counts kg_crowd syncs, into the fixture:
/// one (problem, submissions, likes, dislikes) per row.
pub fn crowd_json(fx: &Fx, rows: &[(&str, i64, i64, i64)]) {
    let mut m = serde_json::Map::new();
    for (p, submissions, likes, dislikes) in rows {
        let s = crate::crowd::Stats {
            submissions: *submissions,
            likes: *likes,
            dislikes: *dislikes,
        };
        m.insert(p.to_string(), crate::crowd::entry("x", s, &iso(0)));
    }
    std::fs::create_dir_all(fx.dir.0.join("data")).unwrap();
    crate::crowd::save(&fx.dir.0, &m).unwrap();
}

/// Writes data/leetcode_ratings.tsv, the ratings the first-sight Elo
/// prices its games with, into the fixture.
pub fn ratings_tsv(fx: &Fx, pairs: &[(&str, f64)]) {
    let dir = fx.dir.0.join("data");
    std::fs::create_dir_all(&dir).unwrap();
    let mut text = String::from("rating\tid\tslug\n");
    for (p, r) in pairs {
        text.push_str(&format!("{r}\t{p}\tx\n"));
    }
    std::fs::write(dir.join("leetcode_ratings.tsv"), text).unwrap();
}

/// data/leetcode_submissions.json under Fx::dir: one accepted submission
/// per (problem, day), the shape make lc-sync writes.
pub fn submissions_json(fx: &Fx, pairs: &[(&str, &str)]) {
    let dir = fx.dir.0.join("data");
    std::fs::create_dir_all(&dir).unwrap();
    let subs: Vec<serde_json::Value> = pairs
        .iter()
        .enumerate()
        .map(|(i, (p, d))| {
            serde_json::json!({
                "id": i + 1, "number": p, "slug": format!("p{p}"), "date": d,
                "timestamp": 0, "lang": "python3"
            })
        })
        .collect();
    let doc = serde_json::json!({"submissions": subs});
    std::fs::write(
        dir.join("leetcode_submissions.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();
}

pub fn map(pairs: &[(&str, i64)]) -> HashMap<String, i64> {
    pairs.iter().map(|(k, v)| (k.to_string(), *v)).collect()
}

pub fn fmap(pairs: &[(&str, f64)]) -> HashMap<String, f64> {
    pairs.iter().map(|(k, v)| (k.to_string(), *v)).collect()
}
