// The drill bank: "after" edges to drills, the cross-bank ladder, the
// ownership rep, the early and cram walks.

use std::collections::HashSet;

use super::*;
use crate::bank::{dependents, easiest_first, gates, held_behind, Dependent};
use crate::data::{Assist, SOLID_WINDOW_DAYS};
use crate::drills::{drill_clean, drill_held, drill_warm, drills_left, due_drill, servable_drills};
use crate::status::{graduation_due, node_status, owned, GRAD_LADDER_SPARSE};

fn held(fx: &Fx, pnum: &str, ev: &Evidence) -> Option<String> {
    held_behind(&fx.ctx(), pnum, &fx.pv(), ev, today())
}

fn due(fx: &Fx, node: &str, ev: &Evidence) -> Option<PathBuf> {
    due_drill(&fx.ctx(), node, ev, today(), false, false)
}

fn due_early(fx: &Fx, node: &str, ev: &Evidence) -> Option<PathBuf> {
    due_drill(&fx.ctx(), node, ev, today(), true, false)
}

fn due_assisted(fx: &Fx, node: &str, ev: &Evidence) -> Option<PathBuf> {
    due_drill(&fx.ctx(), node, ev, today(), false, true)
}

// --------------------------------------------------------------------------
// "after" edges to drills: a problem waits for the bank drill it builds on
// --------------------------------------------------------------------------

/// 713 declares "after": ["d1"], the Count by Contribution drill. No rep
/// of that drill anywhere: 713 is held, and the hold names the drill.
#[test]
fn a_problem_waits_for_a_drill_never_done() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    assert_eq!(held(&fx, "713", &no_evidence()), Some("d1".into()));
}

#[test]
fn a_warm_drill_releases_the_problem() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    let ev = evidence(vec![drill_rep("Count by Contribution", "sw", 3)]);
    assert_eq!(held(&fx, "713", &ev), None);
}

/// Same bar as a drill releasing the next drill of its node: the unaided
/// clean is what releases, a walkthrough clean is a rep but not ownership.
#[test]
fn an_assisted_drill_rep_does_not_release() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    let ev = evidence(vec![drill_rep_a(
        "Count by Contribution",
        "sw",
        3,
        level("walkthrough"),
    )]);
    assert_eq!(held(&fx, "713", &ev), Some("d1".into()));
}

#[test]
fn a_drill_rep_outside_the_solid_window_does_not_release() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    let ev = evidence(vec![drill_rep(
        "Count by Contribution",
        "sw",
        SOLID_WINDOW_DAYS + 1,
    )]);
    assert_eq!(held(&fx, "713", &ev), Some("d1".into()));
}

/// Latest rep decides, as for drills releasing drills.
#[test]
fn a_struggle_after_a_clean_holds_again() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    let ev = evidence(vec![
        drill_rep("Count by Contribution", "sw", 9),
        drill_rep_v("Count by Contribution", "sw", 2, "struggled", Assist::None),
    ]);
    assert_eq!(held(&fx, "713", &ev), Some("d1".into()));
}

/// An id no drill carries cannot be released by anything, so it holds
/// nothing - the deadlock rule for banned predecessors. The real graph is
/// checked by every_after_id_in_the_real_graph_resolves.
#[test]
fn a_drill_ref_nobody_banks_holds_nothing() {
    let mut fx = Fx::new();
    fx.bank("sw", "Something Else", "d0.py", "d9", &[]);
    fx.problem("713", problem(&["nobank"]).after(&["d1"])); // no bank of its own to hold it
    assert_eq!(held(&fx, "713", &no_evidence()), None);
}

/// The edge names the DRILL title, not the file, so renumbering the bank
/// changes nothing.
#[test]
fn a_renamed_bank_file_keeps_its_edge() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "w09_whatever.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    let ev = evidence(vec![drill_rep("Count by Contribution", "sw", 3)]);
    assert_eq!(held(&fx, "713", &ev), None);
}

/// A drill nobody has done holds every problem that walks its node, the
/// one that names it in "after" and the one that does not: the drill is
/// what the node can be served. A clean unaided rep releases both, and the
/// fresher carrier is served.
#[test]
fn a_cold_drill_holds_every_carrier_of_its_node() {
    let mut fx = Fx::picker();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.nodes(&["sw"]).problems(vec![
        ("713", problem(&["sw"]).after(&["d1"])),
        ("3258", problem(&["sw"])),
    ]);
    let ev = evidence(vec![
        solve("713", &[("sw", "clean")], 300),
        solve("3258", &[("sw", "clean")], 299),
    ]);
    let st = statuses(&[("sw", STALE, Some(299))]);
    assert_eq!(held(&fx, "3258", &ev), Some("d1".into()));
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("sw", STALE, "drill:sw"));
    let ev = evidence(vec![
        solve("713", &[("sw", "clean")], 300),
        solve("3258", &[("sw", "clean")], 299),
        drill_rep("Count by Contribution", "sw", 3),
    ]);
    assert_eq!(held(&fx, "3258", &ev), None);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("sw", STALE, "713"));
}

/// What `make next` prints under a served drill or problem: the problems
/// and drills whose "after" names it, problems first.
#[test]
fn gates_is_the_reverse_of_after() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problems(vec![
        ("713", problem(&["sw"]).after(&["d1"])),
        ("3258", problem(&["sw"]).after(&["d1"])),
        ("47", problem(&["sw"]).after(&["46"])),
        ("46", problem(&["sw"])),
    ]);
    fx.register(&[("d2", "Exactly K", &["d1"])]);
    let ctx = fx.ctx();
    assert_eq!(
        gates(&ctx, "d1", &fx.problems),
        strs(&["713", "3258", "d2"])
    );
    assert_eq!(gates(&ctx, "46", &fx.problems), strs(&["47"]));
    assert!(gates(&ctx, "47", &fx.problems).is_empty());
}

/// `make dependents d1`: each dependent with its status and the OTHER
/// ids still holding it, so the next `make prepare` reads off the list.
#[test]
fn dependents_says_what_opens_and_what_else_holds() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.bank("sw", "Exactly K", "d1.py", "d2", &["d1"]);
    fx.problems(vec![
        ("713", problem(&["sw"]).after(&["d1"])),
        ("992", problem(&["sw"]).after(&["d1", "d2"])),
        ("46", problem(&["sw"])),
    ]);
    let ev = evidence(vec![solve("713", &[("sw", "clean")], 100)]);
    let ctx = fx.ctx();
    let rows: Vec<(String, String, Status, Vec<String>)> =
        dependents(&ctx, "d1", &fx.pv(), &ev, today())
            .into_iter()
            .map(|r| (r.id, r.kind, r.status, r.held_by))
            .collect();
    assert_eq!(
        rows,
        vec![
            ("713".to_string(), "Medium".to_string(), STALE, vec![]),
            (
                "992".to_string(),
                "Medium".to_string(),
                MISSING,
                strs(&["d2"])
            ),
            ("d2".to_string(), "drill".to_string(), MISSING, vec![]),
        ]
    );
    assert!(dependents(&ctx, "46", &fx.pv(), &ev, today()).is_empty());
}

#[test]
fn easiest_first_orders_drills_then_by_difficulty_then_acceptance() {
    let mut fx = Fx::new();
    fx.acceptance("1", 30.0).acceptance("2", 70.0);
    let row = |id: &str, kind: &str| Dependent {
        id: id.to_string(),
        title: String::new(),
        kind: kind.to_string(),
        status: MISSING,
        held_by: vec![],
    };
    let rows = vec![
        row("3", "Hard"),
        row("1", "Medium"),
        row("2", "Medium"),
        row("d5", "drill"),
        row("9", "Easy"),
    ];
    let ids: Vec<String> = easiest_first(&fx.ctx(), &rows)
        .into_iter()
        .map(|r| r.id)
        .collect();
    assert_eq!(ids, strs(&["d5", "9", "2", "1", "3"]));
}

/// d27 waits on d26, d26 waits on d75 of another node. Serving this node
/// reaches neither, so the node has no drill left.
#[test]
fn drills_left_ignores_a_chain_ending_at_another_nodes_drill() {
    let mut fx = Fx::new();
    fx.bank("other", "Atom", "a.py", "d75", &[]);
    fx.bank("sw", "Count", "c.py", "d26", &["d75"]);
    fx.bank("sw", "Exactly", "e.py", "d27", &["d26"]);
    assert!(!drills_left(&fx.ctx(), "sw", &no_evidence(), false));
    let ev = evidence(vec![drill_rep("Atom", "other", 1)]);
    assert!(drills_left(&fx.ctx(), "sw", &ev, false));
}

/// 2026-09-16 (make simulate): binary-search-on-answer went FRAGILE; its
/// bank is d115 after d98, a drill of binary-search-index, last done 43
/// days before. d115 is not servable while d98 is cold, and d98's own
/// node, SOLID and off its clock, never served it: 19 starved days. A
/// cold drill a held drill waits on is due on its own node.
#[test]
fn a_cold_drill_a_held_drill_waits_on_is_due_on_its_own_node() {
    let mut fx = Fx::new();
    fx.nodes(&["idx", "ans"]);
    let lit = fx.bank("idx", "First Lit", "a.py", "d98", &[]);
    fx.bank("ans", "First True", "b.py", "d115", &["d98"]);
    let idx_solid = vec![
        drill_rep("First Lit", "idx", SOLID_WINDOW_DAYS + 1),
        solve("2", &[("idx", "clean")], 1),
    ];
    // ans FRAGILE: d98 is wanted, clock or no clock
    let mut ev = idx_solid.clone();
    ev.push(solve("1", &[("ans", "struggled")], 2));
    let ev = evidence(ev);
    assert_eq!(node_status(&fx.ctx(), "ans", &ev, today()).0, FRAGILE);
    assert_eq!(
        due_drill(&fx.ctx(), "idx", &ev, today(), false, false),
        Some(lit)
    );
    // ans SOLID: nothing waits, and idx owns its bank, so nothing is due
    let mut ev = idx_solid;
    ev.push(solve("1", &[("ans", "clean")], 2));
    let ev = evidence(ev);
    assert_eq!(
        due_drill(&fx.ctx(), "idx", &ev, today(), false, false),
        None
    );
}

/// The picker's side of the same hold: the FRAGILE node has no drill of
/// its own to serve, is not parked behind a prereq, and is drill-gated.
/// The rep goes to the cold predecessor's node, and the reason says why.
#[test]
fn a_drill_gated_node_with_nothing_to_serve_rewarms_the_drill_it_waits_on() {
    let mut fx = Fx::picker();
    fx.nodes(&["idx", "ans"]);
    fx.bank("idx", "First Lit", "a.py", "d98", &[]);
    fx.bank("ans", "First True", "b.py", "d115", &["d98"]);
    fx.stubs().bank = set(&["idx", "ans"]);
    fx.stubs().drilled_today = set(&["ans"]);
    let ev = evidence(vec![drill_rep("First Lit", "idx", SOLID_WINDOW_DAYS + 1)]);
    let st = statuses(&[("idx", SOLID, Some(1)), ("ans", FRAGILE, Some(2))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("idx", SOLID, "drill:idx"));
    assert!(reason(&c).contains("d98, gone cold"));
    // d98 warm again: d115 is servable and the fragile move gets its own
    // drill, as before
    let ev = evidence(vec![drill_rep("First Lit", "idx", 3)]);
    assert_eq!(
        t3(&fx.run(&ev, &st, args())),
        tup("ans", FRAGILE, "drill:ans")
    );
}

/// 2026-08-31: substring-enumeration (MISSING, banked) became a prereq of
/// the window node; the window node still had a drill undone and a held
/// dependent, so rule 0c served the window drill over the atom under it.
#[test]
fn rule_0c_does_not_serve_a_prereq_parked_behind_its_own_prereq() {
    let mut fx = Fx::picker();
    fx.nodes(&["atom", "win", "dep"])
        .prereqs("win", &["atom"])
        .prereqs("dep", &["win"])
        .problem("1", problem(&["dep"]));
    let ev = evidence(vec![solve("1", &[("win", "clean")], 1)]);
    let st = statuses(&[
        ("atom", MISSING, None),
        ("win", SOLID, Some(1)),
        ("dep", STALE, Some(300)),
    ]);
    fx.stubs().bank = set(&["atom", "win"]);
    fx.stubs().undone = set(&["atom", "win"]);
    assert_eq!(
        t3(&fx.run(&ev, &st, args())),
        tup("atom", MISSING, "drill:atom")
    );
}

/// 2026-08-31 (make simulate): dedupe siblings waited on start-index,
/// start-index on choose-undo, and choose-undo was SOLID through an
/// assisted rep. Rule 0c found start-index, saw it parked, and gave up;
/// nothing named choose-undo for 14 simulated days. It climbs now.
#[test]
fn rule_0c_climbs_a_hold_chain_to_its_root() {
    let mut fx = Fx::picker();
    fx.nodes(&["cu", "si", "dd"])
        .prereqs("si", &["cu"])
        .prereqs("dd", &["si"])
        .problem("1", problem(&["dd"]));
    fx.stubs().bank = set(&["cu", "si", "dd"]);
    fx.stubs().undone = set(&["si"]);
    let ev = evidence(vec![
        solve_a("8", &[("cu", "clean")], 1, level("walkthrough")),
        solve("9", &[("si", "clean")], 1),
    ]);
    let st = statuses(&[
        ("dd", FRAGILE, Some(1)),
        ("si", SOLID, Some(1)),
        ("cu", SOLID, Some(1)),
    ]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("cu", SOLID, "drill:cu"));
    assert!(reason(&c).contains("own it unaided"));
}

/// 2026-08-31 (make simulate): 102 is the one carrier of the level BFS
/// and waits on drill d67; ordinary STALE is not drill-gated, so the
/// stale rule offered nothing for 60 simulated days. No carrier can fire,
/// so the drill is the rep.
#[test]
fn a_stale_move_whose_carriers_are_all_held_gets_its_drill() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problems(vec![
        ("1", problem(&["a"]).after(&["9"])),
        ("9", problem(&["b"])),
    ]);
    fx.stubs().bank = set(&["a"]);
    let ev = evidence(vec![solve("1", &[("a", "clean")], 20)]);
    let st = statuses(&[("a", STALE, Some(20)), ("b", SOLID, Some(1))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("a", STALE, "drill:a"));
}

/// 2026-08-31 (make simulate): 310 carries topological order and waits
/// on 210, which waits on 207; every move of 207 was SOLID, so no rule
/// re-solved it and it never warmed - 47 simulated days. The root of the
/// chain is served, as the problem its own moves name.
#[test]
fn a_held_carrier_serves_the_root_predecessor_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problems(vec![
        ("1", problem(&["a"]).after(&["9"])),
        ("9", problem(&["b"]).after(&["8"])),
        ("8", problem(&["b"])),
    ]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean")], 20),
        solve("8", &[("b", "clean")], 140),
        solve("8", &[("b", "clean")], 100),
    ]);
    let st = statuses(&[("a", STALE, Some(20)), ("b", SOLID, Some(1))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("b", SOLID, "8"));
    assert!(reason(&c).contains("waits on 8"));
}

/// A Hard is a summit, not a refresh: the hold rule leaves it alone, and
/// the summit rule takes it on its own terms.
#[test]
fn a_held_carrier_behind_a_hard_serves_nothing() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problems(vec![
        ("1", problem(&["a"]).after(&["9"])),
        ("9", hard(&["b"])),
    ]);
    let ev = evidence(vec![solve("1", &[("a", "clean")], 20)]);
    let st = statuses(&[("a", STALE, Some(20)), ("b", SOLID, Some(1))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(pnum(&c), "9");
    assert!(reason(&c).contains("summit"));
}

/// Every id in an "after" list (problems.json, drills.json) names a
/// problem, a bank drill, or a node; every drills.json title names a bank
/// file; every bank file has an id; the drill edges have no cycle. A
/// dangling id holds nothing, silently; this is where it gets caught.
#[test]
fn every_after_id_in_the_real_graph_resolves() {
    let (ctx, _) = Ctx::load(repo_root());
    let problems = ctx.evidenced();
    let mut bad: Vec<String> = Vec::new();
    for (pnum, p) in &problems {
        for pred in &p.after {
            if ctx.vertex_kind(pred, &problems).is_none() {
                bad.push(format!("{pnum} {pred}: nothing carries this id"));
            }
        }
    }
    let id_re = regex::Regex::new(r"^d\d+$").unwrap();
    for (did, d) in &ctx.drills {
        if !id_re.is_match(did) {
            bad.push(format!("{did}: not a drill id"));
        }
        if ctx.drill_path(did).is_none() {
            bad.push(format!("{did} {}: no bank file", d.title));
        }
        for pred in &d.after {
            if ctx.vertex_kind(pred, &problems).is_none() {
                bad.push(format!("{did} {pred}: nothing carries this id"));
            }
        }
    }
    let titles: HashSet<&String> = ctx.drills.values().map(|d| &d.title).collect();
    assert_eq!(titles.len(), ctx.drills.len(), "two ids for one title");
    for path in ctx.every_bank_path() {
        if ctx.drill_id(&path).is_none() {
            bad.push(format!(
                "{}: bank file with no id in drills.json",
                path.display()
            ));
        }
    }
    assert!(bad.is_empty(), "{bad:?}");

    fn cyclic(ctx: &Ctx, did: &str, seen: &[&str]) -> bool {
        if seen.contains(&did) {
            return true;
        }
        let mut path = seen.to_vec();
        path.push(did);
        ctx.drills
            .get(did)
            .map(|d| &d.after)
            .into_iter()
            .flatten()
            .filter(|a| ctx.drills.contains_key(a.as_str()))
            .any(|a| cyclic(ctx, a, &path))
    }
    let cycles: Vec<&String> = ctx.drills.keys().filter(|t| cyclic(&ctx, t, &[])).collect();
    assert!(cycles.is_empty(), "{cycles:?}");
}

// --------------------------------------------------------------------------
// the cross-bank ladder: drills gate one another through node prereqs
// --------------------------------------------------------------------------

/// The dedupe-siblings case: the dependent's drill waits and its carrier
/// stays held; the rusty base gets served instead - on its own drill,
/// since it has a bank (2026-09-02: the bank is the move, the problem is
/// the test).
#[test]
fn a_drill_is_held_while_its_banked_prereq_is_not_solid() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .problems(vec![("1", problem(&["dep"])), ("2", problem(&["base"]))]);
    fx.stubs().bank = set(&["base", "dep"]);
    let st = statuses(&[("dep", FRAGILE, Some(1)), ("base", STALE, Some(50))]);
    assert_eq!(
        t3(&fx.run(&no_evidence(), &st, args())),
        tup("base", STALE, "drill:base")
    );
}

/// No bank: the spaced re-solve stays on the carrier.
#[test]
fn a_stale_move_without_a_bank_re_solves_its_carrier() {
    let mut fx = Fx::picker();
    fx.nodes(&["base"]).problem("2", problem(&["base"]));
    let st = statuses(&[("base", STALE, Some(50))]);
    assert_eq!(
        t3(&fx.run(&no_evidence(), &st, args())),
        tup("base", STALE, "2")
    );
}

/// A hold nothing can open is a deadlock: an unbanked prereq releases.
#[test]
fn a_prereq_without_a_bank_holds_nothing() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .problem("1", problem(&["dep"]));
    fx.stubs().bank = set(&["dep"]);
    let st = statuses(&[("dep", FRAGILE, Some(1)), ("base", STALE, Some(50))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "drill:dep");
}

/// SOLID standing on an unaided clean: the base is owned.
#[test]
fn a_solid_prereq_releases_the_drill() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .problem("1", problem(&["dep"]));
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![solve("9", &[("base", "clean")], 1)]);
    let st = statuses(&[("dep", FRAGILE, Some(1)), ("base", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:dep");
}

/// If it got assisted then it's not clean: SOLID reached through a
/// walkthrough rep is re-learning, not ownership - the dependent waits
/// for the unaided rep. And that rep gets SERVED (rule 0c): the prereq is
/// SOLID, so rules 1-3 would never target it, and a hold nothing serves
/// is a deadlock - 18 nodes sat behind two such prereqs on 2026-08-29.
#[test]
fn an_assisted_clean_on_the_prereq_still_holds() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .problem("1", problem(&["dep"]));
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![solve_a(
        "9",
        &[("base", "clean")],
        1,
        level("walkthrough"),
    )]);
    let st = statuses(&[("dep", FRAGILE, Some(1)), ("base", SOLID, Some(1))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("base", SOLID, "drill:base"));
    assert!(reason(&c).contains("own it unaided"));
    // the dependent is reported as waiting on it, not as a dry node
    let b = fx.blocked(&ev, &st, &[], &[]);
    let [(nid, _, why, dry)] = b.as_slice() else {
        panic!("{b:?}")
    };
    assert_eq!((nid.as_str(), *dry), ("dep", false));
    assert!(why.contains("held behind base"));
}

#[test]
fn the_ownership_rep_releasing_the_most_held_moves_goes_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b", "d1", "d2", "d3"])
        .prereqs("d1", &["a"])
        .prereqs("d2", &["a"])
        .prereqs("d3", &["b"]);
    fx.stubs().bank = set(&["a", "b", "d1", "d2", "d3"]);
    let ev = evidence(vec![solve_a(
        "9",
        &[("a", "clean"), ("b", "clean")],
        1,
        level("hint"),
    )]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("d1", MISSING, None),
        ("d2", MISSING, None),
        ("d3", MISSING, None),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:a");
    // its drill done for today: the next prereq is served, never the dependents
    fx.stubs().drilled_today = set(&["a"]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:b");
    fx.stubs().drilled_today = set(&["a", "b"]);
    assert!(fx.run(&ev, &st, args()).is_none());
}

/// Rule 0c reaches floor-due SOLID targets too. sql-anti-join was due on
/// its floor, its drill held behind sql-join-left-keep with drills undone,
/// and nothing served the prereq; the floor fell through to 2115. The
/// prereq's undone drill goes first, the problem waits (2026-09-02).
#[test]
fn a_floor_due_move_held_behind_a_prereq_serves_the_prereq_drill() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .problem("1", easy(&["dep"]));
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![
        solve("8", &[("base", "clean")], 30),
        solve("9", &[("dep", "clean")], 5),
    ]);
    let st = statuses(&[("base", SOLID, Some(30)), ("dep", SOLID, Some(5))]);
    fx.stubs().undone = set(&["base"]);
    assert_eq!(
        t3(&fx.run(&ev, &st, args())),
        tup("base", SOLID, "drill:base")
    );
}

#[test]
fn cram_skips_the_ownership_rep() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"]).prereqs("dep", &["base"]);
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![solve_a("9", &[("base", "clean")], 1, level("hint"))]);
    let st = statuses(&[("dep", MISSING, None), ("base", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&ev, &st, args().cram())), "drill:dep");
}

/// `make next sql cram early`: nothing rusty in the group, yet every
/// SOLID node with a rung left is served, base before dependent.
#[test]
fn early_reviews_solid_nodes_prereqs_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep", "other"])
        .prereqs("dep", &["base"])
        .group(&["base", "dep"], "g")
        .group(&["other"], "elsewhere");
    fx.stubs().bank = set(&["base", "dep", "other"]);
    let ev = evidence(vec![solve("9", &[("base", "clean"), ("dep", "clean")], 1)]);
    let st = statuses(&[
        ("base", SOLID, Some(1)),
        ("dep", SOLID, Some(1)),
        ("other", SOLID, Some(1)),
    ]);
    assert!(fx.run(&ev, &st, args().group("g")).is_none());
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:base"
    );
    fx.stubs().drilled_today = set(&["base"]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:dep"
    );
    fx.stubs().drilled_today = set(&["base", "dep"]);
    assert!(fx.run(&ev, &st, args().group("g").early()).is_none());
}

/// The 2026-08-30 spark serve: `make next spark cram early` jumped
/// straight to the MISSING window node. Early means the whole group in
/// ladder order - the SOLID prereqs are jogged first, the new move after.
#[test]
fn early_walks_the_ladder_missing_after_its_solid_prereqs() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .group(&["base", "dep"], "g");
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![solve("9", &[("base", "clean")], 1)]);
    let st = statuses(&[("base", SOLID, Some(1)), ("dep", MISSING, None)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args().group("g"))), "drill:dep");
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:base"
    );
    fx.stubs().drilled_today = set(&["base"]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:dep"
    );
}

/// The 2026-08-29 empty serve: pair-count-formula's one carrier was
/// solved three days ago, pick() skipped it as not cooled, and the old
/// blocked_frontier (which never applied cooled) called it servable - so
/// --why printed nothing and the headline claimed the bank was starved.
#[test]
fn a_node_whose_only_carrier_is_cooling_is_waiting_not_dry() {
    let mut fx = Fx::picker();
    fx.nodes(&["t"]).problem("2475", easy(&["t"]));
    let ev = evidence(vec![solve("2475", &[("t", "clean")], 3)]);
    let st = statuses(&[("t", STALE, Some(55))]);
    assert!(fx.run(&ev, &st, args()).is_none());
    let b = fx.blocked(&ev, &st, &[], &[]);
    let [(nid, _, why, dry)] = b.as_slice() else {
        panic!("{b:?}")
    };
    assert_eq!((nid.as_str(), *dry), ("t", false));
    assert!(why.contains(&format!("carrier 2475 cools {}", iso(-2))));
}

#[test]
fn a_node_whose_carrier_is_asleep_names_the_park() {
    let mut fx = Fx::picker();
    fx.nodes(&["t"]).problem("7", problem(&["t"]));
    let st = statuses(&[("t", STALE, Some(55))]);
    let b = fx.blocked(&no_evidence(), &st, &["7"], &[]);
    let [(nid, _, why, dry)] = b.as_slice() else {
        panic!("{b:?}")
    };
    assert_eq!((nid.as_str(), *dry), ("t", false));
    assert!(why.contains("7 is asleep") && why.contains("make wake"));
}

/// The plan-serving clause: judgment may order items freely, so a
/// dependent's drill item waits while the prereq's item is still pending.
#[test]
fn a_pending_plan_drill_for_the_prereq_holds_the_dependent() {
    let mut fx = Fx::new();
    fx.nodes(&["base", "dep"]).prereqs("dep", &["base"]);
    let st = statuses(&[("base", SOLID, Some(1)), ("dep", STALE, Some(300))]);
    let ctx = fx.ctx(); // no bank anywhere
    assert!(drill_held(
        &ctx,
        "dep",
        &st,
        &no_evidence(),
        &set(&["base"])
    ));
    assert!(!drill_held(
        &ctx,
        "dep",
        &st,
        &no_evidence(),
        &HashSet::new()
    ));
}

/// Drills sit on the same forgetting curve as problems: a node SOLID on
/// an unaided clean is not re-served, whatever flagged it - once every
/// drill of the node has been done. A never-done drill is still due: one
/// clean drill does not stand for the others (2026-08-31, a clean Pairs
/// marked start-index solid with five drills, subsets included, untouched).
#[test]
fn a_solid_owned_node_has_no_drill_due() {
    let fx = Fx::new();
    let d0 = fx.bank_file("some-node", "d0.py", "DRILL: Only One\n");
    let done = drill_file("solved/d_Only_One_1.py", "some-node", 5, Assist::None);
    let ev = evidence(vec![solve("7", &[("some-node", "clean")], 2), done.clone()]);
    assert_eq!(due(&fx, "some-node", &ev), None);
    let assisted = evidence(vec![
        solve_a("7", &[("some-node", "clean")], 2, level("walkthrough")),
        done,
    ]);
    assert!(due(&fx, "some-node", &assisted).is_some());
    let undone = evidence(vec![solve("7", &[("some-node", "clean")], 2)]);
    assert_eq!(due(&fx, "some-node", &undone), Some(d0));
}

/// 2026-08-31: Combinations was done once with a walkthrough, so Reuse
/// Allowed and Subsets above it stayed held; every released rung had a
/// rep, the node read done, and the dedupe drill got served with subsets
/// never done. A rung held by the warm rule counts as ladder left, and the
/// assisted rung below it is what gets served. A rung held only because
/// another node is not owned does not count - nothing here clears it.
#[test]
fn an_assisted_rung_with_undone_rungs_above_it_is_served_again() {
    let mut fx = Fx::new();
    let d0 = fx.bank_file("some-node", "d0.py", "DRILL: Lower\nTRAINS: some-node\n");
    fx.bank_file("some-node", "d1.py", "DRILL: Upper\nTRAINS: some-node\n");
    fx.register(&[("d1", "Lower", &[]), ("d2", "Upper", &["d1"])]);
    let lower = drill_file("solved/d_Lower_1.py", "some-node", 5, level("walkthrough"));
    let ev = evidence(vec![solve("7", &[("some-node", "clean")], 2), lower]);
    assert!(drills_left(&fx.ctx(), "some-node", &ev, false));
    assert_eq!(due(&fx, "some-node", &ev), Some(d0));
    fx.bank_file(
        "some-node",
        "d1.py",
        "DRILL: Upper\nTRAINS: some-node, other\n",
    );
    let unaided = drill_file("solved/d_Lower_1.py", "some-node", 5, Assist::None);
    let ev = evidence(vec![solve("7", &[("some-node", "clean")], 2), unaided]);
    assert!(!drills_left(&fx.ctx(), "some-node", &ev, false));
}

/// 2026-08-31: every sql node SOLID, `make next sql` spent, `cram early`
/// walking the group from the bottom through drills already owned three
/// times over. `assisted` is the early walk restricted to drills whose
/// latest rep was a hint, a walkthrough, a learning rep or a struggle: the
/// ones still waiting for their unaided rep. Never-done drills are not in
/// it, an owned drill is not in it, and the once-a-day rule still holds.
#[test]
fn assisted_serves_only_drills_whose_latest_rep_was_assisted() {
    let fx = Fx::new();
    let mut paths = vec![];
    for (i, t) in ["Owned", "Hinted", "Learning", "Fresh"].iter().enumerate() {
        paths.push(fx.bank_file(
            "some-node",
            &format!("r{i}.py"),
            &format!("DRILL: {t}\nTRAINS: some-node\n"),
        ));
    }
    let reps = vec![
        drill_file("solved/d_Owned_1.py", "some-node", 3, Assist::None),
        drill_file("solved/d_Hinted_1.py", "some-node", 2, level("hint")),
        drill_file(
            "solved/d_Learning_1.py",
            "some-node",
            1,
            assist_map(&[("some-node", "learning")]),
        ),
    ];
    let mut all = vec![solve("7", &[("some-node", "clean")], 1)];
    all.extend(reps.clone());
    let ev = evidence(all.clone());
    assert_eq!(due_assisted(&fx, "some-node", &ev), Some(paths[1].clone()));
    all.push(drill_file(
        "solved/d_Hinted_2.py",
        "some-node",
        0,
        Assist::None,
    ));
    let ev = evidence(all.clone());
    assert_eq!(due_assisted(&fx, "some-node", &ev), Some(paths[2].clone()));
    all.push(drill_file(
        "solved/d_Learning_2.py",
        "some-node",
        0,
        level("hint"),
    ));
    let ev = evidence(all);
    assert_eq!(due_assisted(&fx, "some-node", &ev), None); // today
}

/// `assisted` implies early: SOLID nodes are served, prereqs before
/// dependents, and the reason names the walk.
#[test]
fn assisted_walks_the_group_prereqs_first_whatever_the_status() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .group(&["base", "dep"], "g");
    fx.stubs().bank = set(&["base", "dep"]);
    let st = statuses(&[("base", SOLID, Some(0)), ("dep", SOLID, Some(0))]);
    let ev = evidence(vec![solve("7", &[("base", "clean"), ("dep", "clean")], 0)]);
    let got = fx.run(&ev, &st, args().group("g").assisted());
    assert_eq!(pnum(&got), "drill:base");
    assert!(reason(&got).starts_with("assisted review"));
    fx.stubs().drilled_today = set(&["base"]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").assisted())),
        "drill:dep"
    );
}

/// 2026-08-31: Pairs (two for loops) went clean, start-index read SOLID,
/// and the picker served the dedupe drill with subsets never done. A
/// solid prereq with drills undone is served its next drill; the
/// dependent waits.
#[test]
fn picker_serves_the_next_undone_drill_of_a_solid_prereq() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"]).prereqs("dep", &["base"]);
    fx.stubs().bank = set(&["base", "dep"]);
    fx.stubs().undone = set(&["base"]);
    let st = statuses(&[("base", SOLID, Some(0)), ("dep", FRAGILE, Some(300))]);
    let ev = evidence(vec![solve("7", &[("base", "clean")], 0)]);
    let got = fx.run(&ev, &st, args());
    assert_eq!(pnum(&got), "drill:base");
    assert!(reason(&got).starts_with("next undone drill"));
    fx.stubs().undone = HashSet::new();
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:dep");
}

/// A prereq node with drills never done does not unlock the node after
/// it, and the picker serves the prereq's next undone drill instead.
#[test]
fn undone_drills_hold_the_dependent_and_get_served() {
    let mut fx = Fx::new();
    fx.bank_file("base", "b0.py", "DRILL: B Zero\nTRAINS: base\n");
    let b1 = fx.bank_file("base", "b1.py", "DRILL: B One\nTRAINS: base\n");
    fx.register(&[("d1", "B Zero", &[]), ("d2", "B One", &["d1"])]);
    fx.nodes(&["base", "dep"]).prereqs("dep", &["base"]);
    let st = statuses(&[("base", SOLID, Some(0)), ("dep", STALE, Some(300))]);
    let b0 = drill_file("solved/d_B_Zero_1.py", "base", 0, Assist::None);
    let ev = evidence(vec![b0.clone()]);
    let ctx = fx.ctx();
    assert!(drill_held(&ctx, "dep", &st, &ev, &HashSet::new()));
    assert_eq!(due(&fx, "base", &ev), Some(b1));
    let ev2 = evidence(vec![
        b0,
        drill_file("solved/d_B_One_1.py", "base", 0, Assist::None),
    ]);
    let ctx = fx.ctx();
    assert!(!drill_held(&ctx, "dep", &st, &ev2, &HashSet::new()));
    assert_eq!(due(&fx, "base", &ev2), None);
}

/// Assist is per move. 1004 on 2026-08-17: the hint was on the sliding
/// window bookkeeping, the prefix sums were the operator's own, yet the
/// solve-level flag stamped both, and `owned` then held every drill
/// behind prefix-sums for an unaided rep of a move with three unaided
/// reps the week before. With {move: level}, only the helped move is
/// unowned; the bare-string form still means the whole walk.
#[test]
fn a_hint_on_one_move_does_not_taint_the_rest_of_the_walk() {
    let (_, r) = solve_a(
        "1004",
        &[("window", "clean"), ("prefix", "clean")],
        1,
        assist_map(&[("window", "hint")]),
    );
    assert_eq!(r.assist_for("window"), "hint");
    assert_eq!(r.assist_for("prefix"), "none");
    assert_eq!(r.assist_any(), "hint"); // the solve as a whole
    let ev = evidence(vec![solve_a(
        "1004",
        &[("window", "clean"), ("prefix", "clean")],
        1,
        assist_map(&[("window", "hint")]),
    )]);
    assert!(owned(&ev, "prefix"));
    assert!(!owned(&ev, "window"));
    let legacy = evidence(vec![solve_a(
        "1004",
        &[("window", "clean"), ("prefix", "clean")],
        1,
        level("hint"),
    )]);
    assert!(!owned(&legacy, "prefix"));
    // and the picker serves the ownership rep for the helped move only
    let mut fx = Fx::picker();
    fx.nodes(&["window", "prefix", "dep"])
        .prereqs("dep", &["window", "prefix"]);
    fx.stubs().bank = set(&["window", "prefix", "dep"]);
    let st = statuses(&[
        ("window", SOLID, Some(1)),
        ("prefix", SOLID, Some(1)),
        ("dep", MISSING, None),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:window");
    // prefix is never served as an ownership rep; once window's rep is done
    // for today nothing else is held open (dep waits for that evidence to land)
    fx.stubs().drilled_today = set(&["window"]);
    assert!(fx.run(&ev, &st, args()).is_none());
}

/// node_status reads the per-move level too: a learning move earns no
/// clean rep, the other move in the same walk does.
#[test]
fn a_learning_move_is_censored_only_for_itself() {
    let fx = Fx::new();
    let ev = evidence(vec![solve_a(
        "9",
        &[("a", "clean"), ("b", "clean")],
        1,
        assist_map(&[("a", "learning")]),
    )]);
    let ctx = fx.ctx();
    assert_eq!(node_status(&ctx, "a", &ev, today()).0, FRAGILE);
    assert_eq!(node_status(&ctx, "b", &ev, today()).0, SOLID);
}

/// A rung whose TRAINS lists a second node is a walk, not a move: it is
/// held until that node is owned (its own atomic rung clean, unaided), the
/// way a carrier waits for every other move in its walk to be SOLID. The
/// ladder below it still applies, and the first rung is never held.
#[test]
fn a_composite_rung_waits_for_every_move_it_combines() {
    let mut fx = Fx::new();
    let r1 = fx.bank_file(
        "left-keep",
        "r1.py",
        "\"\"\"\nDRILL: R One\nTRAINS: left-keep\n\"\"\"\n",
    );
    let r2 = fx.bank_file(
        "left-keep",
        "r2.py",
        "\"\"\"\nDRILL: R Two\nTRAINS: left-keep, group-agg\n\"\"\"\n",
    );
    fx.register(&[("d1", "R One", &[]), ("d2", "R Two", &["d1"])]);
    let cands = vec![r1.clone(), r2.clone()];
    let serv = |ev: &Evidence, cands: &[PathBuf]| {
        servable_drills(&fx.ctx(), cands, ev, Some("left-keep"), false)
    };
    // r1 warm (clean, unaided, recent) but group-agg never owned: r2 stays held
    let one = drill_file("solved/d_R_One_1.py", "left-keep", 3, Assist::None);
    let ev = evidence(vec![one.clone()]);
    assert_eq!(serv(&ev, &cands), vec![r1.clone()]);
    // group-agg owned only through a hinted rep: still held
    let ev2 = evidence(vec![
        one.clone(),
        solve_a("5", &[("group-agg", "clean")], 1, level("hint")),
    ]);
    assert_eq!(serv(&ev2, &cands), vec![r1.clone()]);
    // an unaided clean on group-agg releases it
    let ev3 = evidence(vec![one, solve("5", &[("group-agg", "clean")], 1)]);
    assert_eq!(serv(&ev3, &cands), vec![r1.clone(), r2.clone()]);
    // order of the candidates is not an edge
    assert_eq!(serv(&ev3, &[r2.clone(), r1.clone()]), vec![r2, r1]);
}

/// The 2026-08-30 spark serve: `make next spark cram early` swept one
/// rung per node, so plan-shuffles came round with five group-agg atoms
/// unseen. Early is depth first - a dependent waits while an in-scope
/// prereq's bank still has an undrilled released rung.
#[test]
fn early_walks_one_ladder_to_the_top_before_the_node_above_it() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .group(&["base", "dep"], "g");
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![solve_a("9", &[("base", "clean")], 1, level("hint"))]);
    let st = statuses(&[("base", SOLID, Some(1)), ("dep", MISSING, None)]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:base"
    );
    // base repped today but its ladder not done: dep still waits, and the
    // base has nothing due either - the serve is empty, not a skip ahead
    fx.stubs().drilled_today = set(&["base"]);
    fx.stubs().undone = set(&["base"]);
    assert!(fx.run(&ev, &st, args().group("g").early()).is_none());
    fx.stubs().undone = HashSet::new();
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:dep"
    );
}

/// Outside cram a rung releases the one above only on an unaided clean
/// (drill_warm). In the early walk a hinted clean is enough, so a ladder
/// is climbed in one sitting instead of one rung per day.
#[test]
fn the_cram_ladder_climbs_on_an_assisted_clean() {
    let mut fx = Fx::new();
    let r1 = fx.bank_file(
        "group-agg",
        "r1.py",
        "\"\"\"\nDRILL: R One\nTRAINS: group-agg\n\"\"\"\n",
    );
    let r2 = fx.bank_file(
        "group-agg",
        "r2.py",
        "\"\"\"\nDRILL: R Two\nTRAINS: group-agg\n\"\"\"\n",
    );
    fx.register(&[("d1", "R One", &[]), ("d2", "R Two", &["d1"])]);
    let cands = vec![r1.clone(), r2.clone()];
    let one = drill_file("solved/d_R_One_1.py", "group-agg", 0, level("hint"));
    let ev = evidence(vec![one.clone()]);
    assert_eq!(
        servable_drills(&fx.ctx(), &cands, &ev, Some("group-agg"), false),
        vec![r1.clone()]
    );
    assert_eq!(
        servable_drills(&fx.ctx(), &cands, &ev, Some("group-agg"), true),
        vec![r1, r2.clone()]
    );
    assert_eq!(due_early(&fx, "group-agg", &ev), Some(r2));
    assert!(drills_left(&fx.ctx(), "group-agg", &ev, true));
    let ev2 = evidence(vec![
        one,
        drill_file("solved/d_R_Two_1.py", "group-agg", 0, Assist::None),
    ]);
    assert!(!drills_left(&fx.ctx(), "group-agg", &ev2, true));
}

/// The 2026-08-30 `make next spark cram early` traceback: two reps of
/// one rung on the same date tied on the sort key and the comparison fell
/// through to the records. The later solved file (timestamp in its name)
/// is the latest rep.
#[test]
fn two_same_day_reps_of_one_drill_do_not_crash_the_ladder() {
    let fx = Fx::new();
    let r1 = fx.bank_file("n", "r1.py", "\"\"\"\nDRILL: R One\nTRAINS: n\n\"\"\"\n");
    let t1 = drill_file("solved/d_R_One_2026_08_30T01.py", "n", 0, Assist::None);
    let (f2, mut rec2) = drill_file("solved/d_R_One_2026_08_30T02.py", "n", 0, Assist::None);
    rec2.moves.insert("n".into(), "struggled".into());
    let ev = evidence(vec![t1.clone(), (f2.clone(), rec2.clone())]);
    let ctx = fx.ctx();
    assert!(!drill_clean(&ctx, &r1, &ev));
    assert!(!drill_warm(&ctx, &r1, &ev, today()));
    let ev = evidence(vec![
        t1,
        (f2, rec2),
        drill_file("solved/d_R_One_2026_08_30T03.py", "n", 0, Assist::None),
    ]);
    let ctx = fx.ctx();
    assert!(drill_clean(&ctx, &r1, &ev));
    assert!(drill_warm(&ctx, &r1, &ev, today()));
}

/// `make next sql cram` lifts the cross-bank hold and nothing else: a
/// SOLID node owned by an unaided clean is still not re-served. That is
/// what `early` adds.
#[test]
fn cram_keeps_the_curve() {
    let mut fx = Fx::picker();
    fx.nodes(&["base"]).group(&["base"], "g");
    fx.stubs().bank = set(&["base"]);
    let ev = evidence(vec![solve("9", &[("base", "clean")], 1)]);
    let st = statuses(&[("base", SOLID, Some(1))]);
    // due_drill (stubbed) follows the real one: an owned SOLID node is not
    // due outside early, so neither the curve nor cram serves it
    fx.stubs().due_early_only = true;
    assert!(fx.run(&ev, &st, args().group("g").cram()).is_none());
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:base"
    );
}

/// The group scope survives cram: a held node in another group is not
/// what `make next sql cram` releases.
#[test]
fn cram_stays_inside_the_group() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep", "far"])
        .prereqs("dep", &["base"])
        .prereqs("far", &["base"])
        .group(&["base", "dep"], "g")
        .group(&["far"], "elsewhere");
    fx.stubs().bank = set(&["base", "dep", "far"]);
    let ev = evidence(vec![solve_a("9", &[("base", "clean")], 1, level("hint"))]);
    let st = statuses(&[
        ("base", SOLID, Some(1)),
        ("dep", MISSING, None),
        ("far", MISSING, None),
    ]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").cram())),
        "drill:dep"
    );
    fx.stubs().drilled_today = set(&["dep"]);
    assert!(fx.run(&ev, &st, args().group("g").cram()).is_none());
}

/// Cram drops the "prereq owned by an unaided rep" hold only. A prereq
/// that is not SOLID at all is the more urgent gap: it is served first,
/// and the MISSING dependent still waits for it to turn SOLID - the ZPD
/// rule, which cram does not touch.
#[test]
fn cram_lifts_the_ownership_bar_not_the_solid_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["base", "dep"])
        .prereqs("dep", &["base"])
        .group(&["base", "dep"], "g");
    fx.stubs().bank = set(&["base", "dep"]);
    let ev = evidence(vec![solve("9", &[("base", "struggled")], 1)]);
    let mut st = statuses(&[("base", FRAGILE, Some(1)), ("dep", MISSING, None)]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").cram())),
        "drill:base"
    );
    fx.stubs().drilled_today = set(&["base"]);
    assert!(fx.run(&ev, &st, args().group("g").cram()).is_none());
    st.insert("base".into(), (SOLID, Some(ago(0))));
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").cram())),
        "drill:dep"
    );
}

/// a -> b -> c in one group: a's whole ladder, then b's, then c's. c is
/// held by b's unfinished ladder even while a is done, so the walk never
/// skips a level.
#[test]
fn early_walks_a_chain_bottom_up_one_ladder_at_a_time() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b", "c"])
        .prereqs("b", &["a"])
        .prereqs("c", &["b"])
        .group(&["a", "b", "c"], "g");
    fx.stubs().bank = set(&["a", "b", "c"]);
    let ev = evidence(vec![solve("9", &[("a", "clean"), ("b", "clean")], 1)]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("c", MISSING, None),
    ]);
    fx.stubs().undone = set(&["a", "b", "c"]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:a"
    );
    fx.stubs().drilled_today = set(&["a"]);
    assert!(fx.run(&ev, &st, args().group("g").early()).is_none());
    fx.stubs().undone.remove("a");
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:b"
    );
    fx.stubs().drilled_today = set(&["a", "b"]);
    assert!(fx.run(&ev, &st, args().group("g").early()).is_none());
    fx.stubs().undone.remove("b");
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("g").early())),
        "drill:c"
    );
}

/// A spark node's sql prereqs are out of scope for `make next spark cram
/// early`: their unfinished ladders do not hold the spark walk, and they
/// are never served by it.
#[test]
fn early_is_not_held_by_a_prereq_outside_the_group() {
    let mut fx = Fx::picker();
    fx.nodes(&["sql-base", "spark-dep"])
        .prereqs("spark-dep", &["sql-base"])
        .group(&["spark-dep"], "spark")
        .group(&["sql-base"], "sql");
    fx.stubs().bank = set(&["sql-base", "spark-dep"]);
    let ev = evidence(vec![solve_a(
        "9",
        &[("sql-base", "clean")],
        1,
        level("hint"),
    )]);
    let st = statuses(&[("sql-base", SOLID, Some(1)), ("spark-dep", MISSING, None)]);
    fx.stubs().undone = set(&["sql-base", "spark-dep"]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().group("spark").early())),
        "drill:spark-dep"
    );
}

/// `make next sql cram early` with -n 2: the second pick excludes the
/// first drill and goes to the next node in ladder order, not the same
/// node twice.
#[test]
fn early_with_two_picks_moves_on_to_the_next_ladder() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).group(&["a", "b"], "g");
    fx.stubs().bank = set(&["a", "b"]);
    let ev = evidence(vec![solve("9", &[("a", "clean"), ("b", "clean")], 1)]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let first = fx.run(&ev, &st, args().group("g").early());
    assert_eq!(pnum(&first), "drill:a");
    let second = fx.run(&ev, &st, args().group("g").early().exclude(&["drill:a"]));
    assert_eq!(pnum(&second), "drill:b");
}

/// A new drill on a known move (Reuse Allowed on start-index, 2026-09-01):
/// he copied the answer. That is first exposure to the drill, not a failed
/// recall of the move, so the node keeps ownership and the copy counts as
/// a clean rep; the same help on the drill's SECOND rep is a real assist.
/// The drill itself still waits for an unaided rep either way.
#[test]
fn the_first_rep_of_a_drill_is_unaided_at_the_node() {
    let mut fx = Fx::new();
    fx.bank("sw", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problem("713", problem(&["sw"]).after(&["d1"]));
    let ev = evidence(vec![
        solve("9", &[("sw", "clean")], 20),
        drill_rep_a("Count by Contribution", "sw", 1, level("learning")),
    ]);
    assert!(owned(&ev, "sw"));
    let ctx = fx.ctx();
    assert_eq!(
        node_status(&ctx, "sw", &ev, today())
            .1
            .map(|d| d.format("%Y-%m-%d").to_string()),
        Some(iso(1))
    );
    assert_eq!(held(&fx, "713", &ev), Some("d1".into()));
    let second = evidence(vec![
        solve("9", &[("sw", "clean")], 20),
        drill_rep_a("Count by Contribution", "sw", 1, level("learning")),
        drill_rep_a("Count by Contribution", "sw", 0, level("hint")),
    ]);
    assert!(!owned(&second, "sw"));
}

/// 2026-09-06: Shake Hands was done once as a learning rep. The first
/// rep of a drill scores as unaided at the node level, so the node read
/// owned with no drills left and due_drill declined; the drill itself was
/// not warm, so Install Order after it stayed held, and topological order
/// starved 23 days. An owned node's drill whose latest rep was assisted
/// is still due: the unaided rep is what releases what comes after it.
/// An owned node whose drill is owned too holds as before.
#[test]
fn an_owned_node_still_serves_its_assisted_drill() {
    let mut fx = Fx::new();
    let s = fx.bank("some-node", "Shake", "s.py", "d1", &[]);
    let held = drill_rep_a(
        "Shake",
        "some-node",
        3,
        assist_map(&[("some-node", "learning")]),
    );
    let ev = evidence(vec![solve("7", &[("some-node", "clean")], 2), held]);
    assert!(owned(&ev, "some-node"));
    assert_eq!(due(&fx, "some-node", &ev), Some(s));
    let ev = evidence(vec![
        solve("7", &[("some-node", "clean")], 2),
        drill_rep("Shake", "some-node", 3),
    ]);
    assert_eq!(due(&fx, "some-node", &ev), None);
}

/// 2115 carries topological order and waits on Install Order (d2), the
/// target's own drill; Install Order waits on Shake Hands (d1) of another
/// node, done once assisted. The chain used to stop at the target's own
/// drill and serve nothing. It climbs to d1 and serves its node's drill.
#[test]
fn a_held_carrier_climbs_its_drills_after_chain() {
    let mut fx = Fx::picker();
    fx.bank("b", "Shake", "s.py", "d1", &[]);
    fx.bank("a", "Install", "i.py", "d2", &["d1"]);
    fx.nodes(&["a", "b"])
        .problem("1", problem(&["a"]).after(&["d2"]));
    fx.stubs().bank = set(&["b"]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean")], 20),
        solve("7", &[("b", "clean")], 2),
        drill_rep_a("Shake", "b", 3, assist_map(&[("b", "learning")])),
    ]);
    let st = statuses(&[("a", STALE, Some(20)), ("b", SOLID, Some(2))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("b", SOLID, "drill:b"));
    assert!(reason(&c).contains("waits on d1"));
}

/// 2026-09-06 (make simulate, once its filenames matched `make solved`):
/// every sql move is carried by drills alone, and once each drill had
/// been done once the owned node got no drill and had no carrier, so it
/// sat at its graduating floor for the whole run. At the floor the least
/// recently drilled bank file is served again; off the floor an owned
/// node with nothing left holds as before.
#[test]
fn a_move_at_its_floor_gets_its_bank_again() {
    let mut fx = Fx::new();
    fx.flat_window();
    let a = fx.bank("some-node", "Lower", "a.py", "d1", &[]);
    fx.bank("some-node", "Upper", "b.py", "d2", &[]);
    let floor = GRAD_LADDER_SPARSE[0];
    let reps = evidence(vec![
        drill_rep("Lower", "some-node", floor + 3),
        drill_rep("Upper", "some-node", floor),
    ]);
    assert!(owned(&reps, "some-node") && !drills_left(&fx.ctx(), "some-node", &reps, false));
    assert!(graduation_due(&reps, "some-node", 0).unwrap().0 <= today());
    assert_eq!(due(&fx, "some-node", &reps), Some(a));
    let reps = evidence(vec![
        drill_rep("Lower", "some-node", 10),
        drill_rep("Upper", "some-node", 5),
        drill_rep("Lower", "some-node", 1),
    ]); // a proof day
    assert!(graduation_due(&reps, "some-node", 0).unwrap().0 > today());
    assert_eq!(due(&fx, "some-node", &reps), None);
}
