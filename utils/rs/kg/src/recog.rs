// The recognition axis (utils/kg/recognition.py) as the picker reads it:
// graph/recognition.json plus what solves and parks say (derived), the
// per-node status (RECOGNIZED / FAILED_TO_RECOGNIZE / UNTESTED), and the
// spot rep due today (due_spot), which `make next` announces as one line.

use std::collections::{HashMap, HashSet};

use chrono::NaiveDate;
use indexmap::IndexMap;

use crate::ctx::{Ctx, PView};
use crate::data::{
    env_str, parse_date, pnum_key, read_json, value_str, Problem, SOLID_WINDOW_DAYS,
};
use crate::evidence::Evidence;
use crate::git::sleep_records;
use crate::status::{gentleness, is_solid, Statuses};

pub const RECOGNIZED: &str = "RECOGNIZED";
pub const FAILED_TO_RECOGNIZE: &str = "FAILED_TO_RECOGNIZE";
pub const UNTESTED: &str = "UNTESTED";
pub const HIT: &str = "hit";
pub const MISSED: &str = "missed";
pub const ALTERNATIVE: &str = "alternative";
pub const LEFT_TO_SOLVES: usize = 2;

#[derive(Clone, Debug, Default)]
pub struct RecogRec {
    pub date: String,
    pub problem: Option<String>,
    pub kind: Option<String>,
    pub moves: IndexMap<String, String>,
}

pub type Recog = IndexMap<String, RecogRec>;

pub fn spot_every() -> i64 {
    env_str("SPOT_EVERY").trim().parse().unwrap_or(3)
}

pub fn load_recognition(ctx: &Ctx) -> Recog {
    let mut out = Recog::new();
    let Some(v) = read_json(&ctx.graph_dir().join("recognition.json")) else {
        return out;
    };
    for (k, r) in v
        .get("recognition")
        .and_then(|r| r.as_object())
        .into_iter()
        .flatten()
    {
        out.insert(
            k.clone(),
            RecogRec {
                date: r
                    .get("date")
                    .and_then(|d| d.as_str())
                    .unwrap_or("")
                    .to_string(),
                problem: r.get("problem").map(value_str),
                kind: r.get("kind").and_then(|d| d.as_str()).map(String::from),
                moves: r
                    .get("moves")
                    .and_then(|m| m.as_object())
                    .map(|o| o.iter().map(|(k, v)| (k.clone(), value_str(v))).collect())
                    .unwrap_or_default(),
            },
        );
    }
    out
}

/// recognition._Index.by_node: (date, verdict, key) per node, same-day
/// ties resolved miss < alternative < hit.
fn by_node(recog: &Recog) -> HashMap<String, Vec<(NaiveDate, String, String)>> {
    let mut out: HashMap<String, Vec<(NaiveDate, String, String)>> = HashMap::new();
    for (key, rec) in recog {
        let d = parse_date(&rec.date);
        for (node, v) in &rec.moves {
            out.entry(node.clone())
                .or_default()
                .push((d, v.clone(), key.clone()));
        }
    }
    let order = |v: &str| match v {
        MISSED => 0,
        ALTERNATIVE => 1,
        HIT => 2,
        _ => 1,
    };
    for v in out.values_mut() {
        v.sort_by(|a, b| (a.0, order(&a.1), &a.2).cmp(&(b.0, order(&b.1), &b.2)));
    }
    out
}

pub fn recognition_window(hits: i64) -> f64 {
    SOLID_WINDOW_DAYS as f64 * 1.3f64.powi((hits - 1).max(0) as i32)
}

/// recognition.recognition_status: (status, last event date).
pub fn recognition_status(
    node: &str,
    recog: &Recog,
    today: NaiveDate,
) -> (&'static str, Option<NaiveDate>) {
    let idx = by_node(recog);
    let Some(events) = idx.get(node) else {
        return (UNTESTED, None);
    };
    if events.is_empty() {
        return (UNTESTED, None);
    }
    let last_date = events[events.len() - 1].0;
    let decided: Vec<&(NaiveDate, String, String)> = events
        .iter()
        .filter(|(_, v, _)| v == HIT || v == MISSED)
        .collect();
    let Some(last) = decided.last() else {
        return (UNTESTED, Some(last_date));
    };
    if last.1 == MISSED {
        return (FAILED_TO_RECOGNIZE, Some(last_date));
    }
    let hits = decided.iter().filter(|(_, v, _)| v == HIT).count() as i64;
    if (today - last.0).num_days() as f64 <= recognition_window(hits) {
        (RECOGNIZED, Some(last_date))
    } else {
        (UNTESTED, Some(last_date))
    }
}

/// The statuses of every node at once (one index build).
pub fn recognition_statuses(
    recog: &Recog,
    nodes: &[String],
    today: NaiveDate,
) -> HashMap<String, (&'static str, Option<NaiveDate>)> {
    let idx = by_node(recog);
    let mut out = HashMap::new();
    for node in nodes {
        let st = match idx.get(node) {
            None => (UNTESTED, None),
            Some(events) if events.is_empty() => (UNTESTED, None),
            Some(events) => {
                let last_date = events[events.len() - 1].0;
                let decided: Vec<&(NaiveDate, String, String)> = events
                    .iter()
                    .filter(|(_, v, _)| v == HIT || v == MISSED)
                    .collect();
                match decided.last() {
                    None => (UNTESTED, Some(last_date)),
                    Some(last) if last.1 == MISSED => (FAILED_TO_RECOGNIZE, Some(last_date)),
                    Some(last) => {
                        let hits = decided.iter().filter(|(_, v, _)| v == HIT).count() as i64;
                        if (today - last.0).num_days() as f64 <= recognition_window(hits) {
                            (RECOGNIZED, Some(last_date))
                        } else {
                            (UNTESTED, Some(last_date))
                        }
                    }
                }
            }
        };
        out.insert(node.clone(), st);
    }
    out
}

pub fn left_to_solves(node: &str, recog: &Recog) -> bool {
    let idx = by_node(recog);
    let Some(events) = idx.get(node) else {
        return false;
    };
    let n = events.len();
    if n < LEFT_TO_SOLVES {
        return false;
    }
    events[n - LEFT_TO_SOLVES..]
        .iter()
        .all(|(_, v, _)| v == ALTERNATIVE)
}

pub fn spotted_problems(recog: &Recog) -> HashSet<String> {
    recog
        .values()
        .filter(|r| r.kind.as_deref() == Some("spot"))
        .filter_map(|r| r.problem.clone())
        .collect()
}

pub fn spots_today(recog: &Recog, today: NaiveDate) -> i64 {
    let t = today.format("%Y-%m-%d").to_string();
    recog
        .values()
        .filter(|r| r.kind.as_deref() == Some("spot") && r.date == t)
        .count() as i64
}

pub fn solves_today(ev: &Evidence, today: NaiveDate) -> i64 {
    ev.date_recs(&today.format("%Y-%m-%d").to_string()).len() as i64
}

pub fn spot_due_by_ratio(recog: &Recog, ev: &Evidence, today: NaiveDate) -> bool {
    let every = spot_every();
    if every <= 0 {
        return false;
    }
    spots_today(recog, today) <= solves_today(ev, today) / every
}

/// recognition.solve_hits: the first unaided all-clean solve of a mapped
/// problem is a hit on every move of its walk.
pub fn solve_hits(ev: &Evidence, pv: &PView) -> Recog {
    let mut out = Recog::new();
    let mut seen: HashSet<String> = HashSet::new();
    for (fname, rec) in &ev.recs {
        let pnum = rec.problem.clone().unwrap_or_default();
        if !seen.insert(pnum.clone()) {
            continue;
        }
        let Some(p) = pv.get(&pnum) else { continue };
        if pnum == "drill"
            || rec.moves.is_empty()
            || rec.moves.values().any(|v| v != "clean")
            || rec.moves.keys().any(|m| rec.assist_for(m) != "none")
        {
            continue;
        }
        let walk: Vec<&String> = p
            .moves
            .iter()
            .filter(|m| rec.moves.contains_key(*m))
            .collect();
        if !walk.is_empty() {
            out.insert(
                format!("{fname}#solve"),
                RecogRec {
                    date: rec.date.clone(),
                    problem: Some(pnum),
                    kind: Some("solve".into()),
                    moves: walk
                        .into_iter()
                        .map(|m| (m.clone(), HIT.to_string()))
                        .collect(),
                },
            );
        }
    }
    out
}

/// recognition.park_misses: a park on an all-SOLID walk is a miss on its
/// moves, dated at the park.
pub fn park_misses(ctx: &Ctx, pv: &PView, ev: &Evidence, statuses: &Statuses) -> Recog {
    let mut out = Recog::new();
    for rec in sleep_records(ctx, pv, ev) {
        let moves = pv
            .get(&rec.pnum)
            .map(|p| p.moves.clone())
            .unwrap_or_default();
        if moves.is_empty() || moves.iter().any(|m| !is_solid(statuses, m)) {
            continue;
        }
        let day = chrono::TimeZone::timestamp_opt(&crate::data::manila(), rec.slept, 0)
            .unwrap()
            .date_naive()
            .format("%Y-%m-%d")
            .to_string();
        out.insert(
            format!("{}#park", rec.branch),
            RecogRec {
                date: day,
                problem: Some(rec.pnum.clone()),
                kind: Some("park".into()),
                moves: moves.into_iter().map(|m| (m, MISSED.to_string())).collect(),
            },
        );
    }
    out
}

/// recognition.derived: stored records plus what solves and parks say.
pub fn derived(ctx: &Ctx, recog: &Recog, ev: &Evidence, pv: &PView, statuses: &Statuses) -> Recog {
    let mut out = solve_hits(ev, pv);
    for (k, v) in park_misses(ctx, pv, ev, statuses) {
        out.insert(k, v);
    }
    for (k, v) in recog {
        out.insert(k.clone(), v.clone());
    }
    out
}

/// recognition.drafted_carriers + spot_pool: the drafted problems never
/// solved as in-memory entries, then the evidenced ones on top.
fn spot_pool(ctx: &Ctx, pv: &PView) -> PView {
    let mut pool: IndexMap<String, Problem> = IndexMap::new();
    for (pnum, v) in &ctx.predicted {
        if pv.contains(pnum) {
            continue;
        }
        if v.walks.len() != 1 || v.walks[0].missing || v.walks[0].moves.is_empty() {
            continue;
        }
        pool.insert(
            pnum.clone(),
            Problem {
                title: v.title.clone(),
                difficulty: Some(ctx.problem_difficulty(pnum, &pv.map)),
                moves: v.walks[0].moves.clone(),
                draft: false,
                ..Default::default()
            },
        );
    }
    let drafted: HashSet<String> = pool.keys().cloned().collect();
    for (k, v) in &pv.map {
        pool.insert(k.clone(), v.clone());
    }
    let mut out = PView::new(pool);
    // the "drafted" flag the ranking reads: kept as a side table
    out.drafted = drafted;
    out
}

/// recognition.carriers_by_node: {node: [carriers]} the way the solve
/// picker counts reach; mapped before drafted, gentlest first.
pub fn carriers_by_node(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    recog: &Recog,
    statuses: &Statuses,
    skip: &HashSet<String>,
) -> HashMap<String, Vec<String>> {
    carriers_by_node_with(ctx, pv, ev, recog, statuses, skip, None)
}

/// carriers_by_node with a tier: only problems of that difficulty carry
/// (`make spot medium`), a rep costing no code.
pub fn carriers_by_node_with(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    recog: &Recog,
    statuses: &Statuses,
    skip: &HashSet<String>,
    difficulty: Option<&str>,
) -> HashMap<String, Vec<String>> {
    let solved = ev.solved_problems();
    let seen = spotted_problems(recog);
    let pool = spot_pool(ctx, pv);
    let mut by_node: HashMap<String, Vec<String>> = HashMap::new();
    for (pnum, p) in &pool.map {
        let moves = &p.moves;
        if solved.contains(pnum)
            || seen.contains(pnum)
            || skip.contains(pnum)
            || ctx.unservable(pnum, p)
            || moves.is_empty()
            || !moves.iter().all(|m| ctx.nodes.contains_key(m))
            || difficulty.is_some_and(|d| p.difficulty.as_deref() != Some(d))
        {
            continue;
        }
        let gaps: Vec<&String> = moves.iter().filter(|m| !is_solid(statuses, m)).collect();
        if gaps.len() > 1 {
            continue;
        }
        let targets: Vec<String> = if gaps.is_empty() {
            let mut s: Vec<String> = moves
                .iter()
                .cloned()
                .collect::<HashSet<_>>()
                .into_iter()
                .collect();
            s.sort();
            s
        } else {
            gaps.into_iter().cloned().collect()
        };
        for n in targets {
            by_node.entry(n).or_default().push(pnum.clone());
        }
    }
    for v in by_node.values_mut() {
        v.sort_by(|a, b| {
            (
                pool.drafted.contains(a),
                gentleness(ctx, a, &pool),
                pnum_key(a),
            )
                .cmp(&(
                    pool.drafted.contains(b),
                    gentleness(ctx, b, &pool),
                    pnum_key(b),
                ))
        });
    }
    by_node
}

/// recognition.due_spot: (target, pnum, reason) for the spot rep due today.
pub fn due_spot(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    recog: &Recog,
    statuses: &Statuses,
    today: NaiveDate,
    skip: &HashSet<String>,
) -> Option<(String, String, String)> {
    due_spot_with(ctx, pv, ev, recog, statuses, today, skip, false, None)
}

/// due_spot with `force` (make spot: the SPOT_EVERY ratio skipped) and a
/// difficulty tier for the carrier.
#[allow(clippy::too_many_arguments)]
pub fn due_spot_with(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    recog: &Recog,
    statuses: &Statuses,
    today: NaiveDate,
    skip: &HashSet<String>,
    force: bool,
    difficulty: Option<&str>,
) -> Option<(String, String, String)> {
    if !force && !spot_due_by_ratio(recog, ev, today) {
        return None;
    }
    let carriers = carriers_by_node_with(ctx, pv, ev, recog, statuses, skip, difficulty);
    let mut ranked: Vec<(bool, i64, NaiveDate, String)> = Vec::new();
    for (n, cs) in &carriers {
        let (status, last) = recognition_status(n, recog, today);
        if status == RECOGNIZED || left_to_solves(n, recog) {
            continue;
        }
        ranked.push((
            status != FAILED_TO_RECOGNIZE,
            -(cs.len() as i64),
            last.unwrap_or(NaiveDate::MIN),
            n.clone(),
        ));
    }
    let (_, _, _, n) = ranked.into_iter().min()?;
    let status = recognition_status(&n, recog, today).0;
    let why = if status == FAILED_TO_RECOGNIZE {
        "failed to recognize last time"
    } else {
        "untested"
    };
    let cs = &carriers[&n];
    Some((
        n.clone(),
        cs[0].clone(),
        format!("{why}, {} problem(s) need only it", cs.len()),
    ))
}

/// recognition.reveal: the lines `make solved` prints after a spot rep is
/// judged, from the raw graph/recognition.json record.
pub fn reveal(rec: &serde_json::Value) -> String {
    use serde_json::Value;
    let text = |k: &str| rec.get(k).and_then(Value::as_str).unwrap_or("").to_string();
    let list = |k: &str| -> Vec<String> {
        rec.get(k)
            .and_then(Value::as_array)
            .map(|a| a.iter().map(crate::data::value_str).collect())
            .unwrap_or_default()
    };
    let title = text("title");
    let pnum = rec
        .get("problem")
        .map(crate::data::value_str)
        .unwrap_or_else(|| "?".to_string());
    let walk = list("walk");
    let walk = if walk.is_empty() {
        "(unmapped)".to_string()
    } else {
        walk.join(", ")
    };
    let moves = rec.get("moves").and_then(Value::as_object);
    let mut verdict = if moves.is_some_and(|m| m.values().any(|v| v.as_str() == Some(MISSED))) {
        "missed".to_string()
    } else {
        "hit".to_string()
    };
    let target = rec.get("target").and_then(Value::as_str);
    if let Some(t) = target {
        if moves.and_then(|m| m.get(t)).and_then(Value::as_str) == Some(ALTERNATIVE) {
            verdict = format!("hit, {t} not needed");
        }
    }
    let seconds = rec
        .get("seconds")
        .map(crate::data::value_str)
        .unwrap_or_else(|| "0".to_string());
    let mut lines = vec![format!("{pnum}. {title}")];
    if rec.get("valid") == Some(&Value::Bool(false)) {
        // a failed route reveals nothing: not the walk, not which named
        // moves fall outside it. The problem stays there to solve cold.
        lines.push(format!(
            "the route as written does not solve it ({verdict} on the target, {seconds}s); the walk stays hidden"
        ));
        if !text("why").is_empty() {
            lines.push(text("why"));
        }
        if !list("named").is_empty() {
            lines.push(format!("named: {}", list("named").join(", ")));
        }
        if let Some(t) = target {
            lines.push(format!("served for: {t}"));
        }
        return lines.join("\n");
    }
    lines.push(format!("walk: {walk}"));
    lines.push(format!("{verdict} in {seconds}s"));
    if !list("alternative").is_empty() {
        lines.push(format!(
            "hit through an alternative walk, not yet evidenced by code: {}",
            list("alternative").join(", ")
        ));
        if !text("why").is_empty() {
            lines.push(text("why"));
        }
    }
    if !list("named").is_empty() {
        lines.push(format!("named: {}", list("named").join(", ")));
    }
    if !list("false").is_empty() {
        lines.push(format!(
            "named but not in any walk: {}",
            list("false").join(", ")
        ));
    }
    if !text("summary").is_empty() {
        lines.push(text("summary"));
    }
    let reason = text("reason");
    if target.is_some() || !reason.is_empty() {
        let served = target.unwrap_or("chosen by hand");
        let why = if reason.is_empty() {
            String::new()
        } else {
            format!(" ({reason})")
        };
        lines.push(format!("served for: {served}{why}"));
    }
    lines.join("\n")
}

/// recognition.load_spot_meta / save_spot_meta: .spot.json, branch -> pick.
pub fn load_spot_meta(root: &std::path::Path) -> serde_json::Value {
    crate::pyjson::load(&root.join(".spot.json"))
        .filter(serde_json::Value::is_object)
        .unwrap_or_else(|| serde_json::json!({}))
}

pub fn save_spot_meta(root: &std::path::Path, meta: &serde_json::Value) -> std::io::Result<()> {
    crate::pyjson::save(&root.join(".spot.json"), meta, Some(2))
}

/// recognition.load_recognition, raw: the records of graph/recognition.json.
pub fn load_recognition_raw(root: &std::path::Path) -> serde_json::Value {
    crate::pyjson::load(&root.join("graph/recognition.json"))
        .and_then(|v| v.get("recognition").cloned())
        .filter(serde_json::Value::is_object)
        .unwrap_or_else(|| serde_json::json!({}))
}

// ---- the statement ---------------------------------------------------------

/// recognition._MD: LeetCode's statement HTML as markdown - emphasis, code,
/// lists, images, superscripts and example blocks kept; everything else is
/// text. A small tag tokenizer stands in for html.parser.HTMLParser.
struct Md {
    out: Vec<String>,
    pending: Vec<&'static str>,
    pre: i32,
    list_stack: Vec<i32>,
    cell: Option<Vec<String>>,
    row: Option<Vec<String>>,
    table: Option<Vec<Vec<String>>>,
}

const BLOCK_TAGS: [&str; 11] = [
    "p",
    "div",
    "ul",
    "ol",
    "pre",
    "table",
    "tr",
    "h1",
    "h2",
    "h3",
    "blockquote",
];

impl Md {
    fn new() -> Md {
        Md {
            out: vec![],
            pending: vec![],
            pre: 0,
            list_stack: vec![],
            cell: None,
            row: None,
            table: None,
        }
    }

    fn sink(&mut self) -> &mut Vec<String> {
        match self.cell.as_mut() {
            Some(c) => c,
            None => &mut self.out,
        }
    }

    fn emit(&mut self, s: &str) {
        self.sink().push(s.to_string());
    }

    fn open_mark(&mut self, mark: &'static str) {
        if self.pre > 0 {
            return;
        }
        self.pending.push(mark);
    }

    fn close_mark(&mut self, mark: &'static str) {
        if self.pre > 0 {
            return;
        }
        if self.pending.last() == Some(&mark) {
            self.pending.pop(); // empty element: nothing to mark
            return;
        }
        let sink = self.sink();
        match sink.last() {
            Some(last) if !last.trim().is_empty() && *last != last.trim_end() => {
                let body = last.trim_end().to_string();
                let tail = last[body.len()..].to_string();
                let n = sink.len();
                sink[n - 1] = body;
                sink.push(format!("{mark}{tail}"));
            }
            _ => sink.push(mark.to_string()),
        }
    }

    fn data(&mut self, data: &str) {
        if self.pre > 0 {
            self.emit(data);
            return;
        }
        // re.sub(r"[ \t\r\n]+", " ", data)
        let mut collapsed = String::new();
        let mut in_ws = false;
        for c in data.chars() {
            if matches!(c, ' ' | '\t' | '\r' | '\n') {
                if !in_ws {
                    collapsed.push(' ');
                }
                in_ws = true;
            } else {
                collapsed.push(c);
                in_ws = false;
            }
        }
        let mut data = collapsed;
        if !self.pending.is_empty() && !data.trim().is_empty() {
            let stripped = data.trim_start().to_string();
            let mut lead = data[..data.len() - stripped.len()].to_string();
            if self
                .sink()
                .last()
                .is_some_and(|l| l.chars().last().is_some_and(char::is_whitespace))
            {
                lead.clear(); // the text before the marker already ends in one
            }
            let marks = self.pending.join("");
            self.emit(&format!("{lead}{marks}"));
            self.pending.clear();
            data = stripped;
        }
        self.emit(&data);
    }

    fn start(&mut self, tag: &str, attrs: &HashMap<String, String>) {
        match tag {
            "pre" => {
                self.pre += 1;
                self.emit("\n```\n");
            }
            "strong" | "b" => self.open_mark("**"),
            "em" | "i" => self.open_mark("*"),
            "code" => self.open_mark("`"),
            "sup" => self.emit("^"),
            "br" => self.emit("\n"),
            "img" => {
                let alt = attrs.get("alt").cloned().unwrap_or_default();
                let src = attrs.get("src").cloned().unwrap_or_default();
                self.emit(&format!("\n![{alt}]({src})\n"));
            }
            "ul" | "ol" => {
                if self.list_stack.is_empty() {
                    self.emit("\n");
                }
                self.list_stack.push(0);
            }
            "li" => {
                let depth = self.list_stack.len();
                if let Some(last) = self.list_stack.last_mut() {
                    *last += 1;
                }
                self.emit(&format!("\n{}- ", "  ".repeat(depth.saturating_sub(1))));
            }
            "table" => self.table = Some(vec![]),
            "tr" => self.row = Some(vec![]),
            "td" | "th" => self.cell = Some(vec![]),
            t if BLOCK_TAGS.contains(&t) => self.emit("\n"),
            _ => {}
        }
    }

    fn end(&mut self, tag: &str) {
        match tag {
            "pre" => {
                self.pre -= 1;
                self.emit("\n```\n");
            }
            "strong" | "b" => self.close_mark("**"),
            "em" | "i" => self.close_mark("*"),
            "code" => self.close_mark("`"),
            "ul" | "ol" => {
                self.list_stack.pop();
                if self.list_stack.is_empty() {
                    self.emit("\n");
                }
            }
            "td" | "th" => {
                if let Some(cell) = self.cell.take() {
                    let text = cell.concat().trim().replace('\n', " ");
                    if let Some(row) = self.row.as_mut() {
                        row.push(text);
                    }
                }
            }
            "tr" => {
                if let (Some(table), Some(row)) = (self.table.as_mut(), self.row.take()) {
                    table.push(row);
                }
                self.row = None;
            }
            "table" => {
                let rows = self.table.take().unwrap_or_default();
                if !rows.is_empty() {
                    let width = rows.iter().map(Vec::len).max().unwrap_or(0);
                    let rows: Vec<Vec<String>> = rows
                        .into_iter()
                        .map(|mut r| {
                            r.resize(width, String::new());
                            r
                        })
                        .collect();
                    let mut lines = vec![
                        format!("| {} |", rows[0].join(" | ")),
                        format!("|{}", "---|".repeat(width)),
                    ];
                    lines.extend(rows[1..].iter().map(|r| format!("| {} |", r.join(" | "))));
                    self.out.push(format!("\n{}\n", lines.join("\n")));
                }
            }
            "p" | "div" | "h1" | "h2" | "h3" | "blockquote" => self.emit("\n"),
            _ => {}
        }
    }

    fn text(&self) -> String {
        let s = self.out.concat().replace('\u{a0}', " ");
        // [ \t]+\n -> \n ; \n (?=\S) -> \n ; ```\n\n+ -> ```\n ; \n\n+``` -> \n``` ; \n{3,} -> \n\n
        let re1 = regex::Regex::new(r"[ \t]+\n").unwrap();
        let re2 = regex::Regex::new(r"\n (\S)").unwrap();
        let re3 = regex::Regex::new(r"```\n\n+").unwrap();
        let re4 = regex::Regex::new(r"\n\n+```").unwrap();
        let re5 = regex::Regex::new(r"\n{3,}").unwrap();
        let s = re1.replace_all(&s, "\n");
        let s = re2.replace_all(&s, "\n$1");
        let s = re3.replace_all(&s, "```\n");
        let s = re4.replace_all(&s, "\n```");
        let s = re5.replace_all(&s, "\n\n");
        format!("{}\n", s.trim())
    }
}

/// html.parser's character reference decoding for the entities LeetCode
/// statements use.
fn unescape(s: &str) -> String {
    if !s.contains('&') {
        return s.to_string();
    }
    let mut out = String::new();
    let mut rest = s;
    while let Some(i) = rest.find('&') {
        out.push_str(&rest[..i]);
        let tail = &rest[i..];
        let Some(end) = tail.find(';') else {
            out.push_str(tail);
            return out;
        };
        let name = &tail[1..end];
        let decoded: Option<String> = match name {
            "lt" => Some("<".into()),
            "gt" => Some(">".into()),
            "amp" => Some("&".into()),
            "quot" => Some("\"".into()),
            "apos" | "#39" => Some("'".into()),
            "nbsp" => Some("\u{a0}".into()),
            "le" => Some("\u{2264}".into()),
            "ge" => Some("\u{2265}".into()),
            "ne" => Some("\u{2260}".into()),
            "hellip" => Some("\u{2026}".into()),
            "ndash" => Some("\u{2013}".into()),
            "mdash" => Some("\u{2014}".into()),
            "rarr" => Some("\u{2192}".into()),
            "larr" => Some("\u{2190}".into()),
            "times" => Some("\u{d7}".into()),
            "minus" => Some("\u{2212}".into()),
            n if n.starts_with("#x") || n.starts_with("#X") => u32::from_str_radix(&n[2..], 16)
                .ok()
                .and_then(char::from_u32)
                .map(String::from),
            n if n.starts_with('#') => n[1..]
                .parse::<u32>()
                .ok()
                .and_then(char::from_u32)
                .map(String::from),
            _ => None,
        };
        match decoded {
            Some(d) => {
                out.push_str(&d);
                rest = &tail[end + 1..];
            }
            None => {
                out.push('&');
                rest = &tail[1..];
            }
        }
    }
    out.push_str(rest);
    out
}

/// recognition.html_to_markdown.
pub fn html_to_markdown(html: &str) -> String {
    let mut md = Md::new();
    let mut rest = html;
    let attr_re = regex::Regex::new(
        r#"([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))"#,
    )
    .unwrap();
    while !rest.is_empty() {
        let Some(lt) = rest.find('<') else {
            md.data(&unescape(rest));
            break;
        };
        if lt > 0 {
            md.data(&unescape(&rest[..lt]));
        }
        let tail = &rest[lt..];
        if tail.starts_with("<!--") {
            match tail.find("-->") {
                Some(e) => rest = &tail[e + 3..],
                None => break,
            }
            continue;
        }
        let Some(gt) = tail.find('>') else {
            md.data(&unescape(tail));
            break;
        };
        let inner = tail[1..gt].trim();
        rest = &tail[gt + 1..];
        if let Some(name) = inner.strip_prefix('/') {
            md.end(&name.trim().to_lowercase());
            continue;
        }
        let self_closing = inner.ends_with('/');
        let inner = inner.trim_end_matches('/').trim();
        let (name, attr_text) = inner.split_once(char::is_whitespace).unwrap_or((inner, ""));
        let name = name.to_lowercase();
        let mut attrs: HashMap<String, String> = HashMap::new();

        for c in attr_re.captures_iter(attr_text) {
            let v = c
                .get(2)
                .or(c.get(3))
                .or(c.get(4))
                .map(|m| m.as_str())
                .unwrap_or("");
            attrs.insert(c[1].to_lowercase(), unescape(v));
        }
        md.start(&name, &attrs);
        if self_closing {
            md.end(&name);
        }
    }
    md.text()
}

/// recognition.fetch_content: LeetCode's statement HTML for a problem, with
/// title, slug and difficulty; cached in .prepare_cache/<num>.content.json.
pub fn fetch_content(root: &std::path::Path, num: &str) -> Result<serde_json::Value, String> {
    let cache = root
        .join(".prepare_cache")
        .join(format!("{num}.content.json"));
    if let Some(v) = crate::pyjson::load(&cache) {
        return Ok(v);
    }
    let url = "https://leetcode.com/graphql/";
    let post = |body: serde_json::Value| -> Result<serde_json::Value, String> {
        let mut resp = ureq::post(url)
            .header("Content-Type", "application/json")
            .send_json(&body)
            .map_err(|e| e.to_string())?;
        resp.body_mut()
            .read_json::<serde_json::Value>()
            .map_err(|e| e.to_string())
    };
    let q1 = "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n      problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {\n        questions: data { difficulty frontendQuestionId: questionFrontendId paidOnly: isPaidOnly title titleSlug }\n      }\n    }";
    let skip: i64 = num
        .parse::<i64>()
        .map_err(|_| format!("bad number {num}"))?
        - 1;
    let r = post(
        serde_json::json!({"query": q1, "variables": {"categorySlug": "", "limit": 1, "skip": skip, "filters": {}}}),
    )?;
    let qs = r["data"]["problemsetQuestionList"]["questions"]
        .as_array()
        .cloned()
        .unwrap_or_default();
    let q = match qs.first() {
        Some(q) if q["frontendQuestionId"].as_str() == Some(num) => q.clone(),
        _ => return Err(format!("no question found for number {num}")),
    };
    if q["paidOnly"].as_bool() == Some(true) {
        return Err(format!("question {num} is paid only"));
    }
    let q2 = "\n    query questionDetails($titleSlug: String!) {\n      question(titleSlug: $titleSlug) { content }\n    }";
    let r = post(serde_json::json!({"query": q2, "variables": {"titleSlug": q["titleSlug"]}}))?;
    let entry = serde_json::json!({
        "title": q["title"],
        "slug": q["titleSlug"],
        "difficulty": q["difficulty"],
        "content": r["data"]["question"]["content"],
    });
    let _ = std::fs::create_dir_all(root.join(".prepare_cache"));
    crate::pyjson::save(&cache, &entry, None).map_err(|e| e.to_string())?;
    Ok(entry)
}

/// recognition.spot_document: current.md for a spot rep.
pub fn spot_document(markdown: &str) -> String {
    format!("{}\n\n<!-- answer -->\n---\n\n", markdown.trim_end())
}
