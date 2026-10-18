// Learning mode (settled 2026-10-18): LEARNING=1 in .envrc.
//
// Every first sight was a game for the rating, so each loss was a loss of
// rating. In learning mode a solve is evidence for its moves and no game:
// kg_solved marks the record `"learning": true`, and model::scored_games
// leaves it out the way it leaves out a studied file. A later rep of the
// problem is a repeat.
//
// Learning mode gates every problem it serves (kg_next), at every rating,
// repeats too: a problem with no "after" list gets one from the gate
// model (kg::queue), and a gate that is not warm is served in its place.
// The same check runs on the gate. A problem the check cannot clear is
// held, and the picker picks the next one. Only a problem with no plainer
// candidate below it (the floor) is served with no gates.
// Unset or anything but 1 switches the mode off.

use std::collections::HashSet;

use chrono::NaiveDate;

use crate::bank::warm;
use crate::ctx::{Ctx, PView};
use crate::data::env_str;
use crate::drills::drill_gate_warm;
use crate::evidence::Evidence;

/// LEARNING=1 switches the mode on.
pub fn enabled() -> bool {
    env_str("LEARNING").trim() == "1"
}

/// What a problem's "after" list asks before it is served.
#[derive(Debug, PartialEq)]
pub enum GateState {
    /// every gate warm: serve the problem
    Warm,
    /// this gate first: serve it, with the same check on it
    Cold(String),
    /// a gate that is not warm and cannot be served now (asleep, solved
    /// today, a drill that is not warm): hold the problem
    Held(String),
}

/// The state of `after`, gate by gate in its order; the first gate that
/// is not warm decides. A problem gate is warm with a clean solve in the
/// last SOLID_WINDOW_DAYS, a drill gate with DRILL_GATE_REPS clean days.
/// A banned or paid-only gate can never be served and counts for nothing.
pub fn gate_state(
    ctx: &Ctx,
    after: &[String],
    pv: &PView,
    ev: &Evidence,
    today: NaiveDate,
    skip: &HashSet<String>,
) -> GateState {
    for g in after {
        if ctx.vertex_kind(g, &pv.map) == Some("drill") {
            let warm = ctx
                .drill_path(g)
                .is_some_and(|p| drill_gate_warm(ctx, &p, ev));
            if !warm {
                return GateState::Held(g.clone());
            }
            continue;
        }
        let servable = match pv.get(g).or_else(|| ctx.ro.get(g)) {
            Some(p) => !ctx.unservable(g, p),
            None => !ctx.paid_only(g),
        };
        if !servable || warm(ctx, g, pv, ev, today, false) != Some(false) {
            continue;
        }
        if skip.contains(g) {
            return GateState::Held(g.clone());
        }
        return GateState::Cold(g.clone());
    }
    GateState::Warm
}
