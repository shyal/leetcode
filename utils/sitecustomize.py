"""
sitecustomize.py enables to add or override builtins. This is useful
for calling utility functions without having to import them.

This is not clean, but useful in the context of trying to solve quickly.
"""

import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "utils"))

import builtins

# types
from Types import TreeNode
from typing import List, Optional

# utils
from tree_utils import *
from bst_utils import *

# pretty printing
from rich import print as rich_print
from tabulate import tabulate

# types
builtins.List = List
builtins.Optional = Optional
builtins.TreeNode = TreeNode

# pretty printing
builtins.tabulate = tabulate
builtins.rich_print = rich_print
builtins.draw_tree = draw_tree
builtins.draw_general_tree = draw_general_tree

# building
builtins.build_tree = build_tree
builtins.generate_and_print_random_bst = generate_and_print_random_bst
builtins.generate_full_binary_tree = generate_full_binary_tree

# utilities
builtins.find_node = find_node
builtins.get_inorder = get_inorder
builtins.is_balanced = is_balanced
builtins.is_valid_bst = is_valid_bst
