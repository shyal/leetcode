"""
Given an integer array nums, return the number of subarrays whose sum is
odd. A subarray is a contiguous non-empty part of nums. Two subarrays
with the same values at different positions are two subarrays.

Example 1:

Input: nums = [2, 3, 4, 5]
Output: 6
Explanation: the odd sums are [2, 3] = 5, [2, 3, 4] = 9, [3] = 3,
[3, 4] = 7, [4, 5] = 9 and [5] = 5.

Example 2:

Input: nums = [-1, -1]
Output: 2
Explanation: [-1] and [-1] are odd. [-1, -1] = -2 is even.

Example 3:

Input: nums = [0, 2, -4]
Output: 0

Constraints:

    1 <= len(nums) <= 10^5
    -1000 <= nums[i] <= 1000

    REQUIRED: O(n) time and O(1) extra space. NO loop over the start
    and end of every subarray.
"""


class Solution:
    def oddSumSubarrays(self, nums: list[int]) -> int:
        pass


sol = Solution()

print(sol.oddSumSubarrays([2, 3, 4, 5]))  # 6

# assert sol.oddSumSubarrays([2, 3, 4, 5]) == 6
# assert sol.oddSumSubarrays([-1, -1]) == 2
# assert sol.oddSumSubarrays([0, 2, -4]) == 0
# assert sol.oddSumSubarrays([7]) == 1
# assert sol.oddSumSubarrays([4]) == 0
# assert sol.oddSumSubarrays([1, 2]) == 2
# assert sol.oddSumSubarrays([2, 1]) == 2
# assert sol.oddSumSubarrays([1, 0, 1]) == 4
# assert sol.oddSumSubarrays([-3, 5, -7, 9, 0, 2, 4, 6]) == 14
# assert sol.oddSumSubarrays([1, 1, 1, 1, 1, 1, 1, 1, 1]) == 25
# assert sol.oddSumSubarrays([1] * 10 ** 5) == 2500050000
# assert sol.oddSumSubarrays([2] * 10 ** 5) == 0
# assert sol.oddSumSubarrays([1, 2] * 50000) == 2500050000
# assert sol.oddSumSubarrays([1000, -999] * 50000) == 2500050000
