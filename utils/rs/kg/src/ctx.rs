// The run's fixed tables and its clock. Everything the Python picker reads
// from disk once per process lives here: the graph files, the drill
// registry and the bank directory, the metadata, the fitted curve, plus
// the small caches kg_lib keeps for the bank files (headers, titles,
// ids). `today` is a Cell so the replay can freeze it, as
// kg_next.freeze does.

use std::cell::{Cell, RefCell};
use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::rc::Rc;

use chrono::NaiveDate;

use crate::bank::DraftMatrix;
use crate::data::{
    evidenced_view, load_all_problems, load_curve, load_drills, load_metadata, load_nodes,
    pnum_key, predicted_view, real_today, Curve, DrillMap, Metadata, Nodes, Problem, Problems,
};

/// The evidence a node's drill scheduling depends on (Ctx::deps).
pub struct NodeDeps {
    pub nodes: HashSet<String>,
    pub drill_keys: Vec<String>,
    pub problems: HashSet<String>,
}

impl NodeDeps {
    /// Whether a record with these moves / drill basename / problem can
    /// change the node's answers.
    pub fn hit(&self, moves: &[String], base: Option<&str>, problem: Option<&str>) -> bool {
        moves.iter().any(|m| self.nodes.contains(m))
            || base.is_some_and(|b| self.drill_keys.iter().any(|k| b.starts_with(k.as_str())))
            || problem.is_some_and(|p| self.problems.contains(p))
    }
}

pub struct Ctx {
    pub root: PathBuf,
    pub nodes: Nodes,
    /// graph/problems.json, every entry (kg_lib._problems_ro)
    pub ro: PView,
    /// the entries carrying drafted walks (kg_lib.load_predicted)
    pub predicted: Problems,
    pub predicted_view: PView,
    draft: RefCell<Option<(Vec<String>, Rc<DraftMatrix>)>>,
    pub drills: DrillMap,
    pub meta: Metadata,
    pub curve: Option<Curve>,
    today: Cell<NaiveDate>,
    bank_files: RefCell<HashMap<String, Rc<Vec<PathBuf>>>>,
    bank_paths: RefCell<HashMap<String, Rc<Vec<PathBuf>>>>,
    evidence_keys: RefCell<HashMap<PathBuf, String>>,
    drill_headers: RefCell<HashMap<PathBuf, Rc<(Option<String>, Vec<String>)>>>,
    drill_paths: RefCell<Option<HashMap<String, PathBuf>>>,
    drill_ids: RefCell<Option<HashMap<String, String>>>,
    deps: RefCell<HashMap<String, Rc<NodeDeps>>>,
    pub git: RefCell<Option<Rc<crate::git::GitState>>>,
    pub git_prefetch: RefCell<Option<std::thread::JoinHandle<crate::git::GitState>>>,
    pub solve_times: RefCell<Option<Vec<(String, NaiveDate, i64, String)>>>,
    pub ratings: RefCell<Option<HashMap<String, f64>>>,
}

impl Ctx {
    /// The tables, the three big files parsed on threads of their own,
    /// and the evidence records loaded alongside for the caller.
    pub fn load(root: PathBuf) -> (Ctx, Vec<(String, crate::data::Rec)>) {
        let today = match std::env::var("KG_TODAY") {
            Ok(s) if !s.trim().is_empty() => crate::data::parse_date(s.trim()),
            _ => real_today(),
        };
        let (all, meta, evidence) = std::thread::scope(|sc| {
            let r = &root;
            let a = sc.spawn(move || load_all_problems(r));
            let m = sc.spawn(move || load_metadata(r));
            let e = sc.spawn(move || crate::data::load_evidence_recs(r));
            (a.join().unwrap(), m.join().unwrap(), e.join().unwrap())
        });
        let predicted = predicted_view(&all);
        let ctx = Ctx {
            nodes: load_nodes(&root),
            predicted_view: PView::new(predicted.clone()),
            predicted,
            ro: PView::new(all),
            draft: RefCell::new(None),
            drills: load_drills(&root),
            meta,
            curve: load_curve(&root),
            today: Cell::new(today),
            bank_files: RefCell::new(HashMap::new()),
            bank_paths: RefCell::new(HashMap::new()),
            evidence_keys: RefCell::new(HashMap::new()),
            deps: RefCell::new(HashMap::new()),
            git: RefCell::new(None),
            git_prefetch: RefCell::new(None),
            drill_headers: RefCell::new(HashMap::new()),
            drill_paths: RefCell::new(None),
            drill_ids: RefCell::new(None),
            solve_times: RefCell::new(None),
            ratings: RefCell::new(None),
            root,
        };
        (ctx, evidence)
    }

    pub fn today(&self) -> NaiveDate {
        self.today.get()
    }

    pub fn freeze(&self, day: NaiveDate) {
        self.today.set(day);
    }

    pub fn graph_dir(&self) -> PathBuf {
        self.root.join("graph")
    }

    pub fn drills_dir(&self) -> PathBuf {
        self.root.join("drills")
    }

    /// kg_lib.load_problems: the evidenced entries, a fresh copy.
    pub fn evidenced(&self) -> Problems {
        evidenced_view(&self.ro.map)
    }

    /// graph/problems.json, every entry.
    pub fn all_problems(&self) -> &Problems {
        &self.ro.map
    }

    /// kg_lib._draft_matrix: the drafted walks over these node ids, built
    /// once per node order.
    pub fn draft_matrix(&self, node_ids: Vec<String>) -> Rc<DraftMatrix> {
        if let Some((ids, dm)) = self.draft.borrow().as_ref() {
            if *ids == node_ids {
                return dm.clone();
            }
        }
        let dm = Rc::new(DraftMatrix::build(self, &self.predicted, node_ids.clone()));
        *self.draft.borrow_mut() = Some((node_ids, dm.clone()));
        dm
    }

    pub fn node(&self, id: &str) -> Option<&crate::data::Node> {
        self.nodes.get(id)
    }

    pub fn prereqs(&self, id: &str) -> &[String] {
        self.nodes
            .get(id)
            .map(|n| n.prereqs.as_slice())
            .unwrap_or(&[])
    }

    pub fn group_of(&self, id: &str) -> Option<&str> {
        self.nodes.get(id).and_then(|n| n.group.as_deref())
    }

    // ---- metadata -----------------------------------------------------

    /// kg_lib.acceptance: percent, 50.0 when unknown.
    pub fn acceptance(&self, pnum: &str) -> f64 {
        self.meta
            .get(pnum)
            .and_then(|m| m.acceptance)
            .unwrap_or(50.0)
    }

    pub fn paid_only(&self, pnum: &str) -> bool {
        self.meta.get(pnum).is_some_and(|m| m.paid_only)
    }

    /// kg_lib.unservable: banned or paid-only.
    pub fn unservable(&self, pnum: &str, p: &Problem) -> bool {
        p.banned || self.paid_only(pnum)
    }

    /// kg_lib.problem_difficulty: the table first, metadata as fallback.
    pub fn problem_difficulty(&self, pnum: &str, problems: &Problems) -> String {
        if let Some(d) = problems.get(pnum).and_then(|p| p.difficulty.clone()) {
            if !d.is_empty() {
                return d;
            }
        }
        self.meta
            .get(pnum)
            .and_then(|m| m.difficulty.clone())
            .unwrap_or_default()
    }

    pub fn meta_difficulty(&self, pnum: &str) -> String {
        self.meta
            .get(pnum)
            .and_then(|m| m.difficulty.clone())
            .unwrap_or_default()
    }

    pub fn meta_title(&self, pnum: &str) -> Option<String> {
        self.meta.get(pnum).and_then(|m| m.title.clone())
    }

    // ---- the bank directory ----------------------------------------------

    /// kg_lib.bank_files: drills/<node>/*.py in filename order.
    pub fn bank_files(&self, node: &str) -> Rc<Vec<PathBuf>> {
        if let Some(v) = self.bank_files.borrow().get(node) {
            return v.clone();
        }
        let mut out: Vec<PathBuf> = std::fs::read_dir(self.drills_dir().join(node))
            .map(|rd| {
                rd.filter_map(Result::ok)
                    .map(|e| e.path())
                    .filter(|p| p.extension().is_some_and(|x| x == "py"))
                    .filter(|p| {
                        !p.file_name()
                            .and_then(|n| n.to_str())
                            .is_some_and(|n| n.starts_with('.'))
                    })
                    .collect()
            })
            .unwrap_or_default();
        out.sort();
        let out = Rc::new(out);
        self.bank_files
            .borrow_mut()
            .insert(node.to_string(), out.clone());
        out
    }

    pub fn has_drill_bank(&self, node: &str) -> bool {
        !self.bank_files(node).is_empty()
    }

    /// Every node directory under drills/ (glob "*/*.py"), sorted.
    fn all_bank_paths(&self) -> Vec<PathBuf> {
        let mut out = Vec::new();
        if let Ok(rd) = std::fs::read_dir(self.drills_dir()) {
            for e in rd.filter_map(Result::ok) {
                if e.path().is_dir() {
                    if let Some(name) = e.file_name().to_str() {
                        if !name.starts_with('.') {
                            out.extend(self.bank_files(name).iter().cloned());
                        }
                    }
                }
            }
        }
        out.sort();
        out
    }

    /// kg_lib.bank_paths: a node's files in drill-id order, id-less last by
    /// name.
    pub fn bank_paths(&self, node: &str) -> Rc<Vec<PathBuf>> {
        if let Some(v) = self.bank_paths.borrow().get(node) {
            return v.clone();
        }
        let files = Rc::new(self.bank_paths_uncached(node));
        self.bank_paths
            .borrow_mut()
            .insert(node.to_string(), files.clone());
        files
    }

    fn bank_paths_uncached(&self, node: &str) -> Vec<PathBuf> {
        let mut files: Vec<PathBuf> = self.bank_files(node).as_ref().clone();
        files.sort_by_key(|p| {
            let id = self.drill_id(p);
            let n: i64 = id
                .as_deref()
                .and_then(|i| i[1..].parse().ok())
                .unwrap_or(1_000_000_000);
            (
                n,
                p.file_name()
                    .and_then(|s| s.to_str())
                    .unwrap_or("")
                    .to_string(),
            )
        });
        files
    }

    /// kg_lib._drill_header: (DRILL title, TRAINS ids) of a bank file.
    pub fn drill_header(&self, path: &Path) -> Rc<(Option<String>, Vec<String>)> {
        if let Some(h) = self.drill_headers.borrow().get(path) {
            return h.clone();
        }
        let text = std::fs::read_to_string(path).unwrap_or_default();
        let mut title = None;
        let mut trains = Vec::new();
        for line in text.lines() {
            let t = line.trim_start();
            if title.is_none() {
                if let Some(rest) = t.strip_prefix("DRILL:") {
                    // r"^\s*DRILL:\s*(.+)$": at least one character after
                    if !rest.trim_end_matches(['\r']).is_empty() {
                        title = Some(rest.trim().to_string());
                    }
                }
            }
            if trains.is_empty() {
                if let Some(rest) = t.strip_prefix("TRAINS:") {
                    // r"^\s*TRAINS:\s*([a-z0-9\-, ]+)$": the whole rest of the
                    // line must be ids, commas and spaces
                    let rest = rest.trim_start();
                    let body = rest.trim_end_matches(['\r']);
                    if !body.is_empty()
                        && body.chars().all(|c| {
                            c.is_ascii_lowercase() || c.is_ascii_digit() || "-, ".contains(c)
                        })
                    {
                        trains = body
                            .split(',')
                            .map(str::trim)
                            .filter(|s| !s.is_empty())
                            .map(String::from)
                            .collect();
                    }
                }
            }
        }
        let h = Rc::new((title, trains));
        self.drill_headers
            .borrow_mut()
            .insert(path.to_path_buf(), h.clone());
        h
    }

    pub fn drill_title(&self, path: &Path) -> Option<String> {
        self.drill_header(path).0.clone()
    }

    /// kg_lib.drill_solved_stem: the DRILL title cleaned as utils/kg/solved
    /// cleans it (re.sub(r"[^\w\s-]", "") then spaces to underscores).
    pub fn drill_solved_stem(&self, path: &Path) -> String {
        let title = self.drill_title(path).unwrap_or_else(|| {
            path.file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("")
                .to_string()
        });
        let cleaned: String = title
            .chars()
            .filter(|c| c.is_alphanumeric() || *c == '_' || c.is_whitespace() || *c == '-')
            .collect();
        cleaned.trim().replace(' ', "_")
    }

    /// The evidence key prefix of a bank file: "d_<stem>_" lowercased.
    pub fn drill_evidence_key(&self, path: &Path) -> String {
        if let Some(k) = self.evidence_keys.borrow().get(path) {
            return k.clone();
        }
        let k = format!("d_{}_", self.drill_solved_stem(path)).to_lowercase();
        self.evidence_keys
            .borrow_mut()
            .insert(path.to_path_buf(), k.clone());
        k
    }

    /// kg_lib.drill_path: the bank file for a drill id or DRILL title.
    pub fn drill_path(&self, r: &str) -> Option<PathBuf> {
        let title = self
            .drills
            .get(r)
            .map(|d| d.title.clone())
            .unwrap_or_else(|| r.to_string());
        let hit = self
            .drill_paths
            .borrow()
            .as_ref()
            .and_then(|m| m.get(&title).cloned());
        if let Some(p) = hit {
            return Some(p);
        }
        let mut paths: HashMap<String, PathBuf> = HashMap::new();
        for path in self.all_bank_paths() {
            if let Some(t) = self.drill_title(&path) {
                paths.entry(t).or_insert(path);
            }
        }
        let out = paths.get(&title).cloned();
        *self.drill_paths.borrow_mut() = Some(paths);
        out
    }

    /// kg_lib.drill_id: the graph id (d61) of a bank file, by its title.
    pub fn drill_id(&self, path: &Path) -> Option<String> {
        let title = self.drill_title(path)?;
        if self.drill_ids.borrow().is_none() {
            let mut map: HashMap<String, String> = HashMap::new();
            // reversed registry: the first id with a title wins
            for (i, d) in self.drills.iter().rev() {
                map.insert(d.title.clone(), i.clone());
            }
            *self.drill_ids.borrow_mut() = Some(map);
        }
        let ids = self.drill_ids.borrow();
        let i = ids.as_ref().unwrap().get(&title)?;
        if self.drills.get(i).is_some_and(|d| d.title == title) {
            Some(i.clone())
        } else {
            None
        }
    }

    /// kg_lib.drill_after: the ids this drill comes after.
    pub fn drill_after(&self, path: &Path) -> Vec<String> {
        self.drill_id(path)
            .and_then(|i| self.drills.get(&i))
            .map(|d| d.after.clone())
            .unwrap_or_default()
    }

    /// kg_lib.drill_trains: the drills.json "trains" list, else the TRAINS
    /// header.
    pub fn drill_trains(&self, path: &Path) -> Vec<String> {
        if let Some(i) = self.drill_id(path) {
            if let Some(t) = self.drills.get(&i).and_then(|d| d.trains.clone()) {
                return t;
            }
        }
        self.drill_header(path).1.clone()
    }

    /// What a node's drill scheduling reads from the evidence (kg_lib
    /// due_drill, cold_drill, drills_left): its own entries and its files'
    /// TRAINS nodes, the reps of its files and of the drills its files come
    /// after, and the problems its files come after. A record touching
    /// none of these leaves those answers as they were.
    pub fn deps(&self, node: &str) -> Rc<NodeDeps> {
        if let Some(d) = self.deps.borrow().get(node) {
            return d.clone();
        }
        let mut d = NodeDeps {
            nodes: HashSet::from([node.to_string()]),
            drill_keys: Vec::new(),
            problems: HashSet::new(),
        };
        for path in self.bank_paths(node).iter() {
            d.drill_keys.push(self.drill_evidence_key(path));
            d.nodes.extend(self.drill_trains(path));
            for a in self.drill_after(path) {
                match self.vertex_kind(&a, &self.ro.map) {
                    Some("drill") => {
                        if let Some(p) = self.drill_path(&a) {
                            d.drill_keys.push(self.drill_evidence_key(&p));
                        }
                    }
                    Some("node") => {
                        d.nodes.insert(a);
                    }
                    _ => {
                        d.problems.insert(a);
                    }
                }
            }
        }
        let d = Rc::new(d);
        self.deps.borrow_mut().insert(node.to_string(), d.clone());
        d
    }

    /// kg_lib.vertex_kind: what an "after" id names.
    pub fn vertex_kind(&self, vid: &str, problems: &Problems) -> Option<&'static str> {
        if problems.contains_key(vid) {
            return Some("problem");
        }
        if self.drills.contains_key(vid) {
            return Some("drill");
        }
        if self.nodes.contains_key(vid) {
            return Some("node");
        }
        if self.ro.map.contains_key(vid) {
            return Some("problem");
        }
        None
    }
}

/// The evidenced problems as the picker holds them (promotions included),
/// with the one-pass tables kg_lib memoizes per bank: carry kinds, the
/// walks carrying each node, carrier counts. Rebuilt when the table grows.
pub struct PView {
    pub map: Problems,
    /// the in-memory drafted entries of recognition.spot_pool
    pub drafted: HashSet<String>,
    cache: RefCell<PCache>,
}

#[derive(Default)]
struct PCache {
    len: usize,
    carry_kinds: Rc<HashMap<String, HashSet<String>>>,
    walks_carrying: Rc<HashMap<String, Vec<(String, Vec<Vec<String>>)>>>,
    counts: Rc<HashMap<String, i64>>,
}

impl Clone for PView {
    fn clone(&self) -> Self {
        PView {
            map: self.map.clone(),
            drafted: self.drafted.clone(),
            cache: RefCell::new(PCache::default()),
        }
    }
}

impl PView {
    pub fn new(map: Problems) -> PView {
        PView {
            map,
            drafted: HashSet::new(),
            cache: RefCell::new(PCache::default()),
        }
    }

    pub fn get(&self, pnum: &str) -> Option<&Problem> {
        self.map.get(pnum)
    }

    pub fn contains(&self, pnum: &str) -> bool {
        self.map.contains_key(pnum)
    }

    pub fn insert(&mut self, pnum: String, p: Problem) {
        self.map.insert(pnum, p);
    }

    /// Problem numbers in file order.
    pub fn keys(&self) -> Vec<String> {
        self.map.keys().cloned().collect()
    }

    /// Problem numbers sorted by kg_lib.pnum_key.
    pub fn keys_sorted(&self) -> Vec<String> {
        let mut k = self.keys();
        k.sort_by_key(|p| pnum_key(p));
        k
    }

    fn refresh(&self, ctx: &Ctx) {
        let mut c = self.cache.borrow_mut();
        if c.len == self.map.len() && (c.len > 0 || self.map.is_empty()) {
            return;
        }
        let mut kinds: HashMap<String, HashSet<String>> = HashMap::new();
        let mut walks_carrying: HashMap<String, Vec<(String, Vec<Vec<String>>)>> = HashMap::new();
        let mut counts: HashMap<String, i64> = HashMap::new();
        for (pnum, p) in &self.map {
            for m in &p.moves {
                *counts.entry(m.clone()).or_insert(0) += 1;
            }
            if !crate::data::is_numeric_id(pnum) || ctx.unservable(pnum, p) || p.is_hard() {
                continue;
            }
            let mut walks: Vec<Vec<String>> = vec![p.moves.clone()];
            walks.extend(p.alt_walks.iter().cloned());
            let mut seen: HashSet<&str> = HashSet::new();
            for w in &walks {
                for m in w {
                    kinds
                        .entry(m.clone())
                        .or_default()
                        .insert(p.difficulty().to_string());
                    if seen.insert(m.as_str()) {
                        walks_carrying
                            .entry(m.clone())
                            .or_default()
                            .push((pnum.clone(), walks.clone()));
                    }
                }
            }
        }
        *c = PCache {
            len: self.map.len(),
            carry_kinds: Rc::new(kinds),
            walks_carrying: Rc::new(walks_carrying),
            counts: Rc::new(counts),
        };
    }

    /// kg_lib._carry_kinds: node -> difficulties of the real, servable,
    /// non-Hard problems carrying it in any walk.
    pub fn carry_kinds(&self, ctx: &Ctx, node: &str) -> HashSet<String> {
        self.refresh(ctx);
        self.cache
            .borrow()
            .carry_kinds
            .get(node)
            .cloned()
            .unwrap_or_default()
    }

    /// The bar kind of a node without copying its kinds.
    pub fn bar_of(&self, ctx: &Ctx, node: &str) -> (&'static str, i64) {
        self.refresh(ctx);
        let c = self.cache.borrow();
        match c.carry_kinds.get(node) {
            Some(k) => crate::status::bar_of(k),
            None => ("none", 0),
        }
    }

    /// kg_lib._walks_carrying for one node, in bank order.
    pub fn walks_carrying(
        &self,
        ctx: &Ctx,
    ) -> Rc<HashMap<String, Vec<(String, Vec<Vec<String>>)>>> {
        self.refresh(ctx);
        self.cache.borrow().walks_carrying.clone()
    }

    /// kg_lib.carrier_counts: move -> evidenced problems walking it.
    pub fn carrier_counts(&self, ctx: &Ctx) -> Rc<HashMap<String, i64>> {
        self.refresh(ctx);
        self.cache.borrow().counts.clone()
    }
}
