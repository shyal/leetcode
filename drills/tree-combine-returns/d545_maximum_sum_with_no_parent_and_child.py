"""
Given the root of a binary tree, choose nodes of the tree and return the
maximum sum of the values of the chosen nodes. You must not choose a
node and its parent.

Example 1:

Input: root = the root of

        3
       / \\
      2   3
       \\   \\
        3   1

Output: 7
Explanation: the root and its two grandchildren: 3 + 3 + 1.

Example 2:

Input: root = the root of

        3
       / \\
      4   5
     / \\   \\
    1   3   1

Output: 9
Explanation: the two children of the root: 4 + 5.

Example 3:

Input: root = a single node with val 5
Output: 5

Constraints:

    1 <= number of nodes <= 10^4
    0 <= node.val <= 10^4

    REQUIRED: O(number of nodes) time.
"""


class Solution:
    def maxSum(self, root: TreeNode | None) -> int:
        pass


sol = Solution()

root = build_tree([3, 2, 3, None, 3, None, 1])
draw_tree(root)
print(sol.maxSum(root))  # 7

# chain = reduce(lambda t, k: TreeNode(1, None, t), range(499), TreeNode(1))
# full = build_tree([1] * (2 ** 13 - 1))
# assert sol.maxSum(build_tree([3, 2, 3, None, 3, None, 1])) == 7
# assert sol.maxSum(build_tree([3, 4, 5, 1, 3, None, 1])) == 9
# assert sol.maxSum(build_tree([5])) == 5
# assert sol.maxSum(build_tree([0])) == 0
# assert sol.maxSum(build_tree([1, 2])) == 2
# assert sol.maxSum(build_tree([2, 1])) == 2
# assert sol.maxSum(build_tree([1, None, 2])) == 2
# assert sol.maxSum(build_tree([10, 1, 1])) == 10
# assert sol.maxSum(build_tree([1, 10, 10])) == 20
# assert sol.maxSum(build_tree([4, 1, None, 2, None, 3])) == 7
# assert sol.maxSum(build_tree([1, 2, 3, 4, 5, 6, 7])) == 23
# assert sol.maxSum(build_tree([7, 6, 5, 4, 3, 2, 1])) == 17
# assert sol.maxSum(build_tree([5, 5, 5, 5, 5, 5, 5])) == 25
# assert sol.maxSum(build_tree([2, 1, 3, None, 4, None, 7, 9, None, None, 2])) == 18
# assert sol.maxSum(build_tree([9, 1, 1, 8, None, None, 8, 1, 1, 1, 1])) == 25
# assert sol.maxSum(chain) == 250
# assert sol.maxSum(full) == 5461
