"""
URL: https://leetcode.com/problems/minimum-element-after-replacement-with-digit-sum/description/

3300. Minimum Element After Replacement With Digit Sum

You are given an array nums consisting of n positive integers.

You can perform the following operation on the array any number of times (possibly zero):

Choose an index i and replace nums[i] with the sum of its digits.

Return the minimum possible value of the smallest element in nums after performing the operations.

Example 1:

Input: nums = [10,12,13,14]
Output: 1
Explanation: Transform the array into [1, 3, 4, 5].
- 10 is replaced by 1 + 0 = 1.
- 12 is replaced by 1 + 2 = 3.
- 13 is replaced by 1 + 3 = 4.
- 14 is replaced by 1 + 4 = 5.
The smallest element is 1.

Example 2:

Input: nums = [1,2,3,4]
Output: 1
Explanation: The array is already good. The smallest element is 1.

Example 3:

Input: nums = [999,999,999]
Output: 9
Explanation: Every element in the array can become 9.
- First 999: 9 + 9 + 9 = 27, then 2 + 7 = 9.
- Similarly for the others.
It is impossible to make any element smaller than 9.


Constraints:

    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^9

"""


class Solution:

    def addDigitsUntil1Digit(self, num):
        num = sum(int(x) for x in str(num))
        return num

    def minElement(self, nums: List[int]) -> int:
        return min(self.addDigitsUntil1Digit(x) for x in nums)


sol = Solution()

assert sol.minElement([999, 19, 199]) == 10
assert sol.minElement([10, 12, 13, 14]) == 1
assert sol.minElement([1, 2, 3, 4]) == 1
