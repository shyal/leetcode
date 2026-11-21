# Given the root of a binary tree, choose nodes of the tree and return the
# maximum sum of the values of the chosen nodes. You must not choose a
# node and its parent.
#
# Example 1:
#
# Input: root = the root of
#
#         3
#        / \
#       2   3
#        \   \
#         3   1
#
# Output: 7
# Explanation: the root and its two grandchildren: 3 + 3 + 1.
#
# Example 2:
#
# Input: root = the root of
#
#         3
#        / \
#       4   5
#      / \   \
#     1   3   1
#
# Output: 9
# Explanation: the two children of the root: 4 + 5.
#
# Example 3:
#
# Input: root = a single node with val 5
# Output: 5
#
# Constraints:
#
#     1 <= number of nodes <= 10^4
#     0 <= node.val <= 10^4
#
#     REQUIRED: O(number of nodes) time.
#
# ---
# learning
# mu 0.18

class Solution
  def maxSum(root: TreeNode?) -> int
    max({
      n ->
        if not n
          return 0, 0
        (ls, lt), (rs, rt) = mu(n.left), mu(n.right)
        max(ls, lt) + max(rs, rt), n.val + ls + rs
    }(root))

sol = Solution()

root = build_tree([1, 2, none, 3, none, 4, none, 5])
draw_tree(root)
print(sol.maxSum(root))  # 7

chain = reduce((t, k) -> TreeNode(1, none, t), 0..<499, TreeNode(1))
full = build_tree([1] * (2 ** 13 - 1))
assert sol.maxSum(build_tree([3, 2, 3, none, 3, none, 1])) == 7
assert sol.maxSum(build_tree([3, 4, 5, 1, 3, none, 1])) == 9
assert sol.maxSum(build_tree([5])) == 5
assert sol.maxSum(build_tree([0])) == 0
assert sol.maxSum(build_tree([1, 2])) == 2
assert sol.maxSum(build_tree([2, 1])) == 2
assert sol.maxSum(build_tree([1, none, 2])) == 2
assert sol.maxSum(build_tree([10, 1, 1])) == 10
assert sol.maxSum(build_tree([1, 10, 10])) == 20
assert sol.maxSum(build_tree([4, 1, none, 2, none, 3])) == 7
assert sol.maxSum(build_tree([1, 2, 3, 4, 5, 6, 7])) == 23
assert sol.maxSum(build_tree([7, 6, 5, 4, 3, 2, 1])) == 17
assert sol.maxSum(build_tree([5, 5, 5, 5, 5, 5, 5])) == 25
assert sol.maxSum(build_tree([2, 1, 3, none, 4, none, 7, 9, none, none, 2])) == 18
assert sol.maxSum(build_tree([9, 1, 1, 8, none, none, 8, 1, 1, 1, 1])) == 25
assert sol.maxSum(chain) == 250
assert sol.maxSum(full) == 5461
