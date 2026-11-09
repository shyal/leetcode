# REFERENCE: d435 EPI 9.4 Compute the LCA when nodes have parent pointers
class Solution
  def lca(node0: TreeNode, node1: TreeNode) -> TreeNode
    def depth(node)
      ret d = 0
      while node.parent
        node, d = node.parent, d + 1
    d0, d1 = depth(node0), depth(node1)
    if d0 < d1
      node0, node1, d0, d1 = node1, node0, d1, d0
    for _ in 0..<d0 - d1
      node0 = node0.parent
    while node0 is not node1
      node0, node1 = node0.parent, node1.parent
    node0
