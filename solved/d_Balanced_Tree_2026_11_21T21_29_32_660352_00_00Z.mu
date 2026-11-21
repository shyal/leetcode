# Given the root node of a binary tree, return True when the tree is
# balanced and False otherwise. A tree is balanced when, at every node,
# the heights of the left subtree and the right subtree differ by at most
# one. An empty tree is balanced.
#
# Example 1:
#
# Input: node = the root of
#
#           a
#          / \
#         b   c
#        /     \
#       d       e
#      /         \
#     f           g
#
# Output: False
# Explanation: the tree is symmetric, but at node b the left subtree has
# height 2 and the right subtree has height 0.
#
# Example 2:
#
# Input: node = the root of
#
#           a
#          / \
#         b   c
#        / \   \
#       d   e   f
#
# Output: True
#
# Example 3:
#
# Input: node = the root of
#
#       a
#      / \
#     b   c
#          \
#           d
#            \
#             e
#
# Output: False
# Explanation: at node c the right subtree has height 2 and the left has
# height 0.
#
# Constraints:
#
#     0 <= number of nodes <= 10^4
#     Node values are single lowercase letters.
#
#     REQUIRED: O(n) time, where n is the number of nodes. NO recomputing
#     the height of a subtree.
#
# ---

# mu 0.18

class Solution
  def is_balanced(node: TreeNode?) -> bool
    self.is_bal = true
    {
      (n) -> 
        if not n
          return 0
        lh, rh = 0
        if n.left
          lh = mu(n.left) + 1
        if n.right
          rh = mu(n.right) + 1
        if abs(lh - rh) > 1
          self.is_bal = false
        h = max(lh, rh)
        n.val = h
        h
    }(node)
    self.is_bal

sol = Solution()

root = build_tree(['a', 'b', 'c', 'd', none, none, 'e', 'f', none, none, 'g'])
print(sol.is_balanced(root))  # False
draw_tree(root)

assert sol.is_balanced(build_tree(['a', 'b', 'c', 'd', none, none, 'e', 'f', none, none, 'g'])) is false
assert sol.is_balanced(build_tree(['a', 'b', 'c', 'd', 'e', none, 'f'])) is true
assert sol.is_balanced(build_tree(['a', 'b', 'c', none, none, none, 'd', none, 'e'])) is false
assert sol.is_balanced(build_tree(['a', 'b', 'c', none, none, none, 'd'])) is true
assert sol.is_balanced(build_tree(['a'])) is true
assert sol.is_balanced(none) is true
assert sol.is_balanced(build_tree(['a', 'b'])) is true
assert sol.is_balanced(build_tree(['a', 'b', none, 'c'])) is false
assert sol.is_balanced(build_tree(['a', 'b', 'c', 'd', 'e', 'f', 'g'])) is true
assert sol.is_balanced(build_tree(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', none, none, none, none, none, none, none, 'i'])) is false
chain = reduce((t, k) -> TreeNode('b', none, t), 0..<499, TreeNode('a'))
assert sol.is_balanced(chain) is false
fork = TreeNode('a', chain, TreeNode('c'))
assert sol.is_balanced(fork) is false
full = build_tree(['a'] * (2 ** 13 - 1))
assert sol.is_balanced(full) is true
