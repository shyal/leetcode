"""
DRILL: Kth Smallest Bounded Value
TRAINS: counting-sort-buckets

Given an integer array nums whose values all lie between 0 and 100
inclusive, and an integer k, return the kth smallest value of nums,
counting duplicates. The value k is 1-based, so k = 1 asks for the
minimum and k = len(nums) asks for the maximum.

Example 1:

Input: nums = [9, 3, 6, 3, 9, 1], k = 4
Output: 6
Explanation: in non-decreasing order the values are 1, 3, 3, 6, 9, 9
and the 4th is 6.

Example 2:

Input: nums = [4, 4, 4], k = 3
Output: 4

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 100
    1 <= k <= len(nums)

    REQUIRED: O(n + 100) time and O(100) extra space. NO sort(), NO
    sorted(), NO heapq, and you must NOT build the sorted array.
    Materialising all n values in order to read one of them is the
    failure mode this drill exists to kill.
"""

from typing import List


class Solution:

    def kthSmallest(self, nums: List[int], k: int) -> int:
        pass


sol = Solution()

print(sol.kthSmallest([9, 3, 6, 3, 9, 1], 4))  # 6

# assert sol.kthSmallest([9, 3, 6, 3, 9, 1], 4) == 6
# assert sol.kthSmallest([4, 4, 4], 3) == 4
# assert sol.kthSmallest([9, 3, 6, 3, 9, 1], 1) == 1
# assert sol.kthSmallest([9, 3, 6, 3, 9, 1], 6) == 9
# assert sol.kthSmallest([9, 3, 6, 3, 9, 1], 3) == 3
# assert sol.kthSmallest([100, 0], 2) == 100
# assert sol.kthSmallest([5], 1) == 5
