# Technique Graph

A skill is a graph of moves; a problem is a walk through that graph. This directory is the
explicit version of that model, used to gate assignments (preflight), pick spaced repeats,
and generate combination drills ("rote sheets").

## Files

- **nodes.json** — the curated move taxonomy. A node is one atomic, drillable move
  (`streaming-ask-then-record`), finer than a LeetCode topic tag (`hash_table`). Each node
  carries prerequisite edges and a <5-minute micro-drill for when it's missing.
- **problems.json** — problem → the list of nodes its clean solution walks. `alt_walks`
  records legitimate alternative solutions (e.g. 1512 batch-math vs streaming) — a solve
  only evidences the walk it actually took.
- **evidence.json** — per solve-file: which moves the actual code exercised, verdict
  `clean` / `struggled` / `avoided`. Append-only, keyed by filename like `.summaries.json`.

## The drill bank (../drills/)

`drills/<node-id>/*.py` is a growing bank of self-authored, leetcode-style drill files —
statement, `Solution` skeleton, asserts — each targeting one node. The docstring headers
route everything automatically:

    DRILL: Next Greater Index      <- title (instead of "290. Word Pattern")
    TRAINS: monotonic-stack        <- node id(s) this drill evidences

Workflow is identical to leetcode problems: `make drill <node-id>` copies the
least-recently-drilled file into current.py; solve; `make solved` files it as
`solved/d_<title>_<ts>.py` and kg_extract records drill evidence against the TRAINS
nodes (problem = "drill"; problems.json is never touched; leetcode solve stats ignore
d-files). Every drill improvised in chat gets deposited here afterwards, so the rote
sheet grows with every gap found.

## Dive (`make dive`)

`make next` is greedy and memoryless — each run picks the single globally-oldest rusty
node, so consecutive sessions hop between unrelated topics. `make dive` answers "where
should I spend a whole session?": rusty (non-SOLID) nodes are clustered by shared curated
group or direct prereq edge, clusters are scored by urgency mass (FRAGILE 3 · STALE 2 ·
MISSING 1), and the heaviest cluster becomes a themed session of up to 3 problems
(`make dive 5` for a longer one, `make dive <group>` to override the pick). Prereqs are scheduled before
dependents, and each pick is simulated as a clean solve so later carriers may stand on
earlier targets; the one-new-move rule still gates every carrier. Solve top-down,
`make solved` after each, re-run — the plan re-derives from fresh evidence.

## Hard (`make hard`)

`make next`/`make dive` work the rusty frontier bottom-up; `make hard` works top-down
from a summit. `make hard 42` takes that problem's full input tree (walk + transitive
prereqs), finds every non-SOLID node in it, and plans one base camp per gap — a carrier
problem chosen the way kg_dive chooses (spaced re-solve / gentle fresh carrier /
anti-dodge; Hard carriers sort last — a camp is never itself a summit), or a drill when
no carrier is READY. Camps are simulated as clean solves, so after the last camp the
summit's walk is all-SOLID and the summit is a pure combination rep. `make hard` with no
argument scores a curated shortlist of interview-classic Hards by route length (fewest
gaps; unmapped-node proposals count as gaps — unroutable territory is distance) and
routes to the closest one. Unmapped candidates cost one claude call, cached into
problems.json like preflight. Solve top-down, `make solved` after each camp, re-run —
the route re-derives and shrinks.

## Sleep (`make sleep`)

Stuck mid-exercise and looping — no new idea in ~15 minutes? `make sleep` parks the
problem for 24h in `sleep.json`: kg_next won't offer it, warms its walk's rusty
moves/prereqs meanwhile (via other carriers), and on expiry the problem jumps the
queue for a fresh from-scratch attempt. Your half-written attempt is parked on branch
`<num>-slept` if you want to peek. One active sleep at a time — it's an incubation
tool for failed retrieval, not a snooze button for discomfort. No evidence is
recorded on sleep: the code is the evidence, and there is no code yet.

## Rules

1. **Mastery is derived, never stored.** Status comes from evidence dates at query time:
   SOLID while the personal forgetting curve (`graph/curve.json`, refit with `make curve`)
   predicts ≥90% recall — stability grows ~1.3× per clean rep, so windows expand with
   repetition (1 rep ≈ 2 months, 5 reps ≈ 5+) · below that = STALE · once-only or
   struggled = FRAGILE · no evidence = MISSING. Delete curve.json to fall back to a flat
   42-day window. Nothing goes stale by sitting in a file.
2. **One new move per assignment.** A problem is READY when at most one of its moves is
   non-SOLID — that move is the training target. Two or more → prep first: spaced re-solve
   for STALE, micro-drill for MISSING/FRAGILE.
3. **Evidence discipline.** A topic tag or problem title is not evidence; the code is.
   Solving a streaming-carrier problem with batch math records `avoided` on the streaming
   move, not `clean`.
4. **Node fission.** When a stumble reveals a hidden sub-move inside a node (2006 exposed
   `solve-pair-condition` hiding inside `derived-key-lookup`), split the node rather than
   widening it. The taxonomy is expected to grow at the frontier of whatever is being drilled.
5. **Curated taxonomy.** Extractors must map onto existing node ids; genuinely new moves go
   to a review queue, not straight into nodes.json.
