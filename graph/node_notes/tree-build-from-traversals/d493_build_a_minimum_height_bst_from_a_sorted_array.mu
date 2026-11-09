# REFERENCE: d493 EPI 14.8 Build a minimum height BST from a sorted array
class Solution
  def build_min_height_bst_from_sorted_array(A: [int]) -> TreeNode?
    def build(lo, hi)
      if lo == hi
        return none
      mid = (lo + hi) // 2
      TreeNode(A[mid], build(lo, mid), build(mid + 1, hi))
    build(0, len(A))
