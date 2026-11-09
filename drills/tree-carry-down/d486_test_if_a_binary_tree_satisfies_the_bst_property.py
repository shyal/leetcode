"""
EPI 14.1 Test if a binary tree satisfies the BST property

Given tree, the root of a binary tree, return True when it satisfies the
BST property and False otherwise. The BST property holds when, at every
node, each key in the left subtree is less than or equal to the node key,
and each key in the right subtree is greater than or equal to it. An
empty tree satisfies the BST property.

Example 1:

Input: tree = [8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13]
Output: True

          8
         / \\
        3   10
       / \\    \\
      1   6    14
         / \\   /
        4   7 13

Example 2:

Input: tree = [8, 3, 10, 1, 9]
Output: False
Explanation: 9 is in the left subtree of 8, and 9 is greater than 8.

Example 3:

Input: tree = [5, 5, 5]
Output: True
Explanation: equal keys are allowed on both sides.

Constraints:

    0 <= number of nodes <= 10^4
    -2^31 <= node.val <= 2^31 - 1

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h. NO list of the keys.
"""


class Solution:
    def is_binary_tree_bst(self, tree: TreeNode | None) -> bool:
        pass


sol = Solution()

t = build_tree([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
draw_tree(t)
print(sol.is_binary_tree_bst(t))  # True

# assert sol.is_binary_tree_bst(t) is True
# assert sol.is_binary_tree_bst(build_tree([8, 3, 10, 1, 9])) is False
# assert sol.is_binary_tree_bst(build_tree([5, 5, 5])) is True
# assert sol.is_binary_tree_bst(None) is True
# assert sol.is_binary_tree_bst(build_tree([1])) is True
# assert sol.is_binary_tree_bst(build_tree([2, 1])) is True
# assert sol.is_binary_tree_bst(build_tree([1, 2])) is False
# assert sol.is_binary_tree_bst(build_tree([1, None, 0])) is False
# assert sol.is_binary_tree_bst(build_tree([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 7])) is False
# assert sol.is_binary_tree_bst(build_tree([8, 3, 10, 1, 6, None, 14, None, None, 2, 7, 13])) is False
# assert sol.is_binary_tree_bst(build_tree([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 10])) is True
# assert sol.is_binary_tree_bst(build_tree([-2 ** 31, None, 2 ** 31 - 1])) is True
# assert sol.is_binary_tree_bst(build_tree([2 ** 31 - 1, 2 ** 31 - 1, None, None, 2 ** 31 - 1])) is True
# chain = build_tree([0] + [v for k in range(1, 499) for v in (None, k)])
# assert sol.is_binary_tree_bst(chain) is True
# assert sol.is_binary_tree_bst(TreeNode(250, chain)) is False
# keys = [(2 * p + 1) * 2 ** (12 - d) - 1 for d in range(13) for p in range(2 ** d)]
# assert sol.is_binary_tree_bst(build_tree(keys)) is True
# assert sol.is_binary_tree_bst(build_tree(keys[:-1] + [0])) is False
# assert sol.is_binary_tree_bst(build_tree(keys[:-1] + [2 ** 13 - 3])) is True
