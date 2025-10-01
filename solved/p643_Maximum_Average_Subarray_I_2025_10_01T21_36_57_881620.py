"""
643. Maximum Average Subarray I
Easy
Topics
premium lock icon
Companies
You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10-5 will be accepted.

 

Example 1:

Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
Example 2:

Input: nums = [5], k = 1
Output: 5.00000
 

Constraints:

n == nums.length
1 <= k <= n <= 105
-104 <= nums[i] <= 104
"""


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        left = 0
        right = k - 1
        av = sum(nums[:k]) / k
        _max = av
        for i in range(k, len(nums)):
            av -= nums[i - k] / k
            av += nums[i] / k
            _max = max(_max, av)
        return int((_max) * 10**5) / 10**5


sol = Solution()
assert sol.findMaxAverage(nums=[1, 12, -5, -6, 50, 3], k=4) == 12.75000
assert sol.findMaxAverage(nums=[5], k=1) == 5
assert sol.findMaxAverage(nums=[0], k=1) == 0.0
assert sol.findMaxAverage(nums=[-1], k=1) == -1.0
assert sol.findMaxAverage(nums=[1, 2, 3, 4, 5], k=3) == 4.0
assert sol.findMaxAverage(nums=[-1, -2, -3, -4, -5], k=3) == -2.0
assert sol.findMaxAverage(nums=[1, 2, 3, 4, 5, 6], k=6) == 3.5
assert sol.findMaxAverage(nums=[10, 20, 30, 40], k=2) == 35.0
assert sol.findMaxAverage(nums=[5, 5, 5, 5], k=4) == 5.0
assert sol.findMaxAverage(nums=[1, -1, 1, -1], k=1) == 1.0
assert sol.findMaxAverage(nums=[1, -1, 1, -1], k=4) == 0.0
assert sol.findMaxAverage(nums=[4, 2, 1, 3, 0, 5], k=2) == 3.0
assert sol.findMaxAverage(nums=[3, -2, 5, 1, 7], k=3) == 4.33333

