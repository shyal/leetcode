# REFERENCE: d128 Smaller Before
class Solution:
    def numPrevSmaller(self, nums):
        dp = table(len(nums), fill=0)
        for j, i in pairs(len(nums)):
            if nums[j] < nums[i]:
                dp[i] += 1
        return dp
