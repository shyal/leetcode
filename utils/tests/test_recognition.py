"""The recognition axis (kg.recognition): a second status per node, next to
execution, derived from graph/recognition.json. These tests pin the pure
parts down on synthetic graphs: what a statement can trigger (the entry
move), how an answer is scored, how status is derived, which rep is due,
how the statement HTML becomes markdown, and how the notes of a solve name
a miss."""

import os
from datetime import date, timedelta

import pytest

from kg import recognition as rc
from kg.kg_lib import SOLID, STALE


def iso(days):
    return (date.today() - timedelta(days=days)).isoformat()


def nodes(*ids, group=None, groups=None):
    out = {}
    for n in ids:
        out[n] = {"id": n, "name": n, "prereqs": [],
                  "group": (groups or {}).get(n, group)}
    return out


def problem(moves, difficulty="Medium", **extra):
    return {"title": f"synthetic {difficulty}", "difficulty": difficulty,
            "moves": list(moves), **extra}


def solve(pnum, days_ago=0):
    return {f"solved/p{pnum}_{days_ago}.py":
            {"date": iso(days_ago), "problem": str(pnum), "moves": {}}}


def spot(pnum, moves, days_ago=0, target=None):
    return {f"recognition/s{pnum}_{days_ago}.md": {
        "date": iso(days_ago), "problem": str(pnum), "kind": "spot",
        "target": target or next(iter(moves)), "moves": dict(moves)}}


def miss(pnum, node, days_ago=0):
    return {f"solved/p{pnum}_{days_ago}.py": {
        "date": iso(days_ago), "problem": str(pnum), "kind": "solve",
        "moves": {node: rc.MISSED}}}


def merged(*recs):
    out = {}
    for r in recs:
        out.update(r)
    return out


# ---- the entry move ---------------------------------------------------------

def test_entry_is_the_first_move_of_every_walk():
    problems = {"1": problem(["bsoa", "pair"], alt_walks=[["greedy", "x"], []])}
    assert rc.entry_nodes("1", problems) == ["bsoa", "greedy"]


def test_score_hit_on_primary_entry():
    problems = {"1": problem(["bsoa", "pair"])}
    assert rc.score(["bsoa"], "1", problems) == ({"bsoa": rc.HIT}, [])


def test_score_hit_on_alt_entry_records_nothing_on_primary():
    problems = {"1": problem(["bsoa", "pair"], alt_walks=[["greedy"]])}
    moves, false = rc.score(["greedy"], "1", problems)
    assert moves == {"greedy": rc.HIT}
    assert false == []


def test_score_miss_lands_on_primary_only():
    problems = {"1": problem(["bsoa", "pair"], alt_walks=[["greedy"]])}
    assert rc.score([], "1", problems) == ({"bsoa": rc.MISSED}, [])


def test_score_false_is_a_named_move_no_walk_uses():
    problems = {"1": problem(["bsoa", "pair"])}
    moves, false = rc.score(["two-pointers", "pair"], "1", problems)
    assert moves == {"pair": rc.HIT, "bsoa": rc.MISSED}  # the route was half read
    assert false == ["two-pointers"]


def test_score_every_walk_move_named_is_a_hit():
    problems = {"1": problem(["bsoa", "pair"])}
    assert rc.score(["bsoa", "pair"], "1", problems) == ({"bsoa": rc.HIT, "pair": rc.HIT}, [])


# ---- derived status ---------------------------------------------------------

def test_status_untested_without_events():
    assert rc.recognition_status("bsoa", {}) == (rc.UNTESTED, None)


def test_status_failed_to_recognize_after_a_miss():
    recog = miss(84, "ms", days_ago=3)
    assert rc.recognition_status("ms", recog)[0] == rc.FAILED_TO_RECOGNIZE


def test_status_wired_after_a_hit_inside_the_window():
    recog = spot(1, {"ms": rc.HIT}, days_ago=10)
    assert rc.recognition_status("ms", recog)[0] == rc.RECOGNIZED


def test_status_lapses_to_untested():
    recog = spot(1, {"ms": rc.HIT}, days_ago=rc.SOLID_WINDOW_DAYS + 1)
    assert rc.recognition_status("ms", recog)[0] == rc.UNTESTED


def test_window_grows_with_hits():
    recog = merged(spot(1, {"ms": rc.HIT}, days_ago=90),
                   spot(2, {"ms": rc.HIT}, days_ago=60),
                   spot(3, {"ms": rc.HIT}, days_ago=50))
    # three hits: 42 * 1.3^2 = 71 days; the last hit was 50 days ago
    assert rc.recognition_status("ms", recog)[0] == rc.RECOGNIZED


def test_a_hit_after_a_miss_clears_failed_to_recognize():
    recog = merged(miss(84, "ms", days_ago=5), spot(1, {"ms": rc.HIT}, days_ago=1))
    assert rc.recognition_status("ms", recog)[0] == rc.RECOGNIZED


def test_spotted_before_sees_only_earlier_spot_reps_with_their_verdict():
    recog = merged(spot(7, {"ms": rc.HIT}, days_ago=3), miss(7, "ms", days_ago=1))
    assert rc.spotted_before("7", iso(0), recog) == (date.today() - timedelta(days=3), rc.HIT)
    assert rc.spotted_before("7", iso(4), recog) is None
    missed = spot(8, {"ms": rc.MISSED}, days_ago=2)
    assert rc.spotted_before("8", iso(0), missed)[1] == rc.MISSED


# ---- the pick ---------------------------------------------------------------

def graph():
    ns = nodes("ms", "bsoa", "bsb", "pair",
               groups={"ms": "stack", "bsoa": "bs", "bsb": "bs", "pair": "bs"})
    problems = {
        "1": problem(["ms"], "Easy"),
        "2": problem(["ms"], "Hard"),
        "3": problem(["bsoa", "pair"], "Medium"),
        "4": problem(["bsb"], "Easy"),
    }
    statuses = {n: (SOLID, date.today()) for n in ns}
    return ns, problems, statuses


def test_the_node_carrying_the_most_reach_is_served():
    ns, problems, statuses = graph()
    # ms reaches 1 and 2; bsoa reaches 3; bsb reaches 4
    assert rc.due_spot(ns, problems, {}, {}, statuses, predicted={}) == \
        ("ms", "1", "untested, 2 reachable through it")


def test_reach_needs_the_whole_walk_solid():
    ns, problems, statuses = graph()
    statuses["ms"] = (STALE, date.today())
    pick = rc.due_spot(ns, problems, {}, {}, statuses, predicted={})
    assert pick[0] in ("bsoa", "bsb")  # ms carries no reach while STALE


def test_a_recognized_node_is_not_served_again_inside_the_window():
    ns, problems, statuses = graph()
    recog = spot(9, {"ms": rc.HIT}, days_ago=5)
    assert rc.due_spot(ns, problems, {}, recog, statuses, predicted={})[0] != "ms"


def test_failed_to_recognize_wins_ties_on_reach():
    ns, problems, statuses = graph()
    evidence = solve(2, days_ago=30)  # ms and bsoa now reach one problem each
    recog = miss(1760, "bsoa", days_ago=2)
    assert rc.due_spot(ns, problems, evidence, recog, statuses, predicted={}) == \
        ("bsoa", "3", "failed to recognize last time, 1 reachable through it")


def test_solved_and_spotted_problems_carry_no_reach():
    ns, problems, statuses = graph()
    recog = spot(1, {"ms": rc.MISSED}, days_ago=1)
    evidence = solve(2, days_ago=30)
    assert rc.due_spot(ns, problems, evidence, recog, statuses, predicted={})[0] != "ms"


def test_ratio_first_rep_is_due_before_the_first_solve():
    assert rc.spot_due_by_ratio({}, {}, every=3)


def test_ratio_one_rep_per_every_solves():
    recog = spot(4, {"bsb": rc.HIT}, days_ago=0)
    two = merged(solve(1), solve(2))
    three = merged(two, solve(3))
    assert not rc.spot_due_by_ratio(recog, two, every=3)
    assert rc.spot_due_by_ratio(recog, three, every=3)
    assert not rc.spot_due_by_ratio(merged(recog, spot(5, {"ms": rc.HIT})), three, every=3)


def test_ratio_zero_turns_spot_reps_off():
    ns, problems, statuses = graph()
    assert rc.due_spot(ns, problems, {}, {}, statuses, predicted={}, every=0) is None


def test_force_skips_the_ratio():
    ns, problems, statuses = graph()
    recog = spot(4, {"bsb": rc.HIT}, days_ago=0)
    assert rc.due_spot(ns, problems, {}, recog, statuses, predicted={}) is None
    assert rc.due_spot(ns, problems, {}, recog, statuses, predicted={}, force=True)[0] == "ms"


def test_ratio_one_is_one_per_solve():
    recog = spot(4, {"bsb": rc.HIT}, days_ago=0)
    assert not rc.spot_due_by_ratio(recog, {}, every=1)
    assert rc.spot_due_by_ratio(recog, solve(1), every=1)


def test_drafted_problems_carry_when_the_map_has_none():
    ns, problems, statuses = graph()
    predicted = {"9": {"title": "draft", "walks": [{"moves": ["bsoa"]}]},
                 "10": {"title": "two walks", "walks": [{"moves": ["bsoa"]}, {"moves": ["ms"]}]},
                 "11": {"title": "gap", "walks": [{"moves": ["bsoa"], "missing": ["x"]}]}}
    evidence = merged(solve(1, days_ago=20), solve(2, days_ago=20), solve(3, days_ago=20))
    recog = miss(1760, "bsoa", days_ago=1)
    assert rc.due_spot(ns, problems, evidence, recog, statuses, predicted=predicted) == \
        ("bsoa", "9", "failed to recognize last time, 1 reachable through it")


def test_mapped_carriers_outrank_drafted_ones():
    ns, problems, statuses = graph()
    predicted = {"9": {"title": "draft", "walks": [{"moves": ["ms"]}]}}
    assert rc.spot_carriers("ms", problems, {}, {}, ns, statuses, predicted=predicted) == ["1", "2", "9"]


# ---- the statement ----------------------------------------------------------

def test_html_to_markdown_keeps_emphasis_code_lists_images():
    html = ('<p>Given <strong>an array </strong>and <em> a value</em> <code>k</code>, '
            '10<sup>5</sup>.</p><ul><li>one<ul><li>nested</li></ul></li></ul>'
            '<pre><strong>Input:</strong> nums = [1]\n<strong>Output:</strong> 2</pre>'
            '<img src="https://assets.leetcode.com/x.png" alt="m"/>')
    md = rc.html_to_markdown(html)
    assert "Given **an array** and *a value* `k`, 10^5." in md
    assert "\n- one\n  - nested\n" in md
    assert "```\nInput: nums = [1]\nOutput: 2\n```" in md
    assert "![m](https://assets.leetcode.com/x.png)" in md


def test_html_table_becomes_a_markdown_table():
    md = rc.html_to_markdown("<table><tr><th>a</th><th>b</th></tr><tr><td>1</td><td>2</td></tr></table>")
    assert "| a | b |\n|---|---|\n| 1 | 2 |" in md


def test_spot_document_round_trips():
    doc = rc.spot_document("Given an array.") + "monotonic stack, nearest smaller\n"
    doc += '\n<!-- spot {"problem": "84", "seconds": 140} -->\n'
    statement, answer = rc.split_answer(doc)
    assert statement == "Given an array."
    assert answer == "monotonic stack, nearest smaller"
    assert rc.read_footer(doc) == {"problem": "84", "seconds": 140}


# ---- a miss written in the notes -------------------------------------------

@pytest.mark.parametrize("notes", [
    "recognition failure, not a binary search failure",
    "i just failed to recognize it was a MS problem",
    "didn't recognise the monotonic stack until the hint",
    "never recognized that this was binary search on the answer",
])
def test_notes_say_missed(notes):
    assert rc.notes_say_missed(notes)


@pytest.mark.parametrize("notes", [
    "recognized it immediately, then fumbled the loop",
    "clean, no hints",
    "",
])
def test_notes_do_not_say_missed(notes):
    assert not rc.notes_say_missed(notes)


def test_reveal_names_the_problem_and_the_verdict():
    rec = {"problem": "84", "title": "Largest Rectangle in Histogram",
           "walk": ["monotonic-stack"], "moves": {"monotonic-stack": rc.MISSED},
           "seconds": 140, "named": ["prefix-sums"], "false": ["prefix-sums"]}
    out = rc.reveal(rec)
    assert "84. Largest Rectangle in Histogram" in out
    assert "walk: monotonic-stack" in out
    assert "missed in 140s" in out
    assert "named but not in any walk: prefix-sums" in out


# ---- the summit gate (kg_next rule 4) ---------------------------------------

def test_a_summit_is_held_while_its_entry_move_failed_to_recognize():
    import os
    from importlib.machinery import SourceFileLoader
    KG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kg")
    kg_next = SourceFileLoader("kg_next_rc", os.path.join(KG, "kg_next")).load_module()
    ns = nodes("ms")
    problems = {"84": problem(["ms"], "Hard")}
    statuses = {"ms": (SOLID, date.today())}
    old = kg_next.immature_nodes
    kg_next.immature_nodes = lambda *a, **k: set()
    try:
        assert kg_next.ready_hards(problems, ns, {}, statuses, recog={}) == ["84"]
        held = merged(miss(84, "ms", days_ago=3))
        assert kg_next.ready_hards(problems, ns, {}, statuses, recog=held) == []
        cleared = merged(held, spot(9, {"ms": rc.HIT}, days_ago=1))
        assert kg_next.ready_hards(problems, ns, {}, statuses, recog=cleared) == ["84"]
    finally:
        kg_next.immature_nodes = old


# ---- an alternative walk ----------------------------------------------------

def test_alternative_is_a_marked_hit_filed_under_spotted_walks():
    problems = {"594": problem(["counter-build", "counts-as-data"])}
    rec = {"problem": "594", "moves": {"counter-build": rc.MISSED},
           "false": ["sliding-window-variable", "sort-then-adjacent"]}
    named = ["sort-then-adjacent", "sliding-window-variable"]
    rc.apply_alternative(rec, named, problems, "matches the sort + sliding window editorial solution")
    assert rec["moves"] == {"sort-then-adjacent": rc.HIT}
    assert rec["false"] == []
    assert rec["alternative"] == named
    assert problems["594"]["spotted_walks"] == [named]
    assert "alt_walks" not in problems["594"]  # code-evidenced only
    rc.apply_alternative(dict(rec), named, problems, "again")
    assert problems["594"]["spotted_walks"] == [named]  # no duplicate
    assert rc.recognition_status("counter-build", {"k": {"date": iso(0), "problem": "594",
                                                         "kind": "spot", **rec}})[0] == rc.UNTESTED
    out = rc.reveal({**rec, "title": "t", "walk": ["counter-build"], "seconds": 3})
    assert "hit through an alternative walk, not yet evidenced by code: sort-then-adjacent, sliding-window-variable" in out
