# REFERENCE: d432 EPI 9.1 Test if a binary tree is height-balanced
class Solution
  def is_balanced_binary_tree(tree: TreeNode?) -> bool
    def height(node)
      if not node
        return 0
      left, right = height(node.left), height(node.right)
      if left < 0 or right < 0 or abs(left - right) > 1
        return -1
      1 + max(left, right)
    height(tree) >= 0
