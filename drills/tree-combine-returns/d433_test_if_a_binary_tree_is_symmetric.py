"""
EPI 9.2 Test if a binary tree is symmetric

Given tree, the root of a binary tree, return True when the tree is
symmetric and False otherwise. A tree is symmetric when its left subtree
is the mirror image of its right subtree: the same shape reflected about
the root, with equal values at reflected positions. An empty tree is
symmetric.

Example 1:

Input: tree = [1, 2, 2, 3, 4, 4, 3]
Output: True

          1
        /   \\
       2     2
      / \\   / \\
     3   4 4   3

Example 2:

Input: tree = [1, 2, 2, None, 3, None, 3]
Output: False
Explanation: the shapes are not mirror images. The left 2 has a right
child, and the right 2 also has a right child.

Example 3:

Input: tree = [1, 2, 3]
Output: False
Explanation: the shapes are mirror images, but 2 and 3 are not equal.

Constraints:

    0 <= number of nodes <= 10^4
    -100 <= node.val <= 100

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h. NO copy of the tree.
"""


class Solution:
    def is_symmetric(self, tree: TreeNode | None) -> bool:
        pass


sol = Solution()

t = build_tree([1, 2, 2, 3, 4, 4, 3])
draw_tree(t)
print(sol.is_symmetric(t))  # True

# assert sol.is_symmetric(t) is True
# assert sol.is_symmetric(build_tree([1, 2, 2, None, 3, None, 3])) is False
# assert sol.is_symmetric(build_tree([1, 2, 3])) is False
# assert sol.is_symmetric(None) is True
# assert sol.is_symmetric(build_tree([1])) is True
# assert sol.is_symmetric(build_tree([1, 2])) is False
# assert sol.is_symmetric(build_tree([1, None, 2])) is False
# assert sol.is_symmetric(build_tree([1, 2, 2])) is True
# assert sol.is_symmetric(build_tree([1, 2, 2, 3, None, None, 3])) is True
# assert sol.is_symmetric(build_tree([1, 2, 2, 3, None, 3])) is False
# assert sol.is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3, 5, None, None, 6, 6, None, None, 5])) is True
# assert sol.is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3, 5, None, None, 6, 6, None, None, 7])) is False
# assert sol.is_symmetric(build_tree([0, -1, -1, None, -2, -2])) is True
# left = build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)])
# right = build_tree([498] + [v for k in range(497, -1, -1) for v in (None, k)])
# assert sol.is_symmetric(TreeNode(7, left, right)) is True
# assert sol.is_symmetric(TreeNode(7, left, left)) is False
# assert sol.is_symmetric(build_tree([5] * (2 ** 13 - 1))) is True
# assert sol.is_symmetric(build_tree([5] * (2 ** 13 - 2) + [6])) is False
