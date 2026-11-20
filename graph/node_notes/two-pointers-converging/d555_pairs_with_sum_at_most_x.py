# REFERENCE: d555 Pairs With Sum At Most X
class Solution:
    def pairsAtMost(self, nums, x):
        count, left, right = 0, 0, len(nums) - 1
        while left < right:
            if nums[left] + nums[right] <= x:
                count += right - left
                left += 1
            else:
                right -= 1
        return count
