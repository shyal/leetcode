# REFERENCE: d68 Count Univalue Subtrees
def countUnivalSubtrees(root: TreeNode?) -> int
  def uni(node)
    if not node
      return true
    left, right = uni(node.left), uni(node.right)
    if not left or not right
      return false
    if node.left and node.left.val != node.val
      return false
    if node.right and node.right.val != node.val
      return false
    count += 1
    true

  count = 0
  uni(root)
  count
