# REFERENCE: d321 Path Cost After Reversing One Suffix
class Solution
  def minCost(nums: [int]) -> int
    total = saving = prev = 0
    for x in nums
      total += abs(prev - x)
      saving = max(saving, abs(prev - x) - abs(prev - nums[-1]))
      prev = x
    total - saving
