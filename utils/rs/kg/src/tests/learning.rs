// Learning mode: a learning solve is no game, and a first sight waits on
// its cold gates.

use super::*;
use crate::learning::cold_gate;

fn cold(fx: &Fx, after: &[&str], ev: &Evidence, skip: &[&str]) -> Option<String> {
    cold_gate(&fx.ctx(), &strs(after), &fx.pv(), ev, today(), &set(skip))
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

/// 1366 comes after 2215 and 49. Neither solved: the first is served.
/// 2215 solved clean today: 49. Both clean: nothing holds 1366.
#[test]
fn the_first_gate_not_warm_is_served() {
    let mut fx = Fx::new();
    fx.nodes(&["q1"]).problems(vec![
        ("1366", problem(&["q1"]).after(&["2215", "49"])),
        ("2215", problem(&["q1"])),
        ("49", problem(&["q1"])),
    ]);
    let gates = ["2215", "49"];
    assert_eq!(cold(&fx, &gates, &no_evidence(), &[]), Some("2215".into()));
    let one = evidence(vec![solve("2215", &[("q1", "clean")], 0)]);
    assert_eq!(cold(&fx, &gates, &one, &[]), Some("49".into()));
    let both = evidence(vec![
        solve("2215", &[("q1", "clean")], 0),
        solve("49", &[("q1", "clean")], 3),
    ]);
    assert_eq!(cold(&fx, &gates, &both, &[]), None);
}

/// A clean solve older than SOLID_WINDOW_DAYS is cold again, a gate in
/// `skip` is passed over, and a drill in the list is the picker's.
#[test]
fn an_old_solve_is_cold_and_skip_and_drills_pass() {
    let mut fx = Fx::new();
    fx.bank("q1", "Count by Contribution", "d0.py", "d1", &[]);
    fx.problems(vec![("2215", problem(&["q1"])), ("49", problem(&["q1"]))]);
    let old = evidence(vec![solve(
        "2215",
        &[("q1", "clean")],
        crate::data::SOLID_WINDOW_DAYS + 1,
    )]);
    assert_eq!(cold(&fx, &["2215"], &old, &[]), Some("2215".into()));
    assert_eq!(
        cold(&fx, &["2215", "49"], &old, &["2215"]),
        Some("49".into())
    );
    assert_eq!(cold(&fx, &["d1"], &no_evidence(), &[]), None);
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
