"""
DRILL: Sort Bounded Values
TRAINS: counting-sort-buckets

Given an integer array nums whose values all lie between 0 and 100
inclusive, return the same values in non-decreasing order.

Example 1:

Input: nums = [1, 3, 6, 9, 9, 3, 5, 9]
Output: [1, 3, 3, 5, 6, 9, 9, 9]
Explanation: the values tallied by value are

    value  1 2 3 4 5 6 7 8 9
    count  1 0 2 0 1 1 0 0 3

and reading that tally left to right, each value repeated count times,
is the output.

Example 2:

Input: nums = [100, 0, 100]
Output: [0, 100, 100]

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 100

    REQUIRED: O(n + 100) time. NO sort(), NO sorted(), NO heapq, NO
    comparison of one element of nums against another. Reaching for a
    comparison sort when the value domain is tiny is the failure mode
    this drill exists to kill.
"""

from typing import List


class Solution:

    def sortBounded(self, nums: List[int]) -> List[int]:
        pass


sol = Solution()

print(sol.sortBounded([1, 3, 6, 9, 9, 3, 5, 9]))  # [1, 3, 3, 5, 6, 9, 9, 9]

# assert sol.sortBounded([1, 3, 6, 9, 9, 3, 5, 9]) == [1, 3, 3, 5, 6, 9, 9, 9]
# assert sol.sortBounded([100, 0, 100]) == [0, 100, 100]
# assert sol.sortBounded([7]) == [7]
# assert sol.sortBounded([0, 0, 0]) == [0, 0, 0]
# assert sol.sortBounded([5, 4, 3, 2, 1, 0]) == [0, 1, 2, 3, 4, 5]
# assert sol.sortBounded([50, 50, 49, 51]) == [49, 50, 50, 51]
