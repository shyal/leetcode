"""
DRILL: Largest Even

Given an array nums of non-negative integers, return the largest even
element of nums. Return -1 when nums has no even element.

Example 1:

Input: nums = [3, 8, 5, 6, 1]
Output: 8
Explanation: The even elements are 8 and 6.

Example 2:

Input: nums = [1, 3, 5]
Output: -1
Explanation: No element is even.

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 10^9

    REQUIRED: O(n), one expression. NO accumulator variable. NO loop
    statement. NO sort.
"""


# mu 0.11
# class Solution
#   def largestEven(nums: [int]) -> int
#     max from -1 for x in nums if even(x): x

def even(n):
    return n % 2 == 0


class Solution:
    def largestEven(self, nums: list[int]) -> int:
        return max(-1, max((x for x in nums if even(x)), default=-1))


sol = Solution()
print(sol.largestEven([3, 8, 5, 6, 1]))
_l, _r = sol.largestEven([3, 8, 5, 6, 1]), 8
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([1, 3, 5]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([10, 3, 4, 7]), 10
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([1, 4, 3, 12]), 12
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([7]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([0, 1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([9, 9, 2, 9]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([10 ** 9, 10 ** 9 - 1]), 1000000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.largestEven([1] * 100000), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
assert folds(Solution, 'max', start=True, where=True)
