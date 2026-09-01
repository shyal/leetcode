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


@pytest.fixture(autouse=True)
def _pin_spot_every(monkeypatch):
    # the operator's .envrc knob (loaded by kg_lib at import) must not
    # reach the suite: SPOT_EVERY=0 turns spots off and fails these tests
    monkeypatch.setattr(rc, "SPOT_EVERY", 3)


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


def test_score_hit_on_the_target():
    problems = {"1": problem(["bsoa", "pair"])}
    assert rc.score(["bsoa"], "1", problems, target="bsoa") == ({"bsoa": rc.HIT}, [])


def test_score_target_not_named_is_missed_whatever_its_position():
    problems = {"1": problem(["split", "bsoa", "pair"])}
    moves, false = rc.score(["bsoa", "pair"], "1", problems, target="split")
    assert moves == {"bsoa": rc.HIT, "pair": rc.HIT, "split": rc.MISSED}
    assert false == []


def test_score_the_first_move_is_not_the_target():
    # 884: served for counter-build, named; the .split() step listed first
    # in the map is not missed for being unnamed
    problems = {"884": problem(["string-build-transform", "counter-build", "counts-as-data"])}
    moves, _ = rc.score(["counter-build", "counts-as-data"], "884", problems, target="counter-build")
    assert moves == {"counter-build": rc.HIT, "counts-as-data": rc.HIT}


def test_score_by_hand_misses_the_first_move_only_when_nothing_was_named():
    problems = {"1": problem(["bsoa", "pair"], alt_walks=[["greedy"]])}
    assert rc.score([], "1", problems) == ({"bsoa": rc.MISSED}, [])
    assert rc.score(["greedy"], "1", problems) == ({"greedy": rc.HIT}, [])
    assert rc.score(["pair"], "1", problems) == ({"pair": rc.HIT}, [])


def test_score_false_is_a_named_move_no_walk_uses():
    problems = {"1": problem(["bsoa", "pair"])}
    moves, false = rc.score(["two-pointers", "pair"], "1", problems, target="bsoa")
    assert moves == {"pair": rc.HIT, "bsoa": rc.MISSED}
    assert false == ["two-pointers"]


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


def test_the_node_more_problems_need_is_served():
    ns, problems, statuses = graph()
    # ms carries 1 and 2; bsoa and pair carry 3; bsb carries 4
    assert rc.due_spot(ns, problems, {}, {}, statuses, predicted={}) == \
        ("ms", "1", "untested, 2 problem(s) need only it")


def test_one_unowned_move_is_fine_and_is_the_target():
    ns, problems, statuses = graph()
    statuses["bsoa"] = (STALE, date.today())
    carriers = rc.carriers_by_node(ns, problems, {}, {}, statuses, predicted={})
    assert carriers["bsoa"] == ["3"]
    assert "pair" not in carriers  # 3 is bsoa's rep, not pair's


def test_two_unowned_moves_carry_nothing():
    ns, problems, statuses = graph()
    statuses["bsoa"] = (STALE, date.today())
    statuses["pair"] = (STALE, date.today())
    carriers = rc.carriers_by_node(ns, problems, {}, {}, statuses, predicted={})
    assert "3" not in carriers.get("bsoa", []) and "3" not in carriers.get("pair", [])


def test_a_recognized_node_is_not_served_again_inside_the_window():
    ns, problems, statuses = graph()
    recog = spot(9, {"ms": rc.HIT}, days_ago=5)
    assert rc.due_spot(ns, problems, {}, recog, statuses, predicted={})[0] != "ms"


def test_failed_to_recognize_comes_first_whatever_its_score():
    ns, problems, statuses = graph()
    recog = miss(1760, "bsb", days_ago=2)  # bsb carries one problem, ms two
    assert rc.due_spot(ns, problems, {}, recog, statuses, predicted={}) == \
        ("bsb", "4", "failed to recognize last time, 1 problem(s) need only it")


def test_solved_and_spotted_problems_carry_nothing():
    ns, problems, statuses = graph()
    recog = spot(1, {"ms": rc.MISSED}, days_ago=1)
    evidence = solve(2, days_ago=30)
    assert rc.due_spot(ns, problems, evidence, recog, statuses, predicted={})[0] != "ms"


def test_mapped_carriers_outrank_drafted_ones():
    ns, problems, statuses = graph()
    predicted = {"9": {"title": "draft", "walks": [{"moves": ["ms"]}]}}
    assert rc.spot_carriers("ms", problems, {}, {}, ns, statuses, predicted=predicted) == ["1", "2", "9"]


# ---- what solves and parks say ----------------------------------------------

def clean_solve(pnum, moves, days_ago=0, assist=None):
    rec = {"date": iso(days_ago), "problem": str(pnum), "moves": {m: "clean" for m in moves}}
    if assist:
        rec["assist"] = assist
    return {f"solved/p{pnum}_{days_ago}.py": rec}


def test_a_freestyle_clean_first_solve_is_a_hit_on_its_walk():
    problems = {"1": problem(["bsoa", "pair"])}
    hits = rc.solve_hits(clean_solve(1, ["bsoa", "pair"], days_ago=3), problems)
    assert list(hits.values())[0]["moves"] == {"bsoa": rc.HIT, "pair": rc.HIT}
    assert list(hits)[0].endswith("#solve")


def test_assisted_struggled_or_drill_solves_are_not_hits():
    problems = {"1": problem(["bsoa"])}
    assert not rc.solve_hits(clean_solve(1, ["bsoa"], assist="hint"), problems)
    assert not rc.solve_hits({"solved/p1_0.py": {"date": iso(0), "problem": "1",
                                                 "moves": {"bsoa": "struggled"}}}, problems)
    assert not rc.solve_hits({"solved/d_x.py": {"date": iso(0), "problem": "drill",
                                                "moves": {"bsoa": "clean"}}}, problems)


def test_only_the_first_solve_of_a_problem_counts():
    problems = {"1": problem(["bsoa"])}
    ev = merged(clean_solve(1, ["bsoa"], days_ago=40, assist="learning"),
                clean_solve(1, ["bsoa"], days_ago=2))
    assert not rc.solve_hits(ev, problems)  # the first was a copy; the re-solve remembers it


def test_derived_stored_records_win_over_derived_ones():
    problems = {"1": problem(["bsoa"])}
    ev = clean_solve(1, ["bsoa"], days_ago=40)
    recog = miss(1, "bsoa", days_ago=2)
    d = rc.derived(recog, ev, problems, {"bsoa": (SOLID, date.today())})
    assert rc.recognition_status("bsoa", d)[0] == rc.FAILED_TO_RECOGNIZE
    d = rc.derived({}, ev, problems, {"bsoa": (SOLID, date.today())})
    assert rc.recognition_status("bsoa", d)[0] == rc.RECOGNIZED


def test_a_park_on_solid_ground_is_a_suspected_miss(monkeypatch):
    problems = {"1760": problem(["bsoa", "pair"])}
    import time
    monkeypatch.setattr(rc, "sleep_records", lambda p, e: {
        "1760": {"branch": "1760-slept", "title": "t", "slept": time.time(), "cycles": 1}})
    solid = {"bsoa": (SOLID, date.today()), "pair": (SOLID, date.today())}
    out = rc.park_misses(problems, {}, solid)
    assert out["1760-slept#park"]["moves"] == {"bsoa": rc.MISSED, "pair": rc.MISSED}
    rusty = {"bsoa": (SOLID, date.today()), "pair": (STALE, date.today())}
    assert rc.park_misses(problems, {}, rusty) == {}  # the solve picker's business


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
        ("bsoa", "9", "failed to recognize last time, 1 problem(s) need only it")


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
    out = rc.reveal({**rec, "target": "monotonic-stack", "reason": "failed to recognize last time"})
    assert "served for: monotonic-stack (failed to recognize last time)" in out


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
    assert rec["moves"] == {"sort-then-adjacent": rc.HIT, "sliding-window-variable": rc.HIT}
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


def test_alternative_mixed_with_walk_moves_keeps_both_as_hits():
    # 120: dp-state-formulate (in the walk) and memoize-recursion (not) were
    # both named; a valid top-down route is a hit on both, no miss on the target
    problems = {"120": problem(["dp-state-formulate", "dp-2d-grid", "dp-1d-rolling"])}
    named = ["dp-state-formulate", "memoize-recursion"]
    rec = {"problem": "120"}
    rec["moves"], rec["false"] = rc.score(named, "120", problems, target="dp-1d-rolling")
    assert rec["moves"] == {"dp-state-formulate": rc.HIT, "dp-1d-rolling": rc.MISSED}
    assert rec["false"] == ["memoize-recursion"]
    rc.apply_alternative(rec, named, problems, "top-down with @cache is the accepted memoized solution")
    assert rec["moves"] == {"dp-state-formulate": rc.HIT, "memoize-recursion": rc.HIT}


def test_an_alternative_marks_the_target_and_two_in_a_row_leave_it_to_solves():
    problems = {"120": problem(["dp-state-formulate", "dp-1d-rolling"])}
    rec = {"problem": "120", "moves": {"dp-1d-rolling": rc.MISSED}, "false": ["memoize-recursion"]}
    rc.apply_alternative(rec, ["memoize-recursion"], problems, "why", target="dp-1d-rolling")
    assert rec["moves"] == {"memoize-recursion": rc.HIT, "dp-1d-rolling": rc.ALTERNATIVE}
    one = merged(miss(1235, "dp-1d-rolling", days_ago=5),
                 spot(120, {"dp-1d-rolling": rc.ALTERNATIVE}, days_ago=2, target="dp-1d-rolling"))
    # status still failed (from the park), date moved, still served
    assert rc.recognition_status("dp-1d-rolling", one) == (rc.FAILED_TO_RECOGNIZE, date.today() - timedelta(days=2))
    assert not rc.left_to_solves("dp-1d-rolling", one)
    two = merged(one, spot(1646, {"dp-1d-rolling": rc.ALTERNATIVE}, days_ago=1, target="dp-1d-rolling"))
    assert rc.left_to_solves("dp-1d-rolling", two)
    ns = nodes("dp-state-formulate", "dp-1d-rolling")
    statuses = {n: (SOLID, date.today()) for n in ns}
    pick = rc.due_spot(ns, {"7": problem(["dp-1d-rolling"])}, {}, two, statuses, predicted={})
    assert pick is None  # left to the solve picker
    # an unaided solve using it is the hit that brings it back
    three = merged(two, {"solved/p7_0.py#solve": {"date": iso(0), "problem": "7", "kind": "solve",
                                                  "moves": {"dp-1d-rolling": rc.HIT}}})
    assert rc.recognition_status("dp-1d-rolling", three)[0] == rc.RECOGNIZED


def test_difficulty_restricts_the_carrier_tier():
    ns, problems, statuses = graph()
    assert rc.spot_carriers("ms", problems, {}, {}, ns, statuses, predicted={}, difficulty="Hard") == ["2"]
    assert rc.due_spot(ns, problems, {}, {}, statuses, predicted={}, difficulty="Hard")[:2] == ("ms", "2")
    assert rc.due_spot(ns, problems, {}, {}, statuses, predicted={}, difficulty="Medium")[:2] == ("bsoa", "3")


def test_a_failed_route_reveals_nothing():
    rec = {"problem": "354", "title": "Russian Doll Envelopes", "target": "sort-by-custom-key",
           "walk": ["sort-by-custom-key", "binary-search-boundary", "dp-1d-rolling"],
           "moves": {"sort-by-custom-key": rc.HIT}, "named": ["sort-by-custom-key"],
           "false": ["heap-simulation"], "seconds": 536, "valid": False,
           "why": "counting chains greedily after the sort fails on [[1,1],[1,2],[2,1]]",
           "summary": "sort by width, heap, count chains"}
    out = rc.reveal(rec)
    assert "binary-search-boundary" not in out and "dp-1d-rolling" not in out
    assert "heap-simulation" not in out and "walk:" not in out
    assert "the route as written does not solve it" in out
    assert "served for: sort-by-custom-key" in out
    ok = rc.reveal({**rec, "valid": True})
    assert "walk: sort-by-custom-key, binary-search-boundary, dp-1d-rolling" in ok


def test_a_hit_on_the_same_day_as_a_miss_wins():
    recog = merged(miss(1760, "spc", days_ago=0),
                   {"solved/p2177_0.py#solve": {"date": iso(0), "problem": "2177", "kind": "solve",
                                                "moves": {"spc": rc.HIT}}})
    assert rc.recognition_status("spc", recog)[0] == rc.RECOGNIZED
