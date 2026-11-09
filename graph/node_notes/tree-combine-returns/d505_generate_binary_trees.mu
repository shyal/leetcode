# REFERENCE: d505 EPI 15.9 Generate binary trees
class Solution
  def generate_all_binary_trees(num_nodes: int) -> [TreeNode?]
    if num_nodes == 0
      return [none]
    ret out = []
    for left in 0..<num_nodes
      for l in self.generate_all_binary_trees(left)
        for r in self.generate_all_binary_trees(num_nodes - 1 - left)
          out <- TreeNode(0, l, r)
