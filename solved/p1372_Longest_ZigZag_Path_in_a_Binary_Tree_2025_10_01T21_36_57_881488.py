"""
URL: https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/description/?envType=study-plan-v2&envId=leetcode-75

1372. Longest ZigZag Path in a Binary Tree

You are given the root of a binary tree.

A ZigZag path for a binary tree is defined as follow:

        Choose any node in the binary tree and a direction (right or left).
        If the current direction is right, move to the right child of the current node; otherwise, move to the left child.
        Change the direction from right to left or from left to right.
        Repeat the second and third steps until you can't move in the tree.

Zigzag length is defined as the number of nodes visited - 1. (A single node has a length of 0).

Return the longest ZigZag path contained in that tree.


Example 1:

Input: root = [1,None,1,1,1,None,None,1,1,None,1,None,None,None,1]
Output: 3
Explanation: Longest ZigZag path in blue nodes (right -> left -> right).

Example 2:

Input: root = [1,1,1,None,1,None,None,1,1,None,1]
Output: 4
Explanation: Longest ZigZag path in blue nodes (left -> right -> left -> right).

Example 3:

Input: root = [1]
Output: 0


Constraints:

        The number of nodes in the tree is in the range [1, 5 * 104].
        1 <= Node.val <= 100
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:

        def helper(node, r=0, l=0):
            if node:
                _max[0] = max(_max[0], max(r, l))
                if node.left:
                    helper(node.left, r=0, l=r + 1)
                if node.right:
                    helper(node.right, r=l + 1, l=0)

        _max = [0]
        helper(root)
        return _max[0]


sol = Solution()

tree1 = build_tree([1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1])
assert sol.longestZigZag(tree1) == 3

tree1 = build_tree([1, 1, 1, None, 1, None, None, 1, 1, None, 1])
assert sol.longestZigZag(tree1) == 4

tree1 = build_tree([1])
assert sol.longestZigZag(tree1) == 0

tree4 = build_tree([1, 1, None])
assert sol.longestZigZag(tree4) == 1

tree5 = build_tree([1, None, 1])
assert sol.longestZigZag(tree5) == 1

tree6 = build_tree([1, 1, None, 1, None, 1, None])
assert sol.longestZigZag(tree6) == 1

tree7 = build_tree([1, None, 1, None, 1, None, 1])
assert sol.longestZigZag(tree7) == 1

tree8 = build_tree([1, None, 1, 1, None, None, 1])
assert sol.longestZigZag(tree8) == 3

tree9 = build_tree([1, 1, None, None, 1, 1, None])
assert sol.longestZigZag(tree9) == 3

tree10 = build_tree([1, 1, 1, 1, 1, 1, 1])
assert sol.longestZigZag(tree10) == 2

tree11 = build_tree([1, 1, 1])
assert sol.longestZigZag(tree11) == 1

tree12 = build_tree([1, None, 1, 1, None, None, 1, 1, None])
assert sol.longestZigZag(tree12) == 4

tree13 = build_tree([1, 1, None, None, 1, 1, None, None, 1])
assert sol.longestZigZag(tree13) == 4
