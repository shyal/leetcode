# REFERENCE: d486 EPI 14.1 Test if a binary tree satisfies the BST property
class Solution
  def is_binary_tree_bst(tree: TreeNode?) -> bool
    def within(node, low, high)
      if not node
        return true
      low <= node.val <= high and within(node.left, low, node.val) and within(node.right, node.val, high)
    within(tree, -inf, inf)
