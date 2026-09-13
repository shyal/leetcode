import importlib.util
import os
import re
import sys

# This file mirrors LeetCode's preloads for solves run inside the repo venv.
# Any other interpreter that inherits PYTHONPATH=./utils (litecli, uv tools,
# system python) lacks rich/tabulate and would print "Error in sitecustomize".
# site.py swallows exactly one thing silently: an ImportError whose name is
# 'sitecustomize'. Use it to opt out.
if importlib.util.find_spec("rich") is None:
    raise ImportError("not the leet venv; skipping sitecustomize", name="sitecustomize")

site_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(site_dir, "..", "..", "..", ".."))

sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "utils"))
sys.path.insert(0, os.path.join(project_root, "utils", "harness"))

import bisect
import builtins
import heapq
import operator

# shortcuts
import random
from collections import Counter, OrderedDict, defaultdict, deque
from collections.abc import Callable as Callable
from functools import *
from itertools import *
from math import ceil, floor, gcd, isclose, log2, log10, prod, sqrt
from random import (
    choice,
    choices,
    getrandbits,
    randint,
    randrange,
    sample,
    shuffle,
    uniform,
)
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits, hexdigits
from sys import maxsize
from typing import (
    Any as Any,
)
from typing import (
    Dict as Dict,
)
from typing import (
    Generic as Generic,
)
from typing import (
    Iterable as Iterable,
)
from typing import (
    Iterator as Iterator,
)

# Type aliases
from typing import (
    List as List,
)
from typing import (
    Optional as Optional,
)
from typing import (
    Tuple as Tuple,
)
from typing import (
    TypeVar as TypeVar,
)
from typing import (
    Union as Union,
)
from typing import (
    overload as overload,
)

from bs_utils import *
from bst_utils import *
from debug_utils import *

# utils
from graph_utils import *
from heap_utils import *
from linked_list_utils import *

# pretty printing
from rich import print as rich_print
from rich.console import Console
from tabulate import tabulate as tabulate_orig
from tree_utils import *

# types
from Types import GraphNode, ListNode, Node, TreeNode

from dsa.maxheapq import (
    maxheapify,
    maxheappeek,
    maxheappop,
    maxheappush,
    maxheappushpop,
    maxheapreplace,
)

console = Console()


_PALETTE = [
    "bright_blue",
    "cyan",
    "green",
    "bright_green",
    "yellow",
    "bright_yellow",
    "orange1",
    "bright_red",
    "magenta",
    "bright_magenta",
    "deep_pink1",
    "white",
]


def _cell_style(v, ranks):
    """Each distinct number in the table gets its own color, by rank."""
    if v is None or v == "":
        return "dim"
    if isinstance(v, bool):
        return "bold green" if v else "bold red"
    if isinstance(v, (int, float)):
        if v == 0:
            return "dim"
        return _PALETTE[ranks[v] % len(_PALETTE)]
    return "yellow"


def tabulate(tabular_data, headers=(), row_labels=(), tablefmt="github"):
    """Print a grid as a colored table. With no headers, columns and rows are
    labelled by index, like a dp table. A flat list is one row."""
    from rich.table import Table  # ~20ms, only when a table is printed

    tabular_data = list(tabular_data)
    if tabular_data and not isinstance(tabular_data[0], (list, tuple)):
        tabular_data = [tabular_data]
    if not headers and tabular_data:
        headers = list(range(max(len(row) for row in tabular_data)))
        row_labels = row_labels or list(range(len(tabular_data)))
    if row_labels and len(row_labels) != len(tabular_data):
        raise ValueError("Number of row labels must match number of rows")

    t = Table(header_style="bold magenta", border_style="bright_black")
    if row_labels:
        t.add_column("", style="bold cyan", justify="right")
    for h in headers:
        t.add_column(str(h), justify="right")
    nums = {v for row in tabular_data for v in row if isinstance(v, (int, float))}
    ranks = {v: r for r, v in enumerate(sorted(nums - {0}))}
    for i, row in enumerate(tabular_data):
        cells = [f"[{_cell_style(v, ranks)}]{v}[/]" for v in row]
        if row_labels:
            cells = [str(row_labels[i])] + cells
        t.add_row(*cells)
    console.print(t)
    return t


_SCALAR = (int, float, str, bool, type(None))


def _is_grid(x):
    """A non-empty list of lists (or tuples) whose entries are all scalars."""
    if not isinstance(x, (list, tuple)) or not x:
        return False
    return all(
        isinstance(row, (list, tuple)) and all(isinstance(v, _SCALAR) for v in row)
        for row in x
    )


def _is_adjacency_list(x):
    """A ragged list of lists of ints: index i lists the neighbors of i.
    A rectangular one is a grid and prints as a table."""
    if not _is_grid(x) or not all(isinstance(v, int) for row in x for v in row):
        return False
    return len({len(row) for row in x}) > 1


def _is_adjacency(x):
    """A non-empty dict whose values are all containers of neighbors."""
    if not isinstance(x, dict) or not x:
        return False
    return all(isinstance(v, (dict, list, tuple, set)) for v in x.values())


def _graph_node_to_adj(node):
    adj = {}
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.val in adj:
            continue
        adj[cur.val] = [nb.val for nb in cur.neighbors]
        stack.extend(cur.neighbors)
    return adj


def _drawer_for(x):
    """The draw function that fits x, or None to print it as-is."""
    if isinstance(x, ListNode):
        return draw_linked_list
    if isinstance(x, TreeNode):
        return draw_tree
    if isinstance(x, Node):
        return draw_general_tree
    if isinstance(x, GraphNode):
        return lambda n: draw_ascii_graph(_graph_node_to_adj(n))
    if _is_adjacency(x):
        return draw_ascii_graph
    if _is_adjacency_list(x):
        return lambda adj: draw_ascii_graph(dict(enumerate(adj)))
    if _is_grid(x):
        return tabulate
    return None


print_orig = builtins.print
_drawing = False


def pprint(*args, **kwargs):
    """print, but a linked list, tree, graph or grid goes to its draw function.

    Plain arguments print as usual. A `file=` keyword bypasses drawing."""
    global _drawing
    if _drawing or "file" in kwargs:
        return print_orig(*args, **kwargs)
    sep = kwargs.pop("sep", " ")

    def flush(plain):
        text = sep.join(str(a) for a in plain)
        console.print(text, markup=False, highlight=True, soft_wrap=True, **kwargs)

    plain = []
    for arg in args:
        draw = _drawer_for(arg)
        if draw is None:
            plain.append(arg)
            continue
        if plain:
            flush(plain)
            plain = []
        _drawing = True
        try:
            draw(arg)
        finally:
            _drawing = False
    if plain or not args:
        flush(plain)
    return None


# types
builtins.List = List
builtins.Optional = Optional
builtins.Dict = Dict
builtins.Tuple = Tuple
builtins.Any = Any
builtins.Callable = Callable
builtins.Generic = Generic
builtins.Iterable = Iterable
builtins.Iterator = Iterator
builtins.TypeVar = TypeVar
builtins.Union = Union
builtins.overload = overload
builtins.TreeNode = TreeNode
builtins.ListNode = ListNode
builtins.GraphNode = GraphNode
builtins.Node = Node

# pretty printing
builtins.tabulate = tabulate
builtins.print_orig = print_orig
builtins.pprint = pprint
if os.environ.get("PRETTY_PRINT", "").lower() not in ("", "0", "false"):
    builtins.print = pprint
builtins.rich_print = rich_print
builtins.draw_tree = draw_tree
builtins.draw_linked_list = draw_linked_list
builtins.draw_general_tree = draw_general_tree
builtins.get_level_order = get_level_order
builtins.debug_var = debug_var
builtins.debug_vars = debug_vars
builtins.viz_binary_search = viz_binary_search
builtins.draw_ascii_graph = draw_ascii_graph
builtins.draw_graphviz = draw_graphviz
builtins.draw_graph = draw_graph
builtins.draw_heap = draw_heap

# building
builtins.build_tree = build_tree
builtins.generate_and_print_random_bst = generate_and_print_random_bst
builtins.generate_full_binary_tree = generate_full_binary_tree
builtins.build_graph_from_edge_list = build_graph_from_edge_list

# utilities
builtins.deque = deque
builtins.get_adj_list = get_adj_list
builtins.build_graph = build_graph
builtins.get_list_values = get_list_values
builtins.print_linked_list = print_linked_list
builtins.build_linked_list = build_linked_list
builtins.find_node = find_node
builtins.get_inorder = get_inorder
builtins.is_balanced = is_balanced
builtins.is_valid_bst = is_valid_bst
builtins.groupby = groupby
builtins.combinations = combinations
builtins.log10 = log10
builtins.log2 = log2
builtins.floor = floor
builtins.ceil = ceil
builtins.pairwise = pairwise
builtins.zip_longest = zip_longest
builtins.reduce = reduce
builtins.takewhile = takewhile
builtins.prod = prod
builtins.product = product
builtins.defaultdict = defaultdict
builtins.dd = defaultdict
builtins.enumr = enumerate
builtins.accumulate = accumulate
builtins.bisect_left = bisect.bisect_left
builtins.bisect_right = bisect.bisect_right
builtins.chain = chain
builtins.Counter = Counter
builtins.OrderedDict = OrderedDict
builtins.add = operator.add
builtins.iadd = operator.iadd
builtins.sub = operator.sub
builtins.isub = operator.isub
builtins.xor = operator.xor
builtins.ixor = operator.ixor
# the module objects themselves, mirroring leetcode's preloaded imports
import collections as _collections
import functools as _functools
import itertools as _itertools
import math as _math
import string as _string

builtins.math = _math
builtins.functools = _functools
builtins.itertools = _itertools
builtins.collections = _collections
builtins.string = _string
builtins.bisect = bisect
builtins.re = re
builtins.operator = operator

builtins.heapq = heapq
builtins.heapify = heapq.heapify
builtins.heappop = heapq.heappop
builtins.heappush = heapq.heappush
builtins.nlargest = heapq.nlargest
builtins.nsmallest = heapq.nsmallest
builtins.maxheapify = maxheapify
builtins.maxheappop = maxheappop
builtins.maxheappush = maxheappush
builtins.maxheappushpop = maxheappushpop
builtins.maxheapreplace = maxheapreplace
builtins.maxheappeek = maxheappeek
builtins.ascii_letters = ascii_letters
builtins.hexdigits = hexdigits
builtins.ascii_lowercase = ascii_lowercase
builtins.ascii_uppercase = ascii_uppercase
builtins.digits = digits
builtins.match = re.match
builtins.permutations = permutations
builtins.or_ = operator.or_
builtins.ior = operator.ior
builtins.and_ = operator.and_
builtins.mul = operator.mul
builtins.truediv = operator.truediv
builtins.floordiv = operator.floordiv
builtins.islice = islice
builtins.compress = compress
builtins.sqrt = sqrt
builtins.starmap = starmap
builtins.maxsize = maxsize
builtins.cache = cache
builtins.gcd = gcd
builtins.isclose = isclose
builtins.dropwhile = dropwhile
builtins.build_nary_tree = build_nary_tree

# random, as leetcode preloads it: the module by name plus the common functions bare
builtins.random = random
builtins.randint = randint
builtins.randrange = randrange
builtins.choice = choice
builtins.choices = choices
builtins.shuffle = shuffle
builtins.sample = sample
builtins.uniform = uniform
builtins.getrandbits = getrandbits


def batched(s, n=1):
    r = list(range(0, len(s), n))
    return [s[a:b] for a, b in zip_longest(r, r[1:])]


def ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("Denominator b must be positive.")
    if a < 0:
        raise ValueError("Numerator a must be non-negative.")
    return (a + b - 1) // b


builtins.batched = batched
builtins.ceil_div = ceil_div


import sys
from io import StringIO


def run_with_input(input_str, main):
    original_stdin = sys.stdin
    sys.stdin = StringIO(input_str)
    original_stdout = sys.stdout
    output = StringIO()
    sys.stdout = output
    try:
        main()
        return output.getvalue().strip()
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout


builtins.run_with_input = run_with_input


def _assert_hook(exc_type, exc, tb):
    """On a failed `assert left == right`, print the traceback and then both
    sides. Plain python prints a bare AssertionError; this is what pytest's
    assertion rewriting gave the branch run, without the 200ms pytest import.
    Both sides are evaluated again in the failing frame."""
    sys.__excepthook__(exc_type, exc, tb)
    if exc_type is not AssertionError or exc.args:
        return
    import ast
    import linecache

    while tb.tb_next:
        tb = tb.tb_next
    frame, lineno = tb.tb_frame, tb.tb_lineno
    filename = frame.f_code.co_filename
    src = "".join(linecache.getlines(filename))
    try:
        tree = ast.parse(src, filename)
    except SyntaxError:
        return
    node = next(
        (
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.Assert)
            and n.lineno <= lineno <= (n.end_lineno or n.lineno)
        ),
        None,
    )
    test = node.test if node else None
    if not (isinstance(test, ast.Compare) and len(test.ops) == 1):
        return
    sides = [test.left, test.comparators[0]]
    op = type(test.ops[0]).__name__
    for label, expr in zip(("left ", "right"), sides):
        code = compile(ast.Expression(expr), filename, "eval")
        try:
            val = eval(code, frame.f_globals, frame.f_locals)
        except Exception as e:  # noqa: BLE001
            val = f"<{type(e).__name__}: {e}>"
        print(f"{label}: {val!r}", file=sys.stderr)
    if op != "Eq":
        print(f"op   : {op}", file=sys.stderr)


sys.excepthook = _assert_hook
