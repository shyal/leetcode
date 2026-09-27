"""
DRILL: Neighbour Counts

Given a grid of m rows and n columns, return a table of the same shape
where each cell holds the number of cardinal neighbours of that cell that
lie on the grid. Use like, cells and nbrs from the harness.

Example 1:

Input: grid = [[1, 0, 2], [0, 1, 0]]
Output: [[2, 3, 2], [2, 3, 2]]

Example 2:

Input: grid = [[1]]
Output: [[0]]

Example 3:

Input: grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
Output: [[2, 3, 2], [3, 4, 3], [2, 3, 2]]

Constraints:

    1 <= m, n <= 1000

    REQUIRED: O(mn). NO rows that share one list, NO if per offset.
"""


# mu 0.6
# def neighbour_counts(grid: [[int]]) -> [[int]]
#   ret res = like grid
#   for (i, j) in cells grid
#     res[i][j] = len nbrs(grid, i, j)

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


CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def nbrs(
    grid, r, c=None, dirs=CARDINALS, val=None, eq=None, lt=None, lte=None, gt=None, gte=None
):
    """On-grid cells next to (r, c): up, left, right, down. nbrs(grid, p)
    takes the cell as one pair. With eq, lt, lte, gt or gte, only the cells
    whose value passes them all. val is the old name for eq."""
    if c is None:
        r, c = r
    eq = val if eq is None else eq
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    m, n = len(grid), len(row(grid, 0))
    if dirs is CARDINALS:
        out = []
        if r > 0:
            out.append((r - 1, c))
        if c > 0:
            out.append((r, c - 1))
        if c + 1 < n:
            out.append((r, c + 1))
        if r + 1 < m:
            out.append((r + 1, c))
    else:
        out = [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < m and 0 <= c + dc < n]
    if eq is None and lt is None and lte is None and gt is None and gte is None:
        return out
    return [(i, j) for i, j in out if _holds(row(grid, i)[j], eq, lt, lte, gt, gte)]


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
    def neighbour_counts(self, grid: list[list[int]]) -> list[list[int]]:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            res = like(grid)
            for (i, j) in cells(grid):
                res[i][j] = len(nbrs(grid, i, j))
            return res
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.neighbour_counts([[1, 0, 2], [0, 1, 0]]))
assert sol.neighbour_counts([[1, 0, 2], [0, 1, 0]]) == [[2, 3, 2], [2, 3, 2]]
assert sol.neighbour_counts([[1]]) == [[0]]
assert sol.neighbour_counts([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == [[2, 3, 2], [3, 4, 3], [2, 3, 2]]
assert sol.neighbour_counts([[0, 0, 0, 0]]) == [[1, 2, 2, 1]]
assert sol.neighbour_counts([[0], [0], [0]]) == [[1], [2], [1]]
t = sol.neighbour_counts([[0, 0], [0, 0]])
t[0][0] = 9
assert t == [[9, 2], [2, 2]]
