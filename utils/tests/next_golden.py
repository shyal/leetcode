# The Python side of the `make next` golden diff: every library value
# `kg_next --golden-json` (utils/rs/kg_next) prints, computed by kg_lib
# and kg_next in-process and printed as the same JSON. Run as a subprocess
# by utils/tests/test_next_parity.py under the same environment as the
# Rust binary (KG_TODAY, the .envrc knobs), never imported under pytest,
# whose conftest strips those knobs.
#
#   PYTHONPATH=utils KG_TODAY=2026-09-11 .venv/bin/python3 utils/tests/next_golden.py

import json
import os
from datetime import date
from importlib.machinery import SourceFileLoader
from typing import Any

from kg import kg_lib
from kg import recognition as rc

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KG = os.path.join(ROOT, "utils", "kg")


def _round(x):
    return f"{x:.12e}"


def _date(d):
    return d.isoformat() if d else None


def _entry(promo):
    return [promo[0], promo[1]["title"], promo[1]["difficulty"], promo[1]["moves"]]


def node_rows(nodes, problems, evidence, statuses, immature, day):
    unl = kg_lib.unlocks(statuses, problems)
    gain = kg_lib.unlocks(statuses, problems, immature=immature)
    carr = kg_lib.carrier_counts(problems)
    out = {}
    for n in nodes:
        status, last, recall, memory = kg_lib._node_curve(n, evidence, day)
        ax = kg_lib.node_axes(n, evidence, problems, day)
        grad = kg_lib.graduation_due(n, evidence, carr.get(n, 0))
        promo = kg_lib.predicted_carrier(
            n, problems, statuses, nodes, evidence=evidence
        )
        lc = kg_lib.latest_carrier(n, evidence)
        out[n] = {
            "status": status,
            "last": _date(last),
            "recall": _round(recall),
            "memory": _round(memory),
            "carriers": ax.carriers,
            "breadth": _round(ax.breadth),
            "degree": _round(ax.degree),
            "immature": n in immature,
            "owned": kg_lib.owned(n, evidence),
            "graduation_due": [grad[0].isoformat(), grad[1]] if grad else None,
            "has_bank": kg_lib.has_drill_bank(n),
            "drill_held": kg_lib.drill_held(n, nodes, statuses, evidence),
            "drill_gated": kg_lib.drill_gated(n, status, last, today=day),
            "drills_left": kg_lib.drills_left(n, evidence),
            "due_drill": kg_lib.due_drill(n, evidence, today=day),
            "cold_drill": kg_lib.cold_drill(n, evidence, today=day),
            "node_drill_hold": kg_lib.node_drill_hold(n, evidence, day),
            "carriers_for": kg_lib.carriers_for(n, problems, statuses, nodes, evidence),
            "proving_carriers": kg_lib.proving_carriers(
                n, problems, statuses, nodes, evidence
            ),
            "unlocks": unl.get(n, 0),
            "gain": gain.get(n, 0),
            "latest_carrier": [lc[0].isoformat(), lc[1], lc[2]] if lc else None,
            "predicted_carrier": _entry(promo) if promo else None,
        }
    return out


def problem_rows(nodes, problems, evidence, day):
    ratings = kg_lib.solve_ratings()
    out = {}
    for pnum, p in problems.items():
        due = kg_lib.problem_due(pnum, evidence)
        la = kg_lib.last_attempt(pnum, evidence)
        fc = kg_lib.solve_forecast(pnum, problems, day)
        r = ratings.get(pnum)
        tier, size = kg_lib.gentleness(pnum, problems, nodes)
        out[pnum] = {
            "last_solved": kg_lib.last_solved(pnum, evidence),
            "last_clean_solve": kg_lib.last_clean_solve(pnum, evidence),
            "held_behind": kg_lib.held_behind(pnum, problems, evidence, day),
            "problem_due": [due[0].isoformat(), due[1]] if due else None,
            "last_attempt": [la[0].isoformat(), la[1]] if la else None,
            "cooled": kg_lib.cooled(pnum, evidence),
            "tree_size": list(kg_lib.tree_size(pnum, problems, nodes)),
            "gentleness": [tier, list(size)],
            "forecast": [_round(v) for v in fc] if fc else None,
            "rating": _round(r) if r is not None else None,
            "warm": kg_lib.warm(pnum, problems, evidence, day),
            "vertex_status": kg_lib.vertex_status(pnum, problems, evidence, day),
            "difficulty": p.get("difficulty", ""),
        }
    return out


def drill_rows(nodes, evidence, day):
    out = {}
    for n in nodes:
        for path in kg_lib.bank_paths(n):
            due = kg_lib.anki_due(path, evidence)
            rec = kg_lib.drill_recall(path, evidence, day)
            fc = kg_lib.drill_forecast(path, day)
            out[path] = {
                "title": kg_lib.drill_title(path),
                "id": kg_lib.drill_id(path),
                "stem": kg_lib.drill_solved_stem(path),
                "trains": kg_lib.drill_trains(path),
                "after": kg_lib.drill_after(path),
                "last_drilled": kg_lib.last_drilled(path, evidence),
                "anki_due": [due[0].isoformat(), due[1]] if due else None,
                "warm": bool(kg_lib.drill_warm(path, evidence, day)),
                "clean": kg_lib.drill_clean(path, evidence),
                "assisted": kg_lib.drill_assisted(path, evidence),
                "capped": kg_lib.drill_capped(path, evidence, day),
                "recall": (
                    [_round(rec[0]) if rec[0] is not None else None, *rec[1:]]
                    if rec
                    else None
                ),
                "forecast": [_round(v) for v in fc] if fc else None,
            }
    return out


def scenario_picks(kg_next, nodes, evidence, statuses, asleep, groups):
    scenarios = {
        "default": dict(asleep=asleep),
        "session_start": dict(asleep=asleep, session_start=True),
        "no_asleep": dict(),
    }
    for g in groups:
        scenarios[f"group_{g}"] = dict(asleep=asleep, group=g)
        scenarios[f"group_{g}_cram"] = dict(asleep=asleep, group=g, cram=True)
        scenarios[f"group_{g}_early"] = dict(asleep=asleep, group=g, early=True)
        scenarios[f"group_{g}_assisted"] = dict(asleep=asleep, group=g, assisted=True)
    out = {}
    for name, kw in scenarios.items():
        problems = kg_lib.load_problems()  # a fresh view: picks promote drafts
        exclude: set = set()
        picks: list[Any] = []
        for _ in range(3):
            choice = kg_next.pick(
                nodes, problems, evidence, statuses, exclude=exclude, **kw
            )
            if choice is None:
                picks.append(None)
                break
            picks.append(list(choice))
            exclude.add(choice[2])
        out[name] = picks
    return out


def compute():
    kg_next = SourceFileLoader(
        "kg_next_golden", os.path.join(KG, "kg_next")
    ).load_module()
    day = date.fromisoformat(os.environ["KG_TODAY"])
    kg_next.freeze(day)
    nodes = kg_lib.load_nodes()
    problems = kg_lib.load_problems()
    evidence = kg_lib.load_evidence()
    statuses = {n: kg_lib.node_status(n, evidence, day) for n in nodes}
    immature = kg_lib.immature_nodes(nodes, evidence, problems)
    asleep, _ = kg_lib.sleep_state(nodes, problems, evidence)
    recog = rc.derived(rc.load_recognition(), evidence, problems, statuses)
    groups = sorted({n.get("group") for n in nodes.values()} - {None})
    spot = rc.due_spot(
        nodes, problems, evidence, recog, statuses, today=day, skip=set(asleep)
    )
    ahead = kg_next.review_ahead(
        nodes, problems, evidence, asleep=asleep, exclude=kg_next.solved_today_pnums()
    )
    return {
        "today": day.isoformat(),
        "nodes": node_rows(nodes, problems, evidence, statuses, immature, day),
        "problems": problem_rows(nodes, problems, evidence, day),
        "drills": drill_rows(nodes, evidence, day),
        "anki_frontier": [
            list(t) for t in kg_lib.anki_frontier(evidence, day, nodes=nodes)
        ],
        "due_problems": [
            [p, d.isoformat(), i]
            for p, d, i in kg_lib.due_problems(evidence, day, problems)
        ],
        "review_queue": [
            p for p, _, _ in kg_next.review_queue(evidence, problems, day)
        ],
        "asleep": asleep,
        "sleep_rows": [
            list(r) for r in kg_lib.sleep_rows(nodes, problems, evidence, statuses)
        ],
        "starved": [
            [n, k] for n, k in kg_next.starved(nodes, problems, evidence, day).items()
        ],
        "routed_around": [
            [n, p]
            for n, p in kg_next.routed_around(nodes, problems, evidence, day).items()
        ],
        "blocked_frontier": [
            list(b)
            for b in kg_next.blocked_frontier(
                nodes, problems, evidence, statuses, asleep, ()
            )
        ],
        "ready_hards": kg_next.ready_hards(problems, nodes, evidence, statuses),
        "parked_summits": kg_next.parked_summits(
            problems, nodes, evidence, statuses, asleep
        ),
        "unmapped_summits": kg_next.unmapped_summits(
            problems, nodes, evidence, statuses
        ),
        "drafted_in_reach_hard": [
            _entry(e)
            for e in kg_lib.drafted_in_reach(
                problems, statuses, nodes, immature, evidence=evidence, first="Hard"
            )
        ],
        "drafted_in_reach_medium": [
            _entry(e)
            for e in kg_lib.drafted_in_reach(
                problems, statuses, nodes, immature, evidence=evidence, first="Medium"
            )
        ],
        "trivial_easies": kg_next.trivial_easies(problems, nodes, evidence, statuses),
        "elo_now": _round(kg_lib.elo_now(evidence)),
        "solve_model": kg_lib.solve_model(),
        "ratings_count": len(kg_lib.solve_ratings()),
        "review_ahead": list(ahead),
        "upcoming": kg_next.upcoming(nodes, problems, evidence, 5, asleep=asleep),
        "scenarios": scenario_picks(kg_next, nodes, evidence, statuses, asleep, groups),
        "recognition": {
            n: [
                rc.recognition_status(n, recog, day)[0],
                _date(rc.recognition_status(n, recog, day)[1]),
            ]
            for n in nodes
        },
        "due_spot": list(spot) if spot else None,
        "solve_seconds_today": kg_next._iss().solve_seconds_today(),
        "solved_today": sorted(kg_next.solved_today_pnums()),
        "group_caps": [[g, c] for g, c in kg_lib.group_caps().items()],
        "group_reps": [
            [g, kg_lib.group_reps(g, nodes, evidence, day)] for g in kg_lib.group_caps()
        ],
    }


if __name__ == "__main__":
    print(json.dumps(compute()))
