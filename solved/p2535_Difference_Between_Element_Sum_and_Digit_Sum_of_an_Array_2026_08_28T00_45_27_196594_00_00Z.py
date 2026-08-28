"""
URL: https://leetcode.com/problems/difference-between-element-sum-and-digit-sum-of-an-array/description/?envType=problem-list-v2&envId=vn57k9wr

2535. Difference Between Element Sum and Digit Sum of an Array

You are given a positive integer array nums.

- The element sum is the sum of all the elements in nums.
- The digit sum is the sum of all the digits (not necessarily distinct) that appear in nums.

Return the absolute difference between the element sum and digit sum of nums.

Note that the absolute difference between two integers x and y is defined as |x - y|.

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
        return digits[::-1]

    def differenceOfSum(self, nums: List[int]) -> int:
        el_sum = sum(nums)
        di_sum = sum([*chain.from_iterable(self.getDigits(x) for x in nums)])
        return el_sum - di_sum


sol = Solution()

print(sol.differenceOfSum([1, 15, 6, 3]))  # 9

assert sol.differenceOfSum([1, 15, 6, 3]) == 9
assert sol.differenceOfSum([1, 2, 3, 4]) == 0

assert sol.differenceOfSum([2000]) == 1998
assert sol.differenceOfSum([1] * 2000) == 0
assert sol.differenceOfSum([2000] * 2000) == 3996000
assert sol.differenceOfSum([10, 100, 1000, 2000]) == 3105
assert sol.differenceOfSum([11, 22, 33, 44]) == 90
assert sol.differenceOfSum([9, 99, 999, 1999]) == 3024
assert sol.differenceOfSum([123, 456, 789]) == 1323
assert sol.differenceOfSum([1]) == 0
assert sol.differenceOfSum([2000]) == 1998
assert sol.differenceOfSum([1000, 1000, 1000, 1000]) == 3996
assert sol.differenceOfSum([101, 202, 303, 404]) == 990
assert sol.differenceOfSum([1999, 1999, 1999]) == 5913
