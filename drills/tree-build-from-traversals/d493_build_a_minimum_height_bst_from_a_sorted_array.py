"""
EPI 14.8 Build a minimum height BST from a sorted array

Given a sorted array A of distinct integers, return the root of a binary
search tree that holds exactly the entries of A and has the smallest
possible height. When several trees have that height, return any of
them. An empty array gives None.

Example 1:

Input: A = [2, 3, 5, 7, 11, 13, 17]
Output: the root of [7, 3, 13, 2, 5, 11, 17]
Explanation: 7 nodes fit in 3 levels, and no tree with 7 nodes has
fewer levels.

          7
        /   \\
       3     13
      / \\   /  \\
     2   5 11   17

Example 2:

Input: A = [1, 2]
Output: the root of [1, None, 2] or of [2, 1]

Example 3:

Input: A = []
Output: None

Constraints:

    0 <= len(A) <= 10^5
    A is in strictly increasing order.

    REQUIRED: O(n) time for n entries. NO list slices.
"""


class Solution:
    def build_min_height_bst_from_sorted_array(self, A: list[int]) -> TreeNode | None:
        pass


sol = Solution()

t = sol.build_min_height_bst_from_sorted_array([2, 3, 5, 7, 11, 13, 17])
draw_tree(t)
print(get_level_order(t))  # [7, 3, 13, 2, 5, 11, 17]


def height(node: TreeNode | None) -> int:
    return 1 + max(height(node.left), height(node.right)) if node else 0


# t = sol.build_min_height_bst_from_sorted_array([2, 3, 5, 7, 11, 13, 17])
# assert get_level_order(t) == [7, 3, 13, 2, 5, 11, 17]
# t = sol.build_min_height_bst_from_sorted_array([1, 2])
# assert get_level_order(t) in ([1, None, 2], [2, 1])
# assert sol.build_min_height_bst_from_sorted_array([]) is None
# assert get_level_order(sol.build_min_height_bst_from_sorted_array([4])) == [4]
# t = sol.build_min_height_bst_from_sorted_array([1, 2, 3])
# assert get_level_order(t) == [2, 1, 3]
# t = sol.build_min_height_bst_from_sorted_array([1, 2, 3, 4])
# assert get_inorder(t) == [1, 2, 3, 4] and height(t) == 3
# t = sol.build_min_height_bst_from_sorted_array([-5, -1, 0, 8, 9])
# assert get_inorder(t) == [-5, -1, 0, 8, 9] and height(t) == 3
# A = list(range(8))
# t = sol.build_min_height_bst_from_sorted_array(A)
# assert get_inorder(t) == A and height(t) == 4
# A = list(range(2 ** 15 - 1))
# t = sol.build_min_height_bst_from_sorted_array(A)
# assert get_inorder(t) == A and height(t) == 15
# A = list(range(0, 3 * 10 ** 5, 3))
# t = sol.build_min_height_bst_from_sorted_array(A)
# assert get_inorder(t) == A and height(t) == (10 ** 5).bit_length()
