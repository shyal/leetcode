// Learning mode: a learning solve is no game, and a first sight waits on
// its cold gates.

use super::*;
use crate::learning::{solved_clean, unmet_gate};

fn unmet(fx: &Fx, after: &[&str], ev: &Evidence) -> Option<String> {
    unmet_gate(&fx.ctx(), &strs(after), &fx.pv(), ev)
}

/// A learning solve is evidence for the moves but no game for the
/// rating, and the next scored rep of the problem is a repeat.
#[test]
fn a_learning_solve_is_no_game_and_the_next_rep_is_a_repeat() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"]).problem("1", problem(&["q1"]));
    let ctx = fx.ctx();
    *ctx.solve_times.borrow_mut() = Some(vec![]);
    let timed = |mut r: (String, Rec), learning: bool| {
        r.1.seconds = Some(600);
        r.1.learning = learning;
        r
    };
    let ev = evidence(vec![
        timed(solve("1", &[("q1", "struggled")], 5), true),
        timed(solve("1", &[("q1", "clean")], 0), false),
    ]);
    let games = crate::model::scored_games(&ctx, &ev);
    assert_eq!(games.len(), 1);
    assert!(!games[0].first);
}

/// 1366 comes after 2215 and 49. Neither solved: 2215 holds it. 2215
/// solved clean, however long ago: 49. Both clean: nothing holds it. A
/// struggled solve clears nothing.
#[test]
fn every_gate_must_be_solved_clean() {
    let mut fx = Fx::new();
    fx.nodes(&["q1"]).problems(vec![
        ("1366", problem(&["q1"]).after(&["2215", "49"])),
        ("2215", problem(&["q1"])),
        ("49", problem(&["q1"])),
    ]);
    let gates = ["2215", "49"];
    assert_eq!(unmet(&fx, &gates, &no_evidence()), Some("2215".into()));
    let one = evidence(vec![solve("2215", &[("q1", "clean")], 400)]);
    assert_eq!(unmet(&fx, &gates, &one), Some("49".into()));
    let both = evidence(vec![
        solve("2215", &[("q1", "clean")], 400),
        solve("49", &[("q1", "clean")], 3),
    ]);
    assert_eq!(unmet(&fx, &gates, &both), None);
    let struggled = evidence(vec![
        solve("2215", &[("q1", "clean")], 400),
        solve("49", &[("q1", "struggled")], 3),
    ]);
    assert_eq!(unmet(&fx, &gates, &struggled), Some("49".into()));
    assert_eq!(solved_clean(&struggled), set(&["2215"]));
}

/// A drill gate with no clean rep holds the problem; a banned gate
/// counts for nothing.
#[test]
fn a_drill_gate_holds_and_a_banned_gate_does_not() {
    let mut fx = Fx::new();
    fx.bank("q1", "Count by Contribution", "d0.py", "d1", &[]);
    let mut banned = problem(&["q1"]);
    banned.banned = true;
    fx.problems(vec![("506", banned)]);
    assert_eq!(unmet(&fx, &["d1"], &no_evidence()), Some("d1".into()));
    assert_eq!(unmet(&fx, &["506"], &no_evidence()), None);
}

/// Two gates on one target land in one "after" list, beside the gate it
/// had: a write per gate kept only the last one.
#[test]
fn two_gates_on_one_target_are_one_list() {
    use crate::queue::{merged_after, Gate};
    let mut fx = Fx::new();
    fx.nodes(&["q1"])
        .problems(vec![("1366", problem(&["q1"]).after(&["3"]))]);
    let gate = |g: &str| Gate {
        problem: "1366".into(),
        gate: g.into(),
        why: String::new(),
    };
    let merged = merged_after(&fx.ctx(), &[gate("49"), gate("2215"), gate("49")]);
    assert_eq!(
        merged,
        vec![("1366".to_string(), strs(&["3", "49", "2215"]))]
    );
}
