"""
DRILL: Range Sum Queries
TRAINS: prefix-sums

Given an integer array nums and a list of queries (l, r) - both indices
INCLUSIVE - return a list with the sum nums[l..r] for each query.

Example 1:

Input: nums = [3, -1, 4, 1, 5, 9], queries = [(0, 2), (1, 4), (3, 3)]
Output: [6, 9, 1]
Explanation:
    (0, 2) -> 3 + -1 + 4       = 6
    (1, 4) -> -1 + 4 + 1 + 5   = 9
    (3, 3) -> 1                = 1

Example 2:

Input: nums = [2, 2, 2], queries = [(0, 2)]
Output: [6]

Constraints:

    1 <= len(nums) <= 10^5
    1 <= len(queries) <= 10^5
    0 <= l <= r < len(nums)

    REQUIRED: O(n) precompute once, then O(1) per query.
    Re-summing the slice per query is the failure mode this drill exists
    to kill. len(queries) makes O(n) per query a TLE.
"""

from typing import List, Tuple


class Solution:

    def rangeSums(self, nums: List[int], queries: List[Tuple[int, int]]) -> List[int]:
        pass


sol = Solution()

print(sol.rangeSums([3, -1, 4, 1, 5, 9], [(0, 2), (1, 4), (3, 3)]))  # [6, 9, 1]

# assert sol.rangeSums([3, -1, 4, 1, 5, 9], [(0, 2), (1, 4), (3, 3)]) == [6, 9, 1]
# assert sol.rangeSums([2, 2, 2], [(0, 2)]) == [6]
# assert sol.rangeSums([5], [(0, 0)]) == [5]
# assert sol.rangeSums([1, -1, 1, -1], [(0, 3), (1, 2), (0, 0), (3, 3)]) == [0, 0, 1, -1]
