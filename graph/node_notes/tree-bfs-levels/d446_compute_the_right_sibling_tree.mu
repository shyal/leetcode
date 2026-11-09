# REFERENCE: d446 EPI 9.15 Compute the right sibling tree
class Solution
  def construct_right_sibling(tree: TreeNode?) -> none
    if tree
      tree.next = none
    level = tree
    while level and level.left
      node = level
      while node
        node.left.next = node.right
        node.right.next = node.next ? node.next.left : none
        node = node.next
      level = level.left
