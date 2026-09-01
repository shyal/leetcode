# Technique Graph

A skill is a graph of moves; a problem is a walk through that graph. This directory is the
explicit version of that model, used to gate assignments (preflight), pick spaced repeats,
and generate combination drills ("rote sheets").

## Files

- **nodes.json** — the curated move taxonomy. A node is one atomic, drillable move
  (`streaming-ask-then-record`), finer than a LeetCode topic tag (`hash_table`). Each node
  carries prerequisite edges, a <5-minute micro-drill for when it's missing, and an
  `added` date — when it entered the taxonomy (clamped back to its earliest evidence),
  so kg_movie can introduce nodes when they actually appeared. Set it when adding a node.
- **problems.json** — problem → the list of nodes its clean solution walks. `alt_walks`
  records legitimate alternative solutions (e.g. 1512 batch-math vs streaming) — a solve
  only evidences the walk it actually took. An optional `note` field flags poorly stated
  problems (statement clarifications, disambiguating test cases, real-vs-tagged
  difficulty); `make next` and `make preflight` print it with the assignment so the
  ambiguity is defused before the timer starts. Notes clarify the *statement* only —
  never the walk. An optional `"banned": true` blacklists a problem from ever being
  offered as a carrier (all pickers route through `carriers_for`) — for problems whose
  training value is buried under busywork. The move still gets trained, just via a
  different carrier; preflight still audits banned problems and labels them ⛔.
- **evidence.json** — per solve-file: which moves the actual code exercised, verdict
  `clean` / `struggled` / `avoided`. Append-only, keyed by filename like `data/summaries.json`.
  An optional `assist` field records how much outside help the solve had — a second
  axis, independent of the verdict, read by kg_extract from your own notes in the
  solve file (an explicit `ASSIST: <level>` line overrides its reading):

      none         unaided — the field is omitted
      hint         a nudge: a question, a pointer at the branch that was wrong
      walkthrough  the shape/recurrence was talked through before the code existed
      learning     the solution was given and copied (the first rep of a node)

  The verdict says whether the code worked; `assist` says how much of it was your
  own recall. Clean-but-walked-through is a real solve that is *not* a real rep, so
  it still earns evidence while shrinking the fitted half-life (the `- d*assist`
  term in curve.json) instead of extending it. A `learning` solve doesn't count as a
  clean rep at all — the node falls back to its previous clean date, which is what
  `make sleep` then re-queues.

## The drill bank (../drills/)

`drills/<node-id>/*.py` is a growing bank of self-authored, leetcode-style drill files —
statement, `Solution` skeleton, asserts — each targeting one node. The docstring headers
route everything automatically:

    DRILL: Next Greater Index      <- title (instead of "290. Word Pattern")
    TRAINS: monotonic-stack        <- node id(s) this drill evidences

Workflow is identical to leetcode problems: `make drill <node-id>` (or
`make prepare <node-id>` — prepare routes non-numeric targets here) copies the
least-recently-drilled file into current.py and commits it on a branch named
after the node, off master; solve; `make solved` files it as
`solved/d_<title>_<ts>.py` and kg_extract records drill evidence against the TRAINS
nodes (problem = "drill"; problems.json is never touched; leetcode solve stats ignore
d-files). Every drill improvised in chat gets deposited here afterwards, so the rote
sheet grows with every gap found.

A drill is a vertex of the graph like a problem or a node. Its id is a number
like `d14`, assigned once in `graph/drills.json` and never reused (the way
LeetCode numbers are); the entry carries the DRILL title, which is how the bank
file and the evidence are found, and its edges: `"after": [ids]`, what the drill
builds on. `make prepare d14` serves it. One relation covers the whole graph: an
id in any `after` list (problems.json or drills.json) is a problem number, a
drill id, or a node id,
and `kg_lib.warm` says when it is met (a problem: an unaided all-clean solve inside
the solid window; a drill: its latest rep is one; a node: owned). A problem or a
drill is not served while an id it comes after is not warm (`kg_lib.held_behind`,
`kg_lib.servable_drills`). Filename order inside `drills/<node>/` means nothing.

Drills also surface in `make next` itself (kg_lib.due_drill picks the node's
least-recently-drilled servable bank file; a drill already solved today is not due again).
Precedence follows rule 2, and the drill is a GATE, not just an opener
(`kg_lib.drill_gated`): a MISSING/FRAGILE target — and deep-stale ones, which
re-enter like FRAGILE — whose node has a drill bank trains on the drill ONLY.
No carrier fires for it until a clean rep lifts the node out of the gated
state; since mastery is derived, the gate clears itself the moment the drill
goes clean. A struggled drill holds the carrier (the drill re-offers next
day) — previously mere drill-recency unlocked the carrier the same day, which
is how 227 fired over two struggled drills. The gate is node-side, so
alt walks are unaffected: they change which walk a solve evidences, never
whether a cold move gets a carrier. Nodes with no bank file keep the old
behavior — depositing a drill is what arms the gate. Ordinary STALE keeps
the spaced re-solve on its carrier, with the drill only as fallback when no
carrier is READY.

## Dive (`make dive`)

`make next <group>` (currently `make next sql` and `make next spark`; `--group <g>` on kg_next for any group)
runs the same rules 1-3 over one curated group only, skipping the sleep warm-up and the
summit fallback, so a new node's drills can be worked without the global frontier interrupting.

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

## Sleep (`make sleep` / `make wake`)

Stuck mid-exercise and looping — no new idea in ~15 minutes? `make sleep` parks the
attempt on branch `<num>-slept` and returns you to master. The branch IS the state —
no metadata file: `sleeping:`/`woke:` marker commits on it carry the timestamps and
the park count. Parked problems are the "not ready yet" signal: kg_next won't offer
them, and warms their walks' rusty moves/prereqs meanwhile (via other carriers).

No timers, no auto-wake (settled 2026-08-28): a park sleeps until YOU run
`make wake <n>`, which resumes its branch where it left off, synced forward to
master. Sleep/wake can cycle any number of times. The only pressure is the cap:
at most `MAX_ASLEEP` (kg_lib) parks at once — at the cap, `make sleep` refuses
until one is faced. `make solved` records ACTIVE time only (awake intervals, the
same `solve time:` trailer as ever) plus a `slept:` trailer for the parked stretch.
It's an incubation tool for failed retrieval, not a snooze button for discomfort.
No evidence is recorded on sleep: the code is the evidence, and there is no code yet.

## Force (`make force <n>`)

`make prepare <n>` is freestyle: solve however you like; evidence records what the code
actually did and nothing else. `make force <n>` prepares the same stub but arms a style
judge: the problem's mapped walk is spelled out in plain English at the top of
current.py, and `make solved` REJECTS the merge (the way LeetCode rejects `bin()` on
a count-the-bits problem) if the solve routes around it. `make unforce` drops the
constraint and files freestyle. The constraint lives in `.force.json` (untracked) and
goes stale automatically if a different problem is prepared.

## Recognition (`make prepare spot`)

Execution evidence says whether a move runs once it is named. It says nothing
about the step before: reading an unnamed statement and reaching for the
move. 84 (2026-08-21) and 1760 (2026-09-01) were both that failure, on nodes
whose execution evidence was clean; the picker could not see it because the
two axes were one status.

A spot rep is a problem statement with the title, number and tags removed,
read and answered in free text: which move it calls for, or `direct` when
none does, or `don't know`. No code, about three minutes. Same workflow as
a solve: `make prepare spot` branches `spot-<stamp>` off master and writes
the statement as markdown (emphasis, code, images kept) into `current.md`
with an answer section under the rule; `make solved` files it as
`recognition/s<num>_<title>_<ts>.md`, the judge (kg_extract) maps the answer
onto node ids with one small claude call and scores it against the walk's
entry move, and the commit squash-merges. The problem number appears
nowhere the candidate sees before the answer is in: the branch and the
marker commit carry only the stamp, the pick sits in `.spot.json`
(untracked) until the judge reads it back, and the title is printed only in
the reveal after the judge.

- **What is scored.** Only the first move of the mapped walk and of each
  alt walk (`kg.recognition.entry_nodes`): later moves (`solve-pair-condition`
  inside 1760) are reached while executing, not read off the statement. A
  hit on any entry is a hit; with none, the primary entry is `missed`. Moves
  named that no walk of the problem uses are recorded as `false`
  (over-triggering).
- **graph/recognition.json** is the second axis, keyed by file like
  evidence.json, verdicts `hit` / `missed`. Spot reps land here, and so does
  a solve whose notes say a move was not recognised ("recognition failure,
  not a binary search failure"): the judge reads it from the notes, as it
  reads assist, and the words themselves put the miss on the walk's entry
  move when the judge does not.
- **Status is derived** (`recognition_status`): FAILED_TO_RECOGNIZE when the latest
  event is a miss, RECOGNIZED when it is a hit inside the window (42 days grown
  1.3x per hit), UNTESTED otherwise.
- **Serving.** Recognition is the check on reach. The graph calls a
  problem reachable when every move of its walk is SOLID; the spot rep asks
  whether the statement actually triggers the move it enters through. So
  `make next` serves the node carrying the most reach (unsolved
  reachable problems entering through it, mapped and drafted) whose trigger
  has not been shown recently: not RECOGNIZED inside the window. A
  FAILED_TO_RECOGNIZE node ranks by the same number, ties go to it. The
  carrier is the gentlest problem it reaches; a drafted problem's walk is
  re-derived by the judge (preflight's mapping call) before scoring. The
  line above the pick never names the node. A spotted problem is never
  served for recognition again. A later solve of it after a miss is not
  unaided (the reveal handed over the walk): kg_extract floors its assist to
  `hint`. After a hit it is unaided: the reveal showed nothing the candidate
  had not produced, and the two records sit side by side for the data.
- **Ratio.** `SPOT_EVERY` (env, default 3): one spot rep per that many
  solves, counted over the day. The first rep is due before the day's first
  solve, the next after three more (drills count). `SPOT_EVERY=1` is one per
  solve, `SPOT_EVERY=0` turns spot reps off. The ratio governs only what
  `make next` suggests: `make prepare spot` (or `make spot`) serves a rep
  whenever it is asked for.
- **Summits wait for it.** Rule 4 does not serve a Hard whose entry move is
  FAILED_TO_RECOGNIZE (`kg_next.ready_hards`): the walk has to be seen before the
  climb is a combination rep, and the spot rep is what clears the miss.

## Rules

1. **Mastery is derived, never stored.** Status comes from evidence dates at query time:
   SOLID while the personal forgetting curve (`graph/curve.json`, refit with `make curve`)
   predicts ≥90% recall — stability grows ~1.3× per clean rep, so windows expand with
   repetition (1 rep ≈ 2 months, 5 reps ≈ 5+) · below that = STALE · once-only or
   struggled = FRAGILE · no evidence = MISSING. Struggles and assistance both shrink
   stability, so a helped rep buys a shorter window than an unaided one. Delete
   curve.json to fall back to a flat 42-day window. Nothing goes stale by sitting in
   a file.
2. **One new move per assignment; summits take zero.** An easy/medium is READY when at
   most one of its moves is non-SOLID — that move is the training target. A Hard is READY
   only when its whole walk is SOLID: hards are summits (pure combination reps), never
   refresh carriers — you don't carry rusty gear up the Himalayas. Any gap → prep first:
   spaced re-solve for STALE, micro-drill for MISSING/FRAGILE (`make hard <num>` plans
   the basecamp route).
2b. **A hold must be servable.** The cross-bank hold (`kg_lib.drill_held`) parks a
   dependent behind a banked prereq until that prereq has an unaided clean rep. A
   prereq that is SOLID only through assisted reps is not rusty, so rules 1-3 never
   target it; `make next` serves its drill anyway (the ownership rep, rule 0c in
   kg_next) - a hold nothing can open is a deadlock, not a standard (18 nodes sat
   behind two such prereqs on 2026-08-29). The empty serve tells "nothing due"
   (carriers cooling, prereqs unowned, a ready summit asleep - `make next --why`
   names each wait) apart from "the bank is dry" (no problem can ever carry the
   move - map one).
3. **Evidence discipline.** A topic tag or problem title is not evidence; the code is.
   Evidence records only what the code actually exercised (`clean`/`struggled`). A mapped
   move the solve routed around is recorded as a discovered `alt_walk` on the PROBLEM
   (this carrier is escapable) — never as a verdict on the candidate. Style is enforced
   only in force mode, before the merge; historic `avoided` entries remain but no new
   ones are written.
4. **Node fission.** When a stumble reveals a hidden sub-move inside a node (2006 exposed
   `solve-pair-condition` hiding inside `derived-key-lookup`), split the node rather than
   widening it. The taxonomy is expected to grow at the frontier of whatever is being drilled.
5. **Curated taxonomy.** Extractors must map onto existing node ids; genuinely new moves go
   to a review queue, not straight into nodes.json.
