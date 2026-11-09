# REFERENCE: d442 EPI 9.11 Reconstruct a binary tree from traversal data
class Solution
  def binary_tree_from_preorder_inorder(preorder: [int], inorder: [int]) -> TreeNode?
    where = {v: i for i, v in enumerate(inorder)}
    roots = iter(preorder)
    def build(lo, hi)
      if lo == hi
        return none
      root = TreeNode(next(roots))
      mid = where[root.val]
      root.left = build(lo, mid)
      root.right = build(mid + 1, hi)
      root
    build(0, len(inorder))
