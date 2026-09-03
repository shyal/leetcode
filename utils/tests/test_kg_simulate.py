"""The simulation runs the real picker (kg_next.pick) forward on the real
graph and evidence, so it is the one test that sees the picker's rules
interact: a hold that nothing clears, a sort key that lets the summit
fallback outrank a repair, a drill that is served and never lands. Each
of those shows up as nodes that go STALE or FRAGILE and stay there.

Two guards on a 60-day run at a fixed pace and seed:

  - the number of rusty nodes at the start of a day stays under a cap. The
    picker repairs a rusty node within days, so the count stays small no
    matter how many go rusty; a picker that stops repairing lets it climb.
  - no node stays rusty for STARVED_DAYS in a row with no pick aimed at
    it. A node picked and failed again and again is the draw, not the
    picker; a node nothing is aimed at is a hold nothing clears. Three
    such holds failed this on 2026-08-31 and were fixed the same day: a
    STALE node whose every carrier is held behind a drill (102 after d67)
    got no drill from the stale rule; rule 0c gave up on a prereq that was
    itself held instead of climbing to the root of the chain; a node whose
    carriers wait on a problem with every move SOLID (310 after 210 after
    207) had nothing re-solve that problem.

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
RUSTY_CAP = 10  # observed 5-8 over seeds 1-5 on 2026-08-31, day 1 excluded


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


def test_series_one_row_per_day(run):
    """The README forecast chart (utils/readme/kg_forecast_svg) reads the
    per-day series: one row per simulated day, the day's solves summing to
    the run's totals, the last row's onsite the run's."""
    s = run["series"]
    assert len(s) == run["day"]
    assert [d["day"] for d in s] == sorted(d["day"] for d in s)
    for kind, n in run["per_kind"].items():
        assert sum(d["solves"][kind] for d in s) == n
    assert s[-1]["onsite"] == run["onsite"]
    assert all(0 <= d[k] <= 1 for d in s for k in ("onsite", "screen", "hard"))


def test_no_node_starves(run):
    assert not run["starved"], "rusty %d+ days in a row with nothing aimed at it: %s" % (
        kg_simulate.STARVED_DAYS,
        ", ".join(f"{n} ({k}d)"
                  for n, k in sorted(run["starved"].items(), key=lambda x: -x[1])))


def test_run_restores_drill_bank(run):
    """A run reads a scratch copy of drills/ that it authors virtual bank
    files into; after it, kg_lib and kg_next read the real bank again and
    the copy is gone."""
    import glob
    real = os.path.join(os.path.dirname(kg_lib.GRAPH_DIR), "drills")
    assert kg_lib.DRILLS_DIR == real
    assert kg_simulate.kg_next.DRILLS_DIR == real
    assert not glob.glob(os.path.join(real, "*", "sim_*.py")), \
        "a virtual bank file landed in the real bank"


def test_authoring_follows_the_measured_rate(run):
    """At the measured rate the run banks nodes: the count of banks is the
    rate times the days, rounded down (a fraction of a bank carries over),
    capped by the nodes that had none."""
    a = run["authored"]
    assert a["rate"] >= 0
    bankless = sum(1 for n in kg_lib.load_nodes() if not kg_lib.has_drill_bank(n))
    assert a["nodes"] == min(int(a["rate"] * run["day"] + 1e-9), bankless)
    assert a["files"] >= a["nodes"]


def test_bank_rate_zero_authors_nothing():
    """`make simulate bank-rate 0` runs on the bank as it is."""
    if not kg_lib._load_curve():
        pytest.skip("graph/curve.json missing - run make curve first")
    r = kg_simulate.run(hours=HOURS, seed=SEED, days=5, log=lambda *a: None, bank_rate=0)
    assert r["authored"] == {"nodes": 0, "files": 0, "rate": 0, "source": "given"}
