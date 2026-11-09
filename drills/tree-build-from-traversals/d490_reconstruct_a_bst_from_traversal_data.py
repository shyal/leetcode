"""
EPI 14.5 Reconstruct a BST from traversal data

Given the preorder list preorder_sequence of the keys of a binary search
tree, return the root of that tree. Every key is distinct, so the
preorder list alone fixes exactly one BST. An empty list gives None.

Example 1:

Input: preorder_sequence = [20, 9, 5, 12, 11, 14, 25]
Output: the root of [20, 9, 25, 5, 12, None, None, None, None, 11, 14]

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

Example 2:

Input: preorder_sequence = [3, 2, 1]
Output: the root of [3, 2, None, 1]

Example 3:

Input: preorder_sequence = []
Output: None

Constraints:

    0 <= len(preorder_sequence) <= 10^5
    preorder_sequence is the preorder list of a BST with distinct keys.

    REQUIRED: O(n) time for n keys. NO sorting. NO list slices.
"""


class Solution:
    def rebuild_bst_from_preorder(self, preorder_sequence: list[int]) -> TreeNode | None:
        pass


sol = Solution()

t = sol.rebuild_bst_from_preorder([20, 9, 5, 12, 11, 14, 25])
draw_tree(t)
print(get_level_order(t))  # [20, 9, 25, 5, 12, None, None, None, None, 11, 14]


def preorder_of(node: TreeNode | None) -> list[int]:
    return [node.val] + preorder_of(node.left) + preorder_of(node.right) if node else []


# assert get_level_order(t) == [20, 9, 25, 5, 12, None, None, None, None, 11, 14]
# assert get_level_order(sol.rebuild_bst_from_preorder([3, 2, 1])) == [3, 2, None, 1]
# assert sol.rebuild_bst_from_preorder([]) is None
# assert get_level_order(sol.rebuild_bst_from_preorder([7])) == [7]
# assert get_level_order(sol.rebuild_bst_from_preorder([1, 2, 3])) == [1, None, 2, None, 3]
# assert get_level_order(sol.rebuild_bst_from_preorder([2, 1, 3])) == [2, 1, 3]
# assert get_level_order(sol.rebuild_bst_from_preorder([1, 3, 2])) == [1, None, 3, 2]
# assert get_level_order(sol.rebuild_bst_from_preorder([3, 1, 2])) == [3, 1, None, None, 2]
# assert get_level_order(sol.rebuild_bst_from_preorder([10, 5, 1, 7, 40, 50])) == [10, 5, 40, 1, 7, None, 50]
# assert get_level_order(sol.rebuild_bst_from_preorder([0, -5, -10, -1, 5])) == [0, -5, 5, -10, -1]
# up = sol.rebuild_bst_from_preorder(list(range(499)))
# assert get_inorder(up) == list(range(499)) and up.left is None
# down = sol.rebuild_bst_from_preorder(list(range(498, -1, -1)))
# assert get_inorder(down) == list(range(499)) and down.right is None
# keys = [(2 * p + 1) * 2 ** (15 - d) - 1 for d in range(16) for p in range(2 ** d)]
# assert get_level_order(sol.rebuild_bst_from_preorder(preorder_of(build_tree(keys)))) == keys
