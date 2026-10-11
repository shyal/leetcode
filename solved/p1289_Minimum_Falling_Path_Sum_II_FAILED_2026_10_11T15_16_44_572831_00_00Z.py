"""
URL: https://leetcode.com/problems/minimum-falling-path-sum-ii/description/?envType=problem-list-v2&envId=vn57k9wr

1289. Minimum Falling Path Sum II

Given an n x n integer matrix grid, return the minimum sum of a falling path with non-zero shifts.

A falling path with non-zero shifts is a choice of exactly one element from each row of grid such that no two elements chosen in adjacent rows are in the same column.

Example 1:

Input: grid = [[1,2,3],[4,5,6],[7,8,9]]
Output: 13
Explanation:
The possible falling paths are:
[1,5,9], [1,5,7], [1,6,7], [1,6,8],
[2,4,8], [2,4,9], [2,6,7], [2,6,8],
[3,4,8], [3,4,9], [3,5,7], [3,5,9]
The falling path with the smallest sum is [1,5,7], so the answer is 13.

Example 2:

Input: grid = [[7]]
Output: 7

Constraints:

    n == grid.length == grid[i].length
    1 <= n <= 200
    -99 <= grid[i][j] <= 99
---
Hmm the question is, bfs or explore the whole space with memoization?


[1,2,3]
[4,5,6]
[7,8,9]

what could be interesting is sorting the rows, and forbidding using the same index
but that's really just an toptimization, and likely not required
def minFallingPathSum(grid: [[int]]) -> int
  @cache
  def helper(row, col)
    print('row', row, 'col', col)
    res = inf
    here = grid[row][col]
    print("   here is: ", here)
    for (i, j) in [[1, -1], [1, 1]]
      ii, jj = row + i, col + j
      if in_bounds(grid, ii, jj)
        res = min(helper(ii, jj), res)
    result = here + (res if res != inf else 0)
    result
  min(helper(0, col) for col in range(len(grid[0])))

I think i'm solving the wrong question. I can pick any col, just not the one
right below where we are.

def minFallingPathSum(grid: [[int]]) -> int
  @cache
  def helper(row, col)
    print('row', row, 'col', col)
    res = inf
    here = grid[row][col]
    print("   here is: ", here)
    for (i, j) in [[1, 0], [1, 1], [1, 2]]
      ii, jj = row + i, col + j
      if in_bounds(grid, ii, jj)
        if grid[ii][jj][0] != col
          res = min(helper(ii, jj), res)
    result = here[1] + (res if res != inf else 0)
    result
  for i in 0..<len(grid)
    grid[i] = [*enumerate(grid[i])]
    grid[i].sort(key=x -> x[1])
  print(grid)
  min(helper(0, col) for col in range(len(grid[0])))

ok so this solution works fine, but it's a TLE:


def minFallingPathSum(grid: [[int]]) -> int
  @cache
  def helper(row, col)
    res = inf
    here = grid[row][col]
    for (ii, jj) in [[row + 1, col] for col in range(len(grid[0]))]
      if in_bounds(grid, ii, jj) and jj != col
        res = min(helper(ii, jj), res)
    result = here + (res if res != inf else 0)
    result
  min(helper(0, col) for col in range(len(grid[0])))

so the sorting solution is correct, but hard to implement:
"""


# mu 0.7
# def minFallingPathSum(grid: [[int]]) -> int
#   @cache
#   def helper(row, col)
#     print('row', row, 'col', col)
#     res = inf
#     here = grid[row][col]
#     print("   here is: ", here)
#     for (i, j) in [[1, 0], [1, 1], [1, -1]]
#       ii, jj = row + i, col + j
#       if in_bounds(grid, ii, jj)
#         if grid[ii][jj][0] != col
#           res = min(helper(ii, jj), res)
#     result = here[1] + (res if res != inf else 0)
#     result
#   for i in 0..<len(grid)
#     grid[i] = [*enumerate(grid[i])]
#     grid[i].sort(key=x -> x[1])
#   print(grid)
#   tabulate(grid)
#   min(helper(0, col) for col in range(min(len(grid[0]), 2)))

from math import inf


def in_bounds(grid, r, c=None):
    if c is None:
        r, c = r
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


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
    def minFallingPathSum(self, grid: list[list[int]]) -> int:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            @cache
            def helper(row, col):
                print('row', row, 'col', col)
                res = inf
                here = grid[row][col]
                print("   here is: ", here)
                for (i, j) in [[1, 0], [1, 1], [1, -1]]:
                    ii, jj = row + i, col + j
                    if in_bounds(grid, ii, jj):
                        if grid[ii][jj][0] != col:
                            res = min(helper(ii, jj), res)
                result = here[1] + (res if res != inf else 0)
                return result
            for i in range(0, len(grid)):
                grid[i] = [*enumerate(grid[i])]
                grid[i].sort(key=lambda x: x[1])
            print(grid)
            tabulate(grid)
            return min(helper(0, col) for col in range(min(len(grid[0]), 2)))
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.minFallingPathSum([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
_l, _r = sol.minFallingPathSum([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 13
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFallingPathSum([[7]]), 7
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFallingPathSum([[0]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFallingPathSum([[1, 1], [1, 1]]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFallingPathSum([[1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFallingPathSum([[1, 2], [2, 1]]), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"


# FAILED: walked away after 40m 44s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
