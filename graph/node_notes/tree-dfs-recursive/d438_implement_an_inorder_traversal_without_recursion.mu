# REFERENCE: d438 EPI 9.7 Implement an inorder traversal without recursion
class Solution
  def inorder_traversal(tree: TreeNode?) -> [int]
    ret out = []
    stack, node = [], tree
    while stack or node
      if node
        stack <- node
        node = node.left
      else
        node = stack .
        out <- node.val
        node = node.right
