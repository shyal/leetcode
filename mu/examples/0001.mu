# 1. Two Sum
class Solution
  def twoSum(nums: [int], target: int) -> [int]
    seen = {}
    for i, x in nums
      if target - x in seen
        return [seen[target - x], i]
      seen[x] = i
