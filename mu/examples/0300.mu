# 300. Longest Increasing Subsequence
def lengthOfLIS(nums: [int]) -> int
  memo f(i) = 1 + max from 0 for j in 0..<i if nums[j] < nums[i]: f(j)
  max for i in 0..<len(nums): f(i)
