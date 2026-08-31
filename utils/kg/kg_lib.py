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
import sys
import time
from datetime import date, datetime, timedelta, timezone

# The system clock runs UTC but the operator lives in Manila (UTC+8);
# "today" everywhere in the toolchain means the Manila calendar day.
os.environ["TZ"] = "Asia/Manila"
time.tzset()

MANILA = timezone(timedelta(hours=8))

# solved/ filenames are stamped in UTC (utils/kg/solved) — same clock as git.
# The Manila day starts at 16:00 UTC, so for any solve between 16:00 and
# 24:00 UTC (midnight to 8am Manila, the usual session hours) the raw Y_M_D
# in the filename is one day behind "today". Anything deriving a calendar
# day from a filename must go through manila_date_from_filename, never
# read the date digits straight out of the name.
FNAME_TS_RE = re.compile(r"_(\d{4})_(\d{2})_(\d{2})T(\d{2})_(\d{2})_(\d{2})")


def manila_date_from_filename(name):
    """Manila calendar day (iso string) of the UTC timestamp embedded in a
    solved/ filename, or None when the name carries no timestamp."""
    m = FNAME_TS_RE.search(os.path.basename(name))
    if not m:
        return None
    y, mo, d, h, mi, s = map(int, m.groups())
    return datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc).astimezone(MANILA).date().isoformat()

UTILS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(UTILS_DIR)
GRAPH_DIR = os.path.join(REPO_ROOT, "graph")
DRILLS_DIR = os.path.join(os.path.dirname(GRAPH_DIR), "drills")
SOLID_WINDOW_DAYS = 42

SITECUSTOMIZE = os.path.join(UTILS_DIR, "harness", "sitecustomize.py")


def sitecustomize_names():
    """Names utils/harness/sitecustomize.py injects into builtins, read from the source
    of truth so this list can never drift from what actually runs."""
    try:
        with open(SITECUSTOMIZE) as f:
            src = f.read()
    except OSError:
        return []
    return sorted(set(re.findall(r"^builtins\.(\w+)\s*=", src, flags=re.M)))


# For any model prompt that judges solve code: the repo's utils/harness/sitecustomize.py
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


def assist_of(rec, node_id=None):
    """The assist level on an evidence record; absent field means unaided.

    Two shapes. A bare string ("hint") is the pre-2026-08-31 form and taints
    every move in the walk. A dict {move: level} names the moves the help
    actually touched; the others are unaided. With `node_id`, the answer is
    for that one move. Without it, the answer is for the solve as a whole:
    the heaviest level on it (one hint anywhere makes the solve a hinted
    solve - the bar last_clean_solve and drill_warm hold releases to).

    The 1004 case (2026-08-17): a hint on the sliding-window bookkeeping
    was stamped on prefix-sums and running-extreme too, and `owned` then
    held every drill behind prefix-sums for an unaided rep of a move that
    had three unaided reps the week before."""
    a = rec.get("assist", "none")
    if isinstance(a, dict):
        levels = [v for v in a.values() if v in ASSIST_WEIGHT]
        if node_id is not None:
            v = a.get(node_id, "none")
            return v if v in ASSIST_WEIGHT else "none"
        return max(levels, key=ASSIST_WEIGHT.__getitem__) if levels else "none"
    return a if a in ASSIST_WEIGHT else "none"


def normalise_assist(raw, moves):
    """The stored shape of an extractor's "assist" answer: {move: level} for
    the moves that were helped, restricted to the walk's moves, or None when
    nothing was. A bare string is spread over every move in the walk (the
    extractor could not say where the help landed, so it landed everywhere -
    the old semantics, now explicit)."""
    if isinstance(raw, str):
        raw = {m: raw for m in moves} if raw in ASSIST_WEIGHT and raw != "none" else {}
    if not isinstance(raw, dict):
        return None
    out = {m: v for m, v in raw.items()
           if m in moves and v in ASSIST_WEIGHT and v != "none"}
    return out or None


def assist_tag(assist):
    """One-line rendering of either assist shape for receipts."""
    if isinstance(assist, dict):
        return ", ".join(f"{m}={v}" for m, v in sorted(assist.items()))
    return str(assist)


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


def unlocks(statuses, problems, predicted=None, immature=frozenset()):
    """node -> how many unsolved bank problems are blocked ONLY by it.

    A problem counts for node n when it is not already solved (a key in
    problems.json means a walk was evidenced), no drafted walk of it is fully
    solid yet, and some walk needs nothing but n: every other move SOLID and
    no missing: suggestion. This is the reachability payoff of servicing n,
    counted against the whole drafted catalog (PLAN.md phase 1). With
    `immature`, a young node is a gap too (mature(): SOLID but not yet
    proven on a real problem at its bar), so the count is the payoff of
    proving n - the reach rule in kg_next. A move the taxonomy has no node
    for is a gap nothing here can close."""
    import numpy as np
    if predicted is None:
        predicted = load_predicted()
    dm = _draft_matrix(predicted, sorted(statuses))
    reach = np.array([statuses[n][0] == SOLID and n not in immature
                      for n in dm.node_ids], dtype=bool)
    gaps = (dm.W & ~reach).sum(1) + dm.unknown
    live = dm.live_problems(problems)
    in_reach = np.zeros(len(dm.problems), dtype=bool)
    np.logical_or.at(in_reach, dm.prob[~dm.missing & (gaps == 0)], True)
    sel = ~dm.missing & (gaps == 1) & (dm.unknown == 0) \
        & live[dm.prob] & ~in_reach[dm.prob]
    if not sel.any():
        return {}
    blocker = (dm.W[sel] & ~reach).argmax(1)
    pairs = np.unique(np.stack([dm.prob[sel], blocker], 1), axis=0)
    counts = np.bincount(pairs[:, 1], minlength=len(dm.node_ids))
    return {dm.node_ids[i]: int(c) for i, c in enumerate(counts) if c}


class _DraftMatrix:
    """graph/predicted.json as arrays, built once per (predicted, node set):
    W[walk, node] says the walk uses the node; prob[walk] its problem's
    row; missing/unknown flag walks the taxonomy cannot express (a missing:
    suggestion, or a move with no node). Per problem: difficulty rank,
    acceptance, numeric key - the static parts of drafted_in_reach's
    ranking. The picker asks about the catalog several times per pick and
    a simulated day asks hundreds of times; walking 3087 dicts each time
    was most of the cost (2026-08-31)."""

    def __init__(self, predicted, node_ids):
        import numpy as np
        self.node_ids = list(node_ids)
        self.index = index = {n: i for i, n in enumerate(self.node_ids)}
        self.problems, rows, prob, missing, unknown = [], [], [], [], []
        self.walk_moves = []  # each walk's moves in file order
        meta = _metadata()
        for num, entry in predicted.items():
            pi = len(self.problems)
            self.problems.append(num)
            for w in entry.get("walks", []):
                moves = w.get("moves", [])
                if not moves:
                    continue
                row = np.zeros(len(index), dtype=bool)
                unk = 0
                for m in moves:
                    if m in index:
                        row[index[m]] = True
                    else:
                        unk += 1
                rows.append(row)
                self.walk_moves.append(list(moves))
                prob.append(pi)
                missing.append(bool(w.get("missing")))
                unknown.append(unk)
        self.W = np.array(rows, dtype=bool).reshape(len(rows), len(index))
        self.prob = np.array(prob, dtype=int)
        self.missing = np.array(missing, dtype=bool)
        self.unknown = np.array(unknown, dtype=int)
        self.diff = [meta.get(str(n), {}).get("difficulty", "") for n in self.problems]
        self.acc = np.array([acceptance(n) for n in self.problems], dtype=float)
        self.pkey = np.array([pnum_key(n)[0] for n in self.problems], dtype=int)
        self._live = (None, None)
        self._counts = (None, None)

    def live_problems(self, problems):
        """Boolean per problem: not in problems.json (unsolved, unmapped)."""
        import numpy as np
        key = (id(problems), len(problems))
        if self._live[0] != key:
            self._live = (key, np.array([n not in problems for n in self.problems],
                                        dtype=bool))
        return self._live[1]

    def carrier_counts(self, problems):
        """Per node: evidenced problems carrying it (predicted_carrier's
        rehearsal mass), as a vector over node_ids."""
        import numpy as np
        key = (id(problems), len(problems))
        if self._counts[0] != key:
            counts = {}
            for p in problems.values():
                for m in p.get("moves", []):
                    counts[m] = counts.get(m, 0) + 1
            self._counts = (key, np.array([counts.get(n, 0) for n in self.node_ids],
                                          dtype=float))
        return self._counts[1]


_DRAFT_MATRIX = {}


def _draft_matrix(predicted, node_ids):
    key = (id(predicted), tuple(sorted(node_ids)))
    dm = _DRAFT_MATRIX.get(key)
    if dm is None:
        if len(_DRAFT_MATRIX) > 8:
            _DRAFT_MATRIX.clear()
        dm = _DRAFT_MATRIX[key] = _DraftMatrix(predicted, sorted(node_ids))
    return dm


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
    """graph/curve.json (fitted by utils/kg/kg_curve), or None for the flat window."""
    global _curve_cache
    if _curve_cache is None:
        path = os.path.join(GRAPH_DIR, "curve.json")
        _curve_cache = json.load(open(path)) if os.path.exists(path) else False
    return _curve_cache or None


# --- the evidence index ---------------------------------------------------
# Every reader of evidence.json used to scan the whole dict per node or per
# problem: node_status alone was 94 scans per pick, and a simulated day of
# make next (kg_simulate) ran thousands of them. The index is built once per
# evidence dict and extended in place when records are appended to it (the
# simulation's case); any other change rebuilds it. Records are never
# copied - the same dicts, grouped.

class _EvidenceIndex:
    __slots__ = ("by_node", "by_problem", "by_date", "drills", "n", "last")

    def __init__(self):
        self.by_node = {}     # node -> [(date, verdict, assist, fname, rec)]
        self.by_problem = {}  # problem -> [(date str, fname, rec)]
        self.by_date = {}     # date str -> [(fname, rec)]
        self.drills = []      # [(date str, lowercase basename, rec)] of d_ files
        self.n = 0
        self.last = None

    def add(self, fname, rec):
        d = date.fromisoformat(rec["date"])
        for node, v in rec.get("moves", {}).items():
            self.by_node.setdefault(node, []).append(
                (d, v, assist_of(rec, node), fname, rec))
        pnum = rec.get("problem")
        if pnum is not None:
            self.by_problem.setdefault(str(pnum), []).append((rec["date"], fname, rec))
        self.by_date.setdefault(rec["date"], []).append((fname, rec))
        base = os.path.basename(fname).lower()
        if base.startswith("d_"):
            self.drills.append((rec["date"], base, rec))
        self.n += 1
        self.last = fname


_EV_INDEX = {}  # id(evidence) -> _EvidenceIndex


def ev_index(evidence):
    """The _EvidenceIndex of this evidence dict. Reused while the dict is
    the same object and has only grown at the end since the last call;
    rebuilt otherwise."""
    from itertools import islice
    idx = _EV_INDEX.get(id(evidence))
    n = len(evidence)
    if idx is not None and idx.n == n:
        return idx
    if idx is not None and idx.n <= n and (
            idx.n == 0 or next(islice(evidence, idx.n - 1, idx.n), None) == idx.last):
        for fname, rec in islice(evidence.items(), idx.n, None):
            idx.add(fname, rec)
        return idx
    idx = _EvidenceIndex()
    for fname, rec in evidence.items():
        idx.add(fname, rec)
    _EV_INDEX.clear()
    _EV_INDEX[id(evidence)] = idx
    return idx


def solved_problems(evidence):
    """The problem numbers with any evidence record ("drill" included)."""
    return set(ev_index(evidence).by_problem)


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
    status, last, _ = node_eval(node_id, evidence, today)
    return status, last


def node_recall(node_id, evidence, today=None):
    """Predicted recall probability in [0, 1] for a node today.

    The curve's full fitted model (1-slip)*(1 + gap/s)^(-beta) — node_status
    thresholds just the memory component into SOLID/STALE; this returns the
    probability itself so callers can multiply it across a walk. MISSING and
    FRAGILE nodes have no recall to predict (0.0). Without a fitted curve the
    flat window makes it binary."""
    return node_eval(node_id, evidence, today)[2]


def node_eval(node_id, evidence, today=None):
    """(status, last_relevant_date, predicted_recall) in one evidence scan —
    node_status and node_recall are views of this."""
    today = today or date.today()
    entries = [(d, v, a) for d, v, a, _, _ in
               ev_index(evidence).by_node.get(node_id, ())]  # (date, verdict, assist)
    if not entries:
        return MISSING, None, 0.0
    entries.sort()
    last_date, last_verdict, _ = entries[-1]
    clean_dates = [d for d, v, a in entries if v == "clean" and a != "spoiled"]
    if last_verdict in ("struggled", "avoided") and not (
        clean_dates and clean_dates[-1] >= last_date
    ):
        return FRAGILE, last_date, 0.0
    if not clean_dates:
        return FRAGILE, last_date, 0.0

    curve = _load_curve()
    if curve:
        import math
        p = curve["params"]
        cleans = len(clean_dates)
        struggles = sum(1 for _, v, _ in entries if v == "struggled")
        assisted = sum(ASSIST_WEIGHT[a] for _, _, a in entries)
        # connectivity covariate: widely carried moves hold on longer. The
        # node's log2 carrier count is frozen into curve.json at fit time;
        # unknown nodes get the mean (a centered zero effect).
        cmean = p.get("conn_mean", 0.0)
        cn = curve.get("conn", {}).get(node_id, cmean)
        stability = math.exp(p["a"] + p["b"] * cleans - p["c"] * struggles
                             - p.get("d", 0.0) * assisted
                             + p.get("e", 0.0) * (cn - cmean))
        stability = min(max(stability, 7), 3650)  # sanity clamp
        gap = max((today - clean_dates[-1]).days, 0)
        memory = (1 + gap / stability) ** (-p["beta"])
        recall = (1 - p.get("slip", 0.0)) * memory
        status = SOLID if memory >= curve["target_retention"] else STALE
        return status, clean_dates[-1], recall

    if today - clean_dates[-1] <= timedelta(days=SOLID_WINDOW_DAYS):
        return SOLID, clean_dates[-1], 1.0
    return STALE, clean_dates[-1], 0.0


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
    return _bar_of(_carry_kinds(problems).get(node_id, set()))


def _carry_kinds(problems):
    """node -> the difficulties of the non-banned, non-Hard real problems
    that carry it in any walk. One pass over the bank; carry_bar and
    immature_nodes both read it (immature_nodes used to rescan the bank
    once per node - half of every pick, the 2026-08-31 simulation)."""
    from itertools import islice
    memo = _CARRY_KINDS
    if memo.get("id") == id(problems) and memo["n"] <= len(problems):
        kinds, start = memo["kinds"], memo["n"]  # extend: the bank only grows
    else:
        kinds, start = {}, 0
    for pnum, p in islice(problems.items(), start, None):
        if not str(pnum)[:1].isdigit() or p.get("banned") \
                or p.get("difficulty") == "Hard":
            continue
        for w in [p.get("moves", [])] + list(p.get("alt_walks", [])):
            for m in w:
                kinds.setdefault(m, set()).add(p.get("difficulty"))
    memo.update(id=id(problems), n=len(problems), kinds=kinds)
    return kinds


_CARRY_KINDS = {}  # memo of the last bank seen: problems only ever grow


def _bar_of(kinds):
    if "Medium" in kinds:
        return "medium", MATURE_CARRY_MEDIUMS
    if kinds:
        return "real", 1
    return "none", 0


def _clean_reps(evidence):
    """node -> [(date, problem), ...] over its clean, non-spoiled reps."""
    return {nid: [(d, str(rec.get("problem", ""))) for d, v, a, _, rec in entries
                  if v == "clean" and a != "spoiled"]
            for nid, entries in ev_index(evidence).by_node.items()}


def _mature_from(clean, bar, problems):
    if not clean:
        return False
    dates = sorted(d for d, _ in clean)
    if (dates[-1] - dates[0]).days < MATURE_SPACING_DAYS:
        return False
    kind, need = bar
    if kind == "medium":
        return sum(1 for _, p in clean if p[:1].isdigit()
                   and problem_difficulty(p, problems) in ("Medium", "Hard")
                   ) >= need
    if kind == "real":
        return any(p[:1].isdigit() for _, p in clean)
    return True


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
    return _mature_from(_clean_reps(evidence).get(node_id, []),
                        carry_bar(node_id, problems), problems)


def immature_nodes(nodes, evidence, problems):
    """The nodes mature() rejects — precomputed once per run so route_gaps
    and rank_summits stay pure sort keys. One pass over the bank and one
    over the evidence, whatever the node count."""
    from itertools import islice
    key = (id(evidence), id(problems), tuple(nodes))
    idx = ev_index(evidence)
    kinds = _carry_kinds(problems)

    def young(n):
        clean = [(d, str(rec.get("problem", ""))) for d, v, a, _, rec in
                 idx.by_node.get(n, ()) if v == "clean" and a != "spoiled"]
        return not _mature_from(clean, _bar_of(kinds.get(n, set())), problems)

    memo = _IMMATURE
    if memo.get("key") == key and memo["n"] <= len(evidence) \
            and memo["n_pr"] <= len(problems):
        # records and problems appended since: only the nodes they touch
        # can have changed (a problem changes carry bars for its moves)
        touched = set()
        for _, rec in islice(evidence.items(), memo["n"], None):
            touched.update(rec.get("moves", {}))
        for p in islice(problems.values(), memo["n_pr"], None):
            touched.update(p.get("moves", []))
            for w in p.get("alt_walks", []):
                touched.update(w)
        out = set(memo["out"])
        for n in touched & memo["nodes"]:
            out.discard(n)
            if young(n):
                out.add(n)
        out = frozenset(out)
    else:
        out = frozenset(n for n in nodes if young(n))
    memo.update(key=key, n=len(evidence), n_pr=len(problems), out=out,
                nodes=set(nodes))
    return out


_IMMATURE = {}  # memo: maturity changes only with the evidence or the bank


def proving_carriers(target, problems, statuses, nodes, evidence):
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
    for pnum, walks in _walks_carrying(problems).get(target, ()):
        p = problems[pnum]
        if kind == "medium" and p.get("difficulty") != "Medium":
            continue
        if not any(all(m in nodes for m in walk)
                   and all(statuses[m][0] == SOLID for m in walk if m != target)
                   for walk in walks):
            continue
        if held_behind(pnum, problems, evidence):
            continue
        found.append(pnum)
    return found


_WALKS_CARRYING = {}


def _walks_carrying(problems):
    """node -> [(pnum, [walk, ...])] over the non-banned, non-Hard real
    problems whose recorded walks (primary or alt) use the node, in bank
    order. One pass over the bank, memoized while it is unchanged."""
    from itertools import islice
    memo = _WALKS_CARRYING
    if memo.get("id") == id(problems) and memo["n"] <= len(problems):
        out, start = memo["out"], memo["n"]  # extend: the bank only grows
    else:
        out, start = {}, 0
    for pnum, p in islice(problems.items(), start, None):
        if not str(pnum)[:1].isdigit() or p.get("banned") \
                or p.get("difficulty") == "Hard":
            continue
        walks = [p.get("moves", [])] + list(p.get("alt_walks", []))
        for node in {m for w in walks for m in w}:
            out.setdefault(node, []).append((pnum, walks))
    memo.update(id=id(problems), n=len(problems), out=out)
    return out


def last_solved(pnum, evidence):
    recs = ev_index(evidence).by_problem.get(str(pnum))
    return max(d for d, _, _ in recs) if recs else ""


def last_clean_solve(pnum, evidence):
    """Latest date this problem was solved with every walked move clean and
    no assist at all - the bar a predecessor must meet to release the
    problems declared "after" it. An assisted clean is a real rep, but the
    ladder advances on ownership: the unaided rep is what releases."""
    dates = [d for d, _, r in ev_index(evidence).by_problem.get(str(pnum), ())
             if r.get("moves")
             and all(v == "clean" for v in r["moves"].values())
             and assist_of(r) == "none"]
    return max(dates) if dates else ""


def held_behind(pnum, problems, evidence, today=None):
    """The predecessor problem this one must wait for, or None.

    A problem may declare "after": ["46"] - problems whose walk its own
    builds on (47 is 46's loop plus the dedup rule). While a predecessor is
    due - never solved clean, or its last clean solve has aged out of the
    solid window - this problem stays out of carrier pools so the picker
    serves the predecessor first. A banned predecessor holds nothing back.
    """
    today = today or date.today()
    for pred in problems.get(str(pnum), {}).get("after", []):
        pred = str(pred)
        if problems.get(pred, {}).get("banned"):
            continue
        last = last_clean_solve(pred, evidence)
        if not last or (today - date.fromisoformat(last)).days > SOLID_WINDOW_DAYS:
            return pred
    return None


def pnum_key(pnum):
    """Numeric sort that tolerates non-leetcode ids like '2167B'."""
    digits = "".join(c for c in str(pnum) if c.isdigit())
    return (int(digits) if digits else 0, str(pnum))


_DODGED = {}  # memo of the latest verdict per node, extended as evidence grows


def dodged_nodes(evidence):
    """Nodes whose most recent evidence is 'avoided' — the canonical move was
    routed around. These get anti-dodge treatment: carriers chosen to resist
    the escape, drills prescribed first (a drill cannot be dodged)."""
    from itertools import islice
    memo = _DODGED
    if memo.get("id") == id(evidence) and memo["n"] <= len(evidence):
        latest, start = memo["latest"], memo["n"]  # extend over the new records
    else:
        latest, start = {}, 0
    for fname, rec in islice(evidence.items(), start, None):
        for node, verdict in rec.get("moves", {}).items():
            key = (rec["date"], fname)
            if node not in latest or key > latest[node][0]:
                latest[node] = (key, verdict, rec.get("problem"))
    memo.update(id=id(evidence), n=len(evidence), latest=latest)
    return {n: pnum for n, (_, v, pnum) in latest.items() if v == "avoided"}


def dodgeable(pnum, target, problems):
    """True if a recorded alt walk lets this problem be solved without target."""
    return any(target not in walk
               for walk in problems.get(pnum, {}).get("alt_walks", []))


def clear_branch(name):
    """True when no local branch `name` blocks a fresh checkout -b: either
    none exists, or the user was asked and chose to delete it. Without a
    TTY the branch is kept, never silently deleted."""
    if subprocess.run(["git", "rev-parse", "--verify", "--quiet",
                       "refs/heads/" + name], capture_output=True).returncode:
        return True
    last = subprocess.run(["git", "log", "-1", "--format=%s (%cs)", name],
                          capture_output=True, text=True).stdout.strip()
    if sys.stdin.isatty():
        ans = input(f"branch '{name}' already exists - {last}. Delete it? [y/N] ")
        if ans.strip().lower() in ("y", "yes"):
            subprocess.run(["git", "branch", "-D", name],
                           check=True, capture_output=True)
            return True
    print(f"kept branch '{name}' - `git checkout {name}` to resume it")
    return False


def mined_solve_times(with_file=False):
    """(key, date, seconds) per timed successful solve commit, oldest first;
    key is the problem number, or d:<title stem> for bank drills. With
    with_file=True the solved/ filename is appended, to join evidence. Only
    commits adding exactly ONE solve carry a truthful "solve time" trailer
    (the day-one bulk import smeared a single trailer over 109 files).
    FAILED files measure time-to-walking-away and >10h means a file left
    open across days, so both are dropped."""
    root = os.path.dirname(GRAPH_DIR)
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True, cwd=root).stdout.strip()
    cache = os.path.join(root, ".solvetimes_cache.json")
    try:
        with open(cache) as f:
            data = json.load(f)
        if data.get("head") == head:
            reps = [(k, date.fromisoformat(d), secs, f) for k, d, secs, f in data["reps"]]
            return reps if with_file else [r[:3] for r in reps]
    except (OSError, ValueError, KeyError, TypeError):
        pass
    reps = _mine_solve_times(root)
    try:
        with open(cache, "w") as f:
            json.dump({"head": head, "reps": [(k, d.isoformat(), secs, fn)
                                              for k, d, secs, fn in reps]}, f)
    except OSError:
        pass
    return reps if with_file else [r[:3] for r in reps]


def _mine_solve_times(root):
    """mined_solve_times without the cache: the git log itself. Slow (a
    tenth of a second per call), so the result is cached per HEAD commit
    in .solvetimes_cache.json - every solve is a commit, so the cache is
    exactly as fresh as the history."""
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%x01%at%x01%B%x02",
         "--name-only", "--", "solved/"],
        capture_output=True, text=True, cwd=root).stdout
    parts = out.split("\x01")[1:]
    reps = []
    for at, rest in zip(parts[::2], parts[1::2]):
        body, _, tail = rest.partition("\x02")
        m = re.search(r"solve time: (\d+)m (\d+)s", body)
        if not m:
            continue
        secs = int(m.group(1)) * 60 + int(m.group(2))
        added = re.findall(r"^solved/(\S+\.py)$", tail, flags=re.M)
        if len(added) != 1 or "FAILED" in added[0] or not 0 < secs < 36000:
            continue
        pm = re.match(r"p(\d+)_", added[0])
        dm = re.match(r"d_(.+?)_\d{4}_", added[0])
        key = pm.group(1) if pm else (f"d:{dm.group(1)}" if dm else None)
        if key:
            reps.append((key, datetime.fromtimestamp(int(at)).date(), secs,
                         f"solved/{added[0]}"))
    return sorted(reps, key=lambda r: r[1])


FORECAST_WARM_DAYS = 30


def drill_forecast(path, today=None):
    """(expect_min, hint_min, bail_min) for serving a bank drill file, from
    the mined history — same shape as solve_forecast. First-time rungs fall
    back to the median first-attempt time across all timed drills."""
    import math
    from statistics import median

    today = today or date.today()
    reps = mined_solve_times()
    if not reps:
        return None
    key = f"d:{drill_solved_stem(path)}"
    by_key = {}
    for k, d, secs in reps:
        by_key.setdefault(k, []).append((d, secs))
    mine = by_key.get(key)
    if mine:
        ratios = {True: [], False: []}
        for rs in by_key.values():
            for (d0, s0), (d1, s1) in zip(rs, rs[1:]):
                ratios[(d1 - d0).days <= FORECAST_WARM_DAYS].append(math.log2(s1 / s0))
        d0, s0 = mine[-1]
        warm = (today - d0).days <= FORECAST_WARM_DAYS
        r = median(ratios[warm]) if ratios[warm] else 0.0
        base = s0 / 60 * 2 ** r
    else:
        firsts = [rs[0][1] / 60 for k, rs in by_key.items() if k.startswith("d:")]
        if len(firsts) < 8:
            return None
        base = median(firsts)
    base = max(base, 1.0)
    return base, base * 2, base * 4


def solve_forecast(pnum, problems, today=None):
    """(expect_min, hint_min, bail_min) for serving pnum now, from the mined
    solve-time history, or None when there is nothing to base it on.

    Seen before: the previous attempt's time scaled by the live warm/cold
    re-solve ratio (2026-08-25 analysis: ~0.76x inside a month, ~0.93x
    beyond). First meeting: the median first-attempt time of same-difficulty
    problems in the same connectivity tercile. The hint and bail marks are
    ~P70 and ~P90 of the observed spread (log2 sd ~1.5): base x2 and x4."""
    import math
    from statistics import median

    today = today or date.today()
    reps = mined_solve_times()
    if not reps:
        return None
    by_key = {}
    for key, d, secs in reps:
        by_key.setdefault(key, []).append((d, secs))

    mine = by_key.get(str(pnum))
    if mine:
        ratios = {True: [], False: []}
        for rs in by_key.values():
            for (d0, s0), (d1, s1) in zip(rs, rs[1:]):
                ratios[(d1 - d0).days <= FORECAST_WARM_DAYS].append(math.log2(s1 / s0))
        d0, s0 = mine[-1]
        warm = (today - d0).days <= FORECAST_WARM_DAYS
        r = median(ratios[warm]) if ratios[warm] else 0.0
        base = s0 / 60 * 2 ** r
    else:
        conn = node_conn(problems)
        my = problems.get(str(pnum), {})
        if not my.get("moves"):
            return None
        def mean_conn(p):
            mv = p.get("moves", [])
            return sum(conn.get(m, 0.0) for m in mv) / len(mv) if mv else 0.0
        firsts = [(mean_conn(problems[k]), rs[0][1] / 60)
                  for k, rs in by_key.items()
                  if k in problems and problems[k].get("difficulty") == my.get("difficulty")
                  and problems[k].get("moves")]
        if len(firsts) < 8:
            return None
        cs = sorted(c for c, _ in firsts)
        t1, t2 = cs[len(cs) // 3], cs[2 * len(cs) // 3]
        tier = lambda c: 0 if c <= t1 else (1 if c <= t2 else 2)
        mine_tier = tier(mean_conn(my))
        pool = [t for c, t in firsts if tier(c) == mine_tier]
        base = median(pool if len(pool) >= 8 else [t for _, t in firsts])

    base = max(base, 1.0)
    return base, base * 2, base * 4


def node_conn(problems):
    """log2 carrier count per node — how many problems rehearse the move.
    The forgetting curve's connectivity covariate (kg_curve): widely carried
    moves hold on longer than their rep counts alone predict, because the
    rest of the catalog keeps rehearsing them incidentally."""
    import math

    counts = {}
    for p in problems.values():
        for m in p.get("moves", []):
            counts[m] = counts.get(m, 0) + 1
    return {n: math.log2(1 + c) for n, c in counts.items()}


def carriers_for(target, problems, statuses, nodes, evidence):
    """Problems containing the target move whose every OTHER move is SOLID.
    Banned problems ("banned": true) are never offered as carriers.
    Hards are summits, never refresh carriers — rusty moves get their reps
    at basecamps (easies/mediums); a Hard is attempted only all-green.
    A problem declaring "after" waits until its predecessor is warm
    (held_behind), so 46 is served before 47."""
    found = []
    for pnum, p in problems.items():
        moves = p.get("moves", [])
        if p.get("banned") or p.get("difficulty") == "Hard" or target not in moves \
                or not all(m in nodes for m in moves):
            continue
        if all(statuses[m][0] == SOLID for m in moves if m != target) \
                and not held_behind(pnum, problems, evidence):
            found.append(pnum)
    return found


# A carrier solved within the last few days is not a spaced review: it reruns
# a problem still sitting in working memory, and a rep that close cannot even
# advance the node's maturity spacing (see MATURE_SPACING_DAYS). The picker
# lands there whenever a solve fails to evidence its target move - the node
# stays rusty, so the next morning's plan comes straight back to the same
# problem. Composable predicate, applied where carriers are picked for spaced
# review; deliberately NOT folded into carriers_for, which also answers "does
# a servable carrier exist at all" for the route planners and diagnostics.
CARRIER_COOLDOWN_DAYS = MATURE_SPACING_DAYS


def cooled(pnum, evidence, days=CARRIER_COOLDOWN_DAYS):
    """True when this problem's last solve is old enough to review again.
    Never solved counts as cooled."""
    last = last_solved(pnum, evidence)
    return not last or (date.today() - date.fromisoformat(last)).days >= days


# The connectivity discount on solve time is a threshold, not a gradient:
# the running medians sit flat until a walk's moves are shared by roughly
# thirty problems, then bend down (README, 2026-08-27 charts). Candidates at
# or past the mass cap tie, and the gentleness keys decide between them.
CONN_MASS_CAP = 30


def predicted_carrier(target, problems, statuses, nodes,
                      predicted=None, skip=(), difficulties=("Easy", "Medium")):
    """The frontier mover (PLAN.md phase 4): when no evidenced problem can
    carry `target`, promote the best drafted one. Returns (pnum, entry) or
    None. `entry` is problems.json-shaped and flagged "predicted": True; it
    lives in memory only — what maps the problem for real is the evidenced
    walk kg_extract writes after the solve.

    A candidate is an unmapped easy/medium with a drafted walk in which the
    ONE non-solid move is the target — the one-new-move rule applied to the
    predicted tier — and no missing-move flags (a walk the taxonomy cannot
    express yet is not a carrier). Hards stay summits. Ranking is
    cheap-regime-first: the walk whose rarest supporting move has the most
    problems rehearsing it (capped at CONN_MASS_CAP), then the usual
    gentleness and acceptance keys. `difficulties` narrows the pool: a
    proving rep for a medium-bar node has to be a Medium."""
    import numpy as np
    if predicted is None:
        predicted = load_predicted()
    dm = _draft_matrix(predicted, sorted(statuses))
    if target not in dm.index:
        return None
    t = dm.index[target]
    solid = np.array([statuses[n][0] == SOLID for n in dm.node_ids], dtype=bool)
    others = dm.W.copy()
    others[:, t] = False
    gaps = (others & ~solid).sum(1) + dm.unknown
    sel = dm.W[:, t] & ~dm.missing & (gaps == 0) & dm.live_problems(problems)[dm.prob]
    walks = np.flatnonzero(sel)
    if not len(walks):
        return None
    probs, firsts = np.unique(dm.prob[walks], return_index=True)
    walks = walks[firsts]
    counts = dm.carrier_counts(problems)
    mass = np.where(others[walks], counts, np.inf).min(1)
    mass = np.where(np.isfinite(mass), mass, CONN_MASS_CAP)
    best = []
    for pi, wi, m in zip(probs, walks, mass):
        num = dm.problems[pi]
        diff = dm.diff[pi]
        if num in skip or diff not in ("Easy", "Medium") or diff not in difficulties:
            continue
        best.append((num, dm.walk_moves[wi], diff, min(int(m), CONN_MASS_CAP)))
    if not best:
        return None
    best.sort(key=lambda t: (
        DIFF_RANK.get(t[2], 1),
        -t[3],
        (len(input_tree(t[1], nodes)), len(t[1])),
        -acceptance(t[0]),
        pnum_key(t[0]),
    ))
    num, moves, diff, _ = best[0]
    title = predicted[num].get("title") \
        or _metadata().get(str(num), {}).get("title", f"problem {num}")
    return num, {"title": title, "difficulty": diff, "moves": list(moves),
                 "predicted": True}


def drafted_in_reach(problems, statuses, nodes, immature, predicted=None,
                     skip=(), first="Hard", limit=20):
    """Unsolved drafted problems whose walk is entirely in reach: every move
    a node, SOLID and mature, no missing-move flags. Ranked `first` (Hard
    or Medium) ahead of the other, Easy last; within a difficulty the walk
    whose rarest move has the most evidenced carriers, then acceptance,
    then number. Each entry is problems.json-shaped and flagged
    "predicted": True, like predicted_carrier's; the first `limit` after
    `skip`. The picker's last rule: once the graph is solid and no young
    move has a carrier, this is what is left of leetcode. The caller
    alternates `first` so a day is Hards and Mediums, not Hards alone (the
    2026-08-31 simulation: 550 Hards to 53 Mediums in 120 days, and the
    medium pass rate starved)."""
    import numpy as np
    if predicted is None:
        predicted = load_predicted()
    dm = _draft_matrix(predicted, list(nodes))
    reach = np.array([statuses[n][0] == SOLID and n not in immature
                      for n in dm.node_ids], dtype=bool)
    gaps = (dm.W & ~reach).sum(1) + dm.unknown
    sel = ~dm.missing & (gaps == 0) & dm.live_problems(problems)[dm.prob]
    walks = np.flatnonzero(sel)
    if not len(walks):
        return []
    # the first qualifying walk of each problem, in file order
    probs, firsts = np.unique(dm.prob[walks], return_index=True)
    walks = walks[firsts]
    counts = dm.carrier_counts(problems)
    mass = np.where(dm.W[walks], counts, np.inf).min(1)
    mass = np.minimum(np.where(np.isfinite(mass), mass, CONN_MASS_CAP), CONN_MASS_CAP)
    rank_of = {"Easy": 0, "Medium": 1, "Hard": 1}
    rank_of[first] = 2
    rank = np.array([rank_of.get(dm.diff[p], -1) for p in probs], dtype=int)
    keep = rank >= 0
    probs, walks, mass, rank = probs[keep], walks[keep], mass[keep], rank[keep]
    order = np.lexsort((dm.pkey[probs], -dm.acc[probs], -mass, -rank))
    meta = _metadata()
    out = []
    for i in order:
        num = dm.problems[probs[i]]
        if num in skip:
            continue
        out.append((num, {"title": predicted[num].get("title")
                          or meta.get(str(num), {}).get("title", f"problem {num}"),
                          "difficulty": dm.diff[probs[i]],
                          "moves": list(dm.walk_moves[walks[i]]),
                          "predicted": True}))
        if len(out) >= limit:
            break
    return out


DRAFT_MISSES = 2  # drafted carriers solved without the move before drafts stop
_DRAFTS_OF = {}   # memo: the drafts naming a target, per (predicted, target)


def draft_misses(target, evidence, nodes=None, predicted=None):
    """Drafted carriers for `target` that were solved WITHOUT evidencing it,
    sorted by problem number. Each one falsifies its draft: the walk the
    LLM predicted is not the walk this operator takes. Only evidence from
    on or after the node's `added` date counts - a solve older than the
    node could not have evidenced it whatever the walk was.

    The loop this kills (2026-08-29, counting-sort-buckets): the frontier
    mover promoted 1365, 1854, 1893, 2149 one after another, each came back
    mapped to some other move, the node stayed MISSING, and the mover
    promoted the next of 56 drafts. Nothing counted the misses."""
    if predicted is None:
        predicted = load_predicted()
    key = (id(predicted), target)
    drafts = _DRAFTS_OF.get(key)
    if drafts is None:
        if len(_DRAFTS_OF) > 512:
            _DRAFTS_OF.clear()
        drafts = _DRAFTS_OF[key] = {
            num for num, prob in predicted.items()
            if any(target in w.get("moves", []) for w in prob.get("walks", []))
        }
    added = (nodes or {}).get(target, {}).get("added", "")
    solved, hit = set(), set()
    for pnum, recs in ev_index(evidence).by_problem.items():
        if pnum not in drafts:
            continue
        for d, _, rec in recs:
            if d < added:
                continue
            solved.add(pnum)
            if target in rec.get("moves", {}):
                hit.add(pnum)
    return sorted(solved - hit, key=pnum_key)


def drafts_falsified(target, evidence, nodes=None, predicted=None):
    """True once DRAFT_MISSES drafted carriers for `target` were solved
    without it: the predicted tier is wrong about this move, so promoting
    more of it is a carousel, not a carrier. The node needs a mapped
    carrier or a drill bank, and the picker says so instead of spinning."""
    return len(draft_misses(target, evidence, nodes, predicted)) >= DRAFT_MISSES


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
    DRILL title cleaned exactly the way utils/kg/solved cleans it. Falls back
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
    dates = [d for d, base, _ in ev_index(evidence).drills if base.startswith(key)]
    return max(dates) if dates else ""


def latest_drill_rep(path, evidence):
    """The most recent solved record of this bank drill, or None. Same-day
    reps are ordered by the solved filename, which carries the timestamp."""
    key = f"d_{drill_solved_stem(path)}_".lower()
    reps = [t for t in ev_index(evidence).drills if t[1].startswith(key)]
    return max(reps, key=lambda t: t[:2])[2] if reps else None


def drill_clean(path, evidence):
    """True when this rung's most recent rep is all-clean, assisted or not:
    the cram bar (`make next sql cram early`), where a hinted clean is a
    legit rep and the ladder climbs in one sitting instead of waiting a
    day per rung for the unaided one."""
    rec = latest_drill_rep(path, evidence)
    if rec is None:
        return False
    return bool(rec.get("moves")) and all(v == "clean" for v in rec["moves"].values())


def drill_assisted(path, evidence):
    """True when this drill's most recent rep exists and was not an unaided
    clean: a hint, a walkthrough, a spoil, or a struggle. The drill has been
    met but is not owned; the unaided rep is what it is waiting for."""
    rec = latest_drill_rep(path, evidence)
    if rec is None:
        return False
    return not (rec.get("moves") and all(v == "clean" for v in rec["moves"].values())
                and assist_of(rec) == "none")


def drill_warm(path, evidence, today=None):
    """True when this rung's most recent rep is all-clean, not spoiled, and
    inside the solid window — the bar it must meet to release the rung above
    it. A drill is a problem we created, so this is held_behind's release
    rule; latest-rep because a struggle after a clean means the rung is not
    warm, whatever the graph once believed."""
    rec = latest_drill_rep(path, evidence)
    if rec is None:
        return False
    when = rec["date"]
    today = today or date.today()
    return (rec.get("moves") and all(v == "clean" for v in rec["moves"].values())
            and assist_of(rec) == "none"
            and (today - date.fromisoformat(when)).days <= SOLID_WINDOW_DAYS)


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


def owned(node_id, evidence):
    """True when the node's most recent clean rep was unaided ON THIS MOVE.
    An assisted clean is a legit re-learning rep but it is not recall - the
    same ownership bar last_clean_solve applies to problem release. Same-day
    reps tie generously: one unaided clean that day is ownership. Help on
    another move of the same walk does not count against this one (the
    per-move assist shape, assist_of)."""
    latest, ok = "", False
    for _, v, a, _, rec in ev_index(evidence).by_node.get(node_id, ()):
        if v != "clean":
            continue
        unaided = a == "none"
        if rec["date"] > latest:
            latest, ok = rec["date"], unaided
        elif rec["date"] == latest:
            ok = ok or unaided
    return ok


def drill_held(node_id, nodes, statuses, evidence, has_bank=None, pending=()):
    """The cross-bank ladder: True while a prereq of node_id must train
    first - the prereq has a drill bank of its own and is not standing on
    an unaided clean (not SOLID, or solid only through assisted reps), or
    its drill item is still pending in today's plan. Interconnectivity is
    the point: the dependent's drill lands on an owned base instead of
    re-deriving the base mid-drill. A prereq without a bank never holds -
    nothing servable would clear the hold, and a hold nothing can open is
    a deadlock (same reasoning as banned predecessors in held_behind)."""
    has_bank = has_bank or has_drill_bank
    for p in nodes.get(node_id, {}).get("prereqs", []):
        if p in pending:
            return True
        if has_bank(p) and p in statuses and (
                statuses[p][0] != SOLID or not owned(p, evidence)
                or ladder_left(p, evidence)):
            return True  # rusty, not owned, or drills of its own still undone
    return False


def drill_trains(path):
    """The node ids a bank drill evidences: its TRAINS header, comma
    separated. A composite rung lists every move it combines, the way a
    leetcode problem's walk does; the solve evidences all of them."""
    try:
        with open(path) as f:
            m = re.search(r"^\s*TRAINS:\s*([a-z0-9\-, ]+)$", f.read(), flags=re.M)
    except OSError:
        m = None
    return [t.strip() for t in m.group(1).split(",") if t.strip()] if m else []


def released_rungs(candidates, evidence, node_id=None, early=False):
    """The prefix of a drill ladder that is open to serve. The bank's
    filename order is the ladder: a rung is held while the rung below it is
    not warm — the same "after" rule that serves 46 before 47 (held_behind);
    with `early` (the cram walk) an assisted clean below is enough.
    A composite rung (TRAINS lists other nodes) is also held until each of
    those nodes is owned - its atomic rung clean and unaided - so the
    combination lands on moves the operator has, instead of teaching two at
    once. Holds cascade, so this is always a prefix."""
    below_ok = drill_clean if early else drill_warm
    released = []
    for i, rung in enumerate(candidates):
        if i and not below_ok(candidates[i - 1], evidence):
            break
        if any(not owned(t, evidence)
               for t in drill_trains(rung) if t != node_id):
            break
        released.append(rung)
    return released or candidates[:1]


def due_drill(node_id, evidence, today=None, early=False, assisted=False):
    """Least-recently-drilled RELEASED bank file for a node, or None if the
    bank is empty or that file was already drilled today. The no-carrier
    fallback: a gap node with no READY carrier gets its drill offered instead
    of being silently skipped — a drill cannot be dodged and needs no
    carrier. With `early`, the curve is ignored: a SOLID, owned node still
    gets its next rung (the cram review, `make next sql cram early`); the
    ladder and the once-a-day rule still apply. With `assisted`, only drills
    whose latest rep was assisted are candidates (`make next sql assisted`):
    the ladder is moot, since a drill with a rep is already released, and
    the curve is off as under `early`."""
    status, _ = node_status(node_id, evidence, today)
    if (status == SOLID and owned(node_id, evidence) and not early and not assisted
            and not ladder_left(node_id, evidence)):
        return None  # the curve says the node holds - a drill is a problem
                     # we authored, and problems are not re-served while warm.
                     # A never-done drill of the node is still due: one clean
                     # drill does not stand for the others (2026-08-31, Pairs
                     # clean released the dedupe drill with subsets undone)
    today = (today or date.today()).isoformat()
    candidates = sorted(glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py")))
    if assisted:
        candidates = [p for p in candidates if drill_assisted(p, evidence)]
    if not candidates:
        return None
    pool = candidates if assisted else released_rungs(
        candidates, evidence, node_id, early=early)
    path = min(pool, key=lambda p: last_drilled(p, evidence))
    return None if last_drilled(path, evidence) >= today else path


def ladder_left(node_id, evidence, early=False):
    """True while a rung of the node's bank has never been drilled and the
    ladder can still get there: either a released rung is untouched, or the
    first held rung is held by the warm rule (the rung below it needs an
    unaided clean), which a re-serve of that rung clears. A rung held only
    because another node is not owned does not count - nothing this node
    serves would clear it, and a hold nothing can open is a deadlock (the
    2026-08-31 Combinations serve: done once with a walkthrough, so Reuse
    Allowed and Subsets stayed held, the node read done, and the dedupe
    drill got served with subsets never done)."""
    candidates = sorted(glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py")))
    released = released_rungs(candidates, evidence, node_id, early=early)
    if any(not last_drilled(p, evidence) for p in released):
        return True
    if len(released) == len(candidates):
        return False
    held = candidates[len(released)]
    return not any(not owned(t, evidence)
                   for t in drill_trains(held) if t != node_id)


def latest_carrier(node_id, evidence):
    """Most recent evidence file that exercised this node (for spaced re-solves)."""
    best = None
    for d, _, _, fname, rec in ev_index(evidence).by_node.get(node_id, ()):
        if best is None or d > best[0]:
            best = (d, fname, rec.get("problem"))
    return best


# Sleep is derived from git, never stored: a parked problem IS its
# `<num>-slept` branch, `sleeping:` / `woke:` marker commits on it carry
# the timestamps. A park sleeps until `make wake` — no timers, no
# readiness trigger, nothing auto-wakes (settled 2026-08-28).

# parked problems at once; past this, `make sleep` refuses until one is faced
MAX_ASLEEP = int(os.environ.get("MAX_ASLEEP", 3))


def _git_out(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def branch_events(branch="HEAD"):
    """Branch-only commits as (unix_ts, subject), oldest first — the
    `started` / `sleeping:` / `woke:` markers sleep state and the solve
    clock are derived from. Empty on master."""
    out = _git_out("log", "--reverse", "--format=%ct%x09%s", branch, "--not", "master")
    events = []
    for line in out.splitlines():
        ts, _, subj = line.partition("\t")
        if ts.isdigit():
            events.append((int(ts), subj))
    return events


def active_seconds(branch="HEAD", now=None):
    """(active_s, slept_s, sleeps) for a solve branch: wall time since the
    started commit, split into awake and parked intervals by the marker
    commits. On a branch with no sleeps this is the plain started-to-now
    clock `make solved` has always used."""
    now = now or time.time()
    events = branch_events(branch)
    if not events:
        out = _git_out("log", "-1", "--grep=^started$", "--format=%ct").strip()
        t0 = int(out or _git_out("log", "-1", "--format=%ct").strip() or now)
        return max(int(now - t0), 0), 0, 0
    started = [ts for ts, subj in events if subj == "started"]
    t0 = started[-1] if started else events[0][0]
    active = slept = sleeps = 0
    awake, last = True, t0
    for ts, subj in events:
        if ts < t0:
            continue
        if subj.startswith("sleeping:") and awake:
            active += ts - last
            sleeps += 1
            awake, last = False, ts
        elif subj.startswith("woke") and not awake:
            slept += ts - last
            awake, last = True, ts
    if awake:
        active += now - last
    else:
        slept += now - last
    return int(active), int(slept), sleeps


def slept_branches():
    """{problem_number: branch_name} for every local `<num>-slept` branch."""
    out = _git_out("for-each-ref", "--format=%(refname:short)", "refs/heads/*-slept")
    return {b[: -len("-slept")]: b for b in out.split()}


def sleep_records(problems, evidence):
    """Unresolved parked problems, scanned from the `-slept` branches:
    {pnum: {branch, title, slept (unix ts of last park), cycles}}.

    cycles counts the `sleeping:` commits — how many times the problem was
    parked. A branch whose problem has a solve recorded on/after its last
    park date is resolved: an archive, not a park, and is skipped."""
    recs = {}
    for pnum, branch in slept_branches().items():
        if pnum not in problems:
            continue
        events = branch_events(branch)
        marks = [ts for ts, subj in events if subj.startswith("sleeping:")]
        ts = marks[-1] if marks else (events[-1][0] if events else None)
        if ts is None:
            continue
        slept_day = datetime.fromtimestamp(ts).date().isoformat()
        if any(d >= slept_day
               for d, _, _ in ev_index(evidence).by_problem.get(pnum, ())):
            continue
        recs[pnum] = {"branch": branch, "title": problems[pnum]["title"],
                      "slept": ts, "cycles": max(len(marks), 1)}
    return recs


def sleep_state(nodes, problems, evidence):
    """Split parked problems into (asleep, woken) problem-number lists.

    Every park is ASLEEP until the operator runs `make wake` — woken is
    always empty; nothing wakes a problem automatically. asleep is ordered
    most-reslept first, so the strongest not-ready signal gets its ground
    warmed first (kg_next rule 0)."""
    recs = sleep_records(problems, evidence)
    asleep = sorted(recs, key=lambda p: (-recs[p]["cycles"], recs[p]["slept"]))
    return asleep, []


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
# utils/kg/kg_mock_rs) and the README's P(pass) history chart. The Rust port keeps
# this exact math (same RNG stream, same float-op order); change them together.

REC_POWER = {"E": 0.5, "M": 1.0, "H": 1.6}
SCENARIOS = {"cautious": 0.75, "central": 0.85, "optimistic": 0.95}

# Recognition - seeing which move a problem wants without being told - is
# the one term of the model nothing measures. It rises with mocks, and
# (2026-08-31) with cold first solves: a problem never seen before, solved
# clean and unaided, is the same test a mock poses, minus the clock. A mock
# is six problems, so six cold solves count as one. The `mocks` slot of the
# practice triple is mock-equivalents: recognition_practice(). The Rust
# port (kg_mock_rs SimState::practice) applies the same credit.
COLD_SOLVES_PER_MOCK = 6

# The practice terms' saturation constants: after this many, 63% of the
# headroom is earned. Assumed, not fitted (kg_mock_rs carries the same
# numbers); `make simulate --hard-sat 45` shows what a slower Hard curve
# does to the date. The Hard one is the whole onsite question - 15 cold
# Hards attempted so far say nothing about its slope yet.
MEDIUM_SAT = 120
HARD_SAT = 15
MOCK_SAT = 8


def recognition_practice(mocks_done, cold_first_solves):
    if not COLD_SOLVES_PER_MOCK:
        return mocks_done
    return mocks_done + cold_first_solves // COLD_SOLVES_PER_MOCK


def recognition(base, mocks_done):
    import math
    return base + (0.98 - base) * (1 - math.exp(-mocks_done / MOCK_SAT))


def carrier_counts(problems):
    """move -> how many evidenced problems walk it (problems.json primary
    walks). The rehearsal mass of a walk is the count of its rarest move."""
    counts = {}
    for p in problems.values():
        for m in p.get("moves", []):
            counts[m] = counts.get(m, 0) + 1
    return counts


def walk_mass(walk, counts):
    """x = log(1 + mass) of a walk: mass is the carrier count of its rarest
    move; a move nothing evidenced carries (off-taxonomy) counts 0."""
    return math.log1p(min((counts.get(m, 0) for m in walk), default=0))


def mass_term(pools, problems, curve=None):
    """The per-walk rehearsal-mass adjustment for pass_rates over these
    pools: {"beta", "ref": {dif: pool mean x}, "x": {dif: [[x per walk]]}}.
    beta is fitted by kg_curve (curve.json "mass"); 0 when unfitted, which
    makes the term inert. The reference is the pool mean, so a problem
    drawn uniformly keeps the model's average and only the spread between
    rehearsed and rare walks changes."""
    curve = _load_curve() if curve is None else curve
    beta = (curve or {}).get("mass", {}).get("beta", 0.0) if curve else 0.0
    counts = carrier_counts(problems)
    x = {dif: [[walk_mass(w, counts) for w in prob] for prob in probs]
         for dif, probs in pools.items()}
    ref = {dif: (sum(max(xs) for xs in xp) / len(xp) if xp else 0.0)
           for dif, xp in x.items()}
    return {"beta": beta, "ref": ref, "x": x}


def mass_adjust(p, x, ref, beta):
    """p on the logit scale shifted by beta * (x - ref); p clamped away
    from 0 and 1 so the shift is finite. Same arithmetic as the Rust port."""
    if not beta:
        return p
    p = min(max(p, 1e-9), 1 - 1e-9)
    return 1 / (1 + math.exp(-(math.log(p / (1 - p)) + beta * (x - ref))))


def pass_rates(node_recall, pools, r_base, practice, rng, n_mc=20000, mass=None):
    """(full clear, onsite 2E+2M+>=1H, screen both-M, single-hard P).

    pools: {"E"/"M"/"H": [problem, ...]}, each problem a list of walks, each
    walk a list of move names — real problems (evidenced + drafted walks, the
    Rust Bank), not fabricated ones. practice = (mediums, mock-equivalents,
    hards) done since the snapshot; see recognition_practice() for the
    second. A problem is drawn uniformly from its
    difficulty pool and scored by its BEST walk's recall product; a move
    without recall (off-taxonomy) costs the derive rate. Same draw order as
    the Rust port (randrange then random), so the RNG streams match. With
    `mass` (mass_term), the drawn problem's best walk also carries its
    rehearsal-mass adjustment (mass_adjust)."""
    time_f, rec, derive = practice_factors(practice, r_base)
    full = onsite = screen = h_solved = 0
    for _ in range(n_mc):
        solved = {"E": 0, "M": 0, "H": 0}
        for dif in ("E", "E", "M", "M", "H", "H"):
            i = rng.randrange(len(pools[dif]))
            prob = pools[dif][i]
            best, best_w = -1.0, 0
            for wi, walk in enumerate(prob):
                prod = math.prod(node_recall.get(mv, derive) for mv in walk)
                if prod > best:
                    best, best_w = prod, wi
            p = time_f[dif] * rec ** REC_POWER[dif] * best
            if mass:
                p = mass_adjust(p, mass["x"][dif][i][best_w], mass["ref"][dif],
                                mass["beta"])
            solved[dif] += rng.random() < p
        full += solved["E"] == 2 and solved["M"] == 2 and solved["H"] == 2
        onsite += solved["E"] == 2 and solved["M"] == 2 and solved["H"] >= 1
        screen += solved["M"] == 2
        h_solved += solved["H"]
    return full / n_mc, onsite / n_mc, screen / n_mc, h_solved / (2 * n_mc)


def practice_factors(practice, r_base):
    """The pass model's practice terms for a cold problem: per-difficulty
    time factor, recognition, and the derive rate for an off-taxonomy move.
    P(solve a cold problem) = time_f[dif] * rec ** REC_POWER[dif] * recall
    product; pass_rates draws sets with it, kg_simulate draws single cold
    solves with it, so the two never disagree about what a cold Hard is
    worth today."""
    import math
    mediums, mocks, hards = practice
    grow = 1 - math.exp(-mediums / MEDIUM_SAT)
    time_f = {"E": 0.88 + 0.07 * grow, "M": 0.87 + 0.07 * grow,
              "H": 0.40 + 0.42 * (1 - math.exp(-hards / HARD_SAT))}
    derive = 0.25 + 0.20 * (1 - math.exp(-(mocks + hards) / 30))
    return time_f, recognition(r_base, mocks), derive


def current_recall(nodes, evidence, curve, today=None):
    """Predicted recall per node. Pass `today` (and evidence filtered to
    entries on or before it) to replay a historical snapshot."""
    today = today or date.today()
    return {nid: node_curve_recall(nid, evidence, curve, today) for nid in nodes}


def node_curve_recall(nid, evidence, curve, today=None):
    """One node of current_recall."""
    import math
    today = today or date.today()
    p = curve["params"]
    status, last = node_status(nid, evidence, today=today)
    if status == MISSING or not last:
        return 0.25
    cleans = sum(1 for _, v, _, _, _ in ev_index(evidence).by_node.get(nid, ())
                 if v == "clean")
    s = min(max(math.exp(p["a"] + p["b"] * cleans), 7), 3650)
    rec = (1 + (today - last).days / s) ** (-p["beta"])
    return rec * 0.5 if status == FRAGILE else rec


# --- the replay clock (utils/kg/kg_movie_rs) ----------------------------------
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
