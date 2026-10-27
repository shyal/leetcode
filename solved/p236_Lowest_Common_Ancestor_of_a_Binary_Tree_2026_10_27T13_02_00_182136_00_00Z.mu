# URL: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 236. Lowest Common Ancestor of a Binary Tree
#
# Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
#
# According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”
#
# Example 1:
#
# Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
# Output: 3
# Explanation: The LCA of nodes 5 and 1 is 3.
#
# Example 2:
#
# Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
# Output: 5
# Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.
#
# Example 3:
#
# Input: root = [1,2], p = 1, q = 2
# Output: 1
#
# Constraints:
#
#     The number of nodes in the tree is in the range [2, 10^5].
#     -10^9 <= Node.val <= 10^9
#     All Node.val are unique.
#     p != q
#     p and q will exist in the tree.
#
# ---
# LEETCODE: Accepted (154 ms, 50 MB)

# mu 0.13

class Solution
  def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode
    self.lca = None
    {
      (n) ->
        if n is None or self.lca
          return None
        left = mu(n.left)
        right = mu(n.right)
        if (left and right) or ((left or right) and (n is p or n is q))
          self.lca = n
          return True
        if n is p or n is q
          return True
        if left or right
          return True
    }(root)
    return self.lca

sol = Solution()

root1 = build_tree([3, 5, 1, 6, 2, 0, 8, none, none, 7, 4])
print(root1)
p1 = find_node(root1, 5)
q1 = find_node(root1, 1)
print(sol.lowestCommonAncestor(root1, p1, q1).val)  # 3

root2 = build_tree([3, 5, 1, 6, 2, 0, 8, none, none, 7, 4])
p2 = find_node(root2, 5)
q2 = find_node(root2, 4)
assert sol.lowestCommonAncestor(root2, p2, q2).val == 5

root3 = build_tree([1, 2])
p3 = find_node(root3, 1)
q3 = find_node(root3, 2)
assert sol.lowestCommonAncestor(root3, p3, q3).val == 1
