import re
import sys
import os

site_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(site_dir, "..", "..", "..", ".."))

sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "utils"))

import bisect
import builtins

# types
from Types import TreeNode
from Types import ListNode
from typing import List, Optional

# shortcuts
from functools import *
from itertools import *
from math import log10, log2, floor, ceil, prod
from collections import defaultdict, Counter
import operator
import heapq
from string import ascii_letters, ascii_lowercase, ascii_uppercase

# utils
from tree_utils import *
from bst_utils import *
from linked_list_utils import *

# pretty printing
from rich import print as rich_print
from tabulate import tabulate

# types
builtins.List = List
builtins.Optional = Optional
builtins.TreeNode = TreeNode
builtins.ListNode = ListNode

# pretty printing
builtins.tabulate = tabulate
builtins.rich_print = rich_print
builtins.draw_tree = draw_tree
builtins.draw_linked_list = draw_linked_list
builtins.draw_general_tree = draw_general_tree

# building
builtins.build_tree = build_tree
builtins.generate_and_print_random_bst = generate_and_print_random_bst
builtins.generate_full_binary_tree = generate_full_binary_tree

# utilities

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
builtins.add = operator.add
builtins.xor = operator.xor
builtins.heapify = heapq.heapify
builtins.heappop = heapq.heappop
builtins.heappush = heapq.heappush
builtins.nlargest = heapq.nlargest
builtins.nsmallest = heapq.nsmallest
builtins.ascii_letters = ascii_letters
builtins.ascii_lowercase = ascii_lowercase
builtins.ascii_uppercase = ascii_uppercase
builtins.match = re.match
