# REFERENCE: d319 Maximum Alternating Subarray Sum
class Solution
  def maxAlternatingSum(nums: [int]) -> int
    plus = minus = best = -inf
    for x in nums
      plus, minus = max(x, minus + x), plus - x
      best = max(best, plus, minus)
    best
