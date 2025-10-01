"""
URL: https://leetcode.com/problems/unique-paths-ii/description/

63. Unique Paths II

You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to 2 * 109.


Example 1:

Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
Explanation: There is one obstacle in the middle of the 3x3 grid above.
There are two ways to reach the bottom-right corner:
1. Right -> Right -> Down -> Down
2. Down -> Down -> Right -> Right

Example 2:

Input: obstacleGrid = [[0,1],[0,0]]
Output: 1


Constraints:

    m == obstacleGrid.length
    n == obstacleGrid[i].length
    1 <= m, n <= 100
    obstacleGrid[i][j] is 0 or 1.

"""


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        g = obstacleGrid
        dp = [1] * len(g[0])
        if 1 in g[0]:
            block = g[0].index(1)
            for i in range(len(dp)):
                if i >= block:
                    dp[i] = 0
        for i in range(1, len(g)):
            if g[i][0] == 1:
                dp[0] = 0
            for j in range(1, len(g[0])):
                dp[j] = dp[j] + dp[j - 1] if g[i][j] == 0 else 0
        return dp[-1]


sol = Solution()

assert sol.uniquePathsWithObstacles([[1]]) == 0
assert sol.uniquePathsWithObstacles([[0]]) == 1
assert sol.uniquePathsWithObstacles([[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) == 7
assert sol.uniquePathsWithObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
assert sol.uniquePathsWithObstacles([[0, 1], [0, 0]]) == 1
assert sol.uniquePathsWithObstacles([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]) == 4
