# REFERENCE: d537 Odd Sum Subarrays
class Solution:
    def oddSumSubarrays(self, nums):
        oddc = 0
        for prefix in accumulate(nums):
            oddc += prefix % 2
        evenc = len(nums) - oddc + 1
        return oddc * evenc
