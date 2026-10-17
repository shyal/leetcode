"""
DRILL: Kth Smallest Bounded Value

Given an integer array nums whose values all lie between 0 and 100
inclusive, and an integer k, return the kth smallest value of nums,
counting duplicates. The value k is 1-based, so k = 1 asks for the
minimum and k = len(nums) asks for the maximum.

Example 1:

Input: nums = [9, 3, 6, 3, 9, 1], k = 4
Output: 6
Explanation: in non-decreasing order the values are 1, 3, 3, 6, 9, 9
and the 4th is 6.

Example 2:

Input: nums = [4, 4, 4], k = 3
Output: 4

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 100
    1 <= k <= len(nums)

    REQUIRED: O(n + 100) time and O(100) extra space. NO sort(), NO
    sorted(), NO heapq, and you must NOT build the sorted array.
    Materialising all n values in order to read one of them is the
    failure mode this drill exists to kill.

DRILL_FILL: part of the solve is given, from solved/d_Kth_Smallest_Bounded_Value_2026_09_18T22_07_22_091594_00_00Z.py (4 Good reps in a row). Write the lines marked pass.
"""


# mu 0.12
# class Solution
#   def kthSmallest(nums: [int], k: int) -> int
#     buckets = [0] * 101
#     for n in nums
#       buckets[n] += 1
#     total = 0
#     for >i, v in buckets
#       total += v
#       if total == k
#         return i

class Solution:
    def kthSmallest(self, nums: list[int], k: int) -> int:
        buckets = [0] * 101
        for n in nums:
            buckets[n] += 1
        total = 0
        for i, v in enumerate(buckets):
            total += v
            if total == k:
                return i


sol = Solution()
print(sol.kthSmallest([9, 3, 6, 3, 9, 1], 4))
_l, _r = sol.kthSmallest([9, 3, 6, 3, 9, 1], 4), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.kthSmallest([4, 4, 4], 3), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.kthSmallest([9, 3, 6, 3, 9, 1], 1), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.kthSmallest([9, 3, 6, 3, 9, 1], 6), 9
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.kthSmallest([9, 3, 6, 3, 9, 1], 3), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.kthSmallest([100, 0], 2), 100
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.kthSmallest([5], 1), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
