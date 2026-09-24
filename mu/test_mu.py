"""Transpile every example and run it against the problem's cached asserts.

The Python runs with `-S`, so no harness builtin leaks in: what passes
here is what LeetCode receives.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from mu import MuError, fmt, transpile  # noqa: E402

CACHE = HERE.parent / ".prepare_cache"
EXAMPLES = sorted((HERE / "examples").glob("*.mu"))

# cached asserts whose input breaks the problem's stated constraints
OUTSIDE_CONSTRAINTS = {
    "0300": ["lengthOfLIS([])"],  # 1 <= nums.length
    "0743": ["], 10, 11, )"],  # 1 <= k <= n
    "0875": ["10**4, 1)", "[5, 5, 5, 5, 5], 3)", "[2, 2, 2, 2, 2], 2)"],  # n <= h
}


def asserts(stem):
    sol = json.loads((CACHE / f"{int(stem)}.json").read_text())["solution"]
    tail = sol[sol.index("\nsol = ") :]
    head, *rest = tail.split("\nassert")
    bad = OUTSIDE_CONSTRAINTS.get(stem, [])
    kept = [a for a in rest if not any(b in " ".join(a.split()) for b in bad)]
    assert len(rest) - len(kept) == len(bad), "an OUTSIDE_CONSTRAINTS entry went stale"
    return "\nassert".join([head] + kept)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_example(path):
    code = transpile(path.read_text()) + asserts(path.stem)
    run = subprocess.run(
        [sys.executable, "-S", "-c", code], capture_output=True, text=True, timeout=60
    )
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize(
    "src, message",
    [
        ("def f(a: int) -> int\n  sum for x in a\n    y = x\n", "must be a value"),
        ("def f(a: int) -> int\n  first k in a if k\n", "needs a range"),
        ("def f(a: int) -> int\n    x = 1\n  x\n", "indentation"),
    ],
)
def test_errors(src, message):
    with pytest.raises(MuError, match=re.escape(message)):
        transpile(src)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_examples_are_formatted(path):
    assert fmt(path.read_text()) == path.read_text()


def test_fmt_messy():
    messy = (
        "# 322. Coin Change\n"
        "def coinChange(coins:[int],amount:int)->int\n"
        "    memo f(a)=\n"
        "        |a==0->0\n"
        "        |a<0->inf\n"
        "        |else->1+min for c in coins:f(a-c)\n"
        "    f(amount) if f(amount)<inf else -1\n"
    )
    want = (HERE / "examples" / "0322.mu").read_text()
    assert fmt(messy) == want
    assert fmt(want) == want


def test_fmt_ranges_unary_and_joined_brackets():
    src = "def f(a: [int]) -> int\n  x = [ -1 ,\n     2 ]\n  sum for i in 0 ..< len( a ): a[ i ] * -x[0]\n"
    assert fmt(src) == (
        "def f(a: [int]) -> int\n  x = [-1, 2]\n  sum for i in 0..<len(a): a[i] * -x[0]\n"
    )


def test_library_copies_agree_with_the_harness():
    """mu pastes its own copies of these harness builtins into the output;
    they must behave as the utils/harness ones do."""
    from collections import deque

    sys.path.insert(0, str(HERE.parent / "utils" / "harness"))
    import adj_utils
    import combo_utils
    import grid_utils

    from mu import HELPERS

    ns = {}
    names = ("cells", "nbrs", "table", "like", "pairs", "levels", "adjacency")
    for name in names + ("indegrees",):
        for imp in HELPERS[name][0]:
            exec(imp, ns)
        exec(HELPERS[name][2], ns)
    grid = [[1, 2, 3], [4, 5, 6]]
    assert list(ns["cells"](grid)) == list(grid_utils.cells(grid))
    assert list(ns["cells"](grid, 1)) == list(grid_utils.cells(grid, 1))
    for r, c in grid_utils.cells(grid):
        assert list(ns["nbrs"](grid, r, c)) == list(grid_utils.nbrs(grid, r, c))
        assert list(ns["nbrs"](grid, (r, c))) == list(grid_utils.nbrs(grid, r, c))
    assert ns["table"](2, 3, fill=7) == grid_utils.table(2, 3, fill=7)
    assert ns["like"](grid, fill=-1) == grid_utils.like(grid, fill=-1)
    assert list(ns["pairs"](4)) == list(combo_utils.pairs(4))
    assert list(ns["levels"](deque([1, 2]))) == list(adj_utils.levels(deque([1, 2])))
    edges = [[0, 1, 5], [1, 2, 6], [2, 0, 7]]
    for kw in (
        {},
        {"n": 4},
        {"reverse": True},
        {"directed": False},
        {"weighted": True},
    ):
        assert ns["adjacency"](edges, **kw) == adj_utils.adjacency(edges, **kw)
        if "weighted" not in kw:
            assert ns["indegrees"](edges, **kw) == adj_utils.indegrees(edges, **kw)
    assert ns["indegrees"](edges, 3, type=list) == adj_utils.indegrees(
        edges, 3, type=list
    )


def test_push_operator():
    src = "def f(a: [int], x: int) -> [int]\n  if x < -1: a <- -x\n  a <- x\n"
    out = transpile(src)
    assert "if x < -1:" in out
    assert "a.append(-x)" in out
    assert "return a.append" not in out  # a push is never the block's value
    assert fmt("def f(a: [int]) -> int\n  a<-  -1\n  a[0]\n") == (
        "def f(a: [int]) -> int\n  a <- -1\n  a[0]\n"
    )


def test_pop_dot():
    src = "def f(stack: [int], res: [int]) -> int\n  res[stack .] = 1\n  stack .\n  x = stack . + 1\n  stack.count(x)\n"
    out = transpile(src)
    assert "res[stack.pop()] = 1" in out
    assert "        stack.pop()" in out
    assert "x = stack.pop() + 1" in out
    assert "return stack.count(x)" in out  # a name after the dot is an attribute
    assert "w = s.pop() if s else 0" in transpile(
        "def f(s: [int]) -> int\n  w = s . if s else 0\n  w\n"
    )
    assert fmt("def f(s: [int]) -> int\n  res[s.] = 1\n  s .\n  s.x\n") == (
        "def f(s: [int]) -> int\n  res[s .] = 1\n  s .\n  s.x\n"
    )


def test_fmt_moves_one_line_bodies_onto_their_own_line():
    src = (
        "def f(a: [int]) -> int\n"
        "  for x in a: if x > 0: a <- x  # kept\n"
        "  if s[1:2] == {1: 2}: return 1\n"
        "  elif sum for x in a: x > 3\n"
        "    return 2\n"
        "  else: return 3\n"
    )
    assert fmt(src) == (
        "def f(a: [int]) -> int\n"
        "  for x in a\n"
        "    if x > 0\n"
        "      a <- x  # kept\n"
        "  if s[1:2] == {1: 2}\n"
        "    return 1\n"
        "  elif sum for x in a: x > 3\n"
        "    return 2\n"
        "  else\n"
        "    return 3\n"
    )
    assert fmt(fmt(src)) == fmt(src)


def test_one_argument_calls_drop_their_brackets():
    src = (
        "def f(nums: [int], grid: [[int]], v: int) -> int\n"
        "  x = len nums - 1\n"
        "  print len nums\n"
        "  y = max(x, 3) + int '7'\n"
        "  count for (i, j) in cells grid if grid[i][j] == v\n"
    )
    out = transpile(src)
    assert "x = len(nums) - 1" in out
    assert "print(len(nums))" in out
    assert "y = max(x, 3) + int('7')" in out
    assert "for (i, j) in cells(grid) if" in out
    # keywords, operators and brackets end the argument
    out = transpile(
        "def g(a: [int], s: [int]) -> int\n  helper(1)\n  a[0] if a else s -1\n"
    )
    assert "a[0] if a else s - 1" in out


def test_a_bracketless_call_takes_a_generator():
    src = "def f(a: [int]) -> int\n  return len set self.find y for y in a\n"
    out = transpile(src)
    assert "len(set(self.find(y) for y in a))" in out
    src = "def g(a: [int]) -> int\n  sum x for x in a if x > 0\n"
    assert "sum(x for x in a if x > 0)" in transpile(src)


def test_string_prefixes():
    out = transpile("def f(a: str) -> str\n  b = f' {a}'\n  r'\\d' + b\n")
    assert "b = f' {a}'" in out
    assert "return r'\\d' + b" in out
    assert (
        fmt("def f(a: str) -> str\n  f' {a}'\n") == "def f(a: str) -> str\n  f' {a}'\n"
    )


def test_chained_assignment():
    src = (
        "def f(n: int) -> int\n  a = b = n\n  def g()\n    a = b = 0\n  g()\n  a + b\n"
    )
    out = transpile(src)
    assert "a = b = n" in out
    assert "nonlocal a, b" in out  # every target of the chain is bound
    assert "return a + b" in out
    assert (
        fmt("def f() -> int\n  a=b  =1\n  a\n") == "def f() -> int\n  a = b = 1\n  a\n"
    )
    with pytest.raises(MuError):
        transpile("def f() -> int\n  a += b = 1\n  a\n")


def test_triple_quoted_strings_span_lines():
    src = (
        "def f() -> str\n"
        "  a = '''one\n"
        '  two\'\'\' + """x"""\n'
        '  b = f"""{a}\n'
        "\n"
        'it\'s "quoted" """\n'
        "  b\n"
    )
    out = transpile(src)
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f() == 'one\n  twox\n\nit\'s "quoted" '
    assert fmt(src) == src  # the string's own lines are never touched
    assert fmt(fmt(src)) == fmt(src)
    with pytest.raises(MuError, match="line 2: unclosed ''' string"):
        transpile("def f() -> str\n  '''abc\n")
