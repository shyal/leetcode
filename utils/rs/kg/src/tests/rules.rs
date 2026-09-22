// The frontier rules: what is due, in what order, and on which carrier.

use std::collections::HashSet;

use chrono::Duration;

use super::*;
use crate::bank::unlocks;
use crate::data::{test_env, Assist};
use crate::drills::{
    drill_review_cap, drill_reviews_left, drill_reviews_today, group_caps, group_reps,
    new_drill_cap, new_drills_left, new_drills_today,
};
use crate::pick::{ready_hards, routed_around, starved};
use crate::recog::{self, Recog, RecogRec};
use crate::status::{graduation_due, DEEP_STALE_DAYS, GRAD_LADDER_SPARSE, STARVED_DAYS};

// --------------------------------------------------------------------------
// rule 1: consolidate a FRAGILE move on a READY carrier
// --------------------------------------------------------------------------

#[test]
fn fragile_move_is_served_on_a_ready_carrier() {
    let mut fx = Fx::picker();
    fx.nodes(&["bsearch", "pivot"])
        .problem("33", problem(&["bsearch", "pivot"]));
    let st = statuses(&[("bsearch", SOLID, Some(1)), ("pivot", FRAGILE, Some(1))]);
    assert_eq!(
        t3(&fx.run(&no_evidence(), &st, args())),
        tup("pivot", FRAGILE, "33")
    );
}

/// Preference order is fragile, then stale, then missing: a rusty move
/// is repaired before a cold one is re-entered or a new one introduced.
#[test]
fn fragile_beats_stale_and_missing() {
    let mut fx = Fx::picker();
    fx.nodes(&["frag", "stale", "new"]).problems(vec![
        ("1", problem(&["frag"])),
        ("2", problem(&["stale"])),
        ("3", problem(&["new"])),
    ]);
    let st = statuses(&[
        ("frag", FRAGILE, Some(1)),
        ("stale", STALE, Some(50)),
        ("new", MISSING, None),
    ]);
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "frag");
}

#[test]
fn oldest_fragile_goes_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["recent", "ancient"]).problems(vec![
        ("1", problem(&["recent"])),
        ("2", problem(&["ancient"])),
    ]);
    let st = statuses(&[
        ("recent", FRAGILE, Some(2)),
        ("ancient", FRAGILE, Some(200)),
    ]);
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "ancient");
}

// --------------------------------------------------------------------------
// reachability-aware ordering (PLAN.md phase 1): unlock count ranks the due
// nodes; evidence age breaks ties
// --------------------------------------------------------------------------

#[test]
fn higher_unlock_fragile_outranks_an_older_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["old_dud", "young_key"]).problems(vec![
        ("1", problem(&["old_dud"])),
        ("2", problem(&["young_key"])),
    ]);
    let st = statuses(&[
        ("old_dud", FRAGILE, Some(200)),
        ("young_key", FRAGILE, Some(2)),
    ]);
    fx.stubs().unlocks = map(&[("young_key", 12), ("old_dud", 1)]);
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "young_key");
}

#[test]
fn age_breaks_an_unlock_tie() {
    let mut fx = Fx::picker();
    fx.nodes(&["recent", "ancient"]).problems(vec![
        ("1", problem(&["recent"])),
        ("2", problem(&["ancient"])),
    ]);
    let st = statuses(&[
        ("recent", FRAGILE, Some(2)),
        ("ancient", FRAGILE, Some(200)),
    ]);
    fx.stubs().unlocks = map(&[("recent", 5), ("ancient", 5)]);
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "ancient");
}

#[test]
fn highest_unlock_missing_move_is_introduced_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a"])), ("2", problem(&["b"]))]);
    let st = statuses(&[("a", MISSING, None), ("b", MISSING, None)]);
    fx.stubs().unlocks = map(&[("b", 10), ("a", 2)]);
    let c = fx.run(&no_evidence(), &st, args());
    assert_eq!(
        (target(&c), c.as_ref().unwrap().status),
        ("b".to_string(), MISSING)
    );
}

#[test]
fn unlocks_counts_only_problems_blocked_by_exactly_one_node() {
    let mut fx = Fx::new();
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", FRAGILE, Some(1)),
        ("c", MISSING, None),
    ]);
    fx.problem("1", problem(&["a"])); // already solved, never counted
    fx.predicted.insert("1".into(), drafted(&["a", "b"])); // solved: skipped
    fx.predicted.insert("2".into(), drafted(&["a", "b"])); // blocked only by b
    fx.predicted.insert("3".into(), drafted(&["b", "c"])); // two gaps: nobody
    fx.predicted.insert("4".into(), drafted(&["a"])); // in reach: skipped
    let mut five = drafted_missing(&["a", "b"], &["segment-tree"]);
    five.walks.push(Walk {
        moves: strs(&["a", "c"]),
        ..Default::default()
    });
    fx.predicted.insert("5".into(), five); // only clean walk -> c
    let mut six = drafted(&["a"]);
    six.walks.push(Walk {
        moves: strs(&["a", "b"]),
        ..Default::default()
    });
    fx.predicted.insert("6".into(), six); // in reach
    let ctx = fx.ctx();
    assert_eq!(
        unlocks(&ctx, &st, &fx.pv(), &HashSet::new()),
        map(&[("b", 1), ("c", 1)])
    );
}

// --------------------------------------------------------------------------
// the one-new-move rule, and who is allowed to be a carrier
// --------------------------------------------------------------------------

/// A carrier that would introduce a second rusty move is not a carrier:
/// the ZPD constraint is one fragile/stale node per assignment.
#[test]
fn carrier_needs_every_other_move_solid() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "alsorusty", "solid"]).problems(vec![
        ("1", problem(&["target", "alsorusty"])), // two rusty moves: never
        ("2", problem(&["target", "solid"])),     // one rusty move: this one
    ]);
    let st = statuses(&[
        ("target", FRAGILE, Some(1)),
        ("alsorusty", STALE, Some(90)),
        ("solid", SOLID, Some(1)),
    ]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "2");
}

/// Himalayas rule: a Hard is a summit attempted all-green, never the
/// place a rusty move gets its rep. With the move rusty the Hard is not
/// servable at all, as a carrier or as a summit.
#[test]
fn hards_are_never_carriers() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problem("41", hard(&["target"]));
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

/// Summits are the LAST rule: an all-green Hard waits until there is
/// nothing rusty left to train.
#[test]
fn a_rusty_move_is_repaired_before_a_summit_is_offered() {
    let mut fx = Fx::picker();
    fx.nodes(&["frag", "solid"])
        .problems(vec![("1", problem(&["frag"])), ("76", hard(&["solid"]))]);
    let st = statuses(&[("frag", FRAGILE, Some(1)), ("solid", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "1");
}

#[test]
fn banned_problems_are_never_carriers() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"])
        .problem("1", problem(&["target"]).banned());
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

#[test]
fn problems_solved_today_are_excluded() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problems(vec![
        ("1", problem(&["target"])),
        ("2", problem(&["target"])),
    ]);
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    assert_eq!(
        pnum(&fx.run(&no_evidence(), &st, args().exclude(&["1"]))),
        "2"
    );
}

#[test]
fn a_group_at_its_daily_cap_leaves_the_default_frontier() {
    let mut fx = Fx::picker();
    test_env("KG_GROUP_CAP", "sql=2");
    fx.nodes(&["q1", "q2", "other"])
        .group(&["q1", "q2"], "sql")
        .group(&["other"], "trees")
        .problems(vec![
            ("1", problem(&["q1"])),
            ("2", problem(&["q2"])),
            ("3", problem(&["other"])),
            ("4", problem(&["q1"])),
        ]);
    let st = statuses(&[
        ("q1", FRAGILE, Some(1)),
        ("q2", FRAGILE, Some(1)),
        ("other", STALE, Some(40)),
    ]);
    let ev = evidence(vec![
        solve("1", &[("q1", "clean")], 0),
        solve("2", &[("q2", "clean")], 0),
    ]);
    // two sql reps today: the fragile sql moves wait, the stale tree move is served
    assert_eq!(
        target(&fx.run(&ev, &st, args().exclude(&["1", "2"]))),
        "other"
    );
    // one rep short of the cap: sql is still on the frontier
    let one = evidence(vec![solve("1", &[("q1", "clean")], 0)]);
    let t = target(&fx.run(&one, &st, args().exclude(&["1"])));
    assert!(t == "q1" || t == "q2");
    // naming the group is the override
    assert_eq!(
        t3(&fx.run(&ev, &st, args().exclude(&["1", "2"]).group("sql"))),
        tup("q1", FRAGILE, "4")
    );
}

/// DRILL_SCHEDULER=anki: a due file in a capped group waits with the
/// rest of the group; the clock moves to the next due file, and naming
/// the group is still the override (2026-09-06, KG_GROUP_CAP=sql=1
/// ignored by the clock).
#[test]
fn a_group_at_its_daily_cap_is_out_of_the_clock_too() {
    let mut fx = Fx::picker();
    test_env("DRILL_SCHEDULER", "anki");
    test_env("KG_GROUP_CAP", "sql=1");
    fx.nodes(&["q1", "other"])
        .group(&["q1"], "sql")
        .group(&["other"], "trees")
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["other"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("other", SOLID, Some(1))]);
    fx.stubs().clock = vec![
        (PathBuf::from("drills/q1/a.py"), "q1".into()),
        (PathBuf::from("drills/other/b.py"), "other".into()),
    ];
    // no sql rep today: the sql file leads the clock
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "drill:q1");
    // one sql rep today, at the cap: the next due file is served instead
    let ev = evidence(vec![solve("1", &[("q1", "clean")], 0)]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().exclude(&["1"]))),
        "drill:other"
    );
    // naming the group is the override
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().exclude(&["1"]).group("sql"))),
        "drill:q1"
    );
}

#[test]
fn group_reps_counts_drills_and_problems_touching_the_group() {
    let mut fx = Fx::new();
    fx.nodes(&["q1", "other"]).group(&["q1"], "sql");
    let ev = evidence(vec![
        solve("1", &[("q1", "clean")], 0),
        solve("2", &[("other", "clean")], 0),
        drill_file("solved/d_Some_Drill_0.py", "q1", 0, Assist::None),
        solve("3", &[("q1", "clean")], 1), // yesterday does not count
    ]);
    let ctx = fx.ctx();
    assert_eq!(group_reps(&ctx, "sql", &ev, today()), 2);
    assert_eq!(group_reps(&ctx, "trees", &ev, today()), 0);
}

/// MAX_NEW_DRILLS: past the cap, a bank file with no rep waits until
/// tomorrow; a file with a rep is a review and is served as usual.
#[test]
fn the_new_drill_cap_withholds_files_never_drilled() {
    let mut fx = Fx::picker();
    test_env("DRILL_SCHEDULER", "anki");
    test_env("MAX_NEW_DRILLS", "1");
    fx.nodes(&["q1", "q2"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q2"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(1))]);
    fx.stubs().clock = vec![
        (PathBuf::from("drills/q1/a.py"), "q1".into()),
        (PathBuf::from("drills/q2/b.py"), "q2".into()),
    ];
    // nothing met today: the first due file is served whether or not it is new
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "drill:q1");
    // one first exposure today, at the cap: a.py is still never drilled, so
    // the clock moves on to b.py - which has a rep, and is a review
    let ev = evidence(vec![
        drill_file(
            "solved/d_Met_Today_2026_01_01T00_00_00_000000_00_00Z.py",
            "q1",
            0,
            Assist::None,
        ),
        drill_file(
            "solved/d_B_2026_01_01T00_00_00_000000_00_00Z.py",
            "q2",
            3,
            Assist::None,
        ),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:q2");
}

/// The cap is on the whole day's new ground: a MISSING node whose bank
/// file has never been drilled is withheld on the frontier as well, and
/// naming its group does not lift it.
#[test]
fn the_new_drill_cap_holds_the_frontier_too() {
    let mut fx = Fx::picker();
    test_env("MAX_NEW_DRILLS", "1");
    fx.nodes(&["q1"])
        .group(&["q1"], "sql")
        .problem("1", problem(&["q1"]));
    let st = statuses(&[("q1", MISSING, None)]);
    fx.stubs().bank = set(&["q1"]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "drill:q1");
    let ev = evidence(vec![drill_file(
        "solved/d_Met_Today_2026_01_01T00_00_00_000000_00_00Z.py",
        "q1",
        0,
        Assist::None,
    )]);
    assert!(fx.run(&ev, &st, args()).is_none());
    assert!(fx.run(&ev, &st, args().group("sql")).is_none());
    assert!(fx.run(&ev, &st, args().cram().early()).is_none());
}

#[test]
fn new_drill_knob_parses_and_counts_first_reps() {
    let _fx = Fx::new();
    test_env("MAX_NEW_DRILLS", "3");
    assert_eq!(new_drill_cap(), Some(3));
    test_env("MAX_NEW_DRILLS", "lots");
    assert_eq!(new_drill_cap(), None);
    test_env("MAX_NEW_DRILLS", "");
    assert_eq!(new_drill_cap(), None);
    let ev = evidence(vec![
        drill_file(
            "solved/d_First_2026_01_01T00_00_00_000000_00_00Z.py",
            "q1",
            1,
            Assist::None,
        ),
        drill_file(
            "solved/d_First_2026_01_02T00_00_00_000000_00_00Z.py",
            "q1",
            0,
            Assist::None,
        ),
        drill_file(
            "solved/d_Second_2026_01_02T00_00_00_000000_00_00Z.py",
            "q1",
            0,
            Assist::None,
        ),
    ]);
    // today: one first exposure (Second), one review (First, met yesterday)
    assert_eq!(new_drills_today(&ev, today()), 1);
    test_env("MAX_NEW_DRILLS", "2");
    assert_eq!(new_drills_left(&ev, today()), Some(1));
    test_env("MAX_NEW_DRILLS", "");
    assert_eq!(new_drills_left(&ev, today()), None);
}

/// MAX_DRILL_REVIEWS: past the cap, a bank file with a rep waits until
/// tomorrow; a file never drilled is first exposure and is unaffected.
#[test]
fn the_drill_review_cap_withholds_files_already_met() {
    let mut fx = Fx::picker();
    test_env("DRILL_SCHEDULER", "anki");
    test_env("MAX_DRILL_REVIEWS", "1");
    fx.nodes(&["q1", "q2"])
        .problems(vec![("1", problem(&["q1"])), ("2", problem(&["q2"]))]);
    let st = statuses(&[("q1", SOLID, Some(1)), ("q2", SOLID, Some(1))]);
    fx.stubs().clock = vec![
        (PathBuf::from("drills/q1/a.py"), "q1".into()),
        (PathBuf::from("drills/q2/b.py"), "q2".into()),
    ];
    let a3 = drill_file(
        "solved/d_A_2026_01_01T00_00_00_000000_00_00Z.py",
        "q1",
        3,
        Assist::None,
    );
    let ev = evidence(vec![a3.clone()]);
    // nothing back today: a.py is a review and leads the clock
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:q1");
    // one review today, at the cap: a.py waits, b.py is never drilled and
    // answers to the other budget
    let ev = evidence(vec![
        a3,
        drill_file(
            "solved/d_A_2026_01_02T00_00_00_000000_00_00Z.py",
            "q1",
            0,
            Assist::None,
        ),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:q2");
}

/// With the day's new drills and its reviews both spent, the bank is
/// out and the picker serves the problem the drills exist for.
#[test]
fn both_drill_budgets_spent_falls_through_to_a_problem() {
    let mut fx = Fx::picker();
    fx.nodes(&["q1"]).problem("1", problem(&["q1"]));
    let st = statuses(&[("q1", STALE, Some(40))]);
    fx.stubs().bank = set(&["q1"]);
    let ev = evidence(vec![drill_file(
        "solved/d_New_2026_01_01T00_00_00_000000_00_00Z.py",
        "q1",
        0,
        Assist::None,
    )]);
    // uncapped, the stale move gets its bank
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "drill:q1");
    // one first exposure today and no review: due_drill's file has no rep of
    // its own, so it is new ground and the new-drill budget is spent
    test_env("MAX_NEW_DRILLS", "1");
    test_env("MAX_DRILL_REVIEWS", "1");
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "1");
}

#[test]
fn drill_review_knob_parses_and_counts_returning_files() {
    let _fx = Fx::new();
    test_env("MAX_DRILL_REVIEWS", "6");
    assert_eq!(drill_review_cap(), Some(6));
    test_env("MAX_DRILL_REVIEWS", "some");
    assert_eq!(drill_review_cap(), None);
    test_env("MAX_DRILL_REVIEWS", "");
    assert_eq!(drill_review_cap(), None);
    let ev = evidence(vec![
        solve("1", &[("q1", "clean")], 0), // a problem is not a drill rep
        drill_file(
            "solved/d_First_2026_01_01T00_00_00_000000_00_00Z.py",
            "q1",
            1,
            Assist::None,
        ),
        drill_file(
            "solved/d_First_2026_01_02T00_00_00_000000_00_00Z.py",
            "q1",
            0,
            Assist::None,
        ),
        drill_file(
            "solved/d_Second_2026_01_02T00_00_00_000000_00_00Z.py",
            "q1",
            0,
            Assist::None,
        ),
    ]);
    // today: First comes back (a review), Second is first exposure
    assert_eq!(drill_reviews_today(&ev, today()), 1);
    assert_eq!(new_drills_today(&ev, today()), 1);
    test_env("MAX_DRILL_REVIEWS", "3");
    assert_eq!(drill_reviews_left(&ev, today()), Some(2));
    test_env("MAX_DRILL_REVIEWS", "");
    assert_eq!(drill_reviews_left(&ev, today()), None);
}

#[test]
fn group_caps_parses_the_envrc_knob() {
    let _fx = Fx::new();
    test_env("KG_GROUP_CAP", "sql=3");
    assert_eq!(group_caps(), vec![("sql".to_string(), 3)]);
    test_env("KG_GROUP_CAP", "sql=3, graphs=2");
    assert_eq!(
        group_caps(),
        vec![("sql".to_string(), 3), ("graphs".to_string(), 2)]
    );
    test_env("KG_GROUP_CAP", "sql=lots");
    assert_eq!(group_caps(), vec![]);
    test_env("KG_GROUP_CAP", "");
    assert_eq!(group_caps(), vec![]);
}

#[test]
fn sleeping_problems_are_not_offered() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problems(vec![
        ("1", problem(&["target"])),
        ("2", problem(&["target"])),
    ]);
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    assert_eq!(
        pnum(&fx.run(&no_evidence(), &st, args().asleep(&["1"]))),
        "2"
    );
}

// --------------------------------------------------------------------------
// carrier sort keys: the 153-before-33 regression
// --------------------------------------------------------------------------

/// Gentleness decided before freshness, so an Easy solved a month ago
/// kept beating a Medium never seen. A carrier that has never been solved
/// is a rep and new ground at once; a smaller solved one is neither.
#[test]
fn an_unsolved_carrier_outranks_a_gentler_solved_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["m"])
        .problems(vec![("1", easy(&["m"])), ("2", problem(&["m"]))]);
    let ev = evidence(vec![solve("1", &[("m", "clean")], 30)]);
    let st = statuses(&[("m", FRAGILE, Some(30))]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "2");
}

/// The bug this suite was started for: 153 (55% acceptance, failed
/// yesterday) kept being served ahead of 33 (45%, untouched for months)
/// because acceptance was baked into the gentleness key and decided before
/// last_solved was ever compared. Acceptance is the LAST tiebreak.
#[test]
fn freshness_outranks_acceptance() {
    let mut fx = Fx::picker();
    fx.nodes(&["bsearch", "pivot"])
        .problems(vec![
            ("33", problem(&["bsearch", "pivot"])),
            ("153", problem(&["bsearch", "pivot"])),
        ])
        .acceptance("33", 45.5)
        .acceptance("153", 55.2);
    let ev = evidence(vec![
        solve("33", &[("bsearch", "clean")], 300),
        solve("153", &[("bsearch", "clean"), ("pivot", "struggled")], 1),
    ]);
    let st = statuses(&[("bsearch", SOLID, Some(1)), ("pivot", FRAGILE, Some(1))]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "33");
}

/// Same tier, same tree, neither ever solved: the gentler problem (higher
/// acceptance = less community friction) sorts first, since nothing more
/// meaningful separates them.
#[test]
fn acceptance_still_breaks_a_genuine_tie() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"])
        .problems(vec![
            ("1", problem(&["target"])),
            ("2", problem(&["target"])),
        ])
        .acceptance("1", 70.0)
        .acceptance("2", 30.0);
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "1");
}

#[test]
fn easier_carrier_wins_over_a_harder_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "extra"]).problems(vec![
        ("1", problem(&["target", "extra"])),
        ("2", easy(&["target", "extra"])),
    ]);
    let st = statuses(&[("target", FRAGILE, Some(1)), ("extra", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "2");
}

/// Gentleness after difficulty is fewest concepts in the room, counted
/// over the transitive prereq closure, not just the walk length.
#[test]
fn smaller_input_tree_wins_within_a_tier() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "plain", "deep", "p1", "p2"])
        .prereqs("deep", &["p1"])
        .prereqs("p1", &["p2"])
        .problems(vec![
            ("1", problem(&["target", "deep"])),
            ("2", problem(&["target", "plain"])),
        ]);
    let st = statuses(&[
        ("target", FRAGILE, Some(1)),
        ("deep", SOLID, Some(1)),
        ("plain", SOLID, Some(1)),
        ("p1", SOLID, Some(1)),
        ("p2", SOLID, Some(1)),
    ]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "2");
}

// --------------------------------------------------------------------------
// STALE: spaced re-solve vs deep-stale re-entry
// --------------------------------------------------------------------------

/// An ordinary stale move is a spaced repetition: the same problem comes
/// back, because the rep IS the re-solve.
#[test]
fn stale_move_reuses_its_latest_carrier() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problems(vec![
        ("1", problem(&["target"])),
        ("2", problem(&["target"])),
    ]);
    let ev = evidence(vec![solve("2", &[("target", "clean")], 50)]);
    let st = statuses(&[("target", STALE, Some(50))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("target", STALE, "2"));
}

/// Past 2x the solid window the memory is gone, so a cold "re-solve"
/// would play like a new problem. Re-enter on a gentle carrier instead.
#[test]
fn deep_stale_move_re_enters_on_a_fresh_carrier() {
    let old = DEEP_STALE_DAYS + 30;
    let mut fx = Fx::picker();
    fx.nodes(&["target"])
        .problems(vec![("1", easy(&["target"])), ("2", problem(&["target"]))]);
    let ev = evidence(vec![solve("2", &[("target", "clean")], old)]);
    let st = statuses(&[("target", STALE, Some(old))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("target", STALE, "1"));
    assert!(reason(&c).contains("deep-stale"));
}

// --------------------------------------------------------------------------
// rule 1b: the graduating floor - young moves get spaced reps the curve
// would never schedule
// --------------------------------------------------------------------------

#[test]
fn graduation_ladder_steps_and_sparse_tightening() {
    let ev = evidence(vec![solve("9", &[("m", "clean")], 1)]);
    assert_eq!(
        graduation_due(&ev, "m", 5),
        Some((ago(1) + Duration::days(3), 3))
    );
    assert_eq!(
        graduation_due(&ev, "m", 2),
        Some((ago(1) + Duration::days(2), 2))
    );
}

#[test]
fn same_day_slam_is_one_ladder_step() {
    let ev = evidence(vec![
        solve("8", &[("m", "clean")], 1),
        solve("9", &[("m", "clean")], 1),
    ]);
    assert_eq!(graduation_due(&ev, "m", 5).unwrap().1, 3); // still step 1
}

#[test]
fn assisted_days_do_not_start_or_advance_the_ladder() {
    let ev = evidence(vec![solve_a(
        "9",
        &[("m", "clean")],
        1,
        assist_map(&[("m", "walkthrough")]),
    )]);
    assert_eq!(graduation_due(&ev, "m", 5), None);
    let ev = evidence(vec![
        solve("8", &[("m", "clean")], 5),
        solve_a("9", &[("m", "clean")], 1, assist_map(&[("m", "hint")])),
    ]);
    // the hinted day does not advance: still step 1, counted from day -5
    assert_eq!(
        graduation_due(&ev, "m", 5),
        Some((ago(5) + Duration::days(3), 3))
    );
}

#[test]
fn a_survived_long_gap_graduates_the_move() {
    let ev = evidence(vec![
        solve("8", &[("m", "clean")], 40),
        solve("9", &[("m", "clean")], 10),
    ]);
    assert_eq!(graduation_due(&ev, "m", 5), None);
}

/// A drill's first rep is scored unaided at the node (Steiner copying),
/// but a copy is not recall: first-rep-only days past the first neither
/// advance the ladder nor pass the long-gap trial (the union-find read of
/// 2026-09-02: five first-exposure drills as a survived 282-day gap).
#[test]
fn first_exposure_copies_start_the_clock_but_certify_nothing() {
    let alpha = drill_file("solved/d_alpha_40.py", "m", 40, level("learning"));
    let beta = drill_file("solved/d_beta_10.py", "m", 10, level("learning"));
    let ev = evidence(vec![alpha.clone(), beta.clone()]);
    // the 30-day gap ends on a first-rep day: no trial, still step 1
    assert_eq!(
        graduation_due(&ev, "m", 5),
        Some((ago(40) + Duration::days(3), 3))
    );
    // a real unaided second rep of the first drill does advance it
    let ev = evidence(vec![
        alpha,
        beta,
        drill_file("solved/d_alpha_5.py", "m", 5, Assist::None),
    ]);
    assert_eq!(
        graduation_due(&ev, "m", 5),
        Some((ago(5) + Duration::days(10), 10))
    );
}

/// One unaided clean 4 days ago, two carriers (sparse, 2d floor): due,
/// and served on the gentle fresh carrier even though the node is SOLID.
#[test]
fn graduating_floor_serves_a_young_solid_move() {
    let mut fx = Fx::picker();
    fx.nodes(&["young"])
        .problems(vec![("1", easy(&["young"])), ("2", problem(&["young"]))]);
    let ev = evidence(vec![solve("2", &[("young", "clean")], 4)]);
    let st = statuses(&[("young", SOLID, Some(4))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("young", SOLID, "1"));
    assert!(reason(&c).contains("graduating"));
}

/// The bank is the move, the problem is the test: a banked young move
/// takes its floor rep on the drill; the carrier fires only once no drill
/// is due (2026-09-02: 721 served as the union-find rep over six drills).
#[test]
fn graduating_floor_serves_the_drill_when_the_move_has_a_bank() {
    let mut fx = Fx::picker();
    fx.nodes(&["young"])
        .problems(vec![("1", easy(&["young"])), ("2", problem(&["young"]))]);
    let ev = evidence(vec![solve("2", &[("young", "clean")], 4)]);
    let st = statuses(&[("young", SOLID, Some(4))]);
    fx.stubs().bank = set(&["young"]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(t3(&c), tup("young", SOLID, "drill:young"));
    assert!(reason(&c).contains("graduating"));
    // drilled today and still due: the carrier is the test after the drill
    fx.stubs().drilled_today = set(&["young"]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("young", SOLID, "1"));
}

/// Drills before problems (2026-09-02): topological order at 271 days
/// overdue with only a carrier sorted above union-find at 15 with six
/// drills in the bank. The bank is the asset; the unbanked move waits.
#[test]
fn a_drill_due_move_is_served_before_a_more_overdue_unbanked_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["banked", "bare"])
        .problems(vec![("1", easy(&["banked"])), ("2", easy(&["bare"]))]);
    let ev = evidence(vec![
        solve("1", &[("banked", "clean")], 5),
        solve("2", &[("bare", "clean")], 40),
        // a rep of it six days ago: waiting, not aged (clock.rs, aging),
        // and its one carrier cooled
        solve("2", &[("bare", "struggled")], 6),
    ]);
    let st = statuses(&[("banked", SOLID, Some(5)), ("bare", SOLID, Some(40))]);
    fx.stubs().bank = set(&["banked"]);
    assert_eq!(
        t3(&fx.run(&ev, &st, args())),
        tup("banked", SOLID, "drill:banked")
    );
    fx.stubs().drilled_today = set(&["banked"]);
    assert_eq!(target(&fx.run(&ev, &st, args())), "bare");
}

/// A currently decayed memory beats insurance on a young one.
#[test]
fn rusty_moves_outrank_the_graduating_floor() {
    let mut fx = Fx::picker();
    fx.nodes(&["young", "rusty"]).problems(vec![
        ("1", easy(&["young"])),
        ("2", easy(&["rusty"])),
        ("3", easy(&["rusty"])),
    ]);
    let ev = evidence(vec![
        solve("1", &[("young", "clean")], 4),
        solve("2", &[("rusty", "struggled")], 3),
    ]);
    let st = statuses(&[("young", SOLID, Some(4)), ("rusty", FRAGILE, Some(3))]);
    assert_eq!(target(&fx.run(&ev, &st, args())), "rusty");
}

// --------------------------------------------------------------------------
// MISSING: one genuinely new move, prereqs all solid
// --------------------------------------------------------------------------

/// A new move whose prereq is itself rusty is not on the frontier: the
/// prereq gets served instead.
#[test]
fn missing_move_needs_solid_prereqs() {
    let mut fx = Fx::picker();
    fx.nodes(&["prereq", "new"])
        .prereqs("new", &["prereq"])
        .problems(vec![("1", problem(&["new"])), ("2", problem(&["prereq"]))]);
    let st = statuses(&[("prereq", FRAGILE, Some(1)), ("new", MISSING, None)]);
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "prereq");
}

#[test]
fn missing_move_with_solid_prereqs_is_introduced() {
    let mut fx = Fx::picker();
    fx.nodes(&["prereq", "new"])
        .prereqs("new", &["prereq"])
        .problem("1", problem(&["new", "prereq"]));
    let st = statuses(&[("prereq", SOLID, Some(1)), ("new", MISSING, None)]);
    assert_eq!(
        t3(&fx.run(&no_evidence(), &st, args())),
        tup("new", MISSING, "1")
    );
}

// --------------------------------------------------------------------------
// the drill-success gate
// --------------------------------------------------------------------------

/// drill_gated: a fragile move that HAS a bank trains on the drill only.
/// The carrier is held until a clean rep clears the status.
#[test]
fn fragile_move_with_a_drill_bank_drills_instead_of_solving() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problem("1", problem(&["target"]));
    fx.stubs().bank = set(&["target"]);
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "drill:target");
}

/// Drilled today and still not clean: the carrier stays held rather than
/// unlocking on drill recency alone (the 227 hole).
#[test]
fn a_drill_already_done_today_holds_the_carrier() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "other"]).problems(vec![
        ("1", problem(&["target"])),
        ("2", problem(&["other"])),
    ]);
    fx.stubs().bank = set(&["target"]);
    fx.stubs().drilled_today = set(&["target"]);
    let st = statuses(&[("target", FRAGILE, Some(1)), ("other", STALE, Some(50))]);
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "other");
}

/// A frontier node whose only walk is a Hard has no carrier at all. Its
/// drill is offered instead of the node being silently skipped.
#[test]
fn missing_move_with_no_carrier_falls_back_to_its_drill() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problem("41", hard(&["target"]));
    fx.stubs().bank = set(&["target"]);
    let st = statuses(&[("target", MISSING, None)]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "drill:target");
}

// --------------------------------------------------------------------------
// sleep
// --------------------------------------------------------------------------

#[test]
fn woken_problem_jumps_the_queue() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "other"]).problems(vec![
        ("1", problem(&["target"])),
        ("2", problem(&["other"])),
    ]);
    let st = statuses(&[("target", FRAGILE, Some(1)), ("other", FRAGILE, Some(200))]);
    let c = fx.run(&no_evidence(), &st, args().woken(&["1"]));
    assert_eq!(pnum(&c), "1");
    assert!(reason(&c).contains("sleep"));
}

/// While a problem sleeps it is excluded everywhere, but its walk's rusty
/// moves still get reps, through a different carrier.
#[test]
fn ground_under_a_sleeping_problem_is_warmed_elsewhere() {
    let mut fx = Fx::picker();
    fx.nodes(&["rusty", "solid"]).problems(vec![
        ("1", problem(&["rusty", "solid"])),
        ("2", problem(&["rusty"])),
    ]);
    let st = statuses(&[("rusty", FRAGILE, Some(1)), ("solid", SOLID, Some(1))]);
    let c = fx.run(&no_evidence(), &st, args().asleep(&["1"]));
    assert_eq!(
        (target(&c), pnum(&c)),
        ("rusty".to_string(), "2".to_string())
    );
    assert!(reason(&c).contains("sleeping"));
}

// --------------------------------------------------------------------------
// session start
// --------------------------------------------------------------------------

/// Inside the session-start window the first pick is juice: an all-SOLID
/// easy, nothing rusty and nothing new.
#[test]
fn session_start_serves_a_trivial_easy() {
    let mut fx = Fx::picker();
    fx.nodes(&["solid", "rusty"])
        .problems(vec![("1", easy(&["solid"])), ("2", problem(&["rusty"]))]);
    let st = statuses(&[("solid", SOLID, Some(1)), ("rusty", FRAGILE, Some(1))]);
    let c = fx.run(&no_evidence(), &st, args().session_start());
    assert_eq!(
        (pnum(&c), c.as_ref().unwrap().status),
        ("1".to_string(), SOLID)
    );
    assert!(reason(&c).contains("session start"));
}

/// A problem solved inside the cooldown is muscle memory, not a warmup.
#[test]
fn session_start_skips_a_warmup_done_this_week() {
    let mut fx = Fx::picker();
    fx.nodes(&["solid"])
        .problems(vec![("1", easy(&["solid"])), ("2", easy(&["solid"]))]);
    let ev = evidence(vec![solve("1", &[("solid", "clean")], 2)]);
    let st = statuses(&[("solid", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&ev, &st, args().session_start())), "2");
}

/// No trivial easy in the bank must not swallow the pick: normal rules
/// resume in the same call.
#[test]
fn session_start_falls_through_when_no_easy_qualifies() {
    let mut fx = Fx::picker();
    fx.nodes(&["rusty"]).problem("1", problem(&["rusty"]));
    let st = statuses(&[("rusty", FRAGILE, Some(1))]);
    assert_eq!(
        t3(&fx.run(&no_evidence(), &st, args().session_start())),
        tup("rusty", FRAGILE, "1")
    );
}

// --------------------------------------------------------------------------
// anti-dodge
// --------------------------------------------------------------------------

/// When the last evidence for a move says it was routed around, the
/// carrier is chosen for having no recorded escape route.
#[test]
fn dodged_move_gets_a_carrier_that_resists_the_dodge() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "solid"]).problems(vec![
        ("1", problem(&["target", "solid"]).alt_walks(&[&["solid"]])), // escapable
        ("2", problem(&["target", "solid"])),                          // not
    ]);
    let ev = evidence(vec![solve("9", &[("target", "avoided")], 3)]);
    let st = statuses(&[("target", FRAGILE, Some(3)), ("solid", SOLID, Some(1))]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(pnum(&c), "2");
    assert!(reason(&c).contains("dodge"));
}

// --------------------------------------------------------------------------
// exhaustion: the case that made `make next` go quiet
// --------------------------------------------------------------------------

/// `make next` was never about basecamps: with nothing rusty left, the
/// answer to "what now" is an all-green Hard, served as a normal pick.
#[test]
fn an_all_solid_graph_serves_a_summit() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"])
        .problems(vec![("1", easy(&["a"])), ("76", hard(&["a"]))]);
    let st = statuses(&[("a", SOLID, Some(1))]);
    let c = fx.run(&no_evidence(), &st, args());
    assert_eq!(
        (pnum(&c), c.as_ref().unwrap().status),
        ("76".to_string(), SOLID)
    );
    assert!(reason(&c).contains("summit"));
}

/// Fewest gaps on the route wins, not the shortest walk. 76 carries an
/// unmapped trick, so 4 is closer even with the longer walk.
#[test]
fn the_most_reachable_summit_goes_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b", "c"]).problems(vec![
        ("4", hard(&["a", "b", "c"])),
        ("76", hard(&["a"]).unmapped(&["a trick with no node"])),
    ]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("c", SOLID, Some(1)),
    ]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "4");
}

#[test]
fn a_summited_hard_is_not_offered_again() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problem("76", hard(&["a"]));
    let st = statuses(&[("a", SOLID, Some(1))]);
    let ev = evidence(vec![solve("76", &[("a", "clean")], 30)]);
    assert!(fx.run(&ev, &st, args()).is_none());
}

/// Every node solid, every Hard already summited: there is genuinely
/// nothing to serve, and None is the honest answer.
#[test]
fn nothing_to_pick_returns_none_when_no_summit_is_green() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problem("1", problem(&["a"]));
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

/// The real state of the graph on 2026-08-20: counting-sort-buckets is
/// MISSING, its only walk is a Hard (so no carrier can exist), and it has
/// no drill bank, so every pick() branch fell through and `make next`
/// printed nothing about the one node still standing between here and an
/// all-solid graph. pick() still returns None, but the blockage is now
/// nameable. (The node has a bank today, so the empty bank directory is
/// what keeps the state the test is about.)
#[test]
fn a_node_walked_only_by_hards_is_reported_as_blocked() {
    let mut fx = Fx::picker();
    fx.nodes(&["counting-sort-buckets"])
        .problem("41", hard(&["counting-sort-buckets"]));
    let st = statuses(&[("counting-sort-buckets", MISSING, None)]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());

    let b = fx.blocked(&no_evidence(), &st, &[], &[]);
    let [(nid, status, why, dry)] = b.as_slice() else {
        panic!("{b:?}")
    };
    assert_eq!(
        (nid.as_str(), *status, *dry),
        ("counting-sort-buckets", MISSING, true)
    );
    assert!(why.contains("Hard") && why.contains("41"));
    assert!(why.contains("no drill exists"));
}

// --------------------------------------------------------------------------
// starvation: a due move nothing was aimed at for STARVED_DAYS in a row
// --------------------------------------------------------------------------

/// The simulator's starvation, measured on the real evidence: a move
/// that has been due STARVED_DAYS days running with no rep of it in that
/// time. A rep of any verdict ends the run (b: picked and failed three
/// days ago is the draw, not the picker); a move due for a few days is
/// merely waiting (c).
#[test]
fn a_move_due_for_two_weeks_with_nothing_aimed_at_it_is_starved() {
    let mut fx = Fx::new();
    fx.nodes(&["a", "b", "c"]).problems(vec![
        ("1", problem(&["a"])),
        ("2", problem(&["b"])),
        ("3", problem(&["c"])),
    ]);
    let ev = evidence(vec![
        solve("1", &[("a", "struggled")], 20),
        solve("2", &[("b", "struggled")], 20),
        solve("2", &[("b", "struggled")], 3),
        solve("3", &[("c", "struggled")], STARVED_DAYS - 1),
    ]);
    let ctx = fx.ctx();
    assert_eq!(
        starved(&ctx, &fx.pv(), &ev, today()),
        vec![("a".to_string(), 20)]
    );
}

/// Due is pick()'s own kind(), not just rusty: a young SOLID move whose
/// graduating rep fell due (the sparse ladder's first floor after its one
/// clean day, since one problem carries it) and never came is starved
/// from the floor date, not from the clean day. The curve is off so the
/// window is the flat one and the count is exact.
#[test]
fn a_young_solid_move_past_its_floor_is_starved_too() {
    let mut fx = Fx::new();
    fx.flat_window()
        .nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a"])), ("2", problem(&["b"]))]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean")], 20),
        solve("2", &[("b", "clean")], 1),
    ]);
    let floor = GRAD_LADDER_SPARSE[0];
    let ctx = fx.ctx();
    assert_eq!(
        starved(&ctx, &fx.pv(), &ev, today()),
        vec![("a".to_string(), 20 - floor + 1)]
    );
}

/// A MISSING move is due once every prereq is SOLID (the one-new-move
/// rule), so its run starts the day the last prereq went clean - the
/// prereq's evidence is read as of each day, not as of today.
#[test]
fn a_missing_move_is_starved_only_from_the_day_its_prereqs_went_solid() {
    let mut fx = Fx::new();
    fx.flat_window()
        .nodes(&["p", "m"])
        .prereqs("m", &["p"])
        .problems(vec![("1", problem(&["p"])), ("2", problem(&["p", "m"]))]);
    let ev = evidence(vec![solve("1", &[("p", "clean")], STARVED_DAYS - 2)]);
    let ctx = fx.ctx();
    assert_eq!(starved(&ctx, &fx.pv(), &ev, today()), vec![]); // due 13 days counting today
    let ev = evidence(vec![solve("1", &[("p", "clean")], STARVED_DAYS + 5)]);
    let hungry = starved(&ctx, &fx.pv(), &ev, today());
    assert_eq!(
        hungry.iter().find(|(n, _)| n == "m").map(|(_, d)| *d),
        Some(STARVED_DAYS + 6)
    );
}

/// Nothing due and nothing blocked are different answers: only the second
/// one is a to-do, so an all-solid graph must report an empty frontier.
#[test]
fn an_all_solid_graph_has_no_blocked_frontier() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problem("1", problem(&["a"]));
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert!(fx.blocked(&no_evidence(), &st, &[], &[]).is_empty());
}

/// pick() preferring something else is not a blockage.
#[test]
fn a_servable_node_is_not_called_blocked() {
    let mut fx = Fx::picker();
    fx.nodes(&["frag", "stale"])
        .problems(vec![("1", problem(&["frag"])), ("2", problem(&["stale"]))]);
    let st = statuses(&[("frag", FRAGILE, Some(1)), ("stale", STALE, Some(50))]);
    assert!(fx.blocked(&no_evidence(), &st, &[], &[]).is_empty());
}

/// A move with a real carrier that has already been solved today is
/// blocked for today only: the reason has to say so rather than claiming
/// the bank is missing something.
#[test]
fn a_node_whose_carriers_are_all_spent_today_is_blocked() {
    let mut fx = Fx::picker();
    fx.nodes(&["target"]).problem("1", problem(&["target"]));
    let st = statuses(&[("target", FRAGILE, Some(1))]);
    let b = fx.blocked(&no_evidence(), &st, &[], &["1"]);
    let [(nid, _, why, dry)] = b.as_slice() else {
        panic!("{b:?}")
    };
    assert_eq!((nid.as_str(), *dry), ("target", false));
    assert!(why.contains("already solved today"));
}

/// Its carrier exists and is not a Hard; it just needs another move made
/// solid first. That is a different to-do from writing a drill.
#[test]
fn a_node_blocked_only_by_a_second_rusty_move_says_so() {
    let mut fx = Fx::picker();
    fx.nodes(&["target", "alsorusty"])
        .problem("1", problem(&["target", "alsorusty"]));
    let st = statuses(&[
        ("target", FRAGILE, Some(1)),
        ("alsorusty", FRAGILE, Some(1)),
    ]);
    let reasons: HashMap<String, String> = fx
        .blocked(&no_evidence(), &st, &[], &[])
        .into_iter()
        .map(|(nid, _, why, _)| (nid, why))
        .collect();
    assert!(reasons["target"].contains("second rusty move"));
}

/// When basecamp is dry the answer to "what now" is a summit.
#[test]
fn an_all_green_hard_is_offered_as_the_summit() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problems(vec![("76", hard(&["a", "b"])), ("1", easy(&["a"]))]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    assert_eq!(fx.summits(&no_evidence(), &st), strs(&["76"]));
}

#[test]
fn a_hard_with_a_rusty_move_is_not_ready() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problem("76", hard(&["a", "b"]));
    let st = statuses(&[("a", SOLID, Some(1)), ("b", FRAGILE, Some(1))]);
    assert!(fx.summits(&no_evidence(), &st).is_empty());
}

/// Reachability is the whole input tree, not just the walk: a solid move
/// resting on a rusty prereq is still a gap on the route.
#[test]
fn a_hard_with_a_rusty_prereq_is_not_ready() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "deep"])
        .prereqs("a", &["deep"])
        .problem("76", hard(&["a"]));
    let st = statuses(&[("a", SOLID, Some(1)), ("deep", STALE, Some(200))]);
    assert!(fx.summits(&no_evidence(), &st).is_empty());
}

/// 295 was being served as all-green while carrying "balance two heaps to
/// maintain a running median", a trick with no node in the taxonomy. An
/// unmapped move is unroutable new ground, so it counts as a gap.
#[test]
fn a_hard_with_an_unmapped_move_is_not_ready() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problem(
        "295",
        hard(&["a"]).unmapped(&["balance two heaps for a running median"]),
    );
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert!(fx.summits(&no_evidence(), &st).is_empty());
}

/// The simmer rule: SOLID is not enough for a summit. A young badge from
/// one burst of drills has not proven it can carry a Hard yet, so an
/// immature move counts as a gap on the route.
#[test]
fn a_hard_with_an_immature_move_is_not_ready() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problem("76", hard(&["a", "b"]));
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    assert!(fx.summits(&no_evidence(), &st).is_empty());
}

#[test]
fn an_already_summited_hard_is_not_offered_again() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problem("76", hard(&["a"]));
    let st = statuses(&[("a", SOLID, Some(1))]);
    let ev = evidence(vec![solve("76", &[("a", "clean")], 30)]);
    assert!(fx.summits(&ev, &st).is_empty());
}

/// rank_summits is the ordering `make hard` uses, and `make next` shares
/// it so the two can never name different summits.
#[test]
fn summits_are_ranked_by_reachability_then_number() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problems(vec![
        ("212", hard(&["a"])),
        ("76", hard(&["a"])),
        ("4", hard(&["a"])),
    ]);
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert_eq!(fx.summits(&no_evidence(), &st), strs(&["4", "76", "212"]));
}

/// `make hard` only ever offers interview classics, so `make next` puts
/// them first rather than serving a summit `make hard` would never name.
#[test]
fn a_classic_summit_outranks_a_non_classic_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problems(vec![
        ("76", hard(&["a"])),   // a CLASSIC
        ("3000", hard(&["a"])), // not
    ]);
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert_eq!(fx.summits(&no_evidence(), &st), strs(&["76"]));
}

/// It is not blocked, it is simply not up yet: reporting it would turn
/// the frontier list into noise.
#[test]
fn a_missing_node_behind_a_rusty_prereq_is_not_on_the_frontier() {
    let mut fx = Fx::picker();
    fx.nodes(&["prereq", "new"])
        .prereqs("new", &["prereq"])
        .problems(vec![("1", hard(&["new"])), ("2", problem(&["prereq"]))]);
    let st = statuses(&[("prereq", FRAGILE, Some(1)), ("new", MISSING, None)]);
    assert!(fx.blocked(&no_evidence(), &st, &[], &[]).is_empty());
}

// --------------------------------------------------------------------------
// "after" edges: a problem waits for the problem its walk builds on
// --------------------------------------------------------------------------

/// 47 declares "after": ["46"]. With both cold, plain freshness sorting
/// would serve 47 (older last solve) - the hold flips it to 46, the core
/// the variation builds on.
#[test]
fn a_problem_waits_for_its_due_predecessor() {
    let mut fx = Fx::picker();
    fx.nodes(&["bt"]).problems(vec![
        ("46", problem(&["bt"])),
        ("47", problem(&["bt"]).after(&["46"])),
    ]);
    let ev = evidence(vec![
        solve("46", &[("bt", "clean")], 299),
        solve("47", &[("bt", "clean")], 300),
    ]);
    let st = statuses(&[("bt", STALE, Some(299))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("bt", STALE, "46"));
}

/// Once 46 has a clean solve inside the solid window, 47 rejoins the
/// pool and wins on freshness (least recently solved).
#[test]
fn a_warm_predecessor_releases_the_problem() {
    let mut fx = Fx::picker();
    fx.nodes(&["bt"]).problems(vec![
        ("46", problem(&["bt"])),
        ("47", problem(&["bt"]).after(&["46"])),
    ]);
    let ev = evidence(vec![
        solve("46", &[("bt", "clean")], 3),
        solve("47", &[("bt", "clean")], 300),
    ]);
    let st = statuses(&[("bt", STALE, Some(300))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("bt", STALE, "47"));
}

/// A learning rep is not recall evidence anywhere else either.
#[test]
fn a_learning_predecessor_solve_does_not_release() {
    let mut fx = Fx::picker();
    fx.nodes(&["bt"]).problems(vec![
        ("46", problem(&["bt"])),
        ("47", problem(&["bt"]).after(&["46"])),
    ]);
    let ev = evidence(vec![
        solve_a("46", &[("bt", "clean")], 10, level("learning")),
        solve("46", &[("bt", "clean")], 299),
        solve("47", &[("bt", "clean")], 300),
    ]);
    let st = statuses(&[("bt", STALE, Some(299))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("bt", STALE, "46"));
}

/// The move stayed rusty because the solve did not evidence it, but the
/// problem is still in working memory: the picker must not hand back
/// yesterday's problem this morning.
#[test]
fn a_carrier_solved_days_ago_is_not_a_spaced_review() {
    let mut fx = Fx::picker();
    fx.nodes(&["bt"])
        .problems(vec![("46", problem(&["bt"])), ("47", problem(&["bt"]))]);
    let ev = evidence(vec![
        solve("46", &[], 1),
        solve("47", &[("bt", "clean")], 300),
    ]);
    let st = statuses(&[("bt", STALE, Some(300))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("bt", STALE, "47"));
}

/// When the whole pool is inside the cooldown the node waits its turn:
/// better an empty review slot than a rerun of this week's work.
#[test]
fn every_carrier_still_warm_serves_nothing() {
    let mut fx = Fx::picker();
    fx.nodes(&["bt"])
        .problems(vec![("46", problem(&["bt"])), ("47", problem(&["bt"]))]);
    let ev = evidence(vec![solve("46", &[], 1), solve("47", &[], 2)]);
    let st = statuses(&[("bt", STALE, Some(300))]);
    assert!(fx.run(&ev, &st, args()).is_none());
}

/// If the predecessor can never be offered, the hold would deadlock: a
/// banned one releases the edge.
#[test]
fn a_banned_predecessor_holds_nothing_back() {
    let mut fx = Fx::picker();
    fx.nodes(&["bt"]).problems(vec![
        ("46", problem(&["bt"]).banned()),
        ("47", problem(&["bt"]).after(&["46"])),
    ]);
    let ev = evidence(vec![solve("47", &[("bt", "clean")], 300)]);
    let st = statuses(&[("bt", STALE, Some(300))]);
    assert_eq!(t3(&fx.run(&ev, &st, args())), tup("bt", STALE, "47"));
}

/// Free-mode evidence records only what the code did, so a starved move
/// whose carrier was solved another way during the run gets nothing and
/// is served again. routed_around names that move with the carrier that
/// went around it (a); a starved move whose carriers were simply never
/// solved is starved, not routed around (b); a carrier solved around
/// BEFORE the run began does not count (c).
#[test]
fn a_starved_move_solved_around_on_a_carrier_is_served_forced() {
    let mut fx = Fx::new();
    fx.nodes(&["a", "b", "c", "x"]).problems(vec![
        ("1", problem(&["a", "x"])),
        ("2", problem(&["b"])),
        ("3", problem(&["c", "x"])),
    ]);
    let ev = evidence(vec![
        solve("1", &[("a", "struggled"), ("x", "clean")], 20),
        solve("1", &[("x", "clean")], 5),      // a: went around
        solve("2", &[("b", "struggled")], 20), // b: nothing since
        solve("3", &[("c", "struggled")], 20),
        solve("3", &[("x", "clean")], 25), // c: before the run
    ]);
    let ctx = fx.ctx();
    let hungry: HashSet<String> = starved(&ctx, &fx.pv(), &ev, today())
        .into_iter()
        .map(|(n, _)| n)
        .collect();
    assert_eq!(hungry, set(&["a", "b", "c"]));
    assert_eq!(
        routed_around(&ctx, &fx.pv(), &ev, today()),
        vec![("a".to_string(), "1".to_string())]
    );
}

// --------------------------------------------------------------------------
// the summit gate under recognition (rule 4)
// --------------------------------------------------------------------------

fn recog_rec(pnum: &str, kind: &str, moves: &[(&str, &str)], days_ago: i64) -> RecogRec {
    RecogRec {
        date: iso(days_ago),
        problem: Some(pnum.to_string()),
        kind: Some(kind.to_string()),
        moves: moves
            .iter()
            .map(|(k, v)| (k.to_string(), v.to_string()))
            .collect(),
    }
}

/// A Hard whose entry move was FAILED_TO_RECOGNIZE on the last solve is
/// not a summit until a spot rep clears the move.
#[test]
fn a_summit_is_held_while_its_entry_move_failed_to_recognize() {
    let mut fx = Fx::picker();
    fx.nodes(&["ms"]).problem("84", hard(&["ms"]));
    let st = statuses(&[("ms", SOLID, Some(0))]);
    let summits = |recog: &Recog| {
        ready_hards(
            &fx.ctx(),
            &fx.pv(),
            &no_evidence(),
            &st,
            None,
            Some(recog),
            today(),
        )
    };
    assert_eq!(summits(&Recog::new()), strs(&["84"]));
    let mut held = Recog::new();
    held.insert(
        "solved/p84_3.py".into(),
        recog_rec("84", "solve", &[("ms", recog::MISSED)], 3),
    );
    assert!(summits(&held).is_empty());
    let mut cleared = held.clone();
    cleared.insert(
        "recognition/s9_1.md".into(),
        recog_rec("9", "spot", &[("ms", recog::HIT)], 1),
    );
    assert_eq!(summits(&cleared), strs(&["84"]));
}
