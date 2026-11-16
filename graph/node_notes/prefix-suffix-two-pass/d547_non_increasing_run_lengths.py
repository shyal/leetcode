# REFERENCE: d547 Non-Increasing Run Lengths
class Solution:
    def run_lengths(self, nums):
        res = [1] * len(nums)
        for i in range(1, len(nums)):
            if nums[i - 1] >= nums[i]:
                res[i] = res[i - 1] + 1  # extend the run that ends at i - 1
        return res
