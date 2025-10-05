"""
URL: https://leetcode.com/problems/minimum-path-sum/description/

64. Minimum Path Sum

Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.


Example 1:

Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.

Example 2:

Input: grid = [[1,2,3],[4,5,6]]
Output: 12


Constraints:

        m == grid.length
        n == grid[i].length
        1 <= m, n <= 200
        0 <= grid[i][j] <= 200
"""


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        dp = [0] * len(grid[0])
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if j > 0:
                    from_left_cost = dp[j - 1]
                    from_current_cost = grid[i][j]
                    from_top_cost = dp[j]
                    dp[j] = from_current_cost + min(
                        from_left_cost, from_top_cost if i > 0 else float("inf")
                    )
                else:
                    dp[j] += grid[i][j]
        return dp[-1]


sol = Solution()
grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
assert sol.minPathSum(grid) == 7

grid = [[1, 2, 3], [4, 5, 6]]
assert sol.minPathSum(grid) == 12

grid = [[1], [1]]
assert sol.minPathSum(grid) == 2

grid = [[1]]
assert sol.minPathSum(grid) == 1
