# REFERENCE: d176 Longest Increasing Subsequence Ending At Each Index
class Solution
  def longestEndingAt(nums: [int]) -> [int]
    dp = table(len(nums), fill = 1)
    for (j, i) in pairs(len(nums), back = True)
      if nums[j] < nums[i]
        dp[i] = max(dp[i], dp[j] + 1)
    dp
