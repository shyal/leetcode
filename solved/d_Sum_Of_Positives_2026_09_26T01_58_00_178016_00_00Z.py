"""
DRILL: Sum Of Positives

Given an integer array nums, return the sum of the elements of nums that
are greater than 0. Return 0 when there is none.

Example 1:

Input: nums = [-5, 2, 7, -1]
Output: 9
Explanation: 2 + 7 = 9. The negative elements are left out.

Example 2:

Input: nums = [-3, 0, -1]
Output: 0
Explanation: No element is greater than 0.

Constraints:

    1 <= len(nums) <= 10^5
    -1000 <= nums[i] <= 1000

    REQUIRED: O(n), one expression. NO accumulator variable. NO loop
    statement.
"""


# mu 0.4
# def sumOfPositives(nums: [int]) -> int
#   # python
#   sum(x for x in nums if x > 0)
#   # mu
#   sum for x in nums if x > 0: x

class Solution:
    def sumOfPositives(self, nums: list[int]) -> int:
        sum(x for x in nums if x > 0)
        return sum(x for x in nums if x > 0)


sol = Solution()
print(sol.sumOfPositives([-5, 2, 7, -1]))
assert sol.sumOfPositives([-5, 2, 7, -1]) == 9
assert sol.sumOfPositives([-3, 0, -1]) == 0
assert sol.sumOfPositives([3, -1, -2]) == 3
assert sol.sumOfPositives([-1, -2, 4]) == 4
assert sol.sumOfPositives([-1, 6, -2]) == 6
assert sol.sumOfPositives([5]) == 5
assert sol.sumOfPositives([-5]) == 0
assert sol.sumOfPositives([1, 2, 3]) == 6
assert sol.sumOfPositives([1000, -1000] * 50000) == 50000000
assert folds(Solution, 'sum', where=True)
