# REFERENCE: d488 EPI 14.3 Find the k largest elements in a BST
class Solution
  def find_k_largest_in_bst(tree: TreeNode?, k: int) -> [int]
    ret out = []
    def walk(node)
      if node and len(out) < k
        walk(node.right)
        if len(out) < k
          out <- node.val
          walk(node.left)
    walk(tree)
