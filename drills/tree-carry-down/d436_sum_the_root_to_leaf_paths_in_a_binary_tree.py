"""
EPI 9.5 Sum the root-to-leaf paths in a binary tree

Given tree, the root of a binary tree whose node values are binary digits,
return the sum of the numbers that the root-to-leaf paths encode. A path
from the root down to a leaf, read from the root, gives the bits of a
binary number: the root holds the most significant bit. An empty tree
gives 0.

Example 1:

Input: tree = [1, 0, 1, 0, 1, None, 1]
Output: 16
Explanation: the paths read 100, 101 and 111, which are 4, 5 and 7.

        1
       / \\
      0   1
     / \\   \\
    0   1   1

Example 2:

Input: tree = [0, 1, None, 1, 0]
Output: 5
Explanation: the paths read 011 and 010, which are 3 and 2.

Example 3:

Input: tree = [1]
Output: 1

Constraints:

    0 <= number of nodes <= 10^4
    node.val is 0 or 1.

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h. NO strings. NO list of the paths.
"""


class Solution:
    def sum_root_to_leaf(self, tree: TreeNode | None) -> int:
        pass


sol = Solution()

t = build_tree([1, 0, 1, 0, 1, None, 1])
draw_tree(t)
print(sol.sum_root_to_leaf(t))  # 16

# assert sol.sum_root_to_leaf(t) == 16
# assert sol.sum_root_to_leaf(build_tree([0, 1, None, 1, 0])) == 5
# assert sol.sum_root_to_leaf(build_tree([1])) == 1
# assert sol.sum_root_to_leaf(build_tree([0])) == 0
# assert sol.sum_root_to_leaf(None) == 0
# assert sol.sum_root_to_leaf(build_tree([1, 1])) == 3
# assert sol.sum_root_to_leaf(build_tree([1, None, 0])) == 2
# assert sol.sum_root_to_leaf(build_tree([1, 0, 1])) == 5
# assert sol.sum_root_to_leaf(build_tree([0, 0, 0, 0, 0, 0, 0])) == 0
# assert sol.sum_root_to_leaf(build_tree([1, 0, 1, 0, 1, 0, 1])) == 4 + 5 + 6 + 7
# assert sol.sum_root_to_leaf(build_tree([1, 0, 1, None, 1, None, None, 1, 0])) == 11 + 10 + 3
# chain = build_tree([1] + [v for k in range(498) for v in (1, None)])
# assert sol.sum_root_to_leaf(chain) == 2 ** 499 - 1
# assert sol.sum_root_to_leaf(build_tree([1] * (2 ** 13 - 1))) == 2 ** 12 * (2 ** 13 - 1)
# assert sol.sum_root_to_leaf(build_tree([1] + [0] * (2 ** 13 - 2))) == 2 ** 12 * 2 ** 12
