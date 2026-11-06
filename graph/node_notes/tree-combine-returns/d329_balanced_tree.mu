# REFERENCE: d329 Balanced Tree
class Solution
  def is_balanced(node: TreeNode?) -> bool
    def height(n)
      if not n
        return 0
      left, right = height(n.left), height(n.right)
      if left == -1 or right == -1 or abs(left - right) > 1
        return -1
      1 + max(left, right)
    height(node) != -1
