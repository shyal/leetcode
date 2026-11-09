# REFERENCE: d489 EPI 14.4 Compute the LCA in a BST
class Solution
  def find_lca(tree: TreeNode, s: TreeNode, b: TreeNode) -> TreeNode
    ret node = tree
    while not s.val <= node.val <= b.val
      node = b.val < node.val ? node.left : node.right
