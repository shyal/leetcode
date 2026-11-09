# REFERENCE: d437 EPI 9.6 Find a root to leaf path with specified sum
class Solution
  def has_path_sum(tree: TreeNode?, remaining_weight: int) -> bool
    if not tree
      return false
    remaining_weight -= tree.val
    if not tree.left and not tree.right
      return remaining_weight == 0
    self.has_path_sum(tree.left, remaining_weight) or self.has_path_sum(tree.right, remaining_weight)
