# REFERENCE: d128 Smaller Before
def numPrevSmaller(nums: [int]) -> [int]
  dp = table(len(nums), fill = 0)
  for (j, i) in pairs(len(nums))
    if nums[j] < nums[i]
      dp[i] += 1
  dp
