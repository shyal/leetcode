"""
DRILL: Smaller Before
TRAINS: dp-1d-rolling

Given an integer array nums, return an array dp of the same length where
dp[i] is how many values at an index below i are strictly smaller than
nums[i].

Example 1:

Input: nums = [4, 1, 6, 2, 8, 5, 9]
Output: [0, 0, 2, 1, 4, 3, 6]
Explanation: before the 5 at index 5 sit 4, 1, 6, 2, 8, and three of
them are smaller than 5.

Example 2:

Input: nums = [5, 4, 3, 2, 1]
Output: [0, 0, 0, 0, 0]

Example 3:

Input: nums = [2, 2, 3, 3]
Output: [0, 0, 2, 2]
Explanation: equal values do not count.

Constraints:

    1 <= len(nums) <= 2500
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n^2), every earlier index compared against i. NO sorting.
    The test is strictly smaller: counting an equal value is the fail.
"""


class Solution:

    def numPrevSmaller(self, nums: List[int]) -> List[int]:
        pass


sol = Solution()

print(sol.numPrevSmaller([4, 1, 6, 2, 8, 5, 9]))  # [0, 0, 2, 1, 4, 3, 6]

# assert sol.numPrevSmaller([4, 1, 6, 2, 8, 5, 9]) == [0, 0, 2, 1, 4, 3, 6]
# assert sol.numPrevSmaller([5, 4, 3, 2, 1]) == [0, 0, 0, 0, 0]
# assert sol.numPrevSmaller([2, 2, 3, 3]) == [0, 0, 2, 2]
# assert sol.numPrevSmaller([1, 2, 3, 4, 5]) == [0, 1, 2, 3, 4]
# assert sol.numPrevSmaller([7]) == [0]
# assert sol.numPrevSmaller([3, 3, 3]) == [0, 0, 0]
# assert sol.numPrevSmaller([-1, -3, -2, 0]) == [0, 0, 1, 3]
# assert sol.numPrevSmaller([2, 3, 1, 4]) == [0, 1, 0, 3]
# assert sol.numPrevSmaller([9, 1, 8, 2, 7, 3]) == [0, 0, 1, 1, 2, 2]
# assert sol.numPrevSmaller(list(range(2500)))[-1] == 2499
