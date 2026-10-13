"""
URL: https://leetcode.com/problems/majority-element/description/?envType=problem-list-v2&envId=vn57k9wr

169. Majority Element

Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

Example 1:

Input: nums = [3,2,3]
Output: 3

Example 2:

Input: nums = [2,2,1,1,1,2,2]
Output: 2

Constraints:

    n == nums.length
    1 <= n <= 5 * 10^4
    -10^9 <= nums[i] <= 10^9
    The input is generated such that a majority element will exist in the array.

Follow-up: Could you solve the problem in linear time and in O(1) space?
---
I have no recollection of Boyer moor, so re-doing this.
ok so we start with a candidate (nums[0]). If the count is 0, we switch
candidate to n, else we increment or decrement count depending on whether
n is our candidate. no matter the distribution of numbers in the array
since we have a majority element, the count cannot decrease enough to
switch before we reach the end of the array. neat.

LEETCODE: Accepted (17 ms, 21.6 MB)
"""


# mu 0.10
# class Solution
#   def majorityElement(nums: [int]) -> int
#     ret cand, count = nums[0], 0
#     for n in nums
#       if count == 0
#         cand = n
#       count += [-1, 1][n == cand]

class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        cand, count = nums[0], 0
        for n in nums:
            if count == 0:
                cand = n
            count += [-1, 1][n == cand]
        return cand


sol = Solution()
print(sol.majorityElement([3, 2, 3]))
_l, _r = sol.majorityElement([3, 2, 3]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([2, 2, 1, 1, 1, 2, 2]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 2, 1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([-1, -1, -1, 2, 2]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([10 ** 9] * 25000 + [1] * 24999), 1000000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([-10 ** 9] * 30000 + [10 ** 9] * 20000), -1000000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([5] * 25000 + [4] * 25000 + [5]), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([0] * 10000 + [1] * 20001), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([7] * 1 + [8] * 1 + [7] * 1), 7
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([-5] * 25001 + [-4] * 24999), -5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([2] * 25000 + [3] * 25000 + [2]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([100] * 50000), 100
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
