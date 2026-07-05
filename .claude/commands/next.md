Recommend my next leetcode problem using the technique graph in `graph/` (read `graph/README.md` for the rules if this is your first time in this repo this session).

Procedure:

1. Load `graph/evidence.json` and derive current node statuses (or run `make preflight <candidate>` per candidate — it's instant and deterministic). Identify the current training frontier: FRAGILE nodes needing consolidation, STALE nodes needing spaced re-solves, and the next MISSING node adjacent to SOLID ones.
2. Pick ONE problem obeying the one-new-move rule: at most one non-SOLID move in its walk, verified with `make preflight <problem>`. Never assign on vibes — if preflight says PREP FIRST, administer the prescribed micro-drills in chat first (drills live on each node in `graph/nodes.json`).
3. Prefer, in order: (a) consolidating a FRAGILE node via a fresh carrier problem, (b) a spaced re-solve of a STALE node's carrier, (c) one genuinely new move adjacent to SOLID prerequisites. Themed gentle progressions — each assignment gets ONE sentence connecting it to the previous problem's move. Repeats after a gap are deliberate (spacing effect), not remedial.
4. Present the assignment with title, link, and the connection sentence. NO solution hints beyond naming the training-target move. The user asks for hints separately if wanted.
5. After any micro-drill administered in chat, record it immediately: `PYTHONPATH=./utils .venv/bin/python3 utils/kg_drill <node-id> <clean|struggled> --note "..."`. A drill not recorded didn't happen.
6. After the user reports solving, verify by running their solve file, review the code against the intended move (evidence discipline: the code may reveal an `avoided` walk — say so), and confirm `make solved` ran the auto-ingest (or run `make kg-extract`).

Coaching style (from long-standing feedback): don't rush; one new move per rung; wait for the user to confirm understanding in their own words before assigning; name new concepts before drilling them (labels unlock concepts for this user); if a needed node is missing from the taxonomy, improvise a <5-minute micro-drill inline BEFORE assigning, then consider adding the node (fission) to `graph/nodes.json`.
