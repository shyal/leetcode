"""
EPI 14.10 The range lookup problem

Given tree, the root of a binary search tree, and a pair interval =
(left, right), return the keys k of the tree with left <= k <= right,
in ascending order.

Example 1:

Input: tree = [20, 9, 25, 5, 12, None, None, None, None, 11, 14],
       interval = (10, 21)
Output: [11, 12, 14, 20]

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

Example 2:

Input: the same tree, interval = (0, 4)
Output: []

Example 3:

Input: the same tree, interval = (25, 25)
Output: [25]
Explanation: both ends of the interval are included.

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= left <= right <= 10^9
    The tree satisfies the BST property, and every key is distinct.

    REQUIRED: O(m + h) time for a tree of height h, where m is the
    number of keys returned. NO list of all the keys. NO sorting.
"""


class Solution:
    def range_lookup_in_bst(self, tree: TreeNode | None, interval: tuple[int, int]) -> list[int]:
        pass


sol = Solution()

t = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(t)
print(sol.range_lookup_in_bst(t, (10, 21)))  # [11, 12, 14, 20]

# assert sol.range_lookup_in_bst(t, (10, 21)) == [11, 12, 14, 20]
# assert sol.range_lookup_in_bst(t, (0, 4)) == []
# assert sol.range_lookup_in_bst(t, (25, 25)) == [25]
# assert sol.range_lookup_in_bst(t, (5, 25)) == [5, 9, 11, 12, 14, 20, 25]
# assert sol.range_lookup_in_bst(t, (-10 ** 9, 10 ** 9)) == [5, 9, 11, 12, 14, 20, 25]
# assert sol.range_lookup_in_bst(t, (5, 5)) == [5]
# assert sol.range_lookup_in_bst(t, (13, 13)) == []
# assert sol.range_lookup_in_bst(t, (12, 19)) == [12, 14]
# assert sol.range_lookup_in_bst(t, (26, 100)) == []
# assert sol.range_lookup_in_bst(None, (0, 10)) == []
# assert sol.range_lookup_in_bst(build_tree([3]), (3, 3)) == [3]
# assert sol.range_lookup_in_bst(build_tree([3]), (4, 9)) == []
# chain = build_tree([0] + [v for k in range(1, 499) for v in (None, k)])
# assert sol.range_lookup_in_bst(chain, (100, 120)) == list(range(100, 121))
# keys = [(2 * p + 1) * 2 ** (15 - d) - 1 for d in range(16) for p in range(2 ** d)]
# big = build_tree(keys)
# assert sol.range_lookup_in_bst(big, (1000, 1010)) == list(range(1000, 1011))
# assert sol.range_lookup_in_bst(big, (-5, 2)) == [0, 1, 2]
# assert sol.range_lookup_in_bst(big, (0, 2 ** 16)) == list(range(2 ** 16 - 1))
