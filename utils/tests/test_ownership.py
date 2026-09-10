"""Degree of ownership (kg_lib.node_axes): the graded axis under the four
status labels. Status says whether the curve predicts recall today; degree
is the weaker of that memory and breadth, the distinct real problems the
move was executed on unaided at its carry bar. These tests pin the axes
down on synthetic evidence under the flat 42-day window (no curve file),
so nothing here reads graph/*.json."""

from datetime import date, timedelta

import pytest

from kg import kg_lib
from kg.kg_lib import (
    FRAGILE,
    MISSING,
    SOLID,
    STALE,
    breadth_score,
    mature,
    node_axes,
    node_degree,
    node_eval,
    proven_carriers,
)


@pytest.fixture(autouse=True)
def _flat_window(monkeypatch):
    monkeypatch.setattr(kg_lib, "_load_curve", lambda: None)
    # memos keyed by id(dict): a fresh dict can reuse a freed id
    kg_lib._CARRY_KINDS.clear()
    kg_lib._EV_INDEX.clear()


def iso(days):
    return (date.today() - timedelta(days=days)).isoformat()


def problem(moves, difficulty="Medium"):
    return {
        "title": f"synthetic {difficulty}",
        "difficulty": difficulty,
        "moves": list(moves),
    }


def solve(pnum, moves, days_ago=1, assist=None):
    rec = {"date": iso(days_ago), "problem": str(pnum), "moves": dict(moves)}
    if assist:
        rec["assist"] = assist
    return {f"solved/p{pnum}_{days_ago}.py": rec}


def drill(name, moves, days_ago=1, assist=None):
    rec = {"date": iso(days_ago), "problem": "drill", "moves": dict(moves)}
    if assist:
        rec["assist"] = assist
    return {f"solved/d_{name}_{days_ago}.py": rec}


def evidence(*records):
    out = {}
    for r in records:
        out.update(r)
    return out


# one Medium carries n, so its bar is ("medium", 2)
BANK = {
    "1": problem(["n"]),
    "2": problem(["n"]),
    "3": problem(["n"]),
    "4": problem(["n"]),
    "5": problem(["n"], "Easy"),
}


# --- the axes -------------------------------------------------------------


def test_a_missing_node_has_degree_zero():
    ax = node_axes("n", {}, BANK)
    assert (ax.status, ax.memory, ax.carriers, ax.breadth, ax.degree) == (
        MISSING,
        0.0,
        0,
        0.0,
        0.0,
    )


def test_assisted_reps_give_no_breadth():
    ev = evidence(solve("1", {"n": "clean"}, assist={"n": "hint"}))
    ax = node_axes("n", ev, BANK)
    assert ax.status == SOLID
    assert (ax.carriers, ax.breadth, ax.degree) == (0, 0.0, 0.0)


def test_a_drill_only_node_reads_a_quarter():
    ev = evidence(drill("A", {"n": "clean"}, 10), drill("A", {"n": "clean"}, 3))
    ax = node_axes("n", ev, BANK)
    assert (ax.status, ax.memory) == (SOLID, 1.0)
    assert (ax.carriers, ax.breadth, ax.degree) == (0, 0.25, 0.25)


@pytest.mark.parametrize("k, breadth", [(1, 0.5), (2, 0.75), (3, 1.0), (4, 1.0)])
def test_each_distinct_carrier_adds_a_quarter_up_to_three(k, breadth):
    ev = evidence(
        *(
            solve(p, {"n": "clean"}, days_ago=i + 1)
            for i, p in enumerate(("1", "2", "3", "4")[:k])
        )
    )
    ax = node_axes("n", ev, BANK)
    assert (ax.carriers, ax.breadth, ax.degree) == (min(k, 4), breadth, breadth)


def test_a_second_rep_of_the_same_problem_is_not_breadth():
    ev = evidence(solve("1", {"n": "clean"}, 20), solve("1", {"n": "clean"}, 2))
    ax = node_axes("n", ev, BANK)
    assert (ax.carriers, ax.breadth) == (1, 0.5)


def test_an_easy_rep_does_not_count_at_a_medium_bar():
    ev = evidence(solve("5", {"n": "clean"}, 2))
    ax = node_axes("n", ev, BANK)
    assert (ax.carriers, ax.breadth) == (0, 0.25)
    easy_bank = {"5": problem(["n"], "Easy")}  # only easies carry n: bar ("real", 1)
    kg_lib._CARRY_KINDS.clear()
    assert node_axes("n", ev, easy_bank).breadth == 0.5


def test_a_node_no_real_problem_carries_has_nothing_to_prove():
    hard_only = {"9": problem(["n"], "Hard")}
    ev = evidence(drill("A", {"n": "clean"}, 3))
    assert node_axes("n", ev, hard_only).breadth == 1.0
    assert node_axes("n", {}, hard_only).breadth == 0.0


def test_degree_is_the_weaker_axis():
    three = [
        solve(p, {"n": "clean"}, days_ago=d)
        for p, d in (("1", 60), ("2", 55), ("3", 50))
    ]
    stale = node_axes("n", evidence(*three), BANK)
    assert (stale.status, stale.breadth, stale.degree) == (STALE, 1.0, 0.0)
    fragile = node_axes("n", evidence(*three, solve("4", {"n": "struggled"}, 1)), BANK)
    assert (fragile.status, fragile.degree) == (FRAGILE, 0.0)
    assert (
        node_degree("n", evidence(*three, solve("4", {"n": "clean"}, 1)), BANK) == 1.0
    )


def test_breadth_score_table():
    bar = ("medium", 2)
    assert breadth_score(0, bar, any_unaided=False) == 0.0
    assert [breadth_score(k, bar, True) for k in range(5)] == [
        0.25,
        0.5,
        0.75,
        1.0,
        1.0,
    ]
    assert breadth_score(0, ("none", 0), True) == 1.0


def test_node_eval_keeps_its_three_tuple():
    ev = evidence(solve("1", {"n": "clean"}, 2))
    assert node_eval("n", ev) == (SOLID, date.today() - timedelta(days=2), 1.0)


# --- maturity counts distinct problems ------------------------------------


def test_two_reps_of_one_medium_do_not_mature_a_node():
    ev = evidence(solve("1", {"n": "clean"}, 20), solve("1", {"n": "clean"}, 2))
    assert proven_carriers("n", ev, BANK) == {"1"}
    assert not mature("n", ev, BANK)


def test_two_distinct_mediums_spaced_apart_do():
    ev = evidence(solve("1", {"n": "clean"}, 20), solve("2", {"n": "clean"}, 2))
    assert proven_carriers("n", ev, BANK) == {"1", "2"}
    assert mature("n", ev, BANK)


def test_proven_carriers_can_be_held_to_unaided():
    ev = evidence(
        solve("1", {"n": "clean"}, 20),
        solve("2", {"n": "clean"}, 2, assist={"n": "walkthrough"}),
    )
    assert proven_carriers("n", ev, BANK) == {"1", "2"}
    assert proven_carriers("n", ev, BANK, unaided=True) == {"1"}
