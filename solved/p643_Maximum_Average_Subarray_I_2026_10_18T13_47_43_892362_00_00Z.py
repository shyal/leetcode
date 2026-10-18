"""
URL: https://leetcode.com/problems/maximum-average-subarray-i/description/?envType=problem-list-v2&envId=vn57k9wr

643. Maximum Average Subarray I

You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10^-5 will be accepted.

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

LEETCODE: Accepted (96 ms, 29 MB)
"""


# mu 0.12
# class Solution
#   def findMaxAverage(nums: [int], k: int) -> float
#     avg = sum(nums[:k]) / k
#     ret max_avg = avg
#     for i in k..len(nums)-1
#       avg *= k
#       avg -= nums[i-k]
#       avg += nums[i]
#       avg /= k
#       max_avg = max(max_avg, avg)

class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        avg = sum(nums[:k]) / k
        max_avg = avg
        for i in range(k, len(nums) - 1 + 1):
            avg *= k
            avg -= nums[i - k]
            avg += nums[i]
            avg /= k
            max_avg = max(max_avg, avg)
        return max_avg


sol = Solution()
print(sol.findMaxAverage([1, 12, -5, -6, 50, 3], 4))
_l, _r = abs(sol.findMaxAverage([1, 12, -5, -6, 50, 3], 4) - 12.75), 1e-05
assert _l < _r, f"left : {_l!r}\nright: {_r!r}\nop   : <"
_l, _r = abs(sol.findMaxAverage([5], 1) - 5.0), 1e-05
assert _l < _r, f"left : {_l!r}\nright: {_r!r}\nop   : <"
_l, _r = sol.findMaxAverage([0] * 100000, 50000), 0.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([-10000] * 100000, 100000), -10000.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([10000] * 100000, 1), 10000.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10), 5.5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([1, -1, 1, -1, 1, -1, 1, -1], 2), 0.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([5, 5, 5, 5, 5, 5, 5], 3), 5.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([-5, -5, -5, -5, -5], 2), -5.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([10 ** 4, -10 ** 4] * 50000, 2), 0.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([1] * 99999 + [10000], 1), 10000.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([10000] + [1] * 99999, 100000), 1.09999
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([0, 0, 0, 0, 0], 1), 0.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findMaxAverage([1, 2, 3, 4, 5], 1), 5.0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
