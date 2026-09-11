// kg_next (Rust): deterministically pick the next problem from the
// technique graph and draw its input tree. The rules and the output are
// utils/kg/kg_next's; utils/tests/test_next_parity.py runs both over the
// real graph/ data and diffs them, so the two cannot drift apart. `make
// next` runs this binary; the Python file stays as the reference and the
// home of the rule comments.
//
//   kg_next              # pick, print the panel, draw the tree
//   kg_next --graph      # label tree nodes with move names
//   kg_next --no-show    # skip the drawing
//   kg_next --why        # with nothing to serve, table the blocked moves
//   kg_next sql 2        # group and rank, makefile form
//   kg_next --golden-json  # the library values the parity test diffs
//
// KG_SEED=<n> seeds the status faces like random.seed(n) does on the
// Python side; KG_TODAY=YYYY-MM-DD freezes the day (kg_next.freeze).
#![allow(clippy::too_many_arguments)]

use std::cell::RefCell;
use std::collections::HashSet;
use std::process::Command;

use chrono::NaiveDate;
use kg_mock::PyRandom;
use serde_json::Value;

use kg_next::clock::{last_attempt, problem_due};
use kg_next::console::{Console, Line};
use kg_next::ctx::{Ctx, PView};
use kg_next::data::{load_envrc, repo_root};
use kg_next::drills::{
    anki, anki_due, anki_frontier, cold_drill, drill_held, drill_recall, drill_review_cap,
    drill_reviews_today, due_drill, group_caps, group_reps, new_drill_cap, new_drills_today,
    reviews_first,
};
use kg_next::evidence::Evidence;
use kg_next::git::{
    is_session_start, is_stale, pending_judgements, sleep_rows, sleep_state, solve_seconds_today,
    solved_today_pnums, spawn_judge,
};
use kg_next::model::{drill_forecast, elo_now, solve_forecast, solve_ratings};
use kg_next::pick::{
    blocked_frontier, park_full_lines, parked_summits, pick, review_ahead, review_line,
    review_queue, starved, unmapped_summits, withheld, Choice, PickArgs,
};
use kg_next::recog;
use kg_next::render::{
    animate, degree_color, display, faces, prespawn_dot, render_in_background, Dot, PreDot,
};
use kg_next::status::{
    all_statuses, carry_bar, immature_nodes, input_tree, node_axes, node_degree, owned, st, Status,
    Statuses, FRAGILE, MISSING, SOLID, STALE,
};
use kg_next::table::{columns, panel, BoxKind, Table};

mod golden;

/// KG_TRACE=1: elapsed milliseconds at each phase, on stderr.
fn trace(label: &str) {
    use std::sync::OnceLock;
    use std::time::Instant;
    static T0: OnceLock<Instant> = OnceLock::new();
    let t0 = T0.get_or_init(Instant::now);
    if std::env::var_os("KG_TRACE").is_some() {
        eprintln!("[{:>6.1} ms] {label}", t0.elapsed().as_secs_f64() * 1000.0);
    }
}

thread_local! {
    static RNG: RefCell<Option<PyRandom>> = const { RefCell::new(None) };
}

/// The face stream: random.seed(KG_SEED) when set (the parity test), else
/// seeded by the day and the pick, so a `make next` run again shows the
/// same faces on the same pick and the drawing is not laid out twice.
fn seed_faces(today: NaiveDate, pick: &str) {
    let seed = std::env::var("KG_SEED")
        .ok()
        .and_then(|s| s.trim().parse::<u32>().ok())
        .unwrap_or_else(|| {
            let mut h: u32 = 2166136261;
            for b in format!("{today}|{pick}").bytes() {
                h ^= b as u32;
                h = h.wrapping_mul(16777619);
            }
            h
        });
    RNG.with(|r| *r.borrow_mut() = Some(PyRandom::new(seed)));
}

/// random.choice over a status's face pool.
fn face(status: Status) -> &'static str {
    let pool = faces(status);
    let i = RNG.with(|r| {
        r.borrow_mut()
            .get_or_insert_with(|| PyRandom::new(0))
            .randbelow(pool.len() as u32)
    }) as usize;
    pool[i]
}

fn status_style(s: Status) -> &'static str {
    match s {
        SOLID => "green",
        STALE => "yellow",
        FRAGILE => "red",
        MISSING => "dim",
    }
}

fn styled_status(s: Status) -> String {
    let st = status_style(s);
    format!("[{st}]{s}[/{st}]")
}

fn review_note(label: &str) -> &'static str {
    match label {
        "failed" => "you walked away from this one",
        "learning" => "the solution was given and copied",
        "walkthrough" => "the shape was talked through before the code existed",
        "hint" => "you took a hint",
        "struggled" => "a move on it was marked struggled",
        _ => "",
    }
}

struct Args {
    n: usize,
    group: Option<String>,
    graph: bool,
    no_show: bool,
    why: bool,
    cram: bool,
    early: bool,
    assisted: bool,
    prepare: bool,
    golden: bool,
}

fn usage_error(msg: &str) -> ! {
    eprintln!("usage: kg_next [-h] [--graph] [--no-show] [--why] [--group GROUP] [--cram] [--early] [--assisted] [--prepare] [WORD ...]");
    eprintln!("kg_next: error: {msg}");
    std::process::exit(2);
}

fn parse_args(ctx: &Ctx) -> Args {
    let mut a = Args {
        n: 1,
        group: None,
        graph: false,
        no_show: false,
        why: false,
        cram: false,
        early: false,
        assisted: false,
        prepare: false,
        golden: false,
    };
    let groups: HashSet<String> = ctx.nodes.values().filter_map(|n| n.group.clone()).collect();
    let mut it = std::env::args().skip(1);
    while let Some(w) = it.next() {
        match w.as_str() {
            "--graph" => a.graph = true,
            "--no-show" => a.no_show = true,
            "--why" => a.why = true,
            "--cram" => a.cram = true,
            "--early" => a.early = true,
            "--assisted" => a.assisted = true,
            "--prepare" => a.prepare = true,
            "--golden-json" => a.golden = true,
            "--group" => {
                a.group = Some(
                    it.next()
                        .unwrap_or_else(|| usage_error("argument --group: expected one argument")),
                )
            }
            "-h" | "--help" => {
                println!("usage: kg_next [--graph] [--no-show] [--why] [--group GROUP] [--cram] [--early] [--assisted] [--prepare] [WORD ...]");
                std::process::exit(0);
            }
            _ if w.starts_with("--group=") => a.group = Some(w["--group=".len()..].to_string()),
            _ if w.starts_with('-') && w.len() > 1 => {
                usage_error(&format!("unrecognized arguments: {w}"))
            }
            _ => {
                if !w.is_empty() && w.chars().all(|c| c.is_ascii_digit()) {
                    a.n = w.parse().unwrap_or(1);
                } else if groups.contains(&w) {
                    a.group = Some(w.clone());
                } else {
                    let mut g: Vec<&String> = groups.iter().collect();
                    g.sort();
                    let listed: Vec<&str> = g.iter().map(|s| s.as_str()).collect();
                    usage_error(&format!(
                        "'{w}' is not a number or a group ({})",
                        listed.join(", ")
                    ));
                }
            }
        }
    }
    a
}

fn plain_table(columns: &[&str], title: Option<&str>) -> Table {
    Table::plain(columns, title, BoxKind::Rounded)
}

fn head_table() -> Table {
    Table::plain(
        &["Move", "Status", "Maturity", "Own", "Last evidence"],
        None,
        BoxKind::SimpleHead,
    )
}

fn problem_url(ctx: &Ctx, pnum: &str) -> String {
    match ctx.meta.get(pnum).and_then(|m| m.slug.clone()) {
        Some(slug) => format!("https://leetcode.com/problems/{slug}/"),
        None => format!("https://leetcode.com/problemset/?search={pnum}"),
    }
}

fn difficulty_line(ctx: &Ctx, pnum: &str, pv: &PView) -> Option<String> {
    let diff = ctx.problem_difficulty(pnum, &pv.map);
    let acc = ctx.meta.get(pnum).and_then(|m| m.acceptance);
    if diff.is_empty() && acc.is_none() {
        return None;
    }
    let mut parts = Vec::new();
    if !diff.is_empty() {
        let style = match diff.as_str() {
            "Easy" => "green",
            "Medium" => "yellow",
            "Hard" => "red",
            _ => "dim",
        };
        parts.push(format!("[{style}]{diff}[/{style}]"));
    }
    if let Some(a) = acc {
        parts.push(format!("[dim]{a:.1}% accepted[/dim]"));
    }
    Some(parts.join(" [dim]·[/dim] "))
}

fn rating_line(ctx: &Ctx, pnum: &str, ev: &Evidence) -> Option<String> {
    let rating = *solve_ratings(ctx).get(pnum)?;
    let elo = elo_now(ctx, ev);
    let gap = rating - elo;
    let odds = 1.0 / (1.0 + 10f64.powf(gap / 400.0));
    let colour = if gap > 100.0 {
        "red"
    } else if gap > -100.0 {
        "yellow"
    } else {
        "green"
    };
    Some(format!(
        "[dim]rating[/dim] [bold]{:.0}[/bold] [dim]·[/dim] [dim]elo[/dim] {:.0} [dim]·[/dim] [{colour}]{:+.0}[/{colour}] [dim]·[/dim] [dim]odds[/dim] [{colour}]{:.0}%[/{colour}]",
        rating,
        elo,
        gap,
        odds * 100.0
    ))
}

fn headline(ctx: &Ctx, pnum: &str, pv: &PView, ev: &Evidence) -> String {
    let parts: Vec<String> = [difficulty_line(ctx, pnum, pv), rating_line(ctx, pnum, ev)]
        .into_iter()
        .flatten()
        .collect();
    parts.join(" [dim]·[/dim] ")
}

fn header_line(secs: i64, clock_len: usize, reviews: usize) -> String {
    let mut parts = Vec::new();
    if secs != 0 {
        let (h, m) = ((secs / 60) / 60, (secs / 60) % 60);
        let t = if h != 0 {
            format!("{h}h {m:02}m")
        } else {
            format!("{m}m")
        };
        parts.push(format!("today [bold]{t}[/bold] solving"));
    }
    if clock_len != 0 {
        parts.push(format!(
            "drill clock [bold]{clock_len}[/bold] due ({reviews} review, {} never done)",
            clock_len - reviews
        ));
    }
    parts.join(" [dim]·[/dim] ")
}

fn pace_line(fc: Option<(f64, f64, f64)>) -> Option<String> {
    let (e, h, b) = fc?;
    let m = |v: f64| format!("{}m", v.round_ties_even() as i64);
    Some(format!(
        "[dim]pace[/dim] ~{} expected [dim]·[/dim] hint fair game after {} [dim]·[/dim] at {} stop, mark it, reinforce",
        m(e),
        m(h),
        m(b)
    ))
}

fn ahead_line(line: &str) -> String {
    format!(
        "[dim]ahead[/dim] {}",
        line.strip_prefix("review ahead: ").unwrap_or(line)
    )
}

fn park_table(ctx: &Ctx, pv: &PView, ev: &Evidence, statuses: &Statuses) -> Option<Table> {
    let rows = sleep_rows(ctx, pv, ev, statuses);
    if rows.is_empty() {
        return None;
    }
    let mut table = plain_table(&["Problem", "Ground", "Parked", "Wake"], Some("asleep"));
    for (pnum, title, rusty, since, cycles) in rows {
        let ground = if rusty.is_empty() {
            "[green]solid[/green]".to_string()
        } else {
            format!("[yellow]warming: {}[/yellow]", rusty.join(", "))
        };
        let slept = if cycles > 1 {
            format!(" [dim]x{cycles}[/dim]")
        } else {
            String::new()
        };
        table.add_row(&[
            format!("{pnum}. {title}"),
            ground,
            format!("{}{slept}", since.replace('T', " ")),
            format!("make wake {pnum}"),
        ]);
    }
    Some(table)
}

fn cap_cell(k: i64, c: i64) -> String {
    let colour = if k >= c { "red" } else { "green" };
    format!("[{colour}]{k}/{c}[/{colour}]")
}

fn caps_table(ctx: &Ctx, pv: &PView, ev: &Evidence, today: NaiveDate) -> Option<Table> {
    let mut rows: Vec<[String; 3]> = Vec::new();
    let mut caps = group_caps();
    caps.sort();
    for (g, c) in caps {
        let k = group_reps(ctx, &g, ev, today);
        rows.push([
            g.clone(),
            cap_cell(k, c),
            if k >= c {
                format!("at the cap - make next {g} to go past it")
            } else {
                "KG_GROUP_CAP".to_string()
            },
        ]);
    }
    if let Some(cap) = new_drill_cap() {
        let k = new_drills_today(ev, today);
        rows.push([
            "new drills".into(),
            cap_cell(k, cap),
            if k >= cap {
                "at the cap - reviews only until tomorrow".into()
            } else {
                "MAX_NEW_DRILLS".into()
            },
        ]);
    }
    if let Some(cap) = drill_review_cap() {
        let k = drill_reviews_today(ev, today);
        rows.push([
            "drill reviews".into(),
            cap_cell(k, cap),
            if k >= cap {
                "at the cap - the bank waits until tomorrow".into()
            } else {
                "MAX_DRILL_REVIEWS".into()
            },
        ]);
    }
    let due = review_queue(ctx, ev, pv, today);
    if !due.is_empty() {
        let n = due.len();
        let oldest = &due[0].0;
        let mut note = String::new();
        if n > 1 {
            note.push_str(&format!(
                "oldest {oldest}. {} - ",
                pv.get(oldest).unwrap().title
            ));
        }
        note.push_str("due until an unaided clean rep");
        if reviews_first() {
            note.push_str(" (REVIEWS_FIRST)");
        }
        rows.push([
            "problem reviews".into(),
            format!("[yellow]{n} due[/yellow]"),
            note,
        ]);
    }
    if rows.is_empty() {
        return None;
    }
    let mut table = plain_table(&["Budget", "Used", "Note"], Some("today"));
    for r in rows {
        table.add_row(&r);
    }
    Some(table)
}

fn judge_line(ctx: &Ctx, ev: &Evidence) -> Option<String> {
    let pending = pending_judgements(ev);
    if pending.is_empty() {
        return None;
    }
    let stale: Vec<&String> = pending
        .iter()
        .filter(|(_, age)| is_stale(*age))
        .map(|(p, _)| p)
        .collect();
    for p in &stale {
        spawn_judge(&ctx.root, p);
    }
    let mut s = format!("judge pending on {} rep(s)", pending.len());
    if !stale.is_empty() {
        s.push_str(&format!(", {} respawned", stale.len()));
    }
    s.push_str(" (.judge.log)");
    Some(s)
}

enum FooterItem {
    Table(Table),
    Line(String),
}

fn build_footer(
    ctx: &Ctx,
    pv: &PView,
    ev: &Evidence,
    statuses: &Statuses,
    asleep: &[String],
    today: NaiveDate,
) -> Vec<FooterItem> {
    let mut items = Vec::new();
    if !asleep.is_empty() {
        if let Some(t) = park_table(ctx, pv, ev, statuses) {
            items.push(FooterItem::Table(t));
        }
    }
    if let Some(t) = caps_table(ctx, pv, ev, today) {
        items.push(FooterItem::Table(t));
    }
    if let Some(l) = judge_line(ctx, ev) {
        items.push(FooterItem::Line(l));
    }
    items
}

/// kg_next.gate_table + kg_lib.gates without copying the table: every
/// problem number (the caller's entries winning over graph/problems.json)
/// and drill id whose "after" names `vid`, problems first in number
/// order, then drills.
fn gates_merged(ctx: &Ctx, pv: &PView, vid: &str) -> Vec<String> {
    let names = |p: &kg_next::data::Problem| p.after.iter().any(|a| a == vid);
    let mut held: Vec<String> = ctx
        .all_problems()
        .iter()
        .filter(|(k, p)| names(pv.get(k).unwrap_or(p)))
        .map(|(k, _)| k.clone())
        .collect();
    held.extend(
        pv.map
            .iter()
            .filter(|(k, p)| !ctx.all_problems().contains_key(*k) && names(p))
            .map(|(k, _)| k.clone()),
    );
    held.sort_by_key(|p| kg_next::data::pnum_key(p));
    let mut drills: Vec<String> = ctx
        .drills
        .iter()
        .filter(|(_, d)| d.after.iter().any(|a| a == vid))
        .map(|(i, _)| i.clone())
        .collect();
    drills.sort_by_key(|p| kg_next::data::pnum_key(p));
    held.extend(drills);
    held
}

fn gated_label(
    ctx: &Ctx,
    h: &str,
    pv: &PView,
    ev: &Evidence,
    labeled: bool,
    today: NaiveDate,
) -> String {
    if labeled {
        let title = pv
            .get(h)
            .or_else(|| ctx.all_problems().get(h))
            .map(|p| p.title.clone())
            .or_else(|| ctx.drills.get(h).map(|d| d.title.clone()))
            .unwrap_or_default();
        return format!("{h}. {title}");
    }
    // vertex_status over the merged table: the caller's view first, the
    // whole table behind it (vertex_kind already falls through to it)
    let s = kg_next::bank::vertex_status(ctx, h, pv, ev, today);
    format!("{s} {}", face(s))
}

/// kg_next.print_gates' names, drawn in the Python order (after the table
/// faces, before the tree's).
fn gate_names(
    ctx: &Ctx,
    vid: &str,
    pv: &PView,
    ev: &Evidence,
    labeled: bool,
    today: NaiveDate,
) -> Vec<String> {
    gates_merged(ctx, pv, vid)
        .iter()
        .map(|h| gated_label(ctx, h, pv, ev, labeled, today))
        .collect()
}

fn print_gates(console: &Console, names: &[String]) {
    if names.is_empty() {
        return;
    }
    console.print(&format!("[dim]gates: {}[/dim]", names.join(" · ")));
}

fn add_gated(
    ctx: &Ctx,
    dot: &mut Dot,
    from: &str,
    vid: &str,
    pv: &PView,
    ev: &Evidence,
    labeled: bool,
    today: NaiveDate,
) {
    for h in gates_merged(ctx, pv, vid) {
        let gid = format!("gated_{h}");
        let label = gated_label(ctx, &h, pv, ev, labeled, today);
        dot.node(
            &gid,
            &[
                ("label", &label),
                ("shape", "box"),
                ("style", "rounded"),
                ("color", "#8b949e"),
                ("fontcolor", "#c9d1d9"),
                ("margin", "0.15,0.08"),
            ],
        );
        dot.edge(from, &gid, &[("color", "#8b949e"), ("style", "dashed")]);
    }
}

struct Run<'a> {
    console: &'a Console,
    ctx: &'a Ctx,
    args: &'a Args,
    pv: RefCell<PView>,
    ev: Evidence,
    statuses: Statuses,
    immature: HashSet<String>,
    today: NaiveDate,
    footer: Vec<FooterItem>,
    starved_memo: RefCell<Option<Vec<(String, i64)>>>,
    pre_dot: RefCell<Option<PreDot>>,
}

type DotJob = std::thread::JoinHandle<Result<u32, String>>;

impl<'a> Run<'a> {
    fn maturity_cell(&self, n: &str) -> String {
        if self.immature.contains(n) {
            "[yellow]young[/yellow]".into()
        } else {
            "[dim]mature[/dim]".into()
        }
    }

    fn own_cell(&self, n: &str) -> String {
        let pv = self.pv.borrow();
        let ax = node_axes(self.ctx, n, &self.ev, &pv, self.today);
        let k = ax.carriers;
        let note = if carry_bar(self.ctx, n, &pv).0 == "none" {
            "none in bank".to_string()
        } else {
            format!("{k} carrier{}", if k == 1 { "" } else { "s" })
        };
        format!("{:.2} [dim]({note})[/dim]", ax.degree)
    }

    fn recall_line(&self, path: &std::path::Path) -> Option<String> {
        let (p, cleans, gap, copies) = drill_recall(self.ctx, path, &self.ev, self.today)?;
        let cells = 12usize;
        let Some(p) = p else {
            let bar = format!("[dim]{}[/dim]", "\u{2591}".repeat(cells));
            let seen = if copies == 0 {
                "never done".to_string()
            } else {
                format!(
                    "{copies} cop{}, {gap}d gap",
                    if copies == 1 { "y" } else { "ies" }
                )
            };
            return Some(format!(
                "[dim]recall:[/dim] {bar} [cyan]no unaided rep yet[/cyan] [dim]{seen} - copying is the rep, recall is the next one[/dim]"
            ));
        };
        let (colour, note) = if p >= 0.85 {
            ("green", "should come back cold")
        } else if p >= 0.65 {
            ("yellow", "likely, expect to fumble the bookkeeping")
        } else if p >= 0.40 {
            ("dark_orange", "even odds - expect to reconstruct it")
        } else {
            ("red", "expect a miss - this is a relearning rep")
        };
        let full = ((p * cells as f64).round_ties_even() as i64).clamp(1, cells as i64) as usize;
        let bar = format!(
            "[{colour}]{}[/{colour}][dim]{}[/dim]",
            "\u{2588}".repeat(full),
            "\u{2591}".repeat(cells - full)
        );
        let reps = format!("{cleans} clean rep{}", if cleans == 1 { "" } else { "s" });
        Some(format!(
            "[dim]recall:[/dim] {bar} [{colour}]{}%[/{colour}] [dim]{reps}, {gap}d gap - {note}[/dim]",
            (p * 100.0).round_ties_even() as i64
        ))
    }

    /// kg_next.starved, computed once per run (routed_around and warn_dry
    /// both read it).
    fn starved(&self) -> Vec<(String, i64)> {
        if let Some(s) = self.starved_memo.borrow().as_ref() {
            return s.clone();
        }
        let s = starved(self.ctx, &self.pv.borrow(), &self.ev, self.today);
        *self.starved_memo.borrow_mut() = Some(s.clone());
        s
    }

    fn warn_dry(&self, asleep: &[String]) {
        let pv = self.pv.borrow();
        let mut hungry = self.starved();
        hungry.sort_by_key(|(_, k)| -k);
        if !hungry.is_empty() {
            let names: Vec<String> = hungry.iter().map(|(n, k)| format!("{n} ({k}d)")).collect();
            self.console.print(&format!(
                "[yellow]⚠ starved: {} - due that long with nothing aimed at {}[/yellow]",
                names.join(", "),
                if hungry.len() == 1 { "it" } else { "them" }
            ));
        }
        let dry: Vec<String> = blocked_frontier(
            self.ctx,
            &pv,
            &self.ev,
            &self.statuses,
            asleep,
            &HashSet::new(),
            self.today,
        )
        .into_iter()
        .filter(|(nid, _, _, is_dry)| *is_dry && !self.ctx.has_drill_bank(nid))
        .map(|(nid, _, _, _)| nid)
        .collect();
        if !dry.is_empty() {
            self.console.print(&format!(
                "[yellow]⚠ dry on {} \u{2014} nothing can serve {} (make next --why)[/yellow]",
                dry.join(", "),
                if dry.len() == 1 {
                    "this move"
                } else {
                    "these moves"
                }
            ));
        }
    }

    fn prepare(&self, target: &str, force: bool) {
        if !self.args.prepare {
            return;
        }
        let cur = self.ctx.root.join("current.py");
        if std::fs::read_to_string(&cur).is_ok_and(|s| !s.trim().is_empty()) {
            self.console.print("[yellow]current.py is not empty \u{2014} record it (make solved) before preparing the next one.[/yellow]");
            self.flush_footer();
            std::process::exit(1);
        }
        let tool = if force { "kg_force" } else { "prepare" };
        let py = self.ctx.root.join(".venv/bin/python3");
        let py = if py.exists() {
            py
        } else {
            std::path::PathBuf::from("python3")
        };
        let pythonpath = format!(
            "{}:{}",
            self.ctx.root.join("utils").display(),
            std::env::var("PYTHONPATH").unwrap_or_default()
        );
        let _ = Command::new(py)
            .arg(self.ctx.root.join("utils/kg").join(tool))
            .arg(target)
            .current_dir(&self.ctx.root)
            .env("PYTHONPATH", pythonpath)
            .status();
    }

    /// kg_next.main's finally: the park and the day's budgets, always.
    fn flush_footer(&self) {
        if self.footer.is_empty() {
            return;
        }
        self.console.blank();
        let tables: Vec<&Table> = self
            .footer
            .iter()
            .filter_map(|f| match f {
                FooterItem::Table(t) => Some(t),
                _ => None,
            })
            .collect();
        if !tables.is_empty() {
            self.console
                .print_lines(columns(&tables, self.console.width));
        }
        for f in &self.footer {
            if let FooterItem::Line(l) = f {
                self.console.print(&format!("[dim]{l}[/dim]"));
            }
        }
    }

    fn move_row(&self, table: &mut Table, m: &str, labeled: bool) {
        let (s, d) = st(&self.statuses, m);
        let label = if labeled {
            m.to_string()
        } else {
            face(s).to_string()
        };
        table.add_row(&[
            label,
            styled_status(s),
            self.maturity_cell(m),
            self.own_cell(m),
            d.map(|d| d.format("%Y-%m-%d").to_string())
                .unwrap_or_else(|| "\u{2014}".into()),
        ]);
    }

    fn draw_tree(
        &self,
        dot: &mut Dot,
        tree: &[String],
        highlight: &HashSet<String>,
        labeled: bool,
    ) {
        let pv = self.pv.borrow();
        for n in tree {
            let (s, d) = st(&self.statuses, n);
            let node = &self.ctx.nodes[n];
            let label = if labeled {
                n.replacen('-', "-\n", 1)
            } else {
                format!("{s} {}", face(s))
            };
            dot.status_node(
                n,
                &node.name,
                s,
                d.map(|d| d.format("%Y-%m-%d").to_string()).as_deref(),
                highlight.contains(n),
                &label,
                node_degree(self.ctx, n, &self.ev, &pv, self.today),
            );
        }
        for n in tree {
            for pre in self.ctx.prereqs(n) {
                if tree.contains(pre) {
                    dot.edge(pre, n, &[]);
                }
            }
        }
    }

    /// Start `dot` on the drawing, to be shown by `show`. None when there is
    /// nothing to show it on (no terminal): kg_render.display draws nothing
    /// when piped, so the layout is skipped too.
    fn start_drawing(&self, dot: &Dot) -> Option<DotJob> {
        if !kg_next::console::stdout_is_tty() {
            return None;
        }
        let pre = self.pre_dot.borrow_mut().take();
        Some(render_in_background(
            self.ctx.graph_dir(),
            dot.source(),
            "kg_next",
            pre,
        ))
    }

    fn show(&self, job: Option<DotJob>) {
        let Some(job) = job else { return };
        match job.join().unwrap_or_else(|_| Err("dot thread".into())) {
            Ok(w) => display(self.console, &self.ctx.graph_dir(), "kg_next", w),
            Err(e) => self.console.print(&format!(
                "[dim](tree drawing failed \u{2014} {e}; cosmetic, pick unaffected)[/dim]"
            )),
        }
    }
}

/// kg_next.load_plan: today's frozen plan, frozen first if absent.
fn load_plan(console: &Console, ctx: &Ctx, today: NaiveDate) -> Option<Value> {
    let flag = std::env::var("KG_NO_PLAN").unwrap_or_default();
    if !matches!(flag.trim(), "" | "0") {
        return None;
    }
    let path = ctx
        .root
        .join("data/study_plan")
        .join(format!("{}.json", today.format("%Y-%m-%d")));
    if !path.exists() {
        console.print("[dim]new day \u{2014} freezing today's plan...[/dim]");
        let py = ctx.root.join(".venv/bin/python3");
        let py = if py.exists() {
            py
        } else {
            std::path::PathBuf::from("python3")
        };
        let _ = Command::new(py)
            .arg(ctx.root.join("utils/kg/kg_today"))
            .env(
                "PYTHONPATH",
                format!(
                    "{}:{}",
                    ctx.root.join("utils").display(),
                    std::env::var("PYTHONPATH").unwrap_or_default()
                ),
            )
            .status();
    }
    kg_next::data::read_json(&path)
}

fn plan_item_done(ctx: &Ctx, item: &Value, ev: &Evidence, plan: &Value) -> bool {
    let kind = item["kind"].as_str().unwrap_or("");
    let plan_date = plan["date"].as_str().unwrap_or("");
    if kind == "create-drill" {
        let gen = plan["generated"]
            .as_str()
            .and_then(|s| {
                chrono::NaiveDateTime::parse_from_str(s, "%Y-%m-%dT%H:%M:%S%.f")
                    .or_else(|_| chrono::NaiveDateTime::parse_from_str(s, "%Y-%m-%dT%H:%M:%S"))
                    .ok()
            })
            .map(|dt| {
                dt.and_local_timezone(kg_next::data::manila())
                    .unwrap()
                    .timestamp()
            })
            .unwrap_or(0);
        let node = item["node"].as_str().unwrap_or("");
        return ctx.bank_files(node).iter().any(|p| {
            std::fs::metadata(p)
                .and_then(|m| m.modified())
                .ok()
                .and_then(|t| t.duration_since(std::time::UNIX_EPOCH).ok())
                .is_some_and(|d| d.as_secs() as i64 >= gen)
        });
    }
    if kind == "drill" {
        let node = item["node"].as_str().unwrap_or("");
        return ev
            .recs
            .iter()
            .any(|(_, r)| r.date.as_str() >= plan_date && r.moves.contains_key(node));
    }
    let problem = kg_next::data::value_str(&item["problem"]);
    ev.recs.iter().any(|(_, r)| {
        r.problem.as_deref() == Some(problem.as_str()) && r.date.as_str() >= plan_date
    })
}

fn main() {
    trace("start");
    let root = repo_root();
    load_envrc(&root);
    // a terminal run will draw: dot starts now and gets the graph later
    let argv: Vec<String> = std::env::args().skip(1).collect();
    let will_draw = kg_next::console::stdout_is_tty()
        && !argv
            .iter()
            .any(|a| a == "--no-show" || a == "--golden-json" || a == "-h" || a == "--help");
    let pre = if will_draw {
        prespawn_dot(&root.join("graph"))
    } else {
        None
    };
    // git and its cache file are read on a thread while the JSON parses
    let git_root = root.clone();
    let git_prefetch = std::thread::spawn(move || kg_next::git::fetch_git_state(&git_root));
    let (ctx, recs) = Ctx::load(root);
    *ctx.git_prefetch.borrow_mut() = Some(git_prefetch);
    trace("ctx loaded");
    let args = parse_args(&ctx);
    let console = Console::new();
    let today = ctx.today();

    let pv = RefCell::new(PView::new(ctx.evidenced()));
    let ev = Evidence::new(recs);
    let statuses = all_statuses(&ctx, &ev, today);
    let immature = immature_nodes(&ctx, &ev, &pv.borrow());
    trace("statuses");

    if args.golden {
        golden::dump(&ctx, &pv.borrow(), &ev, &statuses, &immature, today);
        return;
    }

    let asleep = sleep_state(&ctx, &pv.borrow(), &ev);
    trace("sleep state");
    let woken: Vec<String> = vec![];
    let footer = build_footer(&ctx, &pv.borrow(), &ev, &statuses, &asleep, today);
    trace("footer");
    let run = Run {
        console: &console,
        ctx: &ctx,
        args: &args,
        pv,
        ev,
        statuses,
        immature,
        today,
        footer,
        starved_memo: RefCell::new(None),
        pre_dot: RefCell::new(pre),
    };
    run_main(&run, &asleep, &woken);
    run.flush_footer();
    trace("done");
    kg_next::pick::ptrace("dump", std::time::Instant::now());
}

fn run_main(run: &Run, asleep: &[String], woken: &[String]) {
    let (console, ctx, args, ev, statuses, today) = (
        run.console,
        run.ctx,
        run.args,
        &run.ev,
        &run.statuses,
        run.today,
    );
    let labeled = args.graph;
    let session_start = is_session_start(ctx);
    trace("session start");

    // the clock, announced
    let (clock, reviews) = if anki() {
        let scope: Vec<String> = ctx
            .nodes
            .keys()
            .filter(|n| args.group.is_none() || ctx.group_of(n) == args.group.as_deref())
            .cloned()
            .collect();
        let clock = anki_frontier(ctx, ev, today, None, Some(&scope), args.assisted);
        let reviews = clock
            .iter()
            .filter(|(p, _)| anki_due(ctx, p, ev).is_some())
            .count();
        (clock, reviews)
    } else {
        (vec![], 0)
    };
    trace("clock");
    let head = header_line(solve_seconds_today(ctx), clock.len(), reviews);
    trace("header");
    if !head.is_empty() {
        console.print(&format!("[dim]{head}[/dim]"));
    }

    // the recognition axis
    if !(args.group.is_some() || args.early || args.assisted) {
        let pv = run.pv.borrow();
        let derived = recog::derived(ctx, &recog::load_recognition(ctx), ev, &pv, statuses);
        let skip: HashSet<String> = asleep.iter().cloned().collect();
        if recog::due_spot(ctx, &pv, ev, &derived, statuses, today, &skip).is_some() {
            console.print("[bold]spot rep due[/bold] - make prepare spot (read the statement, name the move, no code; before the solve)");
        }
    }

    trace("spot");
    let mut exclude: HashSet<String> = solved_today_pnums(ctx);
    let mut choice: Option<Choice> = None;
    let mut shown = 0usize;
    let mut refused = false;
    let mut plan_note: Option<String> = None;

    let plan = if args.early || args.assisted || !clock.is_empty() {
        None
    } else {
        load_plan(console, ctx, today)
    };
    if let Some(plan) = plan {
        let items: Vec<Value> = plan["items"].as_array().cloned().unwrap_or_default();
        let mut pending: Vec<Value> = items
            .into_iter()
            .filter(|it| {
                !plan_item_done(ctx, it, ev, &plan)
                    && !exclude.contains(&kg_next::data::value_str(
                        it.get("problem").unwrap_or(&Value::String(String::new())),
                    ))
                    && !it
                        .get("problem")
                        .map(kg_next::data::value_str)
                        .is_some_and(|p| asleep.contains(&p))
            })
            .collect();
        let plan_drills: HashSet<String> = pending
            .iter()
            .filter(|it| it["kind"].as_str() == Some("drill"))
            .filter_map(|it| it["node"].as_str().map(String::from))
            .collect();
        pending.retain(|it| {
            if it["kind"].as_str() != Some("drill") {
                return true;
            }
            let node = it["node"].as_str().unwrap_or("").to_string();
            let mut others = plan_drills.clone();
            others.remove(&node);
            // the curve outranks the flag, then the cross-bank hold
            !(drill_held(ctx, &node, statuses, ev, &others)
                || (st(statuses, &node).0 == SOLID && owned(ev, &node)))
        });
        let idx = args.n.max(1) - 1;
        if idx < pending.len() {
            let item = &pending[idx];
            let kind = item["kind"].as_str().unwrap_or("");
            if kind == "create-drill" {
                let node = item["node"].as_str().unwrap_or("");
                console.begin_capture();
                console.blank();
                console.print(&format!("[bold]create drill: {node}[/bold]"));
                if let Some(spec) = item
                    .get("spec")
                    .and_then(|s| s.as_str())
                    .filter(|s| !s.is_empty())
                {
                    console.print(spec);
                }
                console.print(&format!(
                    "[dim]plan item \u{2014} clears when a new bank file lands in drills/{node}/[/dim]"
                ));
                let cap = console.end_capture();
                animate(console, cap);
                return;
            }
            if kind == "drill" {
                let node = item["node"].as_str().unwrap_or("").to_string();
                if due_drill(ctx, &node, ev, today, false, false).is_some() {
                    choice = Some(Choice {
                        target: node.clone(),
                        status: st(statuses, &node).0,
                        pnum: format!("drill:{node}"),
                        reason: format!(
                            "plan: {}",
                            item.get("why").and_then(|w| w.as_str()).unwrap_or("")
                        ),
                    });
                }
            } else {
                let pnum = kg_next::data::value_str(
                    item.get("problem").unwrap_or(&Value::String(String::new())),
                );
                if let Some(p) = run.pv.borrow().get(&pnum) {
                    let target = p
                        .moves
                        .iter()
                        .find(|m| st(statuses, m).0 != SOLID)
                        .unwrap_or(&p.moves[0])
                        .clone();
                    plan_note = item.get("note").and_then(|n| n.as_str()).map(String::from);
                    choice = Some(Choice {
                        target: target.clone(),
                        status: st(statuses, &target).0,
                        pnum,
                        reason: format!("plan: {kind}"),
                    });
                }
            }
            if withheld(choice.as_ref(), asleep) {
                choice = None;
                refused = true;
            }
            shown = if choice.is_some() { 1 } else { 0 };
        }
    }

    if choice.is_none() {
        for _ in 0..args.n.max(1) {
            let pa = PickArgs {
                asleep: asleep.to_vec(),
                woken: woken.to_vec(),
                exclude: exclude.clone(),
                session_start,
                group: args.group.clone(),
                cram: args.cram,
                early: args.early,
                assisted: args.assisted,
            };
            choice = pick(ctx, &run.pv, ev, statuses, &pa);
            let Some(c) = &choice else { break };
            if withheld(Some(c), asleep) {
                choice = None;
                refused = true;
                break;
            }
            shown += 1;
            exclude.insert(c.pnum.clone());
        }
    }
    trace("pick");
    if refused && choice.is_none() {
        for line in park_full_lines(asleep) {
            console.print(&line);
        }
        return;
    }
    let Some(choice) = choice else {
        nothing_to_serve(run, asleep, &exclude, shown);
        return;
    };
    let Choice { target, pnum, .. } = choice;
    seed_faces(today, &pnum);

    // the "ahead" line is the last line of the body; its replay is run
    // after the drawing has been handed to `dot`, so the two overlap. It
    // draws no faces, so the faces still come out in the Python order.
    let ahead = || {
        if args.early || args.assisted {
            return None;
        }
        let pv = run.pv.borrow();
        let (d, s, r) = review_ahead(
            ctx,
            &pv,
            ev,
            asleep,
            &solved_today_pnums(ctx),
            args.group.as_deref(),
            14,
            200,
        );
        Some(review_line(d, s, r))
    };

    if pnum.starts_with("drill:") {
        // the file pick()'s due() named: its clock's, else the cold one it
        // fell back to
        let path = due_drill(ctx, &target, ev, today, args.early, args.assisted)
            .or_else(|| cold_drill(ctx, &target, ev, today, true))
            .expect("the drill the pick named");
        let title = kg_next_drill_title(&path);
        let did = ctx.drill_id(&path);
        let name = match &did {
            Some(d) => format!("{d}. {title}"),
            None => format!("drill: {title}"),
        };
        let mut table = head_table();
        run.move_row(&mut table, &target, labeled);
        let gate_id = did.clone().unwrap_or_else(|| title.clone());
        let names = gate_names(ctx, &gate_id, &run.pv.borrow(), ev, labeled, today);
        // the drawing goes to `dot` before the body is priced: the layout
        // is the long pole and the two overlap
        let mut job = None;
        if !args.no_show {
            let mut tree: Vec<String> = input_tree(std::slice::from_ref(&target), &ctx.nodes)
                .into_iter()
                .collect();
            tree.sort();
            let mut dot = Dot::new("input-tree");
            let hl: HashSet<String> = [target.clone()].into_iter().collect();
            run.draw_tree(&mut dot, &tree, &hl, labeled);
            dot.node(
                "drill_box",
                &[
                    ("label", &name),
                    ("shape", "box"),
                    ("style", "filled"),
                    ("fillcolor", "#1f6feb"),
                    ("color", "#c9d1d9"),
                    ("penwidth", "2"),
                    ("fontsize", "13"),
                    ("margin", "0.2,0.12"),
                ],
            );
            dot.edge(&target, "drill_box", &[("penwidth", "1.4")]);
            add_gated(
                ctx,
                &mut dot,
                "drill_box",
                &gate_id,
                &run.pv.borrow(),
                ev,
                labeled,
                today,
            );
            job = run.start_drawing(&dot);
        }
        console.begin_capture();
        kg_next::table::print_table(console, &table);
        if let Some(rl) = run.recall_line(&path) {
            console.print(&rl);
        }
        print_gates(console, &names);
        if let Some(p) = pace_line(drill_forecast(ctx, &path, today)) {
            console.print(&p);
        }
        if let Some(a) = ahead() {
            console.print(&ahead_line(&a));
        }
        trace("review ahead");
        let body = console.end_capture();
        console.begin_capture();
        console.blank();
        console.print_lines(panel(
            &body,
            &format!("[bold]{name}[/bold]"),
            None,
            console.width,
        ));
        console.print(&format!(
            "[bold]make prepare {}[/bold]",
            did.clone().unwrap_or_else(|| target.clone())
        ));
        let cap = console.end_capture();
        run.show(job);
        animate(console, cap);
        run.warn_dry(asleep);
        run.prepare(&path.display().to_string(), false);
        return;
    }

    let p = run
        .pv
        .borrow()
        .get(&pnum)
        .cloned()
        .expect("the problem the pick named");
    let around = kg_next::pick::routed_around_from(&run.pv.borrow(), ev, today, &run.starved())
        .into_iter()
        .find(|(n, _)| *n == target)
        .map(|(_, c)| c);
    let forced = around.is_some();
    let force_note = around.map(|a| {
        format!("{a} was solved without this move while it was due - this rep must use it")
    });

    let mut table = head_table();
    for m in &p.moves {
        run.move_row(&mut table, m, labeled);
    }
    let names = gate_names(ctx, &pnum, &run.pv.borrow(), ev, labeled, today);
    let summit = if p.is_hard() { "⛰  " } else { "" };

    // the drawing goes to `dot` before the body is priced: the layout is
    // the long pole and the two overlap
    let mut job = None;
    if !args.no_show {
        let mut tree: Vec<String> = input_tree(&p.moves, &ctx.nodes).into_iter().collect();
        tree.sort();
        let mut dot = Dot::new("input-tree");
        let hl: HashSet<String> = p.moves.iter().cloned().collect();
        run.draw_tree(&mut dot, &tree, &hl, labeled);
        let problem_node = format!("problem_{pnum}");
        let plabel = format!("{pnum}. {}", p.title);
        let url = problem_url(ctx, &pnum);
        dot.node(
            &problem_node,
            &[
                ("label", &plabel),
                ("shape", "box"),
                ("style", "filled"),
                ("fillcolor", "#1f6feb"),
                ("color", "#c9d1d9"),
                ("penwidth", "2"),
                ("fontsize", "13"),
                ("margin", "0.2,0.12"),
                ("tooltip", &url),
            ],
        );
        for m in &p.moves {
            dot.edge(m, &problem_node, &[("penwidth", "1.4")]);
        }
        add_gated(
            ctx,
            &mut dot,
            &problem_node,
            &pnum,
            &run.pv.borrow(),
            ev,
            labeled,
            today,
        );
        job = run.start_drawing(&dot);
    }

    console.begin_capture();
    console.print(&headline(ctx, &pnum, &run.pv.borrow(), ev));
    if p.predicted {
        console.print("[yellow]⚠ drafted walk, not yet evidenced \u{2014} your solve is what maps this problem[/yellow]");
    }
    if let Some(note) = p.note.as_deref().filter(|n| !n.is_empty()) {
        console.print(&format!("[yellow]⚠ {note}[/yellow]"));
    }
    if let Some(pn) = plan_note.as_deref().filter(|n| !n.is_empty()) {
        console.print(&format!("[yellow]{pn}[/yellow]"));
    }
    if let Some(fnote) = &force_note {
        console.print(&format!("[yellow]⚠ {fnote}[/yellow]"));
    }
    if let Some((due, _)) = problem_due(ev, &pnum) {
        if due <= today {
            if let Some((when, label)) = last_attempt(ev, &pnum) {
                console.print(&format!(
                    "[yellow]⚠ review: {} {}d ago - this rep is the unaided one[/yellow]",
                    review_note(&label),
                    (today - when).num_days()
                ));
            }
        }
    }
    kg_next::table::print_table(console, &table);
    print_gates(console, &names);
    if let Some(pl) = pace_line(solve_forecast(ctx, &pnum, &run.pv.borrow(), today)) {
        console.print(&pl);
    }
    if let Some(a) = ahead() {
        console.print(&ahead_line(&a));
    }
    trace("review ahead");
    let body = console.end_capture();
    console.begin_capture();
    console.blank();
    console.print_lines(panel(
        &body,
        &format!("[bold]{summit}{pnum}. {}[/bold]", p.title),
        Some(&format!("[dim]{}[/dim]", problem_url(ctx, &pnum))),
        console.width,
    ));
    if forced {
        console.print(&format!("[bold]make force {pnum}[/bold]"));
    }
    let cap = console.end_capture();
    trace("panel");
    run.show(job);
    animate(console, cap);
    run.warn_dry(asleep);
    trace("warn dry");
    run.prepare(&pnum, forced);
}

/// kg_next.drill_title: the DRILL: header, else the filename stem.
fn kg_next_drill_title(path: &std::path::Path) -> String {
    if let Ok(text) = std::fs::read_to_string(path) {
        for line in text.lines() {
            let t = line.trim_start();
            if let Some(rest) = t.strip_prefix("DRILL:") {
                let rest = rest.trim_end_matches('\r');
                if !rest.is_empty() {
                    return rest.trim().to_string();
                }
            }
        }
    }
    path.file_stem()
        .and_then(|s| s.to_str())
        .unwrap_or("")
        .to_string()
}

fn nothing_to_serve(run: &Run, asleep: &[String], exclude: &HashSet<String>, shown: usize) {
    let (console, ctx, args, ev, statuses, today) = (
        run.console,
        run.ctx,
        run.args,
        &run.ev,
        &run.statuses,
        run.today,
    );
    let pv = run.pv.borrow();
    if shown != 0 {
        console.print(&format!(
            "[yellow]Only {shown} recommendation(s) available.[/yellow]"
        ));
    } else if let Some(group) = &args.group {
        let held: Vec<String> = if args.cram || args.early || args.assisted {
            vec![]
        } else {
            let mut h: Vec<String> = ctx
                .nodes
                .keys()
                .filter(|n| {
                    ctx.group_of(n) == Some(group.as_str())
                        && st(statuses, n).0 != SOLID
                        && drill_held(ctx, n, statuses, ev, &HashSet::new())
                })
                .cloned()
                .collect();
            h.sort();
            h
        };
        if !held.is_empty() {
            console.print(&format!(
                "\nNothing to serve \u{2014} {} {group} node(s) are held behind a prereq without an unaided clean rep. `make next {group} cram` ignores the hold.",
                held.len()
            ));
        } else {
            console.print("\nNothing to serve \u{2014} the group is spent for today.");
        }
    } else {
        let blocked = blocked_frontier(ctx, &pv, ev, statuses, asleep, exclude, today);
        let dry: Vec<_> = blocked.iter().filter(|b| b.3).collect();
        let waiting: Vec<_> = blocked.iter().filter(|b| !b.3).collect();
        let parked = parked_summits(ctx, &pv, ev, statuses, asleep, today);
        let unmapped = unmapped_summits(ctx, &pv, ev, statuses);
        if !dry.is_empty() {
            console.print("\nNothing to serve \u{2014} the graph needs new problems mapped.");
        } else if !waiting.is_empty() || !parked.is_empty() {
            console.print("\nNothing due today.");
        } else {
            console.print("\nNothing to serve \u{2014} every mapped move is solid and every summit is climbed.");
        }
        if !waiting.is_empty() {
            let n = waiting.len();
            console.print(&format!(
                "[dim]{n} move{} waiting (make next --why)[/dim]",
                if n > 1 { "s" } else { "" }
            ));
        }
        for pnum in &parked {
            console.print(&format!(
                "⛰  {pnum}. {} is ready and asleep \u{2014} `make wake {pnum}`",
                pv.get(pnum).unwrap().title
            ));
        }
        if !unmapped.is_empty() {
            console.print(&format!(
                "[dim]summits blocked only by an unmapped move (needs a node): {}[/dim]",
                unmapped.join(", ")
            ));
        }
        let gain = kg_next::bank::unlocks(ctx, statuses, &pv, &run.immature);
        let mut young: Vec<(String, i64)> = gain
            .into_iter()
            .filter(|(n, _)| run.immature.contains(n) && st(statuses, n).0 == SOLID)
            .collect();
        young.sort_by(|a, b| (-a.1, &a.0).cmp(&(-b.1, &b.0)));
        young.truncate(3);
        if !young.is_empty() {
            let names: Vec<String> = young.iter().map(|(n, g)| format!("{n} ({g})")).collect();
            console.print(&format!(
                "[dim]young moves with no proving carrier today, by drafted problems waiting: {}[/dim]",
                names.join(", ")
            ));
        }
    }
    drop(pv);
    if !args.why {
        run.warn_dry(asleep);
    }
    if args.why {
        let pv = run.pv.borrow();
        let blocked = blocked_frontier(ctx, &pv, ev, statuses, asleep, exclude, today);
        if !blocked.is_empty() {
            let mut table = plain_table(&["Move", "Status", "Why it can't be served"], None);
            for (nid, status, why, is_dry) in blocked {
                table.add_row(&[
                    nid,
                    styled_status(status),
                    format!(
                        "{}{why}",
                        if is_dry { "[yellow]dry:[/yellow] " } else { "" }
                    ),
                ]);
            }
            console.blank();
            kg_next::table::print_table(console, &table);
        }
    }
}

#[allow(dead_code)]
fn unused(_: &[Line]) {
    let _ = degree_color(0.0);
}
