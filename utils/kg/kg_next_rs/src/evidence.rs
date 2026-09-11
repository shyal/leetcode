// graph/evidence.json in memory, with the index kg_lib._EvidenceIndex keeps:
// records grouped by node, by problem and by date, the d_ drill reps, and
// which record is the first rep of its drill (first exposure, scored as
// unaided at the node). Records stay in file order; the replay
// (review_ahead) appends to a copy and the index grows with it.

use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::path::PathBuf;
use std::rc::Rc;

use chrono::NaiveDate;

use crate::data::{parse_date, Rec};

#[derive(Clone, Debug)]
pub struct NodeEntry {
    pub date: NaiveDate,
    pub verdict: String,
    pub assist: String,
    pub idx: usize,
}

/// kg_lib.drill_key: the drill a d_ solved file is a rep of.
pub fn drill_key(fname: &str) -> Option<String> {
    kg_mock::drill_key(fname)
}

pub fn basename(fname: &str) -> &str {
    fname.rsplit('/').next().unwrap_or(fname)
}

#[derive(Clone, Default)]
pub struct Caches {
    /// drill file key ("d_<stem>_") -> indices into `drills`, in order
    drill_reps: HashMap<String, Rc<Vec<usize>>>,
    /// the latest verdict per node (kg_lib.dodged_nodes' memo)
    dodged: Option<HashMap<String, String>>,
    /// kg_lib._NODE_DRILL_HOLD: (node, day) -> (servable cold files, cold files)
    pub cold: HashMap<(String, NaiveDate), (Vec<PathBuf>, Vec<PathBuf>)>,
    /// kg_lib._IMMATURE: (problems len) -> the young nodes
    pub immature: Option<(usize, HashSet<String>)>,
    /// kg_lib.problem_due per problem, every problem with records
    pub problem_due: Option<HashMap<String, Option<(NaiveDate, i64)>>>,
    /// kg_lib.graduation_due per (node, carriers)
    pub graduation: HashMap<(String, i64), Option<(NaiveDate, i64)>>,
    /// kg_lib.node_axes per (node, day, problems len)
    pub axes: HashMap<(String, NaiveDate, usize), crate::status::Axes>,
    /// the nodes whose entries changed since `immature` was computed
    pub immature_dirty: HashSet<String>,
    /// kg_lib.anki_rank per bank file for (day, assisted), plus whether the
    /// file's latest rep was assisted
    pub anki: HashMap<(NaiveDate, bool), Rc<HashMap<PathBuf, Option<crate::drills::AnkiKey>>>>,
    /// kg_lib.due_drill per (node, day, early, assisted)
    pub due_drill: HashMap<(String, NaiveDate, bool, bool), Option<PathBuf>>,
    /// kg_lib.drills_left per (node, early)
    pub drills_left: HashMap<(String, bool), bool>,
    /// the records appended since the drill caches were last checked:
    /// (moves, drill basename, problem). drills::sync_caches drops the
    /// entries a record can have changed (kg_lib recomputes; the answer
    /// is the same).
    pub push_log: Vec<(Vec<String>, Option<String>, Option<String>)>,
}

#[derive(Clone)]
pub struct Evidence {
    pub recs: Vec<(String, Rec)>,
    pub by_fname: HashMap<String, usize>,
    pub by_node: HashMap<String, Vec<NodeEntry>>,
    pub by_problem: HashMap<String, Vec<usize>>,
    pub by_date: HashMap<String, Vec<usize>>,
    /// (date, lowercase basename, record index) of every d_ file
    pub drills: Vec<(String, String, usize)>,
    pub first_reps: HashSet<usize>,
    /// record indices per drill key, file order (the first with a date on
    /// or before a cut is that cut's first rep)
    pub drill_key_order: HashMap<String, Vec<usize>>,
    drills_seen: HashSet<String>,
    version: u64,
    caches: RefCell<Caches>,
}

impl Evidence {
    pub fn new(recs: Vec<(String, Rec)>) -> Evidence {
        let mut ev = Evidence {
            recs: Vec::new(),
            by_fname: HashMap::new(),
            by_node: HashMap::new(),
            by_problem: HashMap::new(),
            by_date: HashMap::new(),
            drills: Vec::new(),
            first_reps: HashSet::new(),
            drill_key_order: HashMap::new(),
            drills_seen: HashSet::new(),
            version: 0,
            caches: RefCell::new(Caches::default()),
        };
        for (f, r) in recs {
            ev.push(f, r);
        }
        ev
    }

    pub fn len(&self) -> usize {
        self.recs.len()
    }

    pub fn is_empty(&self) -> bool {
        self.recs.is_empty()
    }

    pub fn version(&self) -> u64 {
        self.version
    }

    /// Append one record and index it (kg_lib._EvidenceIndex.add).
    pub fn push(&mut self, fname: String, rec: Rec) {
        let idx = self.recs.len();
        let d = parse_date(&rec.date);
        let key = drill_key(&fname);
        let first = key.as_ref().is_some_and(|k| !self.drills_seen.contains(k));
        if let Some(k) = &key {
            self.drill_key_order.entry(k.clone()).or_default().push(idx);
        }
        if first {
            self.drills_seen.insert(key.unwrap());
            self.first_reps.insert(idx);
        }
        for (node, v) in &rec.moves {
            self.by_node
                .entry(node.clone())
                .or_default()
                .push(NodeEntry {
                    date: d,
                    verdict: v.clone(),
                    assist: if first {
                        "none".to_string()
                    } else {
                        rec.assist_for(node).to_string()
                    },
                    idx,
                });
        }
        if let Some(p) = &rec.problem {
            self.by_problem.entry(p.clone()).or_default().push(idx);
        }
        self.by_date.entry(rec.date.clone()).or_default().push(idx);
        let base = basename(&fname).to_lowercase();
        if base.starts_with("d_") {
            self.drills.push((rec.date.clone(), base.clone(), idx));
        }
        self.by_fname.insert(fname.clone(), idx);
        // the caches: what the new record can change is dropped, the rest
        // kept (the Python memos extend the same way, kg_lib._IMMATURE)
        let touched: Vec<String> = rec.moves.keys().cloned().collect();
        let problem = rec.problem.clone();
        let is_drill = base.starts_with("d_");
        self.recs.push((fname, rec));
        self.version += 1;
        let mut c = self.caches.borrow_mut();
        if is_drill {
            let di = self.drills.len() - 1;
            for (key, v) in c.drill_reps.iter_mut() {
                if base.starts_with(key.as_str()) {
                    Rc::make_mut(v).push(di);
                }
            }
        }
        c.dodged = None;
        if is_drill {
            c.anki.clear();
        }
        c.push_log.push((
            touched.clone(),
            if is_drill { Some(base.clone()) } else { None },
            problem.clone(),
        ));
        c.immature_dirty.extend(touched.iter().cloned());
        c.graduation.retain(|(n, _), _| !touched.contains(n));
        c.axes.retain(|(n, _, _), _| !touched.contains(n));
        if let (Some(m), Some(p)) = (c.problem_due.as_mut(), problem) {
            m.remove(&p);
        }
    }

    pub fn rec(&self, idx: usize) -> &Rec {
        &self.recs[idx].1
    }

    pub fn fname(&self, idx: usize) -> &str {
        &self.recs[idx].0
    }

    pub fn node_entries(&self, node: &str) -> &[NodeEntry] {
        self.by_node.get(node).map(Vec::as_slice).unwrap_or(&[])
    }

    /// The problem's records as (date, fname, rec index), file order.
    pub fn problem_recs(&self, pnum: &str) -> Vec<(&str, &str, usize)> {
        self.by_problem
            .get(pnum)
            .map(|v| {
                v.iter()
                    .map(|&i| (self.recs[i].1.date.as_str(), self.recs[i].0.as_str(), i))
                    .collect()
            })
            .unwrap_or_default()
    }

    pub fn date_recs(&self, day: &str) -> &[usize] {
        self.by_date.get(day).map(Vec::as_slice).unwrap_or(&[])
    }

    /// Indices into `drills` of the reps of one bank file: the d_ records
    /// whose basename starts with `key` ("d_<stem>_", lowercase), file order.
    pub fn drill_reps(&self, key: &str) -> Rc<Vec<usize>> {
        let mut c = self.caches.borrow_mut();
        if let Some(v) = c.drill_reps.get(key) {
            return v.clone();
        }
        let v: Vec<usize> = self
            .drills
            .iter()
            .enumerate()
            .filter(|(_, (_, base, _))| base.starts_with(key))
            .map(|(i, _)| i)
            .collect();
        let v = Rc::new(v);
        c.drill_reps.insert(key.to_string(), v.clone());
        v
    }

    /// kg_lib.solved_problems: every problem number with a record.
    pub fn solved_problems(&self) -> HashSet<String> {
        self.by_problem.keys().cloned().collect()
    }

    /// kg_lib.dodged_nodes: nodes whose latest evidence is "avoided", with
    /// the problem it was on.
    pub fn dodged_nodes(&self) -> HashMap<String, String> {
        let mut c = self.caches.borrow_mut();
        if let Some(d) = &c.dodged {
            return d.clone();
        }
        let mut latest: HashMap<&str, ((&str, &str), &str, String)> = HashMap::new();
        for (fname, rec) in &self.recs {
            for (node, verdict) in &rec.moves {
                let key = (rec.date.as_str(), fname.as_str());
                let better = latest.get(node.as_str()).is_none_or(|(k, _, _)| key > *k);
                if better {
                    latest.insert(node, (key, verdict, rec.problem_str()));
                }
            }
        }
        let out: HashMap<String, String> = latest
            .into_iter()
            .filter(|(_, (_, v, _))| *v == "avoided")
            .map(|(n, (_, _, p))| (n.to_string(), p))
            .collect();
        c.dodged = Some(out.clone());
        out
    }

    /// Read-modify access to the per-evidence caches.
    pub fn cold_cache(&self) -> std::cell::RefMut<'_, Caches> {
        self.caches.borrow_mut()
    }

    /// The evidence with only the records dated on or before `cut`, as its
    /// own indexed table (kg_next.due_on's `seen`).
    pub fn up_to(&self, cut: &str) -> Evidence {
        Evidence::new(
            self.recs
                .iter()
                .filter(|(_, r)| r.date.as_str() <= cut)
                .cloned()
                .collect(),
        )
    }
}
