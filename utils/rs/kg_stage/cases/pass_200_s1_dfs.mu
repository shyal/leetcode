# URL: https://leetcode.com/problems/number-of-islands/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 200. Number of Islands
#
# Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.
#
# An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
#
# Example 1:
#
# Input: grid = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]
# Output: 1
#
# Example 2:
#
# Input: grid = [
#   ["1","1","0","0","0"],
#   ["1","1","0","0","0"],
#   ["0","0","1","0","0"],
#   ["0","0","0","1","1"]
# ]
# Output: 3
#
# Constraints:
#
#     m == grid.length
#     n == grid[i].length
#     1 <= m, n <= 300
#     grid[i][j] is '0' or '1'.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# Loop over every cell. When a cell is land and not visited, count one island and flood fill from it with dfs to mark the whole island visited.

# mu 0.17

class Solution
  def solve(x)
    pass

sol = Solution()
