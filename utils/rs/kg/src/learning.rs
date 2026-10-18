// Learning mode (settled 2026-10-18): LEARNING=1 in .envrc.
//
// Every first sight was a game for the rating, so each loss was a loss of
// rating. In learning mode a solve is evidence for its moves and no game:
// kg_solved marks the record `"learning": true`, and model::scored_games
// leaves it out the way it leaves out a studied file. A later rep of the
// problem is a repeat.
//
// Learning mode serves a problem in his band only when it is gated by
// his own solves (kg_next): a problem with no "after" list gets one from
// the gate model (kg::queue), whose candidates are the problems he has
// solved clean, so no gate is ever served. A problem whose gates are not
// all solved clean, or with a piece none of his solves isolates, is held,
// and the picker picks the next one.
// Unset or anything but 1 switches the mode off.

use std::collections::HashSet;

use crate::ctx::{Ctx, PView};
use crate::data::env_str;
use crate::drills::drill_gate_warm;
use crate::evidence::Evidence;
use crate::status::last_clean_solve;

/// LEARNING=1 switches the mode on.
pub fn enabled() -> bool {
    env_str("LEARNING").trim() == "1"
}

/// The problems with a clean solve on record: the gate candidates.
pub fn solved_clean(ev: &Evidence) -> HashSet<String> {
    ev.recs
        .iter()
        .map(|(_, r)| r.problem_str())
        .filter(|p| !last_clean_solve(ev, p).is_empty())
        .collect()
}

/// The first gate in `after` that does not clear the problem, or None. A
/// problem gate clears it with a clean solve on record, a drill gate with
/// DRILL_GATE_REPS clean days. A banned or paid-only gate counts for
/// nothing.
pub fn unmet_gate(ctx: &Ctx, after: &[String], pv: &PView, ev: &Evidence) -> Option<String> {
    after
        .iter()
        .find(|g| {
            if ctx.vertex_kind(g, &pv.map) == Some("drill") {
                return !ctx
                    .drill_path(g)
                    .is_some_and(|p| drill_gate_warm(ctx, &p, ev));
            }
            let servable = match pv.get(g).or_else(|| ctx.ro.get(g)) {
                Some(p) => !ctx.unservable(g, p),
                None => !ctx.paid_only(g),
            };
            servable && last_clean_solve(ev, g).is_empty()
        })
        .cloned()
}
