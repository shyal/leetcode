# REFERENCE: d436 EPI 9.5 Sum the root-to-leaf paths in a binary tree
class Solution
  def sum_root_to_leaf(tree: TreeNode?) -> int
    def total(node, prefix)
      if not node
        return 0
      prefix = 2 * prefix + node.val
      if not node.left and not node.right
        return prefix
      total(node.left, prefix) + total(node.right, prefix)
    total(tree, 0)
