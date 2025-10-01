"""
URL: https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/description/?envType=study-plan-v2&envId=leetcode-75

1161. Maximum Level Sum of a Binary Tree

Given the root of a binary tree, the level of its root is 1, the level of its children is 2, and so on.

Return the smallest level x such that the sum of all the values of nodes at level x is maximal.


Example 1:

Input: root = [1,7,0,7,-8,None,None]
Output: 2
Explanation:
Level 1 sum = 1.
Level 2 sum = 7 + 0 = 7.
Level 3 sum = 7 + -8 = -1.
So we return the level with the maximum sum which is level 2.

Example 2:

Input: root = [989,None,10250,98693,-89388,None,None,None,-32127]
Output: 2


Constraints:

        The number of nodes in the tree is in the range [1, 104].
        -105 <= Node.val <= 105
"""

from typing import Optional, List
from collections import defaultdict


class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        D = defaultdict(int)

        def dfs(node, depth):
            if node:
                D[depth] += node.val
                dfs(node.left, depth + 1)
                dfs(node.right, depth + 1)

        dfs(root, 1)
        levels = [*D.items()]
        max_val = max(levels, key=lambda x: x[1])[1]
        max_levels = [*filter(lambda x: x[1] == max_val, levels)]
        sorted_max_levels = sorted(max_levels, key=lambda x: x[0])
        return next(iter(sorted_max_levels))[0]


sol = Solution()

tree = build_tree([1, 7, 0, 7, -8, 4, 5])
res = sol.maxLevelSum(tree)
assert res == 3

tree = build_tree([1, 7, 0, 7, -8, None, None])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([989, None, 10250, 98693, -89388, None, None, None, -32127])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([1])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([1, 2, 3])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([1, None, 3])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([-1, -2, -3])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([1, -10, -5, 1, 2])
res = sol.maxLevelSum(tree)
assert res == 3

tree = build_tree([0, 3, -3])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([1, 2, None, 3, None])
res = sol.maxLevelSum(tree)
assert res == 3

tree = build_tree([1, None, 2, None, 3])
res = sol.maxLevelSum(tree)
assert res == 3

tree = build_tree([100, 50, 50, 25, 25, 25, 25])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([10, -20, 30, -40, 50])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([5, 4, 6])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([-100, -50, -50])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([100000, -100000, 100000])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([2, -1, 1])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([1, 1, 1, 1, 1, 1, 1])
res = sol.maxLevelSum(tree)
assert res == 3

tree = build_tree([1, 10, 10, 5, 5, 5, 5])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([1, None, 1, None, 1])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([-1, -2, 1])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([4, 1, 1, 1, 1, 1, 1])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([0, 0, 0, 0, 0, 0, 0])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([3, None, 6, None, 6])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([-6, None, -3, None, -3])
res = sol.maxLevelSum(tree)
assert res == 2

tree = build_tree([5, None, 4, None, 5])
res = sol.maxLevelSum(tree)
assert res == 1

tree = build_tree([1, 2, 2, 1, 1, 1, 1])
res = sol.maxLevelSum(tree)
assert res == 2
