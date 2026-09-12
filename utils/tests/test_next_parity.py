# Lockstep test for `make next`: utils/kg/kg_next (Python, the reference)
# and utils/kg/kg_next_rs (Rust, what `make next` runs) implement the same
# picker over the same graph/ data. Nothing but this test keeps them in
# step, so it diffs them two ways over the REAL repo state:
#
#   1. the printed output, byte for byte, for every argument set the
#      makefile can produce (plain, --why, ranks, --graph, each group with
#      cram / early / assisted). Both sides run with KG_SEED so the status
#      faces come from the same random stream, KG_TODAY so a midnight
#      crossing cannot split them, --no-show so no tree is drawn, and no
#      tty so rich prints plain text;
#   2. the library values behind that output (`kg_next --golden-json`
#      against utils/tests/next_golden.py, kg_lib / kg_next run the same
#      way): node statuses and
#      axes, the drill clock, the holds, carriers, the drafted tier, the
#      review clocks, the replay, the picks under each scenario.
#
# A change to either side that moves any of it fails `make test`. This
# file is not in `make test-fast` (it takes minutes: the Python picker runs
# once per argument set); run it by hand after touching either picker:
#
#   .venv/bin/pytest -q utils/tests/test_next_parity.py

import json
import os
import subprocess
from datetime import date

import pytest

from kg import kg_lib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KG = os.path.join(ROOT, "utils", "kg")
CRATE = os.path.join(KG, "kg_next_rs")
RUST_BIN = os.path.join(CRATE, "target", "release", "kg_next")
PY = os.path.join(ROOT, ".venv", "bin", "python3")
SEED = "7"
COLUMNS = "250"

# the argument sets `make next` can produce; --no-show on all of them
ARG_SETS = [
    [],
    ["--why"],
    ["2"],
    ["3"],
    ["--graph"],
]


def groups():
    return sorted({n.get("group") for n in kg_lib.load_nodes().values()} - {None})


def arg_sets():
    out = list(ARG_SETS)
    for g in groups():
        out += [[g], [g, "--cram"], [g, "--early"], [g, "--assisted"], [g, "2"]]
    return out


@pytest.fixture(scope="session", autouse=True)
def build_rust():
    subprocess.run(
        [
            "cargo",
            "build",
            "--release",
            "--quiet",
            "--manifest-path",
            os.path.join(CRATE, "Cargo.toml"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture(scope="session")
def today():
    """One day for every run of the session: the Manila date now."""
    return date.today().isoformat()


def env(today):
    e = dict(os.environ)
    e.update(
        {
            "KG_SEED": SEED,
            "KG_TODAY": today,
            "KG_NO_PLAN": "1",
            "LEET_NO_ANIMATE": "1",
            "COLUMNS": COLUMNS,
            "PYTHONPATH": os.path.join(ROOT, "utils"),
        }
    )
    return e


# The Python side, run the way the Rust binary is: random seeded like
# KG_SEED, the day frozen like KG_TODAY, then kg_next.main().
PY_WRAPPER = """
import os, random, sys
from datetime import date
from importlib.machinery import SourceFileLoader
random.seed(int(os.environ["KG_SEED"]))
sys.argv = ["kg_next"] + sys.argv[1:]
m = SourceFileLoader("kg_next", os.environ["KG_NEXT_PATH"]).load_module()
m.freeze(date.fromisoformat(os.environ["KG_TODAY"]))
m.main()
"""


def run_python(args, today):
    e = env(today)
    e["KG_NEXT_PATH"] = os.path.join(KG, "kg_next")
    proc = subprocess.run(
        [PY, "-c", PY_WRAPPER, *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=e,
    )
    return proc


def run_rust(args, today):
    return subprocess.run(
        [RUST_BIN, *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env(today),
    )


@pytest.mark.parametrize("args", arg_sets(), ids=lambda a: " ".join(a) or "plain")
def test_output_matches(args, today):
    args = [*args, "--no-show"]
    py = run_python(args, today)
    rs = run_rust(args, today)
    assert py.returncode == rs.returncode, (py.stderr, rs.stderr)
    assert rs.stderr == ""
    assert py.stdout == rs.stdout


def test_bad_word_is_refused_by_both(today):
    py = run_python(["no-such-group", "--no-show"], today)
    rs = run_rust(["no-such-group", "--no-show"], today)
    assert py.returncode == 2 and rs.returncode == 2
    assert "is not a number or a group" in py.stderr
    assert "is not a number or a group" in rs.stderr


def test_cell_widths_are_rich_s():
    """The Rust cell-width table is rich's own: the two must agree on every
    range, or the tables pad differently."""
    import re

    from rich._cell_widths import CELL_WIDTHS

    src = open(os.path.join(CRATE, "src", "cell_widths.rs")).read()
    body = src[src.index("= &[") + 4 :]
    rows = [
        tuple(int(x) for x in m.groups())
        for m in re.finditer(r"\(\s*(\d+),\s*(\d+),\s*(-?\d+)\s*\)", body)
    ]
    assert rows == [tuple(t) for t in CELL_WIDTHS]


# ---- the golden diff ----------------------------------------------------
# Both sides print the same JSON document: `kg_next --golden-json` and
# utils/tests/next_golden.py, each a subprocess under the same environment
# (the conftest strips the .envrc knobs from this process; the tooling
# reads them, so the comparison runs where the tooling runs).

GOLDEN_KEYS = [
    "today",
    "anki_frontier",
    "due_problems",
    "review_queue",
    "asleep",
    "sleep_rows",
    "starved",
    "routed_around",
    "blocked_frontier",
    "ready_hards",
    "parked_summits",
    "unmapped_summits",
    "drafted_in_reach_hard",
    "drafted_in_reach_medium",
    "trivial_easies",
    "elo_now",
    "solve_model",
    "ratings_count",
    "review_ahead",
    "upcoming",
    "recognition",
    "due_spot",
    "solve_seconds_today",
    "solved_today",
    "group_caps",
    "group_reps",
]


@pytest.fixture(scope="module")
def golden(today):
    proc = subprocess.run(
        [RUST_BIN, "--golden-json"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env(today),
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stderr == ""
    return json.loads(proc.stdout)


@pytest.fixture(scope="module")
def expected(today):
    proc = subprocess.run(
        [PY, os.path.join(ROOT, "utils", "tests", "next_golden.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env(today),
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _diff(name, exp, got):
    assert exp == got, f"{name}: python {exp!r} != rust {got!r}"


def _diff_table(name, exp, got):
    assert set(exp) == set(got), f"{name}: keys differ"
    for k in exp:
        _diff(f"{name}[{k}]", exp[k], got[k])


def test_golden_has_the_same_shape(golden, expected):
    assert set(golden) == set(expected)


def test_nodes_lockstep(golden, expected):
    _diff_table("nodes", expected["nodes"], golden["nodes"])


def test_problems_lockstep(golden, expected):
    _diff_table("problems", expected["problems"], golden["problems"])


def test_drills_lockstep(golden, expected):
    _diff_table("drills", expected["drills"], golden["drills"])


@pytest.mark.parametrize("key", GOLDEN_KEYS)
def test_tables_lockstep(golden, expected, key):
    _diff(key, expected[key], golden[key])


def test_scenario_picks_lockstep(golden, expected):
    _diff_table("scenarios", expected["scenarios"], golden["scenarios"])
