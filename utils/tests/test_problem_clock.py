"""The problem review clock (kg_lib.problem_due): a problem gets a card when
an attempt at it needed help or ended in walking away, and the card is retired
only by an unaided clean rep.

Everything else in the picker serves a MOVE and then finds a carrier for it,
so before this a problem that beat you was never asked again unless one of
its moves happened to go stale. These tests pin what opens a card, what
cannot close one, and the intervals.
"""
from datetime import date, timedelta

from kg.kg_lib import (OPENS_CARD, PROBLEM_GRADUATING_DAYS, ANKI_HARD_FACTOR,
                       attempt_label, due_problems, last_attempt, problem_due)


def iso(days):
    return (date.today() - timedelta(days=days)).isoformat()


_seq = iter(range(1, 1 << 20))


def rec(pnum, days_ago, moves, assist=None, failed=False):
    """One evidence record, keyed the way solved/ names its files. Every
    record gets a distinct filename: kg_lib.ev_index caches on the evidence
    dict's identity and last key, and two test dicts whose first key matches
    a previous dict's last one hand back a stale index."""
    r = {"date": iso(days_ago), "problem": str(pnum), "moves": dict(moves)}
    if assist:
        r["assist"] = assist
    name = f"solved/p{pnum}{'_FAILED' if failed else ''}_{days_ago}_{next(_seq)}.py"
    return {name: r}


def ev(*records):
    merged = {}
    for r in records:
        merged.update(r)
    return merged


# --- what one attempt is worth ---------------------------------------------

def test_attempt_label_reads_the_file_then_the_moves_then_the_assist():
    assert attempt_label("solved/p1_FAILED_x.py", {"moves": {"a": "clean"}}) == "failed"
    assert attempt_label("solved/p1.py", {"moves": {"a": "struggled"}}) == "struggled"
    assert attempt_label("solved/p1.py", {"moves": {}}) == "unmapped"
    assert attempt_label("solved/p1.py", {"moves": {"a": "clean"}}) == "clean"
    assert attempt_label("solved/p1.py",
                         {"moves": {"a": "clean"}, "assist": "hint"}) == "hint"


def test_a_struggle_outranks_the_assist_on_the_same_attempt():
    """A hinted solve that also struggled is not a hinted clean rep, and must
    not grade Hard on the strength of its assist field."""
    r = {"moves": {"a": "struggled"}, "assist": "hint"}
    assert attempt_label("solved/p1.py", r) == "struggled"


# --- what opens a card -----------------------------------------------------

def test_help_and_walking_away_open_a_card():
    for label in OPENS_CARD:
        assist = None if label == "failed" else label
        e = ev(rec(1, 30, {"a": "clean"}, assist=assist, failed=label == "failed"))
        assert problem_due("1", e), f"{label} should open a card"


def test_a_clean_unaided_solve_never_opens_a_card():
    assert problem_due("1", ev(rec(1, 30, {"a": "clean"}))) is None


def test_a_struggle_alone_does_not_open_a_card():
    """The judge's verdict already shrinks that node's stability - the node
    curve's job. 52 problems from autumn 2025 would otherwise sit ahead of
    this week's."""
    assert problem_due("1", ev(rec(1, 300, {"a": "struggled"}))) is None


def test_an_unmapped_solve_grades_nothing():
    """No move in it at all: a trivial solve is not a struggle, and it neither
    opens a card nor retires one."""
    assert problem_due("1", ev(rec(1, 30, {}))) is None
    e = ev(rec(1, 30, {"a": "clean"}, assist="learning"), rec(1, 5, {}))
    assert problem_due("1", e)[0] == date.today() - timedelta(days=30) \
        + timedelta(days=PROBLEM_GRADUATING_DAYS)


# --- the intervals ---------------------------------------------------------

def test_a_new_card_is_due_three_days_after_the_attempt():
    e = ev(rec(1, 10, {"a": "clean"}, assist="walkthrough"))
    due, interval = problem_due("1", e)
    assert interval == PROBLEM_GRADUATING_DAYS
    assert due == date.today() - timedelta(days=10 - PROBLEM_GRADUATING_DAYS)


def test_an_unaided_clean_rep_retires_the_card():
    e = ev(rec(1, 10, {"a": "clean"}, assist="learning"), rec(1, 2, {"a": "clean"}))
    assert problem_due("1", e) is None


def test_an_assisted_rep_can_never_retire_a_card():
    """The help that put the problem on the list is not what takes it off."""
    for assist in ("hint", "walkthrough", "learning"):
        e = ev(rec(1, 10, {"a": "clean"}, assist="learning"),
               rec(1, 2, {"a": "clean"}, assist=assist))
        assert problem_due("1", e), f"a {assist} rep must leave the card open"


def test_a_struggle_while_the_card_is_open_resets_it():
    e = ev(rec(1, 10, {"a": "clean"}, assist="learning"), rec(1, 2, {"a": "struggled"}))
    due, interval = problem_due("1", e)
    assert interval == PROBLEM_GRADUATING_DAYS
    assert due == date.today() + timedelta(days=1)


def test_a_hinted_clean_rep_pushes_the_card_out_instead_of_closing_it():
    e = ev(rec(1, 10, {"a": "clean"}, assist="walkthrough"),
           rec(1, 4, {"a": "clean"}, assist="hint"))
    due, interval = problem_due("1", e)
    assert interval == max(PROBLEM_GRADUATING_DAYS + 1,
                           round(PROBLEM_GRADUATING_DAYS * ANKI_HARD_FACTOR))
    assert due > date.today() - timedelta(days=4)


def test_a_later_bad_attempt_opens_a_new_card():
    e = ev(rec(1, 30, {"a": "clean"}, assist="learning"),
           rec(1, 20, {"a": "clean"}),
           rec(1, 10, {"a": "clean"}, assist="hint"))
    assert problem_due("1", e)


def test_the_days_last_attempt_is_the_days_grade():
    e = ev(rec(1, 10, {"a": "clean"}, assist="learning"))
    e["solved/p1_second.py"] = {"date": iso(10), "problem": "1",
                                "moves": {"a": "clean"}}
    assert problem_due("1", e) is None


# --- the queue -------------------------------------------------------------

def test_due_problems_is_most_overdue_first():
    e = ev(rec(1, 5, {"a": "clean"}, assist="hint"),
           rec(2, 40, {"a": "clean"}, assist="learning"),
           rec(3, 1, {"a": "clean"}, assist="learning"))
    assert [p for p, _, _ in due_problems(e)] == ["2", "1"]  # 3 is not due yet


def test_due_problems_can_be_held_to_a_problems_table():
    e = ev(rec(1, 40, {"a": "clean"}, assist="hint"),
           rec(2, 40, {"a": "clean"}, assist="hint"))
    assert [p for p, _, _ in due_problems(e, problems={"2": {}})] == ["2"]


def test_drills_have_no_card():
    e = {"solved/d_Pairs_1.py": {"date": iso(10), "problem": "drill",
                                 "moves": {"a": "struggled"}}}
    assert due_problems(e) == []


def test_last_attempt_names_what_happened_and_when():
    e = ev(rec(1, 10, {"a": "clean"}, assist="learning"), rec(1, 3, {}))
    when, label = last_attempt("1", e)
    assert (when, label) == (date.today() - timedelta(days=10), "learning")
