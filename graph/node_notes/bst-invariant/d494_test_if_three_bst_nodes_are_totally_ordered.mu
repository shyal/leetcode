# REFERENCE: d494 EPI 14.9 Test if three BST nodes are totally ordered
class Solution
  def pair_includes_ancestor_and_descendant_of_m(possible_anc_or_desc_0: TreeNode, possible_anc_or_desc_1: TreeNode, middle: TreeNode) -> bool
    a, b = possible_anc_or_desc_0, possible_anc_or_desc_1
    def step(node, target): target.val < node.val ? node.left : node.right
    def reaches(node, target)
      while node and node is not target
        node = step(node, target)
      node is target
    x, y = a, b
    while (x or y) and x is not middle and x is not b and y is not middle and y is not a
      x = x and step(x, middle)
      y = y and step(y, middle)
    if x is middle
      return reaches(middle, b)
    if y is middle
      return reaches(middle, a)
    false
