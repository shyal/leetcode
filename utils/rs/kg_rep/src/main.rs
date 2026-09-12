// kg_rep - what do we know about this problem or drill?
//
//   make rep                 # the thing in current.py
//   make rep 1004            # a problem, by number
//   make rep d44             # a drill, by graph id
//   make rep "Paid Orders Per Customer"   # a drill, by DRILL title
//   make rep sql-join-left-keep           # a node: its reps and its bank
//   kg_rep --line            # one line, for the UserPromptSubmit hook
//
// One question, one command: is this a first rep or not, how did the
// earlier reps go, and where do the moves it trains stand. Reading the
// graph by hand for this took several queries every time (2026-09-03).
//
// The first rep of a drill or problem is first exposure to it, whatever
// the status of the nodes it trains: the drill can add a piece none of the
// nodes' earlier drills showed. On "i don't know" at rep 1 the answer is
// given (CLAUDE.md, Coaching).
//
// Ported from utils/kg/kg_rep (Python) on 2026-09-12; the Python was
// deleted once the two agreed on every problem, drill and node.

use std::path::{Path, PathBuf};

use chrono::NaiveDate;
use kg::ctx::{Ctx, PView};
use kg::data::{load_envrc, repo_root, Assist, Rec};
use kg::evidence::Evidence;
use kg::status::{node_axes, node_curve};
use regex::Regex;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Kind {
    Drill,
    Problem,
    Node,
}

/// ("drill", title) or ("problem", number) from the first docstring of
/// current.py; None when it holds neither.
pub fn parse_current(path: &Path) -> Option<(Kind, String)> {
    let content = std::fs::read_to_string(path).ok()?;
    let block = Regex::new(r#"(?s)"""(.*?)""""#).unwrap();
    let body = block.captures(&content)?.get(1)?.as_str().to_string();
    let drill = Regex::new(r"^\**DRILL:\**\s*(.+)").unwrap();
    let problem = Regex::new(r"^(\d+[a-zA-Z]?)\.\s+\S").unwrap();
    for line in body.lines() {
        let line = line.trim();
        if let Some(d) = drill.captures(line) {
            return Some((Kind::Drill, d[1].trim().to_string()));
        }
        if let Some(p) = problem.captures(line) {
            return Some((Kind::Problem, p[1].to_string()));
        }
    }
    None
}

/// os.path.abspath: the working directory joined, "." and ".." folded.
fn abspath(p: &str) -> String {
    let joined = std::path::absolute(p).unwrap_or_else(|_| PathBuf::from(p));
    let mut out = PathBuf::new();
    for c in joined.components() {
        match c {
            std::path::Component::ParentDir => {
                out.pop();
            }
            std::path::Component::CurDir => {}
            other => out.push(other.as_os_str()),
        }
    }
    out.to_string_lossy().into_owned()
}

/// os.path.relpath(path, root).
fn relpath(path: &Path, root: &Path) -> String {
    let p: Vec<_> = path.components().collect();
    let r: Vec<_> = root.components().collect();
    let common = p.iter().zip(&r).take_while(|(a, b)| a == b).count();
    let mut out = PathBuf::new();
    for _ in common..r.len() {
        out.push("..");
    }
    for c in &p[common..] {
        out.push(c.as_os_str());
    }
    if out.as_os_str().is_empty() {
        return ".".to_string();
    }
    out.to_string_lossy().into_owned()
}

/// Resolve a reference: the bank path of a drill, a problem number, a node
/// id; Err(reference) when it is none of those.
fn resolve(
    ctx: &Ctx,
    reference: Option<&str>,
    problems: &PView,
) -> Result<(Kind, String), Option<String>> {
    let Some(r) = reference else {
        return match parse_current(&ctx.root.join("current.py")) {
            Some((Kind::Drill, key)) => Ok((
                Kind::Drill,
                ctx.drill_path(&key)
                    .map(|p| p.to_string_lossy().into_owned())
                    .unwrap_or(key),
            )),
            Some((kind, key)) => Ok((kind, key)),
            None => Err(None),
        };
    };
    if problems.map.contains_key(r) {
        return Ok((Kind::Problem, r.to_string()));
    }
    if ctx.nodes.contains_key(r) {
        return Ok((Kind::Node, r.to_string()));
    }
    if Path::new(r).is_file() {
        return Ok((Kind::Drill, abspath(r)));
    }
    if let Some(p) = ctx.drill_path(r) {
        return Ok((Kind::Drill, p.to_string_lossy().into_owned()));
    }
    Err(Some(r.to_string()))
}

fn basename(path: &str) -> &str {
    path.rsplit('/').next().unwrap_or(path)
}

/// [(date, lowercase basename, record index)] of this bank drill, oldest
/// first.
fn drill_reps<'a>(ctx: &Ctx, path: &str, ev: &'a Evidence) -> Vec<(&'a str, &'a str, usize)> {
    let stem = if Path::new(path).is_file() {
        ctx.drill_solved_stem(Path::new(path))
    } else {
        // a title with no bank file: match on the title alone
        let cleaned: String = basename(path)
            .chars()
            .filter(|c| c.is_alphanumeric() || *c == '_' || c.is_whitespace() || *c == '-')
            .collect();
        cleaned.trim().replace(' ', "_")
    };
    let key = format!("d_{stem}_").to_lowercase();
    let mut reps: Vec<(&str, &str, usize)> = ev
        .drills
        .iter()
        .filter(|(_, base, _)| base.starts_with(&key))
        .map(|(d, base, i)| (d.as_str(), base.as_str(), *i))
        .collect();
    reps.sort_by(|a, b| (a.0, a.1).cmp(&(b.0, b.1)));
    reps
}

fn problem_reps<'a>(pnum: &str, ev: &'a Evidence) -> Vec<(&'a str, &'a str, usize)> {
    let mut reps = ev.problem_recs(pnum);
    reps.sort_by(|a, b| (a.0, a.1).cmp(&(b.0, b.1)));
    reps
}

fn node_line(ctx: &Ctx, node: &str, ev: &Evidence, pv: &PView, today: NaiveDate) -> String {
    let (status, _, _, _) = node_curve(ctx, node, ev, today);
    let ax = node_axes(ctx, node, ev, pv, today);
    let entries = ev.node_entries(node);
    let clean = entries.iter().filter(|e| e.verdict == "clean").count();
    let unaided = entries
        .iter()
        .filter(|e| e.verdict == "clean" && e.assist == "none")
        .count();
    let latest = entries.iter().max_by_key(|e| (e.date, ev.fname(e.idx)));
    let tail = match latest {
        Some(e) => {
            let assist = if e.assist != "none" {
                format!(" ({})", e.assist)
            } else {
                String::new()
            };
            format!(
                "  last {} {}{assist}  {}",
                e.date,
                e.verdict,
                basename(ev.fname(e.idx))
            )
        }
        None => String::new(),
    };
    format!(
        "  {node:<28} {:<8} reps {} (clean {clean}, unaided {unaided})  carriers {}  own {:.2}{tail}",
        status.to_string(),
        entries.len(),
        ax.carriers,
        ax.degree
    )
}

/// kg_lib.assist_tag: one-line rendering of either assist shape.
fn assist_tag(a: &Assist) -> String {
    match a {
        Assist::None => "none".to_string(),
        Assist::Level(s) if s.is_empty() => "none".to_string(),
        Assist::Level(s) => s.clone(),
        Assist::Map(m) if m.is_empty() => "none".to_string(),
        Assist::Map(m) => {
            let mut items: Vec<(&String, &String)> = m.iter().collect();
            items.sort();
            items
                .iter()
                .map(|(k, v)| format!("{k}={v}"))
                .collect::<Vec<_>>()
                .join(", ")
        }
    }
}

fn rep_lines(reps: &[(&str, &str, usize)], ev: &Evidence) -> Vec<String> {
    let mut out = Vec::new();
    for (n, (d, _, idx)) in reps.iter().enumerate() {
        let rec: &Rec = ev.rec(*idx);
        let verdict = if rec.moves.is_empty() {
            "-".to_string()
        } else {
            rec.moves
                .iter()
                .map(|(m, v)| format!("{m}={v}"))
                .collect::<Vec<_>>()
                .join(", ")
        };
        let mut line = format!(
            "  rep {}  {d}  {verdict}  assist {}",
            n + 1,
            assist_tag(&rec.assist)
        );
        if rec.pending.as_deref().is_some_and(|p| !p.is_empty()) {
            line.push_str("  (judge pending)");
        }
        if let Some(note) = rec.note.as_deref().filter(|s| !s.is_empty()) {
            let head: String = note.chars().take(140).collect();
            line.push_str(&format!("\n         {head}"));
        }
        out.push(line);
    }
    out
}

fn first_rep_verdict(n: usize) -> String {
    if n == 0 {
        "FIRST REP: first exposure. On \"i don't know\" give the answer.".to_string()
    } else {
        format!("rep {}: not first exposure. No answer unless asked.", n + 1)
    }
}

fn report_drill(ctx: &Ctx, path: &str, ev: &Evidence, pv: &PView, today: NaiveDate) -> Vec<String> {
    let p = Path::new(path);
    let is_file = p.is_file();
    let reps = drill_reps(ctx, path, ev);
    let title = if is_file {
        ctx.drill_title(p).unwrap_or_else(|| "None".to_string())
    } else {
        basename(path).to_string()
    };
    let did = if is_file { ctx.drill_id(p) } else { None };
    let rel = if is_file {
        relpath(p, &ctx.root)
    } else {
        "(no bank file)".to_string()
    };
    let mut lines = vec![
        format!("drill: {title}  {}  {rel}", did.unwrap_or_default())
            .trim_end()
            .to_string(),
    ];
    let after = if is_file {
        ctx.drill_after(p)
    } else {
        Vec::new()
    };
    if !after.is_empty() {
        lines.push(format!("after: {}", after.join(", ")));
    }
    lines.push(first_rep_verdict(reps.len()));
    lines.extend(rep_lines(&reps, ev));
    let trains = if is_file {
        ctx.drill_trains(p)
    } else {
        Vec::new()
    };
    if !trains.is_empty() {
        lines.push("trains:".to_string());
        lines.extend(trains.iter().map(|n| node_line(ctx, n, ev, pv, today)));
    }
    lines
}

fn report_problem(
    ctx: &Ctx,
    pnum: &str,
    pv: &PView,
    ev: &Evidence,
    today: NaiveDate,
) -> Vec<String> {
    let p = pv.map.get(pnum);
    let reps = problem_reps(pnum, ev);
    let title = p
        .map(|p| p.title.as_str())
        .filter(|t| !t.is_empty())
        .unwrap_or("?");
    let difficulty = p.and_then(|p| p.difficulty.as_deref()).unwrap_or("");
    let mut lines = vec![format!("problem: {pnum}. {title}  {difficulty}")
        .trim_end()
        .to_string()];
    if let Some(after) = p.map(|p| &p.after).filter(|a| !a.is_empty()) {
        lines.push(format!("after: {}", after.join(", ")));
    }
    lines.push(first_rep_verdict(reps.len()));
    lines.extend(rep_lines(&reps, ev));
    if let Some(moves) = p.map(|p| &p.moves).filter(|m| !m.is_empty()) {
        lines.push("moves:".to_string());
        lines.extend(moves.iter().map(|n| node_line(ctx, n, ev, pv, today)));
    }
    lines
}

fn report_node(ctx: &Ctx, node: &str, ev: &Evidence, pv: &PView, today: NaiveDate) -> Vec<String> {
    let mut lines = vec!["node:".to_string(), node_line(ctx, node, ev, pv, today)];
    let bank = ctx.bank_paths(node);
    if !bank.is_empty() {
        lines.push("bank:".to_string());
        for path in bank.iter() {
            let n = drill_reps(ctx, &path.to_string_lossy(), ev).len();
            lines.push(format!("  {:<60} reps {n}", relpath(path, &ctx.root)));
        }
    }
    lines
}

/// The hook line: what current.py holds, its rep number, node statuses.
fn one_line(
    ctx: &Ctx,
    kind: Kind,
    key: &str,
    pv: &PView,
    ev: &Evidence,
    today: NaiveDate,
) -> Option<String> {
    let (reps, nodes, head) = match kind {
        Kind::Drill => {
            let p = Path::new(key);
            let is_file = p.is_file();
            let title = if is_file {
                ctx.drill_title(p).unwrap_or_else(|| "None".to_string())
            } else {
                basename(key).to_string()
            };
            let nodes = if is_file {
                ctx.drill_trains(p)
            } else {
                Vec::new()
            };
            (
                drill_reps(ctx, key, ev),
                nodes,
                format!("drill \"{title}\""),
            )
        }
        Kind::Problem => {
            let nodes = pv.map.get(key).map(|p| p.moves.clone()).unwrap_or_default();
            (problem_reps(key, ev), nodes, format!("problem {key}"))
        }
        Kind::Node => return None,
    };
    let n = reps.len() + 1;
    let rep = if n == 1 {
        "rep 1 = FIRST EXPOSURE, answer on \"i don't know\"".to_string()
    } else {
        format!(
            "rep {n} (last {}), no answer unless asked",
            reps[reps.len() - 1].0
        )
    };
    let st = nodes
        .iter()
        .map(|m| format!("{m} {}", node_curve(ctx, m, ev, today).0))
        .collect::<Vec<_>>()
        .join(", ");
    Some(format!("[current: {head}, {rep} | {st}]"))
}

/// Python's repr() of a str, for the "nothing known" line.
fn py_repr(s: &str) -> String {
    if s.contains('\'') && !s.contains('"') {
        format!("\"{s}\"")
    } else {
        format!("'{}'", s.replace('\\', "\\\\").replace('\'', "\\'"))
    }
}

fn main() {
    let mut line = false;
    let mut refs: Vec<String> = Vec::new();
    for a in std::env::args().skip(1) {
        match a.as_str() {
            "--line" => line = true,
            "-h" | "--help" => {
                println!("usage: kg_rep [--line] [ref ...]\n\n  ref: problem number, drill id/title/path, node id; default current.py\n  --line: one line for the prompt hook");
                return;
            }
            _ => refs.push(a),
        }
    }
    let root = repo_root();
    load_envrc(&root);
    let (ctx, recs) = Ctx::load(root);
    let today = ctx.today();
    let pv = PView::new(ctx.evidenced());
    let ev = Evidence::new(recs);
    let joined = refs.join(" ");
    let reference = if refs.is_empty() {
        None
    } else {
        Some(joined.as_str())
    };
    let resolved = resolve(&ctx, reference, &pv);

    if line {
        if let Ok((kind, key)) = &resolved {
            if let Some(l) = one_line(&ctx, *kind, key, &pv, &ev, today) {
                println!("{l}");
            }
        }
        return;
    }
    let lines = match &resolved {
        Ok((Kind::Drill, key)) => report_drill(&ctx, key, &ev, &pv, today),
        Ok((Kind::Problem, key)) => report_problem(&ctx, key, &pv, &ev, today),
        Ok((Kind::Node, key)) => report_node(&ctx, key, &ev, &pv, today),
        Err(Some(key)) => {
            println!("nothing known for {}", py_repr(key));
            std::process::exit(1);
        }
        Err(None) => {
            println!("current.py holds no problem or drill");
            std::process::exit(1);
        }
    };
    println!("{}", lines.join("\n"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn current_docstring_forms() {
        let dir = std::env::temp_dir().join(format!("kg_rep_test_{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let f = dir.join("current.py");
        std::fs::write(&f, "\"\"\"\n1004. Max Consecutive Ones III\n\"\"\"\n").unwrap();
        assert_eq!(parse_current(&f), Some((Kind::Problem, "1004".to_string())));
        std::fs::write(&f, "\"\"\"\n**DRILL:** Paid Orders Per Customer\n\"\"\"\n").unwrap();
        assert_eq!(
            parse_current(&f),
            Some((Kind::Drill, "Paid Orders Per Customer".to_string()))
        );
        std::fs::write(&f, "x = 1\n").unwrap();
        assert_eq!(parse_current(&f), None);
        std::fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn verdict_lines() {
        assert!(first_rep_verdict(0).starts_with("FIRST REP"));
        assert_eq!(
            first_rep_verdict(2),
            "rep 3: not first exposure. No answer unless asked."
        );
        assert_eq!(py_repr("abc"), "'abc'");
        assert_eq!(py_repr("it's"), "\"it's\"");
    }

    #[test]
    fn relative_paths() {
        assert_eq!(relpath(Path::new("/a/b/c.py"), Path::new("/a")), "b/c.py");
        assert_eq!(
            relpath(Path::new("/x/c.py"), Path::new("/a/b")),
            "../../x/c.py"
        );
    }
}
