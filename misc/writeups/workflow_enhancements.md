# Offline solving workflow

Ok first of all, i'm not advocating everyone should work offline. But for those who want to do so, in Python, here are some really useful workflow enhancements i've recently discovered.

- Copy description and Solution class to a local .py file, e.g `current.py`.
- Copy solution
- Structure something like this:

```python

"""
Problem description
"""

class Solution:
    def func(self, root: Optional[TreeNode]) -> bool:
        pass


sol = Solution()
tree = build_tree([...])
assert sol.func(...) == check_tree(...)
assert sol.func(...) == check_tree(...)

```

There are couple of immediate drawbacks:

- missing `Optional` and `List` every single time (which gets very annoying if you're aiming for a high number of solves).
- the need to import custom utilities, like `print` from the `rich` module, custom `tree_utils`, `bst_utils` or whatever else you've built for custom tree building, tree checking etc. or things like `tabulate`, `PrettyPrintTree` etc.
- python's `assert` doesn't show the expected value, and it only shows the backtrace and line number.

# sitecustomize.py

You can modify `.venv/lib/pythonX.X/site-packages/sitecustomize.py` to add more builtins.

Example `sitecustomize.py`:

```python
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

```

This "hack" (yes it feels a bit like a hack - but a useful one) allows to write solutions with no imports, which really lets you just focus on solving and nothing else.

```python3

"""
URL: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

108. Convert Sorted Array to Binary Search Tree

Given an integer array ....

"""

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def helper(start, end):
            if start < end:
                mid = (start + end) // 2
                return TreeNode(nums[mid], helper(start, mid), helper(mid + 1, end))

        return helper(0, len(nums))


sol = Solution()

assert get_inorder(sol.sortedArrayToBST([-10, -3, 0, 5, 9])) == [-10, -3, 0, 5, 9]
assert is_balanced(sol.sortedArrayToBST([-10, -3, 0, 5, 9]))
assert is_valid_bst(sol.sortedArrayToBST([-10, -3, 0, 5, 9]))
assert get_inorder(sol.sortedArrayToBST([1, 3])) == [1, 3]
assert is_balanced(sol.sortedArrayToBST([1, 3]))
assert is_valid_bst(sol.sortedArrayToBST([1, 3]))
```

But why bother with no imports? Well if you want to solve hundreds, or thousands of questions, then saving yourself a few seconds here and there makes sense.. also if you then paste the solution in a file with many others, you don't have to bother thinking about deleting the imports etc. because they're now python builtins.

I realize this is a debatable approach (adding builtins feels last resort for some reason), so not right for everyone. For me, making the stuff i use constantly python `builtins` makes sense, for now.

# Fixing `assert` with `pytest`

Assert not showing the expected result is a major annoyance.

## Assert without pytest

![image.png](https://assets.leetcode.com/users/images/3be90616-39b9-49f2-b399-20b43f8100c6_1759113896.3348942.png)

This can be fixed with `pytest`, without the need for a test function

## Assert with pytest

![image.png](https://assets.leetcode.com/users/images/31740547-dc70-4212-9dd1-70d0722cf2f1_1759113966.0869079.png)

Ah this is great, because we can see the values (even if stored in a variable) and we don't have to jump back to the file to see which line failed.

To use `pytest`'s assert without needing a test function, you can create a `runner.py`:

```python3
import pytest

pytest.register_assert_rewrite("leetcode")
pytest.register_assert_rewrite("leetcode_easy")
pytest.register_assert_rewrite("leetcode_medium")
pytest.register_assert_rewrite("leetcode_hard")
pytest.register_assert_rewrite("current")


def test_current():
    import leetcode
    import leetcode_easy
    import leetcode_medium
    import leetcode_hard
    import current


if __name__ == "__main__":
    pytest.main([__file__, "-s", "-q"])
```

Then simply run your code with something like:

```python3
PYTHONPATH=./utils:${PYTHONPATH} python3 utils/runner.py
```

e.g via a `makefile`.

# Useful third party modules

[PrettyPrintTree](https://github.com/AharonSambol/PrettyPrintTree)
[tabulate](https://pypi.org/project/tabulate/)
[rich](https://rich.readthedocs.io/en/latest/introduction.html)

And of course, you should build your own, for dealing with linked lists, trees, binary trees, bsts, graphs etc. that's where you can really focus on fundamentals rather than solving.

# Git and custom scripts

Of course you should use git. You can then write custom scripts (or ask AI to write the scripts for you) to scan your git history, compute your solve rate, compute estimates for your milestones etc.

# But why bother? Leetcode's interface is excellent

Leetcode is amazing, and it's actually faster to just solve directly in the interface. But for me this is worth it because:

- I can very easily organize, access and review solutions.. i have my own ratings e.g `leetcode_easy.py` for the no brainers, `leetcode_medium.py` for the stuff i have to think about, or want to review and `leetcode_hard.py` for the mind benders.
- Git add, so i can easily go back when i need, or branching and commits to tackle a hard problem step by step (e.g brutforce, pseudocode, solve, try different approaches etc.)
- My regular day to day IDE.
- Organize important algorithms, and data structures that can be used frequently for solving. Again, incorporate fundamentals side by side with my solving workflow.

Happy solving!
