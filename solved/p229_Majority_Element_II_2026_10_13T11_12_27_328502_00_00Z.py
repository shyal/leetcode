"""
URL: https://leetcode.com/problems/majority-element-ii/description/?envType=problem-list-v2&envId=vn57k9wr

229. Majority Element II

Given an integer array of size n, find all elements that appear more than ⌊n / 3⌋ times.

Example 1:

Input: nums = [3,2,3]
Output: [3]

Example 2:

Input: nums = [1]
Output: [1]

Example 3:

Input: nums = [1,2]
Output: [1,2]

Constraints:

    1 <= nums.length <= 5 * 10^4
    -10^9 <= nums[i] <= 10^9

Follow up: Could you solve the problem in linear time and in O(1) space?
---
This is very easy using a counter, however the follow up is the interesting
but maybe not so easy part. let's implement boyer moor.

Hinted.

LEETCODE: Accepted (7 ms, 22.3 MB)
"""


# mu 0.10
# class Solution
#   def majorityElement(nums: [int]) -> [int]
#     # bf = [k for k, v in counter(nums).items() if v > len(nums) / 3]
#     # bf
#     # print(bf)
#     count1, count2 = 0, 0
#     cand1, cand2 = None, None
#     for n in nums
#       if n == cand1
#         count1 += 1
#       elif n == cand2
#         count2 += 1
#       elif count1 == 0
#         cand1, count1 = n, 1
#       elif count2 == 0
#         cand2, count2 = n, 1
#       else
#         count1 -= 1
#         count2 -= 1
#     [c for c in (cand1, cand2) if nums.count(c) > len(nums) // 3]

class Solution:
    def majorityElement(self, nums: list[int]) -> list[int]:
        count1, count2 = 0, 0
        cand1, cand2 = None, None
        for n in nums:
            if n == cand1:
                count1 += 1
            elif n == cand2:
                count2 += 1
            elif count1 == 0:
                cand1, count1 = n, 1
            elif count2 == 0:
                cand2, count2 = n, 1
            else:
                count1 -= 1
                count2 -= 1
        return [c for c in (cand1, cand2) if nums.count(c) > len(nums) // 3]


sol = Solution()
print(sol.majorityElement([1, 3, 3, 3, 4, 4, 4]))
_l, _r = sol.majorityElement([3, 2, 3]), [3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1]), [1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sorted(sol.majorityElement([1, 2])), [1, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([]), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 1, 1, 2, 2, 2, 3, 3, 3]), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1] * 16667 + [2] * 16667 + [3] * 16666), [1, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([-1, -1, -1, 0, 0, 1, 1, 1]), [-1, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([10 ** 9, 10 ** 9, 10 ** 9, -10 ** 9, -10 ** 9, -10 ** 9]), [1000000000, -1000000000]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([2] * 50000), [2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]), []
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([0] * 16667 + [1] * 16667 + [2] * 16666), [0, 1]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 1, 1, 2, 2, 3, 3, 3, 3]), [3]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]), [4]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.majorityElement([1] * 25000 + [2] * 25000), [1, 2]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
