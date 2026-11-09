# REFERENCE: d440 EPI 9.9 Compute the successor
class Solution
  def find_successor(node: TreeNode) -> TreeNode?
    if node.right
      node = node.right
      while node.left
        node = node.left
      return node
    while node.parent and node.parent.right is node
      node = node.parent
    node.parent
