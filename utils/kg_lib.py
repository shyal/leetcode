# kg_lib — shared helpers for the technique graph (graph/*.json).
#
# Mastery is DERIVED here at query time from evidence dates, never stored:
#   SOLID   clean evidence within SOLID_WINDOW_DAYS, no more-recent struggle
#   STALE   clean evidence exists, but older than the window
#   FRAGILE most recent evidence is struggled/avoided, or struggles only
#   MISSING no evidence at all

import glob
import json
import os
import re
import subprocess
import time
from datetime import date, timedelta

# The system clock runs UTC but the operator lives in Manila (UTC+8);
# "today" everywhere in the toolchain means the Manila calendar day.
os.environ["TZ"] = "Asia/Manila"
time.tzset()

GRAPH_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "graph")
DRILLS_DIR = os.path.join(os.path.dirname(GRAPH_DIR), "drills")
SOLID_WINDOW_DAYS = 42

SITECUSTOMIZE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitecustomize.py")


def sitecustomize_names():
    """Names utils/sitecustomize.py injects into builtins, read from the source
    of truth so this list can never drift from what actually runs."""
    try:
        with open(SITECUSTOMIZE) as f:
            src = f.read()
    except OSError:
        return []
    return sorted(set(re.findall(r"^builtins\.(\w+)\s*=", src, flags=re.M)))


# For any model prompt that judges solve code: the repo's utils/sitecustomize.py
# mirrors LeetCode's judge, which preloads names (functools.reduce, collections,
# typing names, heapq, TreeNode/ListNode/Node, draw_* helpers, ...) into builtins
# before user code runs. Bare use of these names is valid in both environments —
# and it is CLASSES like Node, not just imports, that judges wrongly call
# "undefined", so the note has to cover any undefined name, not only imports.
def _harness_env_note():
    names = sitecustomize_names()
    listed = f" The injected names are: {', '.join(names)}." if names else ""
    return (
        "Environment: this code runs under a harness that (like LeetCode's judge) "
        "preloads a large set of names into builtins — typing names, collections, "
        "itertools/functools, heapq, math, AND classes and helper functions such as "
        "TreeNode, ListNode, GraphNode, Node, build_tree, draw_tree, tabulate."
        + listed
        + " Using ANY of these without an import or a local definition is VALID and "
        "NEVER a bug. More generally: if a name looks undefined, assume it comes from "
        "the harness rather than concluding the code is broken. NEVER report a missing "
        "import, an undefined name, or an undefined class in a verdict or note."
    )


HARNESS_ENV_NOTE = _harness_env_note()

SOLID, STALE, FRAGILE, MISSING = "SOLID", "STALE", "FRAGILE", "MISSING"

# How much outside help a solve had, recorded per evidence entry alongside the
# verdict. A verdict says whether the code worked; assist says how much of it
# was the candidate's own recall. They are independent: clean-but-walked-through
# is a real solve that is NOT a real rep, so it earns evidence but shrinks the
# fitted half-life instead of extending it.
#   none        unaided
#   hint        a nudge (a question, a pointer to the branch that was wrong)
#   walkthrough the shape was talked through before the code existed
#   spoiled     saw the solution — no recall happened; `make sleep` re-queues it
ASSIST_LEVELS = ("none", "hint", "walkthrough", "spoiled")
ASSIST_WEIGHT = {"none": 0.0, "hint": 0.5, "walkthrough": 1.0, "spoiled": 2.0}


def assist_of(rec):
    """The assist level on an evidence record; absent field means unaided."""
    a = rec.get("assist", "none")
    return a if a in ASSIST_WEIGHT else "none"


def _load(name):
    with open(os.path.join(GRAPH_DIR, name)) as f:
        return json.load(f)


def load_nodes():
    return {n["id"]: n for n in _load("nodes.json")["nodes"]}


def load_problems():
    return _load("problems.json")["problems"]


def load_evidence():
    return _load("evidence.json")["evidence"]


def load_predicted():
    """graph/predicted.json (LLM-drafted walks); {} before it exists."""
    try:
        return _load("predicted.json")["problems"]
    except OSError:
        return {}


def unlocks(statuses, problems, predicted=None):
    """node -> how many unsolved bank problems are blocked ONLY by it.

    A problem counts for node n when it is not already solved (a key in
    problems.json means a walk was evidenced), no drafted walk of it is fully
    solid yet, and some walk needs nothing but n: every other move SOLID and
    no missing: suggestion. This is the reachability payoff of servicing n,
    counted against the whole drafted catalog (PLAN.md phase 1)."""
    if predicted is None:
        predicted = load_predicted()
    counts = {}
    for num, prob in predicted.items():
        if num in problems:
            continue
        walks = [w["moves"] for w in prob["walks"]
                 if w["moves"] and not w.get("missing")]
        if not walks:
            continue
        solid = {m for w in walks for m in w
                 if statuses.get(m, (None,))[0] == SOLID}
        if any(all(m in solid for m in w) for w in walks):
            continue
        blockers = set()
        for w in walks:
            gaps = [m for m in w if m not in solid]
            if len(gaps) == 1:
                blockers.add(gaps[0])
        for b in blockers:
            counts[b] = counts.get(b, 0) + 1
    return counts


def save_problems(problems):
    path = os.path.join(GRAPH_DIR, "problems.json")
    with open(path) as f:
        data = json.load(f)
    data["problems"] = problems
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def save_evidence(evidence):
    path = os.path.join(GRAPH_DIR, "evidence.json")
    with open(path) as f:
        data = json.load(f)
    data["evidence"] = evidence
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


_curve_cache = None


def _load_curve():
    """graph/curve.json (fitted by utils/kg_curve), or None for the flat window."""
    global _curve_cache
    if _curve_cache is None:
        path = os.path.join(GRAPH_DIR, "curve.json")
        _curve_cache = json.load(open(path)) if os.path.exists(path) else False
    return _curve_cache or None


def node_status(node_id, evidence, today=None):
    """Derive a node's mastery status from evidence entries.

    SOLID vs STALE uses the personal forgetting curve (graph/curve.json) when
    one has been fitted: predicted recall 2^(-gap/h) with a half-life that
    grows with clean reps and shrinks with struggles and assistance, SOLID
    while predicted recall >= the fitted target. Without a curve: flat
    SOLID_WINDOW_DAYS.

    A spoiled solve is not recall evidence at all — it neither counts as a
    clean rep nor keeps the node SOLID.
    """
    today = today or date.today()
    entries = []  # (date, verdict, assist)
    for rec in evidence.values():
        verdict = rec.get("moves", {}).get(node_id)
        if verdict:
            entries.append((date.fromisoformat(rec["date"]), verdict, assist_of(rec)))
    if not entries:
        return MISSING, None
    entries.sort()
    last_date, last_verdict, _ = entries[-1]
    clean_dates = [d for d, v, a in entries if v == "clean" and a != "spoiled"]
    if last_verdict in ("struggled", "avoided") and not (
        clean_dates and clean_dates[-1] >= last_date
    ):
        return FRAGILE, last_date
    if not clean_dates:
        return FRAGILE, last_date

    curve = _load_curve()
    if curve:
        import math
        p = curve["params"]
        cleans = len(clean_dates)
        struggles = sum(1 for _, v, _ in entries if v == "struggled")
        assisted = sum(ASSIST_WEIGHT[a] for _, _, a in entries)
        stability = math.exp(p["a"] + p["b"] * cleans - p["c"] * struggles
                             - p.get("d", 0.0) * assisted)
        stability = min(max(stability, 7), 3650)  # sanity clamp
        gap = (today - clean_dates[-1]).days
        if (1 + gap / stability) ** (-p["beta"]) >= curve["target_retention"]:
            return SOLID, clean_dates[-1]
        return STALE, clean_dates[-1]

    if today - clean_dates[-1] <= timedelta(days=SOLID_WINDOW_DAYS):
        return SOLID, clean_dates[-1]
    return STALE, clean_dates[-1]


DEEP_STALE_DAYS = 2 * SOLID_WINDOW_DAYS  # beyond this, a "re-solve" plays like a new problem

# A SOLID badge earned in one burst of drills is not yet load-bearing: six
# clean reps crammed into two days look identical to a node held for months,
# and nothing in node_status measures spacing or what kind of evidence it was.
MATURE_SPACING_DAYS = 5


MATURE_CARRY_MEDIUMS = 2


def carry_bar(node_id, problems):
    """The carry-proof bar the bank can actually hold this node to.

    ("medium", MATURE_CARRY_MEDIUMS)  a non-banned Medium carries the move in
                                      some walk: proof means clean reps at
                                      Medium+ altitude — easy cleans are
                                      dilution, not proof (a share would
                                      punish warmups; a count is monotone)
    ("real", 1)                       only easies carry it (micro-moves that
                                      genuinely live inside easies): one clean
                                      on any real problem suffices
    ("none", 0)                       no real problem carries it at all:
                                      spacing alone decides — a gate nobody
                                      can open is a deadlock, not a standard"""
    kinds = set()
    for pnum, p in problems.items():
        if not str(pnum)[:1].isdigit() or p.get("banned") \
                or p.get("difficulty") == "Hard":
            continue
        if node_id in p.get("moves", []) \
                or any(node_id in w for w in p.get("alt_walks", [])):
            kinds.add(p.get("difficulty"))
    if "Medium" in kinds:
        return "medium", MATURE_CARRY_MEDIUMS
    if kinds:
        return "real", 1
    return "none", 0


def mature(node_id, evidence, problems):
    """True when a node's mastery is proven enough to carry a Hard.

    Two signals, both required:
      spacing      clean (non-spoiled) reps on two days at least
                   MATURE_SPACING_DAYS apart — the badge survived a gap,
                   not just a same-week burst
      carry proof  clean reps on real leetcode problems (numeric id; drills
                   record problem="drill") at the altitude the bank can hold
                   the node to — see carry_bar(). Drill green is not trigger
                   wired, and for a node with medium carriers, easy green is
                   not altitude proof either.

    Gates SUMMITS ONLY. Easies/mediums are the proving ground where a young
    node earns both signals, so gating them would block the very reps that
    mature it. Callers fold immature nodes into route_gaps: an immature move
    is a camp on the route, not a servable summit."""
    clean = [(date.fromisoformat(rec["date"]), str(rec.get("problem", "")))
             for rec in evidence.values()
             if rec.get("moves", {}).get(node_id) == "clean"
             and assist_of(rec) != "spoiled"]
    if not clean:
        return False
    dates = sorted(d for d, _ in clean)
    if (dates[-1] - dates[0]).days < MATURE_SPACING_DAYS:
        return False
    kind, need = carry_bar(node_id, problems)
    if kind == "medium":
        return sum(1 for _, p in clean if p[:1].isdigit()
                   and problem_difficulty(p, problems) in ("Medium", "Hard")
                   ) >= need
    if kind == "real":
        return any(p[:1].isdigit() for _, p in clean)
    return True


def immature_nodes(nodes, evidence, problems):
    """The nodes mature() rejects — precomputed once per run so route_gaps
    and rank_summits stay pure sort keys."""
    return frozenset(n for n in nodes if not mature(n, evidence, problems))


def proving_carriers(target, problems, statuses, nodes):
    """Carriers that can give an immature move its carry proof: non-banned,
    non-Hard, real (numeric) problems carrying the target in ANY recorded
    walk whose every OTHER move is SOLID. Wider than carriers_for — primary
    carriers for a young move are often the very Hards it gates, so the
    proving camp lives on an alt walk (solve the medium VIA the young move;
    kg_extract records the walk actually taken). Held to the node's own
    carry bar: for a medium-bar node only Mediums count — an easy rep would
    be a camp that moves the route no closer to the summit."""
    kind, _ = carry_bar(target, problems)
    found = []
    for pnum, p in problems.items():
        if not str(pnum)[:1].isdigit() or p.get("banned") \
                or p.get("difficulty") == "Hard":
            continue
        if kind == "medium" and p.get("difficulty") != "Medium":
            continue
        walks = [p.get("moves", [])] + list(p.get("alt_walks", []))
        for walk in walks:
            if target in walk and all(m in nodes for m in walk) \
                    and all(statuses[m][0] == SOLID for m in walk if m != target):
                found.append(pnum)
                break
    return found


def last_solved(pnum, evidence):
    dates = [r["date"] for r in evidence.values() if r.get("problem") == str(pnum)]
    return max(dates) if dates else ""


def pnum_key(pnum):
    """Numeric sort that tolerates non-leetcode ids like '2167B'."""
    digits = "".join(c for c in str(pnum) if c.isdigit())
    return (int(digits) if digits else 0, str(pnum))


def dodged_nodes(evidence):
    """Nodes whose most recent evidence is 'avoided' — the canonical move was
    routed around. These get anti-dodge treatment: carriers chosen to resist
    the escape, drills prescribed first (a drill cannot be dodged)."""
    latest = {}
    for fname, rec in evidence.items():
        for node, verdict in rec.get("moves", {}).items():
            key = (rec["date"], fname)
            if node not in latest or key > latest[node][0]:
                latest[node] = (key, verdict, rec.get("problem"))
    return {n: pnum for n, (_, v, pnum) in latest.items() if v == "avoided"}


def dodgeable(pnum, target, problems):
    """True if a recorded alt walk lets this problem be solved without target."""
    return any(target not in walk
               for walk in problems.get(pnum, {}).get("alt_walks", []))


def carriers_for(target, problems, statuses, nodes):
    """Problems containing the target move whose every OTHER move is SOLID.
    Banned problems ("banned": true) are never offered as carriers.
    Hards are summits, never refresh carriers — rusty moves get their reps
    at basecamps (easies/mediums); a Hard is attempted only all-green."""
    found = []
    for pnum, p in problems.items():
        moves = p.get("moves", [])
        if p.get("banned") or p.get("difficulty") == "Hard" or target not in moves \
                or not all(m in nodes for m in moves):
            continue
        if all(statuses[m][0] == SOLID for m in moves if m != target):
            found.append(pnum)
    return found


# Interview-classic Hards worth summiting: number -> why it's valuable.
# Filtered against data/problems_metadata.json difficulty at runtime, so a
# mislabeled entry silently drops out rather than lying. Lives here rather
# than in kg_hard because `make next` serves summits too, and the two must
# never name different problems.
CLASSICS = {
    "4": "binary-search partitioning at its purest",
    "23": "the canonical heap hard — k-way merge",
    "25": "pointer surgery mastery — reverse in k-groups",
    "32": "stack meets DP on parentheses",
    "41": "in-place index cycling, O(1) space",
    "42": "the most famous hard — prefix-max / two-pointer",
    "76": "sliding window with need/have counters",
    "84": "monotonic stack at full power",
    "85": "84 lifted into 2-D",
    "124": "global-vs-path tree DP",
    "127": "implicit-graph BFS",
    "212": "trie + backtracking",
    "224": "expression parsing with a stack",
    "239": "monotonic deque",
    "295": "two-heap running median",
    "297": "tree serialization round-trip",
    "460": "layered data-structure design (LFU)",
    "502": "greedy + heap",
    "815": "BFS where routes are the nodes",
    "895": "stacked frequency stacks",
    "968": "greedy tree DP",
    "1235": "sort + binary search + DP",
    "2402": "two-heap simulation",
}


def route_gaps(pnum, problems, nodes, statuses, immature=frozenset()):
    """Non-SOLID — or SOLID-but-immature — nodes in the problem's input tree,
    and how many of them are consolidation (moves you once had) vs new ground.
    Unmapped proposals count as gaps too: they are unroutable new territory,
    so a walk carrying them is farther away than its mapped moves suggest."""
    closure = input_tree(problems[pnum]["moves"], nodes)
    gaps = [n for n in closure if statuses[n][0] != SOLID or n in immature]
    gap_count = len(gaps) + len(problems[pnum].get("unmapped", []))
    consolidation = sum(1 for n in gaps if statuses[n][0] != MISSING)
    return gaps, gap_count, consolidation


def rank_summits(candidates, problems, nodes, statuses, immature=frozenset()):
    """Candidate Hards ordered by reachability: fewest gaps first, then the
    one whose gaps are mostly consolidation (moves you once had) rather than
    new ground. The single ordering `make hard` and `make next` share, so a
    summit cannot be named differently depending on which one you ran."""
    scored = [(route_gaps(p, problems, nodes, statuses, immature)[1:], pnum_key(p), p)
              for p in candidates if p in problems]
    scored.sort(key=lambda s: (s[0][0], -s[0][1], s[1]))
    return [p for _, _, p in scored]


def input_tree(moves, nodes):
    """Transitive prerequisite closure of a walk (unknown ids skipped)."""
    seen = set()
    stack = list(moves)
    while stack:
        n = stack.pop()
        if n in seen or n not in nodes:
            continue
        seen.add(n)
        stack.extend(nodes[n].get("prereqs", []))
    return seen


def tree_size(pnum, problems, nodes):
    """Carrier gentleness for sort keys: (input-tree size, walk length).
    After freshness, the picker proposes the smallest composition that still
    exercises the target — fewest concepts in the room, not just fewest moves."""
    moves = problems[pnum]["moves"]
    return (len(input_tree(moves, nodes)), len(moves))


_METADATA = None


def _metadata():
    global _METADATA
    if _METADATA is None:
        path = os.path.join(os.path.dirname(GRAPH_DIR), "data/problems_metadata.json")
        try:
            with open(path) as f:
                _METADATA = json.load(f)
        except Exception:
            _METADATA = {}
    return _METADATA


def acceptance(pnum):
    """Community acceptance rate in percent from data/problems_metadata.json
    (refreshed by metadata.get_problems_metadata). 50.0 = neutral when the
    problem is unknown or the metadata predates the acceptance field."""
    v = _metadata().get(str(pnum), {}).get("acceptance")
    return v if isinstance(v, (int, float)) else 50.0


def problem_difficulty(pnum, problems):
    """Difficulty of a real problem: problems.json first (the curated truth
    for mapped ones), metadata as fallback for evidence-only references."""
    return problems.get(str(pnum), {}).get("difficulty") \
        or _metadata().get(str(pnum), {}).get("difficulty", "")


DIFF_RANK = {"Easy": 0, "Medium": 1, "Hard": 2}


def gentleness(pnum, problems, nodes):
    """Gentler-first key for fresh-carrier sorts: difficulty tier, then
    input-tree size. Community friction (acceptance) is deliberately NOT
    part of this key — it is a noisy, popularity-skewed proxy, so callers
    append -acceptance(p) as their FINAL tiebreak, after freshness
    (last_solved), never before it."""
    tier = DIFF_RANK.get(problems.get(str(pnum), {}).get("difficulty"), 1)
    return (tier, tree_size(pnum, problems, nodes))


def drill_solved_stem(path):
    """The d_-filename stem `make solved` writes for this drill file: its
    DRILL title cleaned exactly the way utils/solved cleans it. Falls back
    to the bank filename slug if the header is missing."""
    try:
        with open(path) as f:
            m = re.search(r"^\s*DRILL:\s*(.+)$", f.read(), flags=re.M)
    except OSError:
        m = None
    title = m.group(1).strip() if m else os.path.splitext(os.path.basename(path))[0]
    return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")


def last_drilled(path, evidence):
    """Latest date this bank drill file was solved. Matched on the DRILL
    title (what d_ solved filenames are built from), not the bank filename —
    the two rarely coincide."""
    key = f"d_{drill_solved_stem(path)}_".lower()
    dates = [r["date"] for k, r in evidence.items()
             if os.path.basename(k).lower().startswith(key)]
    return max(dates) if dates else ""


def has_drill_bank(node_id):
    """True when drills/<node-id>/ holds at least one bank file."""
    return bool(glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py")))


def drill_gated(node_id, status, last, today=None):
    """The drill-success gate: a MISSING/FRAGILE — or deep-stale — target
    with a drill bank trains on its drill ONLY; no carrier fires for it
    until a clean rep lifts the node out of the gated state. Mastery is
    derived, so the gate clears itself: a clean drill changes the status,
    a struggled one keeps the carrier held (drill-recency alone used to
    unlock it — that was the 227 hole). Ordinary STALE is ungated: its
    spaced re-solve IS the rep. Node-side on purpose: alt walks change
    which walk a solve evidences, never whether a cold move gets a carrier."""
    if status in (FRAGILE, MISSING):
        return has_drill_bank(node_id)
    if status == STALE and last:
        today = today or date.today()
        if (today - last).days > DEEP_STALE_DAYS:
            return has_drill_bank(node_id)
    return False


def due_drill(node_id, evidence, today=None):
    """Least-recently-drilled bank file for a node, or None if the bank is
    empty or that file was already drilled today. The no-carrier fallback:
    a gap node with no READY carrier gets its drill offered instead of being
    silently skipped — a drill cannot be dodged and needs no carrier."""
    today = (today or date.today()).isoformat()
    candidates = sorted(glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py")))
    if not candidates:
        return None
    path = min(candidates, key=lambda p: last_drilled(p, evidence))
    return None if last_drilled(path, evidence) >= today else path


def latest_carrier(node_id, evidence):
    """Most recent evidence file that exercised this node (for spaced re-solves)."""
    best = None
    for fname, rec in evidence.items():
        if node_id in rec.get("moves", {}):
            d = date.fromisoformat(rec["date"])
            if best is None or d > best[0]:
                best = (d, fname, rec.get("problem"))
    return best


def load_sleep():
    """graph/sleep.json — problems parked by `make sleep`. Returns {} if absent."""
    path = os.path.join(GRAPH_DIR, "sleep.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f).get("sleeps", {})


def save_sleep(sleeps):
    path = os.path.join(GRAPH_DIR, "sleep.json")
    data = {
        "_comment": "Problems parked mid-exercise by `make sleep`: excluded from kg_next "
        "picks until `until`, their walk's rusty dependencies warmed meanwhile; on expiry "
        "the problem jumps the queue for a fresh attempt. An entry is resolved (and later "
        "pruned) once a solve is recorded on or after its slept date.",
        "sleeps": sleeps,
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def sleep_state(sleeps, evidence, now=None):
    """Split sleep entries into (asleep, woken) problem-number lists.

    Resolved entries — a solve recorded on/after the slept date — fall in neither.
    """
    from datetime import datetime

    now = now or datetime.now()
    asleep, woken = [], []
    for pnum, rec in sleeps.items():
        slept_day = rec["slept"][:10]
        if any(r.get("problem") == pnum and r["date"] >= slept_day for r in evidence.values()):
            continue
        (asleep if now < datetime.fromisoformat(rec["until"]) else woken).append(pnum)
    return asleep, woken


def claude_json(prompt, system_prompt, model="sonnet"):
    """One non-interactive claude call; returns parsed JSON from the result text."""
    proc = subprocess.run(
        [
            "claude", "-p", prompt,
            "--system-prompt", system_prompt,
            "--model", model,
            "--output-format", "json",
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr[:500]}")
    result = json.loads(proc.stdout).get("result", "")
    # tolerate fences/preamble/trailing junk (haiku sometimes emits the object
    # twice): parse the FIRST valid {...} and ignore whatever follows
    text = result.strip()
    start = text.find("{")
    if start == -1:
        raise ValueError(f"no JSON object in result: {text[:200]!r}")
    obj, _ = json.JSONDecoder().raw_decode(text[start:])
    return obj


def taxonomy_summary(nodes):
    """Compact node list for prompts: id — desc."""
    return "\n".join(f"- {nid}: {n['desc']}" for nid, n in nodes.items())


# ---- cold-mock pass-rate model ----------------------------------------------
# The Monte-Carlo model behind `make mock` (implemented in Rust under
# utils/kg_mock_rs) and the README's P(pass) history chart. The Rust port keeps
# this exact math (same RNG stream, same float-op order); change them together.

REC_POWER = {"E": 0.5, "M": 1.0, "H": 1.6}
SCENARIOS = {"cautious": 0.75, "central": 0.85, "optimistic": 0.95}


def recognition(base, mocks_done):
    import math
    return base + (0.98 - base) * (1 - math.exp(-mocks_done / 8))


def pass_rates(node_recall, pools, r_base, practice, rng, n_mc=20000):
    """(full clear, onsite 2E+2M+>=1H, screen both-M, single-hard P).

    pools: {"E"/"M"/"H": [problem, ...]}, each problem a list of walks, each
    walk a list of move names — real problems (evidenced + drafted walks, the
    Rust Bank), not fabricated ones. A problem is drawn uniformly from its
    difficulty pool and scored by its BEST walk's recall product; a move
    without recall (off-taxonomy) costs the derive rate. Same draw order as
    the Rust port (randrange then random), so the RNG streams match."""
    import math
    mediums, mocks, hards = practice
    grow = 1 - math.exp(-mediums / 120)
    time_f = {"E": 0.88 + 0.07 * grow, "M": 0.87 + 0.07 * grow,
              "H": 0.40 + 0.42 * (1 - math.exp(-hards / 15))}
    derive = 0.25 + 0.20 * (1 - math.exp(-(mocks + hards) / 30))
    rec = recognition(r_base, mocks)
    full = onsite = screen = h_solved = 0
    for _ in range(n_mc):
        solved = {"E": 0, "M": 0, "H": 0}
        for dif in ("E", "E", "M", "M", "H", "H"):
            prob = pools[dif][rng.randrange(len(pools[dif]))]
            best = max(
                math.prod(node_recall.get(mv, derive) for mv in walk)
                for walk in prob
            )
            p = time_f[dif] * rec ** REC_POWER[dif] * best
            solved[dif] += rng.random() < p
        full += solved["E"] == 2 and solved["M"] == 2 and solved["H"] == 2
        onsite += solved["E"] == 2 and solved["M"] == 2 and solved["H"] >= 1
        screen += solved["M"] == 2
        h_solved += solved["H"]
    return full / n_mc, onsite / n_mc, screen / n_mc, h_solved / (2 * n_mc)


def current_recall(nodes, evidence, curve, today=None):
    """Predicted recall per node. Pass `today` (and evidence filtered to
    entries on or before it) to replay a historical snapshot."""
    import math
    today = today or date.today()
    p = curve["params"]
    out = {}
    for nid in nodes:
        status, last = node_status(nid, evidence, today=today)
        cleans = sum(1 for r in evidence.values()
                     if r.get("moves", {}).get(nid) == "clean")
        if status == MISSING or not last:
            out[nid] = 0.25
            continue
        s = min(max(math.exp(p["a"] + p["b"] * cleans), 7), 3650)
        rec = (1 + (today - last).days / s) ** (-p["beta"])
        out[nid] = rec * 0.5 if status == FRAGILE else rec
    return out


# --- the replay clock (utils/kg_movie_rs) ----------------------------------
# Python mirror of kg_movie's pacing, bit-for-bit: ticks run from the day
# before the first evidence entry to the last one, each day's screen time is
# its unique leetcode solve count + LULL_WEIGHT (long solve-less stretches
# fast-forward), and the loop closes with a dissolve. Every animated SVG that
# wants to play in sync with kg_movie.svg / kg_pass.svg builds its keyTimes
# from this. Change the pacing here and in kg_movie_rs/src/main.rs together.

MOVIE_SECONDS = 10.0        # kg_movie's DEFAULT_SECONDS
MOVIE_END_FADE_S = 1.2      # loop-closing dissolve, capped by the fraction
MOVIE_FADE_FRACTION = 0.08
MOVIE_LULL_WEIGHT = 0.25    # screen time a solve-less day gets, in solves


class MovieClock:
    def __init__(self, evidence, seconds=MOVIE_SECONDS):
        from collections import defaultdict

        all_dates = sorted(rec["date"] for rec in evidence.values())
        self.first = date.fromisoformat(all_dates[0]) - timedelta(days=1)
        self.last = date.fromisoformat(all_dates[-1])
        self.n_ticks = (self.last - self.first).days + 1
        self.dur = seconds
        self.fade_s = min(MOVIE_END_FADE_S, seconds * MOVIE_FADE_FRACTION)
        self.ticks_end = (seconds - self.fade_s) / seconds

        # kg_movie's solves_by_day: unique leetcode-numbered problems per day
        by_day = defaultdict(set)
        for rec in evidence.values():
            p = rec.get("problem", "")
            if p[:1].isdigit():
                by_day[rec["date"]].add(p)
        self.weights = [
            len(by_day[(self.first + timedelta(days=i)).isoformat()]) + MOVIE_LULL_WEIGHT
            for i in range(self.n_ticks)
        ]
        self.total_w = sum(self.weights)
        self.cum = [0.0]
        for w in self.weights:
            self.cum.append(self.cum[-1] + w)  # cum[i] = tick i's start

    def frac(self, day_offset):
        """Loop fraction of a day offset from `first`; fractional offsets
        interpolate within the day's own tick length."""
        i = min(int(day_offset), self.n_ticks - 1)
        c = self.cum[i] + self.weights[i] * (day_offset - i)
        return min(c / self.total_w, 1.0) * self.ticks_end

    def frac_date(self, d):
        return self.frac((d - self.first).days)

    def dissolve_rect(self, w, h, fill):
        """The loop-closing cover fade, identical to kg_movie's."""
        return (f'<rect width="{w}" height="{h}" fill="{fill}" opacity="0" pointer-events="none">'
                f'<animate attributeName="opacity" calcMode="linear" values="0;0;1" '
                f'keyTimes="0;{self.ticks_end:.4f};1" dur="{self.dur}s" repeatCount="indefinite"/></rect>')


# era banner shared by the animated SVGs: the one flip that is the point of
# all of them. Mirrors kg_movie_rs's ERA_SWITCH / labels / inks.
ERA_SWITCH = date(2026, 8, 7)
ERA_PRE_LABEL = "pre graph scheduling era"
ERA_GRAPH_LABEL = "graph scheduling era"
ERA_PRE_INK = "#8b949e"
ERA_GRAPH_INK = "#58a6ff"


def era_banner(clock, x, y, size, anchor="start", halo=None):
    """Two <text> layers flipping grey -> blue on the switch date's tick;
    non-SMIL viewers see today's era. halo outlines the text in a background
    color for banners placed over chart ink."""
    halo_attr = (f' stroke="{halo}" stroke-width="{max(size // 7, 3)}" '
                 f'paint-order="stroke" stroke-linejoin="round"') if halo else ""
    common = f'y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="bold"'
    if not (clock.first < ERA_SWITCH <= clock.last):
        label, ink = ((ERA_PRE_LABEL, ERA_PRE_INK) if clock.last < ERA_SWITCH
                      else (ERA_GRAPH_LABEL, ERA_GRAPH_INK))
        return [f'<text x="{x}" {common} fill="{ink}"{halo_attr}>{label}</text>']
    f = clock.frac((ERA_SWITCH - clock.first).days)
    out = []
    for label, ink, vals, init in ((ERA_PRE_LABEL, ERA_PRE_INK, "1;0", 0),
                                   (ERA_GRAPH_LABEL, ERA_GRAPH_INK, "0;1", 1)):
        out.append(f'<text x="{x}" {common} fill="{ink}"{halo_attr} opacity="{init}">{label}'
                   f'<animate attributeName="opacity" calcMode="discrete" values="{vals}" '
                   f'keyTimes="0;{f:.4f}" dur="{clock.dur}s" repeatCount="indefinite"/></text>')
    return out
