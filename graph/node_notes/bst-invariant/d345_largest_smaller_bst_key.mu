# REFERENCE: d345 Largest Smaller BST Key
class Solution
  def find_largest_smaller_key(rootNode: TreeNode?, num: int) -> int
    result = -1
    node = rootNode
    while node
      if node.val < num
        result = node.val
        node = node.right
      else
        node = node.left
    result
