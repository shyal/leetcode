# REFERENCE: d495 EPI 14.10 The range lookup problem
class Solution
  def range_lookup_in_bst(tree: TreeNode?, interval: (int, int)) -> [int]
    left, right = interval
    ret out = []
    def walk(node)
      if not node
        return
      if left < node.val
        walk(node.left)
      if left <= node.val <= right
        out <- node.val
      if node.val < right
        walk(node.right)
    walk(tree)
