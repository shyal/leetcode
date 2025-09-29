"""
sitecustomize.py enables to add or override builtins. This is useful
for calling utility functions without having to import them.

This is not clean, but useful in the context of trying to solve quickly.
"""

import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "utils"))

from Types import TreeNode
from tree_utils import (
    build_tree,
    draw_tree,
    draw_general_tree,
    generate_full_binary_tree,
    find_node,
    get_inorder,
    is_balanced,
)
from bst_utils import generate_and_print_random_bst, is_valid_bst
import builtins
from typing import List, Optional
from rich import print as rich_print
from tabulate import tabulate
from rich.markup import escape
import re
from copy import copy

_global = {"is_tree": False}

org_print = copy(print)


def _print(*args, **kwargs):
    if _global["is_tree"]:
        org_print(*args, **kwargs)
        return
    if type(args[0]) is TreeNode:
        _global["is_tree"] = True
        org_print(draw_tree(args[0]))
        _global["is_tree"] = False
        return
    if args and isinstance(args[0], list):
        is_table = all(isinstance(x, list) for x in args[0])
        if is_table:
            table_str = tabulate(*args, **kwargs)
            rich_print(table_str)
            return
    new_args = []
    for a in args:
        if isinstance(a, str):
            if re.search(r"(?<!\\)\[.*?(?<!\\)\]", a):
                # new_args.append(escape(a))
                new_args.append(a)
            else:
                new_args.append(a)
        else:
            new_args.append(a)
    rich_print(*new_args, **kwargs)


# builtins.print = _print
builtins.List = List
builtins.Optional = Optional
builtins.print_table = _print
builtins.build_tree = build_tree
builtins.TreeNode = TreeNode
builtins.draw_tree = draw_tree
builtins.draw_general_tree = draw_general_tree
builtins.generate_and_print_random_bst = generate_and_print_random_bst
builtins.generate_full_binary_tree = generate_full_binary_tree
builtins.find_node = find_node
builtins.get_inorder = get_inorder
builtins.is_balanced = is_balanced
builtins.is_valid_bst = is_valid_bst
