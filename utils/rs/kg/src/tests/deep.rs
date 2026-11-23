// The deep dive (KG_DEEP, deep.rs): one technique a day, its problems
// easy to hard, the memory work after.

use super::*;
use crate::data::test_env;
use crate::deep::{technique, weakness, Scope};

fn failed(pnum: &str, moves: &[(&str, &str)], days_ago: i64) -> (String, Rec) {
    let (_, rec) = solve(pnum, moves, days_ago);
    (format!("solved/p{pnum}_FAILED_{days_ago}.py"), rec)
}

/// Two techniques of one group: `weak` failed both its first sights,
/// `strong` passed both alone. Three problems never met need `weak`, one
/// needs `strong`.
fn fixture() -> (Fx, Vec<(String, Rec)>, Statuses) {
    let mut fx = Fx::picker();
    fx.nodes(&["weak", "strong"])
        .group(&["weak", "strong"], "graphs")
        .problems(vec![
            ("1", problem(&["weak"])),
            ("2", problem(&["weak"])),
            ("3", problem(&["strong"])),
            ("4", problem(&["strong"])),
        ])
        .draft("10", drafted(&["weak"]), "Medium")
        .draft("11", drafted(&["weak"]), "Medium")
        .draft("13", drafted(&["weak"]), "Medium")
        .draft("12", drafted(&["strong"]), "Medium");
    fx.stubs().solve_ratings = Some(fmap(&[
        ("1", 1500.0),
        ("2", 1500.0),
        ("3", 1500.0),
        ("4", 1500.0),
        ("10", 1500.0),
        ("11", 1300.0),
        ("12", 1200.0),
        ("13", 1400.0),
    ]));
    let recs = vec![
        failed("1", &[("weak", "struggled")], 5),
        failed("2", &[("weak", "struggled")], 5),
        solve("3", &[("strong", "clean")], 5),
        solve("4", &[("strong", "clean")], 5),
    ];
    let st = statuses(&[("weak", SOLID, Some(1)), ("strong", SOLID, Some(1))]);
    (fx, recs, st)
}

/// The measure reads first sights only, and the technique with the lower
/// alone share comes first.
#[test]
fn the_weakest_technique_is_the_one_with_the_fewest_first_sights_alone() {
    let (fx, recs, _) = fixture();
    let ctx = fx.ctx();
    let ev = evidence(recs);
    let w = weakness(&ctx, &ev, today());
    assert_eq!(w[0].node, "weak");
    assert_eq!((w[0].met, w[0].alone), (2, 0));
    assert_eq!((w[1].met, w[1].alone), (2, 2));
    let r = crate::model::solve_ratings(&ctx);
    let (weak, scope) = technique(&ctx, &ev, today(), &r).unwrap();
    assert_eq!(weak.node, "weak");
    assert_eq!(scope, Scope::Node("weak".into()));
}

/// A repeat does not count: `weak` solved alone on the second try is
/// still the weakest technique.
#[test]
fn a_repeat_does_not_count_toward_the_measure() {
    let (fx, mut recs, _) = fixture();
    recs.push(solve("1", &[("weak", "clean")], 1));
    let w = weakness(&fx.ctx(), &evidence(recs), today());
    assert_eq!((w[0].node.as_str(), w[0].met, w[0].alone), ("weak", 2, 0));
}

/// Unset, the mode is off: the pick is whatever the ordinary rules give.
#[test]
fn the_mode_is_off_without_kg_deep() {
    let (fx, recs, st) = fixture();
    test_env("NO_REVIEWS", "1");
    let c = fx.run(&evidence(recs), &st, args());
    assert!(c.is_none_or(|c| !c.reason.starts_with("deep dive")));
}

/// The turns: a new problem first, then a due repeat that uses the
/// technique, then a new problem.
#[test]
fn a_new_problem_and_a_repeat_of_the_technique_take_turns() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "2");
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(t3(&c), tup("weak", SOLID, "11"));
    assert!(reason(&c).contains("new problem 1 of 2"));
    recs.push(solve("11", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(target(&c), "weak");
    assert_eq!(pnum(&c), "1");
    assert!(reason(&c).contains("a due repeat"));
    recs.push(solve("1", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert!(reason(&c).contains("new problem 2 of 2"));
}

/// 2026-11-16, a day is one topic: with the new problems done, the
/// repeats of the technique are served, the ones that are not due
/// included, and no problem of the other technique, due or not.
#[test]
fn a_day_serves_no_problem_of_another_technique() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "1");
    recs.push(solve("11", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "1");
    recs.push(solve("1", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "2");
    recs.push(solve("2", &[("weak", "clean")], 0));
    // every problem of `weak` has a record of today: 3, 4 and 12 are left
    let c = fx.run(&evidence(recs), &st, args());
    assert!(c.is_none_or(|c| !["3", "4", "12"].contains(&c.pnum.as_str())));
}

/// A repeat of the technique that is not due is served when no due one
/// is left, the one he did longest ago first.
#[test]
fn a_repeat_that_is_not_due_is_served_the_oldest_first() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "1");
    recs.push(solve("2", &[("weak", "clean")], 4));
    recs.push(solve("1", &[("weak", "clean")], 3));
    recs.push(solve("11", &[("weak", "clean")], 0));
    let ev = evidence(recs);
    let due = crate::clock::due_problems(&ev, today(), None);
    assert!(due.iter().all(|(p, _, _)| p != "1" && p != "2"));
    let c = fx.run(&ev, &st, args());
    assert_eq!(pnum(&c), "2");
    assert!(reason(&c).contains("not due"));
}

/// 2026-11-20: a repeat that is not due is not served in the
/// PROBLEM_GRADUATING_DAYS days after its last record. 3021 was solved
/// clean on 2026-11-19 and came back on 2026-11-20.
#[test]
fn a_repeat_that_is_not_due_is_not_served_too_soon() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "1");
    let gap = crate::clock::PROBLEM_GRADUATING_DAYS;
    recs.push(solve("2", &[("weak", "clean")], gap));
    recs.push(solve("1", &[("weak", "clean")], gap - 1));
    recs.push(solve("11", &[("weak", "clean")], 0));
    let ev = evidence(recs.clone());
    let c = fx.run(&ev, &st, args());
    assert_eq!(pnum(&c), "2");
    recs.push(solve("2", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert!(c.is_none_or(|c| c.pnum != "1"));
}

/// Block 3: with no first sight solved alone on the technique, the first
/// new problem is the easiest one.
#[test]
fn the_first_new_problem_is_the_easiest_of_the_technique() {
    let (fx, recs, st) = fixture();
    test_env("KG_DEEP", "2");
    test_env("NO_REVIEWS", "1");
    let (c, pv) = fx.run_pv(&evidence(recs), &st, args());
    assert_eq!(t3(&c), tup("weak", SOLID, "11"));
    assert!(reason(&c).contains("new problem 1 of 2"));
    assert_eq!(pv.get("11").unwrap().moves, strs(&["weak"]));
}

/// After a pass the next problem is harder; after a fail it is the
/// nearest at or below the failed one, else the easiest left.
#[test]
fn a_pass_goes_up_and_a_fail_does_not() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "3");
    test_env("NO_REVIEWS", "1");
    recs.push(solve("11", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "13");
    recs.push(failed("10", &[("weak", "struggled")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(pnum(&c), "13");
}

/// 2026-11-14: with FIRST_SIGHT_WITHIN_BAND set, a new problem rated more
/// than the band below his first-sight elo is not served: the first one
/// is the easiest at or above the floor, and a fail does not go below
/// it. When every candidate is below the floor, the hardest is served.
#[test]
fn a_new_problem_is_not_below_the_band() {
    use crate::model::first_sight_elo_now;
    let (mut fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "3");
    test_env("NO_REVIEWS", "1");
    test_env("FIRST_SIGHT_WITHIN_BAND", "50");
    ratings_tsv(
        &fx,
        &[
            ("1", 1500.0),
            ("2", 1500.0),
            ("3", 1500.0),
            ("4", 1500.0),
            ("13", 1500.0),
        ],
    );
    let elo = first_sight_elo_now(&fx.ctx(), &evidence(recs.clone()));
    let rate = |fx: &mut Fx, r10: f64, r11: f64, r13: f64| {
        fx.stubs().solve_ratings = Some(fmap(&[
            ("1", 1500.0),
            ("2", 1500.0),
            ("3", 1500.0),
            ("4", 1500.0),
            ("10", r10),
            ("11", r11),
            ("12", 1200.0),
            ("13", r13),
        ]));
    };
    rate(&mut fx, elo + 30.0, elo - 300.0, elo - 40.0);
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "13");
    rate(&mut fx, elo - 60.0, elo - 300.0, elo - 200.0);
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "10");
    rate(&mut fx, elo + 30.0, elo - 300.0, elo - 40.0);
    recs.push(failed("13", &[("weak", "struggled")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(pnum(&c), "10");
}

/// The day's new problems are spent: no problem never met is served by
/// any rule, the other technique's included.
#[test]
fn after_the_new_problems_no_first_sight_is_served() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "1");
    test_env("NO_REVIEWS", "1");
    recs.push(solve("11", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert!(c.is_none_or(|c| !["10", "12", "13"].contains(&c.pnum.as_str())));
}

/// A record of today does not change the technique of the day.
#[test]
fn the_technique_holds_for_the_day() {
    let (fx, mut recs, st) = fixture();
    test_env("KG_DEEP", "3");
    test_env("NO_REVIEWS", "1");
    recs.push(solve("11", &[("weak", "clean")], 0));
    recs.push(solve("13", &[("weak", "clean")], 0));
    recs.push(failed("12", &[("strong", "struggled")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(t3(&c), tup("weak", SOLID, "10"));
}

/// A technique with no problem left takes the never-met problems of its
/// group.
#[test]
fn a_technique_with_no_new_problem_takes_its_group() {
    let mut fx = Fx::picker();
    fx.nodes(&["weak", "strong"])
        .group(&["weak", "strong"], "graphs")
        .problems(vec![("1", problem(&["weak"])), ("3", problem(&["strong"]))])
        .draft("12", drafted(&["strong"]), "Medium");
    fx.stubs().solve_ratings = Some(fmap(&[("1", 1500.0), ("3", 1500.0), ("12", 1200.0)]));
    test_env("KG_DEEP", "2");
    test_env("NO_REVIEWS", "1");
    let recs = vec![
        failed("1", &[("weak", "struggled")], 5),
        solve("3", &[("strong", "clean")], 5),
    ];
    let st = statuses(&[("weak", SOLID, Some(1)), ("strong", SOLID, Some(1))]);
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(t3(&c), tup("weak", SOLID, "12"));
}

/// A named group is his own call and goes past the mode.
#[test]
fn a_named_group_goes_past_the_mode() {
    let (fx, recs, st) = fixture();
    test_env("KG_DEEP", "2");
    test_env("NO_REVIEWS", "1");
    let c = fx.run(&evidence(recs), &st, args().group("graphs"));
    assert!(c.is_none_or(|c| !c.reason.starts_with("deep dive")));
}

/// Three drills are due on the clock: a language drill, the drill of
/// the day's technique and the drill of the other algorithm technique.
/// The language drill is first, the technique's drill second, and the
/// other technique's drill is not served, before the dive or after it.
#[test]
fn only_the_language_drills_and_the_drills_of_the_technique_are_served() {
    let (mut fx, mut recs, st) = fixture();
    fx.nodes(&["query"]).group(&["query"], "sql");
    let st: Statuses = st
        .into_iter()
        .chain(statuses(&[("query", SOLID, Some(1))]))
        .collect();
    test_env("KG_DEEP", "1");
    test_env("NO_REVIEWS", "1");
    test_env("DRILL_SCHEDULER", "anki");
    fx.stubs().clock = vec![
        (PathBuf::from("drills/strong/s.py"), "strong".into()),
        (PathBuf::from("drills/weak/w.py"), "weak".into()),
        (PathBuf::from("drills/query/q.sql"), "query".into()),
    ];
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "drill:query");
    let c = fx.run(
        &evidence(recs.clone()),
        &st,
        args().exclude(&["drill:query"]),
    );
    assert_eq!(pnum(&c), "drill:weak");
    let done = args().exclude(&["drill:query", "drill:weak"]);
    let c = fx.run(&evidence(recs.clone()), &st, done.clone());
    assert!(reason(&c).starts_with("deep dive"));
    // the new problem of the day is done: still no drill of `strong`
    recs.push(solve("11", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs), &st, done);
    assert!(c.is_none_or(|c| c.pnum != "drill:strong"));
}

/// A named group goes past the mode: the clock serves every due drill.
#[test]
fn a_named_group_serves_the_drill_of_another_technique() {
    let (mut fx, recs, st) = fixture();
    test_env("KG_DEEP", "1");
    test_env("DRILL_SCHEDULER", "anki");
    fx.stubs().clock = vec![(PathBuf::from("drills/strong/s.py"), "strong".into())];
    let c = fx.run(&evidence(recs), &st, args().group("graphs"));
    assert_eq!(pnum(&c), "drill:strong");
}

/// The drill of the day's technique is cold: its rep of today was not
/// clean. It holds none of the technique's problems: the due repeat and
/// the new problem are served (2026-11-14: prefix sums, d537, and a day of
/// the due repeats of the other techniques only).
#[test]
fn the_drill_of_the_technique_holds_none_of_its_problems() {
    let (mut fx, mut recs, st) = fixture();
    fx.bank("weak", "Weak Drill", "w.py", "d1", &[]);
    recs.push(drill_rep_v(
        "Weak Drill",
        "weak",
        0,
        "struggled",
        Assist::None,
    ));
    test_env("KG_DEEP", "2");
    let ctx = fx.ctx();
    let ev = evidence(recs.clone());
    let held = crate::bank::held_behind(&ctx, "10", &ctx.predicted_view, &ev, today());
    assert_eq!(held, Some("d1".into()));
    let c = fx.run(&ev, &st, args());
    assert_eq!(target(&c), "weak");
    assert!(reason(&c).contains("new problem 1 of 2"));
    recs.push(solve("11", &[("weak", "clean")], 0));
    let c = fx.run(&evidence(recs), &st, args());
    assert!(reason(&c).contains("a due repeat"));
}

/// 2026-11-20: a drill never done of another algorithm technique is
/// served (d552, d553 and d554 were made that day and never came). The
/// same drill with a rep on file is held, due or not.
#[test]
fn a_drill_never_done_of_another_technique_is_served() {
    let (mut fx, mut recs, st) = fixture();
    let path = fx.bank("strong", "Strong Drill", "s.py", "d2", &[]);
    fx.stubs().clock = vec![(path, "strong".into())];
    test_env("KG_DEEP", "1");
    test_env("NO_REVIEWS", "1");
    test_env("DRILL_SCHEDULER", "anki");
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "drill:strong");
    recs.push(drill_rep("Strong Drill", "strong", 30));
    let c = fx.run(&evidence(recs), &st, args());
    assert!(reason(&c).starts_with("deep dive"));
}

/// `weak` and `strong` on one draft that only the drill of `strong` can
/// hold, under the file clock.
fn held_fixture(days_ago: i64) -> (Fx, Vec<(String, Rec)>, Statuses, PathBuf) {
    let (mut fx, mut recs, st) = fixture();
    let path = fx.bank("strong", "Strong Drill", "s.py", "d2", &[]);
    fx.draft("11", drafted(&["weak", "strong"]), "Medium");
    recs.push(drill_rep("Strong Drill", "strong", days_ago));
    test_env("KG_DEEP", "1");
    test_env("NO_REVIEWS", "1");
    test_env("DRILL_SCHEDULER", "anki");
    (fx, recs, st, path)
}

/// 2026-11-24: the easiest problem of the day waits on a due drill of
/// another technique. The drill is served, and no harder problem in its
/// place; the rep opens the problem.
#[test]
fn a_drill_that_holds_the_next_problem_is_served_first() {
    let (mut fx, mut recs, st, path) = held_fixture(50);
    fx.stubs().clock = vec![(path, "strong".into())];
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "drill:strong");
    assert!(reason(&c).starts_with("11 waits on d2"));
    recs.push(drill_rep("Strong Drill", "strong", 0));
    fx.stubs().clock = vec![];
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(pnum(&c), "11");
}

/// 2026-11-24, d146: a cold drill the drill band has off the clock holds
/// nothing, because no day can serve it.
#[test]
fn a_drill_off_the_clock_holds_no_problem() {
    let (mut fx, recs, st, _) = held_fixture(50);
    let held = |fx: &Fx| {
        let ctx = fx.ctx();
        let ev = evidence(recs.clone());
        crate::bank::held_behind(&ctx, "11", &ctx.predicted_view, &ev, today())
    };
    assert_eq!(held(&fx), Some("d2".into()));
    let rated = [("1", 1500.0), ("2", 1500.0), ("3", 1500.0), ("4", 1500.0)];
    ratings_tsv(&fx, &rated);
    // d2's one target is far above the drill band
    fx.problem("99", problem(&["strong"]).after(&["d2"]));
    test_env("DRILLS_WITHIN_BAND", "50");
    fx.stubs().solve_ratings = Some(fmap(&[
        ("1", 1500.0),
        ("10", 1500.0),
        ("11", 1300.0),
        ("13", 1400.0),
        ("99", 4000.0),
    ]));
    assert_eq!(held(&fx), None);
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "11");
}

/// A drill holds a problem only on a day the clock can serve the drill:
/// cold, and not due yet, it holds nothing.
#[test]
fn every_drill_that_holds_a_problem_is_on_the_clock() {
    use crate::drills::{anki_frontier, node_drill_hold};
    let (mut fx, mut recs, _, _) = held_fixture(50);
    fx.bank("weak", "Weak Drill", "w.py", "d1", &[]);
    fx.bank("weak", "Never Done", "n.py", "d3", &["d1"]);
    for d in [400, 399, 396, 388, 368, 318, 200, 43] {
        recs.push(drill_rep("Weak Drill", "weak", d));
    }
    let ctx = fx.ctx();
    let ev = evidence(recs);
    let clock: Vec<String> = anki_frontier(&ctx, &ev, today(), None, None, false)
        .iter()
        .filter_map(|(p, _)| ctx.drill_id(p))
        .collect();
    assert!(!clock.contains(&"d1".to_string()), "d1 is not due");
    for node in ["weak", "strong"] {
        let held = node_drill_hold(&ctx, node, &ev, today()).expect("a drill is due");
        assert!(clock.contains(&held), "{held} holds {node} off the clock");
    }
}

/// The problem that holds a new problem is served first.
#[test]
fn a_problem_that_holds_the_next_problem_is_served_first() {
    let (mut fx, recs, st) = fixture();
    fx.problem("20", problem(&["strong"]));
    fx.draft("11", drafted(&["weak"]).after(&["20"]), "Medium");
    test_env("KG_DEEP", "1");
    test_env("NO_REVIEWS", "1");
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(pnum(&c), "20");
    assert!(reason(&c).contains("11 waits on 20"));
}

/// 2026-11-24: the band has a ceiling on a deep dive day. 3335 came at
/// 197 above his elo. With no candidate in the band, the nearest to his
/// elo is served.
#[test]
fn a_new_problem_is_not_above_the_band() {
    use crate::model::first_sight_elo_now;
    let (mut fx, recs, st) = fixture();
    test_env("KG_DEEP", "3");
    test_env("NO_REVIEWS", "1");
    test_env("FIRST_SIGHT_WITHIN_BAND", "50");
    ratings_tsv(
        &fx,
        &[("1", 1500.0), ("2", 1500.0), ("3", 1500.0), ("4", 1500.0)],
    );
    let elo = first_sight_elo_now(&fx.ctx(), &evidence(recs.clone()));
    let rate = |fx: &mut Fx, r10: f64, r11: f64, r13: f64| {
        fx.stubs().solve_ratings = Some(fmap(&[("10", r10), ("11", r11), ("13", r13)]));
    };
    rate(&mut fx, elo + 197.0, elo + 40.0, elo + 300.0);
    let c = fx.run(&evidence(recs.clone()), &st, args());
    assert_eq!(pnum(&c), "11");
    rate(&mut fx, elo + 197.0, elo + 70.0, elo - 300.0);
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(pnum(&c), "11");
}
