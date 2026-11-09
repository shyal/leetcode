"""
EPI 9.11 Reconstruct a binary tree from traversal data

Given the preorder and the inorder lists of the node values of a binary
tree, return the root of that tree. Every value in the tree is distinct,
so the two lists fix exactly one tree. Two empty lists give None.

Example 1:

Input: preorder = [1, 2, 4, 5, 7, 8, 3, 6],
       inorder = [4, 2, 7, 5, 8, 1, 3, 6]
Output: the root of [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]

          1
         / \\
        2   3
       / \\   \\
      4   5   6
         / \\
        7   8

Example 2:

Input: preorder = [1, 2, 3], inorder = [3, 2, 1]
Output: the root of [1, 2, None, 3]
Explanation: every node is the left child of the node before it.

Example 3:

Input: preorder = [], inorder = []
Output: None

Constraints:

    0 <= len(preorder) == len(inorder) <= 10^5
    preorder and inorder hold the same distinct values.

    REQUIRED: O(n) time for n nodes. NO list slices.
"""


class Solution:
    def binary_tree_from_preorder_inorder(self, preorder: list[int], inorder: list[int]) -> TreeNode | None:
        pass


sol = Solution()

t = sol.binary_tree_from_preorder_inorder([1, 2, 4, 5, 7, 8, 3, 6], [4, 2, 7, 5, 8, 1, 3, 6])
draw_tree(t)
print(get_level_order(t))  # [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]


def preorder_of(node: TreeNode | None) -> list[int]:
    return [node.val] + preorder_of(node.left) + preorder_of(node.right) if node else []


# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2, 4, 5, 7, 8, 3, 6], [4, 2, 7, 5, 8, 1, 3, 6])) == [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2, 3], [3, 2, 1])) == [1, 2, None, 3]
# assert sol.binary_tree_from_preorder_inorder([], []) is None
# assert get_level_order(sol.binary_tree_from_preorder_inorder([7], [7])) == [7]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2, 3], [1, 2, 3])) == [1, None, 2, None, 3]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2, 3], [2, 1, 3])) == [1, 2, 3]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2], [1, 2])) == [1, None, 2]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2], [2, 1])) == [1, 2]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([1, 2, 3, 4], [2, 4, 3, 1])) == [1, 2, None, None, 3, 4]
# assert get_level_order(sol.binary_tree_from_preorder_inorder([-1, 5, 0], [5, -1, 0])) == [-1, 5, 0]
# chain = build_tree([0] + [v for k in range(1, 499) for v in (None, k)])
# assert get_inorder(sol.binary_tree_from_preorder_inorder(list(range(499)), list(range(499)))) == list(range(499))
# assert get_level_order(sol.binary_tree_from_preorder_inorder(list(range(499)), list(range(499)))) == get_level_order(chain)
# full = build_tree(list(range(2 ** 16 - 1)))
# assert get_level_order(sol.binary_tree_from_preorder_inorder(preorder_of(full), get_inorder(full))) == list(range(2 ** 16 - 1))
