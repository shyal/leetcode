"""
URL: https://leetcode.com/problems/maximum-depth-of-binary-tree/description/?envType=study-plan-v2&envId=leetcode-75

104. Maximum Depth of Binary Tree

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.


Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:

Input: root = [1,null,2]
Output: 2


Constraints:

        The number of nodes in the tree is in the range [0, 104].
        -100 <= Node.val <= 100
"""

from typing import List, Optional
from tree_utils import build_tree


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:

        def helper(node):
            return 1 + max(
                helper(node.left) if node.left else 0,
                helper(node.right) if node.right else 0,
            )

        return helper(root) if root else 0


sol = Solution()

tree1 = build_tree([3, 9, 20, None, None, 15, 7])
assert sol.maxDepth(tree1) == 3

tree2 = build_tree([1, None, 2])
assert sol.maxDepth(tree2) == 2

tree3 = build_tree([])
assert sol.maxDepth(tree3) == 0

tree4 = build_tree([5])
assert sol.maxDepth(tree4) == 1

tree5 = build_tree([1, 2])
assert sol.maxDepth(tree5) == 2

tree6 = build_tree([1, 2, None, 3, None, None, 4])
assert sol.maxDepth(tree6) == 4

tree7 = build_tree([1, None, 2, None, 3, None, 4])
assert sol.maxDepth(tree7) == 4

tree8 = build_tree([1, 2, 3, 4, 5])
assert sol.maxDepth(tree8) == 3

tree9 = build_tree([1, 2, 3, 4, None, None, None, 5])
assert sol.maxDepth(tree9) == 4

tree10 = build_tree([1, None, 2, None, 3])
assert sol.maxDepth(tree10) == 3
