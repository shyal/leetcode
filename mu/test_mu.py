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
from mu import VERSION, MuError, fmt, transpile  # noqa: E402

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
        ("def f(a: int) -> int\n  ret x = 1\n  ret y = 2\n", "more than one ret"),
        ("def f(a: int) -> int\n  for i in a\n    ret x = i\n", "own body"),
        ("@as_list\nx = 1\n", "a decorator goes above a def or a memo"),
        ("def f(a: int) -> int\n  a\n@as_list\n", "a decorator goes above a def"),
    ],
)
def test_errors(src, message):
    with pytest.raises(MuError, match=re.escape(message)):
        transpile(src)


def test_ret_names_the_return_value():
    src = (
        "def decode(encoded: [int], first: int) -> [int]\n"
        "  ret res = [first]\n"
        "  for i in range len encoded\n"
        "    if encoded[i] < 0\n"
        "      return\n"
        "    res <- encoded[i] ^ res[i]\n"
        "  ret = 0\n"
    )
    ns: dict = {}
    exec(transpile(src), ns)
    decode = ns["Solution"]().decode
    assert decode([1, 2, 3], 1) == [1, 0, 2, 1]
    assert decode([1, -1, 3], 1) == [1, 0]


def test_ret_takes_the_first_name_of_a_tuple_assignment():
    src = "def f() -> int\n  ret res, foo = 0, 10\n  res += foo\n"
    ns: dict = {}
    exec(transpile(src), ns)
    assert ns["Solution"]().f() == 10


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
        "    f(amount) or -1 if inf\n"
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
    import bs_utils
    import combo_utils
    import counter_utils
    import digit_utils
    import gen_utils
    import grid_utils
    from sitecustomize import ceil_div

    from mu import HELPERS

    ns = {}
    names = (
        "as_list",
        "_holds",
        "cells",
        "nbrs",
        "table",
        "like",
        "shape",
        "_spread",
        "put",
        "row",
        "col",
        "set_row",
        "set_col",
        "pairs",
        "levels",
        "adjacency",
        "to_digits",
        "to_int",
        "even",
        "odd",
        "in_bounds",
        "is_edge",
        "edges",
        "grid_bfs",
        "triples",
        "ceil_div",
        "first_true",
        "last_true",
        "first_false",
        "last_false",
        "min_chunks",
        "Multiset",
    )
    for name in names + ("indegrees",):
        for imp in HELPERS[name][0]:
            exec(imp, ns)
        exec(HELPERS[name][2], ns)
    for wrap in (ns["as_list"], gen_utils.as_list):
        upto = wrap(lambda n: (i for i in range(n)))
        assert upto(3) == [0, 1, 2] and upto(0) == []
    grid = [[1, 2, 3], [4, 5, 6]]
    assert list(ns["cells"](grid)) == list(grid_utils.cells(grid))
    assert list(ns["cells"](grid, 1)) == list(grid_utils.cells(grid, 1))
    for kw in (
        {"eq": 5},
        {"val": 5},
        {"lt": 3},
        {"lte": 3},
        {"gt": 4},
        {"gte": 2, "lt": 6},
    ):
        assert list(ns["cells"](grid, **kw)) == list(grid_utils.cells(grid, **kw))
    for r, c in grid_utils.cells(grid):
        assert list(ns["nbrs"](grid, r, c)) == list(grid_utils.nbrs(grid, r, c))
        assert list(ns["nbrs"](grid, (r, c))) == list(grid_utils.nbrs(grid, r, c))
        assert list(ns["nbrs"](grid, (r, c), gte=3)) == list(
            grid_utils.nbrs(grid, r, c, gte=3)
        )
    assert ns["table"](2, 3, fill=7) == grid_utils.table(2, 3, fill=7)
    assert ns["like"](grid, fill=-1) == grid_utils.like(grid, fill=-1)
    for args in ((grid,), ([],), ("abcde", "ace")):
        for li in (False, True):
            assert ns["shape"](*args, last_index=li) == grid_utils.shape(
                *args, last_index=li
            )
    a, b = [[1, 2], [1, 3]], [[1, 2], [1, 3]]
    ns["put"](a, [(0, 0), (1, 0)], 9)
    grid_utils.put(b, [(0, 0), (1, 0)], 9)
    assert a == b == [[9, 2], [9, 3]]
    ns["put"](a, [(0, 1), (1, 1)], iter([5, 6]))
    grid_utils.put(b, [(0, 1), (1, 1)], iter([5, 6]))
    assert a == b == [[9, 5], [9, 6]]
    assert ns["row"](grid, 1) == grid_utils.row(grid, 1) == [4, 5, 6]
    assert ns["col"](grid, 2) == grid_utils.col(grid, 2) == [3, 6]
    for f, g in (("set_row", grid_utils.set_row), ("set_col", grid_utils.set_col)):
        for v in (0, iter([7, 8])):
            a, b = [[1, 2], [1, 3]], [[1, 2], [1, 3]]
            ns[f](a, 1, v)
            g(b, 1, v if v == 0 else iter([7, 8]))
            assert a == b
    assert list(ns["pairs"](4)) == list(combo_utils.pairs(4))
    assert list(ns["pairs"](4, back=True)) == list(combo_utils.pairs(4, back=True))
    for num in (0, 7, 65875, "0042", -31):
        for rev in (False, True):
            for base in (10, 2, 7):
                assert ns["to_digits"](num, rev, base) == digit_utils.to_digits(
                    num, rev, base
                )
    for ds in ([], [0, 0, 4, 2], [8, 7, 6, 5, 5], [1, 0, 1, 1]):
        for rev in (False, True):
            for base in (10, 2, 16):
                assert ns["to_int"](ds, rev, base) == digit_utils.to_int(ds, rev, base)
    for n in range(-3, 4):
        assert ns["even"](n) == digit_utils.even(n)
        assert ns["odd"](n) == digit_utils.odd(n)
    assert list(ns["levels"](deque([1, 2]))) == list(adj_utils.levels(deque([1, 2])))
    a, b = set(), set()
    got = list(ns["levels"](deque([(0, 0), (0, 0), (1, 1)]), grid, a, gte=2))
    assert got == list(
        adj_utils.levels(deque([(0, 0), (0, 0), (1, 1)]), grid, b, gte=2)
    )
    assert a == b == {(1, 1)}
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
    for r, c in grid_utils.cells(grid):
        assert ns["is_edge"](grid, r, c) == grid_utils.is_edge(grid, r, c)
    for r in range(-1, 3):
        for c in range(-1, 4):
            assert ns["in_bounds"](grid, r, c) == grid_utils.in_bounds(grid, r, c)
            assert ns["in_bounds"](grid, (r, c)) == grid_utils.in_bounds(grid, (r, c))
    assert list(ns["edges"](grid)) == list(grid_utils.edges(grid))
    maze = [[0, 1, 0], [0, 0, 0], [1, 1, 0]]
    for kw in ({}, {"ok": lambda v: v == 0}):
        assert ns["grid_bfs"](maze, [(0, 0)], **kw) == grid_utils.grid_bfs(
            maze, [(0, 0)], **kw
        )
    assert list(ns["triples"](5)) == list(combo_utils.triples(5))
    for a in range(0, 12):
        for b in range(1, 5):
            assert ns["ceil_div"](a, b) == ceil_div(a, b)
    for k in range(-1, 12):
        ok = lambda x, k=k: x >= k  # noqa: E731
        for f in ("first_true", "last_true", "first_false", "last_false"):
            assert ns[f](0, 10, ok) == getattr(bs_utils, f)(0, 10, ok)
    for nums in ([], [3, 1, 4, 1, 5], [9, 2]):
        for cap in (1, 5, 8, 100):
            assert ns["min_chunks"](nums, cap) == bs_utils.min_chunks(nums, cap)
    a, b = ns["Multiset"]("aab"), counter_utils.Multiset("aab")
    for op in ("a", "a", "b", "c"):
        a[op] -= 1
        b[op] -= 1
        assert dict(a) == dict(b) and len(a) == len(b)


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


def test_a_push_is_a_comprehension_element():
    src = "def f(s: str) -> dict\n  pos = {:list}\n  [pos[v] <- i for i, v in s]\n  pos\n"
    assert "[pos[v].append(i) for i, v in enumerate(s)]" in transpile(src)
    assert fmt(src.replace(" <- ", "<-")) == src
    assert "(a.append(x * 2) for x in a)" in transpile(
        "def f(a: [int]) -> int\n  g = (a <- x * 2 for x in a)\n  0\n"
    )
    assert "[out.append(st.pop()) for _ in range(0, 2)]" in transpile(
        "def f(st: [int], out: [int]) -> int\n  [out <- st . for _ in 0..<2]\n  0\n"
    )


def run_f(src, *args):
    ns = {}
    exec(transpile(src), ns)
    return ns["Solution"]().f(*args)


def test_a_default_dict_collects_under_each_key():
    src = "def f(s: str) -> dict\n  {:list: c <- i for i, c in s}\n"
    assert "_pushed(defaultdict(list), ((c, i) for i, c in enumerate(s)))" in transpile(src)
    assert run_f(src, "egg") == {"e": [0], "g": [1, 2]}
    assert fmt(src.replace(": c <- i", ":c<-i")) == src
    src = "def f(es: [[int]]) -> dict\n  {:set: b <- a for (a, b) in es}\n"
    assert run_f(src, [[1, 0], [2, 0], [1, 0]]) == {0: {1, 2}}
    src = "def f(xs: [int]) -> dict\n  {:() -> [9]: x % 2 <- x for x in xs if x != 2}\n"
    assert run_f(src, [0, 1, 2, 3]) == {0: [9, 0], 1: [9, 1, 3]}


def test_a_default_dict_updates_each_key_in_place():
    src = "def f(s: str) -> dict\n  {:int: c += 1 for c in s}\n"
    assert "_updated(defaultdict(int), ((c, 1) for c in s), iadd)" in transpile(src)
    assert run_f(src, "egg") == {"e": 1, "g": 2}
    assert fmt(src) == src
    src = "def f(ps: [(int, {int})]) -> dict\n  {:set: k |= xs for (k, xs) in ps}\n"
    assert run_f(src, [(1, {2}), (1, {3})]) == {1: {2, 3}}


@pytest.mark.parametrize(
    "body, message",
    [
        ("{:list: v <- 1}", "expected 'for' after v <- 1"),
        ("{:list: v for v in s}", "expected <- or an operator like \\+=, got 'for'"),
        ("{:list: v = 1 for v in s}", "expected <- or an operator like \\+=, got '='"),
    ],
)
def test_a_collecting_default_dict_says_what_is_missing(body, message):
    with pytest.raises(MuError, match=f"line 2: {message}"):
        transpile(f"def f(s: str) -> dict\n  {body}\n")


def test_a_push_in_brackets_needs_a_for():
    with pytest.raises(MuError, match="line 2: a push in brackets needs a for"):
        transpile("def f(a: [int]) -> int\n  [a <- 1, 2]\n")


def test_fmt_keeps_a_space_after_a_pop_in_a_comprehension():
    src = "def f(h: [int]) -> [int]\n  [h .for _ in 0..1]\n"
    assert fmt(src) == "def f(h: [int]) -> [int]\n  [h . for _ in 0..1]\n"


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


def test_assignment_converts_targets():
    src = "def f(log: str) -> int\n  int(id), ev, int(t) = log.split ':'\n  id + t\n"
    out = transpile(src)
    assert "id, ev, t = log.split(':')" in out
    assert "id, t = int(id), int(t)" in out
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f("0:start:3") == 3
    assert fmt(src) == src


def test_a_loop_that_names_no_variable_reads_the_item_as_underscore():
    src = "def f(ps: [(int, int)]) -> int\n  ret s = 0\n  for ps\n    s += _[0]\n"
    out = transpile(src)
    assert "for _ in ps:" in out
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f([(1, 9), (2, 9)]) == 3
    assert fmt(src) == src


@pytest.mark.parametrize(
    "body, want",
    [
        ("sum for xs: _ * _", 14),
        ("max from 0 for xs if _ < 3: _", 2),
        ("count for xs if _ > 1", 2),
        ("sum for xs\n    y = _ * 2\n    y", 12),
    ],
)
def test_a_fold_that_names_no_variable_reads_the_item_as_underscore(body, want):
    src = f"def f(xs: [int]) -> int\n  {body}\n"
    out = transpile(src)
    assert "for _ in xs" in out
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f([1, 2, 3]) == want
    assert fmt(src) == src


def test_a_fold_over_an_attribute_call_names_no_variable():
    src = "def f(d: {str: int}) -> int\n  sum for d.values(): _\n"
    out = transpile(src)
    assert "sum(_ for _ in d.values())" in out
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f({"a": 2, "b": 5}) == 7


def test_a_loop_may_name_no_variable():
    src = "def f(n: int) -> int\n  k = 0\n  for 0..<n\n    k += 2\n  k\n"
    out = transpile(src)
    assert "for _ in range(0, n):" in out
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f(3) == 6
    assert fmt(src) == src
    assert "for i, x in enumerate(xs):" in transpile(
        "def f(xs: [int]) -> int\n  k = 0\n  for i, x in xs\n    k += i\n  k\n"
    )


def test_a_lambda_may_be_assigned_to_a_name():
    src = "def f(a: int, b: int) -> int\n  add = (x, y) -> x + y\n  add(a, b)\n"
    ns = {}
    exec(transpile(src), ns)
    assert ns["Solution"]().f(2, 3) == 5
    assert fmt(src) == src


def test_a_brace_literal_starting_with_a_colon_is_a_defaultdict():
    src = (
        "def f(xs: [int]) -> int\n"
        "  d = {:list}\n"
        "  e = {:() -> [0, 0]}\n"
        "  s = {1}\n"
        "  for x in xs\n"
        "    d[x % 2] <- x\n"
        "    e[x][0] += 1\n"
        "  len(d[0]) + e[3][0] + len(s)\n"
    )
    py = transpile(src)
    assert "from collections import defaultdict" in py
    assert "defaultdict(list)" in py and "defaultdict(lambda: [0, 0])" in py
    ns = {}
    exec(py, ns)
    assert ns["Solution"]().f([2, 3, 4]) == 4
    assert fmt(src) == src


def test_heap_pushes_and_pops_with_the_list_operators():
    src = (
        "def f(xs: [int]) -> [int]\n"
        "  lo, hi = heap(xs), heap(xs, type=max)\n"
        "  lo <- 0\n"
        "  hi <- 99\n"
        "  [lo ., hi ., hi.peek(), len(lo)]\n"
    )
    ns = {}
    exec(transpile(src), ns)
    assert ns["Solution"]().f([5, 1, 7]) == [0, 99, 7, 3]


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


def test_vscode_grammar_highlights_every_helper():
    """The VS Code grammar's builtin rule names every mu helper, so a new
    helper cannot ship without highlighting."""
    import json

    grammar = json.loads(
        (HERE / "vscode" / "syntaxes" / "mu.tmLanguage.json").read_text()
    )
    rule = grammar["repository"]["builtin"]["match"]
    listed = set(re.search(r"\\b\((.*?)\)\\b", rule).group(1).split("|"))
    from mu import HELPERS

    # Grid and deep are pasted in by the transpiler, never written in mu
    helpers = {h for h in HELPERS if not h.startswith("_")} - {"Grid", "deep"}
    assert helpers <= listed, sorted(helpers - listed)


def test_vscode_grammar_highlights_the_item_underscore():
    import json

    grammar = json.loads(
        (HERE / "vscode" / "syntaxes" / "mu.tmLanguage.json").read_text()
    )
    rule = re.compile(grammar["repository"]["item"]["match"])
    assert rule.search("sum for xs: _ * 2")
    assert not rule.search("_x = 0") and not rule.search("x_ = 0")
    assert {"include": "#item"} in grammar["patterns"]


def test_transpile_maps_every_python_line_to_its_mu_line():
    """transpile(src, mapped=True) gives, per output line, the mu line it
    came from; pasted helpers, blank lines and the class line have none."""
    src = (HERE / "examples" / "2231.mu").read_text()
    code, origin = transpile(src, mapped=True)
    lines = code.split("\n")
    assert len(origin) == len(lines) - 1  # the trailing newline
    mu = src.split("\n")
    for line, o in zip(lines, origin):
        if o is None:
            continue
        assert mu[o - 1].strip() and not mu[o - 1].startswith("#"), (line, o)
    assert origin[lines.index("class Solution:")] is None
    assert origin[lines.index("    def largestInteger(self, num: int) -> int:")] == 2
    assert origin[lines.index("        ds = to_digits(num)")] == 3
    assert (
        origin[lines.index("        return to_int([by[d % 2].pop() for d in ds])")] == 5
    )
    # a file with globals and a script maps the same way
    src = "N = 3\ndef f(a: int) -> int\n  a + N\n\nprint(Solution().f(1))\n"
    code, origin = transpile(src, mapped=True)
    lines = code.split("\n")
    assert len(origin) == len(lines) - 1
    assert origin[lines.index("N = 3")] == 1
    assert origin[lines.index("        return a + N")] == 3
    assert origin[lines.index("print(Solution().f(1))")] == 5


def test_vscode_debug_adapter():
    """The debug adapter's own tests (mu/vscode/adapter.test.js): the
    protocol rewriting, and a live run against the bundled debugpy when the
    Python Debugger extension is installed."""
    import shutil
    import subprocess

    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    run = subprocess.run(
        [node, "--test", str(HERE / "vscode" / "adapter.test.js")],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert run.returncode == 0, run.stdout[-3000:] + run.stderr[-3000:]


def test_a_helper_passed_by_name_is_pasted():
    """`even` in `sort(ds, by=even)` or `[even, odd]` is a use of the helper,
    so its source goes into the output; a file that binds the name keeps its
    own."""
    src = "def f(ds: [int]) -> [int]\n  sort(ds, by=even)\n"
    assert "def even(n):" in transpile(src)
    src = "def f(ds: [int]) -> [int]\n  [r for r in [even, odd]]\n"
    out = transpile(src)
    assert "def even(n):" in out and "def odd(n):" in out
    src = "def f(ds: [int], odd: int) -> int\n  even = 1\n  even + odd\n"
    out = transpile(src)
    assert "def even(n):" not in out and "def odd(n):" not in out


def test_scan_reverse_folds_from_the_right():
    """`scan(max, xs, reverse=True)` is the running max of every suffix."""
    src = "def f(xs: [int]) -> [int]\n  scan(max, xs, reverse=True)\n"
    assert "list(accumulate(xs[::-1], max))[::-1]" in transpile(src)
    src = "def f(xs: [int]) -> [int]\n  scan(+, xs, reverse=True)\n"
    assert "list(accumulate(xs[::-1]))[::-1]" in transpile(src)
    src = "def f(xs: [int]) -> [int]\n  scan(max, xs)\n"
    assert "accumulate(xs, max)" in transpile(src)


def test_every_spec_version_is_linked_from_the_readme():
    """The current version has a spec, and the readme links every spec."""
    specs = sorted(p.name for p in (HERE / "spec").glob("v*.md"))
    assert f"v{VERSION}.md" in specs
    readme = (HERE.parent / "README.md").read_text()
    section = readme.split("## Sitecustomize, harness and helpers")[1].split("\n## ")[0]
    linked = re.findall(r"\(mu/spec/(v[\d.]+\.md)\)", section)
    assert sorted(linked) == specs


def test_memo_block_form_is_a_cached_def_on_a_deep_stack():
    src = (
        "def f(n: int) -> int\n"
        "  memo g(i)\n"
        "    m = []\n"
        "    if i < n\n"
        "      m <- g(i + 1)\n"
        "    return max(m) + 1 if m else 0\n"
        "  return g(0)\n"
    )
    py = transpile(src)
    assert "@cache\n        def g(i):" in py.replace("    def run():\n", "").replace(
        "            ", "        "
    )
    ns = {}
    exec(py, ns)
    assert ns["Solution"]().f(20000) == 20000
    assert fmt(src) == src


def test_memo_block_form_rejects_ret():
    src = "def f(n: int) -> int\n  memo g(i)\n    ret x = i\n  g(n)\n"
    with pytest.raises(MuError):
        transpile(src)


def test_or_if_is_x_or_d_when_x_equals_v():
    out = transpile(
        "def f(t: int, dp: [int]) -> int\n  a = t or -1 if inf\n  dp[t] or -1 if inf\n"
    )
    assert "a = (-1 if t == inf else t)" in out
    assert "return (-1 if (_v := dp[t]) == inf else _v)" in out
    ns = {}
    exec(out, ns)
    assert ns["Solution"]().f(1, [0, 3]) == 3
    assert ns["Solution"]().f(1, [0, float("inf")]) == -1
    out = transpile("def g(t: int) -> int\n  t or -1 if inf\n")
    exec(out, ns)
    assert ns["Solution"]().g(4) == 4
    assert ns["Solution"]().g(float("inf")) == -1


def test_or_if_needs_an_or_and_keeps_the_ternary():
    assert "x if c else y" in transpile(
        "def f(x: int, c: bool, y: int) -> int\n  x if c else y\n"
    )
    assert "(x or y) if c else 0" in transpile(
        "def f(x: int, c: bool, y: int) -> int\n  (x or y) if c else 0\n"
    ) or "x or y if c else 0" in transpile(
        "def f(x: int, c: bool, y: int) -> int\n  x or y if c else 0\n"
    )
    with pytest.raises(MuError):
        transpile("def f(x: int, c: bool) -> int\n  x if c\n")


def test_as_list_returns_the_yields_of_a_def_as_a_list():
    src = (
        "# 78. Subsets\n"
        "@as_list\n"
        "def subsets(nums: [int]) -> [[int]]\n"
        "  for mask in 0..<(1 << len(nums))\n"
        "    yield [x for i, x in nums if mask >> i & 1]\n"
    )
    py = transpile(src)
    assert "    @as_list\n    def subsets(self, nums" in py
    assert "def as_list(f):" in py and "from functools import wraps" in py
    ns = {}
    exec(py, ns)
    assert ns["Solution"]().subsets([1, 2]) == [[], [1], [2], [1, 2]]
    assert fmt(src) == src
    assert fmt(src.replace("@as_list", "@ as_list")) == src


def test_decorators_stack_and_take_arguments():
    src = (
        "def f(n: int) -> int\n"
        "  def add(k)\n"
        "    def wrap(fn)\n"
        "      h = x -> fn(x) + k\n"
        "      h\n"
        "    wrap\n"
        "  def double(fn)\n"
        "    h = x -> fn(x) * 2\n"
        "    h\n"
        "  @double\n"
        "  @add(1)\n"
        "  def g(x)\n"
        "    x\n"
        "  g(n)\n"
    )
    py = transpile(src)
    assert "        @double\n        @add(1)\n        def g(x):" in py
    ns = {}
    exec(py, ns)
    assert ns["Solution"]().f(5) == 12  # add runs first, then double
    assert fmt(src) == src


def test_a_decorator_above_a_memo_wraps_the_cached_function():
    src = (
        "def f(n: int) -> int\n"
        "  def double(fn)\n"
        "    h = x -> fn(x) * 2\n"
        "    h\n"
        "  @double\n"
        "  memo g(i) =\n"
        "    | i == 0 -> 1\n"
        "    | else   -> g(i - 1)\n"
        "  @double\n"
        "  memo h(i)\n"
        "    return i\n"
        "  g(n) + h(n)\n"
    )
    py = transpile(src)
    assert py.count("@double\n            @cache\n            def ") == 2
    ns = {}
    exec(py, ns)
    assert ns["Solution"]().f(2) == 8 + 4
    assert fmt(src) == src


def test_yield_is_a_statement():
    src = (
        "def f(n: int)\n"
        "  for i in 0..<n\n"
        "    if i == 2: yield\n"
        "    yield i, -i\n"
        "  yield from [7]\n"
        "  yield n\n"
    )
    py = transpile(src)
    assert "return yield" not in py  # a last line that yields is not returned
    ns = {}
    exec(py, ns)
    got = list(ns["Solution"]().f(3))
    assert got == [(0, 0), (1, -1), None, (2, -2), 7, 3]


def test_a_def_that_yields_and_defines_a_memo_runs_on_the_deep_stack():
    src = (
        "@as_list\n"
        "def f(g: [[int]]) -> [int]\n"
        "  memo depth(i) =\n"
        "    | i == 0 -> 0\n"
        "    | else   -> 1 + depth(i - 1)\n"
        "  for (i, j) in cells(g)\n"
        "    yield depth(g[i, j])\n"
    )
    ns = {}
    exec(transpile(src), ns)
    assert ns["Solution"]().f([[20000, 1], [2, 3]]) == [20000, 1, 2, 3]


def test_decorator_lines_map_to_their_own_mu_lines():
    src = "@as_list\ndef f(n: int) -> [int]\n  yield n\n"
    code, origin = transpile(src, mapped=True)
    at = {line.strip(): o for line, o in zip(code.split("\n"), origin) if o}
    assert at["@as_list"] == 1
    assert at["def f(self, n: int) -> list[int]:"] == 2
    assert at["yield n"] == 3


def test_a_lambda_may_be_a_dict_value_and_its_body_a_push():
    src = (
        "def f(x: int) -> [int]\n"
        "  stack = []\n"
        "  ops = {\n"
        "    '+': n -> stack <- n,\n"
        "    '-': (s, n) -> s <- -n,\n"
        "    '*': (a, b) -> a * b\n"
        "  }\n"
        "  ops['+'](x)\n"
        "  ops['-'](stack, x)\n"
        "  stack <- ops['*'](x, x)\n"
        "  stack\n"
    )
    ns: dict = {}
    exec(transpile(src), ns)
    assert ns["Solution"]().f(3) == [3, -3, 9]
    src = "def f(d: [int]) -> int\n  {k: (k, 1) for k in d}\n"
    assert "{k: (k, 1) for k in d}" in transpile(src)


def test_a_lambda_may_name_no_argument():
    """`-> e` reads one argument as `_`, several as the tuple `_`."""
    src = (
        "def f(xs: [int]) -> [int]\n"
        "  stack = []\n"
        "  ops = {'+': -> _[0] <- _[1], '2': -> _ * 2}\n"
        "  ops['+'](stack, ops['2'](xs[0]))\n"
        "  double = -> _ * 2\n"
        "  stack <- double(xs[1])\n"
        "  stack + sorted(xs, key=-> -_)\n"
    )
    ns: dict = {}
    exec(transpile(src), ns)
    assert ns["Solution"]().f([1, 5]) == [2, 10, 5, 1]
    assert fmt(src) == src
