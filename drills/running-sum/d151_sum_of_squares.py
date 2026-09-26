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


class Solution:

    def sumOfSquares(self, nums: List[int]) -> int:
        pass


sol = Solution()

print(sol.sumOfSquares([1, 2, 3]))  # 14

# assert sol.sumOfSquares([1, 2, 3]) == 14
# assert sol.sumOfSquares([-4]) == 16
# assert sol.sumOfSquares([0]) == 0
# assert sol.sumOfSquares([0, 5, -2]) == 29
# assert sol.sumOfSquares([-1, -1, -1]) == 3
# assert sol.sumOfSquares([1000] * 100000) == 100000000000
