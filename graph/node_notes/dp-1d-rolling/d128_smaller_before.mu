# REFERENCE: d128 Smaller Before
class Solution
  def numPrevSmaller(nums: [int]) -> [int]
    dp = table(len(nums), fill = 0)
    for (j, i) in pairs(len(nums), back = True)
      if nums[j] < nums[i]
        dp[i] += 1
    dp
