"""
DRILL: Neighbour Values

Given a grid of m rows and n columns and a cell (r, c), return the values
of the cardinal neighbours of (r, c) that lie on the grid, in the order
up, left, right, down. Use nbrs from the harness.

Example 1:

Input: grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], r = 1, c = 1
Output: [2, 4, 6, 8]

Example 2:

Input: grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], r = 0, c = 0
Output: [2, 4]
Explanation: (-1, 0) and (0, -1) are off the grid.

Example 3:

Input: grid = [[1]], r = 0, c = 0
Output: []

Constraints:

    1 <= m, n <= 1000
    0 <= r < m
    0 <= c < n

    REQUIRED: one pass over the four offsets. NO if per offset, NO
    try/except around an index.
"""


# mu 0.12
# class Solution
#   def neighbour_values(grid: [[int]], r: int, c: int) -> [int]
#     [*nbrs(grid, r, c)]

CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (eq is None or v == eq) and (lt is None or v < lt) and (lte is None or v <= lte) and (gt is None or v > gt) and (gte is None or v >= gte)


def in_bounds(grid, r, c=None):
    if c is None:
        (r, c) = r
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def nbrs(grid, r, c=None, dirs=CARDINALS, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    if c is None:
        (r, c) = r
    eq = val if eq is None else eq
    for (dr, dc) in dirs:
        (nr, nc) = (r + dr, c + dc)
        if in_bounds(grid, nr, nc):
            if _holds(grid[nr][nc], eq, lt, lte, gt, gte):
                yield (nr, nc)


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
    def neighbour_values(self, grid: list[list[int]], r: int, c: int) -> list[int]:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            return [*nbrs(grid, r, c)]
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.neighbour_values([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1))
