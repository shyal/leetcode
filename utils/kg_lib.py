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
