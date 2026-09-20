// The replay (review_ahead), the park (rule 0b), the .envrc knobs, and
// the assist axis helpers the judge and `make solved` share.

use std::collections::HashSet;

use indexmap::IndexMap;
use serde_json::json;

use super::*;
use crate::data::{
    apply_assist_floor, envrc_pairs, normalise_assist, notes_assist_level, test_env,
    SOLID_WINDOW_DAYS,
};
use crate::drills::{drill_review_cap, drill_scheduler, group_caps, new_drill_cap};
use crate::git::{sleep_lines, GitState};
use crate::pick::{park_full_lines, review_ahead, review_line, withheld, Choice};

// --------------------------------------------------------------------------
// review_ahead: the review between now and the first pick that is new ground
// --------------------------------------------------------------------------

fn ahead(fx: &Fx, ev: &Evidence) -> (i64, i64, bool) {
    review_ahead(&fx.ctx(), &fx.pv(), ev, &[], &HashSet::new(), None, 14, 200)
}

/// A fragile move with a bank: one clean drill clears it, and the Hard
/// whose walk is then all solid is new ground. One drill, no problems.
#[test]
fn review_ahead_counts_a_gated_drill_before_the_summit() {
    let mut fx = Fx::picker();
    fx.flat_window()
        .nodes(&["a", "b"])
        .problems(vec![("1", problem(&["a"])), ("2", hard(&["a", "b"]))]);
    fx.stubs().bank = set(&["a"]);
    let ev = evidence(vec![
        solve("1", &[("a", "struggled")], 1),
        solve("3", &[("b", "clean")], 1),
    ]);
    assert_eq!(ahead(&fx, &ev), (1, 0, true));
}

/// An ordinary stale move re-solves its carrier: that is one problem of
/// review, then the summit.
#[test]
fn review_ahead_counts_a_stale_re_solve_as_a_problem() {
    let mut fx = Fx::picker();
    fx.flat_window()
        .nodes(&["a"])
        .problems(vec![("1", problem(&["a"])), ("2", hard(&["a"]))]);
    let ev = evidence(vec![solve("1", &[("a", "clean")], SOLID_WINDOW_DAYS + 5)]);
    assert_eq!(ahead(&fx, &ev), (0, 1, true));
}

/// Every move solid: the first pick is already the summit.
#[test]
fn review_ahead_is_zero_when_the_pick_is_new_ground() {
    let mut fx = Fx::picker();
    fx.flat_window().nodes(&["a"]).problem("2", hard(&["a"]));
    let ev = evidence(vec![solve("1", &[("a", "clean")], 1)]);
    assert_eq!(ahead(&fx, &ev), (0, 0, true));
}

/// The granted rep changes what is served next: once the prereq's drill
/// is clean the dependent it held gets its own drill. Two drills, then
/// new ground.
#[test]
fn review_ahead_follows_a_released_dependent() {
    let mut fx = Fx::picker();
    fx.flat_window()
        .nodes(&["a", "b"])
        .prereqs("b", &["a"])
        .problem("2", hard(&["a", "b"]));
    fx.stubs().bank = set(&["a", "b"]);
    let ev = evidence(vec![solve(
        "1",
        &[("a", "struggled"), ("b", "struggled")],
        1,
    )]);
    assert_eq!(ahead(&fx, &ev), (2, 0, true));
}

#[test]
fn review_ahead_restores_the_clock() {
    let mut fx = Fx::picker();
    fx.flat_window().nodes(&["a"]).problem("2", hard(&["a"]));
    let ctx = fx.ctx();
    review_ahead(
        &ctx,
        &fx.pv(),
        &no_evidence(),
        &[],
        &HashSet::new(),
        None,
        14,
        200,
    );
    assert_eq!(ctx.today(), today());
}

#[test]
fn review_line_wording() {
    assert_eq!(
        review_line(2, 1, true, 14),
        "review ahead: 2 drills, 1 problem over the next 14 days, then new ground (if every rep is clean)"
    );
    assert_eq!(
        review_line(0, 0, true, 14),
        "review ahead: none - this pick is new ground"
    );
    assert_eq!(
        review_line(0, 0, false, 14),
        "review ahead: none in the next 14 days, and nothing new to serve either"
    );
    assert_eq!(
        review_line(3, 0, false, 7),
        "review ahead: 3 drills over the next 7 days, and still nothing new (if every rep is clean)"
    );
}

fn levels(pairs: &[(&str, &str)]) -> Option<IndexMap<String, String>> {
    Some(
        pairs
            .iter()
            .map(|(k, v)| (k.to_string(), v.to_string()))
            .collect(),
    )
}

/// 2026-09-01: a drill whose notes read "Asked for a walkthrough." was
/// filed with no assist because the judge did not act on the note. The
/// word in the notes is authoritative; the judge's answer is a floor.
#[test]
fn the_level_word_in_the_notes_is_the_mark() {
    assert_eq!(
        notes_assist_level("Asked for a walkthrough."),
        "walkthrough"
    );
    assert_eq!(notes_assist_level("one hint on the pop"), "hint");
    assert_eq!(
        notes_assist_level("hinted, then walked through"),
        "walkthrough"
    );
    assert_eq!(
        notes_assist_level("learning rep, copied the solution"),
        "learning"
    );
    assert_eq!(notes_assist_level(""), "none");
    assert_eq!(notes_assist_level("solved it cold"), "none");
    // the floor lands on the drill's TRAINS node and raises, never lowers
    let a = strs(&["a"]);
    assert_eq!(
        apply_assist_floor(None, "walkthrough", &a),
        levels(&[("a", "walkthrough")])
    );
    assert_eq!(
        apply_assist_floor(levels(&[("a", "hint")]), "walkthrough", &a),
        levels(&[("a", "walkthrough")])
    );
    assert_eq!(
        apply_assist_floor(levels(&[("a", "learning")]), "hint", &a),
        levels(&[("a", "learning")])
    );
    assert_eq!(
        apply_assist_floor(levels(&[("b", "hint")]), "walkthrough", &a),
        levels(&[("b", "hint"), ("a", "walkthrough")])
    );
    assert_eq!(
        apply_assist_floor(levels(&[("a", "hint")]), "none", &a),
        levels(&[("a", "hint")])
    );
    assert_eq!(apply_assist_floor(None, "none", &a), None);
}

#[test]
fn normalise_assist_stores_the_per_move_shape() {
    let moves = strs(&["a", "b"]);
    assert_eq!(
        normalise_assist(Some(&json!({"a": "hint"})), &moves),
        levels(&[("a", "hint")])
    );
    assert_eq!(
        normalise_assist(
            Some(&json!({"a": "hint", "zzz": "hint", "b": "none"})),
            &moves
        ),
        levels(&[("a", "hint")])
    );
    assert_eq!(
        normalise_assist(Some(&json!("hint")), &moves),
        levels(&[("a", "hint"), ("b", "hint")])
    );
    assert_eq!(normalise_assist(Some(&json!("none")), &moves), None);
    assert_eq!(normalise_assist(Some(&json!({})), &moves), None);
    assert_eq!(normalise_assist(None, &moves), None);
}

// --------------------------------------------------------------------------
// rule 0b: a full park withholds new ground, review still flows
// --------------------------------------------------------------------------

fn choice(target: &str, status: Status, pnum: &str, reason: &str) -> Choice {
    Choice {
        target: target.to_string(),
        status,
        pnum: pnum.to_string(),
        reason: reason.to_string(),
    }
}

/// 2026-09-01: four problems asleep, cap three, and make next kept
/// serving as if nothing were parked. At the cap a new-ground pick is
/// held back; a review pick is not.
#[test]
fn a_full_park_withholds_new_ground_but_not_review() {
    let _fx = Fx::new();
    test_env("MAX_ASLEEP", "3");
    let full = strs(&["1", "2", "3"]);
    let new_move = choice("m", MISSING, "9", "new move");
    let summit = choice("m", SOLID, "9", "summit: gentlest all-solid Hard");
    let review = choice("m", STALE, "9", "spaced re-solve");
    assert!(withheld(Some(&new_move), &full));
    assert!(withheld(Some(&summit), &full));
    assert!(!withheld(Some(&review), &full));
    assert!(!withheld(Some(&new_move), &strs(&["1", "2"])));
    assert!(!withheld(None, &full));
}

#[test]
fn the_park_full_message_names_the_ways_out() {
    let _fx = Fx::new();
    test_env("MAX_ASLEEP", "3");
    let lines = park_full_lines(&strs(&["1235", "752"]));
    assert_eq!(lines.len(), 1);
    assert!(lines[0].starts_with("2 asleep (cap 3)"));
    assert!(
        lines[0].contains("make wake")
            && lines[0].contains("make failed")
            && lines[0].contains("learning")
    );
}

/// 2026-09-01: the park must be seen daily, not only when make sleep
/// refuses. sleep_lines is what make next prints at the bottom and what
/// make sleep -- --list prints; one line per park.
#[test]
fn the_park_is_listed_under_every_make_next() {
    let mut fx = Fx::new();
    fx.nodes(&["a", "b"])
        .problem("7", problem(&["a", "b"]).title("Parked One"));
    let slept = 1_756_000_000;
    let mut events = HashMap::new();
    events.insert(
        "7-slept".to_string(),
        (
            "abc".to_string(),
            vec![
                (slept - 86_400, "sleeping: first".to_string()),
                (slept, "sleeping: again".to_string()),
            ],
        ),
    );
    let git = GitState {
        heads: vec![("7-slept".to_string(), "abc".to_string())],
        branch_events: events,
        ..Default::default()
    };
    fx.git = Some(git);
    let mut st = statuses(&[("a", SOLID, Some(1)), ("b", STALE, Some(40))]);
    let lines = sleep_lines(&fx.ctx(), &fx.pv(), &no_evidence(), &st);
    assert_eq!(lines.len(), 1);
    assert!(lines[0].starts_with("7. Parked One - asleep (warming: b)"));
    assert!(lines[0].contains("slept x2") && lines[0].ends_with("make wake 7 when you choose"));
    st.insert("b".into(), (SOLID, Some(ago(1))));
    assert!(sleep_lines(&fx.ctx(), &fx.pv(), &no_evidence(), &st)[0]
        .contains("ground solid, simmering"));
    fx.git = Some(GitState::default());
    assert!(sleep_lines(&fx.ctx(), &fx.pv(), &no_evidence(), &st).is_empty());
}

/// The repo's .envrc is read like a dotenv file: literal exports are
/// taken, shell expansions are left alone.
#[test]
fn envrc_knobs_hold_without_direnv() {
    let fx = Fx::new();
    std::fs::write(
        fx.dir.0.join(".envrc"),
        "export MAX_ASLEEP=5\n\
         # a comment\n\
         \n\
         export NAME=\"quoted value\"\n\
         SINGLE='x$y'\n\
         export PYTHONPATH=./utils/:${PYTHONPATH}\n\
         export SET_ALREADY=new\n\
         not a var line\n",
    )
    .unwrap();
    let pairs: Vec<(String, String)> = envrc_pairs(&fx.dir.0);
    assert_eq!(
        pairs,
        vec![
            ("MAX_ASLEEP".to_string(), "5".to_string()),
            ("NAME".to_string(), "quoted value".to_string()),
            ("SINGLE".to_string(), "x$y".to_string()),
            ("SET_ALREADY".to_string(), "new".to_string()),
        ]
    );
    assert!(envrc_pairs(&fx.dir.0.join("missing")).is_empty());
}

/// The operator's own knobs (DRILL_SCHEDULER=anki in .envrc) would answer
/// for the defaults these tests assert: under `cargo test` the process
/// environment is never read, and a test that wants a knob sets it
/// itself (data::test_env).
#[test]
fn the_envrc_knobs_do_not_reach_the_suite() {
    let _fx = Fx::new();
    assert_eq!(drill_scheduler(), "node");
    assert!(group_caps().is_empty());
    assert_eq!(new_drill_cap(), None);
    assert_eq!(drill_review_cap(), None);
}
