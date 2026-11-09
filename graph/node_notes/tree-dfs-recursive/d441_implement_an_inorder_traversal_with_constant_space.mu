# REFERENCE: d441 EPI 9.10 Implement an inorder traversal with constant space
class Solution
  def inorder_traversal(tree: TreeNode?) -> [int]
    ret out = []
    prev, node = none, tree
    while node
      if prev is node.parent and node.left
        prev, node = node, node.left
      elif prev is node.parent or prev is node.left
        out <- node.val
        prev, node = node, node.right or node.parent
      else
        prev, node = node, node.parent
