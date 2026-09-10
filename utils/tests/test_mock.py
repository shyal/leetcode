# Guards for `make mock` (utils/kg/kg_mock_rs): output structure, column
# alignment, the hours override, and the <100ms speed budget. The model math is
# shared with kg_lib.py (pass_rates / current_recall for the README chart);
# keep the two in sync when either changes.

import os
import re
import subprocess
import time

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUST_BIN = os.path.join(
    ROOT, "utils", "kg", "kg_mock_rs", "target", "release", "kg_mock"
)
MONTH_ROW = re.compile(r"^  \d{1,2} \w{3} \d{2} ")


@pytest.fixture(scope="session", autouse=True)
def build_rust():
    subprocess.run(
        [
            "cargo",
            "build",
            "--release",
            "--quiet",
            "--manifest-path",
            os.path.join(ROOT, "utils", "kg", "kg_mock_rs", "Cargo.toml"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def run_mock(args=()):
    proc = subprocess.run(
        [RUST_BIN, *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    )
    assert proc.stderr == ""
    return proc.stdout


def test_output_structure():
    out = run_mock()
    lines = out.splitlines()
    assert lines[0] == "today, cold, on a random 2E+2M+2H set:"
    for name in ("cautious", "central", "optimistic"):
        assert any(line.lstrip().startswith(name) for line in lines), name
    assert sum(1 for line in lines if MONTH_ROW.match(line)) == 18
    assert any(line.startswith("forward at ") for line in lines)
    percents = re.findall(r"(\d+(?:\.\d+)?)%", out)
    assert percents and all(0.0 <= float(p) <= 100.0 for p in percents)


def test_columns_aligned():
    out = run_mock()
    lines = out.splitlines()
    # forward table: header and every month row end flush at the same column
    # (all numeric columns are right-aligned), so their lengths must agree
    header = next(line for line in lines if line.lstrip().startswith("month "))
    month_rows = [line for line in lines if MONTH_ROW.match(line)]
    assert {len(r) for r in month_rows} == {len(header)}
    # same property for the today table
    header = next(line for line in lines if line.lstrip().startswith("scenario "))
    scen_rows = [
        line
        for line in lines
        if line.lstrip().split(" ")[0] in ("cautious", "central", "optimistic")
    ]
    assert len(scen_rows) == 3
    assert {len(r) for r in scen_rows} == {len(header)}


def test_hours_override():
    out = run_mock(["3"])
    assert "forward at 3h/day (solves in his measured mix" in out


def test_measured_pace_default():
    out = run_mock()
    m = re.search(
        r"forward at (\d+(?:\.\d+)?)h/day \((.*?)solves in his measured mix", out
    )
    assert m, out
    # either a measured window (with the source note) or the empty-window 2h fallback
    if m.group(2):
        assert m.group(2) == "avg of the current streak; "
    else:
        assert m.group(1) == "2"


def test_onsite_ready_milestone_within_a_row_month():
    # milestones are bisected to the exact crossing day, so the date no longer
    # lands on a monthly table row — but it must fall within the 30 days
    # ending at some row (the checkpoint that bracketed the crossing)
    out = run_mock()
    m = re.search(
        r"onsite-ready \(central P\(onsite\) >=50%\) ~ (\d{1,2} \w{3} \d{4})", out
    )
    if not m:
        pytest.skip("central P(onsite) never crosses 50% inside the horizon")
    from datetime import datetime

    milestone = datetime.strptime(m.group(1), "%d %b %Y").date()
    rows = [
        datetime.strptime(r, "%d %b %y").date()
        for r in re.findall(r"^  (\d{1,2} \w{3} \d{2}) ", out, re.M)
    ]
    assert any(
        0 <= (r - milestone).days < 30 for r in rows
    ), f"milestone {milestone} not within a month of any table row"


def test_json_mode():
    # the contract utils/kg/estimate depends on: milestone dates (or null) plus
    # today's central rates, matching what the human tables print
    import json

    data = json.loads(run_mock(["--json"]))
    assert set(data) == {
        "hours",
        "screen",
        "onsite",
        "hard",
        "hards_workable",
        "hard_competent",
        "onsite_ready",
    }
    for k in ("screen", "onsite", "hard"):
        assert 0.0 <= data[k] <= 1.0, k
    for k in ("hards_workable", "hard_competent", "onsite_ready"):
        assert data[k] is None or re.fullmatch(r"\d{4}-\d{2}-\d{2}", data[k]), k
    # the JSON dates and the human output's milestone lines agree
    out = run_mock()
    m = re.search(
        r"onsite-ready \(central P\(onsite\) >=50%\) ~ (\d{1,2} \w{3} \d{4})", out
    )
    if m and data["onsite_ready"]:
        from datetime import datetime

        human = datetime.strptime(m.group(1), "%d %b %Y").date().isoformat()
        assert human == data["onsite_ready"]


def test_speed():
    # a regression guard, not a benchmark: the sim sits ~0.1s on a laptop and
    # ~0.12s on CI runners, so the ceiling only trips on order-of-magnitude
    # slowdowns (the failure mode worth catching), not hardware variance
    times = []
    for _ in range(3):
        start = time.perf_counter()
        run_mock()
        times.append(time.perf_counter() - start)
    assert min(times) < 0.5, f"kg_mock too slow: best of 3 was {min(times):.3f}s"


def test_python_and_rust_agree_on_todays_rates():
    """The Rust Monte Carlo and the Python closed form are two readings of the
    same fitted cold-solve model; on today's evidence they must land on the
    same numbers, within Monte-Carlo noise."""
    import json
    import sys

    sys.path.insert(0, os.path.join(ROOT, "utils"))
    from importlib.machinery import SourceFileLoader

    from kg import kg_lib

    curve = kg_lib._load_curve()
    coef = kg_lib.solve_model(curve)
    if not coef:
        pytest.skip("no fitted cold-solve model in graph/curve.json")
    kg_simulate = SourceFileLoader(
        "kg_simulate", os.path.join(ROOT, "utils", "kg", "kg_simulate")
    ).load_module()
    nodes = kg_lib.load_nodes()
    pools, ratings = kg_simulate.build_pools(
        kg_lib.load_problems(), kg_lib.load_predicted(), nodes
    )
    expect = kg_simulate.PassExpectation(pools, ratings, list(nodes), coef)
    recall = kg_lib.current_recall(nodes, kg_lib.load_evidence(), curve)
    shift = kg_lib.solve_scenarios(curve)["central"]
    _, onsite, screen, hard = expect.rates(recall, shift)

    mock = json.loads(run_mock(["--json"]))
    for name, mine, theirs in (
        ("onsite", onsite, mock["onsite"]),
        ("screen", screen, mock["screen"]),
        ("hard", hard, mock["hard"]),
    ):
        assert (
            abs(mine - theirs) < 0.02
        ), f"{name}: python {mine:.3f} vs rust {theirs:.3f}"
