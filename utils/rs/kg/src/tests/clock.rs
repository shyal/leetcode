// The clocks: every bank file's SM-2 clock (DRILL_SCHEDULER=anki), a
// problem's own review clock (rule 2c), and the paid-only problems no
// clock may serve.

use chrono::Duration;

use super::*;
use crate::clock::{attempt_label, problem_due, PROBLEM_GRADUATING_DAYS};
use crate::data::test_env;
use crate::drills::{anki_due, anki_frontier, anki_next_if_good, due_drill};
use crate::pick::review_queue;
use crate::status::{graduation_due, owned};

// --------------------------------------------------------------------------
// the drill clock
// --------------------------------------------------------------------------

/// SM-2 per bank file: Good runs 1, 3, 8, 20, 50 days; Hard (a hinted
/// clean) stretches by 1.2; Again (a struggle, a walkthrough or a copy)
/// goes back to one day. A file never done has no clock and is due.
#[test]
fn the_anki_clock_grades_a_drill_file_from_its_own_reps() {
    let mut fx = Fx::new();
    let path = fx.bank("n", "Clock", "c.py", "d1", &[]);
    let ctx = fx.ctx();
    assert_eq!(anki_due(&ctx, &path, &no_evidence()), None);
    let mut ivl = vec![];
    let mut reps = vec![];
    for days in [60, 59, 56, 48, 28] {
        // 1, 3, 8, 20 apart
        reps.push(drill_rep("Clock", "n", days));
        ivl.push(anki_due(&ctx, &path, &evidence(reps.clone())).unwrap().1);
    }
    assert_eq!(ivl, vec![1, 3, 8, 20, 50]);
    let hard = evidence(vec![
        drill_rep("Clock", "n", 10),
        drill_rep_a("Clock", "n", 9, assist_map(&[("n", "hint")])),
    ]);
    assert_eq!(
        anki_due(&ctx, &path, &hard),
        Some((ago(9) + Duration::days(2), 2))
    );
    let again = evidence(vec![
        drill_rep("Clock", "n", 10),
        drill_rep("Clock", "n", 9),
        drill_rep_v("Clock", "n", 5, "struggled", Assist::None),
    ]);
    assert_eq!(
        anki_due(&ctx, &path, &again),
        Some((ago(5) + Duration::days(1), 1))
    );
    let copy = evidence(vec![drill_rep_a(
        "Clock",
        "n",
        3,
        assist_map(&[("n", "learning")]),
    )]);
    assert_eq!(
        anki_due(&ctx, &path, &copy),
        Some((ago(3) + Duration::days(1), 1))
    );
}

/// One step ahead on the same clock: a Good answer today multiplies the
/// last interval by the ease the history left (2.5 untouched, 2.35 after
/// a Hard, 2.3 after an Again), dated from today; a file never done
/// comes back tomorrow.
#[test]
fn a_clean_rep_today_projects_the_next_due_day() {
    let mut fx = Fx::new();
    let path = fx.bank("n", "Clock", "c.py", "d1", &[]);
    let key = fx.ctx().drill_evidence_key(&path);
    assert_eq!(
        anki_next_if_good(&key, &no_evidence(), today()),
        (today() + Duration::days(1), 1)
    );
    let good = evidence(vec![
        drill_rep("Clock", "n", 60),
        drill_rep("Clock", "n", 59),
        drill_rep("Clock", "n", 56),
    ]);
    assert_eq!(
        anki_next_if_good(&key, &good, today()),
        (today() + Duration::days(20), 20)
    );
    let hard = evidence(vec![
        drill_rep("Clock", "n", 10),
        drill_rep("Clock", "n", 9),
        drill_rep_a("Clock", "n", 6, assist_map(&[("n", "hint")])),
    ]);
    // 3 * 1.2 = 4 on the Hard, then 4 * 2.35 = 9
    assert_eq!(
        anki_next_if_good(&key, &hard, today()),
        (today() + Duration::days(9), 9)
    );
    let again = evidence(vec![
        drill_rep("Clock", "n", 10),
        drill_rep_v("Clock", "n", 5, "struggled", Assist::None),
    ]);
    // back to 1 on the Again, then max(2, 1 * 2.3) = 2
    assert_eq!(
        anki_next_if_good(&key, &again, today()),
        (today() + Duration::days(2), 2)
    );
}

/// DRILL_SCHEDULER=anki: a SOLID, owned node's drill comes back when the
/// file's own clock says so, and not before. Under the node clock the
/// same file is held (the node reads owned with nothing left).
#[test]
fn under_the_anki_clock_a_solid_node_still_serves_its_due_drill() {
    let mut fx = Fx::new();
    fx.flat_window();
    let path = fx.bank("some-node", "Own", "o.py", "d1", &[]);
    let due = |ev: &Evidence| due_drill(&fx.ctx(), "some-node", ev, today(), false, false);
    // (the evidence memoises due_drill per day, so a knob flipped between
    // two reads needs a fresh copy - nothing flips it mid-process)
    let ev = || {
        evidence(vec![
            solve("7", &[("some-node", "clean")], 2),
            drill_rep("Own", "some-node", 5),
        ])
    };
    assert!(owned(&ev(), "some-node"));
    assert_eq!(due(&ev()), None);
    test_env("DRILL_SCHEDULER", "anki");
    assert_eq!(due(&ev()), Some(path));
    let fresh = evidence(vec![
        solve("7", &[("some-node", "clean")], 2),
        drill_rep("Own", "some-node", 9),
        drill_rep("Own", "some-node", 8),
        drill_rep("Own", "some-node", 5),
    ]); // interval 8: due in 3 days
    assert_eq!(due(&fresh), None);
    let held = evidence(vec![
        drill_rep("Own", "some-node", 5),
        drill_rep("Own", "some-node", 0),
    ]); // once a day
    assert_eq!(due(&held), None);
}

/// A SOLID node off its floor is not due under the node clock. With
/// DRILL_SCHEDULER=anki it is due when its bank has a due file, after
/// FRAGILE and floor moves and before STALE ones, and the reason names
/// the clock.
#[test]
fn under_the_anki_clock_a_solid_node_with_a_due_drill_enters_the_frontier() {
    let mut fx = Fx::picker();
    test_env("DRILL_SCHEDULER", "anki");
    fx.stubs().graduation_none = true;
    fx.stubs().anki_due = Some(|_| Some((today() - Duration::days(4), 3)));
    fx.nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a"])), ("2", problem(&["b"]))]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean")], 30),
        solve("2", &[("b", "clean")], 20),
    ]);
    let st = statuses(&[("a", SOLID, Some(30)), ("b", STALE, Some(20))]);
    assert_eq!(target(&fx.run(&ev, &st, args())), "b"); // node clock: a is not due
    fx.stubs().bank = set(&["a"]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("a", SOLID, "drill:a"));
    assert_eq!(
        reason(&c),
        "drill due on its own clock - 3d interval, 4d overdue"
    );
    test_env("DRILL_SCHEDULER", "");
    assert_eq!(target(&fx.run(&ev, &st, args())), "b");
}

/// DRILL_SCHEDULER=anki: a bank file due on its own clock is served
/// before the session-start easy, before a STALE move with a carrier,
/// and whatever the node's status. The reason names the clock. A group
/// name scopes the clock; an excluded drill id steps to the next file.
#[test]
fn a_file_due_on_the_clock_outranks_every_other_rule() {
    let mut fx = Fx::picker();
    test_env("DRILL_SCHEDULER", "anki");
    fx.stubs().anki_due = Some(|path| {
        if path.ends_with("a.py") {
            Some((today() - Duration::days(2), 3))
        } else {
            None
        }
    });
    fx.nodes(&["a", "b", "c"])
        .group(&["c"], "sql")
        .problems(vec![("1", problem(&["a"])), ("2", problem(&["b"]))]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean")], 2),
        solve("2", &[("b", "clean")], 20),
    ]);
    let st = statuses(&[
        ("a", SOLID, Some(2)),
        ("b", STALE, Some(20)),
        ("c", MISSING, None),
    ]);
    assert_eq!(target(&fx.run(&ev, &st, args())), "b"); // the clock is empty
    fx.stubs().clock = vec![
        (PathBuf::from("drills/a/a.py"), "a".into()),
        (PathBuf::from("drills/c/c.py"), "c".into()),
    ];
    let c = fx.run(&ev, &st, args().session_start());
    assert_eq!(t3(&c), tup("a", SOLID, "drill:a"));
    assert_eq!(
        reason(&c),
        "drill due on its own clock - 3d interval, 2d overdue"
    );
    let c = fx.run(&ev, &st, args().exclude(&["drill:a"]));
    assert_eq!(t3(&c), tup("c", MISSING, "drill:c"));
    assert_eq!(reason(&c), "drill never done - on its own clock");
    assert_eq!(pnum(&fx.run(&ev, &st, args().group("sql"))), "drill:c");
    test_env("DRILL_SCHEDULER", "");
    assert_eq!(target(&fx.run(&ev, &st, args())), "b");
}

fn basenames(f: &[(PathBuf, String)]) -> Vec<String> {
    f.iter()
        .map(|(p, _)| p.file_name().unwrap().to_str().unwrap().to_string())
        .collect()
}

/// kg_lib.anki_frontier: a file past its due date comes first, most
/// overdue first, but a due file's due "after" drills come before it;
/// files never done follow, atoms before the drills that come after
/// them; a file done today is out; a file due tomorrow is out.
/// The "after" hold does not withhold a due file (Install Order sat
/// behind Shake Hands for 23 days, 2026-09-06).
#[test]
fn the_clock_orders_reviews_before_new_files_and_ignores_holds() {
    let mut fx = Fx::new();
    test_env("DRILL_SCHEDULER", "anki");
    fx.bank("atom", "Atom", "a.py", "d1", &[]);
    fx.bank("comp", "Comp", "c.py", "d2", &["d1"]);
    fx.bank("atom", "Late", "l.py", "d3", &[]);
    let m = fx.bank("atom", "Later", "m.py", "d4", &[]);
    fx.bank("atom", "Fresh", "f.py", "d5", &[]);
    fx.bank("atom", "Today", "t.py", "d6", &[]);
    let p = fx.bank("comp", "Top", "p.py", "d7", &["d3"]);
    let c = fx.path("comp", "c.py");
    fx.nodes(&["atom", "comp"]).prereqs("comp", &["atom"]);
    let ev = evidence(vec![
        drill_rep("Top", "comp", 20), // interval 1: 19d overdue, after Late
        drill_rep("Late", "atom", 3), // interval 1: 2d overdue
        drill_rep("Later", "atom", 10),
        drill_rep("Later", "atom", 9), // interval 3: 6d overdue
        drill_rep("Fresh", "atom", 0),
        drill_rep("Today", "atom", 5),
        drill_rep("Today", "atom", 4),
        drill_rep("Today", "atom", 0),
    ]);
    let ctx = fx.ctx();
    let f = anki_frontier(&ctx, &ev, today(), Some(&fx.nodes), None, false);
    assert_eq!(
        basenames(&f),
        strs(&["l.py", "p.py", "m.py", "a.py", "c.py"])
    );
    let nodes: Vec<&str> = f.iter().map(|(_, n)| n.as_str()).collect();
    assert_eq!(nodes, vec!["atom", "comp", "atom", "atom", "comp"]);
    assert_eq!(
        anki_frontier(
            &ctx,
            &ev,
            today(),
            Some(&fx.nodes),
            Some(&strs(&["comp"])),
            false
        ),
        vec![(p.clone(), "comp".to_string()), (c, "comp".to_string())]
    );
    // due_drill agrees with the clock on the file it serves
    assert_eq!(due_drill(&ctx, "atom", &ev, today(), false, false), Some(m)); // Top is out of scope
    assert_eq!(due_drill(&ctx, "comp", &ev, today(), false, false), Some(p));
}

/// kg_lib.anki_frontier: the "after" chain is climbed through drills
/// that are not due. 2026-09-10: How Many Companies (after Union Links,
/// after Find Roots) was a day more overdue than Find Roots, Union Links
/// was not due, and the climb stopped there - Find Roots came second.
#[test]
fn a_due_drill_waits_for_a_due_ancestor_past_one_that_is_not_due() {
    let mut fx = Fx::new();
    test_env("DRILL_SCHEDULER", "anki");
    fx.bank("uf", "Find Roots", "r.py", "d1", &[]);
    fx.bank("uf", "Union Links", "u.py", "d2", &["d1"]);
    fx.bank("uf", "Companies", "c.py", "d3", &["d2"]);
    fx.nodes(&["uf"]);
    let ev = evidence(vec![
        drill_rep("Find Roots", "uf", 2), // interval 1: 1d overdue
        drill_rep("Union Links", "uf", 5),
        drill_rep("Union Links", "uf", 1), // interval 4: not due
        drill_rep("Companies", "uf", 3),   // interval 1: 2d overdue
    ]);
    let ctx = fx.ctx();
    let f = anki_frontier(&ctx, &ev, today(), Some(&fx.nodes), None, false);
    assert_eq!(basenames(&f), strs(&["r.py", "c.py"]));
}

// --------------------------------------------------------------------------
// rule 2c: a problem on its own review clock
// --------------------------------------------------------------------------

/// A solve that needed help, which is what opens a problem's card.
fn assisted(pnum: &str, moves: &[(&str, &str)], days_ago: i64) -> (String, Rec) {
    solve_a(pnum, moves, days_ago, level("learning"))
}

/// Nothing else re-serves a problem for its own sake: every other rule
/// picks a move and then a carrier for it, so a node that went SOLID on
/// some other carrier left the problem that beat you untouched.
#[test]
fn a_problem_that_needed_help_comes_back_on_its_own() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q1"]))]);
    let st = statuses(&[("q1", SOLID, Some(1))]);
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "1");
}

/// It may still be picked as a carrier; what it must not be is a debt.
#[test]
fn a_clean_first_solve_is_never_re_served_as_a_review() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"]).problem("1", problem(&["q1"]));
    let st = statuses(&[("q1", SOLID, Some(1))]);
    let ev = evidence(vec![solve("1", &[("q1", "clean")], 30)]);
    assert_eq!(problem_due(&ev, "1"), None);
    assert!(!reason(&fx.run(&ev, &st, args())).contains("waiting for"));
}

/// `make studied`: the file carries the marker and the record no moves.
fn studied(pnum: &str, days_ago: i64) -> (String, Rec) {
    let (_, r) = solve(pnum, &[], days_ago);
    (format!("solved/p{pnum}_STUDIED_{days_ago}.py"), r)
}

/// A problem read and played with, nothing scored: no node sees it, but
/// the card opens like a copied solution's - three days, then unaided.
#[test]
fn a_studied_problem_opens_its_card_and_touches_no_node() {
    let ev = evidence(vec![studied("1", 0)]);
    assert_eq!(
        attempt_label("solved/p1_STUDIED_0.py", ev.rec(0)),
        "studied"
    );
    assert_eq!(
        problem_due(&ev, "1"),
        Some((
            ago(0) + Duration::days(PROBLEM_GRADUATING_DAYS),
            PROBLEM_GRADUATING_DAYS
        ))
    );
    assert!(!owned(&ev, "q1"));
    assert_eq!(crate::status::last_clean_solve(&ev, "1"), "");
    // the clean rep three days on retires it
    let ev = evidence(vec![studied("1", 3), solve("1", &[("q1", "clean")], 0)]);
    assert_eq!(problem_due(&ev, "1"), None);
}

/// The picker sees a studied problem as seen: cooled as a carrier, and
/// served back on its card once that is due, not as a fresh carrier of
/// the move tomorrow.
#[test]
fn a_studied_problem_is_not_re_served_before_its_card_is_due() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q1"]))]);
    let st = statuses(&[("q1", STALE, Some(60))]);
    let ev = evidence(vec![solve("2", &[("q1", "clean")], 60), studied("1", 1)]);
    assert_ne!(pnum(&fx.run(&ev, &st, args())), "1");
    let ev = evidence(vec![
        solve("2", &[("q1", "clean")], 60),
        studied("1", PROBLEM_GRADUATING_DAYS),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "1");
}

/// No game: Elo and `make stats` never see it. The next scored rep of the
/// problem is a repeat, since it has been seen.
#[test]
fn a_studied_problem_is_no_game_but_the_next_rep_is_a_repeat() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"]).problem("1", problem(&["q1"]));
    let ctx = fx.ctx();
    *ctx.solve_times.borrow_mut() = Some(vec![]);
    let timed = |mut r: (String, Rec)| {
        r.1.seconds = Some(600);
        r
    };
    let ev = evidence(vec![
        studied("1", 5),
        timed(solve("1", &[("q1", "clean")], 0)),
    ]);
    let games = crate::model::scored_games(&ctx, &ev);
    assert_eq!(games.len(), 1);
    assert!(!games[0].first);
    assert_eq!(games[0].score, 1.0);
}

#[test]
fn a_review_outranks_the_spaced_re_solve_of_a_stale_move() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1", "q2"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q2"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", STALE, Some(60))]);
    let ev = evidence(vec![
        assisted("1", &[("q1", "clean")], 30),
        solve("2", &[("q2", "clean")], 60),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "1");
}

/// A broken move is a rep the graph needs now; a review is a debt.
#[test]
fn a_fragile_move_still_goes_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1", "q2"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q2"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", FRAGILE, Some(20))]);
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "2");
}

#[test]
fn the_drill_clock_still_outranks_a_review() {
    let mut fx = Fx::picker();
    test_env("DRILL_SCHEDULER", "anki");
    fx.nodes(&["q1", "q2"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q2"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(1))]);
    fx.stubs().clock = vec![(PathBuf::from("drills/q2/a.py"), "q2".into())];
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:q2");
}

/// A floor rep goes to a fresh carrier, so with REVIEWS_FIRST unset the
/// due review is never reached while a young move has one (2026-09-10).
#[test]
fn a_graduating_floor_outranks_a_review_by_default() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1", "q2"]).problems(vec![
        ("1", problem(&["q1"])),
        ("2", problem(&["q2"])),
        ("3", problem(&["q2"])),
    ]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(7))]);
    let ev = evidence(vec![
        assisted("1", &[("q1", "clean")], 30),
        solve("2", &[("q2", "clean")], 7),
    ]);
    assert!(graduation_due(&ev, "q2", 2).is_some());
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "3");
}

#[test]
fn reviews_first_serves_the_review_ahead_of_the_floor() {
    let mut fx = Fx::picker();
    test_env("REVIEWS_FIRST", "1");
    fx.nodes(&["q1", "q2"]).problems(vec![
        ("1", problem(&["q1"])),
        ("2", problem(&["q2"])),
        ("3", problem(&["q2"])),
    ]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(7))]);
    let ev = evidence(vec![
        assisted("1", &[("q1", "clean")], 30),
        solve("2", &[("q2", "clean")], 7),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "1");
}

/// 2026-09-16: 815 and 752 asleep on a node 2812 had just broken, and
/// rule 0b served 909 to warm it over 12 due reviews.
#[test]
fn reviews_first_outranks_the_sleeping_problem_warm_up() {
    let mut fx = Fx::picker();
    test_env("REVIEWS_FIRST", "1");
    fx.nodes(&["q1", "q2"]).problems(vec![
        ("1", problem(&["q1"])),
        ("2", problem(&["q2"])),
        ("3", problem(&["q2"])),
    ]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", FRAGILE, Some(0))]);
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args().asleep(&["2"]))), "1");
    test_env("REVIEWS_FIRST", "");
    assert_eq!(pnum(&fx.run(&ev, &st, args().asleep(&["2"]))), "3");
}

#[test]
fn reviews_first_still_yields_to_the_drill_clock() {
    let mut fx = Fx::picker();
    test_env("REVIEWS_FIRST", "1");
    test_env("DRILL_SCHEDULER", "anki");
    fx.nodes(&["q1", "q2"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q2"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(1))]);
    fx.stubs().clock = vec![(PathBuf::from("drills/q2/a.py"), "q2".into())];
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:q2");
}

#[test]
fn a_review_outranks_a_summit() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"])
        .problems(vec![("1", problem(&["q1"])), ("9", hard(&["q1"]))]);
    let st = statuses(&[("q1", SOLID, Some(1))]);
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "1");
}

#[test]
fn a_sleeping_or_spent_problem_is_not_served_for_review() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"]).problem("1", problem(&["q1"]));
    let st = statuses(&[("q1", SOLID, Some(1))]);
    let ev = evidence(vec![assisted("1", &[("q1", "clean")], 30)]);
    assert!(fx.run(&ev, &st, args().asleep(&["1"])).is_none());
    assert!(fx.run(&ev, &st, args().exclude(&["1"])).is_none());
}

#[test]
fn a_review_respects_the_daily_group_cap() {
    let mut fx = Fx::picker();
    test_env("KG_GROUP_CAP", "sql=1");
    fx.nodes(&["q1"])
        .group(&["q1"], "sql")
        .problem("1", problem(&["q1"]));
    let st = statuses(&[("q1", SOLID, Some(1))]);
    let ev = evidence(vec![
        assisted("1", &[("q1", "clean")], 30),
        solve("2", &[("q1", "clean")], 0),
    ]);
    assert!(fx.run(&ev, &st, args()).is_none());
}

/// The pick is rendered off the target node, so it has to be one the
/// walk actually carries.
#[test]
fn the_review_target_is_a_move_of_the_walk() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1", "q2"]).problem("1", problem(&["q1", "q2"]));
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(1))]);
    let ev = evidence(vec![assisted("1", &[("q1", "clean"), ("q2", "clean")], 30)]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(pnum(&c), "1");
    assert!(fx.problems["1"].moves.contains(&target(&c)));
}

// --------------------------------------------------------------------------
// paid-only problems: there is no statement to prepare
// --------------------------------------------------------------------------

#[test]
fn a_paid_only_problem_is_never_a_carrier() {
    let mut fx = Fx::picker();
    fx.premium("1")
        .nodes(&["q1"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q1"]))]);
    let st = statuses(&[("q1", FRAGILE, Some(20))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "2");
    fx.problems.shift_remove("2");
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

/// 261 was solved in November 2025, came back on the review clock ten
/// months later, and `make prepare` could not fetch it.
#[test]
fn a_paid_only_problem_is_never_a_review() {
    let mut fx = Fx::picker();
    fx.premium("1")
        .nodes(&["q1"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q1"]))]);
    let st = statuses(&[("q1", SOLID, Some(1))]);
    let ev = evidence(vec![
        assisted("1", &[("q1", "clean")], 30),
        assisted("2", &[("q1", "clean")], 20),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "2");
    let queue: Vec<String> = review_queue(&fx.ctx(), &ev, &fx.pv(), today())
        .into_iter()
        .map(|(p, _, _)| p)
        .collect();
    assert_eq!(queue, strs(&["2"]));
}

/// Reviews come out clustered by primary move: groups in order of their
/// earliest due date, problems inside a group by due date. Plain due order
/// here would be 1, 3, 2.
#[test]
fn reviews_are_clustered_by_primary_move() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1", "q2"]).problems(vec![
        ("1", problem(&["q1"])),
        ("2", problem(&["q1"])),
        ("3", problem(&["q2"])),
    ]);
    let ev = evidence(vec![
        assisted("1", &[("q1", "clean")], 30),
        assisted("2", &[("q1", "clean")], 10),
        assisted("3", &[("q2", "clean")], 20),
    ]);
    let queue: Vec<String> = review_queue(&fx.ctx(), &ev, &fx.pv(), today())
        .into_iter()
        .map(|(p, _, _)| p)
        .collect();
    assert_eq!(queue, strs(&["1", "2", "3"]));
}

#[test]
fn a_paid_only_summit_is_never_offered() {
    let mut fx = Fx::picker();
    fx.premium("9").nodes(&["q1"]).problem("9", hard(&["q1"]));
    let st = statuses(&[("q1", SOLID, Some(1))]);
    assert!(fx.summits(&no_evidence(), &st).is_empty());
}

#[test]
fn unservable_covers_both_reasons() {
    let mut fx = Fx::new();
    fx.premium("1");
    let ctx = fx.ctx();
    assert!(ctx.unservable("1", &problem(&["a"])));
    assert!(ctx.unservable("2", &problem(&["a"]).banned()));
    assert!(!ctx.unservable("2", &problem(&["a"])));
}
