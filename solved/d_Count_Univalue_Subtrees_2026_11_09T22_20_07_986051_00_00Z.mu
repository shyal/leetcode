# Given the root of a binary tree, return the number of univalue subtrees.
# A subtree is a node together with all of its descendants. A subtree is
# univalue when every node in it holds the same value.
#
# Example 1:
#
# Input: root = [5, 1, 5, 5, 5, None, 5]
# Output: 4
# Explanation: the three leaf 5s, plus the right child of the root: it
# holds 5 and its only descendant holds 5.
#
# Example 2:
#
# Input: root = [7]
# Output: 1
# Explanation: a leaf is a univalue subtree.
#
# Example 3:
#
# Input: root = [1, 1, 2]
# Output: 2
# Explanation: both leaves qualify. The whole tree holds two values, so
# it does not.
#
# Constraints:
#
#     1 <= number of nodes <= 1000
#     -100 <= Node.val <= 100
#
#     REQUIRED: one pass, O(n). NO tuple returns bundling the count, NO
#     second traversal.
#
# ---

# mu 0.17

class Solution
  def countUnivalSubtrees(root: TreeNode?) -> int
    self.count = 0
    {
      n ->
        is_leaf = n.left is n.right is None
        if is_leaf
          r = (n.val, true)
          n.val = true
          self.count += 1
          return r
        is_unival = true
        if n.left
          left_val, is_left_uni = mu(n.left)
          is_unival = is_unival and is_left_uni and n.val == left_val
        if n.right
          right_val, is_right_uni = mu(n.right)
          is_unival = is_unival and is_right_uni and n.val == right_val
        r =  n.val, is_unival
        self.count += is_unival
        n.val = is_unival
        r
    }(root)
    self.count

sol = Solution()

tree = build_tree([5, 1, 5, 5, 5, none, 5])

print(sol.countUnivalSubtrees(tree))  # 4
print(tree)

assert sol.countUnivalSubtrees(build_tree([5, 1, 5, 5, 5, none, 5])) == 4
assert sol.countUnivalSubtrees(build_tree([7])) == 1
assert sol.countUnivalSubtrees(build_tree([1, 1, 2])) == 2
assert sol.countUnivalSubtrees(build_tree([2, 2, 2])) == 3
assert sol.countUnivalSubtrees(build_tree([5, 5, 5, 5, 5, none, 5])) == 6
assert sol.countUnivalSubtrees(build_tree([1, 1, 1, 1, 1, 1, 1])) == 7
assert sol.countUnivalSubtrees(build_tree([1, none, 1, none, 1])) == 3
assert sol.countUnivalSubtrees(build_tree([5, 5, 5, 5, 5, 5, 9])) == 5
assert sol.countUnivalSubtrees(build_tree([1, 2, 3])) == 2
