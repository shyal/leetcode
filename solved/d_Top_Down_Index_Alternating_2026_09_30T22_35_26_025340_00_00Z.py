"""
DRILL: Top Down Index Alternating
TRAINS: index-conversion

Given an integer n, return the n x n grid numbered 0 to n * n - 1,
starting at the top-left cell. The top row is filled left to right, the
row below it right to left, and the direction alternates on every row
down. The cell [r, c] is the r-th row from the top and the c-th column
from the left, both counted from 0.

Example 1:

Input: n = 4
Output: [[0, 1, 2, 3], [7, 6, 5, 4], [8, 9, 10, 11], [15, 14, 13, 12]]
Explanation: the grid is numbered

     0  1  2  3
     7  6  5  4
     8  9 10 11
    15 14 13 12

Example 2:

Input: n = 3
Output: [[0, 1, 2], [5, 4, 3], [6, 7, 8]]
Explanation: the grid is numbered

    0 1 2
    5 4 3
    6 7 8

Example 3:

Input: n = 2
Output: [[0, 1], [3, 2]]

Constraints:

    2 <= n <= 20

    REQUIRED: keep the stub's loop over the cells. Each cell gets its
    number by O(1) arithmetic on n, r and c. NO counter carried from one
    cell to the next. The parity test is on r: the top row is even.
"""


# mu 0.7
# def numbered(n: int) -> [[int]]
#   grid = table(n, n)
#   for (r, c) in cells(grid)
#     grid[r][c] = r * n + (c if r % 2 == 0 else (n - 1 - c))
#   return grid

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


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


class Solution:
    def numbered(self, n: int) -> list[list[int]]:
        grid = table(n, n)
        for (r, c) in cells(grid):
            grid[r][c] = r * n + (c if r % 2 == 0 else (n - 1 - c))
        return grid


sol = Solution()
print(sol.numbered(4))
