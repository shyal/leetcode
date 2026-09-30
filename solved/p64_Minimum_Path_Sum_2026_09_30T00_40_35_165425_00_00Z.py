"""
URL: https://leetcode.com/problems/minimum-path-sum/description/?envType=problem-list-v2&envId=vn57k9wr

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
---
Hmm my first instinct was to reach for a BFS, but a bfs would be equivalent to
greedy, and take us down the wrong path.. 

┏━━━┳━━━┳━━━┳━━━┓
┃   ┃ 0 ┃ 1 ┃ 2 ┃
┡━━━╇━━━╇━━━╇━━━┩
│ 0 │ 1 │ 3 │ 1 │
│ 1 │ 1 │ 5 │ 1 │
│ 2 │ 4 │ 2 │ 1 │
└───┴───┴───┴───┘

┏━━━┳━━━┳━━━┳━━━┓
┃   ┃ 0 ┃ 1 ┃ 2 ┃
┡━━━╇━━━╇━━━╇━━━┩
│ 0 │ 1 │ 3 │ 1 │
│ 1 │ 1 │ 5 │ 9 │
│ 2 │ 4 │ 2 │ 1 │
└───┴───┴───┴───┘

So this is more of a memoized dfs problem.

at the starting cell, we look at the cell to the right, and below. 
so we have 2 options, 1 or 3.. but actually it's even simpler.. 
we can simply iterate through the grid using DP. 

yes the key point is: You can only move either down or right at any point in time.

┏━━━┳━━━┳━━━┳━━━┓
┃   ┃ 0 ┃ 1 ┃ 2 ┃
┡━━━╇━━━╇━━━╇━━━┩
│ 0 │ 1 │ 4 │ 5 │
│ 1 │ 2 │ 7 │ 6 │
│ 2 │ 6 │ 8 │ 7 │
└───┴───┴───┴───┘

So compute the first row and column, and for the rest, simply compute the min(above, left) + val

LEETCODE: Accepted (27 ms, 21.9 MB)
"""


# mu 0.7
# def minPathSum(grid: [[int]]) -> int
#   dp = like(grid)
#   dp[0] = [*accumulate(grid[0])]
#   p = 0
#   for i in range(len(grid))
#     p += grid[i][0]
#     dp[i][0] = p
#   for (row, col) in cells(grid)
#     if row > 0 and col > 0
#       dp[row][col] = min(dp[row-1][col], dp[row][col-1]) + grid[row][col]
#   return dp[len(dp)-1][len(dp[0])-1]

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def like(grid, fill=0):
    return table(len(grid), len(grid[0]), fill=fill)


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def cells(grid, start=0, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    eq = val if eq is None else eq
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            if _holds(grid[i][j], eq, lt, lte, gt, gte):
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
    def minPathSum(self, grid: list[list[int]]) -> int:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            dp = like(grid)
            dp[0] = [*accumulate(grid[0])]
            p = 0
            for i in range(len(grid)):
                p += grid[i][0]
                dp[i][0] = p
            for (row, col) in cells(grid):
                if row > 0 and col > 0:
                    dp[row][col] = min(dp[row - 1][col], dp[row][col - 1]) + grid[row][col]
            return dp[len(dp) - 1][len(dp[0]) - 1]
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))
assert sol.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
assert sol.minPathSum([[1, 2, 3], [4, 5, 6]]) == 12
assert sol.minPathSum([[0]]) == 0
assert sol.minPathSum([[5]]) == 5
assert sol.minPathSum([[1, 0, 1], [1, 0, 1], [1, 0, 1]]) == 2
assert sol.minPathSum([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 5
assert sol.minPathSum([[200] * 200 for _ in range(0, 200)]) == 79800
assert sol.minPathSum([[0] * 200 for _ in range(0, 200)]) == 0
assert sol.minPathSum([[1]]) == 1
assert sol.minPathSum([[1, 2], [1, 1]]) == 3
assert sol.minPathSum([[1, 2, 3]]) == 6
assert sol.minPathSum([[1], [2], [3]]) == 6
assert sol.minPathSum([[1, 1, 1, 1, 1]]) == 5
assert sol.minPathSum([[1], [1], [1], [1], [1]]) == 5
