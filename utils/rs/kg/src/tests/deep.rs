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

/// Block 2: a due repeat that uses the technique comes before the new
/// problems.
#[test]
fn a_due_repeat_of_the_technique_comes_before_its_new_problems() {
    let (fx, recs, st) = fixture();
    test_env("KG_DEEP", "2");
    let c = fx.run(&evidence(recs), &st, args());
    assert_eq!(target(&c), "weak");
    assert!(["1", "2"].contains(&pnum(&c).as_str()));
    assert!(reason(&c).contains("a due repeat"));
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
