"""
DRILL: Count Cells

Given a grid of m rows and n columns and an integer v, return the number
of cells of grid equal to v. Use cells from the harness.

Example 1:

Input: grid = [[1, 0, 2], [0, 1, 0]], v = 0
Output: 3

Example 2:

Input: grid = [[1, 0, 2], [0, 1, 0]], v = 5
Output: 0

Constraints:

    1 <= m, n <= 1000
    -10**9 <= grid[i][j], v <= 10**9

    REQUIRED: O(mn). NO nested range loops.
---
Learning mu

def count(grid: [[int]], v: int) -> int
  c = 0
  for (i, j) in cells(grid)
    if grid[i][j] == v
      c += 1
  c
"""


# mu source (current.mu), the candidate's solution. The Python
# under it is the transpiler's output, and it is what ran.
#
# def count(grid: [[int]], v: int) -> int
#   count for (i, j) in cells(grid) if grid[i][j] == v

def cells(grid, start=0):
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            yield i, j


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def count(self, grid: list[list[int]], v: int) -> int:
        grid = Grid(grid)
        return sum(1 for (i, j) in cells(grid) if (grid[i][j] == v))


sol = Solution()
print(sol.count([[1, 0, 2], [0, 1, 0]], 0))
assert sol.count([[1, 0, 2], [0, 1, 0]], 0) == 3
assert sol.count([[1, 0, 2], [0, 1, 0]], 5) == 0
assert sol.count([[7]], 7) == 1
assert sol.count([[2, 2, 2, 2]], 2) == 4
assert sol.count([[3], [3], [1]], 3) == 2
assert sol.count([[0] * 1000 for _ in range(0, 1000)], 0) == 1000000
