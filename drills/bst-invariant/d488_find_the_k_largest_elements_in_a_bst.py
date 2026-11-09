"""
EPI 14.3 Find the k largest elements in a BST

Given tree, the root of a binary search tree, and an integer k, return the
k largest keys in the tree, in any order. A key that appears in several
nodes counts once for each node.

Example 1:

Input: tree = [20, 9, 25, 5, 12, None, None, None, None, 11, 14], k = 3
Output: [25, 20, 14]

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

Example 2:

Input: the same tree, k = 1
Output: [25]

Example 3:

Input: tree = [5, 3, 5], k = 2
Output: [5, 5]
Explanation: the key 5 is in two nodes.

Constraints:

    0 <= k <= number of nodes <= 10^5
    The tree satisfies the BST property: left keys <= node key <= right
    keys.

    REQUIRED: O(h + k) time for a tree of height h. NO list of all the
    keys. NO sorting.
"""


class Solution:
    def find_k_largest_in_bst(self, tree: TreeNode | None, k: int) -> list[int]:
        pass


sol = Solution()

t = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(t)
print(sol.find_k_largest_in_bst(t, 3))  # [25, 20, 14]

# assert sorted(sol.find_k_largest_in_bst(t, 3)) == [14, 20, 25]
# assert sorted(sol.find_k_largest_in_bst(t, 1)) == [25]
# assert sorted(sol.find_k_largest_in_bst(t, 7)) == [5, 9, 11, 12, 14, 20, 25]
# assert sorted(sol.find_k_largest_in_bst(t, 6)) == [9, 11, 12, 14, 20, 25]
# assert sorted(sol.find_k_largest_in_bst(t, 4)) == [12, 14, 20, 25]
# assert sol.find_k_largest_in_bst(t, 0) == []
# assert sol.find_k_largest_in_bst(None, 0) == []
# assert sorted(sol.find_k_largest_in_bst(build_tree([5, 3, 5]), 2)) == [5, 5]
# assert sorted(sol.find_k_largest_in_bst(build_tree([5, 3, 5]), 3)) == [3, 5, 5]
# assert sol.find_k_largest_in_bst(build_tree([1]), 1) == [1]
# assert sorted(sol.find_k_largest_in_bst(build_tree([2, 1]), 1)) == [2]
# assert sorted(sol.find_k_largest_in_bst(build_tree([1, None, 2]), 1)) == [2]
# left = build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)])
# assert sorted(sol.find_k_largest_in_bst(left, 3)) == [496, 497, 498]
# keys = [(2 * p + 1) * 2 ** (15 - d) - 1 for d in range(16) for p in range(2 ** d)]
# big = build_tree(keys)
# assert sorted(sol.find_k_largest_in_bst(big, 5)) == [65530, 65531, 65532, 65533, 65534]
# assert sorted(sol.find_k_largest_in_bst(big, 1000)) == list(range(2 ** 16 - 1001, 2 ** 16 - 1))
