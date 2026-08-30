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

import os
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
                           "unlocks": {}, "immature": set()})()

    monkeypatch.setattr(kg_next, "drill_gated",
                        lambda nid, status, last, today=None:
                        nid in ctl.bank and status in (FRAGILE, MISSING))
    monkeypatch.setattr(kg_next, "unlocks", lambda statuses, problems: ctl.unlocks)
    monkeypatch.setattr(kg_next, "due_drill",
                        lambda nid, ev, today=None, early=False:
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
                        lambda target, problems, statuses, nodes, skip=():
                        kg_lib.predicted_carrier(target, problems, statuses,
                                                 nodes, predicted=ctl.predicted,
                                                 skip=skip))
    monkeypatch.setattr(kg_next, "draft_misses",
                        lambda target, ev, nodes=None, predicted=None:
                        kg_lib.draft_misses(target, ev, nodes, ctl.predicted))
    monkeypatch.setattr(kg_next, "drafts_falsified",
                        lambda target, ev, nodes=None, predicted=None:
                        kg_lib.drafts_falsified(target, ev, nodes, ctl.predicted))
    monkeypatch.setattr(kg_next, "has_drill_bank", lambda nid: nid in ctl.bank)
    monkeypatch.setattr(kg_next, "ladder_left",
                        lambda nid, ev, early=False:
                        nid in ctl.bank and nid not in ctl.drilled_today)
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


def test_a_spoiled_predecessor_solve_does_not_release(picker):
    """A spoiled rep is not recall evidence anywhere else either."""
    ns = nodes("bt")
    ps = {"46": problem(["bt"]), "47": problem(["bt"], after=["46"])}
    ev = evidence(solve("46", {"bt": "clean"}, days_ago=10, assist="spoiled"),
                  solve("46", {"bt": "clean"}, days_ago=299),
                  solve("47", {"bt": "clean"}, days_ago=300))
    st = {"bt": (STALE, ago(299))}
    assert picker.run(ns, ps, ev, st)[:3] == ("bt", STALE, "46")


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
    an unaided clean is not re-served, whatever flagged it."""
    from kg import kg_lib
    bank = tmp_path / "some-node"
    bank.mkdir()
    (bank / "d0.py").write_text("pass\n")
    monkeypatch.setattr(kg_lib, "DRILLS_DIR", str(tmp_path))
    ev = evidence(solve("7", {"some-node": "clean"}, days_ago=2))
    assert kg_lib.due_drill("some-node", ev) is None
    assisted = evidence(solve("7", {"some-node": "clean"}, days_ago=2,
                              assist="walkthrough"))
    assert kg_lib.due_drill("some-node", assisted) is not None


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
    r1, r2 = str(bank / "r1.py"), str(bank / "r2.py")
    # r1 warm (clean, unaided, recent) but group-agg never owned: r2 stays held
    ev = evidence({"solved/d_R_One_1.py": {"date": iso(3), "problem": "drill",
                                           "moves": {"left-keep": "clean"}}})
    assert kg_lib.released_rungs([r1, r2], ev, "left-keep") == [r1]
    # group-agg owned only through a hinted rep: still held
    ev2 = evidence(ev, solve("5", {"group-agg": "clean"}, days_ago=1, assist="hint"))
    assert kg_lib.released_rungs([r1, r2], ev2, "left-keep") == [r1]
    # an unaided clean on group-agg releases it
    ev3 = evidence(ev, solve("5", {"group-agg": "clean"}, days_ago=1))
    assert kg_lib.released_rungs([r1, r2], ev3, "left-keep") == [r1, r2]
    # the first rung is never held by its own TRAINS list
    assert kg_lib.released_rungs([r2, r1], ev, "left-keep") == [r2]


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
    kg_next.ladder_left = picker_ladder
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
    r1, r2 = str(bank / "r1.py"), str(bank / "r2.py")
    ev = evidence({"solved/d_R_One_1.py": {"date": iso(0), "problem": "drill",
                                           "moves": {"group-agg": "clean"},
                                           "assist": "hint"}})
    assert kg_lib.released_rungs([r1, r2], ev, "group-agg") == [r1]
    assert kg_lib.released_rungs([r1, r2], ev, "group-agg", early=True) == [r1, r2]
    assert kg_lib.due_drill("group-agg", ev, early=True) == r2
    assert kg_lib.ladder_left("group-agg", ev, early=True)
    ev2 = evidence(ev, {"solved/d_R_Two_1.py": {"date": iso(0), "problem": "drill",
                                                "moves": {"group-agg": "clean"}}})
    assert not kg_lib.ladder_left("group-agg", ev2, early=True)


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
