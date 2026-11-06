# REFERENCE: d332 BST Successor Search
class Solution
  def find_in_order_successor(root: TreeNode?, inputNode: TreeNode) -> TreeNode?
    succ = none
    node = root
    while node
      if node.val > inputNode.val
        succ = node
        node = node.left
      else
        node = node.right
    succ
