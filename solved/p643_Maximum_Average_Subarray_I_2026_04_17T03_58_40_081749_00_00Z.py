"""
URL: https://leetcode.com/problems/maximum-average-subarray-i/description/?envType=problem-list-v2&envId=vn57k9wr

643. Maximum Average Subarray I

You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average
value and return this value. Any answer with a calculation error less than 10^-5
will be accepted.


Example 1:

Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

Example 2:

Input: nums = [5], k = 1
Output: 5.00000


Constraints:

    n == nums.length
    1 <= k <= n <= 10^5
    -10^4 <= nums[i] <= 10^4

---

[1, 12, -5, -6, 50, 3], 4




"""

class Solution:

    def av(self, nums):
        return sum(nums) / len(nums)

    def findMaxAverageSlow(self, nums: List[int], k: int) -> float:
        _max = float('-inf')
        for r in range(k-1, len(nums)):
            l = r - k + 1
            av = self.av(nums[l:r+1])
            _max = max(_max, av)
        return _max

    def findMaxAverage(self, nums: List[int], k: int) -> float:
        _max = float('-inf')
        _sum = 0
        for r in range(len(nums)):
            _sum += nums[r]
            if r >= k -1:
                av = _sum / k
                _max = max(_max, av)
            l = r -k + 1
            if l >= 0:
                _sum -= nums[l]
        return _max


sol = Solution()

assert isclose(sol.findMaxAverage([1, 12, -5, -6, 50, 3], 4), 12.75)
assert isclose(sol.findMaxAverage([5], 1), 5.00000)
assert isclose(sol.findMaxAverage([0, 0, 0, 0], 2), 0.0)
assert isclose(sol.findMaxAverage([-1, -2, -3, -4, -5], 2), -1.5)
assert isclose(sol.findMaxAverage([-1, -2, -3, -4, -5], 5), -3.0)
assert isclose(sol.findMaxAverage([10000, 10000, 10000], 3), 10000.0)
assert isclose(sol.findMaxAverage([-10000, -10000, -10000], 1), -10000.0)
assert isclose(sol.findMaxAverage([1, 2, 3, 4, 5], 1), 5.0)
assert isclose(sol.findMaxAverage([1, 2, 3, 4, 5], 5), 3.0)
assert isclose(sol.findMaxAverage([5, 5, 5, 5, 5], 3), 5.0)
assert isclose(sol.findMaxAverage([-5, 5, -5, 5, -5], 2), 0.0)
assert isclose(sol.findMaxAverage([4, 0, 4, 3, 3], 5), 2.8)
assert isclose(sol.findMaxAverage([0, 1, 1, 3, 3], 4), 2.0)
assert isclose(sol.findMaxAverage([-10000, 10000], 1), 10000.0)
assert isclose(sol.findMaxAverage([-10000, 10000], 2), 0.0)