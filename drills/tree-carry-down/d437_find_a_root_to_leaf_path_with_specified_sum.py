"""
EPI 9.6 Find a root to leaf path with specified sum

Given tree, the root of a binary tree with integer node weights, and an
integer remaining_weight, return True when some path from the root down
to a leaf has weights that add up to remaining_weight, and False
otherwise. An empty tree has no path.

Example 1:

Input: tree = [3, 9, 2, 1, 6, None, 7, None, None, None, 5],
       remaining_weight = 23
Output: True
Explanation: the path 3, 9, 6, 5 adds up to 23.

        3
       / \\
      9   2
     / \\   \\
    1   6   7
         \\
          5

Example 2:

Input: the same tree, remaining_weight = 18
Output: False
Explanation: 3, 9, 6 adds up to 18, but 6 is not a leaf.

Example 3:

Input: tree = [], remaining_weight = 0
Output: False

Constraints:

    0 <= number of nodes <= 10^4
    -1000 <= node.val <= 1000
    -10^7 <= remaining_weight <= 10^7

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h. NO list of the path sums.
"""


class Solution:
    def has_path_sum(self, tree: TreeNode | None, remaining_weight: int) -> bool:
        pass


sol = Solution()

t = build_tree([3, 9, 2, 1, 6, None, 7, None, None, None, 5])
draw_tree(t)
print(sol.has_path_sum(t, 23))  # True

# assert sol.has_path_sum(t, 23) is True
# assert sol.has_path_sum(t, 18) is False
# assert sol.has_path_sum(t, 13) is True
# assert sol.has_path_sum(t, 12) is True
# assert sol.has_path_sum(t, 3) is False
# assert sol.has_path_sum(t, 5) is False
# assert sol.has_path_sum(None, 0) is False
# assert sol.has_path_sum(build_tree([4]), 4) is True
# assert sol.has_path_sum(build_tree([4]), 0) is False
# assert sol.has_path_sum(build_tree([1, 2]), 1) is False
# assert sol.has_path_sum(build_tree([1, 2]), 3) is True
# assert sol.has_path_sum(build_tree([0, -3, 3, 3, None, None, -3]), 0) is True
# assert sol.has_path_sum(build_tree([-2, None, -3]), -5) is True
# chain = build_tree([0] + [v for k in range(1, 500) for v in (None, k)])
# assert sol.has_path_sum(chain, 500 * 499 // 2) is True
# assert sol.has_path_sum(chain, 499 * 498 // 2) is False
# full = build_tree([1] * (2 ** 13 - 1))
# assert sol.has_path_sum(full, 13) is True
# assert sol.has_path_sum(full, 12) is False
# assert sol.has_path_sum(build_tree([1] * (2 ** 13 - 2) + [2]), 14) is True
