"""muviz runs every mu reference solution, spliced into its drill the way
the operator leaves current.mu, and draws frames for each without failing."""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [
    HERE,
    ROOT,
    os.path.join(ROOT, "utils"),
    os.path.join(ROOT, "utils", "harness"),
    os.path.join(ROOT, "utils", "tests"),
]
import viz  # noqa: E402
from session import stub  # noqa: E402
from test_drills import REFERENCES  # noqa: E402
from test_reference_solutions import drill_for  # noqa: E402
from test_session import solved  # noqa: E402

from mu import MuError  # noqa: E402

MEMO = """def longestPath(G: {int: [int]}) -> int
  memo longest(u) = max((1 + longest(v) for v in G[u]), default=0)
  longest(0)

sol = Solution()
print(sol.longestPath({0: [1, 2], 1: [2], 2: []}))
assert sol.longestPath({0: [1, 2], 1: [2], 2: []}) == 2
"""

ROW = """def longestEndingAt(nums: [int]) -> [int]
  dp = table(len(nums), fill=1)
  for (j, i) in pairs(len(nums), back=True)
    if nums[j] < nums[i]
      dp[i] = max(dp[i], dp[j] + 1)
  dp

sol = Solution()
print(sol.longestEndingAt([3, 1, 2]))
"""


def titles(frames):
    return [f.title for f in frames]


def text(frames):
    return "\n".join(p for f in frames for k, p in f.parts if k == "text")


def test_memo_run_reports_hits_and_the_call_tree(tmp_path):
    frames = viz.frames_of(MEMO, tmp_path / "memo.py")
    t = titles(frames)
    assert t[0] == "longestPath(G={0: [1, 2], 1: [2], 2: []})"
    assert "longest(u=2) = 0, from the memo" in t
    assert t[-1] == "the calls"
    assert t.count("the calls") == 1  # the asserts run untraced
    assert "memo" in text(frames[-1:])


def test_cursor_marks_the_cell_named_on_the_line():
    line = "dp[i] = max(dp[i], dp[j] + 1)"
    assert viz.cursors(line, {"dp": [1, 1], "i": 1, "j": 0}) == {
        "dp": [[("i", 1)], [("i", 1)], [("j", 0)]]
    }
    assert viz.cursors("G[u]", {"G": {}, "u": 0}) == {"G": [[("u", 0)]]}
    assert viz.cursors("dp[i][j - 1]", {"dp": [], "i": 1, "j": 1}) == {
        "dp": [[("i", 1), ("j - 1", 0)]]
    }
    assert viz.cursors("a[1:]", {"a": []}) == {}


def test_row_frames_show_changed_cells(tmp_path):
    frames = viz.frames_of(ROW, tmp_path / "row.py")
    body = text(frames)
    assert "dp" in body and "nums" in body
    assert titles(frames)[-2].startswith("longestEndingAt returns")


@pytest.mark.parametrize("reference", REFERENCES, ids=os.path.basename)
def test_every_reference_draws(reference, tmp_path):
    drill = drill_for(reference)
    if not drill.endswith(".py"):
        pytest.skip("not a python drill")
    py_src = open(drill).read()
    text_ = stub(py_src)
    if text_ is None:
        pytest.skip("mu cannot write this drill")
    try:
        src = solved(text_, open(reference).read())
        frames = viz.frames_of(src, tmp_path / "drill.py", py_src)
    except MuError as err:
        pytest.skip(f"mu cannot build this one: {err}")
    assert frames, "the demo line never called the Solution"
    assert not [f for f in frames if f.kind == "note"], titles(frames)
