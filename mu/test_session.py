"""The mu side of a solve: stub at serve, run while solving, fold at solved."""

import glob
import os
import re
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [HERE, os.path.join(ROOT, "utils", "tests")]
from session import stub  # noqa: E402
from test_reference_solutions import PY, SETUP, continued, drill_for  # noqa: E402

from mu import Parser, transpile  # noqa: E402

REFERENCES = sorted(
    glob.glob(os.path.join(ROOT, "graph", "node_notes", "*", "d[0-9]*.mu"))
)
SESSION = os.path.join(HERE, "session.py")
ENV = dict(
    os.environ,
    PYTHONPATH=os.pathsep.join(
        [ROOT, os.path.join(ROOT, "utils"), os.path.join(ROOT, "utils", "harness")]
    ),
)


def signatures(src):
    p = Parser(src)
    return [(d[1], [n for n, _ in d[2]]) for d in p.program()], p.base


@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_every_drill_gets_a_stub_with_the_reference_signature(reference):
    s = stub(open(drill_for(reference)).read())
    transpile(s)
    assert signatures(s) == signatures(open(reference).read())


def test_stub_carries_handed_over_helpers_and_scaffolding():
    s = stub(
        open(
            os.path.join(ROOT, "drills/event-sweep/d119_turn_knobs_to_a_total.py")
        ).read()
    )
    assert "  def band(a, b)\n    (min(a, b) + 1, max(a, b) + limit)\n" in s
    s = stub(
        open(
            os.path.join(ROOT, "drills/index-conversion/d133_top_down_index.py")
        ).read()
    )
    assert "  for (r, c) in cells(grid)\n    pass\n  return grid\n" in s
    s = stub(
        open(os.path.join(ROOT, "drills/union-find/d71_component_counts.py")).read()
    )
    assert "extends UnionFind" in s


def session(cwd, *args):
    return subprocess.run(
        [PY, SESSION, *args],
        cwd=cwd,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=60,
    )


def python(cwd, name="current.py"):
    return subprocess.run(
        [PY, name], cwd=cwd, env=ENV, capture_output=True, text=True, timeout=60
    )


def uncommented(drill_src):
    """The drill as the operator runs it: every assert turned on."""
    return continued(re.sub(rf"^# ({SETUP}.*)$", r"\1", drill_src, flags=re.M))


# one drill of each shape: a callable argument, a class built as `p =`,
# a base class, a helper in the stub, multi-line asserts, a tree
CASES = ["d115_", "d17_", "d71_", "d119_", "d2_", "d68_"]


@pytest.mark.parametrize("prefix", CASES)
def test_a_whole_session(prefix, tmp_path):
    reference = next(r for r in REFERENCES if os.path.basename(r).startswith(prefix))
    (tmp_path / "current.py").write_text(uncommented(open(drill_for(reference)).read()))

    assert session(tmp_path, "stub").returncode == 0
    assert (tmp_path / "current.mu").read_text() == (tmp_path / ".mu_stub").read_text()

    # the stub alone runs current.py as served, and its asserts fail
    run = session(tmp_path, "run")
    assert run.returncode != 0 and "Running the mu" not in run.stderr

    (tmp_path / "current.mu").write_text(open(reference).read())
    run = session(tmp_path, "run")
    assert run.returncode == 0, run.stdout[-1500:] + run.stderr[-1500:]
    assert "Running the mu solution from current.mu." in run.stderr

    # serving again never overwrites a written solution
    assert "left alone" in session(tmp_path, "stub").stdout
    assert (tmp_path / "current.mu").read_text() == open(reference).read()

    assert session(tmp_path, "fold").returncode == 0
    folded = (tmp_path / "current.py").read_text()
    assert "# mu source (current.mu)" in folded
    assert folded.startswith('"""')  # statement and notes stay on top for the judge
    assert (tmp_path / "current.mu").read_text() == ""
    assert not (tmp_path / ".mu_stub").exists()
    ran = python(tmp_path)
    assert ran.returncode == 0, ran.stdout[-1500:] + ran.stderr[-1500:]


def test_a_mu_syntax_error_names_the_line(tmp_path):
    reference = next(r for r in REFERENCES if "d115_" in r)
    (tmp_path / "current.py").write_text(open(drill_for(reference)).read())
    (tmp_path / "current.mu").write_text("def firstTrue(lo: int) -> int\n  x = \n")
    run = session(tmp_path, "run")
    assert run.returncode == 1
    assert run.stderr.startswith("current.mu: line 2:")


def test_nothing_to_do_without_current_mu(tmp_path):
    shutil.copy(
        os.path.join(ROOT, "drills/binary-search-on-answer/d115_first_true.py"),
        tmp_path / "current.py",
    )
    assert session(tmp_path, "fold").returncode == 0
    assert "mu source" not in (tmp_path / "current.py").read_text()
