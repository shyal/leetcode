# REFERENCE: d176 Longest Ending Here
def longestEndingAt(nums: [int]) -> [int]
  dp = table(len(nums), fill = 1)
  for (j, i) in pairs(len(nums))
    if nums[j] < nums[i]
      dp[i] = max(dp[i], dp[j] + 1)
  dp
