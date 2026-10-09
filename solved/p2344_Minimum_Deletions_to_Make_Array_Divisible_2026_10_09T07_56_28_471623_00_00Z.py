"""
URL: https://leetcode.com/problems/minimum-deletions-to-make-array-divisible/description/?envType=problem-list-v2&envId=vn57k9wr

2344. Minimum Deletions to Make Array Divisible

You are given two positive integer arrays nums and numsDivide. You can delete any number of elements from nums.

Return the minimum number of deletions such that the smallest element in nums divides all the elements of numsDivide. If this is not possible, return -1.

Note that an integer x divides y if y % x == 0.

Example 1:

Input: nums = [2,3,2,4,3], numsDivide = [9,6,9,3,15]
Output: 2
Explanation:
The smallest element in [2,3,2,4,3] is 2, which does not divide all the elements of numsDivide.
We use 2 deletions to delete the elements in nums that are equal to 2 which makes nums = [3,4,3].
The smallest element in [3,4,3] is 3, which divides all the elements of numsDivide.
It can be shown that 2 is the minimum number of deletions needed.

Example 2:

Input: nums = [4,3,6], numsDivide = [8,2,6,10]
Output: -1
Explanation:
We want the smallest element in nums to divide all the elements of numsDivide.
There is no way to delete elements from nums to allow this.

Constraints:

    1 <= nums.length, numsDivide.length <= 10^5
    1 <= nums[i], numsDivide[i] <= 10^9
---
bf solution: TLE

def minOperations(nums: [int], numsDivide: [int]) -> int
  _min = inf
  for n in sorted([*set(nums)])
    if all([x % n == 0 for x in numsDivide])
      _min = n
      break
  if _min != inf
    cnt = 0
    for x in nums
      cnt += x < _min
    return cnt
  return -1

need a binary search


def minOperations(nums: [int], numsDivide: [int]) -> int
  arr = [*sorted(set(nums))]
  _min = last_true(0, len(arr) -1, x -> all(y % arr[x] == 0 for y in numsDivide))
  val = arr[_min]
  len([1 for x in nums if x < val])

no clear true false boundary, so not a binary search

don't know. Will go with brute force for now.

LEETCODE: Time Limit Exceeded (38/49 cases)
"""


# mu 0.7
# def minOperations(nums: [int], numsDivide: [int]) -> int
#   _min = inf
#   for n in sorted([*set(nums)])
#     if all([x % n == 0 for x in numsDivide])
#       _min = n
#       break
#   if _min != inf
#     cnt = 0
#     for x in nums
#       cnt += x < _min
#     return cnt
#   return -1

from math import inf


class Solution:
    def minOperations(self, nums: list[int], numsDivide: list[int]) -> int:
        _min = inf
        for n in sorted([*set(nums)]):
            if all([x % n == 0 for x in numsDivide]):
                _min = n
                break
        if _min != inf:
            cnt = 0
            for x in nums:
                cnt += x < _min
            return cnt
        return -1


sol = Solution()
print(sol.minOperations([2, 3, 2, 4, 3], [9, 6, 9, 3, 15]))
_l, _r = sol.minOperations([2, 3, 2, 4, 3], [9, 6, 9, 3, 15]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([4, 3, 6], [8, 2, 6, 10]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([1], [1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([10 ** 9], [10 ** 9]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([2, 2, 2, 2], [4, 8, 16]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([3, 6, 9, 12], [18, 36, 54]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([5, 10, 15, 20], [25, 50, 75]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([7, 14, 21, 28], [49, 98, 147]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([1, 2, 3, 4, 5], [10 ** 9, 10 ** 9 - 1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([10, 5, 2, 1], [20, 40, 60]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([2, 4, 6, 8, 10], [3, 6, 9]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([3, 3, 3, 3], [9, 18, 27]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([10 ** 9, 2, 3], [10 ** 9, 2]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minOperations([2, 3, 5, 7, 11], [13, 17, 19]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
