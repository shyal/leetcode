"""
EPI 9.12 Reconstruct a binary tree from a preorder traversal with markers

Given the preorder list of a binary tree with markers, return the root of
that tree. In this list each node gives its value, and each empty child
gives None. So a leaf v gives v, None, None, and an empty tree gives
[None].

Example 1:

Input: preorder = [1, 2, 4, None, None, 5, 7, None, None, 8, None, None,
                   3, None, 6, None, None]
Output: the root of [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]

          1
         / \\
        2   3
       / \\   \\
      4   5   6
         / \\
        7   8

Example 2:

Input: preorder = [1, None, 2, None, None]
Output: the root of [1, None, 2]

Example 3:

Input: preorder = [None]
Output: None

Constraints:

    1 <= len(preorder) <= 2 * 10^5 + 1
    preorder is the preorder list with markers of a binary tree.
    Node values are not None.

    REQUIRED: O(n) time for a list of length n. NO list slices. NO
    list.pop(0).
"""


class Solution:
    def reconstruct_preorder(self, preorder: list[int | None]) -> TreeNode | None:
        pass


sol = Solution()

t = sol.reconstruct_preorder([1, 2, 4, None, None, 5, 7, None, None, 8, None, None, 3, None, 6, None, None])
draw_tree(t)
print(get_level_order(t))  # [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]


def with_markers(node: TreeNode | None) -> list[int | None]:
    return [node.val] + with_markers(node.left) + with_markers(node.right) if node else [None]


# assert get_level_order(t) == [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]
# assert get_level_order(sol.reconstruct_preorder([1, None, 2, None, None])) == [1, None, 2]
# assert sol.reconstruct_preorder([None]) is None
# assert get_level_order(sol.reconstruct_preorder([5, None, None])) == [5]
# assert get_level_order(sol.reconstruct_preorder([1, 2, None, None, None])) == [1, 2]
# assert get_level_order(sol.reconstruct_preorder([1, 2, None, None, 3, None, None])) == [1, 2, 3]
# assert get_level_order(sol.reconstruct_preorder([1, 2, 3, None, None, None, None])) == [1, 2, None, 3]
# assert get_level_order(sol.reconstruct_preorder([1, 2, None, 3, 4, None, None, None, None])) == [1, 2, None, None, 3, 4]
# assert get_level_order(sol.reconstruct_preorder([0, 0, None, None, 0, None, None])) == [0, 0, 0]
# assert get_level_order(sol.reconstruct_preorder([-3, None, -3, -3, None, None, None])) == [-3, None, -3, -3]
# left = sol.reconstruct_preorder(list(range(498, -1, -1)) + [None] * 500)
# assert get_inorder(left) == list(range(499))
# assert left.right is None and left.left.val == 497
# full = build_tree(list(range(2 ** 16 - 1)))
# assert get_level_order(sol.reconstruct_preorder(with_markers(full))) == list(range(2 ** 16 - 1))
