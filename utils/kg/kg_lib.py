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
from collections import namedtuple
from datetime import date, datetime, timedelta, timezone

# utils/rs/kg as a Python extension (utils/rs/kg_py; `make ext` installs it).
# The functions imported here used to be defined below; each pointer comment
# marks where. New ports are added here and the Python body deleted.
from kg_rs import degree_color, drill_key  # noqa: F401

# The system clock runs UTC but the operator lives in Manila (UTC+8);
# "today" everywhere in the toolchain means the Manila calendar day.
os.environ["TZ"] = "Asia/Manila"
time.tzset()

MANILA = timezone(timedelta(hours=8))

# solved/ filenames are stamped in UTC (utils/rs/kg_solved) - same clock as git.
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
    return (
        datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)
        .astimezone(MANILA)
        .date()
        .isoformat()
    )


UTILS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(UTILS_DIR)
GRAPH_DIR = os.path.join(REPO_ROOT, "graph")
RS_BIN = os.path.join(REPO_ROOT, "utils", "rs", "target", "release")


def load_envrc(path=None, environ=None):
    """Read the repo's .envrc the way a dotenv loader would, so the knobs
    the operator sets there (MAX_ASLEEP, KG_NO_PLAN, LEET_NO_ANIMATE) hold
    in every shell the tooling runs from, not only one with direnv loaded
    (2026-09-01: cap raised to 5 in .envrc, make next from another shell
    still said cap 3). Only `export NAME=VALUE` and `NAME=VALUE` lines with
    a literal value are taken; a value with a `$` in it is shell
    expansion and is left to the shell. The real environment wins: a
    variable already set is not overwritten."""
    path = path or os.path.join(REPO_ROOT, ".envrc")
    environ = os.environ if environ is None else environ
    try:
        with open(path) as f:
            lines = f.read().splitlines()
    except OSError:
        return {}
    loaded = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
        if not m:
            continue
        name, value = m.group(1), m.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif "$" in value:
            continue
        if name not in environ:
            environ[name] = value
            loaded[name] = value
    return loaded


load_envrc()
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


SOLID, STALE, FRAGILE, MISSING = "SOLID", "STALE", "FRAGILE", "MISSING"

ASSIST_WEIGHT = {"none": 0.0, "hint": 0.5, "walkthrough": 1.0, "learning": 2.0}


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


_ASSIST_WORDS = [
    ("learning", re.compile(r"\blearning\b", re.I)),
    ("walkthrough", re.compile(r"\bwalk(?:ed|s)?[ -]?through\b|\bwalkthrough\b", re.I)),
    ("hint", re.compile(r"\bhint(?:ed|s)?\b", re.I)),
]


def _load(name):
    with open(os.path.join(GRAPH_DIR, name)) as f:
        return json.load(f)


def load_nodes():
    return {n["id"]: n for n in _load("nodes.json")["nodes"]}


def load_all_problems():
    """graph/problems.json: every problem the graph knows, drafted and
    evidenced in one table. Gates read this one - a drafted problem waits
    behind its "after" list exactly like an evidenced one."""
    return _load("problems.json")["problems"]


def load_evidence():
    return _load("evidence.json")["evidence"]


def load_predicted():
    """The drafted walks, keyed by problem: every entry carrying "walks",
    drafted or already evidenced. The entries are the table's own, so a
    drafted problem's "after" travels with its walks."""
    return {k: v for k, v in load_all_problems().items() if v.get("walks")}


_DRAFT_MATRIX: dict = {}


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

# drill_key(fname): the drill a d_ solved file is a rep of - its lowercase
# basename with the timestamp `make solved` appends stripped (or the last
# _token when there is none, the shape the tests write); None for a problem
# solve. Implemented in Rust (utils/rs/kg/src/evidence.rs), imported from
# kg_rs above.


class _EvidenceIndex:
    __slots__ = (
        "by_node",
        "by_problem",
        "by_date",
        "drills",
        "first_reps",
        "_drills_seen",
        "n",
        "last",
    )

    def __init__(self):
        self.by_node = {}  # node -> [(date, verdict, assist, fname, rec)]
        self.by_problem = {}  # problem -> [(date str, fname, rec)]
        self.by_date = {}  # date str -> [(fname, rec)]
        self.drills = []  # [(date str, lowercase basename, rec)] of d_ files
        self.first_reps = set()  # fnames that are the first rep of their drill
        self._drills_seen = set()
        self.n = 0
        self.last = None

    def add(self, fname, rec):
        d = date.fromisoformat(rec["date"])
        # The first rep of a drill is first exposure to the drill, whatever
        # the move's status: the help he took on it says nothing about
        # recall of the move. At the node level it is scored as unaided,
        # so it neither shrinks the curve nor breaks ownership; the drill
        # itself still waits for its unaided rep (drill_warm, drill_assisted
        # read the record, not this index). Evidence is appended in
        # chronological order, so first seen is first done (2026-09-01).
        key = drill_key(fname)
        first = key is not None and key not in self._drills_seen
        if first:
            self._drills_seen.add(key)
            self.first_reps.add(fname)
        for node, v in rec.get("moves", {}).items():
            self.by_node.setdefault(node, []).append(
                (d, v, "none" if first else assist_of(rec, node), fname, rec)
            )
        pnum = rec.get("problem")
        if pnum is not None:
            self.by_problem.setdefault(str(pnum), []).append((rec["date"], fname, rec))
        self.by_date.setdefault(rec["date"], []).append((fname, rec))
        base = os.path.basename(fname).lower()
        if base.startswith("d_"):
            self.drills.append((rec["date"], base, rec))
        self.n += 1
        self.last = fname


# id(evidence) -> (evidence, _EvidenceIndex). The dict itself is held so its
# address cannot pass to a new dict of the same length while the index lives:
# without that, a test dict freed and rebuilt at the same address was handed
# the previous dict's index.
_EV_INDEX: dict = {}


def ev_index(evidence):
    """The _EvidenceIndex of this evidence dict. Reused while the dict is
    the same object and has only grown at the end since the last call;
    rebuilt otherwise."""
    from itertools import islice

    _, idx = _EV_INDEX.get(id(evidence), (None, None))
    n = len(evidence)
    if idx is not None and idx.n == n:
        return idx
    if (
        idx is not None
        and idx.n <= n
        and (idx.n == 0 or next(islice(evidence, idx.n - 1, idx.n), None) == idx.last)
    ):
        for fname, rec in islice(evidence.items(), idx.n, None):
            idx.add(fname, rec)
        return idx
    idx = _EvidenceIndex()
    for fname, rec in evidence.items():
        idx.add(fname, rec)
    _EV_INDEX.clear()
    _EV_INDEX[id(evidence)] = (evidence, idx)
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

    A learning solve is not recall evidence at all — it neither counts as a
    clean rep nor keeps the node SOLID.
    """
    status, last, _ = node_eval(node_id, evidence, today)
    return status, last


def node_eval(node_id, evidence, today=None):
    """(status, last_relevant_date, predicted_recall) in one evidence scan —
    node_status and node_recall are views of this."""
    return _node_curve(node_id, evidence, today)[:3]


def _node_curve(node_id, evidence, today=None):
    """(status, last_relevant_date, predicted_recall, memory). `memory` is
    the curve's retention component (1 + gap/s)^(-beta) before the slip
    factor: the number the SOLID cut is applied to, and the recall axis of
    node_axes. node_eval drops it so its callers and the Rust golden diff
    (utils/rs/kg) see the same three-tuple as before."""
    today = today or date.today()
    entries = [
        (d, v, a) for d, v, a, _, _ in ev_index(evidence).by_node.get(node_id, ())
    ]  # (date, verdict, assist)
    if not entries:
        return MISSING, None, 0.0, 0.0
    entries.sort()
    last_date, last_verdict, _ = entries[-1]
    clean_dates = [d for d, v, a in entries if v == "clean" and a != "learning"]
    if last_verdict in ("struggled", "avoided") and not (
        clean_dates and clean_dates[-1] >= last_date
    ):
        return FRAGILE, last_date, 0.0, 0.0
    if not clean_dates:
        return FRAGILE, last_date, 0.0, 0.0

    curve = _load_curve()
    if curve:
        import math

        p = curve["params"]
        # distinct days, not entries: same-day reps are one rep (massed
        # practice does not earn spaced-practice stability), matching
        # kg_curve.extract_trials
        cleans = len(set(clean_dates))
        struggles = sum(1 for _, v, _ in entries if v == "struggled")
        assisted = sum(ASSIST_WEIGHT[a] for _, _, a in entries)
        # connectivity covariate: widely carried moves hold on longer. The
        # node's log2 carrier count is frozen into curve.json at fit time;
        # unknown nodes get the mean (a centered zero effect).
        cmean = p.get("conn_mean", 0.0)
        cn = curve.get("conn", {}).get(node_id, cmean)
        stability = math.exp(
            p["a"]
            + p["b"] * math.log1p(cleans)
            - p["c"] * struggles
            - p.get("d", 0.0) * assisted
            + p.get("e", 0.0) * (cn - cmean)
        )
        stability = min(max(stability, 7), 3650)  # sanity clamp
        gap = max((today - clean_dates[-1]).days, 0)
        memory = (1 + gap / stability) ** (-p["beta"])
        recall = (1 - p.get("slip", 0.0)) * memory
        status = SOLID if memory >= curve["target_retention"] else STALE
        return status, clean_dates[-1], recall, memory

    if today - clean_dates[-1] <= timedelta(days=SOLID_WINDOW_DAYS):
        return SOLID, clean_dates[-1], 1.0, 1.0
    return STALE, clean_dates[-1], 0.0, 0.0


STARVED_DAYS = 14  # a move due this long with no rep aimed at it is starved

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
        if (
            not str(pnum)[:1].isdigit()
            or unservable(pnum, p)
            or p.get("difficulty") == "Hard"
        ):
            continue
        for w in [p.get("moves", [])] + list(p.get("alt_walks", [])):
            for m in w:
                kinds.setdefault(m, set()).add(p.get("difficulty"))
    memo.update(id=id(problems), n=len(problems), kinds=kinds)
    return kinds


_CARRY_KINDS: dict = {}  # memo of the last bank seen: problems only ever grow


def _bar_of(kinds):
    if "Medium" in kinds:
        return "medium", MATURE_CARRY_MEDIUMS
    if kinds:
        return "real", 1
    return "none", 0


def _clean_reps(evidence):
    """node -> [(date, problem), ...] over its clean, non-learning reps."""
    return {
        nid: [
            (d, str(rec.get("problem", "")))
            for d, v, a, _, rec in entries
            if v == "clean" and a != "learning"
        ]
        for nid, entries in ev_index(evidence).by_node.items()
    }


def _at_bar(pnums, bar, problems):
    """The distinct real problems among `pnums` that count toward `bar`:
    Medium/Hard only for a medium bar, any real problem otherwise. Drills
    (problem="drill") never count."""
    kind, _ = bar
    out = {p for p in pnums if p[:1].isdigit()}
    if kind == "medium":
        out = {p for p in out if problem_difficulty(p, problems) in ("Medium", "Hard")}
    return out


def _mature_from(clean, bar, problems):
    if not clean:
        return False
    dates = sorted(d for d, _ in clean)
    if (dates[-1] - dates[0]).days < MATURE_SPACING_DAYS:
        return False
    kind, need = bar
    if kind == "none":
        return True
    # distinct problems, not reps: two clean reps of one Medium prove memory
    # of that problem, not that the move carries (2026-09-07)
    return len(_at_bar({p for _, p in clean}, bar, problems)) >= need


def proven_carriers(node_id, evidence, problems, unaided=False):
    """The distinct real problems that gave node_id a clean non-learning rep
    at its carry bar (carry_bar). With `unaided`, only reps taken with no
    help count - the ownership bar of owned() applied problem by problem."""
    pnums = {
        str(rec.get("problem", ""))
        for _, v, a, _, rec in ev_index(evidence).by_node.get(node_id, ())
        if v == "clean" and a != "learning" and (not unaided or a == "none")
    }
    return _at_bar(pnums, carry_bar(node_id, problems), problems)


# --- degree of ownership --------------------------------------------------
# Status says whether the curve predicts recall today. It says nothing about
# transfer: five drill reps and five distinct carriers grow the same
# stability, so a node fed by drills alone reads as owned as one solved from
# several sides. Degree is the weaker of two axes: memory, the curve's
# retention component, and breadth, how many distinct real problems the move
# has been executed on unaided. A node owns its cell set only to that degree
# (2026-09-07).

BREADTH_FULL = 3  # distinct unaided carriers at bar for breadth 1.0

Axes = namedtuple("Axes", "status last memory carriers breadth degree")


def breadth_score(carriers, bar, any_unaided):
    """Breadth in [0, 1] from `carriers` distinct unaided carriers at `bar`.
    No unaided clean rep at all is 0. A node no real problem carries (bar
    "none") has nothing to prove on: one unaided rep is full breadth, the
    deadlock reasoning of _mature_from. Otherwise a drill-only node reads
    0.25 and each distinct carrier adds 0.25 up to BREADTH_FULL."""
    if not any_unaided:
        return 0.0
    if bar[0] == "none":
        return 1.0
    return (1 + min(carriers, BREADTH_FULL)) / (1 + BREADTH_FULL)


def node_axes(node_id, evidence, problems, today=None):
    """Axes(status, last, memory, carriers, breadth, degree) for a node.
    memory is 0 for MISSING and FRAGILE, as node_recall; degree is
    min(memory, breadth)."""
    status, last, _, memory = _node_curve(node_id, evidence, today)
    bar = carry_bar(node_id, problems)
    carriers = proven_carriers(node_id, evidence, problems, unaided=True)
    any_unaided = any(
        v == "clean" and a == "none"
        for _, v, a, _, _ in ev_index(evidence).by_node.get(node_id, ())
    )
    breadth = breadth_score(len(carriers), bar, any_unaided)
    return Axes(status, last, memory, len(carriers), breadth, min(memory, breadth))


def node_degree(node_id, evidence, problems, today=None):
    """Degree of ownership in [0, 1]: node_axes(...).degree."""
    return node_axes(node_id, evidence, problems, today).degree


# --- the ownership ramp ---------------------------------------------------
# Every drawn node is filled from one ramp over its degree of ownership:
# the FRAGILE red at 0 sweeping through orange and amber to the green a
# full owner reads as at 1 - the order the status colours always had,
# made continuous. Interpolated in OKLCH (lightness, chroma and hue each
# linear, hue the short way round through yellow); every step clears the
# dark chart surface (#0d1117) at 4:1 or better. Red-green is the pair
# colour-blind readers merge; the operator chose it over a one-hue green
# ramp on 2026-09-07, the four labels having been red/yellow/green all
# along. utils/rs/kg/src/render.rs holds the one implementation.

# degree_color(degree): the hex colour of a degree of ownership in [0, 1] on
# the ramp #da3633 (degree 0) to #3fb950 (degree 1). Implemented in Rust
# (utils/rs/kg/src/render.rs), imported from kg_rs above.


def mature(node_id, evidence, problems):
    """True when a node's mastery is proven enough to carry a Hard.

    Two signals, both required:
      spacing      clean (non-learning) reps on two days at least
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
    return _mature_from(
        _clean_reps(evidence).get(node_id, []), carry_bar(node_id, problems), problems
    )


_IMMATURE: dict = {}  # memo: maturity changes only with the evidence or the bank


_WALKS_CARRYING: dict = {}


def last_clean_solve(pnum, evidence):
    """Latest date this problem was solved with every walked move clean and
    no assist at all - the bar a predecessor must meet to release the
    problems declared "after" it. An assisted clean is a real rep, but the
    release is on ownership: the unaided rep is what releases."""
    dates = [
        d
        for d, _, r in ev_index(evidence).by_problem.get(str(pnum), ())
        if r.get("moves")
        and all(v == "clean" for v in r["moves"].values())
        and assist_of(r) == "none"
    ]
    return max(dates) if dates else ""


def vertex_kind(vid, problems):
    """What an id in an "after" list names: "problem", "drill", "node", or
    None when nothing in the graph carries it. Problem keys are numbers,
    drill ids are d1, d2, ... (drills.json), node ids are kebab-case."""
    vid = str(vid)
    if vid in problems:
        return "problem"
    if vid in drills():
        return "drill"
    if vid in load_nodes():
        return "node"
    if vid in _problems_ro():
        return "problem"  # drafted: not in the evidenced view the caller holds
    return None


def warm(vid, problems, evidence, today=None, early=False):
    """Whether the vertex `vid` is owned, by the bar its kind carries. A
    problem: an unaided all-clean solve inside the solid window. A drill:
    its latest rep is such a solve (drill_warm), or with `early` any
    all-clean rep (drill_clean, the cram bar). A node: its latest clean rep
    was unaided (owned). None for an id nothing carries."""
    today = today or date.today()
    kind = vertex_kind(vid, problems)
    if kind == "problem":
        last = last_clean_solve(vid, evidence)
        return (
            bool(last) and (today - date.fromisoformat(last)).days <= SOLID_WINDOW_DAYS
        )
    if kind == "drill":
        path = drill_path(vid)
        return (
            drill_clean(path, evidence) if early else drill_warm(path, evidence, today)
        )
    if kind == "node":
        return owned(vid, evidence)
    return None


def pnum_key(pnum):
    """Numeric sort that tolerates non-leetcode ids like '2167B'."""
    digits = "".join(c for c in str(pnum) if c.isdigit())
    return (int(digits) if digits else 0, str(pnum))


_DODGED: dict = {}  # memo of the latest verdict per node, extended as evidence grows


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


def paid_only(pnum):
    """True for a LeetCode premium problem. `make prepare` cannot fetch one
    ("Question 261 is paid only"), so nothing may be served on it. Read from
    data/problems_metadata.json, which records the flag for the 783 problems
    that carry it; unknown problems are treated as free."""
    return bool(_metadata().get(str(pnum), {}).get("paid_only"))


def unservable(pnum, p):
    """A problem the picker must never offer: banned (its training value is
    buried under busywork) or paid-only (there is no statement to prepare).
    Both are still audited, drawn and counted as evidence - this is only
    about being served. 261 was solved in November 2025 and came back on
    the review clock ten months later, to a prepare that could not fetch it
    (2026-09-09)."""
    return bool(p.get("banned")) or paid_only(pnum)


def problem_difficulty(pnum, problems):
    """Difficulty of a real problem: problems.json first (the curated truth
    for mapped ones), metadata as fallback for evidence-only references."""
    return problems.get(str(pnum), {}).get("difficulty") or _metadata().get(
        str(pnum), {}
    ).get("difficulty", "")


DIFF_RANK = {"Easy": 0, "Medium": 1, "Hard": 2}


def gentleness(pnum, problems, nodes):
    """Gentler-first key for fresh-carrier sorts: difficulty tier, then
    input-tree size. Community friction (acceptance) is deliberately NOT
    part of this key — it is a noisy, popularity-skewed proxy, so callers
    append -acceptance(p) as their FINAL tiebreak, after freshness
    (last_solved), never before it."""
    tier = DIFF_RANK.get(problems.get(str(pnum), {}).get("difficulty"), 1)
    return (tier, tree_size(pnum, problems, nodes))


_DRILL_HEADERS: dict = {}  # path -> (mtime_ns, size, DRILL title, TRAINS ids)


def _drill_header(path):
    """(DRILL title or None, TRAINS ids) of a bank file, read once per
    file version: the picker asks for these thousands of times per pick
    and the file never changes under it. Keyed on the file's mtime and
    size so a rewritten file (the test banks, a bank edit) reads fresh."""
    try:
        st = os.stat(path)
    except OSError:
        return None, []
    hit = _DRILL_HEADERS.get(path)
    if hit is not None and hit[0] == st.st_mtime_ns and hit[1] == st.st_size:
        return hit[2], hit[3]
    try:
        with open(path) as f:
            text = f.read()
    except OSError:
        return None, []
    m = re.search(r"^\s*DRILL:\s*(.+)$", text, flags=re.M)
    title = m.group(1).strip() if m else None
    m = re.search(r"^\s*TRAINS:\s*([a-z0-9\-, ]+)$", text, flags=re.M)
    trains = [t.strip() for t in m.group(1).split(",") if t.strip()] if m else []
    _DRILL_HEADERS[path] = (st.st_mtime_ns, st.st_size, title, trains)
    return title, trains


def drill_title(path):
    """The DRILL header of a bank file, or None when it has none."""
    return _drill_header(path)[0]


def drill_solved_stem(path):
    """The d_-filename stem `make solved` writes for this drill file: its
    DRILL title cleaned exactly the way utils/rs/kg_solved cleans it. Falls back
    to the bank filename slug if the header is missing."""
    title = drill_title(path)
    if title is None:
        title = os.path.splitext(os.path.basename(path))[0]
    return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")


def bank_paths(node_id="*"):
    """The bank files of a node (or of every node), in drill-id order: the
    files are named d<id>_<slug>.py so they are easy to find, and a plain
    string sort would put d76 before d8. Files without an id sort last, by
    name. Where nothing else separates two drills (both never done), the
    lower id is served first."""

    def key(path):
        i = drill_id(path)
        return (int(i[1:]) if i else 10**9, os.path.basename(path))

    return sorted(glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py")), key=key)


_DRILL_PATHS: dict = {}  # DRILLS_DIR -> {DRILL title: bank path}


def drill_path(ref):
    """The bank file for a drill id (d61) or DRILL title, or None. The id
    is how the graph names a drill; the title is the file's DRILL header
    and the key of its evidence, so bank files can be renamed or moved
    without touching the graph."""
    title = drills().get(ref, {}).get("title", ref)
    paths = _DRILL_PATHS.get(DRILLS_DIR)
    if paths is None or title not in paths:
        paths = {}
        for path in sorted(
            glob.glob(os.path.join(DRILLS_DIR, "*", "*.py"))
        ):  # not bank_paths: it needs drill_id
            t = drill_title(path)
            if t is not None:
                paths.setdefault(t, path)
        _DRILL_PATHS.clear()
        _DRILL_PATHS[DRILLS_DIR] = paths
    return paths.get(title)


_DRILLS = None  # drills.json: {id: {"title": DRILL title, "after": [ids], "trains": [node ids]}}


def load_drills():
    return _load("drills.json")["drills"]


def drills():
    global _DRILLS
    if _DRILLS is None:
        _DRILLS = load_drills()
    return _DRILLS


_DRILL_IDS: dict = {}  # {"key": (id(drills()), len), "map": {DRILL title: id}}


def drill_id(path):
    """The graph id (d61) of a bank file, by its DRILL title; None when the
    file has no entry in drills.json. The title index is rebuilt when the
    registry is replaced or grows (the test banks add to it in place)."""
    title = drill_title(path)
    reg = drills()
    key = (id(reg), len(reg))
    if _DRILL_IDS.get("key") != key:
        _DRILL_IDS.clear()
        _DRILL_IDS["key"] = key
        _DRILL_IDS["map"] = {d.get("title"): i for i, d in reversed(list(reg.items()))}
    i = _DRILL_IDS["map"].get(title)
    return i if i is not None and reg.get(i, {}).get("title") == title else None


def drill_after(path):
    """The ids this bank drill comes after (graph/drills.json). A drill with
    no entry comes after nothing."""
    return list(drills().get(drill_id(path), {}).get("after", []))


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
    """True when this drill's most recent rep is all-clean, assisted or not:
    the cram bar (`make next sql cram early`), where a hinted clean is a
    legit rep and a chain of drills is done in one sitting instead of
    waiting a day per drill for the unaided one."""
    rec = latest_drill_rep(path, evidence)
    if rec is None:
        return False
    return bool(rec.get("moves")) and all(v == "clean" for v in rec["moves"].values())


def drill_assisted(path, evidence):
    """True when this drill's most recent rep exists and was not an unaided
    clean: a hint, a walkthrough, a copy, or a struggle. The drill has been
    met but is not owned; the unaided rep is what it is waiting for."""
    rec = latest_drill_rep(path, evidence)
    if rec is None:
        return False
    return not (
        rec.get("moves")
        and all(v == "clean" for v in rec["moves"].values())
        and assist_of(rec) == "none"
    )


def drill_warm(path, evidence, today=None):
    """True when this drill's most recent rep is all-clean, not learning, and
    inside the solid window — the bar it must meet to release what comes
    after it. A drill is a problem we created, so this is held_behind's
    release rule; latest-rep because a struggle after a clean means the
    drill is not warm, whatever the graph once believed."""
    rec = latest_drill_rep(path, evidence)
    if rec is None:
        return False
    when = rec["date"]
    today = today or date.today()
    return (
        rec.get("moves")
        and all(v == "clean" for v in rec["moves"].values())
        and assist_of(rec) == "none"
        and (today - date.fromisoformat(when)).days <= SOLID_WINDOW_DAYS
    )


_NODE_DRILL_HOLD: dict = {}


def walk_nodes(entry):
    """Every node a problem's solution might walk: the evidenced walk and its
    alt walks, or the moves of each drafted walk. What the drill holds read."""
    out = list(entry.get("moves", []))
    for alt in entry.get("alt_walks", []):
        out += list(alt)
    for w in entry.get("walks", []):
        out += list(w.get("moves", []))
    return out


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


GRAD_LADDER = (3, 10, 25)  # days to a young move's next unaided rep
GRAD_LADDER_SPARSE = (2, 7, 18)  # tighter when few problems carry the move
GRAD_SPARSE_CARRIERS = 2  # this many carriers or fewer = sparse


def graduation_due(node_id, evidence, carriers=99):
    """(due date, floor days) for a young move's next unaided rep, or None.

    The graduating floor: the fitted curve schedules no rep inside the
    window it believes, so it never observes a young move fail and the
    young-move tail stays a guess (2026-09-02). Until a move has more
    distinct unaided-clean days than the ladder has steps, its next
    unaided rep falls due at the ladder's pace after the last clean day,
    whatever the curve says. `carriers` (how many problems walk the move)
    picks the ladder: a sparsely carried move rides the tighter one, both
    because low connectivity is where the curve extrapolates most and
    because nothing else will exercise it incidentally. No unaided clean
    day at all means rules 0c/1/3 own the node, not the floor."""
    idx = ev_index(evidence)
    rows = idx.by_node.get(node_id, ())
    unaided = sorted({d for d, v, a, _, _ in rows if v == "clean" and a == "none"})
    if not unaided:
        return None
    # A drill's first rep is scored unaided at the node (the Steiner-copying
    # rule), but a copy is not recall: it may START the clock, never advance
    # the ladder or certify a gap (2026-09-02: five first-exposure drills
    # read as a survived 282-day trial on union-find). Only days holding a
    # non-first-rep unaided clean count past the first.
    proof = {
        d
        for d, v, a, f, _ in rows
        if v == "clean" and a == "none" and f not in idx.first_reps
    }
    days = [unaided[0]] + [d for d in unaided[1:] if d in proof]
    ladder = GRAD_LADDER_SPARSE if carriers <= GRAD_SPARSE_CARRIERS else GRAD_LADDER
    # the day count never graduates a move: five clean days inside one week
    # are one exposure spaced five times, not five spaced reps (2026-09-02,
    # recursive descent: longest survived gap 5 days, curve said 62 more).
    # Past the ladder's last step the floor stays at that step until a gap
    # of that length is survived - the trial below is the only way off.
    # a clean rep that already survived a gap past the ladder's last step is
    # the trial the ladder exists to run: graduated, the curve owns it. This
    # also keeps the floor from retroactively flooding the queue with every
    # long-standing thin-history node. The gap is measured between
    # consecutive EXPOSURES (a copy refreshes memory even though it proves
    # nothing), and only a proof day can end it.
    if any(
        (b - a).days >= ladder[-1] and b in proof for a, b in zip(unaided, unaided[1:])
    ):
        return None
    floor = ladder[min(len(days), len(ladder)) - 1]
    return days[-1] + timedelta(days=floor), floor


def drill_trains(path):
    """The node ids a bank drill evidences: the "trains" list of its
    drills.json entry, keyed by the stable id so a node rename touches one
    line there and never a bank file or a solved copy. A composite drill
    lists every move it combines, the way a leetcode problem's walk does;
    the solve evidences all of them. A file with no entry (the test banks,
    a simulated drill) falls back to its TRAINS header."""
    i = drill_id(path)
    if i is not None and "trains" in drills().get(i, {}):
        return list(drills()[i]["trains"])
    return list(_drill_header(path)[1])


_EVIDENCE_RO: dict = {}  # path -> (mtime_ns, size, evidence)


_BANK_FILES: dict = {}  # node id -> its drill bank files

_PROBLEMS_RO: dict = {}  # path -> (mtime_ns, size, problems)


def _problems_ro():
    """graph/problems.json, the whole table, for READ-ONLY use, parsed once
    per file version. The drill holds below ask for it on every candidate of
    every pick (tens of thousands of times in one kg_simulate run);
    load_problems parses the file each call because its callers mutate the
    result. Never hand this dict to anything that writes into it."""
    path = os.path.join(GRAPH_DIR, "problems.json")
    st = os.stat(path)
    hit = _PROBLEMS_RO.get(path)
    if hit is None or hit[0] != st.st_mtime_ns or hit[1] != st.st_size:
        hit = (st.st_mtime_ns, st.st_size, load_all_problems())
        _PROBLEMS_RO.clear()
        _PROBLEMS_RO[path] = hit
    return hit[2]


def servable_drills(candidates, evidence, node_id=None, early=False):
    """The bank files open to serve: every id in a drill's "after" list is
    warm (with `early`, the cram walk, an assisted clean of a predecessor
    drill is enough), and every other node on its TRAINS line is owned, so
    a drill that combines moves lands on moves the operator has instead of
    teaching two at once. Nothing else orders drills: not the filename,
    not the directory."""
    problems = _problems_ro()
    out = []
    for path in candidates:
        if any(
            warm(a, problems, evidence, early=early) is False for a in drill_after(path)
        ):
            continue
        if any(not owned(t, evidence) for t in drill_trains(path) if t != node_id):
            continue
        out.append(path)
    return out


def drill_scheduler(environ=None):
    """Which clock a drill runs on (DRILL_SCHEDULER, set in .envrc):
    "node", the default, where a drill is served when its node is due;
    or "anki", where every bank file keeps a clock of its own (anki_due)
    and the node's status never withholds it (2026-09-06: with the node
    clock, a drill was served the day after its first rep and then never
    again once a problem on the node went well; 28 of 41 second reps were
    at a gap of one day, the longest gap seen was 18 days, and nine nodes
    had a drill due by any per-file rule with nothing served)."""
    raw = (os.environ if environ is None else environ).get("DRILL_SCHEDULER", "node")
    return raw.strip().lower() or "node"


# The Anki (SM-2) clock, one per bank file. A rep is graded from its own
# record: an unaided all-clean is Good, a hinted all-clean is Hard, a
# walkthrough, a copy or a struggle is Again. Good multiplies the interval
# by the ease (250% to start), Hard by 1.2 and lowers the ease, Again
# sends the file back to one day and lowers the ease more. A new file
# graduates at one day; a file never done is due. Same-day reps are one
# rep: the last of the day is the grade (massed practice earns no
# interval, as in kg_curve.extract_trials).
ANKI_EASE = 2.5
ANKI_EASE_MIN = 1.3
ANKI_HARD_FACTOR = 1.2
ANKI_HARD_EASE_STEP = 0.15
ANKI_AGAIN_EASE_STEP = 0.20
ANKI_GRADUATING_DAYS = 1
ANKI_MAX_INTERVAL = 365


def anki_answer(rec):
    """good / hard / again for one drill record."""
    moves = rec.get("moves") or {}
    if moves and all(v == "clean" for v in moves.values()):
        a = assist_of(rec)
        if a == "none":
            return "good"
        if a == "hint":
            return "hard"
    return "again"


def anki_due(path, evidence):
    """(due date, interval days) for a bank file on its own clock, or None
    when the file has never been done (a new card: due now)."""
    key = f"d_{drill_solved_stem(path)}_".lower()
    reps = sorted(
        (t for t in ev_index(evidence).drills if t[1].startswith(key)),
        key=lambda t: t[:2],
    )
    if not reps:
        return None
    by_day = {}
    for d, _, rec in reps:
        by_day[d] = rec  # the last rep of a day is that day's grade
    interval, ease = 0, ANKI_EASE
    for d in sorted(by_day):
        answer = anki_answer(by_day[d])
        if answer == "good":
            interval = (
                ANKI_GRADUATING_DAYS
                if interval == 0
                else max(interval + 1, int(interval * ease + 0.5))
            )
        elif answer == "hard":
            interval = (
                ANKI_GRADUATING_DAYS
                if interval == 0
                else max(interval + 1, int(interval * ANKI_HARD_FACTOR + 0.5))
            )
            ease = max(ANKI_EASE_MIN, ease - ANKI_HARD_EASE_STEP)
        else:
            interval = ANKI_GRADUATING_DAYS
            ease = max(ANKI_EASE_MIN, ease - ANKI_AGAIN_EASE_STEP)
        interval = min(interval, ANKI_MAX_INTERVAL)
        last = d
    return date.fromisoformat(last) + timedelta(days=interval), interval


# A problem gets a review clock of its own, the drill clock's (SM-2), and
# only when an attempt at it went badly: a FAILED file, any assist, or a move
# the judge marked struggled. A problem solved cleanly unaided the first time
# never gets a card - its moves are the node's job, and 486 carriers on a
# clock would be the whole session.
#
# Until 2026-09-09 nothing in the picker read how a problem itself went.
# Every re-serve was node-driven (a stale move's latest carrier, a deep-stale
# repeat, unhold), so a node that went SOLID on some other carrier left the
# problem that actually beat you untouched: 36 of the 56 problems with a bad
# attempt had never been solved cleanly since, 227 and 207 among them.
#
# The grades are the drill clock's, which is the point: only an unaided
# all-clean rep is Good, so the help that put the problem on the list can
# never be what takes it off. The schedule is shorter than a bank file's,
# because a card here is a debt and not a lifetime: Again puts the problem
# 3 days out, Hard (a hinted clean rep - the answer is partly his) drifts it
# 1.2x further, and Good retires the card. The node curve carries it from
# there; a later bad attempt opens a new one.
#
# 3 days, where a bank file graduates at 1. A drill is three minutes - copy
# today, rote tomorrow. A problem is seventeen, and a next-morning rep on one
# whose solution was on the screen yesterday grades Good for the wrong reason
# and retires a debt that was never paid.
PROBLEM_GRADUATING_DAYS = 3


def attempt_label(fname, rec):
    """What happened on one attempt at a problem: failed, struggled, the
    assist level, clean, or unmapped when the judge found no move in it (a
    trivial solve is not a struggle, and grades nothing either way)."""
    if "FAILED" in fname:
        return "failed"
    moves = rec.get("moves") or {}
    if not moves:
        return "unmapped"
    if any(v != "clean" for v in moves.values()):
        return "struggled"
    level = assist_of(rec)
    return "clean" if level == "none" else level


# What opens a card: help, or walking away. A struggled move on an otherwise
# unaided solve does not - the judge's verdict already shrinks that node's
# stability, which is the node curve doing its job, and 52 such problems from
# autumn 2025 would sit ahead of this week's on any overdue-first order. Once
# a card IS open a struggle still fails it: the rep it waits for is clean.
OPENS_CARD = ("failed", "learning", "walkthrough", "hint")


def problem_grade(fname, rec):
    """good / hard / again for one attempt, or None when it grades nothing.
    Same bar as anki_answer, plus the FAILED file the drill clock never
    sees."""
    return {"clean": "good", "hint": "hard", "unmapped": None}.get(
        attempt_label(fname, rec), "again"
    )


def problem_attempts(pnum, evidence):
    """[(date str, fname, rec)] for a problem, oldest first."""
    return sorted(
        ev_index(evidence).by_problem.get(str(pnum)) or [], key=lambda t: (t[0], t[1])
    )


def problem_due(pnum, evidence):
    """(due date, interval days) for a problem's own review clock, or None
    when it has no card. One grade per day (the day's last attempt, as a bank
    file's clock takes it): help or a walk-away opens the card (OPENS_CARD),
    a hinted clean rep pushes it out, an unaided clean rep retires it, and
    anything else while it is open resets it."""
    by_day = {}
    for d, fname, rec in problem_attempts(pnum, evidence):
        if problem_grade(fname, rec) is not None:
            by_day[d] = (fname, rec)
    interval, last = 0, None
    for d in sorted(by_day):
        answer = problem_grade(*by_day[d])
        if interval == 0 and attempt_label(*by_day[d]) not in OPENS_CARD:
            continue
        if answer == "good":
            interval, last = 0, None  # the rep it was waiting for
        elif answer == "hard":
            interval = (
                PROBLEM_GRADUATING_DAYS
                if interval == 0
                else max(interval + 1, int(interval * ANKI_HARD_FACTOR + 0.5))
            )
            last = d
        else:
            interval, last = PROBLEM_GRADUATING_DAYS, d
    if last is None:
        return None
    return date.fromisoformat(last) + timedelta(days=interval), interval


def due_problems(evidence, today=None, problems=None):
    """[(pnum, due date, interval)] for every problem whose review clock is
    due, most overdue first. With `problems`, only the ones that table
    carries - the picker has to be able to show a walk."""
    day = today or date.today()
    out = []
    for pnum in ev_index(evidence).by_problem:
        if not pnum[:1].isdigit() or (problems is not None and pnum not in problems):
            continue
        d = problem_due(pnum, evidence)
        if d and d[0] <= day:
            out.append((pnum, d[0], d[1]))
    out.sort(key=lambda t: (t[1], pnum_key(t[0])))
    return out


def last_attempt(pnum, evidence):
    """(date, label) of the latest graded attempt at a problem, or None."""
    for d, fname, rec in reversed(problem_attempts(pnum, evidence)):
        if problem_grade(fname, rec) is not None:
            return date.fromisoformat(d), attempt_label(fname, rec)
    return None


def anki_rank(path, evidence, today=None, depth=0):
    """The sort key of a bank file due on its own clock today, or None
    when it is not due (a file done today is not due). A file with reps
    sorts by its due date, most overdue first. A file never done sorts
    after every review, by the depth of its node (atoms before
    compositions) and then by how many drills it comes after."""
    day = today or date.today()
    if last_drilled(path, evidence) >= day.isoformat():
        return None
    d = anki_due(path, evidence)
    if d is None:
        return (1, date.min, depth, len(drill_after(path)), path)
    if d[0] > day:
        return None
    return (0, d[0], 0, 0, path)


def anki_frontier(evidence, today=None, nodes=None, node_ids=None, assisted=False):
    """Every bank file due on its own clock, as (path, node id): reviews
    most overdue first, then files never done, atoms first. A due file
    whose "after" chain holds a due drill comes after it, whatever the
    dates and however many drills that are not due sit between them: the
    atom is served before the drill built on it (2026-09-06, Bundle
    Refunds a day ahead of Tape Reader under it; 2026-09-10, How Many
    Companies ahead of Find Roots two drills up). No hold and no
    node status withholds a due file; the daily group cap (group_caps) is
    applied by the picker, not here. The clock outranks
    everything (2026-09-06: 92 files in the bank, 33 never served and 25
    served once and never again, after a month of pick rules that each
    ranked something above the return of a drill). With `assisted`, only
    files whose latest rep was assisted."""
    day = today or date.today()
    if nodes is None:
        nodes = load_nodes()
    ranked = []
    for node in sorted(nodes if node_ids is None else node_ids):
        depth = len(input_tree([node], nodes)) if node in nodes else 0
        for path in bank_paths(node):
            if assisted and not drill_assisted(path, evidence):
                continue
            key = anki_rank(path, evidence, day, depth)
            if key is not None:
                ranked.append((key, path, node))
    ranked.sort()
    due = {path: node for _, path, node in ranked}
    out, seen = [], set()

    def emit(path):
        if path in seen:
            return
        seen.add(path)
        for a in drill_after(path):
            emit(drill_path(a))
        if path in due:
            out.append((path, due[path]))

    for _, path, _ in ranked:
        emit(path)
    return out


def due_drill(node_id, evidence, today=None, early=False, assisted=False):
    """Least-recently-drilled RELEASED bank file for a node, or None if the
    bank is empty or that file was already drilled today. The no-carrier
    fallback: a gap node with no READY carrier gets its drill offered instead
    of being silently skipped — a drill cannot be dodged and needs no
    carrier. With `early`, the curve is ignored: a SOLID, owned node still
    gets its next drill (the cram review, `make next sql cram early`); the
    "after" holds and the once-a-day rule still apply. With `assisted`, only
    drills whose latest rep was assisted are candidates (`make next sql
    assisted`): the holds are moot, since a drill with a rep was already
    servable, and the curve is off as under `early`."""
    day = today or date.today()
    status, _ = node_status(node_id, evidence, day)
    if drill_scheduler() == "anki":
        # the file's own clock (anki_rank) first, whatever the node's
        # status and whatever holds on the file: a due drill is served.
        # With nothing due on the clock, a node that is not SOLID still
        # trains on its bank (the drill gate), below.
        ranked = anki_frontier(
            evidence, day, nodes={}, node_ids=[node_id], assisted=assisted
        )
        if ranked:
            return ranked[0][0]
    # the graduating floor (graduation_due) asks for a non-first unaided
    # rep; a move carried by drills alone (every sql node) has nowhere
    # else to land one, so it was due at its floor forever once each drill
    # had been done once (kg_simulate, 2026-09-06: twenty sql nodes 45-60
    # days). At the floor the bank is served again.
    g = graduation_due(
        node_id, evidence, carrier_counts(_problems_ro()).get(node_id, 0)
    )
    at_floor = bool(g) and g[0] <= day
    holds = (
        status == SOLID
        and owned(node_id, evidence)
        and not early
        and not assisted
        and not drills_left(node_id, evidence)
        and not at_floor
    )
    # the curve says the node holds - a drill is a problem we authored, and
    # problems are not re-served while warm. A never-done drill of the node
    # is still due: one clean drill does not stand for the others
    # (2026-08-31, Pairs clean released the dedupe drill with subsets
    # undone). So is a drill whose latest rep was assisted: the node reads
    # owned (a first rep scores as unaided at the node level) while the
    # drill is not warm, and everything "after" it stays held until its
    # unaided rep, which nothing else serves (2026-09-06, Install Order
    # behind Shake Hands for 23 starved days).
    today = (today or date.today()).isoformat()
    candidates = bank_paths(node_id)
    if assisted or holds:
        candidates = [p for p in candidates if drill_assisted(p, evidence)]
    if not candidates:
        return None
    pool = (
        candidates
        if assisted
        else servable_drills(candidates, evidence, node_id, early=early)
    )
    if not pool:
        return None  # every bank file is held behind an id not yet warm
    path = min(pool, key=lambda p: last_drilled(p, evidence))
    return None if last_drilled(path, evidence) >= today else path


def drills_left(node_id, evidence, early=False):
    """True while a drill of this node has never been done and serving this
    node can still get there: it is servable and untouched, or everything
    it waits on is a drill of this same node that serving this node can
    reach in turn. A drill held by another node not being owned, or (at
    any depth) by a drill of another node, does not count - nothing this
    node serves would clear it, and a hold nothing can open is a deadlock
    (the 2026-08-31 Combinations serve: done once with a walkthrough, so
    Reuse Allowed and Subsets stayed held, the node read done, and the
    dedupe drill got served with subsets never done)."""
    candidates = bank_paths(node_id)
    problems = _problems_ro()
    by_id = {drill_id(p): p for p in candidates}
    reachable = set(servable_drills(candidates, evidence, node_id, early=early))
    grew = True
    while (
        grew
    ):  # a drill is reachable when all its unmet holds are reachable drills of this node
        grew = False
        for path in candidates:
            if path in reachable:
                continue
            if any(not owned(t, evidence) for t in drill_trains(path) if t != node_id):
                continue
            unmet = [
                a
                for a in drill_after(path)
                if warm(a, problems, evidence, early=early) is False
            ]
            if all(a in by_id and by_id[a] in reachable for a in unmet):
                reachable.add(path)
                grew = True
    return any(not last_drilled(path, evidence) for path in reachable)


# Sleep is derived from git, never stored: a parked problem IS its
# `<num>-slept` branch, `sleeping:` / `woke:` marker commits on it carry
# the timestamps. A park sleeps until `make wake` — no timers, no
# readiness trigger, nothing auto-wakes (settled 2026-08-28).


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
        if any(
            d >= slept_day for d, _, _ in ev_index(evidence).by_problem.get(pnum, ())
        ):
            continue
        recs[pnum] = {
            "branch": branch,
            "title": problems[pnum]["title"],
            "slept": ts,
            "cycles": max(len(marks), 1),
        }
    return recs


def claude_json(prompt, system_prompt, model="sonnet", retries=2):
    """One non-interactive claude call; returns parsed JSON from the result
    text. A reply that is not JSON (haiku, now and then) is asked again, up
    to `retries` more times: the detached judge has no operator to re-run it."""
    for attempt in range(retries + 1):
        try:
            return _claude_json_once(prompt, system_prompt, model)
        except ValueError:
            if attempt == retries:
                raise


def _claude_json_once(prompt, system_prompt, model):
    proc = subprocess.run(
        [
            "claude",
            "-p",
            prompt,
            "--system-prompt",
            system_prompt,
            "--model",
            model,
            "--output-format",
            "json",
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
# utils/rs/kg_mock) and the README's P(pass) history chart. The Rust port keeps
# this exact math (same RNG stream, same float-op order); change them together.
#
# One problem's odds come from the cold-solve model kg_curve fits (curve.json
# "solve"): the problem's contest rating, the walk's summed log recall, and its
# count of never-met moves, each with a fitted coefficient. Nothing here is
# per-difficulty any more - the Easy/Medium/Hard label only says which pool a
# problem is drawn from, which is a fact about the interview, not about him.


# ---- the skill state ---------------------------------------------------------
# Standard Elo over the scored games, K=32 from 1200, problems priced by their
# contest rating (an unrated one takes the median of its difficulty). This is
# the model's only channel for getting BETTER as opposed to knowing more: it
# moves when he outperforms the ratings he was served and not otherwise, so a
# forecast built on it can rise without anyone assuming that it will.

ELO_K, ELO_START = 32.0, 1200.0


# ---- timed attempts, as scored games ----------------------------------------
# One game per solve, scored on a contest clock: a win is clean and unaided
# inside the budget for the problem's difficulty, a draw is a hint inside it,
# a loss is anything else - a fail, a solve over budget, or a rep that needed
# the walkthrough or the answer. A solve the judge marked as meeting the
# follow-up is a harder problem than its label and plays on the next tier's
# clock. A solve whose time was never recorded is missing data, not a loss,
# so it is skipped.
# kg_readme elo rates these games, kg_curve fits P(solve) on them.


def carrier_counts(problems):
    """move -> how many evidenced problems walk it (problems.json primary
    walks). The rehearsal mass of a walk is the count of its rarest move."""
    counts: dict[str, int] = {}
    for p in problems.values():
        for m in p.get("moves", []):
            counts[m] = counts.get(m, 0) + 1
    return counts


# --- the replay clock (utils/rs/kg_movie) ----------------------------------
# Python mirror of kg_movie's pacing, bit-for-bit: ticks run from the day
# before the first evidence entry to the last one, each day's screen time is
# its unique leetcode solve count + LULL_WEIGHT (long solve-less stretches
# fast-forward), and the loop closes with a dissolve. Every animated SVG that
# wants to play in sync with kg_movie.svg / kg_pass.svg builds its keyTimes
# from this. Change the pacing here and in utils/rs/kg_movie/src/main.rs together.
