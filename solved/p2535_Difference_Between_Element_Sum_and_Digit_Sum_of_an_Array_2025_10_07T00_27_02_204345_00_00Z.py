"""
URL: https://leetcode.com/problems/difference-between-element-sum-and-digit-sum-of-an-array/description/?envType=daily-question&envId=2024-09-20

2535. Difference Between Element Sum and Digit Sum of an Array

You are given a positive integer array nums.

    The element sum is the sum of all the elements in nums.
    The digit sum is the sum of all the digits (not necessarily distinct) that appear in nums.

Return the absolute difference between the element sum and digit sum of nums.

Example 1:

Input: nums = [1,15,6,3]
Output: 9
Explanation:
The element sum of nums is 1 + 15 + 6 + 3 = 25.
The digit sum of nums is 1 + 1 + 5 + 6 + 3 = 16.
The absolute difference between the element sum and digit sum is |25 - 16| = 9.

Example 2:

Input: nums = [1,2,3,4]
Output: 0
Explanation:
The element sum of nums is 1 + 2 + 3 + 4 = 10.
The digit sum of nums is 1 + 2 + 3 + 4 = 10.
The absolute difference between the element sum and digit sum is |10 - 10| = 0.

Constraints:

    1 <= nums.length <= 2000
    1 <= nums[i] <= 2000

"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def differenceOfSum(self, nums: List[int]) -> int:
        _sum = sum(nums)
        digit_sum = sum(chain(*[self.getDigits(x) for x in nums]))
        return abs(_sum - digit_sum)


sol = Solution()

assert sol.differenceOfSum([1, 15, 6, 3]) == 9
assert sol.differenceOfSum([1, 2, 3, 4]) == 0
assert sol.differenceOfSum([1]) == 0
assert sol.differenceOfSum([2000]) == 1998
assert sol.differenceOfSum([10]) == 9
assert sol.differenceOfSum([999]) == 972
assert sol.differenceOfSum([100, 200]) == 297
assert sol.differenceOfSum([1, 1, 1, 1]) == 0
