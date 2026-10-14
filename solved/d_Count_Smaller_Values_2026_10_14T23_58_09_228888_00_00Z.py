"""
DRILL: Count Smaller Values

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
---
Learning
"""


# mu 0.10
# class Solution
#   def smallerThanEach(nums: [int]) -> [int]
#     buckets = [0] * 101
#     for v in nums
#       buckets[v] += 1
#     count = 0
#     res = {}
#     for >i, v in buckets
#       if v
#         res[i] = count
#       count += v
#     [res[i] for i in nums]
#
#

class Solution:
    def smallerThanEach(self, nums: list[int]) -> list[int]:
        buckets = [0] * 101
        for v in nums:
            buckets[v] += 1
        count = 0
        res = {}
        for i, v in enumerate(buckets):
            if v:
                res[i] = count
            count += v
        return [res[i] for i in nums]


sol = Solution()
print(sol.smallerThanEach([8, 1, 2, 2, 3]))
