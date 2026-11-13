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
# name each island by its smallest cell
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # names = set
    # for each cell (r, c) that is land
      # bfs from (r, c) over all the land cells joined to it, with a fresh visited set
      # add the smallest cell that the bfs reached to names
    # return len names
    pass

sol = Solution()
