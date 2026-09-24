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
from session import SETUP, stub  # noqa: E402
from test_reference_solutions import PY, drill_for  # noqa: E402

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


def reference(prefix):
    return next(r for r in REFERENCES if os.path.basename(r).startswith(prefix))


def signatures(src):
    p = Parser(src)
    return [(d[1], [n for n, _ in d[2]]) for d in p.program()], p.base


def solved(stub_text, reference_text, note=""):
    """current.mu as the operator leaves it: the stub's statement block,
    with a note under `# ---`, the reference solution in place of the empty
    defs, and every assert of the script turned on."""
    lines = stub_text.split("\n")
    first = next(i for i, ln in enumerate(lines) if ln.startswith(("def ", "extends ")))
    head = lines[:first]
    if note:
        head.insert(head.index("# ---") + 1, f"# {note}")
    p = Parser(stub_text)
    p.program()
    script = lines[p.script_line - 1 :] if p.script_line else []
    script = [re.sub(rf"^# ({SETUP}.*)$", r"\1", ln) for ln in script]
    body = reference_text.split("\n")
    while body and body[0].startswith("#"):
        body.pop(0)  # the # REFERENCE line
    return "\n".join(head + body + [""] + script) + "\n"


def session(cwd, *args):
    return subprocess.run(
        [PY, SESSION, *args],
        cwd=cwd,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=120,
    )


def python(cwd, name="current.py"):
    return subprocess.run(
        [PY, name], cwd=cwd, env=ENV, capture_output=True, text=True, timeout=120
    )


@pytest.mark.parametrize("ref", REFERENCES, ids=os.path.basename)
def test_every_drill_gets_a_stub_with_the_reference_signature(ref):
    s = stub(open(drill_for(ref)).read())
    transpile(s)
    assert signatures(s) == signatures(open(ref).read())
    assert s.startswith("# DRILL:") and "\n# ---\n" in s


@pytest.mark.parametrize("ref", REFERENCES, ids=os.path.basename)
def test_every_drill_runs_green_from_current_mu(ref, tmp_path):
    drill = open(drill_for(ref)).read()
    (tmp_path / "current.py").write_text(drill)
    (tmp_path / "current.mu").write_text(solved(stub(drill), open(ref).read()))
    run = session(tmp_path, "run")
    assert run.returncode == 0, run.stdout[-1500:] + run.stderr[-1500:]
    assert "Running from current.mu." in run.stderr


def test_the_stub_translates_the_asserts():
    s = stub(
        open(
            os.path.join(ROOT, "drills/binary-search-on-answer/d115_first_true.py")
        ).read()
    )
    assert "# assert sol.firstTrue(1, 100, x -> x * x >= 50) == 8" in s
    s = stub(
        open(
            os.path.join(ROOT, "drills/fast-slow-pointers/d109_cut_at_the_middle.py")
        ).read()
    )
    assert "def cut(vals)\n  first, second = sol.cutAtTheMiddle(" in s
    assert (
        "print(get_list_values(first), get_list_values(second))  # [1, 2, 3] [4, 5]"
        in s
    )
    s = stub(
        open(
            os.path.join(ROOT, "drills/event-sweep/d119_turn_knobs_to_a_total.py")
        ).read()
    )
    assert "  def band(a, b)\n    (min(a, b) + 1, max(a, b) + limit)\n" in s


# one drill of each shape: a callable argument, a class built as `p =`,
# a base class, a helper in the stub, multi-line asserts, a tree
CASES = ["d115_", "d17_", "d71_", "d119_", "d2_", "d68_"]


@pytest.mark.parametrize("prefix", CASES)
def test_a_whole_session(prefix, tmp_path):
    ref = reference(prefix)
    (tmp_path / "current.py").write_text(open(drill_for(ref)).read())

    assert session(tmp_path, "stub").returncode == 0
    served = (tmp_path / "current.mu").read_text()
    assert served == (tmp_path / ".mu_stub").read_text()
    assert "Running from current.mu." in session(tmp_path, "run").stderr

    (tmp_path / "current.mu").write_text(
        solved(served, open(ref).read(), "peeked at the loop")
    )
    run = session(tmp_path, "run")
    assert run.returncode == 0, run.stdout[-1500:] + run.stderr[-1500:]

    # serving the same drill again never overwrites the work
    assert "left alone" in session(tmp_path, "stub").stdout

    assert session(tmp_path, "fold").returncode == 0
    folded = (tmp_path / "current.py").read_text()
    assert folded.startswith('"""')
    doc = folded.split('"""')[1]
    assert "\n---\npeeked at the loop\n" in doc  # the notes, where the judge reads them
    quoted = folded.split("# mu source (current.mu)")[1].split("\n\n")[0]
    assert "# def " in quoted and "# DRILL" not in quoted and "# assert" not in quoted
    assert (tmp_path / "current.mu").read_text() == ""
    assert not (tmp_path / ".mu_stub").exists()
    ran = python(tmp_path)
    assert ran.returncode == 0, ran.stdout[-1500:] + ran.stderr[-1500:]


def test_serving_another_drill_keeps_the_old_work(tmp_path):
    first, second = reference("d115_"), reference("d120_")
    (tmp_path / "current.py").write_text(open(drill_for(first)).read())
    session(tmp_path, "stub")
    work = solved((tmp_path / "current.mu").read_text(), open(first).read())
    (tmp_path / "current.mu").write_text(work)
    (tmp_path / "current.py").write_text(open(drill_for(second)).read())
    assert "moved to current.mu.prev" in session(tmp_path, "stub").stdout
    assert (tmp_path / "current.mu.prev").read_text() == work
    assert (tmp_path / "current.mu").read_text().startswith("# DRILL: Last True")


def test_a_current_mu_for_another_drill_is_not_run(tmp_path):
    shutil.copy(drill_for(reference("d120_")), tmp_path / "current.py")
    (tmp_path / "current.mu").write_text(
        stub(open(drill_for(reference("d115_"))).read())
    )
    run = session(tmp_path, "run")
    assert "current.mu" not in run.stderr


def test_a_mu_syntax_error_names_the_line(tmp_path):
    shutil.copy(drill_for(reference("d115_")), tmp_path / "current.py")
    (tmp_path / "current.mu").write_text(
        "# DRILL: First True\ndef firstTrue(lo: int) -> int\n  x = \n"
    )
    run = session(tmp_path, "run")
    assert run.returncode == 1
    assert run.stderr.startswith("current.mu: line 3:")


def test_nothing_to_do_without_current_mu(tmp_path):
    shutil.copy(drill_for(reference("d115_")), tmp_path / "current.py")
    assert session(tmp_path, "fold").returncode == 0
    assert "mu source" not in (tmp_path / "current.py").read_text()


PROBLEM = '''"""
URL: https://leetcode.com/problems/two-sum/description/

1. Two Sum

Given nums and target, return the indices of the two numbers that add up
to target.
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        pass


sol = Solution()

# assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
'''

TWO_SUM = """def twoSum(nums: [int], target: int) -> [int]
  seen = {}
  for i, x in nums
    if target - x in seen
      return [seen[target - x], i]
    seen[x] = i
"""


def test_a_problem_is_served_run_submitted_and_folded(tmp_path):
    (tmp_path / "current.py").write_text(PROBLEM)
    assert "Wrote current.mu" in session(tmp_path, "stub").stdout
    work = (tmp_path / "current.mu").read_text()
    assert work.startswith("# URL: https://leetcode.com/problems/two-sum/")
    work = work.replace(
        "def twoSum(nums: [int], target: int) -> [int]\n  pass\n", TWO_SUM
    )
    work = work.replace("# assert", "assert")
    (tmp_path / "current.mu").write_text(work)
    assert session(tmp_path, "run").returncode == 0
    # make submit sends the transpiled copy while current.mu holds the work
    assert session(tmp_path, "build").stdout.strip() == ".mu_current.py"
    sent = (tmp_path / ".mu_current.py").read_text()
    assert "URL: https://leetcode.com/problems/two-sum/" in sent
    assert "seen[x] = i" in sent
    session(tmp_path, "fold")
    assert "# mu source (current.mu)" in (tmp_path / "current.py").read_text()
    assert session(tmp_path, "build").stdout.strip() == "current.py"


def test_a_problem_mu_cannot_write_is_left_to_current_py(tmp_path):
    design = PROBLEM.replace("class Solution:", "class StockPrice:")
    (tmp_path / "current.py").write_text(design)
    assert "solve it in current.py" in session(tmp_path, "stub").stdout
    assert not (tmp_path / "current.mu").exists()
    given = PROBLEM.replace(
        "sol = Solution()",
        "class Master:\n    def guess(self, w: str) -> int:\n        return 0\n\n\nsol = Solution()",
    )
    (tmp_path / "current.py").write_text(given)
    out = session(tmp_path, "stub")
    assert out.returncode == 0 and "solve it in current.py" in out.stdout


@pytest.mark.parametrize(
    "annotation, want",
    [
        ("Optional['Node']", "Node?"),
        ("'Optional[Node]'", "Node?"),
        ("TreeNode | None", "TreeNode?"),
    ],
)
def test_optional_annotations(annotation, want):
    from session import mu_type

    assert mu_type(__import__("ast").parse(annotation, mode="eval").body) == want
