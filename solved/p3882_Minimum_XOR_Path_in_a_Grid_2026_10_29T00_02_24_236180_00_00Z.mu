# URL: https://leetcode.com/problems/minimum-xor-path-in-a-grid/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3882. Minimum XOR Path in a Grid
#
# You are given a 2D integer array grid of size m * n.
#
# You start at the top-left cell (0, 0) and want to reach the bottom-right cell (m - 1, n - 1).
#
# At each step, you may move either right or down.
#
# The cost of a path is defined as the bitwise XOR of all the values in the cells along that path, including the start and end cells.
#
# Return the minimum possible XOR value among all valid paths from (0, 0) to (m - 1, n - 1).
#
# Example 1:
#
# Input: grid = [[1,2],[3,4]]
# Output: 6
# Explanation:
# There are two valid paths:
# (0, 0) → (0, 1) → (1, 1) with XOR: 1 XOR 2 XOR 4 = 7
# (0, 0) → (1, 0) → (1, 1) with XOR: 1 XOR 3 XOR 4 = 6
# The minimum XOR value among all valid paths is 6.
#
# Example 2:
#
# Input: grid = [[6,7],[5,8]]
# Output: 9
# Explanation:
# There are two valid paths:
# (0, 0) → (0, 1) → (1, 1) with XOR: 6 XOR 7 XOR 8 = 9
# (0, 0) → (1, 0) → (1, 1) with XOR: 6 XOR 5 XOR 8 = 11
# The minimum XOR value among all valid paths is 9.
#
# Example 3:
#
# Input: grid = [[2,7,5]]
# Output: 0
# Explanation:
# There is only one valid path:
# (0, 0) → (0, 1) → (0, 2) with XOR: 2 XOR 7 XOR 5 = 0
# The XOR value of this path is 0, which is the minimum possible.
#
# Constraints:
#
#     1 <= m == grid.length <= 1000
#     1 <= n == grid[i].length <= 1000
#     m * n <= 1000
#     0 <= grid[i][j] <= 1023
#
# ---
# learning: nothing fragile. just can't intuit that we needed to cache
# the set of every xor that reaches this cell

# mu 0.13

class Solution
  def minCost(grid: [[int]]) -> int
    memo f(i, j) =
      | i == 0 and j == 0 -> {grid[0][0]}
      | i == 0            -> {grid[i][j] ^ x for x in f(i, j - 1)}
      | j == 0            -> {grid[i][j] ^ x for x in f(i - 1, j)}
      | else              -> {grid[i][j] ^ x for x in f(i - 1, j) | f(i, j - 1)}
    min(f(*shape(grid, last_index=true)))

sol = Solution()

print(sol.minCost([[1, 2], [3, 4]]))  # 6

assert sol.minCost([[1, 2], [3, 4]]) == 6
assert sol.minCost([[6, 7], [5, 8]]) == 9
assert sol.minCost([[2, 7, 5]]) == 0
assert sol.minCost([[0]]) == 0
assert sol.minCost([[1023]]) == 1023
assert sol.minCost([[1, 1, 1, 1]]) == 0
assert sol.minCost([[1], [1], [1], [1]]) == 0
assert sol.minCost([[0, 0, 0], [0, 0, 0]]) == 0
assert sol.minCost([[5, 5], [5, 5]]) == 5
assert sol.minCost([[0, 1023], [1023, 0]]) == 1023
assert sol.minCost([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 1
assert sol.minCost([[10]]) == 10
assert sol.minCost([[1000, 1000]]) == 0
assert sol.minCost([[0], [1023]]) == 1023
assert sol.minCost([[1, 2, 4, 8, 16]]) == 31
