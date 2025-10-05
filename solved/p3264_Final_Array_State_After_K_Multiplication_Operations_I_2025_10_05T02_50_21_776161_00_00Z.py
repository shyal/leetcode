"""
URL: https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-i/description/

3264. Final Array State After K Multiplication Operations I

You are given a 0-indexed array nums of n positive integers, an integer k, and an integer multiplier.

Perform exactly k operations. In each operation:

- Find the minimum value in nums (if there are multiple, choose any).

- Multiply one occurrence of this minimum value by multiplier.

Example 1:

Input: nums = [3,4], k = 2, multiplier = 4
Output: [12,16]
Explanation: Operation 1: Choose 3, multiply by 4 to get [12,4].
Operation 2: Choose 4, multiply by 4 to get [12,16].
The sorted array is [12,16].

Example 2:

Input: nums = [1,2,1], k = 3, multiplier = 2
Output: [2,2,4]
Explanation: Operation 1: Choose one 1, multiply by 2 to get something like [2,2,1].
Operation 2: Choose the remaining 1, multiply by 2 to get [2,2,2].
Operation 3: Choose a 2, multiply by 2 to get [2,2,4].
The sorted array is [2,2,4].


Constraints:

    1 <= nums.length <= 1000
    1 <= nums[i] <= 1000
    1 <= k <= 1000
    2 <= multiplier <= 100
"""


class Solution:

    def getFinalState(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        for i in range(k):
            _min = min(nums)
            index = nums.index(_min)
            nums[index] *= multiplier
        return nums


sol = Solution()

assert sol.getFinalState([2, 1, 3, 5, 6], 5, 2) == [8, 4, 6, 5, 6]
