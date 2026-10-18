"""
URL: https://leetcode.com/problems/longest-continuous-increasing-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

674. Longest Continuous Increasing Subsequence

Given an unsorted array of integers nums, return the length of the longest continuous increasing subsequence (i.e. subarray). The subsequence must be strictly increasing.

A continuous increasing subsequence is defined by two indices l and r (l < r) such that it is [nums[l], nums[l + 1], ..., nums[r - 1], nums[r]] and for each l <= i < r, nums[i] < nums[i + 1].

Example 1:

Input: nums = [1,3,5,4,7]
Output: 3
Explanation: The longest continuous increasing subsequence is [1,3,5] with length 3.
Even though [1,3,5,7] is an increasing subsequence, it is not continuous as elements 5 and 7 are separated by element 4.

Example 2:

Input: nums = [2,2,2,2,2]
Output: 1
Explanation: The longest continuous increasing subsequence is [2] with length 1. Note that it must be strictly increasing.

Constraints:

    1 <= nums.length <= 10^4
    -10^9 <= nums[i] <= 10^9

---

LEETCODE: Accepted (0 ms, 20.3 MB)
"""


# mu 0.12
# class Solution
#   def findLengthOfLCIS(nums: [int]) -> int
#     ret best = 0
#     count = 0
#     prev = -inf
#     for n in nums
#       if n > prev
#         count += 1
#       else
#         count = 1
#       best = max(best, count)
#       prev = n

from math import inf


class Solution:
    def findLengthOfLCIS(self, nums: list[int]) -> int:
        best = 0
        count = 0
        prev = -inf
        for n in nums:
            if n > prev:
                count += 1
            else:
                count = 1
            best = max(best, count)
            prev = n
        return best


sol = Solution()
print(sol.findLengthOfLCIS([1, 3, 5, 4, 7]))
_l, _r = sol.findLengthOfLCIS([1, 3, 5, 4, 7]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([2, 2, 2, 2, 2]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([10]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 10
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([1, 2, 2, 3, 4]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([-1, 0, 1, 2, -1, 0, 1, 2, 3]), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([1000000000, 1000000001, 1000000002]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([-1000000000, -999999999, -999999998]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([1] * 10000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS(list(range(0, 5000)) + list(range(4999, 0, -1))), 5000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([1, 3, 5, 7, 6, 8, 10, 12]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.findLengthOfLCIS([5, 6, 7, 1, 2, 3, 4, 5, 6]), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
