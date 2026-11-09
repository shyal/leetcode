# REFERENCE: d443 EPI 9.12 Reconstruct a binary tree from a preorder traversal with markers
class Solution
  def reconstruct_preorder(preorder: [int?]) -> TreeNode?
    values = iter(preorder)
    def build()
      val = next(values)
      if val is none
        return none
      left = build()
      TreeNode(val, left, build())
    build()
