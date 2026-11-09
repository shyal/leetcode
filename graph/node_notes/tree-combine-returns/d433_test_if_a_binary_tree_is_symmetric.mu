# REFERENCE: d433 EPI 9.2 Test if a binary tree is symmetric
class Solution
  def is_symmetric(tree: TreeNode?) -> bool
    def mirror(a, b)
      if not a or not b
        return a is b
      a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    not tree or mirror(tree.left, tree.right)
