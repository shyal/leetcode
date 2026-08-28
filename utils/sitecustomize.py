import re
import sys
import os
import importlib.util

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

import bisect
import builtins
from rich.console import Console
from rich.markdown import Markdown
from math import gcd, isclose

# types
from Types import TreeNode
from Types import ListNode
from Types import GraphNode
from Types import Node


# Type aliases
from typing import (
    List as List,
    Optional as Optional,
    Dict as Dict,
    Tuple as Tuple,
    Any as Any,
    Generic as Generic,
    Iterable as Iterable,
    Iterator as Iterator,
    TypeVar as TypeVar,
    Union as Union,
    overload as overload,
)
from collections.abc import Callable as Callable


# shortcuts
import random
from random import randint, randrange, choice, choices, shuffle, sample, uniform, getrandbits
from sys import maxsize
from functools import *
from itertools import *
from math import log10, log2, floor, ceil, prod, sqrt
from collections import defaultdict, Counter, OrderedDict
import operator
import heapq
from collections import deque
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits, hexdigits

# utils
from graph_utils import *
from tree_utils import *
from bst_utils import *
from linked_list_utils import *
from bs_utils import *
from debug_utils import *
from heap_utils import *

# pretty printing
from rich import print as rich_print
from tabulate import tabulate as tabulate_orig

console = Console()


def tabulate(tabular_data, headers=(), row_labels=(), tablefmt="github"):
    if row_labels:
        if len(row_labels) != len(tabular_data):
            raise ValueError("Number of row labels must match number of rows")
        tabular_data = [
            [row_label] + row for row_label, row in zip(row_labels, tabular_data)
        ]
        headers = [""] + list(headers)

    t = tabulate_orig(tabular_data, headers, tablefmt=tablefmt)
    md = Markdown(t)
    console.print(md)
    return md


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
import math as _math
import functools as _functools
import itertools as _itertools
import collections as _collections
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
