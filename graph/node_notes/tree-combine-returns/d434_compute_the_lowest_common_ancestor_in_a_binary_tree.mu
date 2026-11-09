# REFERENCE: d434 EPI 9.3 Compute the lowest common ancestor in a binary tree
class Solution
  def lca(tree: TreeNode, node0: TreeNode, node1: TreeNode) -> TreeNode
    def search(node)
      if not node or node is node0 or node is node1
        return node
      left, right = search(node.left), search(node.right)
      left and right ? node : left or right
    search(tree)
