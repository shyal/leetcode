# kg_lib — shared helpers for the technique graph (graph/*.json).
#
# Mastery is DERIVED here at query time from evidence dates, never stored:
#   SOLID   clean evidence within SOLID_WINDOW_DAYS, no more-recent struggle
#   STALE   clean evidence exists, but older than the window
#   FRAGILE most recent evidence is struggled/avoided, or struggles only
#   MISSING no evidence at all

import glob
import json
import math
import os
import re
import subprocess
import sys
import time
from collections import namedtuple
from datetime import date, datetime, timedelta, timezone
from typing import Any

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


def rs_bin(name):
    """The Rust binary `name` of the utils/rs workspace (built by `make`,
    which every target that runs one depends on)."""
    return os.path.join(RS_BIN, name)


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
#   learning    the solution was given and copied - no recall happened
ASSIST_LEVELS = ("none", "hint", "walkthrough", "learning")
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
    out = {
        m: v
        for m, v in raw.items()
        if m in moves and v in ASSIST_WEIGHT and v != "none"
    }
    return out or None


_ASSIST_WORDS = [
    ("learning", re.compile(r"\blearning\b", re.I)),
    ("walkthrough", re.compile(r"\bwalk(?:ed|s)?[ -]?through\b|\bwalkthrough\b", re.I)),
    ("hint", re.compile(r"\bhint(?:ed|s)?\b", re.I)),
]


def notes_assist_level(notes):
    """The heaviest assist level the candidate's own notes name, or "none".

    The judge is told to read assist from the notes, and it does - mostly.
    On 2026-09-01 a drill whose notes read "Asked for a walkthrough." was
    filed with no assist at all. The candidate will not type an
    `ASSIST: <level>` line to make the model look; the level word in plain
    prose is the mark. So the word is authoritative and this function is
    what reads it, deterministically, before the judge's answer is stored."""
    found = [lvl for lvl, rx in _ASSIST_WORDS if rx.search(notes or "")]
    return max(found, key=ASSIST_WEIGHT.__getitem__) if found else "none"


def apply_assist_floor(assist, level, targets):
    """Raise the assist on each target move to at least `level`. `assist` is
    the stored shape (dict or None); the result is the stored shape too."""
    if level == "none" or not targets:
        return assist
    out = dict(assist or {})
    for m in targets:
        if ASSIST_WEIGHT[out.get(m, "none")] < ASSIST_WEIGHT[level]:
            out[m] = level
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


def load_all_problems():
    """graph/problems.json: every problem the graph knows, drafted and
    evidenced in one table. Gates read this one - a drafted problem waits
    behind its "after" list exactly like an evidenced one."""
    return _load("problems.json")["problems"]


def load_problems():
    """The evidenced problems: a solve mapped the walk, so the entry has
    "moves" and no "draft" flag. Everything that reasons from evidenced
    walks - carriers, carrier counts, node status - reads this view."""
    return {k: v for k, v in load_all_problems().items() if not v.get("draft")}


def load_evidence():
    return _load("evidence.json")["evidence"]


def load_predicted():
    """The drafted walks, keyed by problem: every entry carrying "walks",
    drafted or already evidenced. The entries are the table's own, so a
    drafted problem's "after" travels with its walks."""
    return {k: v for k, v in load_all_problems().items() if v.get("walks")}


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
    reach = np.array(
        [statuses[n][0] == SOLID and n not in immature for n in dm.node_ids], dtype=bool
    )
    gaps = (dm.W & ~reach).sum(1) + dm.unknown
    live = dm.live_problems(problems)
    in_reach = np.zeros(len(dm.problems), dtype=bool)
    np.logical_or.at(in_reach, dm.prob[~dm.missing & (gaps == 0)], True)
    sel = (
        ~dm.missing
        & (gaps == 1)
        & (dm.unknown == 0)
        & live[dm.prob]
        & ~in_reach[dm.prob]
    )
    if not sel.any():
        return {}
    blocker = (dm.W[sel] & ~reach).argmax(1)
    pairs = np.unique(np.stack([dm.prob[sel], blocker], 1), axis=0)
    counts = np.bincount(pairs[:, 1], minlength=len(dm.node_ids))
    return {dm.node_ids[i]: int(c) for i, c in enumerate(counts) if c}


class _DraftMatrix:
    """The drafted walks as arrays, built once per (predicted, node set):
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
        self.problems: list = []
        rows, prob, missing, unknown = [], [], [], []
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
        self._live: tuple[Any, Any] = (None, None)
        self._counts: tuple[Any, Any] = (None, None)

    def live_problems(self, problems):
        """Boolean per problem: not in problems.json (unsolved, unmapped)."""
        import numpy as np

        key = (id(problems), len(problems))
        if self._live[0] != key:
            self._live = (
                key,
                np.array([n not in problems for n in self.problems], dtype=bool),
            )
        return self._live[1]

    def carrier_counts(self, problems):
        """Per node: evidenced problems carrying it (predicted_carrier's
        rehearsal mass), as a vector over node_ids."""
        import numpy as np

        key = (id(problems), len(problems))
        if self._counts[0] != key:
            counts: dict[str, int] = {}
            for p in problems.values():
                for m in p.get("moves", []):
                    counts[m] = counts.get(m, 0) + 1
            self._counts = (
                key,
                np.array([counts.get(n, 0) for n in self.node_ids], dtype=float),
            )
        return self._counts[1]


_DRAFT_MATRIX: dict = {}


def _dict_key(d):
    """Memo key for a dict that may be rebuilt: id() alone is recycled
    across short-lived dicts (the picker tests build one per test and a
    stale matrix served the wrong catalog, 2026-09-01). Small dicts are
    keyed by content, the real 3000-problem catalog by id and size."""
    return (id(d), tuple(sorted(d)) if len(d) < 256 else len(d))


def _draft_matrix(predicted, node_ids):
    key = (_dict_key(predicted), tuple(sorted(node_ids)))
    dm = _DRAFT_MATRIX.get(key)
    if dm is None:
        if len(_DRAFT_MATRIX) > 8:
            _DRAFT_MATRIX.clear()
        dm = _DRAFT_MATRIX[key] = _DraftMatrix(predicted, sorted(node_ids))
    return dm


def save_problems(problems):
    """Write these entries into graph/problems.json, leaving every entry the
    caller did not pass - the drafts - as it is. An entry keeps what the
    file already said and the caller did not: its drafted walks, its "after"
    gate, a "banned" flag. It loses the "draft" flag the moment a solve
    gives it "moves"."""
    path = os.path.join(GRAPH_DIR, "problems.json")
    with open(path) as f:
        data = json.load(f)
    table = data["problems"]
    for num, entry in problems.items():
        entry = {**table.get(num, {}), **entry}
        if entry.get("moves"):
            entry.pop("draft", None)
        table[num] = entry
    with open(path, "w") as f:
        json.dump(data, f, indent=1)


def save_evidence(evidence):
    path = os.path.join(GRAPH_DIR, "evidence.json")
    with open(path) as f:
        data = json.load(f)
    data["evidence"] = evidence
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ---- the judge queue -----------------------------------------------------------
# `make solved` no longer waits for the judge (settled 2026-09-06: a median
# 38s, up to 3 minutes, per drill). The file phase writes a PLACEHOLDER
# entry - the rep exists, its moves are the drill's TRAINS (or the
# problem's canonical walk) marked clean, assist read from the notes - and
# flags it "pending". A detached kg_extract judges the file and replaces the
# entry. The flag is the queue: anything pending is unjudged, whatever
# happened to the worker, and `make next` respawns it when it is stale.
# Two writers (a worker landing, the next solve's placeholder) share
# evidence.json, so every write reloads the file under this lock.
PENDING = "pending"
PENDING_STALE_SECONDS = 600


class evidence_lock:
    """Exclusive lock on graph/evidence.json for a load-modify-save."""

    def __enter__(self):
        import fcntl

        self._f = open(os.path.join(GRAPH_DIR, ".evidence.lock"), "w")
        fcntl.flock(self._f, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        import fcntl

        fcntl.flock(self._f, fcntl.LOCK_UN)
        self._f.close()
        return False


def store_evidence_entry(path, entry):
    """Set ONE entry and save, against the file as it is NOW (not as it was
    when the caller loaded it): a worker that judged for a minute must not
    clobber the placeholder the next `make solved` wrote meanwhile. Returns
    the fresh evidence dict."""
    with evidence_lock():
        evidence = load_evidence()
        evidence[path] = entry
        save_evidence(evidence)
    return evidence


def pending_judgements(evidence):
    """[(path, seconds since the placeholder was written)], oldest first."""
    now = time.time()
    out = []
    for path, e in evidence.items():
        stamp = e.get(PENDING)
        if not stamp:
            continue
        try:
            age = now - datetime.fromisoformat(stamp).timestamp()
        except (TypeError, ValueError):
            age = float("inf")
        out.append((path, age))
    return sorted(out, key=lambda t: -t[1])


def spawn_judge(path):
    """Detach one kg_extract (utils/rs/kg_extract) on this file: it judges,
    folds, refits the curve, and commits the graph files by path onto
    whatever branch is checked out when it finishes. Output goes to
    .judge.log (gitignored). Returns the Popen; nothing waits on it."""
    root = os.path.dirname(GRAPH_DIR)
    log = open(os.path.join(root, ".judge.log"), "a")
    return subprocess.Popen(
        [rs_bin("kg_extract"), "--file", path, "--commit"],
        cwd=root,
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


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


_EV_INDEX: dict = {}  # id(evidence) -> _EvidenceIndex


def ev_index(evidence):
    """The _EvidenceIndex of this evidence dict. Reused while the dict is
    the same object and has only grown at the end since the last call;
    rebuilt otherwise."""
    from itertools import islice

    idx = _EV_INDEX.get(id(evidence))
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

    A learning solve is not recall evidence at all — it neither counts as a
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


DEEP_STALE_DAYS = (
    2 * SOLID_WINDOW_DAYS
)  # beyond this, a "re-solve" plays like a new problem
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


def degree_track(nodes, evidence, problems, clock):
    """node -> [degree per tick of `clock` (kg_lib.MovieClock)], each tick
    node_axes() over the evidence recorded up to that day against today's
    bank. The one replay every animated chart colours its nodes from."""
    by_date = sorted(evidence.items(), key=lambda kv: kv[1]["date"])
    seen, k = {}, 0
    track: dict[str, list] = {nid: [] for nid in nodes}
    for i in range(clock.n_ticks):
        day = clock.first + timedelta(days=i)
        while k < len(by_date) and by_date[k][1]["date"] <= day.isoformat():
            seen[by_date[k][0]] = by_date[k][1]
            k += 1
        for nid in nodes:
            track[nid].append(round(node_axes(nid, seen, problems, day).degree, 2))
    return track


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

DEGREE_LEGEND = (0.0, 0.25, 0.5, 0.75, 1.0)  # the swatches every chart's legend shows


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


def immature_nodes(nodes, evidence, problems):
    """The nodes mature() rejects — precomputed once per run so route_gaps
    and rank_summits stay pure sort keys. One pass over the bank and one
    over the evidence, whatever the node count."""
    from itertools import islice

    key = (id(evidence), id(problems), tuple(nodes))
    idx = ev_index(evidence)
    kinds = _carry_kinds(problems)

    def young(n):
        clean = [
            (d, str(rec.get("problem", "")))
            for d, v, a, _, rec in idx.by_node.get(n, ())
            if v == "clean" and a != "learning"
        ]
        return not _mature_from(clean, _bar_of(kinds.get(n, set())), problems)

    memo = _IMMATURE
    if (
        memo.get("key") == key
        and memo["n"] <= len(evidence)
        and memo["n_pr"] <= len(problems)
    ):
        # records and problems appended since: only the nodes they touch
        # can have changed (a problem changes carry bars for its moves)
        touched = set()
        for _, rec in islice(evidence.items(), memo["n"], None):
            touched.update(rec.get("moves", {}))
        for p in islice(problems.values(), memo["n_pr"], None):
            touched.update(p.get("moves", []))
            for w in p.get("alt_walks", []):
                touched.update(w)
        out: Any = set(memo["out"])
        for n in touched & memo["nodes"]:
            out.discard(n)
            if young(n):
                out.add(n)
        out = frozenset(out)
    else:
        out = frozenset(n for n in nodes if young(n))
    memo.update(key=key, n=len(evidence), n_pr=len(problems), out=out, nodes=set(nodes))
    return out


_IMMATURE: dict = {}  # memo: maturity changes only with the evidence or the bank


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
        if not any(
            all(m in nodes for m in walk)
            and all(statuses[m][0] == SOLID for m in walk if m != target)
            for walk in walks
        ):
            continue
        if held_behind(pnum, problems, evidence):
            continue
        found.append(pnum)
    return found


_WALKS_CARRYING: dict = {}


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
        if (
            not str(pnum)[:1].isdigit()
            or unservable(pnum, p)
            or p.get("difficulty") == "Hard"
        ):
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
    release is on ownership: the unaided rep is what releases."""
    dates = [
        d
        for d, _, r in ev_index(evidence).by_problem.get(str(pnum), ())
        if r.get("moves")
        and all(v == "clean" for v in r["moves"].values())
        and assist_of(r) == "none"
    ]
    return max(dates) if dates else ""


def held_behind(pnum, problems, evidence, today=None):
    """The predecessor this problem must wait for, or None.

    A problem may declare "after": [ids] - what its own solution builds on
    (47 is 46's loop plus the dedup rule; 713 is the Count by Contribution
    drill plus a product). An id is a problem number, a drill title, or a
    node id; `warm` says whether it is owned. While one is not, this
    problem stays out of carrier pools so the predecessor is served first.
    Drafted problems are gated the same way: the "after" list is read from
    the table the caller holds, or from graph/problems.json when the caller
    holds the evidenced view alone.
    A banned problem, or an id nothing in the graph carries, holds nothing:
    a hold nothing can clear is a deadlock.
    """
    today = today or date.today()
    entry = problems.get(str(pnum)) or _problems_ro().get(str(pnum), {})
    for pred in entry.get("after", []):
        pred = str(pred)
        if unservable(pred, problems.get(pred) or _problems_ro().get(pred, {})):
            continue
        if warm(pred, problems, evidence, today) is False:
            return pred
    for node in dict.fromkeys(walk_nodes(entry)):
        held = node_drill_hold(node, evidence, today)
        if held:
            return held
    return None


def gates(vid, problems, drill_map=None):
    """The vertices held behind `vid`: every problem number and drill id
    whose "after" list names it, problems first in number order, then
    drills in id order. The reverse of the one relation."""
    vid = str(vid)
    drill_map = drills() if drill_map is None else drill_map
    held = sorted(
        (k for k, p in problems.items() if vid in map(str, p.get("after", []))),
        key=pnum_key,
    )
    held += sorted(
        (i for i, d in drill_map.items() if vid in map(str, d.get("after", []))),
        key=pnum_key,
    )
    return held


def vertex_status(vid, problems, evidence, today=None):
    """A status word for a problem or drill vertex, the way a node has one:
    SOLID when warm, STALE when it has a rep that is not, MISSING when it
    has never been done. What the unlabeled drawing shows for what a
    served item gates."""
    if warm(vid, problems, evidence, today):
        return SOLID
    kind = vertex_kind(vid, problems)
    if kind == "problem" and ev_index(evidence).by_problem.get(str(vid)):
        return STALE
    if kind == "drill" and latest_drill_rep(drill_path(vid), evidence) is not None:
        return STALE
    return MISSING


def dependents(vid, problems, evidence, drill_map=None, today=None):
    """What `vid` gates, as rows to act on: for each problem or drill whose
    "after" names it - id, title, kind (difficulty or "drill"), status
    (vertex_status), and `held_by`: the other ids in its "after" list that
    are not warm yet, so "done with d26, what can i do now" reads straight
    off the list. Problems first in number order, then drills."""
    vid = str(vid)
    drill_map = drills() if drill_map is None else drill_map
    rows = []
    for h in gates(vid, problems, drill_map):
        if h in problems:
            p = problems[h]
            title = p["title"]
            kind = problem_difficulty(h, problems) or "?"
            after = p.get("after", [])
        else:
            d = drill_map[h]
            title, kind, after = d["title"], "drill", d.get("after", [])
        held = [
            str(a)
            for a in after
            if str(a) != vid and warm(a, problems, evidence, today) is False
        ]
        rows.append(
            {
                "id": h,
                "title": title,
                "kind": kind,
                "status": vertex_status(h, problems, evidence, today),
                "held_by": held,
            }
        )
    return rows


DIFFICULTY_RANK = {"drill": 0, "Easy": 1, "Medium": 2, "Hard": 3}


def easiest_first(rows):
    """Dependent rows (see `dependents`) in the order to prepare them:
    drills, then Easy, Medium, Hard; inside a kind the higher community
    acceptance first. Drills go first for a second reason: the drill
    picker refuses a non-empty current.py, so they must be cut before a
    problem's stub lands there."""
    return sorted(
        rows,
        key=lambda r: (
            DIFFICULTY_RANK.get(r["kind"], 9),
            -acceptance(r["id"]),
            pnum_key(r["id"]),
        ),
    )


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
    return any(
        target not in walk for walk in problems.get(pnum, {}).get("alt_walks", [])
    )


def clear_branch(name):
    """True when no local branch `name` blocks a fresh checkout -b: either
    none exists, or the user was asked and chose to delete it. Without a
    TTY the branch is kept, never silently deleted."""
    if subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "refs/heads/" + name],
        capture_output=True,
    ).returncode:
        return True
    last = subprocess.run(
        ["git", "log", "-1", "--format=%s (%cs)", name], capture_output=True, text=True
    ).stdout.strip()
    if sys.stdin.isatty():
        ans = input(f"branch '{name}' already exists - {last}. Delete it? [y/N] ")
        if ans.strip().lower() in ("y", "yes"):
            subprocess.run(
                ["git", "branch", "-D", name], check=True, capture_output=True
            )
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
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=root
    ).stdout.strip()
    cache = os.path.join(root, ".solvetimes_cache.json")
    try:
        with open(cache) as f:
            data = json.load(f)
        if data.get("head") == head:
            reps = [
                (k, date.fromisoformat(d), secs, f) for k, d, secs, f in data["reps"]
            ]
            return reps if with_file else [r[:3] for r in reps]
    except (OSError, ValueError, KeyError, TypeError):
        pass
    reps = _mine_solve_times(root)
    try:
        with open(cache, "w") as f:
            json.dump(
                {
                    "head": head,
                    "reps": [(k, d.isoformat(), secs, fn) for k, d, secs, fn in reps],
                },
                f,
            )
    except OSError:
        pass
    return reps if with_file else [r[:3] for r in reps]


def _mine_solve_times(root):
    """mined_solve_times without the cache: the git log itself. Slow (a
    tenth of a second per call), so the result is cached per HEAD commit
    in .solvetimes_cache.json - every solve is a commit, so the cache is
    exactly as fresh as the history."""
    out = subprocess.run(
        [
            "git",
            "log",
            "--diff-filter=A",
            "--format=%x01%at%x01%B%x02",
            "--name-only",
            "--",
            "solved/",
        ],
        capture_output=True,
        text=True,
        cwd=root,
    ).stdout
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
            reps.append(
                (
                    key,
                    datetime.fromtimestamp(int(at)).date(),
                    secs,
                    f"solved/{added[0]}",
                )
            )
    return sorted(reps, key=lambda r: r[1])


FORECAST_WARM_DAYS = 30


def drill_forecast(path, today=None):
    """(expect_min, hint_min, bail_min) for serving a bank drill file, from
    the mined history — same shape as solve_forecast. First-time drills fall
    back to the median first-attempt time across all timed drills."""
    import math
    from statistics import median

    today = today or date.today()
    reps = mined_solve_times()
    if not reps:
        return None
    key = f"d:{drill_solved_stem(path)}"
    by_key: dict[str, list] = {}
    for k, d, secs in reps:
        by_key.setdefault(k, []).append((d, secs))
    mine = by_key.get(key)
    if mine:
        ratios: dict[bool, list] = {True: [], False: []}
        for rs in by_key.values():
            for (d0, s0), (d1, s1) in zip(rs, rs[1:]):
                ratios[(d1 - d0).days <= FORECAST_WARM_DAYS].append(math.log2(s1 / s0))
        d0, s0 = mine[-1]
        warm = (today - d0).days <= FORECAST_WARM_DAYS
        r = median(ratios[warm]) if ratios[warm] else 0.0
        base = s0 / 60 * 2**r
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
    by_key: dict[str, list] = {}
    for key, d, secs in reps:
        by_key.setdefault(key, []).append((d, secs))

    mine = by_key.get(str(pnum))
    if mine:
        ratios: dict[bool, list] = {True: [], False: []}
        for rs in by_key.values():
            for (d0, s0), (d1, s1) in zip(rs, rs[1:]):
                ratios[(d1 - d0).days <= FORECAST_WARM_DAYS].append(math.log2(s1 / s0))
        d0, s0 = mine[-1]
        warm = (today - d0).days <= FORECAST_WARM_DAYS
        r = median(ratios[warm]) if ratios[warm] else 0.0
        base = s0 / 60 * 2**r
    else:
        conn = node_conn(problems)
        my = problems.get(str(pnum), {})
        if not my.get("moves"):
            return None

        def mean_conn(p):
            mv = p.get("moves", [])
            return sum(conn.get(m, 0.0) for m in mv) / len(mv) if mv else 0.0

        firsts = [
            (mean_conn(problems[k]), rs[0][1] / 60)
            for k, rs in by_key.items()
            if k in problems
            and problems[k].get("difficulty") == my.get("difficulty")
            and problems[k].get("moves")
        ]
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

    counts: dict[str, int] = {}
    for p in problems.values():
        for m in p.get("moves", []):
            counts[m] = counts.get(m, 0) + 1
    return {n: math.log2(1 + c) for n, c in counts.items()}


def carriers_for(target, problems, statuses, nodes, evidence):
    """Problems containing the target move whose every OTHER move is SOLID.
    Banned and paid-only problems are never offered (kg_lib.unservable).
    Hards are summits, never refresh carriers — rusty moves get their reps
    at basecamps (easies/mediums); a Hard is attempted only all-green.
    A problem declaring "after" waits until its predecessor is warm
    (held_behind), so 46 is served before 47."""
    found = []
    for pnum, p in problems.items():
        moves = p.get("moves", [])
        if (
            unservable(pnum, p)
            or p.get("difficulty") == "Hard"
            or target not in moves
            or not all(m in nodes for m in moves)
        ):
            continue
        if all(
            statuses[m][0] == SOLID for m in moves if m != target
        ) and not held_behind(pnum, problems, evidence):
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


def predicted_carrier(
    target,
    problems,
    statuses,
    nodes,
    predicted=None,
    evidence=None,
    skip=(),
    difficulties=("Easy", "Medium"),
):
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
    proving rep for a medium-bar node has to be a Medium. A draft held
    behind an unmet "after" is not promoted, the hold an evidenced carrier
    obeys."""
    import numpy as np

    if predicted is None:
        predicted = load_predicted()
    if evidence is None:
        evidence = _evidence_ro()
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
        if held_behind(num, predicted, evidence):
            continue
        best.append((num, dm.walk_moves[wi], diff, min(int(m), CONN_MASS_CAP)))
    if not best:
        return None
    best.sort(
        key=lambda t: (
            DIFF_RANK.get(t[2], 1),
            -t[3],
            (len(input_tree(t[1], nodes)), len(t[1])),
            -acceptance(t[0]),
            pnum_key(t[0]),
        )
    )
    num, moves, diff, _ = best[0]
    title = predicted[num].get("title") or _metadata().get(str(num), {}).get(
        "title", f"problem {num}"
    )
    return num, {
        "title": title,
        "difficulty": diff,
        "moves": list(moves),
        "predicted": True,
    }


def drafted_in_reach(
    problems,
    statuses,
    nodes,
    immature,
    predicted=None,
    evidence=None,
    skip=(),
    first="Hard",
    limit=20,
):
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
    medium pass rate starved). A draft held behind an unmet "after" waits,
    the hold an evidenced problem obeys."""
    import numpy as np

    if predicted is None:
        predicted = load_predicted()
    if evidence is None:
        evidence = _evidence_ro()
    dm = _draft_matrix(predicted, list(nodes))
    reach = np.array(
        [statuses[n][0] == SOLID and n not in immature for n in dm.node_ids], dtype=bool
    )
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
        if num in skip or held_behind(num, predicted, evidence):
            continue
        out.append(
            (
                num,
                {
                    "title": predicted[num].get("title")
                    or meta.get(str(num), {}).get("title", f"problem {num}"),
                    "difficulty": dm.diff[probs[i]],
                    "moves": list(dm.walk_moves[walks[i]]),
                    "predicted": True,
                },
            )
        )
        if len(out) >= limit:
            break
    return out


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
    scored = [
        (route_gaps(p, problems, nodes, statuses, immature)[1:], pnum_key(p), p)
        for p in candidates
        if p in problems
    ]
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


def has_drill_bank(node_id):
    """True when drills/<node-id>/ holds at least one bank file."""
    return bool(glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py")))


_NODE_DRILL_HOLD: dict = {}


def bank_files(node_id):
    """The bank files of a node, in filename order. Cached: the holds below
    ask for them on every candidate of every pick."""
    key = (DRILLS_DIR, node_id)
    hit = _BANK_FILES.get(key)
    if hit is None:
        hit = _BANK_FILES[key] = sorted(
            glob.glob(os.path.join(DRILLS_DIR, node_id, "*.py"))
        )
    return hit


def cold_drill(node_id, evidence, today=None, ready_only=False):
    """The bank file of this node that is not warm yet - the one a rep is
    owed on - or None when every drill of the node is warm. Servable files
    (servable_drills) come first; with `ready_only` an unservable one is not
    named at all, which is what a caller about to SERVE the file wants: a
    drill still waiting on its own "after" is reached by climbing that
    chain, not by serving it."""
    day = today or date.today()
    key = (DRILLS_DIR, node_id, id(evidence), len(evidence), day)
    hit = _NODE_DRILL_HOLD.get(key)
    if hit is None:
        cold = [p for p in bank_files(node_id) if not drill_warm(p, evidence, day)]
        ready = servable_drills(cold, evidence, node_id) if cold else []
        hit = _NODE_DRILL_HOLD[key] = (ready, cold)
    ready, cold = hit
    if ready_only:
        return ready[0] if ready else None
    return (ready or cold)[0] if cold else None


def node_drill_hold(node_id, evidence, today=None):
    """The drill of this node that is not warm yet, or None. A node with a
    bank hands its problems to the bank first: while one of its drills has
    no unaided all-clean rep inside the solid window, every problem walking
    the node waits for that drill. This is the hand-written "after" applied
    to the whole node - the drill trains the move, so it gates every problem
    that walks it, drafted or evidenced, not the few listed by hand. The
    picker clears the hold by serving that drill (kg_next.due)."""
    path = cold_drill(node_id, evidence, today)
    return drill_id(path) if path else None


def walk_nodes(entry):
    """Every node a problem's solution might walk: the evidenced walk and its
    alt walks, or the moves of each drafted walk. What the drill holds read."""
    out = list(entry.get("moves", []))
    for alt in entry.get("alt_walks", []):
        out += list(alt)
    for w in entry.get("walks", []):
        out += list(w.get("moves", []))
    return out


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


def drill_held(node_id, nodes, statuses, evidence, has_bank=None, pending=()):
    """The cross-bank hold: True while a prereq of node_id must train
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
        if (
            has_bank(p)
            and p in statuses
            and (
                statuses[p][0] != SOLID
                or not owned(p, evidence)
                or drills_left(p, evidence)
            )
        ):
            return True  # rusty, not owned, or drills of its own still undone
    return False


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


def _evidence_ro():
    """graph/evidence.json for READ-ONLY use, parsed once per file version.
    The gate checks in the predicted rules need evidence to say whether a
    predecessor is warm, and their callers do not all carry it."""
    path = os.path.join(GRAPH_DIR, "evidence.json")
    st = os.stat(path)
    hit = _EVIDENCE_RO.get(path)
    if hit is None or hit[0] != st.st_mtime_ns or hit[1] != st.st_size:
        hit = (st.st_mtime_ns, st.st_size, load_evidence())
        _EVIDENCE_RO.clear()
        _EVIDENCE_RO[path] = hit
    return hit[2]


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


def drill_recall(path, evidence, today=None):
    """Predicted recall for one bank file, from that file's own history.

    node_recall answers "can he recall this move today", pooling every
    carrier and every representation of it. In front of a drill that is the
    wrong question. On 2026-09-08 two-sequence-align was SOLID on four LCS
    solves written as recursion over delete distance, while the drill asking
    for the bottom-up table had one rep, a copy, the day before; the node
    badge promised something the file could not deliver. So the fitted curve
    is applied here to the file's own clean days, struggles and assistance,
    and the number in front of him is about the thing he is about to type.

    (recall, clean days, gap days, copy days). Before the file's first
    unaided clean rep there is no recall to predict and `recall` is None,
    but the copy count and the gap still are, and they are what sets the
    expectation for that rep. None only when the file has no reps at all,
    or with no fitted curve, where recall is binary and a bar would lie.
    """
    import math

    curve = _load_curve()
    if not curve:
        return None
    key = f"d_{drill_solved_stem(path)}_".lower()
    reps = sorted(
        (t for t in ev_index(evidence).drills if t[1].startswith(key)),
        key=lambda t: t[:2],
    )
    if not reps:
        return None
    by_day = {}
    for d, _, rec in reps:
        by_day[d] = rec  # same-day reps are one rep: the last of the day grades it
    clean_days, struggles = [], 0
    for d, rec in by_day.items():
        moves = rec.get("moves") or {}
        if not moves:
            continue
        if all(v == "clean" for v in moves.values()):
            if assist_of(rec) != "learning":
                clean_days.append(d)
        else:
            struggles += 1
    copies = sum(1 for rec in by_day.values() if assist_of(rec) == "learning")
    if not clean_days:
        gap = max(((today or date.today()) - date.fromisoformat(max(by_day))).days, 0)
        return None, 0, gap, copies
    assisted = sum(ASSIST_WEIGHT[assist_of(rec)] for _, _, rec in reps)

    p = curve["params"]
    cmean = p.get("conn_mean", 0.0)
    conn = curve.get("conn", {})
    # the file's connectivity is its node's; a composite drill takes the
    # widest-carried move it combines, the one holding the rest up
    cn = max((conn[n] for n in drill_trains(path) if n in conn), default=cmean)
    stability = math.exp(
        p["a"]
        + p["b"] * math.log1p(len(clean_days))
        - p["c"] * struggles
        - p.get("d", 0.0) * assisted
        + p.get("e", 0.0) * (cn - cmean)
    )
    stability = min(max(stability, 7), 3650)  # sanity clamp, as in _node_curve
    gap = max(((today or date.today()) - date.fromisoformat(max(clean_days))).days, 0)
    memory = (1 + gap / stability) ** (-p["beta"])
    return (1 - p.get("slip", 0.0)) * memory, len(clean_days), gap, copies


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


def group_caps(environ=None):
    """Per-group daily caps from KG_GROUP_CAP, `sql=3` or `sql=3,graphs=2`
    (set in .envrc, read through load_envrc). A group at its cap is left
    out of the default frontier for the rest of the day: the graduating
    floor made drills persistent, and without a cap one bank can fill
    every session (2026-09-04, sql). An explicit `make next <group>` is
    the override and ignores the cap."""
    raw = (os.environ if environ is None else environ).get("KG_GROUP_CAP", "")
    caps = {}
    for part in raw.split(","):
        name, _, count = part.partition("=")
        if name.strip() and count.strip().isdigit():
            caps[name.strip()] = int(count)
    return caps


def new_drill_cap(environ=None):
    """How many bank files may be met for the first time in one day
    (MAX_NEW_DRILLS, set in .envrc), or None when there is no cap. The
    first rep of a drill is first exposure: it is read, copied and
    understood, and a session of them is a different day's work from a
    session of reviews. The group cap (group_caps) bounds one bank; this
    bounds the whole day, whatever the group and whatever the pick rule,
    so a bank with 30 files never served cannot be poured out at once.
    Reviews are never withheld by it."""
    raw = (os.environ if environ is None else environ).get("MAX_NEW_DRILLS", "").strip()
    return int(raw) if raw.isdigit() else None


def new_drills_today(evidence, day=None):
    """How many bank files were met for the first time today: reps dated
    today that are the first rep of their drill (ev_index.first_reps)."""
    day = (day or date.today()).isoformat()
    idx = ev_index(evidence)
    return sum(1 for fname, _ in idx.by_date.get(day, ()) if fname in idx.first_reps)


def new_drills_left(evidence, day=None, environ=None):
    """First exposures the day has left under MAX_NEW_DRILLS, or None when
    there is no cap. Zero means a never-drilled file waits until tomorrow;
    a file with a rep is a review and is served as usual."""
    cap = new_drill_cap(environ)
    return None if cap is None else cap - new_drills_today(evidence, day)


def reviews_first(environ=None):
    """Whether a problem on its own review clock (problem_due) is served
    ahead of the frontier (REVIEWS_FIRST=1 in .envrc). Off, the default,
    it sits under FRAGILE moves and graduating floors, and a floor rep is
    always on a fresh carrier: with 13 young moves on a due floor the 23
    due reviews never reached the top (2026-09-10). The drill clock and the
    sleep rules still come first."""
    raw = (os.environ if environ is None else environ).get("REVIEWS_FIRST", "").strip()
    return raw not in ("", "0")


def drill_review_cap(environ=None):
    """How many bank files already met may come back in one day
    (MAX_DRILL_REVIEWS, set in .envrc), or None when there is no cap. The
    other half of MAX_NEW_DRILLS: with 47 files due on the clock, a
    session is drills and nothing else, and the problems the drills exist
    for never get solved. Past the cap the clock waits and the picker
    falls through to its problem rules."""
    raw = (
        (os.environ if environ is None else environ)
        .get("MAX_DRILL_REVIEWS", "")
        .strip()
    )
    return int(raw) if raw.isdigit() else None


def drill_reviews_today(evidence, day=None):
    """How many bank files came back today: reps dated today of a drill
    that had been met before (a d_ record not in ev_index.first_reps)."""
    day = (day or date.today()).isoformat()
    idx = ev_index(evidence)
    return sum(
        1
        for fname, _ in idx.by_date.get(day, ())
        if drill_key(fname) is not None and fname not in idx.first_reps
    )


def drill_reviews_left(evidence, day=None, environ=None):
    """Reviews the day has left under MAX_DRILL_REVIEWS, or None when there
    is no cap. Zero means a file with a rep waits until tomorrow; a file
    never drilled is first exposure and answers to MAX_NEW_DRILLS."""
    cap = drill_review_cap(environ)
    return None if cap is None else cap - drill_reviews_today(evidence, day)


def drill_capped(path, evidence, day=None, environ=None):
    """True when the day's budget for this bank file is spent. A file never
    drilled is first exposure and spends MAX_NEW_DRILLS; a file with a rep
    is a review and spends MAX_DRILL_REVIEWS. Past its budget the file
    waits until tomorrow and the picker moves on - to the next due file,
    and with both budgets spent, to its problem rules. Unlike the group cap
    (group_caps) there is no override: the budgets are on the whole day,
    not on one bank, so naming a group or cramming it does not lift them."""
    left = (
        drill_reviews_left(evidence, day, environ)
        if last_drilled(path, evidence)
        else new_drills_left(evidence, day, environ)
    )
    return left is not None and left <= 0


def group_reps(group, nodes, evidence, day=None):
    """How many reps dated `day` (today) touched the group: a drill or a
    problem is one rep when its evidenced walk has a node of the group."""
    day = (day or date.today()).isoformat()
    return sum(
        1
        for _, rec in ev_index(evidence).by_date.get(day, ())
        if any(nodes.get(m, {}).get("group") == group for m in rec.get("moves", {}))
    )


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


def sleep_state(nodes, problems, evidence):
    """Split parked problems into (asleep, woken) problem-number lists.

    Every park is ASLEEP until the operator runs `make wake` — woken is
    always empty; nothing wakes a problem automatically. asleep is ordered
    most-reslept first, so the strongest not-ready signal gets its ground
    warmed first (kg_next rule 0)."""
    recs = sleep_records(problems, evidence)
    asleep = sorted(recs, key=lambda p: (-recs[p]["cycles"], recs[p]["slept"]))
    return asleep, []


def sleep_rows(nodes, problems, evidence, statuses=None):
    """The park, one row per parked problem: (pnum, title, ground, since,
    cycles). ground is the list of non-SOLID nodes under the problem (what
    the picker is warming for it), empty when its ground is solid. since
    is the last park time, ISO to the minute. Empty when nothing is
    parked."""
    recs = sleep_records(problems, evidence)
    if not recs:
        return []
    asleep, _ = sleep_state(nodes, problems, evidence)
    if statuses is None:
        statuses = {n: node_status(n, evidence) for n in nodes}
    rows = []
    for pnum in asleep:
        rec = recs[pnum]
        since = datetime.fromtimestamp(rec["slept"]).isoformat(timespec="minutes")
        rusty = sorted(
            n
            for n in input_tree(problems[pnum]["moves"], nodes)
            if statuses[n][0] != SOLID
        )
        rows.append((pnum, rec["title"], rusty, since, rec["cycles"]))
    return rows


def sleep_lines(nodes, problems, evidence, statuses=None):
    """The park, one line per parked problem: what it is, what the picker
    is warming for it (or that its ground is solid), when it was parked,
    how many times, and the wake command. Printed by `make sleep -- --list`;
    `make next` prints the same rows as a table at the bottom of every
    pick (2026-09-01: the daily reminder is the point - the operator wants
    the parked problems in view so they get thought about overnight).
    Empty when nothing is parked."""
    lines = []
    for pnum, title, rusty, since, cycles in sleep_rows(
        nodes, problems, evidence, statuses
    ):
        ground = f"warming: {', '.join(rusty)}" if rusty else "ground solid, simmering"
        slept = f", slept x{cycles}" if cycles > 1 else ""
        lines.append(
            f"{pnum}. {title} - asleep ({ground}) - parked "
            f"{since}{slept} - make wake {pnum} when you choose"
        )
    return lines


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


def solve_model(curve=None):
    """The fitted cold-solve coefficients, or None when curve.json predates
    the fit (in which case there is no pass model to run)."""
    curve = _load_curve() if curve is None else curve
    solve = (curve or {}).get("solve") or {}
    return solve.get("features") or None


def solve_logit(coef, rating, ln_recall, unseen):
    """The cold-solve model's linear predictor for one walk."""
    return (
        coef.get("intercept", 0.0)
        + coef.get("rating", 0.0) * (rating - 1500) / 400
        + coef.get("recall", 0.0) * ln_recall
        + coef.get("unseen", 0.0) * unseen
    )


def walk_terms(walk, node_recall):
    """(summed log recall of the moves already met, count of the rest)."""
    ln_recall, unseen = 0.0, 0
    for mv in walk:
        r = node_recall.get(mv)
        if r is None:
            unseen += 1
        else:
            ln_recall += math.log(max(r, 1e-3))
    return ln_recall, unseen


# ---- the skill state ---------------------------------------------------------
# Standard Elo over the scored games, K=32 from 1200, problems priced by their
# contest rating (an unrated one takes the median of its difficulty). This is
# the model's only channel for getting BETTER as opposed to knowing more: it
# moves when he outperforms the ratings he was served and not otherwise, so a
# forecast built on it can rise without anyone assuming that it will.

ELO_K, ELO_START = 32.0, 1200.0


def elo_games(evidence=None, ratings=None):
    """Every scored game with the Elo he carried INTO it and the rating of the
    problem: [{..., "rating", "elo_before"}], oldest first. Causal by
    construction - a game's elo_before sees only games before it."""
    games = scored_games(evidence)
    ratings = solve_ratings() if ratings is None else ratings
    by_dif: dict[str, list] = {}
    for g in games:
        r = ratings.get(g["problem"])
        if r is not None:
            by_dif.setdefault(g["difficulty"], []).append(r)
    median = {d: sorted(v)[len(v) // 2] for d, v in by_dif.items()}
    elo = ELO_START
    out = []
    for g in games:
        r = ratings.get(g["problem"], median.get(g["difficulty"]))
        if r is None:
            continue
        g = dict(g, rating=r, elo_before=elo)
        elo += ELO_K * (g["score"] - 1 / (1 + 10 ** ((r - elo) / 400)))
        out.append(g)
    return out


def elo_now(evidence=None, ratings=None):
    """His Elo after the last scored game, or the starting rating."""
    games = elo_games(evidence, ratings)
    if not games:
        return ELO_START
    last = games[-1]
    return last["elo_before"] + ELO_K * (
        last["score"] - 1 / (1 + 10 ** ((last["rating"] - last["elo_before"]) / 400))
    )


def elo_drift(evidence=None, ratings=None, window=None):
    """(points per day, its standard error): least squares of Elo on calendar
    day over the games in `window` days, all of them by default. The forward
    simulation advances the skill state by this and nothing else - a measured
    drift, near zero today, rather than an assumed climb."""
    games = elo_games(evidence, ratings)
    if window:
        cutoff = date.today() - timedelta(days=window)
        games = [g for g in games if date.fromisoformat(g["date"]) >= cutoff]
    if len(games) < 30:
        return 0.0, 0.0
    x = [
        (date.fromisoformat(g["date"]) - date.fromisoformat(games[0]["date"])).days
        for g in games
    ]
    y = [g["elo_before"] for g in games]
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    if sxx == 0:
        return 0.0, 0.0
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sxx
    resid = [b - (my + slope * (a - mx)) for a, b in zip(x, y)]
    s2 = sum(r * r for r in resid) / max(n - 2, 1)
    return slope, math.sqrt(s2 / sxx)


def problem_solve_p(pnum, problems, node_recall, coef=None, ratings=None):
    """The cold-solve model's odds on one real problem: its best evidenced
    walk under solve_logit, with the problem's contest rating. None when the
    problem has no walk, no rating, or the model is unfitted - callers order
    on what they have and leave the rest where they were."""
    coef = solve_model() if coef is None else coef
    ratings = solve_ratings() if ratings is None else ratings
    rating = (ratings or {}).get(str(pnum))
    walk = problems.get(str(pnum), {}).get("moves")
    if not coef or rating is None or not walk:
        return None
    ln_recall, unseen = walk_terms(walk, node_recall)
    return 1 / (1 + math.exp(-solve_logit(coef, rating, ln_recall, unseen)))


def solve_ratings():
    """Problem number -> contest rating (utils/kg/clist.py); empty without the
    cache, which leaves every rating-aware sort inert."""
    try:
        from kg import clist

        return clist.combined_ratings()
    except (ImportError, SystemExit, OSError):
        return {}


def target_pass_rate():
    """The central pass rate a milestone has to reach for "ready". Which
    onsite he is aiming at is a choice, not a measurement, so it lives in
    .envrc as TARGET_PASS_RATE (a fraction); kg_mock reads the same variable.
    """
    try:
        v = float(os.environ.get("TARGET_PASS_RATE", "") or 0.5)
    except ValueError:
        return 0.5
    return v if 0.0 < v < 1.0 else 0.5


# ---- timed attempts, as scored games ----------------------------------------
# One game per solve, scored on a contest clock: a win is clean and unaided
# inside the budget for the problem's difficulty, a draw is a hint inside it,
# a loss is anything else - a fail, a solve over budget, or a rep that needed
# the walkthrough or the answer. A solve the judge marked as meeting the
# follow-up is a harder problem than its label and plays on the next tier's
# clock. A solve whose time was never recorded is missing data, not a loss,
# so it is skipped.
# kg_elo_svg rates these games, kg_curve fits P(solve) on them.

BUDGET_MIN = {"Easy": 10, "Medium": 25, "Hard": 45}
NEXT_TIER = {"Easy": "Medium", "Medium": "Hard", "Hard": "Hard"}


def scored_games(evidence=None):
    """[{date, problem, difficulty, score, file, moves}] oldest first."""
    evidence = load_evidence() if evidence is None else evidence
    problems = load_problems()
    secs = {fn: s for _, _, s, fn in mined_solve_times(with_file=True)}
    out = []
    for fname in sorted(evidence, key=lambda k: (evidence[k]["date"], k)):
        rec = evidence[fname]
        pnum = str(rec.get("problem", ""))
        diff = problem_difficulty(pnum, problems)
        if not pnum[:1].isdigit() or diff not in BUDGET_MIN:
            continue
        level = assist_of(rec)
        if "FAILED" in fname or level in ("walkthrough", "learning"):
            score = 0.0
        elif fname not in secs:
            continue
        elif (
            secs[fname]
            > BUDGET_MIN[NEXT_TIER[diff] if rec.get("followup") == "solved" else diff]
            * 60
        ):
            score = 0.0
        else:
            score = 0.5 if level == "hint" else 1.0
        out.append(
            {
                "date": rec["date"],
                "problem": pnum,
                "difficulty": diff,
                "score": score,
                "file": fname,
                "moves": list(rec.get("moves") or {}),
            }
        )
    return out


def carrier_counts(problems):
    """move -> how many evidenced problems walk it (problems.json primary
    walks). The rehearsal mass of a walk is the count of its rarest move."""
    counts: dict[str, int] = {}
    for p in problems.values():
        for m in p.get("moves", []):
            counts[m] = counts.get(m, 0) + 1
    return counts


def walk_mass(walk, counts):
    """x = log(1 + mass) of a walk: mass is the carrier count of its rarest
    move; a move nothing evidenced carries (off-taxonomy) counts 0."""
    return math.log1p(min((counts.get(m, 0) for m in walk), default=0))


def pass_rates(node_recall, pools, ratings, coef, rng, n_mc=20000, shift=0.0):
    """(full clear, onsite 2E+2M+>=1H, screen both-M, single-hard P).

    pools: {"E"/"M"/"H": [problem, ...]}, each problem a list of walks, each
    walk a list of move names - real problems (evidenced + drafted walks, the
    Rust Bank), not fabricated ones. ratings: the same shape, one contest
    rating per problem. A problem is drawn uniformly from its difficulty pool
    and scored by its BEST walk under the cold-solve model; `shift` moves the
    fitted intercept for the scenario band. Same draw order as the Rust port
    (randrange then random), so the RNG streams match."""
    full = onsite = screen = h_solved = 0
    for _ in range(n_mc):
        solved = {"E": 0, "M": 0, "H": 0}
        for dif in ("E", "E", "M", "M", "H", "H"):
            i = rng.randrange(len(pools[dif]))
            best = None
            for walk in pools[dif][i]:
                ln_recall, unseen = walk_terms(walk, node_recall)
                z = solve_logit(coef, ratings[dif][i], ln_recall, unseen)
                if best is None or z > best:
                    best = z
            p = 1 / (1 + math.exp(-(best + shift)))
            solved[dif] += rng.random() < p
        full += solved["E"] == 2 and solved["M"] == 2 and solved["H"] == 2
        onsite += solved["E"] == 2 and solved["M"] == 2 and solved["H"] >= 1
        screen += solved["M"] == 2
        h_solved += solved["H"]
    return full / n_mc, onsite / n_mc, screen / n_mc, h_solved / (2 * n_mc)


def solve_scenarios(curve=None, days=0):
    """The scenario band as a logit shift, from two measured uncertainties:
    the fitted intercept's standard error (today's), and, `days` into a
    projection, the standard error of the Elo drift compounded over them. So
    the band is tight today and widens with the horizon, which is the honest
    shape - and the central line moves only by the drift his games actually
    show. The old hand-set 0.75/0.85/0.95 recognition band said all of this
    with numbers nothing measured."""
    curve = _load_curve() if curve is None else curve
    solve = (curve or {}).get("solve") or {}
    se = solve.get("intercept_se") or 0.0
    centre = skill_shift(curve, days)
    lo, hi = skill_shift(curve, days, -1.96), skill_shift(curve, days, 1.96)
    return {
        "cautious": -1.96 * se + lo,
        "central": centre,
        "optimistic": 1.96 * se + hi,
    }


def retention_cycle(nodes=None, evidence=None, curve=None):
    """The median retention window across the graph: how long the typical move
    holds before the curve calls it due. One of these is a full turn of the
    picker's cycle - every typical node comes due and is repaired once - which
    is as far as a projection needs to run when its target is unreachable."""
    curve = _load_curve() if curve is None else curve
    if not curve:
        return SOLID_WINDOW_DAYS
    nodes = load_nodes() if nodes is None else nodes
    evidence = load_evidence() if evidence is None else evidence
    p = curve["params"]
    index = ev_index(evidence).by_node
    windows = []
    for nid in nodes:
        cleans = len({d for d, v, _, _, _ in index.get(nid, ()) if v == "clean"})
        s = min(max(math.exp(p["a"] + p["b"] * math.log1p(cleans)), 7), 3650)
        windows.append(s * (curve["target_retention"] ** (-1 / p["beta"]) - 1))
    return int(sorted(windows)[len(windows) // 2]) if windows else SOLID_WINDOW_DAYS


def skill_shift(curve=None, days=0, z=0.0):
    """The logit shift `days` of projected practice buys, from the measured
    Elo drift: a skill gain of D points is the same as every problem being D
    points easier, so the shift is -k_rating * D / 400. `z` walks the drift's
    own standard error. Zero drift, zero shift - the model never assumes a
    climb it has not measured."""
    curve = _load_curve() if curve is None else curve
    solve = (curve or {}).get("solve") or {}
    elo = solve.get("elo") or {}
    k_rating = (solve.get("features") or {}).get("rating", 0.0)
    drift = (elo.get("drift_per_day") or 0.0) + z * (elo.get("drift_se") or 0.0)
    return -k_rating * drift * days / 400.0


def current_recall(nodes, evidence, curve, today=None):
    """Predicted recall per node, for the nodes he has actually met. Pass
    `today` (and evidence filtered to entries on or before it) to replay a
    historical snapshot. A node with no clean rep behind it is left out
    entirely: the cold-solve model counts it as a never-met move rather than
    charging it an assumed recall."""
    today = today or date.today()
    out = {}
    for nid in nodes:
        r = node_curve_recall(nid, evidence, curve, today)
        if r is not None:
            out[nid] = r
    return out


def node_curve_recall(nid, evidence, curve, today=None):
    """One node of current_recall, or None when he has never had it clean."""
    import math

    today = today or date.today()
    p = curve["params"]
    status, last = node_status(nid, evidence, today=today)
    if status == MISSING or not last:
        return None
    cleans = len(
        {d for d, v, _, _, _ in ev_index(evidence).by_node.get(nid, ()) if v == "clean"}
    )  # distinct clean days, as in node_eval
    if not cleans:
        return None
    s = min(max(math.exp(p["a"] + p["b"] * math.log1p(cleans)), 7), 3650)
    return (1 + (today - last).days / s) ** (-p["beta"])


# --- the replay clock (utils/rs/kg_movie) ----------------------------------
# Python mirror of kg_movie's pacing, bit-for-bit: ticks run from the day
# before the first evidence entry to the last one, each day's screen time is
# its unique leetcode solve count + LULL_WEIGHT (long solve-less stretches
# fast-forward), and the loop closes with a dissolve. Every animated SVG that
# wants to play in sync with kg_movie.svg / kg_pass.svg builds its keyTimes
# from this. Change the pacing here and in utils/rs/kg_movie/src/main.rs together.

MOVIE_SECONDS = 10.0  # kg_movie's DEFAULT_SECONDS
MOVIE_END_FADE_S = 1.2  # loop-closing dissolve, capped by the fraction
MOVIE_FADE_FRACTION = 0.08
MOVIE_LULL_WEIGHT = 0.25  # screen time a solve-less day gets, in solves


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
            len(by_day[(self.first + timedelta(days=i)).isoformat()])
            + MOVIE_LULL_WEIGHT
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
        return (
            f'<rect width="{w}" height="{h}" fill="{fill}" opacity="0" pointer-events="none">'
            f'<animate attributeName="opacity" calcMode="linear" values="0;0;1" '
            f'keyTimes="0;{self.ticks_end:.4f};1" dur="{self.dur}s" repeatCount="indefinite"/></rect>'
        )


# era banner shared by the animated SVGs: the one flip that is the point of
# all of them. Mirrors kg_movie's ERA_SWITCH / labels / inks.
ERA_SWITCH = date(2026, 8, 7)
ERA_PRE_LABEL = "pre graph scheduling era"
ERA_GRAPH_LABEL = "graph scheduling era"
ERA_PRE_INK = "#8b949e"
ERA_GRAPH_INK = "#58a6ff"


def era_banner(clock, x, y, size, anchor="start", halo=None):
    """Two <text> layers flipping grey -> blue on the switch date's tick;
    non-SMIL viewers see today's era. halo outlines the text in a background
    color for banners placed over chart ink."""
    halo_attr = (
        (
            f' stroke="{halo}" stroke-width="{max(size // 7, 3)}" '
            f'paint-order="stroke" stroke-linejoin="round"'
        )
        if halo
        else ""
    )
    common = f'y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="bold"'
    if not (clock.first < ERA_SWITCH <= clock.last):
        label, ink = (
            (ERA_PRE_LABEL, ERA_PRE_INK)
            if clock.last < ERA_SWITCH
            else (ERA_GRAPH_LABEL, ERA_GRAPH_INK)
        )
        return [f'<text x="{x}" {common} fill="{ink}"{halo_attr}>{label}</text>']
    f = clock.frac((ERA_SWITCH - clock.first).days)
    out = []
    for label, ink, vals, init in (
        (ERA_PRE_LABEL, ERA_PRE_INK, "1;0", 0),
        (ERA_GRAPH_LABEL, ERA_GRAPH_INK, "0;1", 1),
    ):
        out.append(
            f'<text x="{x}" {common} fill="{ink}"{halo_attr} opacity="{init}">{label}'
            f'<animate attributeName="opacity" calcMode="discrete" values="{vals}" '
            f'keyTimes="0;{f:.4f}" dur="{clock.dur}s" repeatCount="indefinite"/></text>'
        )
    return out


def drill_ids_by_key():
    """drill_key of a solved d_ file -> the drill's id (d61), for every bank
    drill drills.json names. A rep of a drill the bank no longer carries has
    no entry."""
    out: dict[str, str] = {}
    for did in drills():
        path = drill_path(did)
        if path:
            out.setdefault(f"d_{drill_solved_stem(path)}".lower(), did)
    return out


def exercises_by_day(evidence):
    """date -> [(label, [moves])] in within-day order of the solved
    timestamps: a problem's number, or a drill's id ("drill" for a rep of a
    drill the bank no longer names). The first of a same-day re-solve only.
    The replays (kg_3d, kg_full) read this for their solve labels."""
    ids = drill_ids_by_key()
    by_day: dict[str, list] = {}
    for fname, rec in evidence.items():
        p = rec.get("problem", "")
        if p[:1].isdigit():
            label = p
        elif p == "drill":
            label = ids.get(drill_key(fname), "drill")
        else:
            continue
        m = re.search(r"\d{4}_\d{2}_\d{2}T[\d_]+", fname)
        by_day.setdefault(rec["date"], []).append(
            (m.group(0) if m else "", label, list(rec.get("moves", {})))
        )
    out = {}
    for day, rows in by_day.items():
        seen, ordered = set(), []
        for _, label, moves in sorted(rows):
            if label not in seen:
                seen.add(label)
                ordered.append((label, moves))
        out[day] = ordered
    return out
