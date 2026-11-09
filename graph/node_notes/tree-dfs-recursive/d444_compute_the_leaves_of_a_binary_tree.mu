# REFERENCE: d444 EPI 9.13 Compute the leaves of a binary tree
class Solution
  def create_list_of_leaves(tree: TreeNode?) -> [TreeNode]
    if not tree
      return []
    if not tree.left and not tree.right
      return [tree]
    self.create_list_of_leaves(tree.left) + self.create_list_of_leaves(tree.right)
