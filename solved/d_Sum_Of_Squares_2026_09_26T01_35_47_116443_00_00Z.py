"""
DRILL: Sum Of Squares

Given an integer array nums, return the sum of x * x over every element x
of nums.

Example 1:

Input: nums = [1, 2, 3]
Output: 14
Explanation: 1 + 4 + 9 = 14.

Example 2:

Input: nums = [-4]
Output: 16
Explanation: A negative element squares to a positive one.

Constraints:

    1 <= len(nums) <= 10^5
    -1000 <= nums[i] <= 1000

    REQUIRED: O(n), one expression. NO accumulator variable. NO loop
    statement.
"""


# mu 0.4
# def sumOfSquares(nums: [int]) -> int
#   # python version:
#   # sum(x*x for x in nums)
#   # fold version:
#   sum for x in nums: x*x

class Solution:
    def sumOfSquares(self, nums: list[int]) -> int:
        return sum(x * x for x in nums)


sol = Solution()
print(sol.sumOfSquares([1, 2, 3]))
assert sol.sumOfSquares([1, 2, 3]) == 14
assert sol.sumOfSquares([-4]) == 16
assert sol.sumOfSquares([0]) == 0
assert sol.sumOfSquares([0, 5, -2]) == 29
assert sol.sumOfSquares([-1, -1, -1]) == 3
assert sol.sumOfSquares([1000] * 100000) == 100000000000
