# kg_lib — shared helpers for the technique graph (graph/*.json).
#
# Mastery is DERIVED here at query time from evidence dates, never stored:
#   SOLID   clean evidence within SOLID_WINDOW_DAYS, no more-recent struggle
#   STALE   clean evidence exists, but older than the window
#   FRAGILE most recent evidence is struggled/avoided, or struggles only
#   MISSING no evidence at all

import json
import os
import subprocess
from datetime import date, timedelta

GRAPH_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "graph")
SOLID_WINDOW_DAYS = 42

# For any model prompt that judges solve code: the repo's utils/sitecustomize.py
# mirrors LeetCode's judge, which preloads common imports (functools.reduce,
# collections, typing names, heapq, ...) before user code runs. Bare use of
# these names is valid in both environments.
HARNESS_ENV_NOTE = (
    "Environment: this code runs under a harness that (like LeetCode's judge) "
    "preloads common imports — reduce, collections, typing names, heapq, etc. "
    "Using such names without an import statement is VALID and NEVER a bug; "
    "never mention missing imports in verdicts or notes."
)

SOLID, STALE, FRAGILE, MISSING = "SOLID", "STALE", "FRAGILE", "MISSING"


def _load(name):
    with open(os.path.join(GRAPH_DIR, name)) as f:
        return json.load(f)


def load_nodes():
    return {n["id"]: n for n in _load("nodes.json")["nodes"]}


def load_problems():
    return _load("problems.json")["problems"]


def load_evidence():
    return _load("evidence.json")["evidence"]


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
    grows with clean reps and shrinks with struggles, SOLID while predicted
    recall >= the fitted target. Without a curve: flat SOLID_WINDOW_DAYS.
    """
    today = today or date.today()
    entries = []  # (date, verdict)
    for rec in evidence.values():
        verdict = rec.get("moves", {}).get(node_id)
        if verdict:
            entries.append((date.fromisoformat(rec["date"]), verdict))
    if not entries:
        return MISSING, None
    entries.sort()
    last_date, last_verdict = entries[-1]
    clean_dates = [d for d, v in entries if v == "clean"]
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
        struggles = sum(1 for _, v in entries if v == "struggled")
        stability = math.exp(p["a"] + p["b"] * cleans - p["c"] * struggles)
        stability = min(max(stability, 7), 3650)  # sanity clamp
        gap = (today - clean_dates[-1]).days
        if (1 + gap / stability) ** (-p["beta"]) >= curve["target_retention"]:
            return SOLID, clean_dates[-1]
        return STALE, clean_dates[-1]

    if today - clean_dates[-1] <= timedelta(days=SOLID_WINDOW_DAYS):
        return SOLID, clean_dates[-1]
    return STALE, clean_dates[-1]


DEEP_STALE_DAYS = 2 * SOLID_WINDOW_DAYS  # beyond this, a "re-solve" plays like a new problem


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
    """Problems containing the target move whose every OTHER move is SOLID."""
    found = []
    for pnum, p in problems.items():
        moves = p.get("moves", [])
        if target not in moves or not all(m in nodes for m in moves):
            continue
        if all(statuses[m][0] == SOLID for m in moves if m != target):
            found.append(pnum)
    return found


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
    # tolerate fences/preamble: parse the outermost {...} span
    text = result.strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"no JSON object in result: {text[:200]!r}")
    return json.loads(text[start : end + 1])


def taxonomy_summary(nodes):
    """Compact node list for prompts: id — desc."""
    return "\n".join(f"- {nid}: {n['desc']}" for nid, n in nodes.items())
