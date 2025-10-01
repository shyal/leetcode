"""
URL: https://leetcode.com/problems/search-in-a-binary-search-tree/description/?envType=study-plan-v2&envId=leetcode-75

700. Search in a Binary Search Tree

You are given the root of a binary search tree (BST) and an integer val.

Find the node in the BST that the node's value equals val and return the subtree rooted with that node. If such a node does not exist, return null.


Example 1:

Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3]

Example 2:

Input: root = [4,2,7,1,3], val = 5
Output: []


Constraints:

        The number of nodes in the tree is in the range [1, 5000].
        1 <= Node.val <= 107
        root is a binary search tree.
        1 <= val <= 107
"""

from tree_utils import build_tree, draw_tree, TreeNode
from typing import Optional, List


class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return
        if root.val == val:
            return root
        if val < root.val and root.left:
            return self.searchBST(root.left, val)
        elif val > root.val and root.right:
            return self.searchBST(root.right, val)


sol = Solution()

tree = build_tree([4, 2, 7, 1, 3])
res = sol.searchBST(tree, 2)
assert res.val == 2

tree = build_tree([4, 2, 7, 1, 3])
res = sol.searchBST(tree, 5)
assert res == None

tree = build_tree([4, 2, 7, 1, 3])
res = sol.searchBST(tree, 2)
assert res.val == 2
assert res.left.val == 1
assert res.right.val == 3
assert res.left.left is None
assert res.left.right is None
assert res.right.left is None
assert res.right.right is None

tree = build_tree([4, 2, 7, 1, 3])
res = sol.searchBST(tree, 5)
assert res == None

tree = build_tree([1])
res = sol.searchBST(tree, 1)
assert res.val == 1
assert res.left is None
assert res.right is None

tree = build_tree([1])
res = sol.searchBST(tree, 2)
assert res == None

tree = build_tree([3, 1, 5])
res = sol.searchBST(tree, 1)
assert res.val == 1
assert res.left is None
assert res.right is None

tree = build_tree([3, 1, 5])
res = sol.searchBST(tree, 5)
assert res.val == 5
assert res.left is None
assert res.right is None

tree = build_tree([3, 1, 5])
res = sol.searchBST(tree, 3)
assert res.val == 3
assert res.left.val == 1
assert res.right.val == 5

tree = build_tree([3, 1, 5])
res = sol.searchBST(tree, 0)
assert res == None

tree = build_tree([3, 1, 5])
res = sol.searchBST(tree, 6)
assert res == None

tree = build_tree([4, 2, 7, 1, 3, 6, 9])
res = sol.searchBST(tree, 7)
assert res.val == 7
assert res.left.val == 6
assert res.right.val == 9
assert res.left.left is None
assert res.left.right is None
assert res.right.left is None
assert res.right.right is None

tree = build_tree([4, 2, 7, 1, 3, 6, 9])
res = sol.searchBST(tree, 2)
assert res.val == 2
assert res.left.val == 1
assert res.right.val == 3

tree = build_tree([4, 2, 7, 1, 3, 6, 9])
res = sol.searchBST(tree, 10)
assert res == None

tree = build_tree([10, 5, 15, 3, 7, 12, 18])
res = sol.searchBST(tree, 7)
assert res.val == 7
assert res.left is None
assert res.right is None

tree = build_tree([10, 5, 15, 3, 7, 12, 18])
res = sol.searchBST(tree, 12)
assert res.val == 12
assert res.left is None
assert res.right is None

tree = build_tree([10, 5, 15, 3, 7, 12, 18])
res = sol.searchBST(tree, 4)
assert res == None

tree = build_tree([50, 30, 70, 20, 40, 60, 80])
res = sol.searchBST(tree, 30)
assert res.val == 30
assert res.left.val == 20
assert res.right.val == 40

tree = build_tree([50, 30, 70, 20, 40, 60, 80])
res = sol.searchBST(tree, 80)
assert res.val == 80
assert res.left is None
assert res.right is None

tree = build_tree([50, 30, 70, 20, 40, 60, 80])
res = sol.searchBST(tree, 90)
assert res == None

tree = build_tree([2, 1, 3])
res = sol.searchBST(tree, 1)
assert res.val == 1

tree = build_tree([2, 1, 3])
res = sol.searchBST(tree, 3)
assert res.val == 3
