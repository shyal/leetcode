# REFERENCE: d318 Maximum Subarray Sum
class Solution
  def maxSubArray(nums: [int]) -> int
    ending = 0
    best = -inf
    for x in nums
      ending = max(x, ending + x)
      best = max(best, ending)
    best
