"""
EPI 17.7 Compute the maximum water trapped by a pair of vertical lines

Given a list heights, where heights[i] is the height of a vertical line at
x = i, return the largest amount of water that two of the lines can hold
with the x-axis. Lines i < j hold min(heights[i], heights[j]) * (j - i).
Return 0 when there are fewer than two lines.

Example 1:

Input: heights = [3, 1, 4, 2, 5, 1, 3]
Output: 18
Explanation: lines 0 and 6 have height 3 and are 6 apart. Lines 2 and 4
are taller, but hold only 4 * 2 = 8.

Example 2:

Input: heights = [1, 1]
Output: 1

Example 3:

Input: heights = [5]
Output: 0

Constraints:

    0 <= len(heights) <= 10^5
    0 <= heights[i] <= 10^4

    REQUIRED: O(n) time and O(1) extra space for n lines.
"""


class Solution:
    def get_max_trapped_water(self, heights: list[int]) -> int:
        pass


sol = Solution()

print(sol.get_max_trapped_water([3, 1, 4, 2, 5, 1, 3]))  # 18

# assert sol.get_max_trapped_water([3, 1, 4, 2, 5, 1, 3]) == 18
# assert sol.get_max_trapped_water([1, 1]) == 1
# assert sol.get_max_trapped_water([5]) == 0
# assert sol.get_max_trapped_water([]) == 0
# assert sol.get_max_trapped_water([0, 0]) == 0
# assert sol.get_max_trapped_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
# assert sol.get_max_trapped_water([2, 3, 10, 5, 7, 8, 9]) == 36
# assert sol.get_max_trapped_water([6, 1, 1, 1, 1, 6]) == 30
# assert sol.get_max_trapped_water([1, 2, 1]) == 2
# assert sol.get_max_trapped_water([1, 100, 100, 1]) == 100
# assert sol.get_max_trapped_water([4, 3, 2, 1, 4]) == 16
# assert sol.get_max_trapped_water([10000] * 100000) == 999990000
# assert sol.get_max_trapped_water(list(range(1, 100001))) == 2500000000
# assert sol.get_max_trapped_water(list(range(100000, 0, -1))) == 2500000000
