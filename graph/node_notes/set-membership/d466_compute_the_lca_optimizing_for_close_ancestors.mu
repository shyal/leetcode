# REFERENCE: d466 EPI 12.4 Compute the LCA, optimizing for close ancestors
class Solution
  def lca(node0: TreeNode, node1: TreeNode) -> TreeNode
    seen = set()
    while node0 not in seen
      if node0
        seen.add(node0)
        node0 = node0.parent
      node0, node1 = node1, node0
    node0
