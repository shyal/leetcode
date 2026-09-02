"""
DRILL: Count Smaller Values
TRAINS: counting-sort-buckets

Given an integer array nums whose values all lie between 0 and 100
inclusive, return an array counts where counts[i] is the number of
elements of nums that are strictly smaller than nums[i].

Example 1:

Input: nums = [8, 1, 2, 2, 3]
Output: [4, 0, 1, 1, 3]
Explanation: four values are smaller than 8, none are smaller than 1,
one value is smaller than each 2, and three values are smaller than 3.

Example 2:

Input: nums = [7, 7, 7, 7]
Output: [0, 0, 0, 0]

Constraints:

    2 <= len(nums) <= 10^5
    0 <= nums[i] <= 100

    REQUIRED: O(n + 100) time. NO sort(), NO sorted(), NO nested loop
    over nums. Comparing every pair is the failure mode this drill
    exists to kill; len(nums) makes it a TLE.
"""


class Solution:

    def smallerThanEach(self, nums: List[int]) -> List[int]:
        pass


sol = Solution()

print(sol.smallerThanEach([8, 1, 2, 2, 3]))  # [4, 0, 1, 1, 3]

# assert sol.smallerThanEach([8, 1, 2, 2, 3]) == [4, 0, 1, 1, 3]
# assert sol.smallerThanEach([7, 7, 7, 7]) == [0, 0, 0, 0]
# assert sol.smallerThanEach([6, 5, 4, 8]) == [2, 1, 0, 3]
# assert sol.smallerThanEach([0, 100]) == [0, 1]
# assert sol.smallerThanEach([0, 0, 1]) == [0, 0, 2]
# assert sol.smallerThanEach([100, 0, 50, 50]) == [3, 0, 1, 1]
