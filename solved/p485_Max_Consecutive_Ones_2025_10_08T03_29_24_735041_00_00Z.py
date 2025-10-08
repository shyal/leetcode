"""
URL: https://leetcode.com/problems/max-consecutive-ones/description/

485. Max Consecutive Ones

Given a binary array nums, return the maximum number of consecutive 1's in the array.

Example 1:

Input: nums = [1,1,0,1,1,1]
Output: 3
Explanation: The first two digits or the last three digits are consecutive 1s. The maximum number of consecutive 1s is 3.

Example 2:

Input: nums = [1,0,1,1,0,1]
Output: 2

Constraints:

    1 <= nums.length <= 10^5
    nums[i] is either 0 or 1.
"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        consecutive = 0
        max_ones = 0
        for n in nums:
            if n:
                consecutive += 1
                max_ones = max(max_ones, consecutive)
            else:
                consecutive = 0
        return max_ones


sol = Solution()

# print(sol.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1]))  # 3

assert sol.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1]) == 3
assert sol.findMaxConsecutiveOnes([1, 0, 1, 1, 0, 1]) == 2
assert sol.findMaxConsecutiveOnes([1]) == 1
assert sol.findMaxConsecutiveOnes([0]) == 0
assert sol.findMaxConsecutiveOnes([1, 1, 1, 1]) == 4
assert sol.findMaxConsecutiveOnes([0, 0, 0, 0]) == 0
assert sol.findMaxConsecutiveOnes([1, 0, 1, 1, 1, 0, 1]) == 3
assert sol.findMaxConsecutiveOnes([0, 1, 1, 0, 1, 1, 1, 1, 0]) == 4
assert sol.findMaxConsecutiveOnes([1, 1, 1, 0, 0, 1, 1]) == 3
assert sol.findMaxConsecutiveOnes([0, 1, 0, 1, 0, 1, 0]) == 1
