"""
Given a sorted integer array nums and an integer x, return the number of
index pairs (i, j) such that i < j and nums[i] + nums[j] <= x.

Example 1:

Input: nums = [0, 1, 4, 4, 5, 7], x = 6
Output: 7
Explanation: The pairs are (0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3)
and (1, 4).

Example 2:

Input: nums = [-3, -1, 2, 5], x = 1
Output: 3
Explanation: The pairs are (0, 1), (0, 2) and (1, 2).

Example 3:

Input: nums = [2, 2, 2, 2], x = 3
Output: 0

Constraints:

    1 <= len(nums) <= 10^5
    -10^9 <= nums[i], x <= 10^9
    nums is sorted in non-decreasing order.

    REQUIRED: O(n) time, O(1) extra space. NO loop over pairs. NO bisect.
"""


class Solution:
    def pairsAtMost(self, nums: list[int], x: int) -> int:
        pass


sol = Solution()

print(sol.pairsAtMost([0, 1, 4, 4, 5, 7], 6))  # 7

# assert sol.pairsAtMost([0, 1, 4, 4, 5, 7], 6) == 7
# assert sol.pairsAtMost([-3, -1, 2, 5], 1) == 3
# assert sol.pairsAtMost([2, 2, 2, 2], 3) == 0
# assert sol.pairsAtMost([0, 1, 4, 4, 5, 7], 2) == 1
# assert sol.pairsAtMost([5], 100) == 0
# assert sol.pairsAtMost([1, 2], 3) == 1
# assert sol.pairsAtMost([1, 2], 2) == 0
# assert sol.pairsAtMost([2, 2, 2, 2], 4) == 6
# assert sol.pairsAtMost([1, 2, 3, 4, 5], 100) == 10
# assert sol.pairsAtMost([1, 2, 3, 4, 5], 2) == 0
# assert sol.pairsAtMost([1, 2, 3, 4, 5], 5) == 4
# assert sol.pairsAtMost([-5, -4, -3], -8) == 2
# assert sol.pairsAtMost([-(10**9), 10**9], 0) == 1
# assert sol.pairsAtMost([10**9, 10**9, 10**9], 2 * 10**9) == 3
# assert sol.pairsAtMost([0] * 100000, 0) == 4999950000
# assert sol.pairsAtMost(list(range(100000)), 1) == 1
