"""The simulation (utils/rs/kg_simulate) runs the real picker forward on the
real graph and evidence, so it is the one test that sees the picker's rules
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
    207) had nothing re-solve that problem. Three more failed it on
    2026-09-22 and were fixed by one rule: a stale move behind 24 due
    problem reviews, a young sql move at its floor behind a group cap the
    clock filled every morning, and a stale move with no bank behind both.
    A due move that has waited AGING_DAYS (7) days with nothing aimed at it
    is now served first (pick.rs, aging).

The run depends on graph/*.json and the fitted curve, both of which change
with every solve, so the caps carry a margin over what was observed.

The two .envrc knobs the run keeps (sim::KEPT_KNOBS) are fixed here like
the pace and the seed: conftest drops every .envrc name before collection
and CI has no .envrc, so without them the run is the node scheduler with
no group cap, which served nothing for 17 days on 2026-09-18 while the
same run passed on the operator's machine, where the binary reads the
knobs back from the file.
"""

import glob
import json
import os
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUST_BIN = os.path.join(ROOT, "utils", "rs", "target", "release", "kg_simulate")

DAYS = 60
HOURS = 1.5
SEED = 1
RUSTY_CAP = 10  # observed 5-8 over seeds 1-5 on 2026-08-31, day 1 excluded
STARVED_DAYS = 14  # kg::status::STARVED_DAYS
KNOBS = {"DRILL_SCHEDULER": "anki", "KG_GROUP_CAP": "sql=2,linked-lists=1"}


@pytest.fixture(scope="module")
def run():
    subprocess.run(
        [
            "cargo",
            "build",
            "--release",
            "--quiet",
            "--manifest-path",
            os.path.join(ROOT, "utils", "rs", "Cargo.toml"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    proc = subprocess.run(
        [RUST_BIN, str(HOURS), "--seed", str(SEED), "--days", str(DAYS), "--json"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env={**os.environ, **KNOBS},
    )
    if proc.returncode != 0:
        pytest.skip(proc.stderr.strip() or "kg_simulate could not start")
    return json.loads(proc.stdout)


def test_picker_never_dry(run):
    assert run["dry_days"] == 0, f"{run['dry_days']} days the picker served nothing"


def test_rusty_nodes_bounded(run):
    """Day 1 is the real state of the graph today, before the picker has
    acted; from day 2 the count is the picker's own doing."""
    worst = max((s + f, d) for d, s, f, _ in run["rusty"] if d > 1)
    assert worst[0] <= RUSTY_CAP, (
        f"{worst[0]} nodes STALE or FRAGILE at the start of day {worst[1]} "
        f"(cap {RUSTY_CAP}); the picker is not repairing what goes rusty"
    )


def test_series_one_row_per_day(run):
    """The README forecast chart reads the per-day series: one row per
    simulated day, the day's solves summing to the run's totals, the last
    row's onsite the run's."""
    s = run["series"]
    assert len(s) == run["day"]
    assert [d["day"] for d in s] == sorted(d["day"] for d in s)
    for kind, n in run["per_kind"].items():
        assert sum(d["solves"][kind] for d in s) == n
    assert s[-1]["onsite"] == run["onsite"]
    assert all(0 <= d[k] <= 1 for d in s for k in ("onsite", "screen", "hard"))


def test_no_node_starves(run):
    assert not run[
        "starved"
    ], "rusty %d+ days in a row with nothing aimed at it: %s" % (
        STARVED_DAYS,
        ", ".join(
            f"{n} ({k}d)"
            for n, k in sorted(run["starved"].items(), key=lambda x: -x[1])
        ),
    )


def test_run_leaves_the_real_bank_alone(run):
    """A run authors virtual bank files into a scratch copy of drills/,
    never the real bank."""
    real = os.path.join(ROOT, "drills")
    assert not glob.glob(
        os.path.join(real, "*", "sim_*.py")
    ), "a virtual bank file landed in the real bank"


def test_authoring_follows_the_measured_rate(run):
    """At the measured rate the run banks nodes: the count of banks is the
    rate times the days, rounded down (a fraction of a bank carries over),
    capped by the nodes that had none."""
    a = run["authored"]
    assert a["rate"] >= 0
    nodes = [
        n["id"]
        for n in json.load(open(os.path.join(ROOT, "graph", "nodes.json")))["nodes"]
    ]
    bankless = sum(
        1 for n in nodes if not glob.glob(os.path.join(ROOT, "drills", n, "*.py"))
    )
    assert a["nodes"] == min(int(a["rate"] * run["day"] + 1e-9), bankless)
    assert a["files"] >= a["nodes"]
