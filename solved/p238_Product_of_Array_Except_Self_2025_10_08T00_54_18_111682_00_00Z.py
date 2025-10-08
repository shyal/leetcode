from typing import List

"""
URL: https://leetcode.com/problems/product-of-array-except-self/description/

238. Product of Array Except Self

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.


Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]


Constraints:

    2 <= nums.length <= 10^5
    -30 <= nums[i] <= 30
    The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.


Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)

---

OK so with this problem, it really helps to use variables instead of numbers, and think in terms
of output.

So with [a, b, c, d], the output is:

bcd, acd, abd, abc

so accumulating from the left, we get:

1, a, ab, abc

accumulating from the right, we get:

dcb dc d  1

multiplying these two gives us:

bcd, acd, abd, abc

"""

from operator import mul


class Solution:
    def productExceptSelfLetters(self, nums: List[int]) -> List[int]:
        acc = lambda x: [*accumulate(x)]
        left = ["1"] + acc(nums[:-1])
        right = (["1"] + acc((nums[1:])[::-1]))[::-1]
        return [a + b for a, b in zip(left, right)]

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        acc = lambda x: [*accumulate(x, mul)]
        left = [1] + acc(nums[:-1])
        right = ([1] + acc((nums[1:])[::-1]))[::-1]
        return [a * b for a, b in zip(left, right)]


sol = Solution()

# print(sol.productExceptSelf(["a", "b", "c", "d"]))  # ["bcd", "acd", "abd", "abc"]
# print(sol.productExceptSelf([1, 2, 3, 4]))  # [24,12,8,6]

assert sol.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
assert sol.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert sol.productExceptSelf([1, 2]) == [2, 1]
assert sol.productExceptSelf([0, 0]) == [0, 0]
assert sol.productExceptSelf([0, 0, 0]) == [0, 0, 0]
assert sol.productExceptSelf([-1, -2]) == [-2, -1]
assert sol.productExceptSelf([1, 0, 2]) == [0, 2, 0]
assert sol.productExceptSelf([3, 3, 3]) == [9, 9, 9]
assert sol.productExceptSelf([-3, 3, -3]) == [-9, 9, -9]
assert sol.productExceptSelf([1, 1, 1, 1]) == [1, 1, 1, 1]
assert sol.productExceptSelf([30, -30, 1]) == [-30, 30, -900]
assert sol.productExceptSelf([-1, 0, 1]) == [0, -1, 0]
