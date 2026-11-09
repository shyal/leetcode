# REFERENCE: d490 EPI 14.5 Reconstruct a BST from traversal data
class Solution
  def rebuild_bst_from_preorder(preorder_sequence: [int]) -> TreeNode?
    i = 0
    def build(low, high)
      nonlocal i
      if i == len(preorder_sequence) or not low < preorder_sequence[i] < high
        return none
      root = TreeNode(preorder_sequence[i])
      i += 1
      root.left = build(low, root.val)
      root.right = build(root.val, high)
      root
    build(-inf, inf)
