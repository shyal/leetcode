"""
URL: https://leetcode.com/problems/maximum-product-subarray/description/?envType=problem-list-v2&envId=vn57k9wr

152. Maximum Product Subarray

Given an integer array nums, find a subarray that has the largest product, and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

Note that the product of an array with a single element is the value of that element.

Example 1:

Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.

Example 2:

Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.

Constraints:

    1 <= nums.length <= 2 * 10^4
    -10 <= nums[i] <= 10
    The product of any subarray of nums is guaranteed to fit in a 32-bit integer.
---
Learning

LEETCODE: Accepted (3 ms, 19.7 MB)
"""


# mu 0.10
# class Solution
#   def maxProduct(nums: [int]) -> int
#     ret best = lo = hi = nums[0]
#     for v in nums[1:]
#       if v < 0
#         hi, lo = lo, hi
#       hi, lo = max(v, hi * v), min(v, lo * v)
#       best = max(best, hi)

class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        best = lo = hi = nums[0]
        for v in nums[1:]:
            if v < 0:
                hi, lo = lo, hi
            hi, lo = max(v, hi * v), min(v, lo * v)
            best = max(best, hi)
        return best


sol = Solution()
print(sol.maxProduct([2, 3, -2, 4]))
_l, _r = sol.maxProduct([2, 3, -2, 4]), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([-2, 0, -1]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([1]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([-1]), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([0, 0, 0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([-1, -2, -3, -4]), 24
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([10, -10, 10, -10]), 10000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([-10, 10, -10, 10]), 10000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([1] * 20000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([-1] * 20000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxProduct([0] * 20000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
