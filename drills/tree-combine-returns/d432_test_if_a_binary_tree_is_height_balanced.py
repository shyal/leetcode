"""
EPI 9.1 Test if a binary tree is height-balanced

Given tree, the root of a binary tree, return True when the tree is
height-balanced and False otherwise. A tree is height-balanced when, at
every node, the heights of the left subtree and the right subtree differ
by at most 1. An empty tree is height-balanced.

Example 1:

Input: tree = [1, 2, 3, 4, 5, None, 6, 7]
Output: True
Explanation: at node 2 the subtree heights are 2 and 1, at node 3 they
are 0 and 1, and at node 1 they are 3 and 2.

          1
         / \\
        2   3
       / \\   \\
      4   5   6
     /
    7

Example 2:

Input: tree = [1, 2, 3, 4, None, None, None, 5]
Output: False
Explanation: at node 2 the left subtree has height 2 and the right
subtree has height 0.

Example 3:

Input: tree = []
Output: True

Constraints:

    0 <= number of nodes <= 10^4
    -10^4 <= node.val <= 10^4

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h. NO computing the height of a subtree twice.
"""


class Solution:
    def is_balanced_binary_tree(self, tree: TreeNode | None) -> bool:
        pass


sol = Solution()

t = build_tree([1, 2, 3, 4, 5, None, 6, 7])
draw_tree(t)
print(sol.is_balanced_binary_tree(t))  # True

# assert sol.is_balanced_binary_tree(t) is True
# assert sol.is_balanced_binary_tree(build_tree([1, 2, 3, 4, None, None, None, 5])) is False
# assert sol.is_balanced_binary_tree(None) is True
# assert sol.is_balanced_binary_tree(build_tree([1])) is True
# assert sol.is_balanced_binary_tree(build_tree([1, 2])) is True
# assert sol.is_balanced_binary_tree(build_tree([1, None, 2])) is True
# assert sol.is_balanced_binary_tree(build_tree([1, None, 2, None, 3])) is False
# assert sol.is_balanced_binary_tree(build_tree([1, 2, None, 3])) is False
# assert sol.is_balanced_binary_tree(build_tree([1, 2, 3, 4, 5, 6, 7])) is True
# assert sol.is_balanced_binary_tree(build_tree([1, 2, 3, 4, 5, None, None, 6, 7])) is False
# assert sol.is_balanced_binary_tree(build_tree([1, 2, 3, None, 4, 5, None, None, None, 6])) is False
# assert sol.is_balanced_binary_tree(build_tree([1, 2, 3, 4, None, 5, 6, None, None, None, None, 7])) is True
# chain = build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)])
# assert sol.is_balanced_binary_tree(chain) is False
# assert sol.is_balanced_binary_tree(TreeNode(0, chain, TreeNode(1))) is False
# full = build_tree(list(range(2 ** 13 - 1)))
# assert sol.is_balanced_binary_tree(full) is True
# assert sol.is_balanced_binary_tree(TreeNode(0, full, build_tree(list(range(2 ** 12 - 1))))) is True
# assert sol.is_balanced_binary_tree(TreeNode(0, full, build_tree(list(range(2 ** 11 - 1))))) is False
