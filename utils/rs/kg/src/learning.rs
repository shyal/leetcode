// Learning mode (settled 2026-10-18): LEARNING=1 in .envrc.
//
// Every first sight was a game for the rating, so each loss was a loss of
// rating. In learning mode a solve is evidence for its moves and no game:
// kg_solved marks the record `"learning": true`, and model::scored_games
// leaves it out the way it leaves out a studied file. A later rep of the
// problem is a repeat.
//
// Learning mode gates every first sight it serves (kg_next): a first sight
// with no "after" list gets one from the gate model (kg::queue), at every
// rating, and a gate that is not warm is served in its place. The same
// check runs on the gate. A repeat is not gated: it was solved once.
// Unset or anything but 1 switches the mode off.

use std::collections::HashSet;

use chrono::NaiveDate;

use crate::bank::warm;
use crate::ctx::{Ctx, PView};
use crate::data::env_str;
use crate::evidence::Evidence;

/// LEARNING=1 switches the mode on.
pub fn enabled() -> bool {
    env_str("LEARNING").trim() == "1"
}

/// The first problem in `after` that is not warm (no clean solve in the
/// last SOLID_WINDOW_DAYS), or None. A drill in the list has its own
/// clock in the picker, and a problem that is banned, paid only or in
/// `skip` (asleep, solved today) is passed over.
pub fn cold_gate(
    ctx: &Ctx,
    after: &[String],
    pv: &PView,
    ev: &Evidence,
    today: NaiveDate,
    skip: &HashSet<String>,
) -> Option<String> {
    after
        .iter()
        .find(|g| {
            let servable = match pv.get(g).or_else(|| ctx.ro.get(g)) {
                Some(p) => !ctx.unservable(g, p),
                None => !ctx.paid_only(g),
            };
            servable
                && !skip.contains(*g)
                && ctx.vertex_kind(g, &pv.map) == Some("problem")
                && warm(ctx, g, pv, ev, today, false) == Some(false)
        })
        .cloned()
}
