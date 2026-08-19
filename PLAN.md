# The Cracking Leetcode Plan

The thesis of this repo is that leetcode was never about solving problems, it was about cracking leetcode itself: keeping a small set of core techniques solid, and treating every problem as a walk through them. The endgame of that thesis is reachability on everything: every leetcode problem "in reach", meaning every move in its walk is solid, meaning solvable on sight.

The reach chart in the README already measures this against the 498 problems the graph knows. This plan extends it to all of leetcode, in order.

## Phase 0: clear the current graph (now)

Get every node in the taxonomy solid and keep it there, with the hards as the tests. Nothing below is worth starting before this, because the later phases only change *what gets picked*, and picking doesn't matter while known nodes are still fragile or stale.

Done when: all nodes solid, all hards in the bank summited with an all-solid walk.

## Phase 1: reachability-aware picking

Rank candidate nodes by unlock count: the number of frontier problems blocked *only* by that node. Feed it into the existing picker as a tie-breaker among due nodes. The ZPD constraint stays exactly as it is; this only decides which fragile/stale node to service first when several are due.

This is nearly free: the data (problems.json walks + node states) already exists, and the change is a sort key behind `make next`. Zero UX change.

Done when: `make next` prefers, among equally due nodes, the one that unlocks the most problems.

## Phase 2: walk the whole catalog

Reachability on everything needs walks for ~3600 problems, not 498. Topic tags are too coarse for this taxonomy, so the realistic path is LLM-drafted walks from solution code.

The critical rule: predicted walks and evidenced walks are separate tiers. A drafted walk stays marked `predicted` until i actually solve the problem and kg_extract confirms the walk the code really took. The 498 evidenced problems are the calibration set: draft walks for them blind, compare against ground truth, and only trust the drafts on unseen problems as much as that comparison earns. The reach chart never mixes guesses into the measured curve; predicted reach gets its own line or its own chart.

Done when: every leetcode problem has a walk (evidenced or predicted), with a measured draft-accuracy number attached to the predicted tier.

## Phase 3: complete the taxonomy

The full catalog will surface problems whose walks need moves the taxonomy doesn't have yet. That list, ranked by unlock count, is the map of what the graph is still blind to, and it is arguably the more interesting output than the reach number itself. Each missing node enters the usual way: added to nodes.json with a micro-drill, then trained through carriers.

Done when: no leetcode problem needs a move that isn't a node.

## Phase 4: optimize for reach on everything

With walks on everything and the taxonomy complete, the picker's objective becomes explicit: pick the problem that maximizes expected reachability gain, still under the ZPD constraint, still balanced against the forgetting curve's review debt. Reach against the full catalog becomes the headline chart, and "cracked" has a number: the day the predicted-reach line hits the whole of leetcode.

## The invariants

These hold through every phase:

- the ZPD constraint never loosens: one fragile or stale node per assignment, on a foundation of solid ones
- evidence is only ever what actually happened; predictions live in their own tier
- the drill bank stays the training floor; problems remain the tests
- scheduling defends what reach has built. The Grok-era lesson stands: reach isn't a ratchet, volume without defense bleeds out
