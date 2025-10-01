"""
URL: https://leetcode.com/problems/binary-tree-right-side-view/description/?envType=study-plan-v2&envId=leetcode-75

199. Binary Tree Right Side View

Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.


Example 1:

Input: root = [1,2,3,None,5,None,4]

Output: [1,3,4]

Explanation:

Example 2:

Input: root = [1,2,3,4,None,None,None,5]

Output: [1,3,4,5]

Explanation:

Example 3:

Input: root = [1,None,3]

Output: [1,3]

Example 4:

Input: root = []

Output: []


Constraints:

        The number of nodes in the tree is in the range [0, 100].
        -100 <= Node.val <= 100
"""

from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node, depth=0):
            if not node:
                return
            if depth > data["max_depth"]:
                right_side.append(node.val)
                data["max_depth"] = depth
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        data = {"max_depth": -1}
        right_side = []
        dfs(root, 0)
        return right_side


sol = Solution()

sol = Solution()

tree = build_tree([1, 2, 3, None, 5, None, 4])
res = sol.rightSideView(tree)
assert res == [1, 3, 4]

tree = build_tree([1, 2, 3, 4, None, None, None, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 4, 5]

tree = build_tree([1, 2, 3, 4, 7, 6, 8, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 8, 5]

tree = build_tree([])
res = sol.rightSideView(tree)
assert res == []

tree = build_tree([1])
res = sol.rightSideView(tree)
assert res == [1]

tree = build_tree([1, None, 3])
res = sol.rightSideView(tree)
assert res == [1, 3]

tree = build_tree([1, 2, None])
res = sol.rightSideView(tree)
assert res == [1, 2]

tree = build_tree([1, 2, 3])
res = sol.rightSideView(tree)
assert res == [1, 3]

tree = build_tree([1, 2, 3, 4, 5, 6, 7])
res = sol.rightSideView(tree)
assert res == [1, 3, 7]

tree = build_tree([1, 2, None, 3, None, 4, None])
res = sol.rightSideView(tree)
assert res == [1, 2, 3, 4]

tree = build_tree([1, None, 2, None, 3])
res = sol.rightSideView(tree)
assert res == [1, 2, 3]

tree = build_tree([1, -2, 3, None, 4, None, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 5]

tree = build_tree([10, 20, 30, 40, 50, None, None, None, None, 60])
res = sol.rightSideView(tree)
assert res == [10, 30, 50, 60]

tree = build_tree([5, 4, None, 3, None, 2, None])
res = sol.rightSideView(tree)
assert res == [5, 4, 3, 2]

tree = build_tree([100, 99, 98, 97, 96])
res = sol.rightSideView(tree)
assert res == [100, 98, 96]

tree = build_tree([1, 3, 2])
res = sol.rightSideView(tree)
assert res == [1, 2]

tree = build_tree([1, 2, 3, 4, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 5]

tree = build_tree([0, -100, 100, -50, 50])
res = sol.rightSideView(tree)
assert res == [0, 100, 50]
