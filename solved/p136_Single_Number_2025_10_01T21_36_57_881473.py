"""
URL: https://leetcode.com/problems/single-number/description/?envType=study-plan-v2&envId=leetcode-75

136. Single Number

Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.


Example 1:

Input: nums = [2,2,1]

Output: 1

Example 2:

Input: nums = [4,1,2,1,2]

Output: 4

Example 3:

Input: nums = [1]

Output: 1


Constraints:

        1 <= nums.length <= 3 * 104
        -3 * 104 <= nums[i] <= 3 * 104
        Each element in the array appears twice except for one element which appears only once.
"""

from typing import List
from functools import reduce
from operator import xor


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)


sol = Solution()
assert sol.singleNumber([2, 2, 1]) == 1
assert sol.singleNumber([4, 1, 2, 1, 2]) == 4
assert sol.singleNumber([1]) == 1
