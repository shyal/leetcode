// The predicted tier: the frontier mover (a due node with no evidenced
// carrier promotes a drafted problem), the THIN kind (a young move off
// its ladder is proved on a real problem), and rule 6 (an unsolved
// drafted problem in reach, Hards first).

use std::collections::HashSet;

use super::*;
use crate::bank::unlocks;

// --------------------------------------------------------------------------
// the frontier mover (PLAN.md phase 4)
// --------------------------------------------------------------------------

/// The 2026-08-28 dry basecamp: the frontier node's only mapped walk is
/// a Hard, but the predicted tier has an easy whose drafted walk needs
/// nothing but the target. Promote it instead of starving.
#[test]
fn a_missing_move_with_no_mapped_carrier_promotes_a_draft() {
    let mut fx = Fx::picker();
    fx.nodes(&["csb"])
        .problem("41", hard(&["csb"]))
        .draft("9001", drafted(&["csb"]), "Easy");
    let st = statuses(&[("csb", MISSING, None)]);
    let (c, pv) = fx.run_pv(&no_evidence(), &st, args());
    assert_eq!(t3(&c), tup("csb", MISSING, "9001"));
    assert!(reason(&c).contains("predicted"));
    assert!(pv.get("9001").unwrap().predicted); // in-memory entry for rendering
    assert_eq!(pv.get("9001").unwrap().moves, strs(&["csb"]));
}

/// The 2026-08-29 carousel was drafts for one move coming back mapped to
/// something else, one after another. The cutoff that answered it
/// (DRAFT_MISSES = 2) latched 27 moves off the drafted tier for good and
/// sent them back to repeats, so it is gone; what stops the carousel now
/// is that a draft is promoted once. A problem with any evidence at all
/// is not new ground, whether or not the judge has mapped it yet.
#[test]
fn a_draft_already_solved_is_never_promoted() {
    let mut fx = Fx::picker();
    fx.nodes(&["csb"]).problem("41", hard(&["csb"]));
    for num in ["1365", "1893", "2149"] {
        fx.draft(num, drafted(&["csb"]), "Easy");
    }
    let st = statuses(&[("csb", MISSING, None)]);
    let ev = evidence(vec![
        solve("1365", &[("dav", "clean")], 1),
        solve("1893", &[("sa", "clean")], 0),
    ]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "2149");
}

/// Drafts are 0.80/0.75 guesses; a mapped carrier is truth. Promotion
/// fires only when the evidenced bank has nothing.
#[test]
fn an_evidenced_carrier_outranks_promotion() {
    let mut fx = Fx::picker();
    fx.nodes(&["m"])
        .problem("1", problem(&["m"]))
        .draft("9001", drafted(&["m"]), "Easy");
    let st = statuses(&[("m", FRAGILE, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "1");
}

/// A mapped carrier the move has never been given is "not today", not
/// "never": an evidenced walk outranks a drafted guess, so the node waits
/// for its carrier to wake instead of promoting.
#[test]
fn an_unsolved_carrier_is_waited_out_not_promoted() {
    let mut fx = Fx::picker();
    fx.nodes(&["m"])
        .problem("1", problem(&["m"]))
        .draft("9001", drafted(&["m"]), "Easy");
    let st = statuses(&[("m", FRAGILE, Some(1))]);
    let got = fx.run(&no_evidence(), &st, args().asleep(&["1"]));
    assert!(got.is_none() || pnum(&got) != "9001");
}

/// The other half of the same rule: a mapped carrier already solved is a
/// repeat, and a repeat does not outrank new ground. Waiting out its
/// cooldown serves nothing today and serves the same problem again after.
/// 2026-09-07: 467 of the 486 mapped carriers were solved, so the old
/// "any mapped carrier" gate had silenced the frontier mover completely
/// and the picker served repeats with 3087 drafts untouched.
#[test]
fn every_mapped_carrier_solved_promotes_a_draft() {
    let mut fx = Fx::picker();
    fx.nodes(&["m"])
        .problem("1", problem(&["m"]))
        .draft("9001", drafted(&["m"]), "Easy");
    let ev = evidence(vec![solve("1", &[("m", "struggled")], 1)]);
    let st = statuses(&[("m", FRAGILE, Some(1))]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "9001");
}

/// A drafted walk with a second non-solid move is not a carrier: the ZPD
/// constraint applies to the predicted tier unchanged.
#[test]
fn a_promoted_walk_obeys_the_one_new_move_rule() {
    let mut fx = Fx::picker();
    fx.nodes(&["t", "alsorusty"])
        .problem("41", hard(&["t"]))
        .draft("9001", drafted(&["t", "alsorusty"]), "Easy");
    let st = statuses(&[("t", MISSING, None), ("alsorusty", STALE, Some(60))]);
    let got = fx.run(&no_evidence(), &st, args());
    assert!(got.is_none() || pnum(&got) != "9001");
}

/// Hards stay summits even in the predicted tier.
#[test]
fn a_drafted_hard_is_never_promoted() {
    let mut fx = Fx::picker();
    fx.nodes(&["t"]).draft("9001", drafted(&["t"]), "Hard");
    let st = statuses(&[("t", MISSING, None)]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

/// A walk the taxonomy cannot express yet is not a carrier for anything:
/// its unexpressed move would ride along as a hidden second gap.
#[test]
fn a_missing_flagged_draft_is_not_promoted() {
    let mut fx = Fx::picker();
    fx.nodes(&["t"])
        .draft("9001", drafted_missing(&["t"], &["fenwick-tree"]), "Easy");
    let st = statuses(&[("t", MISSING, None)]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

/// Cheap regime first: between two qualifying drafts, the one whose
/// rarest supporting move has more problems rehearsing it wins (the
/// connectivity threshold finding), before problem-number order.
#[test]
fn promotion_prefers_the_heavily_rehearsed_walk() {
    let mut fx = Fx::picker();
    fx.nodes(&["t", "common", "rare"]);
    for i in 1..6 {
        fx.problem(&i.to_string(), problem(&["common"]));
    }
    fx.problem("10", problem(&["rare"]))
        .draft("9001", drafted(&["t", "rare"]), "Easy")
        .draft("9002", drafted(&["t", "common"]), "Easy");
    let st = statuses(&[
        ("t", MISSING, None),
        ("common", SOLID, Some(1)),
        ("rare", SOLID, Some(1)),
    ]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "9002");
}

/// heap-lazy-eviction on 2026-08-28: STALE, only walk is a Hard. The
/// spaced re-solve is impossible, so the rep comes from a drafted carrier.
#[test]
fn a_stale_move_with_no_carrier_promotes_a_draft() {
    let mut fx = Fx::picker();
    fx.nodes(&["hle"])
        .problem("218", hard(&["hle"]))
        .draft("9001", drafted(&["hle"]), "Medium");
    let st = statuses(&[("hle", STALE, Some(50))]);
    assert_eq!(
        t3(&fx.run(&no_evidence(), &st, args())),
        tup("hle", STALE, "9001")
    );
}

/// pick() would promote a draft for it, so it is servable, not blocked.
#[test]
fn a_promotable_node_is_not_called_blocked() {
    let mut fx = Fx::picker();
    fx.nodes(&["t"])
        .problem("41", hard(&["t"]))
        .draft("9001", drafted(&["t"]), "Easy");
    let st = statuses(&[("t", MISSING, None)]);
    assert!(fx.blocked(&no_evidence(), &st, &[], &[]).is_empty());
}

/// With the predicted tier empty the blockage message must say the
/// drafts were considered and none qualified.
#[test]
fn blocked_report_says_no_draft_can_carry() {
    let mut fx = Fx::picker();
    fx.nodes(&["t"]).problem("41", hard(&["t"]));
    let st = statuses(&[("t", MISSING, None)]);
    let b = fx.blocked(&no_evidence(), &st, &[], &[]);
    let [(nid, _, why, _)] = b.as_slice() else {
        panic!("{b:?}")
    };
    assert_eq!(nid, "t");
    assert!(why.contains("no drafted walk"));
}

// --------------------------------------------------------------------------
// the THIN kind: a young move off its ladder is proved on a real problem
// --------------------------------------------------------------------------

/// Every node SOLID, no summit ready, so the picker used to say nothing.
/// `b` is SOLID but young: it has never carried a real problem at its bar.
/// Serve the Medium that carries it with every other move SOLID - the rep
/// that widens its breadth (kg_lib.node_axes) and matures it.
#[test]
fn a_young_move_is_proved_when_nothing_else_is_due() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a", "b"])), ("2", problem(&["a"]))]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 40)]);
    let c = fx.run(&no_evidence(), &st, args());
    assert_eq!(t3(&c), tup("b", SOLID, "1"));
    assert!(reason(&c).contains("40"));
}

fn flat_model(fx: &mut Fx, ratings: &[(&str, f64)]) {
    fx.stubs().solve_model = Some(fmap(&[("intercept", 0.0), ("rating", -1.0)]));
    fx.stubs().solve_ratings = Some(fmap(ratings));
}

/// Two carriers prove the same young move. The cold-solve model puts one
/// near the target pass rate and one well above it; the rep goes to the
/// one that can actually fail, not to the gentler problem.
#[test]
fn the_proving_carrier_nearest_the_target_pass_rate_wins() {
    let mut fx = Fx::picker();
    flat_model(&mut fx, &[("1", 1500.0), ("2", 1100.0)]);
    fx.nodes(&["a", "b"]);
    // problem 1 sits at p = 0.50, problem 2 at p = 0.73: 1 is the test
    fx.problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "b"])),
    ]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 40)]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "1");
}

/// The fit can keep a `length` term (it did on 2026-09-16, at -0.60) and
/// the picker must price it: at one rating, the intercept puts a one-move
/// walk above the target and the length term brings a two-move walk down
/// onto it, so the longer walk is the test. Before solve_logit knew the
/// term both priced the same and the one-move walk won on gentleness.
#[test]
fn a_fitted_length_term_prices_the_walk() {
    let mut fx = Fx::picker();
    fx.stubs().solve_model = Some(fmap(&[("intercept", 0.69), ("length", -1.0)]));
    fx.stubs().solve_ratings = Some(fmap(&[("1", 1500.0), ("2", 1500.0)]));
    fx.nodes(&["a", "b"]);
    // problem 1 sits at p = 0.50 (0.69 - ln 2), problem 2 at p = 0.67
    fx.problems(vec![("1", problem(&["a", "b"])), ("2", problem(&["b"]))]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 40)]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "1");
}

/// A problem with no contest rating cannot be placed on the scale, so it
/// keeps its old gentleness order behind every problem that can.
#[test]
fn an_unpriced_carrier_sorts_behind_the_priced_ones() {
    let mut fx = Fx::picker();
    flat_model(&mut fx, &[("2", 1500.0)]);
    fx.nodes(&["a", "b"]).problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "b"])),
    ]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 40)]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "2");
}

/// 2026-09-13: multi-source-bfs had every proving carrier solved, and the
/// drafted fallback served 2812 at rating 2154 (7% odds) on connectivity
/// alone. The drafted tier now takes the proving path's order: among
/// drafts whose walk needs only the target, the one the cold-solve model
/// puts nearest the target pass rate, so the rep can actually fail.
#[test]
fn the_drafted_carrier_nearest_the_target_pass_rate_wins() {
    let mut fx = Fx::picker();
    flat_model(&mut fx, &[("9001", 900.0), ("9002", 1500.0)]);
    fx.nodes(&["m"]).problem("1", problem(&["m"]));
    let ev = evidence(vec![solve("1", &[("m", "struggled")], 1)]);
    let st = statuses(&[("m", FRAGILE, Some(1))]);
    // 9001 sits at p = 0.82, 9002 at p = 0.50: 9002 is the test
    for num in ["9001", "9002"] {
        fx.draft(num, drafted(&["m"]), "Medium");
    }
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "9002");
}

/// A draft with no contest rating keeps the old connectivity order,
/// behind every draft the model can place on the scale.
#[test]
fn an_unpriced_draft_sorts_behind_the_priced_ones() {
    let mut fx = Fx::picker();
    flat_model(&mut fx, &[("9002", 1100.0)]);
    fx.nodes(&["m"]).problem("1", problem(&["m"]));
    let ev = evidence(vec![solve("1", &[("m", "struggled")], 1)]);
    let st = statuses(&[("m", FRAGILE, Some(1))]);
    for num in ["9001", "9002"] {
        fx.draft(num, drafted(&["m"]), "Medium");
    }
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "9002");
}

#[test]
fn the_young_move_with_the_most_reach_goes_first() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b", "c"]).problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "c"])),
    ]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("c", SOLID, Some(1)),
    ]);
    fx.stubs().immature = set(&["b", "c"]);
    fx.stubs().gain = map(&[("b", 5), ("c", 90)]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "2");
}

/// Breadth is owed whether or not a drafted problem waits on the move: a
/// young node also holds back every summit whose route crosses it
/// (route_gaps counts immature as a gap). The count only orders THIN
/// moves and decorates the reason.
#[test]
fn a_young_move_nobody_waits_on_is_still_proved() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problem("1", problem(&["a", "b"]));
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = HashMap::new();
    let c = fx.run(&no_evidence(), &st, args());
    assert_eq!(t3(&c), tup("b", SOLID, "1"));
    assert!(!reason(&c).contains("wait on it"));
}

/// THIN sits in the frontier, ahead of new ground: a summit is a pure
/// combination rep, and a move not yet proven on a second problem is
/// ground still being laid. Once b is mature the summit is served.
#[test]
fn a_thin_move_outranks_a_summit() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a", "b"])), ("76", hard(&["a"]))]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 40)]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "1");
    fx.stubs().immature.clear();
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "76");
}

#[test]
fn a_thin_move_waits_behind_a_stale_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b", "c"]).problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "c"])),
    ]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("c", STALE, Some(50)),
    ]);
    fx.stubs().immature.insert("b".into());
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "c");
}

#[test]
fn a_thin_move_goes_before_a_missing_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b", "c"]).problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "c"])),
    ]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("c", MISSING, None),
    ]);
    fx.stubs().immature.insert("b".into());
    assert_eq!(target(&fx.run(&no_evidence(), &st, args())), "b");
}

/// One unaided rep yesterday puts b on the graduating ladder; the floor
/// paces its next rep, so THIN does not fire the day after.
#[test]
fn a_young_move_on_its_ladder_waits_for_its_floor() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "b"])),
    ]);
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let ev = evidence(vec![solve("1", &[("a", "clean"), ("b", "clean")], 1)]);
    fx.stubs().immature.insert("b".into());
    assert!(fx.run(&ev, &st, args()).is_none());
}

/// Two young moves, both off the ladder (a 30-day gap survived): the one
/// with the lower degree of ownership (kg_lib.node_degree) is proved
/// first, whatever waits on the other. c has one unaided carrier at its
/// bar (breadth 0.5); b has only its drill (0.25).
#[test]
fn thin_moves_order_by_degree() {
    let mut fx = Fx::picker();
    fx.flat_window().nodes(&["a", "b", "c"]).problems(vec![
        ("1", problem(&["a", "b"])),
        ("2", problem(&["a", "c"])),
        ("3", problem(&["a", "c"])),
    ]);
    let st = statuses(&[
        ("a", SOLID, Some(1)),
        ("b", SOLID, Some(1)),
        ("c", SOLID, Some(1)),
    ]);
    let ev = evidence(vec![
        solve("2", &[("c", "clean")], 40),
        solve("2", &[("c", "clean")], 10),
        drill_file("solved/d_Thing_1.py", "b", 40, Assist::None),
        drill_file("solved/d_Thing_2.py", "b", 10, Assist::None),
    ]);
    fx.stubs().immature = set(&["b", "c"]);
    fx.stubs().gain = map(&[("b", 1), ("c", 90)]);
    assert_eq!(target(&fx.run(&ev, &st, args())), "b");
}

/// The only evidenced carrier of `b` is a Medium, so its bar is Medium;
/// that carrier already gave b its rep, so the floor rep widens to the
/// drafted tier - and an easy there is not proof at the bar, so the
/// Medium draft is promoted.
#[test]
fn a_medium_bar_young_move_promotes_a_drafted_medium_not_an_easy() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a", "b"])), ("2", problem(&["a"]))])
        .draft("9001", drafted(&["a", "b"]), "Easy")
        .draft("9002", drafted(&["a", "b"]), "Medium");
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let ev = evidence(vec![
        solve("2", &[("a", "clean")], 60), // a is off its ladder
        solve("1", &[("a", "clean"), ("b", "clean")], 30),
    ]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 40)]);
    let (c, pv) = fx.run_pv(&ev, &st, args());
    assert_eq!(
        (target(&c), pnum(&c)),
        ("b".to_string(), "9002".to_string())
    );
    assert!(pv.get("9002").unwrap().predicted);
    assert!(reason(&c).contains("drafted"));
}

/// 102 on 2026-09-01: the only evidenced Medium carrier of `b` had
/// already given it a clean rep, and cooled, so rule 5 served it again
/// while 18 drafted Mediums waited. A second rep of the same problem
/// proves memory of that problem, not carry: a draft goes first.
#[test]
fn a_counted_carrier_yields_to_a_drafted_medium() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problem("1", problem(&["a", "b"]))
        .draft("9002", drafted(&["a", "b"]), "Medium");
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean"), ("b", "clean")], 40),
        solve("1", &[("a", "clean"), ("b", "clean")], 10),
    ]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 18)]);
    let c = fx.run(&ev, &st, args());
    assert_eq!(
        (target(&c), pnum(&c)),
        ("b".to_string(), "9002".to_string())
    );
}

#[test]
fn a_counted_carrier_is_re_solved_when_no_draft_exists() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"]).problem("1", problem(&["a", "b"]));
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean"), ("b", "clean")], 40),
        solve("1", &[("a", "clean"), ("b", "clean")], 10),
    ]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 18)]);
    let c = fx.run(&ev, &st, args());
    assert_eq!((target(&c), pnum(&c)), ("b".to_string(), "1".to_string()));
    assert!(reason(&c).contains("re-solve"));
}

#[test]
fn a_fresh_evidenced_carrier_still_outranks_a_draft() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problems(vec![
            ("1", problem(&["a", "b"])),
            ("2", problem(&["a", "b"])),
        ])
        .draft("9002", drafted(&["a", "b"]), "Medium");
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let ev = evidence(vec![
        solve("1", &[("a", "clean"), ("b", "clean")], 40),
        solve("1", &[("a", "clean"), ("b", "clean")], 10),
    ]);
    fx.stubs().immature.insert("b".into());
    fx.stubs().gain = map(&[("b", 18)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args())), "2");
}

#[test]
fn unlocks_counts_a_young_move_as_a_gap() {
    let mut fx = Fx::new();
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.predicted.insert("9001".into(), drafted(&["a", "b"]));
    fx.predicted.insert("9002".into(), drafted(&["a"]));
    let ctx = fx.ctx();
    assert_eq!(
        unlocks(&ctx, &st, &fx.pv(), &HashSet::new()),
        HashMap::new()
    );
    assert_eq!(unlocks(&ctx, &st, &fx.pv(), &set(&["b"])), map(&[("b", 1)]));
}

// --------------------------------------------------------------------------
// rule 6: an unsolved drafted problem in reach, Hards first
// --------------------------------------------------------------------------

/// The 2026-08-31 simulation: 180 days of a solid graph, one Hard
/// served, P(onsite) flat. Once nothing is rusty, new, young or a mapped
/// summit, what is left is the drafted catalog itself.
#[test]
fn a_solid_graph_serves_an_unsolved_drafted_hard() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problem("1", problem(&["a", "b"]))
        .draft("9001", drafted(&["a", "b"]), "Hard");
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    let (c, pv) = fx.run_pv(&no_evidence(), &st, args());
    assert_eq!(
        (c.as_ref().unwrap().status, pnum(&c)),
        (SOLID, "9001".to_string())
    );
    assert!(pv.get("9001").unwrap().predicted);
    assert!(reason(&c).contains("in reach"));
}

/// A Hard opens the day; after a Hard solved today the next pick is a
/// Medium, after that Medium a Hard again. Easies come last either way.
#[test]
fn drafted_hards_and_mediums_alternate_within_a_day() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"])
        .problem("1", problem(&["a"]))
        .draft("9001", drafted(&["a"]), "Medium")
        .draft("9002", drafted(&["a"]), "Hard")
        .draft("9003", drafted(&["a"]), "Easy");
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "9002");
    fx.problem("9002", hard(&["a"]));
    let ev = evidence(vec![solve("9002", &[("a", "clean")], 0)]);
    assert_eq!(pnum(&fx.run(&ev, &st, args().exclude(&["9002"]))), "9001");
    fx.problem("9001", problem(&["a"]));
    let ev = evidence(vec![
        solve("9002", &[("a", "clean")], 0),
        solve("9001", &[("a", "clean")], 0),
    ]);
    assert_eq!(
        pnum(&fx.run(&ev, &st, args().exclude(&["9002", "9001"]))),
        "9003"
    );
}

#[test]
fn a_drafted_problem_on_a_young_move_is_not_in_reach() {
    let mut fx = Fx::picker();
    fx.nodes(&["a", "b"])
        .problem("1", problem(&["a"])) // nothing evidenced carries b: THIN has no rep to serve
        .draft("9001", drafted(&["a", "b"]), "Hard")
        .draft("9002", drafted(&["a"]), "Easy");
    let st = statuses(&[("a", SOLID, Some(1)), ("b", SOLID, Some(1))]);
    fx.stubs().immature.insert("b".into());
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "9002");
}

#[test]
fn a_missing_flagged_draft_is_never_in_reach() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"]).problem("1", problem(&["a"])).draft(
        "9001",
        drafted_missing(&["a"], &["some-trick"]),
        "Hard",
    );
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert!(fx.run(&no_evidence(), &st, args()).is_none());
}

#[test]
fn a_mapped_summit_outranks_a_drafted_one() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"])
        .problem("76", hard(&["a"]))
        .draft("9001", drafted(&["a"]), "Hard");
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert_eq!(pnum(&fx.run(&no_evidence(), &st, args())), "76");
}

#[test]
fn a_drafted_problem_solved_today_is_skipped() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"])
        .problem("1", problem(&["a"]))
        .draft("9001", drafted(&["a"]), "Hard");
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert!(fx
        .run(&no_evidence(), &st, args().exclude(&["9001"]))
        .is_none());
}

#[test]
fn a_group_pick_never_reaches_into_the_drafted_catalog() {
    let mut fx = Fx::picker();
    fx.nodes(&["a"])
        .group(&["a"], "sql")
        .problem("1", problem(&["a"]))
        .draft("9001", drafted(&["a"]), "Hard");
    let st = statuses(&[("a", SOLID, Some(1))]);
    assert!(fx.run(&no_evidence(), &st, args().group("sql")).is_none());
}
