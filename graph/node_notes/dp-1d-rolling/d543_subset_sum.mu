# REFERENCE: d543 Subset Sum
class Solution
  def subsetSum(nums: [int], target: int) -> bool
    sums = {0}
    for x in nums
      sums |= {s + x for s in sums if s + x <= target}
    target in sums
