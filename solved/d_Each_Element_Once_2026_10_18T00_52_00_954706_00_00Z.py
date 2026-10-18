"""
DRILL: Each Element Once
SNIPPET: lccomb

Given an array nums of distinct positive integers in increasing order and
an integer target, return every combination of elements of nums whose sum
is target. Each element can be used at most once. List each combination
in increasing order. The combinations themselves can be returned in any
order.

Example 1:

Input: nums = [1, 2, 3, 4, 5], target = 6
Output: [[1, 2, 3], [1, 5], [2, 4]]

Example 2:

Input: nums = [2, 4], target = 5
Output: []
Explanation: 2, 4 and 2 + 4 are all different from 5.

Example 3:

Input: nums = [2, 3, 7], target = 7
Output: [[7]]
Explanation: [2, 2, 3] sums to 7 but uses 2 twice.

Constraints:

    1 <= len(nums) <= 20
    1 <= nums[i] <= 40
    1 <= target <= 40
    The elements of nums are distinct and given in increasing order.

    REQUIRED: never extend a combination whose sum already equals or
    exceeds target. NO fixed length k, NO building every combination and
    filtering by sum at the end.
"""


# mu 0.12
# class Solution
#   def sumOnce(nums: [int], target: int) -> [[int]]
#     def helper(i, t)
#       if t == target
#         res <- path[:]
#         return
#       if t > target
#         return
#       for j in i..<len(nums)
#         path <- nums[j]
#         helper(j + 1, nums[j] + t)
#         path .
#     ret res, path = [], []
#     nums.sort()
#     helper(0, 0)

class Solution:
    def sumOnce(self, nums: list[int], target: int) -> list[list[int]]:
        def helper(i, t):
            if t == target:
                res.append(path[:])
                return
            if t > target:
                return
            for j in range(i, len(nums)):
                path.append(nums[j])
                helper(j + 1, nums[j] + t)
                path.pop()
        res, path = [], []
        nums.sort()
        helper(0, 0)
        return res


sol = Solution()
print_orig(sol.sumOnce([1, 2, 3, 4, 5], 6))
_l, _r = sorted(map(tuple, sol.sumOnce([1, 2, 3, 4, 5], 6))), [(1, 2, 3), (1, 5), (2, 4)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sumOnce([2, 4], 5), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sumOnce([2, 3, 7], 7), [[7]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.sumOnce([2, 3, 5], 8), [[3, 5]]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
res = sol.sumOnce(list(range(1, 11)), 10)
assert len(res) == 10 and len({tuple(c) for c in res}) == 10
assert all((sum(c) == 10 and c == sorted(set(c)) for c in res))
_l, _r = len(sol.sumOnce(list(range(1, 21)), 40)), 806
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
