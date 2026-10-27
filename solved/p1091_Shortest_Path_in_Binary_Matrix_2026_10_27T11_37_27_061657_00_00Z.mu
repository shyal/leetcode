# URL: https://leetcode.com/problems/shortest-path-in-binary-matrix/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1091. Shortest Path in Binary Matrix
#
# Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. If there is no clear path, return -1.
#
# A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)) such that:
#
# - All the visited cells of the path are 0.
# - All the adjacent cells of the path are 8-directionally connected (i.e., they are different and they share an edge or a corner).
#
# The length of a clear path is the number of visited cells of this path.
#
# Example 1:
#
# Input: grid = [[0,1],[1,0]]
# Output: 2
#
# Example 2:
#
# Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
# Output: 4
#
# Example 3:
#
# Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
# Output: -1
#
# Constraints:
#
#     n == grid.length
#     n == grid[i].length
#     1 <= n <= 100
#     grid[i][j] is 0 or 1
#
# ---
# LEETCODE: Accepted (931 ms, 21 MB)

# mu 0.13

class Solution
  def shortestPathBinaryMatrix(grid: [[int]]) -> int
    if grid[0][0] == 1
      return -1
    q = deque([(0, 0)])
    seen = set([])
    for d, (r, c) in levels(q, grid, seen=seen)
      grid[r][c] = 'x'
      if (r, c) == shape(grid, last_index=True)
        return d + 1
      for rr, cc in nbrs(grid, r, c, ALL_EIGHT)
        if (rr, cc) not in seen and grid[rr][cc] == 0
          q <- (rr, cc)
    -1

sol = Solution()

print(sol.shortestPathBinaryMatrix([[0, 1], [1, 0]]))  # 2

assert sol.shortestPathBinaryMatrix([[0, 1], [1, 0]]) == 2
assert sol.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
assert sol.shortestPathBinaryMatrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]]) == -1

assert sol.shortestPathBinaryMatrix([[0]]) == 1
assert sol.shortestPathBinaryMatrix([[1]]) == -1
assert sol.shortestPathBinaryMatrix([[0, 0], [0, 0]]) == 2
assert sol.shortestPathBinaryMatrix([[0, 1], [1, 1]]) == -1
assert sol.shortestPathBinaryMatrix([[0] * 100 for _ in 0..<100]) == 100
assert sol.shortestPathBinaryMatrix([[1] + [0] * 99] + [[0] * 100 for _ in 0..<99]) == -1
assert sol.shortestPathBinaryMatrix([[0] * 99 + [1]] + [[0] * 100 for _ in 0..<99]) == 100
assert sol.shortestPathBinaryMatrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) == 3
assert sol.shortestPathBinaryMatrix([[0] * 50 + [1] + [0] * 49 for _ in 0..<100]) == -1
assert sol.shortestPathBinaryMatrix([[0] * 100 for _ in 0..<99] + [[1] * 99 + [0]]) == 100
assert sol.shortestPathBinaryMatrix([[0] * 100 for _ in 0..<99] + [[0] * 100]) == 100
assert sol.shortestPathBinaryMatrix([[1] * 100 for _ in 0..<100]) == -1
