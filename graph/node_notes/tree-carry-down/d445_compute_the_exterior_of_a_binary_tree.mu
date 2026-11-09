# REFERENCE: d445 EPI 9.14 Compute the exterior of a binary tree
class Solution
  def exterior_binary_tree(tree: TreeNode?) -> [TreeNode]
    def is_leaf(node): not node.left and not node.right
    def left_side(node, edge)
      if not node
        return []
      here = edge or is_leaf(node) ? [node] : []
      here + left_side(node.left, edge) + left_side(node.right, edge and not node.left)
    def right_side(node, edge)
      if not node
        return []
      here = edge or is_leaf(node) ? [node] : []
      right_side(node.left, edge and not node.right) + right_side(node.right, edge) + here
    if not tree
      return []
    if is_leaf(tree)
      return [tree]
    [tree] + left_side(tree.left, true) + right_side(tree.right, true)
