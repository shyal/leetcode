"""
Non-Increasing Run Lengths

Given an array nums, return the array res where res[i] is the length of
the longest non-increasing subarray of nums that ends at index i.

Example 1:

Input: nums = [5, 3, 3, 4, 2]
Output: [1, 2, 3, 1, 2]
Explanation: At index 2 the subarray [5, 3, 3] is non-increasing.
At index 3 the subarray [4] is the longest, because 3 < 4.

Example 2:

Input: nums = [1, 2, 3]
Output: [1, 1, 1]

Example 3:

Input: nums = [7]
Output: [1]

Constraints:

    1 <= len(nums) <= 10^5
    1 <= nums[i] <= 10^6

    REQUIRED: O(len(nums)) time. NO nested loop.
"""


class Solution:
    def run_lengths(self, nums: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.run_lengths([5, 3, 3, 4, 2]))  # [1, 2, 3, 1, 2]

# assert sol.run_lengths([5, 3, 3, 4, 2]) == [1, 2, 3, 1, 2]
# assert sol.run_lengths([1, 2, 3]) == [1, 1, 1]
# assert sol.run_lengths([7]) == [1]
# assert sol.run_lengths([3, 3, 3]) == [1, 2, 3]
# assert sol.run_lengths([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
# assert sol.run_lengths([1, 2, 1, 2, 1]) == [1, 1, 2, 1, 2]
# assert sol.run_lengths([2, 1, 3, 3, 2, 1, 4]) == [1, 2, 1, 2, 3, 4, 1]
# assert sol.run_lengths([9, 1, 9, 1, 9]) == [1, 2, 1, 2, 1]
# assert sol.run_lengths([10 ** 6] * 10 ** 5)[-1] == 10 ** 5
