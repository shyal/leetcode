"""
DRILL: Smaller Before
TRAINS: dp-1d-rolling

Given an integer array nums, return an array dp of the same length where
dp[i] is how many values at an index below i are strictly smaller than
nums[i].

Example 1:

Input: nums = [4, 1, 6, 2, 8, 5, 9]
Output: [0, 0, 2, 1, 4, 3, 6]
Explanation: before the 5 at index 5 sit 4, 1, 6, 2, 8, and three of
them are smaller than 5.

Example 2:

Input: nums = [5, 4, 3, 2, 1]
Output: [0, 0, 0, 0, 0]

Example 3:

Input: nums = [2, 2, 3, 3]
Output: [0, 0, 2, 2]
Explanation: equal values do not count.

Constraints:

    1 <= len(nums) <= 2500
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n^2), every earlier index compared against i. NO sorting.
    The test is strictly smaller: counting an equal value is the fail.

DRILL_FILL: part of the solve is given, from solved/d_Smaller_Before_2026_09_30T03_28_17_449078_00_00Z.py (4 Good reps in a row). Write the lines marked pass.
"""


# mu 0.12
# class Solution
#   def numPrevSmaller(nums: [int]) -> [int]
#     ret res = table(len(nums))
#     for i, j in pairs(len(nums), back=True)
#       res[j] += nums[i] < nums[j]

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def pairs(n, type=tuple, back=False):
    if back:
        for j in range(n):
            for i in range(j):
                yield type((i, j))
        return
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))


class Solution:
    def numPrevSmaller(self, nums: list[int]) -> list[int]:
        res = table(len(nums))
        for i, j in pairs(len(nums), back=True):
            res[j] += nums[i] < nums[j]
        return res


sol = Solution()
print(sol.numPrevSmaller([4, 1, 6, 2, 8, 5, 9]))
_l, _r = sol.numPrevSmaller([4, 1, 6, 2, 8, 5, 9]), [0, 0, 2, 1, 4, 3, 6]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([5, 4, 3, 2, 1]), [0, 0, 0, 0, 0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([2, 2, 3, 3]), [0, 0, 2, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([1, 2, 3, 4, 5]), [0, 1, 2, 3, 4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([7]), [0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([3, 3, 3]), [0, 0, 0]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([-1, -3, -2, 0]), [0, 0, 1, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([2, 3, 1, 4]), [0, 1, 0, 3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller([9, 1, 8, 2, 7, 3]), [0, 0, 1, 1, 2, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numPrevSmaller(list(range(0, 2500)))[-1], 2499
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
