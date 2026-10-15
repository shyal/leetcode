"""
DRILL: Equal Pairs

Given an integer array nums, return the number of index pairs (i, j) with
i < j and nums[i] == nums[j].

Example 1:

Input: nums = [1, 2, 3, 1, 1, 3]
Output: 4
Explanation: The three 1s make 3 pairs and the two 3s make 1.

Example 2:

Input: nums = [1, 2, 3]
Output: 0

Constraints:

    1 <= len(nums) <= 10^5
    1 <= nums[i] <= 1000

    REQUIRED: O(n), one pass over nums. NO accumulator variable. NO
    enumeration of index pairs. NO arithmetic on group sizes.
"""


# mu 0.10
# class Solution
#   def equalPairs(nums: [int]) -> int
#     C = {:int}
#     sum for n in nums
#       got = C[n]
#       C[n] += 1
#       got

from collections import defaultdict


class Solution:
    def equalPairs(self, nums: list[int]) -> int:
        C = defaultdict(int)
        acc = 0
        for n in nums:
            got = C[n]
            C[n] += 1
            acc += got
        return acc


sol = Solution()
print(sol.equalPairs([1, 2, 3, 1, 1, 3]))
_l, _r = sol.equalPairs([1, 2, 3, 1, 1, 3]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([1, 2, 3]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([1, 1, 1, 1]), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([5]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([4, 4]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([4, 5, 4]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([1, 2, 1, 2]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.equalPairs([7] * 100000), 4999950000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
assert folds(Solution, 'sum', block=True)
