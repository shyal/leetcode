"""
EPI 8.6 Compute binary tree nodes in order of increasing depth

Given the root tree of a binary tree, return a list with one entry per
depth, from the root down. The entry for a depth is the list of the
values at that depth, from left to right. An empty tree gives [].

Example 1:

Input: tree = the root of

          1
         / \\
        2   3
       /   / \\
      4   5   6

Output: [[1], [2, 3], [4, 5, 6]]

Example 2:

Input: tree = None
Output: []

Example 3:

Input: tree = the root of

    1
     \\
      2
     /
    3

Output: [[1], [2], [3]]

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= node value <= 10^9

    REQUIRED: O(n) time, where n is the number of nodes. NO recursion.
"""


class Solution:
    def binary_tree_depth_order(self, tree: TreeNode | None) -> list[list[int]]:
        pass


sol = Solution()


def left_chain(n):
    t = TreeNode(0)
    for k in range(1, n):
        t = TreeNode(k, t, None)
    return t


root = build_tree([1, 2, 3, 4, None, 5, 6])
draw_tree(root)
print(sol.binary_tree_depth_order(root))  # [[1], [2, 3], [4, 5, 6]]

# assert sol.binary_tree_depth_order(build_tree([1, 2, 3, 4, None, 5, 6])) == [[1], [2, 3], [4, 5, 6]]
# assert sol.binary_tree_depth_order(None) == []
# assert sol.binary_tree_depth_order(build_tree([1, None, 2, 3])) == [[1], [2], [3]]
# assert sol.binary_tree_depth_order(build_tree([7])) == [[7]]
# assert sol.binary_tree_depth_order(build_tree([1, 2])) == [[1], [2]]
# assert sol.binary_tree_depth_order(build_tree([1, None, 2])) == [[1], [2]]
# assert sol.binary_tree_depth_order(build_tree([0, -1, 1, None, None, -2, 2])) == [[0], [-1, 1], [-2, 2]]
# assert sol.binary_tree_depth_order(build_tree([1, 2, 3, None, 4, None, 5, 6, None, None, 7])) == [[1], [2, 3], [4, 5], [6, 7]]
# assert sol.binary_tree_depth_order(build_tree([5, 5, 5, 5, 5, 5, 5])) == [[5], [5, 5], [5, 5, 5, 5]]
# chain = left_chain(100000)
# assert sol.binary_tree_depth_order(chain) == [[k] for k in range(99999, -1, -1)]
# full = build_tree(list(range(2 ** 16 - 1)))
# assert sol.binary_tree_depth_order(full) == [list(range(2 ** d - 1, 2 ** (d + 1) - 1)) for d in range(16)]
