"""
DRILL: Fewest Cells Between
TRAINS: multi-source-bfs

Given an n x m grid of 0, 1 and 2, return the fewest 0 cells on a path from
any 1 cell to any 2 cell. Each step of a path goes to the cell above, below,
left or right. The grid holds at least one 1 and at least one 2, and some
path between them exists.

Example 1:

Input: grid = [[1, 0, 0], [0, 0, 0], [0, 0, 2]]
Output: 3
Explanation: Right, right, down, down passes three 0 cells. No path passes
fewer.

Example 2:

Input: grid = [[1, 2], [0, 0]]
Output: 0
Explanation: The 1 and the 2 touch.

Example 3:

Input: grid = [[2, 0, 1, 0, 0, 0, 2]]
Output: 1
Explanation: The 2 on the left is nearer than the 2 on the right.

Constraints:

    1 <= n, m <= 400
    grid[r][c] is 0, 1 or 2

    REQUIRED: O(n * m) time, one breadth-first search whose queue starts with
    every 1 cell, returning on the first 2 popped. NO distance table, NO
    second search.
"""


# mu 0.7
# def fewest(grid: [[int]]) -> int
#   q = deque cells(grid, eq=1)
#   seen = set()
#   for (d, pos) in levels(q, grid, seen=seen)
#     for nb in nbrs(grid, pos, eq=2)
#       if grid[nb] == 2
#         return d
#     for nb in nbrs(grid, pos, eq=0)
#       q.append(nb)

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


def levels(
    q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None
):
    bare = eq is None and lt is None and lte is None and gt is None and gte is None
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    d = 0
    while q:
        level = []
        for _ in range(len(q)):
            x = q.popleft()
            if seen is not None and x in seen:
                continue
            if not bare:
                v = x if grid is None else row(grid, x[0])[x[1]]
                if not _holds(v, eq, lt, lte, gt, gte):
                    continue
            if seen is not None:
                seen.add(x)
            if grouped:
                level.append(x)
            else:
                yield d, x
        if grouped and level:
            yield d, level
        d += 1


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
    def fewest(self, grid: list[list[int]]) -> int:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            q = deque(cells(grid, eq=1))
            seen = set()
            for (d, pos) in levels(q, grid, seen=seen):
                for nb in nbrs(grid, pos, eq=2):
                    if grid[nb] == 2:
                        return d
                for nb in nbrs(grid, pos, eq=0):
                    q.append(nb)
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.fewest([[1, 0, 0], [0, 0, 0], [0, 0, 2]]))
assert sol.fewest([[1, 0, 0], [0, 0, 0], [0, 0, 2]]) == 3
assert sol.fewest([[1, 2], [0, 0]]) == 0
assert sol.fewest([[2, 0, 1, 0, 0, 0, 2]]) == 1
assert sol.fewest([[1, 0, 0, 2]]) == 2
assert sol.fewest([[2, 0, 0, 1]]) == 2
assert sol.fewest([[1], [0], [0], [0], [2]]) == 3
assert sol.fewest([[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 2], [0, 0, 2, 2]]) == 3
assert sol.fewest([[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 2], [0, 0, 0, 2, 2]]) == 6
assert sol.fewest([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 2, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]) == 1
assert sol.fewest([[1, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1]]) == 3
assert sol.fewest([[1, 0, 2], [0, 0, 0], [2, 0, 1]]) == 1
assert sol.fewest([[1, 0, 0, 0, 0, 0, 0, 0, 0, 2]]) == 8
assert sol.fewest([[1] + [0] * 399] + [[0] * 400 for _ in range(0, 398)] + [[0] * 399 + [2]]) == 797
assert sol.fewest([[1] * 400] + [[0] * 400 for _ in range(0, 398)] + [[2] * 400]) == 398
