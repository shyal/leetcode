# REFERENCE: d129 Longest Ending Here
class Solution:
    def longestEndingAt(self, nums):
        dp = table(len(nums), fill=1)
        for j, i in pairs(len(nums)):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
        return dp
