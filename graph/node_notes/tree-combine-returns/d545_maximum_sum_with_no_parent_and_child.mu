# REFERENCE: d545 Maximum Sum With No Parent And Child
class Solution
  def maxSum(root: TreeNode?) -> int
    def both(node)
      if not node
        return 0, 0
      (ls, lt), (rs, rt) = both(node.left), both(node.right)
      max(ls, lt) + max(rs, rt), node.val + ls + rs
    max(both(root))
