"""The picker is the one piece of tooling that decides what gets solved, and
until now nothing pinned its rules down. Every regression it has shipped was
a sort key quietly outranking a more important one, or a frontier node that
fell through every branch and left `make next` saying nothing at all.

These tests run `pick()` against synthetic graphs — a handful of nodes and
problems built in the test itself — so each rule is asserted in isolation,
with no dependency on the real graph/*.json (which changes every solve).

pick() takes nodes/problems/evidence/statuses as arguments, so the graph is
pure input. The three things it still reaches out to disk for — the drill
bank (drill_gated, due_drill) and the acceptance metadata — are stubbed by
the `picker` fixture, which is also where a test overrides them to put a
drill in the bank.
"""

import glob
import os
import re
import sys
from datetime import date, timedelta
from importlib.machinery import SourceFileLoader

import pytest

KG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kg")
kg_next = SourceFileLoader("kg_next", os.path.join(KG, "kg_next")).load_module()

from kg import kg_lib  # noqa: E402
from kg.kg_lib import SOLID, STALE, FRAGILE, MISSING, DEEP_STALE_DAYS  # noqa: E402


def ago(days):
    return date.today() - timedelta(days=days)


def iso(days):
    return ago(days).isoformat()


def node(nid, prereqs=()):
    return {"id": nid, "name": nid, "prereqs": list(prereqs)}


def nodes(*specs):
    """nodes("a", ("b", ["a"])) -> {id: node}, prereqs optional per entry."""
    out = {}
    for s in specs:
        nid, prereqs = s if isinstance(s, tuple) else (s, ())
        out[nid] = node(nid, prereqs)
    return out


def problem(moves, difficulty="Medium", **extra):
    return {"title": f"synthetic {difficulty}", "difficulty": difficulty,
            "moves": list(moves), **extra}


def drafted(moves, missing=None):
    """A graph/predicted.json-shaped entry with one drafted walk."""
    w = {"moves": list(moves), "tier": "predicted"}
    if missing:
        w["missing"] = list(missing)
    return {"title": "synthetic draft", "walks": [w]}


def solve(pnum, moves, days_ago=0, assist=None):
    """One evidence record. `moves` maps node -> clean/struggled/avoided."""
    rec = {"date": iso(days_ago), "problem": str(pnum), "moves": dict(moves)}
    if assist:
        rec["assist"] = assist
    return {f"solved/p{pnum}_{days_ago}.py": rec}


def evidence(*records):
    merged = {}
    for r in records:
        merged.update(r)
    return merged


@pytest.fixture
def picker(monkeypatch):
    """pick() with its three disk reads stubbed: no drill bank anywhere and a
    neutral acceptance for every problem. Maturity (the simmer rule) is
    neutral too — every node mature — because it is derived from months of
    real evidence these synthetic graphs don't carry. Tests that care
    override any of it via the returned control object."""
    ctl = type("Ctl", (), {"bank": set(), "drilled_today": set(), "acceptance": {},
                           "unlocks": {}, "immature": set(), "undone": set()})()

    monkeypatch.setattr(kg_next, "drill_gated",
                        lambda nid, status, last, today=None:
                        nid in ctl.bank and status in (FRAGILE, MISSING))
    monkeypatch.setattr(kg_next, "unlocks",
                        lambda statuses, problems, immature=():
                        ctl.gain if immature else ctl.unlocks)
    ctl.gain = {}  # the reach rule's counts: young node -> drafted problems waiting
    monkeypatch.setattr(kg_next, "due_drill",
                        lambda nid, ev, today=None, early=False, assisted=False:
                        f"drills/{nid}/one.py"
                        if nid in ctl.bank and nid not in ctl.drilled_today else None)
    monkeypatch.setattr(kg_next, "acceptance", lambda p: ctl.acceptance.get(str(p), 50.0))
    # the predicted tier: empty by default (no drafted walks anywhere), so
    # promotion is inert unless a test puts drafts in ctl.predicted and their
    # difficulty in ctl.meta. Routed through the REAL kg_lib.predicted_carrier
    # so its filters and ranking are what get asserted.
    ctl.predicted = {}
    ctl.meta = {}
    monkeypatch.setattr(kg_lib, "_METADATA", ctl.meta)
    monkeypatch.setattr(kg_next, "predicted_carrier",
                        lambda target, problems, statuses, nodes, skip=(),
                        difficulties=("Easy", "Medium"):
                        kg_lib.predicted_carrier(target, problems, statuses,
                                                 nodes, predicted=ctl.predicted,
                                                 skip=skip, difficulties=difficulties))
    monkeypatch.setattr(kg_next, "drafted_in_reach",
                        lambda problems, statuses, nodes, immature, skip=(), first="Hard":
                        kg_lib.drafted_in_reach(problems, statuses, nodes, immature,
                                                predicted=ctl.predicted, skip=skip,
                                                first=first))
    monkeypatch.setattr(kg_next, "draft_misses",
                        lambda target, ev, nodes=None, predicted=None:
                        kg_lib.draft_misses(target, ev, nodes, ctl.predicted))
    monkeypatch.setattr(kg_next, "drafts_falsified",
                        lambda target, ev, nodes=None, predicted=None:
                        kg_lib.drafts_falsified(target, ev, nodes, ctl.predicted))
    monkeypatch.setattr(kg_next, "has_drill_bank", lambda nid: nid in ctl.bank)
    # nodes with drills never done (default none): they hold what depends
    # on them and get their next drill served (rule 0c)
    monkeypatch.setattr(kg_next, "drills_left",
                        lambda nid, ev, early=False: nid in ctl.undone)
    monkeypatch.setattr(kg_lib, "drills_left",  # drill_held reads this one
                        lambda nid, ev, early=False: nid in ctl.undone)
    monkeypatch.setattr(kg_next, "immature_nodes",
                        lambda nodes, evidence, problems: frozenset(ctl.immature))

    def run(nodes, problems, ev, statuses, **kw):
        return kg_next.pick(nodes, problems, ev, statuses, **kw)

    def blocked(nodes, problems, ev, statuses, **kw):
        return kg_next.blocked_frontier(nodes, problems, ev, statuses, **kw)

    ctl.run = run
    ctl.blocked = blocked
    def summits(ns, problems, ev, statuses):
        return kg_next.ready_hards(problems, ns, ev, statuses)

    ctl.summits = summits
    return ctl


# --------------------------------------------------------------------------
# rule 1: consolidate a FRAGILE move on a READY carrier
# --------------------------------------------------------------------------

def test_fragile_move_is_served_on_a_ready_carrier(picker):
    ns = nodes("bsearch", "pivot")
    ps = {"33": problem(["bsearch", "pivot"])}
    st = {"bsearch": (SOLID, ago(1)), "pivot": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st)[:3] == ("pivot", FRAGILE, "33")


def test_fragile_beats_stale_and_missing(picker):
    """Preference order is fragile, then stale, then missing — a rusty move
    is repaired before a cold one is re-entered or a new one introduced."""
    ns = nodes("frag", "stale", "new")
    ps = {"1": problem(["frag"]), "2": problem(["stale"]), "3": problem(["new"])}
    st = {"frag": (FRAGILE, ago(1)), "stale": (STALE, ago(50)), "new": (MISSING, None)}
    assert picker.run(ns, ps, {}, st)[0] == "frag"


def test_oldest_fragile_goes_first(picker):
    ns = nodes("recent", "ancient")
    ps = {"1": problem(["recent"]), "2": problem(["ancient"])}
    st = {"recent": (FRAGILE, ago(2)), "ancient": (FRAGILE, ago(200))}
    assert picker.run(ns, ps, {}, st)[0] == "ancient"


# --------------------------------------------------------------------------
# reachability-aware ordering (PLAN.md phase 1): unlock count ranks the due
# nodes; evidence age breaks ties
# --------------------------------------------------------------------------

def test_higher_unlock_fragile_outranks_an_older_one(picker):
    ns = nodes("old_dud", "young_key")
    ps = {"1": problem(["old_dud"]), "2": problem(["young_key"])}
    st = {"old_dud": (FRAGILE, ago(200)), "young_key": (FRAGILE, ago(2))}
    picker.unlocks = {"young_key": 12, "old_dud": 1}
    assert picker.run(ns, ps, {}, st)[0] == "young_key"


def test_age_breaks_an_unlock_tie(picker):
    ns = nodes("recent", "ancient")
    ps = {"1": problem(["recent"]), "2": problem(["ancient"])}
    st = {"recent": (FRAGILE, ago(2)), "ancient": (FRAGILE, ago(200))}
    picker.unlocks = {"recent": 5, "ancient": 5}
    assert picker.run(ns, ps, {}, st)[0] == "ancient"


def test_highest_unlock_missing_move_is_introduced_first(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a"]), "2": problem(["b"])}
    st = {"a": (MISSING, None), "b": (MISSING, None)}
    picker.unlocks = {"b": 10, "a": 2}
    assert picker.run(ns, ps, {}, st)[:2] == ("b", MISSING)


def test_unlocks_counts_only_problems_blocked_by_exactly_one_node():
    from kg.kg_lib import unlocks
    st = {"a": (SOLID, ago(1)), "b": (FRAGILE, ago(1)), "c": (MISSING, None)}
    problems = {"1": problem(["a"])}          # already solved, never counted
    predicted = {
        "1": {"walks": [{"moves": ["a", "b"]}]},           # solved: skipped
        "2": {"walks": [{"moves": ["a", "b"]}]},           # blocked only by b
        "3": {"walks": [{"moves": ["b", "c"]}]},           # two gaps: nobody
        "4": {"walks": [{"moves": ["a"]}]},                # in reach: skipped
        "5": {"walks": [{"moves": ["a", "b"], "missing": ["segment-tree"]},
                        {"moves": ["a", "c"]}]},           # only clean walk -> c
        "6": {"walks": [{"moves": ["a"]}, {"moves": ["a", "b"]}]},  # in reach
    }
    assert unlocks(st, problems, predicted) == {"b": 1, "c": 1}


# --------------------------------------------------------------------------
# the one-new-move rule, and who is allowed to be a carrier
# --------------------------------------------------------------------------

def test_carrier_needs_every_other_move_solid(picker):
    """A carrier that would introduce a second rusty move is not a carrier:
    the ZPD constraint is one fragile/stale node per assignment."""
    ns = nodes("target", "alsorusty", "solid")
    ps = {"1": problem(["target", "alsorusty"]),   # two rusty moves — never
          "2": problem(["target", "solid"])}       # one rusty move — this one
    st = {"target": (FRAGILE, ago(1)), "alsorusty": (STALE, ago(90)),
          "solid": (SOLID, ago(1))}
    assert picker.run(ns, ps, {}, st)[2] == "2"


def test_hards_are_never_carriers(picker):
    """Himalayas rule: a Hard is a summit attempted all-green, never the
    place a rusty move gets its rep. With the move rusty the Hard is not
    servable at all, as a carrier or as a summit."""
    ns = nodes("target")
    ps = {"41": problem(["target"], difficulty="Hard")}
    st = {"target": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st) is None


def test_a_rusty_move_is_repaired_before_a_summit_is_offered(picker):
    """Summits are the LAST rule: an all-green Hard waits until there is
    nothing rusty left to train."""
    ns = nodes("frag", "solid")
    ps = {"1": problem(["frag"]), "76": problem(["solid"], difficulty="Hard")}
    st = {"frag": (FRAGILE, ago(1)), "solid": (SOLID, ago(1))}
    assert picker.run(ns, ps, {}, st)[2] == "1"


def test_banned_problems_are_never_carriers(picker):
    ns = nodes("target")
    ps = {"1": problem(["target"], banned=True)}
    st = {"target": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st) is None


def test_problems_solved_today_are_excluded(picker):
    ns = nodes("target")
    ps = {"1": problem(["target"]), "2": problem(["target"])}
    st = {"target": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st, exclude={"1"})[2] == "2"


def test_sleeping_problems_are_not_offered(picker):
    ns = nodes("target")
    ps = {"1": problem(["target"]), "2": problem(["target"])}
    st = {"target": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st, asleep={"1"})[2] == "2"


# --------------------------------------------------------------------------
# carrier sort keys — the 153-before-33 regression
# --------------------------------------------------------------------------

def test_freshness_outranks_acceptance(picker):
    """The bug this suite was started for: 153 (55% acceptance, failed
    yesterday) kept being served ahead of 33 (45%, untouched for months)
    because acceptance was baked into the gentleness key and decided before
    last_solved was ever compared. Acceptance is the LAST tiebreak."""
    ns = nodes("bsearch", "pivot")
    ps = {"33": problem(["bsearch", "pivot"]), "153": problem(["bsearch", "pivot"])}
    picker.acceptance = {"33": 45.5, "153": 55.2}
    ev = evidence(solve("33", {"bsearch": "clean"}, days_ago=300),
                  solve("153", {"bsearch": "clean", "pivot": "struggled"}, days_ago=1))
    st = {"bsearch": (SOLID, ago(1)), "pivot": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, ev, st)[2] == "33"


def test_acceptance_still_breaks_a_genuine_tie(picker):
    """Same tier, same tree, neither ever solved: the gentler problem (higher
    acceptance = less community friction) sorts first, since nothing more
    meaningful separates them."""
    ns = nodes("target")
    ps = {"1": problem(["target"]), "2": problem(["target"])}
    picker.acceptance = {"1": 70.0, "2": 30.0}
    st = {"target": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st)[2] == "1"


def test_easier_carrier_wins_over_a_harder_one(picker):
    ns = nodes("target", "extra")
    ps = {"1": problem(["target", "extra"], difficulty="Medium"),
          "2": problem(["target", "extra"], difficulty="Easy")}
    st = {"target": (FRAGILE, ago(1)), "extra": (SOLID, ago(1))}
    assert picker.run(ns, ps, {}, st)[2] == "2"


def test_smaller_input_tree_wins_within_a_tier(picker):
    """Gentleness after difficulty is fewest concepts in the room, counted
    over the transitive prereq closure, not just the walk length."""
    ns = nodes("target", "plain", ("deep", ["p1"]), ("p1", ["p2"]), "p2")
    ps = {"1": problem(["target", "deep"]), "2": problem(["target", "plain"])}
    st = {"target": (FRAGILE, ago(1)), "deep": (SOLID, ago(1)),
          "plain": (SOLID, ago(1)), "p1": (SOLID, ago(1)), "p2": (SOLID, ago(1))}
    assert picker.run(ns, ps, {}, st)[2] == "2"


# --------------------------------------------------------------------------
# STALE: spaced re-solve vs deep-stale re-entry
# --------------------------------------------------------------------------

def test_stale_move_reuses_its_latest_carrier(picker):
    """An ordinary stale move is a spaced repetition: the same problem comes
    back, because the rep IS the re-solve."""
    ns = nodes("target")
    ps = {"1": problem(["target"]), "2": problem(["target"])}
    ev = evidence(solve("2", {"target": "clean"}, days_ago=50))
    st = {"target": (STALE, ago(50))}
    assert picker.run(ns, ps, ev, st)[:3] == ("target", STALE, "2")


def test_deep_stale_move_re_enters_on_a_fresh_carrier(picker):
    """Past 2x the solid window the memory is gone, so a cold 're-solve'
    would play like a new problem. Re-enter on a gentle carrier instead."""
    old = DEEP_STALE_DAYS + 30
    ns = nodes("target")
    ps = {"1": problem(["target"], difficulty="Easy"),
          "2": problem(["target"], difficulty="Medium")}
    ev = evidence(solve("2", {"target": "clean"}, days_ago=old))
    st = {"target": (STALE, ago(old))}
    target, status, pnum, reason = picker.run(ns, ps, ev, st)
    assert (target, status, pnum) == ("target", STALE, "1")
    assert "deep-stale" in reason


# --------------------------------------------------------------------------
# MISSING: one genuinely new move, prereqs all solid
# --------------------------------------------------------------------------

def test_missing_move_needs_solid_prereqs(picker):
    """A new move whose prereq is itself rusty is not on the frontier —
    the prereq gets served instead."""
    ns = nodes("prereq", ("new", ["prereq"]))
    ps = {"1": problem(["new"]), "2": problem(["prereq"])}
    st = {"prereq": (FRAGILE, ago(1)), "new": (MISSING, None)}
    assert picker.run(ns, ps, {}, st)[0] == "prereq"


def test_missing_move_with_solid_prereqs_is_introduced(picker):
    ns = nodes("prereq", ("new", ["prereq"]))
    ps = {"1": problem(["new", "prereq"])}
    st = {"prereq": (SOLID, ago(1)), "new": (MISSING, None)}
    assert picker.run(ns, ps, {}, st)[:3] == ("new", MISSING, "1")


# --------------------------------------------------------------------------
# the drill-success gate
# --------------------------------------------------------------------------

def test_fragile_move_with_a_drill_bank_drills_instead_of_solving(picker):
    """drill_gated: a fragile move that HAS a bank trains on the drill only.
    The carrier is held until a clean rep clears the status."""
    ns = nodes("target")
    ps = {"1": problem(["target"])}
    picker.bank = {"target"}
    st = {"target": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st)[2] == "drill:target"


def test_a_drill_already_done_today_holds_the_carrier(picker):
    """Drilled today and still not clean: the carrier stays held rather than
    unlocking on drill recency alone (the 227 hole)."""
    ns = nodes("target", "other")
    ps = {"1": problem(["target"]), "2": problem(["other"])}
    picker.bank = {"target"}
    picker.drilled_today = {"target"}
    st = {"target": (FRAGILE, ago(1)), "other": (STALE, ago(50))}
    assert picker.run(ns, ps, {}, st)[0] == "other"


def test_missing_move_with_no_carrier_falls_back_to_its_drill(picker):
    """A frontier node whose only walk is a Hard has no carrier at all. Its
    drill is offered instead of the node being silently skipped."""
    ns = nodes("target")
    ps = {"41": problem(["target"], difficulty="Hard")}
    picker.bank = {"target"}
    st = {"target": (MISSING, None)}
    assert picker.run(ns, ps, {}, st)[2] == "drill:target"


# --------------------------------------------------------------------------
# sleep
# --------------------------------------------------------------------------

def test_woken_problem_jumps_the_queue(picker):
    ns = nodes("target", "other")
    ps = {"1": problem(["target"]), "2": problem(["other"])}
    st = {"target": (FRAGILE, ago(1)), "other": (FRAGILE, ago(200))}
    target, status, pnum, reason = picker.run(ns, ps, {}, st, woken=["1"])
    assert pnum == "1"
    assert "sleep" in reason


def test_ground_under_a_sleeping_problem_is_warmed_elsewhere(picker):
    """While a problem sleeps it is excluded everywhere, but its walk's rusty
    moves still get reps — through a different carrier."""
    ns = nodes("rusty", "solid")
    ps = {"1": problem(["rusty", "solid"]), "2": problem(["rusty"])}
    st = {"rusty": (FRAGILE, ago(1)), "solid": (SOLID, ago(1))}
    target, status, pnum, reason = picker.run(ns, ps, {}, st, asleep=["1"])
    assert (target, pnum) == ("rusty", "2")
    assert "sleeping" in reason


# --------------------------------------------------------------------------
# session start
# --------------------------------------------------------------------------

def test_session_start_serves_a_trivial_easy(picker):
    """Inside the session-start window the first pick is juice: an all-SOLID
    easy, nothing rusty and nothing new."""
    ns = nodes("solid", "rusty")
    ps = {"1": problem(["solid"], difficulty="Easy"), "2": problem(["rusty"])}
    st = {"solid": (SOLID, ago(1)), "rusty": (FRAGILE, ago(1))}
    target, status, pnum, reason = picker.run(ns, ps, {}, st, session_start=True)
    assert (pnum, status) == ("1", SOLID)
    assert "session start" in reason


def test_session_start_skips_a_warmup_done_this_week(picker):
    """A problem solved inside the cooldown is muscle memory, not a warmup."""
    ns = nodes("solid")
    ps = {"1": problem(["solid"], difficulty="Easy"),
          "2": problem(["solid"], difficulty="Easy")}
    ev = evidence(solve("1", {"solid": "clean"}, days_ago=2))
    st = {"solid": (SOLID, ago(1))}
    assert picker.run(ns, ps, ev, st, session_start=True)[2] == "2"


def test_session_start_falls_through_when_no_easy_qualifies(picker):
    """No trivial easy in the bank must not swallow the pick — normal rules
    resume in the same call."""
    ns = nodes("rusty")
    ps = {"1": problem(["rusty"])}
    st = {"rusty": (FRAGILE, ago(1))}
    assert picker.run(ns, ps, {}, st, session_start=True)[:3] == ("rusty", FRAGILE, "1")


# --------------------------------------------------------------------------
# anti-dodge
# --------------------------------------------------------------------------

def test_dodged_move_gets_a_carrier_that_resists_the_dodge(picker):
    """When the last evidence for a move says it was routed around, the
    carrier is chosen for having no recorded escape route."""
    ns = nodes("target", "solid")
    ps = {"1": problem(["target", "solid"], alt_walks=[["solid"]]),  # escapable
          "2": problem(["target", "solid"])}                        # not
    ev = evidence(solve("9", {"target": "avoided"}, days_ago=3))
    st = {"target": (FRAGILE, ago(3)), "solid": (SOLID, ago(1))}
    target, status, pnum, reason = picker.run(ns, ps, ev, st)
    assert pnum == "2"
    assert "dodge" in reason


# --------------------------------------------------------------------------
# exhaustion — the case that made `make next` go quiet
# --------------------------------------------------------------------------

def test_an_all_solid_graph_serves_a_summit(picker):
    """`make next` was never about basecamps: with nothing rusty left, the
    answer to "what now" is an all-green Hard, served as a normal pick."""
    ns = nodes("a")
    ps = {"1": problem(["a"], difficulty="Easy"), "76": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1))}
    target, status, pnum, reason = picker.run(ns, ps, {}, st)
    assert (pnum, status) == ("76", SOLID)
    assert "summit" in reason


def test_the_most_reachable_summit_goes_first(picker):
    """Fewest gaps on the route wins — not the shortest walk. 76 carries an
    unmapped trick, so 4 is closer even with the longer walk."""
    ns = nodes("a", "b", "c")
    ps = {"4": problem(["a", "b", "c"], difficulty="Hard"),
          "76": problem(["a"], difficulty="Hard", unmapped=["a trick with no node"])}
    st = {n: (SOLID, ago(1)) for n in "abc"}
    assert picker.run(ns, ps, {}, st)[2] == "4"


def test_a_summited_hard_is_not_offered_again(picker):
    ns = nodes("a")
    ps = {"76": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1))}
    ev = evidence(solve("76", {"a": "clean"}, days_ago=30))
    assert picker.run(ns, ps, ev, st) is None


def test_nothing_to_pick_returns_none_when_no_summit_is_green(picker):
    """Every node solid, every Hard already summited: there is genuinely
    nothing to serve, and None is the honest answer."""
    ns = nodes("a")
    ps = {"1": problem(["a"])}
    st = {"a": (SOLID, ago(1))}
    assert picker.run(ns, ps, {}, st) is None


def test_a_node_walked_only_by_hards_is_reported_as_blocked(picker):
    """The real state of the graph on 2026-08-20: counting-sort-buckets is
    MISSING, its only walk is a Hard (so no carrier can exist), and it has no
    drill bank — so every pick() branch fell through and `make next` printed
    nothing about the one node still standing between here and an all-solid
    graph. pick() still returns None, but the blockage is now nameable."""
    ns = nodes("counting-sort-buckets")
    ps = {"41": problem(["counting-sort-buckets"], difficulty="Hard")}
    st = {"counting-sort-buckets": (MISSING, None)}
    assert picker.run(ns, ps, {}, st) is None

    (nid, status, why, dry), = picker.blocked(ns, ps, {}, st)
    assert (nid, status, dry) == ("counting-sort-buckets", MISSING, True)
    assert "Hard" in why and "41" in why
    assert "no drill exists" in why


def test_an_all_solid_graph_has_no_blocked_frontier(picker):
    """Nothing due and nothing blocked are different answers: only the second
    one is a to-do, so an all-solid graph must report an empty frontier."""
    ns = nodes("a")
    ps = {"1": problem(["a"])}
    st = {"a": (SOLID, ago(1))}
    assert picker.blocked(ns, ps, {}, st) == []


def test_a_servable_node_is_not_called_blocked(picker):
    """pick() preferring something else is not a blockage."""
    ns = nodes("frag", "stale")
    ps = {"1": problem(["frag"]), "2": problem(["stale"])}
    st = {"frag": (FRAGILE, ago(1)), "stale": (STALE, ago(50))}
    assert picker.blocked(ns, ps, {}, st) == []


def test_a_node_whose_carriers_are_all_spent_today_is_blocked(picker):
    """A move with a real carrier that has already been solved today is
    blocked for today only — the reason has to say so rather than claiming
    the bank is missing something."""
    ns = nodes("target")
    ps = {"1": problem(["target"])}
    st = {"target": (FRAGILE, ago(1))}
    (nid, _, why, dry), = picker.blocked(ns, ps, {}, st, exclude={"1"})
    assert (nid, dry) == ("target", False)
    assert "already solved today" in why


def test_a_node_blocked_only_by_a_second_rusty_move_says_so(picker):
    """Its carrier exists and is not a Hard — it just needs another move made
    solid first. That is a different to-do from writing a drill."""
    ns = nodes("target", "alsorusty")
    ps = {"1": problem(["target", "alsorusty"])}
    st = {"target": (FRAGILE, ago(1)), "alsorusty": (FRAGILE, ago(1))}
    reasons = {nid: why for nid, _, why, _ in picker.blocked(ns, ps, {}, st)}
    assert "second rusty move" in reasons["target"]


def test_an_all_green_hard_is_offered_as_the_summit(picker):
    """When basecamp is dry the answer to "what now" is a summit."""
    ns = nodes("a", "b")
    ps = {"76": problem(["a", "b"], difficulty="Hard"),
          "1": problem(["a"], difficulty="Easy")}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    assert picker.summits(ns, ps, {}, st) == ["76"]


def test_a_hard_with_a_rusty_move_is_not_ready(picker):
    ns = nodes("a", "b")
    ps = {"76": problem(["a", "b"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1)), "b": (FRAGILE, ago(1))}
    assert picker.summits(ns, ps, {}, st) == []


def test_a_hard_with_a_rusty_PREREQ_is_not_ready(picker):
    """Reachability is the whole input tree, not just the walk: a solid move
    resting on a rusty prereq is still a gap on the route."""
    ns = nodes(("a", ["deep"]), "deep")
    ps = {"76": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1)), "deep": (STALE, ago(200))}
    assert picker.summits(ns, ps, {}, st) == []


def test_a_hard_with_an_unmapped_move_is_not_ready(picker):
    """295 was being served as all-green while carrying "balance two heaps to
    maintain a running median" — a trick with no node in the taxonomy. An
    unmapped move is unroutable new ground, so it counts as a gap."""
    ns = nodes("a")
    ps = {"295": problem(["a"], difficulty="Hard",
                         unmapped=["balance two heaps for a running median"])}
    st = {"a": (SOLID, ago(1))}
    assert picker.summits(ns, ps, {}, st) == []


def test_a_hard_with_an_immature_move_is_not_ready(picker):
    """The simmer rule: SOLID is not enough for a summit — a young badge from
    one burst of drills has not proven it can carry a Hard yet, so an
    immature move counts as a gap on the route."""
    ns = nodes("a", "b")
    ps = {"76": problem(["a", "b"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.immature.add("b")
    assert picker.summits(ns, ps, {}, st) == []


def test_an_already_summited_hard_is_not_offered_again(picker):
    ns = nodes("a")
    ps = {"76": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1))}
    ev = evidence(solve("76", {"a": "clean"}, days_ago=30))
    assert picker.summits(ns, ps, ev, st) == []


def test_summits_are_ranked_by_reachability_then_number(picker):
    """rank_summits is the ordering `make hard` uses, and `make next` shares
    it so the two can never name different summits."""
    ns = nodes("a")
    ps = {"212": problem(["a"], difficulty="Hard"),
          "76": problem(["a"], difficulty="Hard"),
          "4": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1))}
    assert picker.summits(ns, ps, {}, st) == ["4", "76", "212"]


def test_a_classic_summit_outranks_a_non_classic_one(picker):
    """`make hard` only ever offers interview classics, so `make next` puts
    them first rather than serving a summit `make hard` would never name."""
    ns = nodes("a")
    ps = {"76": problem(["a"], difficulty="Hard"),      # a CLASSIC
          "3000": problem(["a"], difficulty="Hard")}    # not
    st = {"a": (SOLID, ago(1))}
    assert picker.summits(ns, ps, {}, st) == ["76"]


def test_a_missing_node_behind_a_rusty_prereq_is_not_on_the_frontier(picker):
    """It is not blocked, it is simply not up yet — reporting it would turn
    the frontier list into noise."""
    ns = nodes("prereq", ("new", ["prereq"]))
    ps = {"1": problem(["new"], difficulty="Hard"), "2": problem(["prereq"])}
    st = {"prereq": (FRAGILE, ago(1)), "new": (MISSING, None)}
    assert [nid for nid, _, _, _ in picker.blocked(ns, ps, {}, st)] == []


# --------------------------------------------------------------------------
# "after" edges: a problem waits for the problem its walk builds on
# --------------------------------------------------------------------------

def test_a_problem_waits_for_its_due_predecessor(picker):
    """47 declares "after": ["46"]. With both cold, plain freshness sorting
    would serve 47 (older last solve) - the hold flips it to 46, the core
    the variation builds on."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"]), "47": problem(["bt"], after=["46"])}
    ev = evidence(solve("46", {"bt": "clean"}, days_ago=299),
                  solve("47", {"bt": "clean"}, days_ago=300))
    st = {"bt": (STALE, ago(299))}
    assert picker.run(ns, ps, ev, st)[:3] == ("bt", STALE, "46")


def test_a_warm_predecessor_releases_the_problem(picker):
    """Once 46 has a clean solve inside the solid window, 47 rejoins the
    pool and wins on freshness (least recently solved)."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"]), "47": problem(["bt"], after=["46"])}
    ev = evidence(solve("46", {"bt": "clean"}, days_ago=3),
                  solve("47", {"bt": "clean"}, days_ago=300))
    st = {"bt": (STALE, ago(300))}
    assert picker.run(ns, ps, ev, st)[:3] == ("bt", STALE, "47")


def test_a_learning_predecessor_solve_does_not_release(picker):
    """A learning rep is not recall evidence anywhere else either."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"]), "47": problem(["bt"], after=["46"])}
    ev = evidence(solve("46", {"bt": "clean"}, days_ago=10, assist="learning"),
                  solve("46", {"bt": "clean"}, days_ago=299),
                  solve("47", {"bt": "clean"}, days_ago=300))
    st = {"bt": (STALE, ago(299))}
    assert picker.run(ns, ps, ev, st)[:3] == ("bt", STALE, "46")


# --------------------------------------------------------------------------
# "after" edges to drills: a problem waits for the bank drill it builds on
# --------------------------------------------------------------------------

class DrillRegistry(dict):
    """A drills.json stand-in the test bank helpers fill."""


def drill_bank(tmp_path, monkeypatch, node, title, fname="d0.py", did="d1", after=()):
    """One bank file under a temporary DRILLS_DIR, registered in the graph
    as drill `did` (drills.json) with its "after" ids."""
    d = tmp_path / node
    d.mkdir(exist_ok=True)
    (d / fname).write_text(f'"""\nDRILL: {title}\nTRAINS: {node}\n"""\n')
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    if not isinstance(kg_lib._DRILLS, DrillRegistry):
        monkeypatch.setattr(kg_lib, "_DRILLS", DrillRegistry())
    kg_lib._DRILLS[did] = {"title": title, "after": list(after)}
    kg_lib._DRILL_PATHS.clear()


def register(monkeypatch, **spec):
    """drills.json for a test bank whose files were written by hand:
    register(monkeypatch, d1="Lower", d2=("Upper", ["d1"]))."""
    reg = {}
    for did, v in spec.items():
        title, after = (v, []) if isinstance(v, str) else v
        reg[did] = {"title": title, "after": list(after)}
    monkeypatch.setattr(kg_lib, "_DRILLS", reg)
    kg_lib._DRILL_PATHS.clear()


def drill_rep(title, node, days_ago, assist=None, verdict="clean"):
    stem = title.replace(" ", "_")
    rec = {"date": iso(days_ago), "problem": "drill", "moves": {node: verdict}}
    if assist:
        rec["assist"] = assist
    return {f"solved/d_{stem}_{days_ago}.py": rec}


def test_a_problem_waits_for_a_drill_never_done(tmp_path, monkeypatch):
    """713 declares "after": ["d1"], the Count by Contribution drill. No rep of that
    drill anywhere: 713 is held, and the hold names the drill."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"])}
    assert kg_lib.held_behind("713", ps, {}) == "d1"


def test_a_warm_drill_releases_the_problem(tmp_path, monkeypatch):
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"])}
    ev = evidence(drill_rep("Count by Contribution", "sw", days_ago=3))
    assert kg_lib.held_behind("713", ps, ev) is None


def test_an_assisted_drill_rep_does_not_release(tmp_path, monkeypatch):
    """Same bar as a drill releasing the next drill of its node: the unaided
    clean is what releases, a walkthrough clean is a rep but not ownership."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"])}
    ev = evidence(drill_rep("Count by Contribution", "sw", days_ago=3,
                            assist="walkthrough"))
    assert kg_lib.held_behind("713", ps, ev) == "d1"


def test_a_drill_rep_outside_the_solid_window_does_not_release(tmp_path, monkeypatch):
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"])}
    ev = evidence(drill_rep("Count by Contribution", "sw",
                            days_ago=kg_lib.SOLID_WINDOW_DAYS + 1))
    assert kg_lib.held_behind("713", ps, ev) == "d1"


def test_a_struggle_after_a_clean_holds_again(tmp_path, monkeypatch):
    """Latest rep decides, as for drills releasing drills."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"])}
    ev = evidence(drill_rep("Count by Contribution", "sw", days_ago=9),
                  drill_rep("Count by Contribution", "sw", days_ago=2,
                            verdict="struggled"))
    assert kg_lib.held_behind("713", ps, ev) == "d1"


def test_a_drill_ref_nobody_banks_holds_nothing(tmp_path, monkeypatch):
    """An id no drill carries cannot be released by anything, so it holds
    nothing - the deadlock rule for banned predecessors. The real graph is
    checked by test_every_after_id_in_the_real_graph_resolves."""
    drill_bank(tmp_path, monkeypatch, "sw", "Something Else", did="d9")
    ps = {"713": problem(["sw"], after=["d1"])}
    assert kg_lib.held_behind("713", ps, {}) is None


def test_a_renamed_bank_file_keeps_its_edge(tmp_path, monkeypatch):
    """The edge names the DRILL title, not the file, so renumbering the bank
    changes nothing."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution", fname="w09_whatever.py")
    ps = {"713": problem(["sw"], after=["d1"])}
    ev = evidence(drill_rep("Count by Contribution", "sw", days_ago=3))
    assert kg_lib.held_behind("713", ps, ev) is None


def test_the_picker_serves_the_free_carrier_over_the_held_one(picker, tmp_path, monkeypatch):
    """Two carriers of a rusty node, 713 fresher on paper but held behind a
    drill never done: 3258 is served."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ns = nodes("sw")
    ps = {"713": problem(["sw"], after=["d1"]),
          "3258": problem(["sw"])}
    ev = evidence(solve("713", {"sw": "clean"}, days_ago=300),
                  solve("3258", {"sw": "clean"}, days_ago=299))
    st = {"sw": (STALE, ago(299))}
    assert picker.run(ns, ps, ev, st)[:3] == ("sw", STALE, "3258")
    ev = evidence(ev, drill_rep("Count by Contribution", "sw", days_ago=3))
    assert picker.run(ns, ps, ev, st)[:3] == ("sw", STALE, "713")


def test_gates_is_the_reverse_of_after(tmp_path, monkeypatch):
    """What `make next` prints under a served drill or problem: the problems
    and drills whose "after" names it, problems first."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"]),
          "3258": problem(["sw"], after=["d1"]),
          "47": problem(["sw"], after=["46"]),
          "46": problem(["sw"])}
    ds = {"d2": {"title": "Exactly K", "after": ["d1"]}}
    assert kg_lib.gates("d1", ps, ds) == ["713", "3258", "d2"]
    assert kg_lib.gates("46", ps, ds) == ["47"]
    assert kg_lib.gates("47", ps, ds) == []


def test_dependents_says_what_opens_and_what_else_holds(tmp_path, monkeypatch):
    """`make dependents d1`: each dependent with its status and the OTHER
    ids still holding it, so the next `make prepare` reads off the list."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    drill_bank(tmp_path, monkeypatch, "sw", "Exactly K", fname="d1.py", did="d2", after=["d1"])
    ps = {"713": problem(["sw"], after=["d1"]),
          "992": problem(["sw"], after=["d1", "d2"]),
          "46": problem(["sw"])}
    ev = evidence(solve("713", {"sw": "clean"}, days_ago=100))
    rows = kg_lib.dependents("d1", ps, ev)
    assert [(r["id"], r["kind"], r["status"], r["held_by"]) for r in rows] == [
        ("713", "Medium", STALE, []),
        ("992", "Medium", MISSING, ["d2"]),
        ("d2", "drill", MISSING, []),
    ]
    assert kg_lib.dependents("46", ps, ev) == []


def test_easiest_first_orders_drills_then_by_difficulty_then_acceptance(monkeypatch):
    monkeypatch.setattr(kg_lib, "_METADATA", {"1": {"acceptance": 30.0}, "2": {"acceptance": 70.0}})
    rows = [{"id": "3", "kind": "Hard"}, {"id": "1", "kind": "Medium"},
            {"id": "2", "kind": "Medium"}, {"id": "d5", "kind": "drill"}, {"id": "9", "kind": "Easy"}]
    assert [r["id"] for r in kg_lib.easiest_first(rows)] == ["d5", "9", "2", "1", "3"]


def test_drills_left_ignores_a_chain_ending_at_another_nodes_drill(tmp_path, monkeypatch):
    """d27 waits on d26, d26 waits on d75 of another node. Serving this node
    reaches neither, so the node has no drill left."""
    drill_bank(tmp_path, monkeypatch, "other", "Atom", fname="a.py", did="d75")
    drill_bank(tmp_path, monkeypatch, "sw", "Count", fname="c.py", did="d26", after=["d75"])
    drill_bank(tmp_path, monkeypatch, "sw", "Exactly", fname="e.py", did="d27", after=["d26"])
    assert not kg_lib.drills_left("sw", {})
    ev = evidence(drill_rep("Atom", "other", days_ago=1))
    assert kg_lib.drills_left("sw", ev)


def test_rule_0c_does_not_serve_a_prereq_parked_behind_its_own_prereq(picker):
    """2026-08-31: substring-enumeration (MISSING, banked) became a prereq of
    the window node; the window node still had a drill undone and a held
    dependent, so rule 0c served the window drill over the atom under it."""
    ns = nodes("atom", ("win", ["atom"]), ("dep", ["win"]))
    ps = {"1": problem(["dep"])}
    ev = evidence(solve("1", {"win": "clean"}, days_ago=1))
    st = {"atom": (MISSING, None), "win": (SOLID, ago(1)), "dep": (STALE, ago(300))}
    picker.bank.update({"atom", "win"})
    picker.undone.update({"atom", "win"})
    assert picker.run(ns, ps, ev, st)[:3] == ("atom", MISSING, "drill:atom")


def test_rule_0c_climbs_a_hold_chain_to_its_root(picker):
    """2026-08-31 (make simulate): dedupe siblings waited on start-index,
    start-index on choose-undo, and choose-undo was SOLID through an
    assisted rep. Rule 0c found start-index, saw it parked, and gave up;
    nothing named choose-undo for 14 simulated days. It climbs now."""
    ns = nodes("cu", ("si", ["cu"]), ("dd", ["si"]))
    ps = {"1": problem(["dd"])}
    picker.bank = {"cu", "si", "dd"}
    picker.undone = {"si"}
    ev = evidence(solve("8", {"cu": "clean"}, days_ago=1, assist="walkthrough"),
                  solve("9", {"si": "clean"}, days_ago=1))
    st = {"dd": (FRAGILE, ago(1)), "si": (SOLID, ago(1)), "cu": (SOLID, ago(1))}
    target, status, pnum, why = picker.run(ns, ps, ev, st)
    assert (target, status, pnum) == ("cu", SOLID, "drill:cu")
    assert "own it unaided" in why


def test_a_stale_move_whose_carriers_are_all_held_gets_its_drill(picker):
    """2026-08-31 (make simulate): 102 is the one carrier of the level
    BFS and waits on drill d67; ordinary STALE is not drill-gated, so the
    stale rule offered nothing for 60 simulated days. No carrier can fire,
    so the drill is the rep."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a"], after=["9"]), "9": problem(["b"])}
    picker.bank = {"a"}
    ev = evidence(solve("1", {"a": "clean"}, days_ago=20))
    st = {"a": (STALE, ago(20)), "b": (SOLID, ago(1))}
    assert picker.run(ns, ps, ev, st)[:3] == ("a", STALE, "drill:a")


def test_a_held_carrier_serves_the_root_predecessor_first(picker):
    """2026-08-31 (make simulate): 310 carries topological order and waits
    on 210, which waits on 207; every move of 207 was SOLID, so no rule
    re-solved it and it never warmed - 47 simulated days. The root of the
    chain is served, as the problem its own moves name."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a"], after=["9"]), "9": problem(["b"], after=["8"]),
          "8": problem(["b"])}
    ev = evidence(solve("1", {"a": "clean"}, days_ago=20),
                  solve("8", {"b": "clean"}, days_ago=100))
    st = {"a": (STALE, ago(20)), "b": (SOLID, ago(1))}
    target, status, pnum, why = picker.run(ns, ps, ev, st)
    assert (target, status, pnum) == ("b", SOLID, "8")
    assert "waits on 8" in why


def test_a_held_carrier_behind_a_hard_serves_nothing(picker):
    """A Hard is a summit, not a refresh: the hold rule leaves it alone,
    and the summit rule takes it on its own terms."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a"], after=["9"]), "9": problem(["b"], difficulty="Hard")}
    ev = evidence(solve("1", {"a": "clean"}, days_ago=20))
    st = {"a": (STALE, ago(20)), "b": (SOLID, ago(1))}
    target, status, pnum, why = picker.run(ns, ps, ev, st)
    assert (pnum, "summit" in why) == ("9", True)


def test_every_after_id_in_the_real_graph_resolves(monkeypatch):
    """Every id in an "after" list (problems.json, drills.json) names a
    problem, a bank drill, or a node; every drills.json title names a bank
    file; every bank file has an id; the drill edges have no cycle. A
    dangling id holds nothing, silently; this is where it gets caught."""
    problems = kg_lib.load_problems()
    drills = kg_lib.load_drills()
    monkeypatch.setattr(kg_lib, "_DRILLS", drills)
    bad = []
    for pnum, p in problems.items():
        for pred in p.get("after", []):
            if kg_lib.vertex_kind(pred, problems) is None:
                bad.append((pnum, pred, "nothing carries this id"))
    for did, d in drills.items():
        if not re.fullmatch(r"d\d+", did):
            bad.append((did, "not a drill id"))
        if kg_lib.drill_path(did) is None:
            bad.append((did, d.get("title"), "no bank file"))
        for pred in d.get("after", []):
            if kg_lib.vertex_kind(pred, problems) is None:
                bad.append((did, pred, "nothing carries this id"))
    titles = [d.get("title") for d in drills.values()]
    assert len(titles) == len(set(titles)), "two ids for one title"
    for path in glob.glob(os.path.join(kg_lib.DRILLS_DIR, "*", "*.py")):
        if kg_lib.drill_id(path) is None:
            bad.append((path, "bank file with no id in drills.json"))
    assert not bad, bad

    def cyclic(did, seen=()):
        if did in seen:
            return True
        return any(cyclic(a, seen + (did,)) for a in drills.get(did, {}).get("after", [])
                   if a in drills)
    assert not [t for t in drills if cyclic(t)]


def test_a_carrier_solved_days_ago_is_not_a_spaced_review(picker):
    """The move stayed rusty because the solve did not evidence it, but the
    problem is still in working memory - the picker must not hand back
    yesterday's problem this morning."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"]), "47": problem(["bt"])}
    ev = evidence(solve("46", {}, days_ago=1),
                  solve("47", {"bt": "clean"}, days_ago=300))
    st = {"bt": (STALE, ago(300))}
    assert picker.run(ns, ps, ev, st)[:3] == ("bt", STALE, "47")


def test_every_carrier_still_warm_serves_nothing(picker):
    """When the whole pool is inside the cooldown the node waits its turn -
    better an empty review slot than a rerun of this week's work."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"]), "47": problem(["bt"])}
    ev = evidence(solve("46", {}, days_ago=1), solve("47", {}, days_ago=2))
    st = {"bt": (STALE, ago(300))}
    assert picker.run(ns, ps, ev, st) is None


def test_a_banned_predecessor_holds_nothing_back(picker):
    """If the predecessor can never be offered, the hold would deadlock -
    a banned one releases the edge."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"], banned=True), "47": problem(["bt"], after=["46"])}
    ev = evidence(solve("47", {"bt": "clean"}, days_ago=300))
    st = {"bt": (STALE, ago(300))}
    assert picker.run(ns, ps, ev, st)[:3] == ("bt", STALE, "47")


# --------------------------------------------------------------------------
# the cross-bank ladder: drills gate one another through node prereqs
# --------------------------------------------------------------------------

def test_a_drill_is_held_while_its_banked_prereq_is_not_solid(picker):
    """The dedupe-siblings case: the dependent's drill waits and its carrier
    stays held; the rusty base gets served instead."""
    ns = nodes("base", ("dep", ["base"]))
    ps = {"1": problem(["dep"]), "2": problem(["base"])}
    picker.bank = {"base", "dep"}
    st = {"dep": (FRAGILE, ago(1)), "base": (STALE, ago(50))}
    assert picker.run(ns, ps, {}, st)[:3] == ("base", STALE, "2")


def test_a_prereq_without_a_bank_holds_nothing(picker):
    """A hold nothing can open is a deadlock - an unbanked prereq releases."""
    ns = nodes("base", ("dep", ["base"]))
    ps = {"1": problem(["dep"])}
    picker.bank = {"dep"}
    st = {"dep": (FRAGILE, ago(1)), "base": (STALE, ago(50))}
    assert picker.run(ns, ps, {}, st)[2] == "drill:dep"


def test_a_solid_prereq_releases_the_drill(picker):
    """SOLID standing on an unaided clean - the base is owned."""
    ns = nodes("base", ("dep", ["base"]))
    ps = {"1": problem(["dep"])}
    picker.bank = {"base", "dep"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1))
    st = {"dep": (FRAGILE, ago(1)), "base": (SOLID, ago(1))}
    assert picker.run(ns, ps, ev, st)[2] == "drill:dep"


def test_an_assisted_clean_on_the_prereq_still_holds(picker):
    """If it got assisted then it's not clean: SOLID reached through a
    walkthrough rep is re-learning, not ownership - the dependent waits
    for the unaided rep. And that rep gets SERVED (rule 0c): the prereq is
    SOLID, so rules 1-3 would never target it, and a hold nothing serves
    is a deadlock - 18 nodes sat behind two such prereqs on 2026-08-29."""
    ns = nodes("base", ("dep", ["base"]))
    ps = {"1": problem(["dep"])}
    picker.bank = {"base", "dep"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1, assist="walkthrough"))
    st = {"dep": (FRAGILE, ago(1)), "base": (SOLID, ago(1))}
    target, status, pnum, why = picker.run(ns, ps, ev, st)
    assert (target, status, pnum) == ("base", SOLID, "drill:base")
    assert "own it unaided" in why
    # the dependent is reported as waiting on it, not as a dry node
    (nid, _, why, dry), = picker.blocked(ns, ps, ev, st)
    assert (nid, dry) == ("dep", False)
    assert "held behind base" in why


def test_the_ownership_rep_releasing_the_most_held_moves_goes_first(picker):
    ns = nodes("a", "b", ("d1", ["a"]), ("d2", ["a"]), ("d3", ["b"]))
    ps = {}
    picker.bank = {"a", "b", "d1", "d2", "d3"}
    ev = evidence(solve("9", {"a": "clean", "b": "clean"}, days_ago=1, assist="hint"))
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1)),
          "d1": (MISSING, None), "d2": (MISSING, None), "d3": (MISSING, None)}
    assert picker.run(ns, ps, ev, st)[2] == "drill:a"
    # its drill done for today: the next prereq is served, never the dependents
    picker.drilled_today = {"a"}
    assert picker.run(ns, ps, ev, st)[2] == "drill:b"
    picker.drilled_today = {"a", "b"}
    assert picker.run(ns, ps, ev, st) is None


def test_cram_skips_the_ownership_rep(picker):
    ns = nodes("base", ("dep", ["base"]))
    ps = {}
    picker.bank = {"base", "dep"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1, assist="hint"))
    st = {"dep": (MISSING, None), "base": (SOLID, ago(1))}
    assert picker.run(ns, ps, ev, st, cram=True)[2] == "drill:dep"


def test_early_reviews_solid_nodes_prereqs_first(picker):
    """`make next sql cram early`: nothing rusty in the group, yet every
    SOLID node with a rung left is served, base before dependent."""
    ns = nodes("base", ("dep", ["base"]), "other")
    ps = {}
    picker.bank = {"base", "dep", "other"}
    ev = evidence(solve("9", {"base": "clean", "dep": "clean"}, days_ago=1))
    st = {"base": (SOLID, ago(1)), "dep": (SOLID, ago(1)),
          "other": (SOLID, ago(1))}
    ns["base"]["group"] = ns["dep"]["group"] = "g"
    ns["base"]["group"] = ns["dep"]["group"] = "g"
    ns["other"]["group"] = "elsewhere"
    assert picker.run(ns, ps, ev, st, group="g") is None
    assert picker.run(ns, ps, ev, st, group="g", early=True)[2] == "drill:base"
    picker.drilled_today = {"base"}
    assert picker.run(ns, ps, ev, st, group="g", early=True)[2] == "drill:dep"
    picker.drilled_today = {"base", "dep"}
    assert picker.run(ns, ps, ev, st, group="g", early=True) is None


def test_early_walks_the_ladder_missing_after_its_solid_prereqs(picker):
    """The 2026-08-30 spark serve: `make next spark cram early` jumped
    straight to the MISSING window node. Early means the whole group in
    ladder order - the SOLID prereqs are jogged first, the new move after."""
    ns = nodes("base", ("dep", ["base"]))
    ps = {}
    picker.bank = {"base", "dep"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1))
    st = {"base": (SOLID, ago(1)), "dep": (MISSING, None)}
    ns["base"]["group"] = ns["dep"]["group"] = "g"
    assert picker.run(ns, ps, ev, st, group="g")[2] == "drill:dep"
    assert picker.run(ns, ps, ev, st, group="g", early=True)[2] == "drill:base"
    picker.drilled_today = {"base"}
    assert picker.run(ns, ps, ev, st, group="g", early=True)[2] == "drill:dep"


def test_a_node_whose_only_carrier_is_cooling_is_waiting_not_dry(picker):
    """The 2026-08-29 empty serve: pair-count-formula's one carrier was
    solved three days ago, pick() skipped it as not cooled, and the old
    blocked_frontier (which never applied cooled) called it servable - so
    --why printed nothing and the headline claimed the bank was starved."""
    ns = nodes("t")
    ps = {"2475": problem(["t"], difficulty="Easy")}
    ev = evidence(solve("2475", {"t": "clean"}, days_ago=3))
    st = {"t": (STALE, ago(55))}
    assert picker.run(ns, ps, ev, st) is None
    (nid, _, why, dry), = picker.blocked(ns, ps, ev, st)
    assert (nid, dry) == ("t", False)
    assert "carrier 2475 cools " + iso(-2) in why


def test_a_node_whose_carrier_is_asleep_names_the_park(picker):
    ns = nodes("t")
    ps = {"7": problem(["t"])}
    st = {"t": (STALE, ago(55))}
    (nid, _, why, dry), = picker.blocked(ns, ps, {}, st, asleep={"7"})
    assert (nid, dry) == ("t", False)
    assert "7 is asleep" in why and "make wake" in why


def test_a_pending_plan_drill_for_the_prereq_holds_the_dependent():
    """The plan-serving clause: judgment may order items freely, so a
    dependent's drill item waits while the prereq's item is still pending."""
    from kg.kg_lib import drill_held
    ns = nodes("base", ("dep", ["base"]))
    st = {"base": (SOLID, ago(1)), "dep": (STALE, ago(300))}
    no_bank = lambda nid: False
    assert drill_held("dep", ns, st, {}, has_bank=no_bank, pending={"base"})
    assert not drill_held("dep", ns, st, {}, has_bank=no_bank, pending=set())


def test_a_solid_owned_node_has_no_drill_due(tmp_path, monkeypatch):
    """Drills sit on the same forgetting curve as problems: a node SOLID on
    an unaided clean is not re-served, whatever flagged it - once every
    drill of the node has been done. A never-done drill is still due: one
    clean drill does not stand for the others (2026-08-31, a clean Pairs
    marked start-index solid with five drills, subsets included, untouched)."""
    from kg import kg_lib
    bank = tmp_path / "some-node"
    bank.mkdir()
    (bank / "d0.py").write_text("DRILL: Only One\n")
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    done = {"solved/d_Only_One_1.py": {"date": iso(5), "problem": "drill",
                                       "moves": {"some-node": "clean"}}}
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=2), done)
    assert kg_lib.due_drill("some-node", ev) is None
    assisted = evidence(solve("7", {"some-node": "clean"}, days_ago=2,
                              assist="walkthrough"), done)
    assert kg_lib.due_drill("some-node", assisted) is not None
    undone = evidence(solve("7", {"some-node": "clean"}, days_ago=2))
    assert kg_lib.due_drill("some-node", undone) == str(bank / "d0.py")


def test_an_assisted_rung_with_undone_rungs_above_it_is_served_again(tmp_path, monkeypatch):
    """2026-08-31: Combinations was done once with a walkthrough, so Reuse
    Allowed and Subsets above it stayed held; every released rung had a rep,
    the node read done, and the dedupe drill got served with subsets never
    done. A rung held by the warm rule counts as ladder left, and the
    assisted rung below it is what gets served. A rung held only because
    another node is not owned does not count - nothing here clears it."""
    from kg import kg_lib
    bank = tmp_path / "some-node"
    bank.mkdir()
    (bank / "d0.py").write_text("DRILL: Lower\nTRAINS: some-node\n")
    (bank / "d1.py").write_text("DRILL: Upper\nTRAINS: some-node\n")
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    register(monkeypatch, d1="Lower", d2=("Upper", ["d1"]))
    lower = {"solved/d_Lower_1.py": {"date": iso(5), "problem": "drill",
                                     "moves": {"some-node": "clean"},
                                     "assist": "walkthrough"}}
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=2), lower)
    assert kg_lib.drills_left("some-node", ev)
    assert kg_lib.due_drill("some-node", ev) == str(bank / "d0.py")
    (bank / "d1.py").write_text("DRILL: Upper\nTRAINS: some-node, other\n")
    unaided = {"solved/d_Lower_1.py": {"date": iso(5), "problem": "drill",
                                       "moves": {"some-node": "clean"}}}
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=2), unaided)
    assert not kg_lib.drills_left("some-node", ev)


def test_assisted_serves_only_drills_whose_latest_rep_was_assisted(tmp_path, monkeypatch):
    """2026-08-31: every sql node SOLID, `make next sql` spent, `cram early`
    walking the group from the bottom through drills already owned three
    times over. `assisted` is the early walk restricted to drills whose
    latest rep was a hint, a walkthrough, a learning rep or a struggle: the ones
    still waiting for their unaided rep. Never-done drills are not in it,
    an owned drill is not in it, and the once-a-day rule still holds."""
    from kg import kg_lib
    bank = tmp_path / "some-node"
    bank.mkdir()
    for i, t in enumerate(["Owned", "Hinted", "Learning", "Fresh"]):
        (bank / f"r{i}.py").write_text(f"DRILL: {t}\nTRAINS: some-node\n")
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    reps = {
        "solved/d_Owned_1.py": {"date": iso(3), "problem": "drill",
                                "moves": {"some-node": "clean"}},
        "solved/d_Hinted_1.py": {"date": iso(2), "problem": "drill",
                                 "moves": {"some-node": "clean"},
                                 "assist": "hint"},
        "solved/d_Learning_1.py": {"date": iso(1), "problem": "drill",
                                  "moves": {"some-node": "clean"},
                                  "assist": {"some-node": "learning"}},
    }
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=1), reps)
    assert kg_lib.due_drill("some-node", ev, assisted=True) == str(bank / "r1.py")
    reps["solved/d_Hinted_2.py"] = {"date": iso(0), "problem": "drill",
                                    "moves": {"some-node": "clean"}}
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=1), reps)
    assert kg_lib.due_drill("some-node", ev, assisted=True) == str(bank / "r2.py")
    reps["solved/d_Learning_2.py"] = {"date": iso(0), "problem": "drill",
                                     "moves": {"some-node": "clean"},
                                     "assist": "hint"}
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=1), reps)
    assert kg_lib.due_drill("some-node", ev, assisted=True) is None  # today


def test_assisted_walks_the_group_prereqs_first_whatever_the_status(picker):
    """`assisted` implies early: SOLID nodes are served, prereqs before
    dependents, and the reason names the walk."""
    ns = nodes("base", ("dep", ["base"]))
    for n in ns.values():
        n["group"] = "g"
    picker.bank = {"base", "dep"}
    st = {"base": (SOLID, ago(0)), "dep": (SOLID, ago(0))}
    ev = evidence(solve("7", {"base": "clean", "dep": "clean"}, days_ago=0))
    got = picker.run(ns, {}, ev, st, group="g", assisted=True)
    assert got[2] == "drill:base" and got[3].startswith("assisted review")
    picker.drilled_today = {"base"}
    assert picker.run(ns, {}, ev, st, group="g", assisted=True)[2] == "drill:dep"


def test_picker_serves_the_next_undone_drill_of_a_solid_prereq(picker):
    """2026-08-31: Pairs (two for loops) went clean, start-index read SOLID,
    and the picker served the dedupe drill with subsets never done. A solid
    prereq with drills undone is served its next drill; the dependent waits."""
    ns = nodes("base", ("dep", ["base"]))
    picker.bank = {"base", "dep"}
    picker.undone = {"base"}
    st = {"base": (SOLID, ago(0)), "dep": (FRAGILE, ago(300))}
    ev = evidence(solve("7", {"base": "clean"}, days_ago=0))
    got = picker.run(ns, {}, ev, st)
    assert got[2] == "drill:base" and got[3].startswith("next undone drill")
    picker.undone = set()
    assert picker.run(ns, {}, ev, st)[2] == "drill:dep"


def test_undone_drills_hold_the_dependent_and_get_served(tmp_path, monkeypatch):
    """A prereq node with drills never done does not unlock the node after
    it, and the picker serves the prereq's next undone drill instead."""
    from kg import kg_lib
    bank = tmp_path / "base"
    bank.mkdir()
    (bank / "b0.py").write_text("DRILL: B Zero\nTRAINS: base\n")
    (bank / "b1.py").write_text("DRILL: B One\nTRAINS: base\n")
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    register(monkeypatch, d1="B Zero", d2=("B One", ["d1"]))
    ns = nodes("base", ("dep", ["base"]))
    st = {"base": (SOLID, ago(0)), "dep": (STALE, ago(300))}
    b0 = {"solved/d_B_Zero_1.py": {"date": iso(0), "problem": "drill",
                                   "moves": {"base": "clean"}}}
    ev = evidence(b0)
    assert kg_lib.drill_held("dep", ns, st, ev)
    assert kg_lib.due_drill("base", ev) == str(bank / "b1.py")
    b1 = {"solved/d_B_One_1.py": {"date": iso(0), "problem": "drill",
                                  "moves": {"base": "clean"}}}
    ev2 = evidence(b0, b1)
    assert not kg_lib.drill_held("dep", ns, st, ev2)
    assert kg_lib.due_drill("base", ev2) is None


def test_a_hint_on_one_move_does_not_taint_the_rest_of_the_walk(picker):
    """Assist is per move. 1004 on 2026-08-17: the hint was on the sliding
    window bookkeeping, the prefix sums were the operator's own, yet the
    solve-level flag stamped both, and `owned` then held every drill
    behind prefix-sums for an unaided rep of a move with three unaided
    reps the week before. With {move: level}, only the helped move is
    unowned; the bare-string form still means the whole walk."""
    ev = evidence(solve("1004", {"window": "clean", "prefix": "clean"},
                        days_ago=1, assist={"window": "hint"}))
    assert kg_lib.assist_of(next(iter(ev.values())), "window") == "hint"
    assert kg_lib.assist_of(next(iter(ev.values())), "prefix") == "none"
    assert kg_lib.assist_of(next(iter(ev.values()))) == "hint"  # the solve as a whole
    assert kg_lib.owned("prefix", ev)
    assert not kg_lib.owned("window", ev)
    legacy = evidence(solve("1004", {"window": "clean", "prefix": "clean"},
                            days_ago=1, assist="hint"))
    assert not kg_lib.owned("prefix", legacy)
    # and the picker serves the ownership rep for the helped move only
    ns = nodes("window", "prefix", ("dep", ["window", "prefix"]))
    picker.bank = {"window", "prefix", "dep"}
    st = {"window": (SOLID, ago(1)), "prefix": (SOLID, ago(1)), "dep": (MISSING, None)}
    assert picker.run(ns, {}, ev, st)[2] == "drill:window"
    # prefix is never served as an ownership rep; once window's rep is done
    # for today nothing else is held open (dep waits for that evidence to land)
    picker.drilled_today = {"window"}
    assert picker.run(ns, {}, ev, st) is None


def test_a_learning_move_is_censored_only_for_itself():
    """node_status reads the per-move level too: a learning move earns no
    clean rep, the other move in the same walk does."""
    ev = evidence(solve("9", {"a": "clean", "b": "clean"}, days_ago=1,
                        assist={"a": "learning"}))
    assert kg_lib.node_status("a", ev)[0] == FRAGILE
    assert kg_lib.node_status("b", ev)[0] == SOLID


def test_normalise_assist_stores_the_per_move_shape():
    moves = {"a": "clean", "b": "clean"}
    assert kg_lib.normalise_assist({"a": "hint"}, moves) == {"a": "hint"}
    assert kg_lib.normalise_assist({"a": "hint", "zzz": "hint", "b": "none"}, moves) == {"a": "hint"}
    assert kg_lib.normalise_assist("hint", moves) == {"a": "hint", "b": "hint"}
    assert kg_lib.normalise_assist("none", moves) is None
    assert kg_lib.normalise_assist({}, moves) is None
    assert kg_lib.normalise_assist(None, moves) is None
    assert kg_lib.assist_tag({"b": "hint", "a": "learning"}) == "a=learning, b=hint"


def test_a_composite_rung_waits_for_every_move_it_combines(tmp_path, monkeypatch):
    """A rung whose TRAINS lists a second node is a walk, not a move: it is
    held until that node is owned (its own atomic rung clean, unaided), the
    way a carrier waits for every other move in its walk to be SOLID. The
    ladder below it still applies, and the first rung is never held."""
    from kg import kg_lib
    bank = tmp_path / "left-keep"
    bank.mkdir()
    (bank / "r1.py").write_text('"""\nDRILL: R One\nTRAINS: left-keep\n"""\n')
    (bank / "r2.py").write_text('"""\nDRILL: R Two\nTRAINS: left-keep, group-agg\n"""\n')
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    register(monkeypatch, d1="R One", d2=("R Two", ["d1"]))
    r1, r2 = str(bank / "r1.py"), str(bank / "r2.py")
    # r1 warm (clean, unaided, recent) but group-agg never owned: r2 stays held
    ev = evidence({"solved/d_R_One_1.py": {"date": iso(3), "problem": "drill",
                                           "moves": {"left-keep": "clean"}}})
    assert kg_lib.servable_drills([r1, r2], ev, "left-keep") == [r1]
    # group-agg owned only through a hinted rep: still held
    ev2 = evidence(ev, solve("5", {"group-agg": "clean"}, days_ago=1, assist="hint"))
    assert kg_lib.servable_drills([r1, r2], ev2, "left-keep") == [r1]
    # an unaided clean on group-agg releases it
    ev3 = evidence(ev, solve("5", {"group-agg": "clean"}, days_ago=1))
    assert kg_lib.servable_drills([r1, r2], ev3, "left-keep") == [r1, r2]
    # order of the candidates is not an edge
    assert kg_lib.servable_drills([r2, r1], ev3, "left-keep") == [r2, r1]


# --------------------------------------------------------------------------
# the frontier mover (PLAN.md phase 4): a due node with no evidenced carrier
# promotes a drafted problem from the predicted tier
# --------------------------------------------------------------------------

def test_a_missing_move_with_no_mapped_carrier_promotes_a_draft(picker):
    """The 2026-08-28 dry basecamp: the frontier node's only mapped walk is
    a Hard, but the predicted tier has an easy whose drafted walk needs
    nothing but the target. Promote it instead of starving."""
    ns = nodes("csb")
    ps = {"41": problem(["csb"], difficulty="Hard")}
    st = {"csb": (MISSING, None)}
    picker.predicted["9001"] = drafted(["csb"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    target, status, pnum, reason = picker.run(ns, ps, {}, st)
    assert (target, status, pnum) == ("csb", MISSING, "9001")
    assert "predicted" in reason
    assert ps["9001"]["predicted"] is True  # in-memory entry for rendering
    assert ps["9001"]["moves"] == ["csb"]


def test_drafts_stop_promoting_after_two_misses(picker):
    """The 2026-08-29 carousel: counting-sort-buckets had 56 drafts and the
    mover served them one after another while every solve came back mapped
    to some other move. Two drafted carriers solved without the target
    falsify the tier for it: no third promotion, and the frontier names
    the misses instead of "no drafted walk can carry it"."""
    ns = nodes("csb")
    ps = {"41": problem(["csb"], difficulty="Hard"),
          "1365": problem(["dav"]), "1893": problem(["sa"])}
    st = {"csb": (MISSING, None)}
    for num in ("1365", "1893", "2149"):
        picker.predicted[num] = drafted(["csb"])
        picker.meta[num] = {"difficulty": "Easy"}
    ev = evidence(solve("1365", {"dav": "clean"}, days_ago=1),
                  solve("1893", {"sa": "clean"}, days_ago=0))
    assert picker.run(ns, ps, ev, st) is None
    [(nid, status, why, dry)] = picker.blocked(ns, ps, ev, st)
    assert (nid, status, dry) == ("csb", MISSING, True)
    assert "1365, 1893" in why and "without the move" in why


def test_one_miss_still_promotes(picker):
    """One draft coming back wrong is noise; the tier keeps serving."""
    ns = nodes("csb")
    ps = {"41": problem(["csb"], difficulty="Hard"), "1365": problem(["dav"])}
    st = {"csb": (MISSING, None)}
    for num in ("1365", "1893"):
        picker.predicted[num] = drafted(["csb"])
        picker.meta[num] = {"difficulty": "Easy"}
    ev = evidence(solve("1365", {"dav": "clean"}, days_ago=1))
    assert picker.run(ns, ps, ev, st)[2] == "1893"


def test_a_solve_older_than_the_node_is_not_a_miss(picker):
    """Evidence from before the node existed could not have tagged it
    whatever the walk was, so it does not falsify the draft."""
    ns = nodes("csb")
    ns["csb"]["added"] = iso(10)
    ps = {"41": problem(["csb"], difficulty="Hard"),
          "1365": problem(["dav"]), "1893": problem(["sa"])}
    st = {"csb": (MISSING, None)}
    for num in ("1365", "1893", "2149"):
        picker.predicted[num] = drafted(["csb"])
        picker.meta[num] = {"difficulty": "Easy"}
    ev = evidence(solve("1365", {"dav": "clean"}, days_ago=30),
                  solve("1893", {"sa": "clean"}, days_ago=1))
    assert picker.run(ns, ps, ev, st)[2] == "2149"


def test_an_evidenced_carrier_outranks_promotion(picker):
    """Drafts are 0.80/0.75 guesses; a mapped carrier is truth. Promotion
    fires only when the evidenced bank has nothing."""
    ns = nodes("m")
    ps = {"1": problem(["m"])}
    st = {"m": (FRAGILE, ago(1))}
    picker.predicted["9001"] = drafted(["m"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    assert picker.run(ns, ps, {}, st)[2] == "1"


def test_a_warm_carrier_is_waited_out_not_promoted(picker):
    """A mapped carrier inside the re-solve cooldown is "not today", not
    "never": evidenced truth outranks a drafted guess, so the node waits
    for its carrier to cool instead of promoting."""
    ns = nodes("m")
    ps = {"1": problem(["m"])}
    ev = evidence(solve("1", {"m": "struggled"}, days_ago=1))
    st = {"m": (FRAGILE, ago(1))}
    picker.predicted["9001"] = drafted(["m"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    got = picker.run(ns, ps, ev, st)
    assert got is None or got[2] != "9001"


def test_a_promoted_walk_obeys_the_one_new_move_rule(picker):
    """A drafted walk with a second non-solid move is not a carrier — the
    ZPD constraint applies to the predicted tier unchanged."""
    ns = nodes("t", "alsorusty")
    ps = {"41": problem(["t"], difficulty="Hard")}
    st = {"t": (MISSING, None), "alsorusty": (STALE, ago(60))}
    picker.predicted["9001"] = drafted(["t", "alsorusty"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    pick = picker.run(ns, ps, {}, st)
    assert pick is None or pick[2] != "9001"


def test_a_drafted_hard_is_never_promoted(picker):
    """Hards stay summits even in the predicted tier."""
    ns = nodes("t")
    ps = {}
    st = {"t": (MISSING, None)}
    picker.predicted["9001"] = drafted(["t"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    assert picker.run(ns, ps, {}, st) is None


def test_a_missing_flagged_draft_is_not_promoted(picker):
    """A walk the taxonomy cannot express yet is not a carrier for anything:
    its unexpressed move would ride along as a hidden second gap."""
    ns = nodes("t")
    ps = {}
    st = {"t": (MISSING, None)}
    picker.predicted["9001"] = drafted(["t"], missing=["fenwick-tree"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    assert picker.run(ns, ps, {}, st) is None


def test_promotion_prefers_the_heavily_rehearsed_walk(picker):
    """Cheap regime first: between two qualifying drafts, the one whose
    rarest supporting move has more problems rehearsing it wins (the
    connectivity threshold finding), before problem-number order."""
    ns = nodes("t", "common", "rare")
    ps = {str(i): problem(["common"]) for i in range(1, 6)}
    ps["10"] = problem(["rare"])
    st = {"t": (MISSING, None), "common": (SOLID, ago(1)),
          "rare": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["t", "rare"])
    picker.predicted["9002"] = drafted(["t", "common"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    picker.meta["9002"] = {"difficulty": "Easy"}
    assert picker.run(ns, ps, {}, st)[2] == "9002"


def test_a_stale_move_with_no_carrier_promotes_a_draft(picker):
    """heap-lazy-eviction on 2026-08-28: STALE, only walk is a Hard. The
    spaced re-solve is impossible, so the rep comes from a drafted carrier."""
    ns = nodes("hle")
    ps = {"218": problem(["hle"], difficulty="Hard")}
    st = {"hle": (STALE, ago(50))}
    picker.predicted["9001"] = drafted(["hle"])
    picker.meta["9001"] = {"difficulty": "Medium"}
    target, status, pnum, _ = picker.run(ns, ps, {}, st)
    assert (target, status, pnum) == ("hle", STALE, "9001")


def test_a_promotable_node_is_not_called_blocked(picker):
    """pick() would promote a draft for it, so it is servable, not blocked."""
    ns = nodes("t")
    ps = {"41": problem(["t"], difficulty="Hard")}
    st = {"t": (MISSING, None)}
    picker.predicted["9001"] = drafted(["t"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    assert picker.blocked(ns, ps, {}, st) == []


def test_blocked_report_says_no_draft_can_carry(picker):
    """With the predicted tier empty the blockage message must say the
    drafts were considered and none qualified."""
    ns = nodes("t")
    ps = {"41": problem(["t"], difficulty="Hard")}
    st = {"t": (MISSING, None)}
    (nid, _, why, _), = picker.blocked(ns, ps, {}, st)
    assert nid == "t"
    assert "no drafted walk" in why


def test_early_walks_one_ladder_to_the_top_before_the_node_above_it(picker):
    """The 2026-08-30 spark serve: `make next spark cram early` swept one
    rung per node, so plan-shuffles came round with five group-agg atoms
    unseen. Early is depth first - a dependent waits while an in-scope
    prereq's bank still has an undrilled released rung."""
    ns = nodes("base", ("dep", ["base"]))
    ps = {}
    picker.bank = {"base", "dep"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1, assist="hint"))
    st = {"base": (SOLID, ago(1)), "dep": (MISSING, None)}
    ns["base"]["group"] = ns["dep"]["group"] = "g"
    assert picker.run(ns, ps, ev, st, group="g", early=True)[2] == "drill:base"
    # base repped today but its ladder not done: dep still waits, and the
    # base has nothing due either - the serve is empty, not a skip ahead
    picker.drilled_today = {"base"}
    ladder = {"base"}
    picker_ladder = lambda nid, ev, early=False: nid in ladder
    kg_next.drills_left = picker_ladder
    assert picker.run(ns, ps, ev, st, group="g", early=True) is None
    ladder.clear()
    assert picker.run(ns, ps, ev, st, group="g", early=True)[2] == "drill:dep"


def test_the_cram_ladder_climbs_on_an_assisted_clean(tmp_path, monkeypatch):
    """Outside cram a rung releases the one above only on an unaided clean
    (drill_warm). In the early walk a hinted clean is enough, so a ladder
    is climbed in one sitting instead of one rung per day."""
    from kg import kg_lib
    bank = tmp_path / "group-agg"
    bank.mkdir()
    (bank / "r1.py").write_text('"""\nDRILL: R One\nTRAINS: group-agg\n"""\n')
    (bank / "r2.py").write_text('"""\nDRILL: R Two\nTRAINS: group-agg\n"""\n')
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    register(monkeypatch, d1="R One", d2=("R Two", ["d1"]))
    r1, r2 = str(bank / "r1.py"), str(bank / "r2.py")
    ev = evidence({"solved/d_R_One_1.py": {"date": iso(0), "problem": "drill",
                                           "moves": {"group-agg": "clean"},
                                           "assist": "hint"}})
    assert kg_lib.servable_drills([r1, r2], ev, "group-agg") == [r1]
    assert kg_lib.servable_drills([r1, r2], ev, "group-agg", early=True) == [r1, r2]
    assert kg_lib.due_drill("group-agg", ev, early=True) == r2
    assert kg_lib.drills_left("group-agg", ev, early=True)
    ev2 = evidence(ev, {"solved/d_R_Two_1.py": {"date": iso(0), "problem": "drill",
                                                "moves": {"group-agg": "clean"}}})
    assert not kg_lib.drills_left("group-agg", ev2, early=True)


def test_two_same_day_reps_of_one_drill_do_not_crash_the_ladder(tmp_path, monkeypatch):
    """The 2026-08-30 `make next spark cram early` traceback: two reps of
    one rung on the same date tied on the sort key and the comparison fell
    through to the records. The later solved file (timestamp in its name)
    is the latest rep."""
    from kg import kg_lib
    bank = tmp_path / "n"
    bank.mkdir()
    (bank / "r1.py").write_text('"""\nDRILL: R One\nTRAINS: n\n"""\n')
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    r1 = str(bank / "r1.py")
    ev = {"solved/d_R_One_2026_08_30T01.py": {"date": iso(0), "problem": "drill",
                                             "moves": {"n": "clean"}},
          "solved/d_R_One_2026_08_30T02.py": {"date": iso(0), "problem": "drill",
                                             "moves": {"n": "struggled"}}}
    assert not kg_lib.drill_clean(r1, ev)
    assert not kg_lib.drill_warm(r1, ev)
    ev["solved/d_R_One_2026_08_30T03.py"] = {"date": iso(0), "problem": "drill",
                                            "moves": {"n": "clean"}}
    assert kg_lib.drill_clean(r1, ev)
    assert kg_lib.drill_warm(r1, ev)


def grouped(ns, group, *ids):
    for n in ids:
        ns[n]["group"] = group
    return ns


def test_cram_keeps_the_curve(picker):
    """`make next sql cram` lifts the cross-bank hold and nothing else: a
    SOLID node owned by an unaided clean is still not re-served. That is
    what `early` adds."""
    ns = grouped(nodes("base"), "g", "base")
    picker.bank = {"base"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1))
    st = {"base": (SOLID, ago(1))}
    picker.drilled_today = set()
    # due_drill (stubbed) follows the real one: an owned SOLID node is not
    # due outside early, so neither the curve nor cram serves it
    monkeypatch_due = lambda nid, ev, today=None, early=False, assisted=False: (
        f"drills/{nid}/one.py" if early else None)
    kg_next.due_drill = monkeypatch_due
    assert picker.run(ns, {}, ev, st, group="g", cram=True) is None
    assert picker.run(ns, {}, ev, st, group="g", early=True)[2] == "drill:base"


def test_cram_stays_inside_the_group(picker):
    """The group scope survives cram: a held node in another group is not
    what `make next sql cram` releases."""
    ns = grouped(nodes("base", ("dep", ["base"]), ("far", ["base"])),
                 "g", "base", "dep")
    ns["far"]["group"] = "elsewhere"
    picker.bank = {"base", "dep", "far"}
    ev = evidence(solve("9", {"base": "clean"}, days_ago=1, assist="hint"))
    st = {"base": (SOLID, ago(1)), "dep": (MISSING, None), "far": (MISSING, None)}
    assert picker.run(ns, {}, ev, st, group="g", cram=True)[2] == "drill:dep"
    picker.drilled_today = {"dep"}
    assert picker.run(ns, {}, ev, st, group="g", cram=True) is None


def test_cram_lifts_the_ownership_bar_not_the_solid_one(picker):
    """Cram drops the "prereq owned by an unaided rep" hold only. A prereq
    that is not SOLID at all is the more urgent gap: it is served first,
    and the MISSING dependent still waits for it to turn SOLID - the ZPD
    rule, which cram does not touch."""
    ns = grouped(nodes("base", ("dep", ["base"])), "g", "base", "dep")
    picker.bank = {"base", "dep"}
    ev = evidence(solve("9", {"base": "struggled"}, days_ago=1))
    st = {"base": (FRAGILE, ago(1)), "dep": (MISSING, None)}
    assert picker.run(ns, {}, ev, st, group="g", cram=True)[2] == "drill:base"
    picker.drilled_today = {"base"}
    assert picker.run(ns, {}, ev, st, group="g", cram=True) is None
    st["base"] = (SOLID, ago(0))
    assert picker.run(ns, {}, ev, st, group="g", cram=True)[2] == "drill:dep"


def test_early_walks_a_chain_bottom_up_one_ladder_at_a_time(picker):
    """a -> b -> c in one group: a's whole ladder, then b's, then c's. c is
    held by b's unfinished ladder even while a is done, so the walk never
    skips a level."""
    ns = grouped(nodes("a", ("b", ["a"]), ("c", ["b"])), "g", "a", "b", "c")
    picker.bank = {"a", "b", "c"}
    ev = evidence(solve("9", {"a": "clean", "b": "clean"}, days_ago=1))
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1)), "c": (MISSING, None)}
    ladder = {"a", "b", "c"}
    kg_next.drills_left = lambda nid, ev, early=False: nid in ladder
    assert picker.run(ns, {}, ev, st, group="g", early=True)[2] == "drill:a"
    picker.drilled_today = {"a"}
    assert picker.run(ns, {}, ev, st, group="g", early=True) is None
    ladder.discard("a")
    assert picker.run(ns, {}, ev, st, group="g", early=True)[2] == "drill:b"
    picker.drilled_today = {"a", "b"}
    assert picker.run(ns, {}, ev, st, group="g", early=True) is None
    ladder.discard("b")
    assert picker.run(ns, {}, ev, st, group="g", early=True)[2] == "drill:c"


def test_early_is_not_held_by_a_prereq_outside_the_group(picker):
    """A spark node's sql prereqs are out of scope for `make next spark
    cram early`: their unfinished ladders do not hold the spark walk, and
    they are never served by it."""
    ns = grouped(nodes("sql-base", ("spark-dep", ["sql-base"])), "spark", "spark-dep")
    ns["sql-base"]["group"] = "sql"
    picker.bank = {"sql-base", "spark-dep"}
    ev = evidence(solve("9", {"sql-base": "clean"}, days_ago=1, assist="hint"))
    st = {"sql-base": (SOLID, ago(1)), "spark-dep": (MISSING, None)}
    kg_next.drills_left = lambda nid, ev, early=False: True
    assert picker.run(ns, {}, ev, st, group="spark", early=True)[2] == "drill:spark-dep"


def test_early_with_two_picks_moves_on_to_the_next_ladder(picker):
    """`make next sql cram early` with -n 2: the second pick excludes the
    first drill and goes to the next node in ladder order, not the same
    node twice."""
    ns = grouped(nodes("a", "b"), "g", "a", "b")
    picker.bank = {"a", "b"}
    ev = evidence(solve("9", {"a": "clean", "b": "clean"}, days_ago=1))
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    first = picker.run(ns, {}, ev, st, group="g", early=True)
    assert first[2] == "drill:a"
    second = picker.run(ns, {}, ev, st, group="g", early=True, exclude={"drill:a"})
    assert second[2] == "drill:b"


def test_prepare_loads_the_exact_drill_file_the_pick_chose(monkeypatch, tmp_path):
    """The 2026-08-30 spark-join circle: `make next spark cram early
    prepare` printed r3 and then handed the NODE to utils/kg/drill, which
    re-picked under the everyday ladder rule and loaded r1 again. Prepare
    gets the file path the pick printed."""
    ns = nodes("j")
    ns["j"]["group"] = "g"
    path = "drills/j/r3_third.py"
    calls = []
    for name, fn in {
        "load_nodes": lambda: ns,
        "load_problems": lambda: {},
        "load_evidence": lambda: {},
        "node_status": lambda n, ev, today=None: (SOLID, ago(1)),
        "immature_nodes": lambda nodes, ev, problems: frozenset(),
        "sleep_state": lambda nodes, problems, ev: ({}, {}),
        "is_session_start": lambda: False,
        "solved_today_pnums": lambda: [],
        "pick": lambda *a, **k: ("j", SOLID, "drill:j", "early review"),
        "due_drill": lambda nid, ev, today=None, early=False, assisted=False: path,
        "drill_title": lambda p: "Third",
        "drill_forecast": lambda p: None,
        "animate": lambda text: None,
    }.items():
        monkeypatch.setattr(kg_next, name, fn)
    monkeypatch.setattr(kg_next, "_iss",
                        lambda: type("S", (), {"solve_seconds_today": lambda self: 0})())
    monkeypatch.setattr(kg_next, "REPO_ROOT", str(tmp_path))  # empty current.py
    monkeypatch.setattr(kg_next.subprocess, "run",
                        lambda cmd, **kw: calls.append(cmd[-1]))
    monkeypatch.setattr(sys, "argv",
                        ["kg_next", "--group=g", "--early", "--prepare", "--no-show"])
    kg_next.main()
    assert calls == [path]


# --------------------------------------------------------------------------
# rule 5: widen reach - a young move is proved on a real problem
# --------------------------------------------------------------------------

def test_a_young_move_is_proved_when_nothing_else_is_due(picker):
    """Every node SOLID, no summit ready, so the picker used to say nothing.
    Reach against the drafted catalog says otherwise: `b` is SOLID but
    young, and drafted problems wait on it. Serve the Medium that carries
    it with every other move SOLID - the rep that matures it."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"]), "2": problem(["a"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.immature.add("b")
    picker.gain = {"b": 40}
    target, status, pnum, reason = picker.run(ns, ps, {}, st)
    assert (target, status, pnum) == ("b", SOLID, "1")
    assert "40" in reason


def test_the_young_move_with_the_most_reach_goes_first(picker):
    ns = nodes("a", "b", "c")
    ps = {"1": problem(["a", "b"]), "2": problem(["a", "c"])}
    st = {n: (SOLID, ago(1)) for n in ns}
    picker.immature |= {"b", "c"}
    picker.gain = {"b": 5, "c": 90}
    assert picker.run(ns, ps, {}, st)[2] == "2"


def test_a_young_move_nobody_waits_on_is_not_served(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.immature.add("b")
    picker.gain = {}
    assert picker.run(ns, ps, {}, st) is None


def test_a_summit_still_outranks_the_reach_rule(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"]), "76": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.immature.add("b")
    picker.gain = {"b": 40}
    assert picker.run(ns, ps, {}, st)[2] == "76"


def test_a_medium_bar_young_move_promotes_a_drafted_medium_not_an_easy(picker):
    """The only evidenced carrier of `b` is a Medium, so its bar is Medium;
    that carrier is warm, so the rule widens to the drafted tier - and an
    easy there is not proof at the bar, so the Medium draft is promoted."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    ev = evidence(solve("1", {"a": "clean", "b": "clean"}, days_ago=1))
    picker.immature.add("b")
    picker.gain = {"b": 40}
    picker.predicted["9001"] = drafted(["a", "b"])
    picker.meta["9001"] = {"difficulty": "Easy"}
    picker.predicted["9002"] = drafted(["a", "b"])
    picker.meta["9002"] = {"difficulty": "Medium"}
    target, status, pnum, reason = picker.run(ns, ps, ev, st)
    assert (target, pnum) == ("b", "9002")
    assert ps["9002"]["predicted"] is True
    assert "drafted" in reason


def test_a_counted_carrier_yields_to_a_drafted_medium(picker):
    """102 on 2026-09-01: the only evidenced Medium carrier of `b` had
    already given it a clean rep, and cooled, so rule 5 served it again
    while 18 drafted Mediums waited. A second rep of the same problem
    proves memory of that problem, not carry: a draft goes first."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    ev = evidence(solve("1", {"a": "clean", "b": "clean"}, days_ago=10))
    picker.immature.add("b")
    picker.gain = {"b": 18}
    picker.predicted["9002"] = drafted(["a", "b"])
    picker.meta["9002"] = {"difficulty": "Medium"}
    target, status, pnum, reason = picker.run(ns, ps, ev, st)
    assert (target, pnum) == ("b", "9002")


def test_a_counted_carrier_is_re_solved_when_no_draft_exists(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    ev = evidence(solve("1", {"a": "clean", "b": "clean"}, days_ago=10))
    picker.immature.add("b")
    picker.gain = {"b": 18}
    target, status, pnum, reason = picker.run(ns, ps, ev, st)
    assert (target, pnum) == ("b", "1")
    assert "re-solve" in reason


def test_a_fresh_evidenced_carrier_still_outranks_a_draft(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"]), "2": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    ev = evidence(solve("1", {"a": "clean", "b": "clean"}, days_ago=10))
    picker.immature.add("b")
    picker.gain = {"b": 18}
    picker.predicted["9002"] = drafted(["a", "b"])
    picker.meta["9002"] = {"difficulty": "Medium"}
    assert picker.run(ns, ps, ev, st)[2] == "2"


def test_a_young_move_with_falsified_drafts_is_skipped(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.immature.add("b")
    picker.gain = {"b": 40}
    for n in ("9001", "9002", "9003"):
        picker.predicted[n] = drafted(["a", "b"])
        picker.meta[n] = {"difficulty": "Medium"}
    # 9001 and 9002 solved without b: the drafts are wrong about this move
    ev = evidence(solve("1", {"a": "clean", "b": "clean"}, days_ago=1),
                  solve("9001", {"a": "clean"}, days_ago=3),
                  solve("9002", {"a": "clean"}, days_ago=4))
    assert picker.run(ns, ps, ev, st) is None


def test_unlocks_counts_a_young_move_as_a_gap():
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    pred = {"9001": drafted(["a", "b"]), "9002": drafted(["a"])}
    assert kg_lib.unlocks(st, {}, predicted=pred) == {}
    assert kg_lib.unlocks(st, {}, predicted=pred, immature={"b"}) == {"b": 1}


# --------------------------------------------------------------------------
# rule 6: an unsolved drafted problem in reach, Hards first
# --------------------------------------------------------------------------

def test_a_solid_graph_serves_an_unsolved_drafted_hard(picker):
    """The 2026-08-31 simulation: 180 days of a solid graph, one Hard
    served, P(onsite) flat. Once nothing is rusty, new, young or a mapped
    summit, what is left is the drafted catalog itself."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["a", "b"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    target, status, pnum, reason = picker.run(ns, ps, {}, st)
    assert (status, pnum) == (SOLID, "9001")
    assert ps["9001"]["predicted"] is True
    assert "in reach" in reason


def test_drafted_hards_and_mediums_alternate_within_a_day(picker):
    """A Hard opens the day; after a Hard solved today the next pick is a
    Medium, after that Medium a Hard again. Easies come last either way."""
    ns = nodes("a")
    ps = {"1": problem(["a"])}
    st = {"a": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["a"])
    picker.meta["9001"] = {"difficulty": "Medium"}
    picker.predicted["9002"] = drafted(["a"])
    picker.meta["9002"] = {"difficulty": "Hard"}
    picker.predicted["9003"] = drafted(["a"])
    picker.meta["9003"] = {"difficulty": "Easy"}
    assert picker.run(ns, ps, {}, st)[2] == "9002"
    ps["9002"] = problem(["a"], difficulty="Hard")
    ev = evidence(solve("9002", {"a": "clean"}, days_ago=0))
    assert picker.run(ns, ps, ev, st, exclude={"9002"})[2] == "9001"
    ps["9001"] = problem(["a"])
    ev.update(solve("9001", {"a": "clean"}, days_ago=0))
    assert picker.run(ns, ps, ev, st, exclude={"9002", "9001"})[2] == "9003"


def test_a_drafted_problem_on_a_young_move_is_not_in_reach(picker):
    ns = nodes("a", "b")
    ps = {"1": problem(["a", "b"])}
    st = {"a": (SOLID, ago(1)), "b": (SOLID, ago(1))}
    picker.immature.add("b")
    picker.predicted["9001"] = drafted(["a", "b"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    picker.predicted["9002"] = drafted(["a"])
    picker.meta["9002"] = {"difficulty": "Easy"}
    assert picker.run(ns, ps, {}, st)[2] == "9002"


def test_a_missing_flagged_draft_is_never_in_reach(picker):
    ns = nodes("a")
    ps = {"1": problem(["a"])}
    st = {"a": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["a"], missing=["some-trick"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    assert picker.run(ns, ps, {}, st) is None


def test_a_mapped_summit_outranks_a_drafted_one(picker):
    ns = nodes("a")
    ps = {"76": problem(["a"], difficulty="Hard")}
    st = {"a": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["a"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    assert picker.run(ns, ps, {}, st)[2] == "76"


def test_a_drafted_problem_solved_today_is_skipped(picker):
    ns = nodes("a")
    ps = {"1": problem(["a"])}
    st = {"a": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["a"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    assert picker.run(ns, ps, {}, st, exclude={"9001"}) is None


def test_a_group_pick_never_reaches_into_the_drafted_catalog(picker):
    ns = {"a": {"id": "a", "prereqs": [], "group": "sql"}}
    ps = {"1": problem(["a"])}
    st = {"a": (SOLID, ago(1))}
    picker.predicted["9001"] = drafted(["a"])
    picker.meta["9001"] = {"difficulty": "Hard"}
    assert picker.run(ns, ps, {}, st, group="sql") is None


def test_the_first_rep_of_a_drill_is_unaided_at_the_node(tmp_path, monkeypatch):
    """A new drill on a known move (Reuse Allowed on start-index, 2026-09-01):
    he copied the answer. That is first exposure to the drill, not a failed
    recall of the move, so the node keeps ownership and the copy counts as
    a clean rep; the same help on the drill's SECOND rep is a real assist.
    The drill itself still waits for an unaided rep either way."""
    drill_bank(tmp_path, monkeypatch, "sw", "Count by Contribution")
    ps = {"713": problem(["sw"], after=["d1"])}
    ev = evidence(solve("9", {"sw": "clean"}, days_ago=20),
                  drill_rep("Count by Contribution", "sw", days_ago=1, assist="learning"))
    assert kg_lib.owned("sw", ev)
    assert kg_lib.node_status("sw", ev)[1].isoformat() == iso(1)
    assert kg_lib.held_behind("713", ps, ev) == "d1"
    second = evidence(ev, drill_rep("Count by Contribution", "sw", days_ago=0, assist="hint"))
    assert not kg_lib.owned("sw", second)


# --------------------------------------------------------------------------
# review_ahead: the review between now and the first pick that is new ground
# --------------------------------------------------------------------------

@pytest.fixture
def flat_window(monkeypatch):
    """No fitted curve: SOLID for SOLID_WINDOW_DAYS after a clean rep, then
    STALE. review_ahead derives statuses from evidence, so the synthetic
    evidence has to land where the test says."""
    monkeypatch.setattr(kg_lib, "_load_curve", lambda: None)


def test_review_ahead_counts_a_gated_drill_before_the_summit(picker, flat_window):
    """A fragile move with a bank: one clean drill clears it, and the Hard
    whose walk is then all solid is new ground. One drill, no problems."""
    ns = nodes("a", "b")
    ps = {"1": problem(["a"]), "2": problem(["a", "b"], difficulty="Hard")}
    picker.bank = {"a"}
    ev = evidence(solve("1", {"a": "struggled"}, days_ago=1),
                  solve("3", {"b": "clean"}, days_ago=1))
    assert kg_next.review_ahead(ns, ps, ev) == (1, 0, True)


def test_review_ahead_counts_a_stale_re_solve_as_a_problem(picker, flat_window):
    """An ordinary stale move re-solves its carrier: that is one problem of
    review, then the summit."""
    ns = nodes("a")
    ps = {"1": problem(["a"]), "2": problem(["a"], difficulty="Hard")}
    ev = evidence(solve("1", {"a": "clean"}, days_ago=kg_lib.SOLID_WINDOW_DAYS + 5))
    assert kg_next.review_ahead(ns, ps, ev) == (0, 1, True)


def test_review_ahead_is_zero_when_the_pick_is_new_ground(picker, flat_window):
    """Every move solid: the first pick is already the summit."""
    ns = nodes("a")
    ps = {"2": problem(["a"], difficulty="Hard")}
    ev = evidence(solve("1", {"a": "clean"}, days_ago=1))
    assert kg_next.review_ahead(ns, ps, ev) == (0, 0, True)


def test_review_ahead_follows_a_released_dependent(picker, flat_window):
    """The granted rep changes what is served next: once the prereq's drill
    is clean the dependent it held gets its own drill. Two drills, then
    new ground."""
    ns = nodes("a", ("b", ["a"]))
    ps = {"2": problem(["a", "b"], difficulty="Hard")}
    picker.bank = {"a", "b"}
    ev = evidence(solve("1", {"a": "struggled", "b": "struggled"}, days_ago=1))
    assert kg_next.review_ahead(ns, ps, ev) == (2, 0, True)


def test_review_ahead_restores_the_clock(picker, flat_window):
    ns = nodes("a")
    ps = {"2": problem(["a"], difficulty="Hard")}
    kg_next.review_ahead(ns, ps, {})
    assert kg_lib.date.today() == date.today()
    assert kg_next.date is date


def test_review_line_wording():
    assert kg_next.review_line(2, 1, True) == \
        "review ahead: 2 drills, 1 problem, then new ground (if every rep is clean)"
    assert kg_next.review_line(0, 0, True) == \
        "review ahead: none - this pick is new ground"
    assert kg_next.review_line(3, 0, False) == \
        "review ahead: 3 drills, and still nothing new (if every rep is clean)"


def test_the_level_word_in_the_notes_is_the_mark():
    """2026-09-01: a drill whose notes read "Asked for a walkthrough." was
    filed with no assist because the judge did not act on the note. The
    word in the notes is authoritative; the judge's answer is a floor."""
    assert kg_lib.notes_assist_level("Asked for a walkthrough.") == "walkthrough"
    assert kg_lib.notes_assist_level("one hint on the pop") == "hint"
    assert kg_lib.notes_assist_level("hinted, then walked through") == "walkthrough"
    assert kg_lib.notes_assist_level("learning rep, copied the solution") == "learning"
    assert kg_lib.notes_assist_level("") == "none"
    assert kg_lib.notes_assist_level(None) == "none"
    assert kg_lib.notes_assist_level("solved it cold") == "none"
    # the floor lands on the drill's TRAINS node and raises, never lowers
    assert kg_lib.apply_assist_floor(None, "walkthrough", ["a"]) == {"a": "walkthrough"}
    assert kg_lib.apply_assist_floor({"a": "hint"}, "walkthrough", ["a"]) == {"a": "walkthrough"}
    assert kg_lib.apply_assist_floor({"a": "learning"}, "hint", ["a"]) == {"a": "learning"}
    assert kg_lib.apply_assist_floor({"b": "hint"}, "walkthrough", ["a"]) == {"a": "walkthrough", "b": "hint"}
    assert kg_lib.apply_assist_floor({"a": "hint"}, "none", ["a"]) == {"a": "hint"}
    assert kg_lib.apply_assist_floor(None, "none", ["a"]) is None


# --------------------------------------------------------------------------
# rule 0b: a full park withholds new ground, review still flows
# --------------------------------------------------------------------------

def test_a_full_park_withholds_new_ground_but_not_review(monkeypatch):
    """2026-09-01: four problems asleep, cap three, and make next kept
    serving as if nothing were parked. At the cap a new-ground pick is
    held back; a review pick is not."""
    monkeypatch.setattr(kg_next, "MAX_ASLEEP", 3)
    full = {"1", "2", "3"}
    new_move = ("m", MISSING, "9", "new move")
    summit = ("m", SOLID, "9", "summit: gentlest all-solid Hard")
    review = ("m", STALE, "9", "spaced re-solve")
    assert kg_next.withheld(new_move, full)
    assert kg_next.withheld(summit, full)
    assert not kg_next.withheld(review, full)
    assert not kg_next.withheld(new_move, {"1", "2"})
    assert not kg_next.withheld(None, full)


def test_the_park_full_message_names_the_ways_out(monkeypatch):
    monkeypatch.setattr(kg_next, "MAX_ASLEEP", 3)
    ps = {"1235": problem(["a"], title="Job Scheduling"),
          "752": problem(["a"], title="Open the Lock")}
    lines = kg_next.park_full_lines({"1235", "752"}, ps)
    assert len(lines) == 1 and lines[0].startswith("2 asleep (cap 3)")
    assert "make wake" in lines[0] and "make failed" in lines[0] and "learning" in lines[0]


def test_the_park_is_listed_under_every_make_next(monkeypatch):
    """2026-09-01: the park must be seen daily, not only when make sleep
    refuses. sleep_lines is what make next prints at the bottom and what
    make sleep -- --list prints; one line per park."""
    ns = nodes("a", "b")
    ps = {"7": problem(["a", "b"], title="Parked One")}
    monkeypatch.setattr(kg_lib, "sleep_records",
                        lambda problems, ev: {"7": {"branch": "7-slept", "title": "Parked One",
                                                    "slept": 1_756_000_000, "cycles": 2}})
    monkeypatch.setattr(kg_lib, "sleep_state", lambda nodes, problems, ev: (["7"], []))
    st = {"a": (SOLID, ago(1)), "b": (STALE, ago(40))}
    lines = kg_lib.sleep_lines(ns, ps, {}, st)
    assert len(lines) == 1
    assert lines[0].startswith("7. Parked One - asleep (warming: b)")
    assert "slept x2" in lines[0] and lines[0].endswith("make wake 7 when you choose")
    st["b"] = (SOLID, ago(1))
    assert "ground solid, simmering" in kg_lib.sleep_lines(ns, ps, {}, st)[0]
    monkeypatch.setattr(kg_lib, "sleep_records", lambda problems, ev: {})
    assert kg_lib.sleep_lines(ns, ps, {}, st) == []


def test_envrc_knobs_hold_without_direnv(tmp_path):
    """The repo's .envrc is read like a dotenv file: literal exports are
    taken, shell expansions are left alone, the environment wins."""
    rc = tmp_path / ".envrc"
    rc.write_text(
        "export MAX_ASLEEP=5\n"
        "# a comment\n"
        "\n"
        "export NAME=\"quoted value\"\n"
        "SINGLE='x$y'\n"
        "export PYTHONPATH=./utils/:${PYTHONPATH}\n"
        "export SET_ALREADY=new\n"
        "not a var line\n"
    )
    env = {"SET_ALREADY": "old"}
    loaded = kg_lib.load_envrc(str(rc), env)
    assert loaded == {"MAX_ASLEEP": "5", "NAME": "quoted value", "SINGLE": "x$y"}
    assert env["SET_ALREADY"] == "old"
    assert "PYTHONPATH" not in env
    assert kg_lib.load_envrc(str(tmp_path / "missing"), {}) == {}
