"""The simulation runs the real picker (kg_next.pick) forward on the real
graph and evidence, so it is the one test that sees the picker's rules
interact: a hold that nothing clears, a sort key that lets the summit
fallback outrank a repair, a drill that is served and never lands. Each
of those shows up as nodes that go STALE or FRAGILE and stay there.

Two guards on a 60-day run at a fixed pace and seed:

  - the number of rusty nodes at the start of a day stays under a cap. The
    picker repairs a rusty node within days, so the count stays small no
    matter how many go rusty; a picker that stops repairing lets it climb.
  - no node stays rusty for STARVED_DAYS in a row. This one is a known
    failure today (2026-08-31): a STALE node whose only carrier is held
    behind the node's own drill (102 after d67) is not drill-gated, so the
    drill is never offered, and its drafted carriers are falsified, so
    the stale rule skips it until it goes deep-stale. Marked xfail strict:
    when the picker is fixed the test passes and pytest fails on the
    marker, which is the signal to remove it.

The run depends on graph/*.json and the fitted curve, both of which change
with every solve, so the caps carry a margin over what was observed.
"""

import os
from importlib.machinery import SourceFileLoader

import pytest

KG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kg")
kg_simulate = SourceFileLoader("kg_simulate", os.path.join(KG, "kg_simulate")).load_module()

from kg import kg_lib  # noqa: E402

DAYS = 60
HOURS = 1.5
SEED = 1
RUSTY_CAP = 14  # observed 11-12 over seeds 1-3 on 2026-08-31, day 1 excluded


@pytest.fixture(scope="module")
def run():
    if not kg_lib._load_curve():
        pytest.skip("graph/curve.json missing - run make curve first")
    return kg_simulate.run(hours=HOURS, seed=SEED, days=DAYS, log=lambda *a: None)


def test_run_restores_kg_lib_clock(run):
    """A run freezes kg_lib's date day by day; after it, today is today."""
    from datetime import date
    assert kg_lib.date.today() == date.today()


def test_picker_never_dry(run):
    assert run["dry_days"] == 0, f"{run['dry_days']} days the picker served nothing"


def test_rusty_nodes_bounded(run):
    """Day 1 is the real state of the graph today, before the picker has
    acted; from day 2 the count is the picker's own doing."""
    worst = max((s + f, d) for d, s, f, _ in run["rusty"] if d > 1)
    assert worst[0] <= RUSTY_CAP, (
        f"{worst[0]} nodes STALE or FRAGILE at the start of day {worst[1]} "
        f"(cap {RUSTY_CAP}); the picker is not repairing what goes rusty")


@pytest.mark.xfail(strict=True, reason=(
    "known starvation (2026-08-31): a STALE node whose only carrier is held "
    "behind its own drill, with falsified drafts, is served by nothing until "
    "deep-stale (tree-bfs-levels, backtracking-mark-unmark, ...)"))
def test_no_node_starves(run):
    assert not run["starved"], "rusty for %d+ days in a row: %s" % (
        kg_simulate.STARVED_DAYS,
        ", ".join(f"{n} ({k}d, picked {p}x)"
                  for n, (k, p) in sorted(run["starved"].items(), key=lambda x: -x[1][0])))
