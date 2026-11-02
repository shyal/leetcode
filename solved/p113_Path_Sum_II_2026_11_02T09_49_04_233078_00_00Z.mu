# URL: https://leetcode.com/problems/path-sum-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 113. Path Sum II
#
# Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references.
#
# A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.
#
# Example 1:
#
# Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
# Output: [[5,4,11,2],[5,8,4,5]]
# Explanation: There are two paths whose sum equals targetSum:
# 5 + 4 + 11 + 2 = 22
# 5 + 8 + 4 + 5 = 22
#
# Example 2:
#
# Input: root = [1,2,3], targetSum = 5
# Output: []
#
# Example 3:
#
# Input: root = [1,2], targetSum = 0
# Output: []
#
# Constraints:
#
#     The number of nodes in the tree is in the range [0, 5000].
#     -1000 <= Node.val <= 1000
#     -1000 <= targetSum <= 1000
#
# ---
# LEETCODE: Accepted (2 ms, 20.1 MB)

# mu 0.16

class Solution
  def pathSum(root: TreeNode?, targetSum: int) -> [[int]]
    ret res = []
    path = []
    {
      (n, total) ->
        if n is None
          return
        path <- n.val 
        total += n.val
        if n.left is None and n.right is None
          if total == targetSum
            res <- path[:]
        mu(n.left, total)
        mu(n.right, total)
        path .
    }(root, 0)

sol = Solution()

root1 = build_tree([5, 4, 8, 11, none, 13, 4, 7, 2, none, none, 5, 1])
print(root1)
print(sol.pathSum(root1, 22))  # [[5,4,11,2],[5,8,4,5]]

assert sol.pathSum(build_tree([5, 4, 8, 11, none, 13, 4, 7, 2, none, none, 5, 1]), 22) == [[5, 4, 11, 2], [5, 8, 4, 5]]
assert sol.pathSum(build_tree([1, 2, 3]), 5) == []
assert sol.pathSum(build_tree([1, 2]), 0) == []
assert sol.pathSum(build_tree([]), 0) == []
assert sol.pathSum(build_tree([1]), 1) == [[1]]
assert sol.pathSum(build_tree([1]), 2) == []
assert sol.pathSum(build_tree([1, -2, -3, 1, 3, -2, none, -1]), -1) == [[1, -2, 1, -1]]
assert sol.pathSum(build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 15) == [[1, 2, 4, 8]]
assert sol.pathSum(build_tree([0, 1, 1]), 1) == [[0, 1], [0, 1]]
assert sol.pathSum(build_tree([1, 2, 2, 3, 3, 3, 3]), 6) == [[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]
assert sol.pathSum(build_tree([1000, 1000, 1000, 1000, none, none, 1000]), 4000) == []
assert sol.pathSum(build_tree([-1000, -1000, -1000, -1000, none, none, -1000]), -3000) == [[-1000, -1000, -1000], [-1000, -1000, -1000]]
assert sol.pathSum(build_tree([1] * 5000), 3) == []
assert sol.pathSum(build_tree([1, none, 2, none, 3, none, 4, none, 5]), 15) == [[1, 2, 3, 4, 5]]
assert sol.pathSum(build_tree([1, 2, none, 3, none, 4, none, 5]), 10) == []
