"""
DRILL: Reach The Far Corner
TRAINS: graph-bfs-shortest

Given an n x m grid of integers and an integer k, return True when you can
walk from cell (0, 0) to cell (n - 1, m - 1). Each move goes to the cell
above, below, left or right. You may stand only on cells whose value is at
least k, and that includes the first and the last cell.

Example 1:

Input: grid = [[3, 1, 2], [3, 0, 2], [3, 3, 3]], k = 3
Output: True
Explanation: Down the left column, then along the bottom row.

Example 2:

Input: grid = [[4, 1], [1, 4]], k = 2
Output: False
Explanation: Both corners hold 4, but no move goes diagonally.

Example 3:

Input: grid = [[1, 5], [5, 5]], k = 2
Output: False
Explanation: Cell (0, 0) holds 1, so you cannot stand on it.

Constraints:

    1 <= n, m <= 400
    0 <= grid[r][c] <= 10^6
    0 <= k <= 10^6

    REQUIRED: O(n * m) time, one breadth-first search from (0, 0). A cell
    below k must never be entered, the first cell included. NO recursion.
---
Learning
"""


# mu 0.4
# def reach(grid: [[int]], k: int) -> bool
#   q = deque([(0, 0)])
#   seen = set()
#   for (_, c) in levels(q, grid, seen, gte=k)
#     q += nbrs(grid, c)
#   shape(grid, last_index=True) in seen

def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


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


def shape(*seqs, last_index=False):
    if len(seqs) == 1:
        dims, x = [len(seqs[0])], seqs[0]
        while dims[-1] and isinstance(x[0], list):
            x = x[0]
            dims.append(len(x))
    else:
        dims = [len(s) for s in seqs]
    return tuple(d - 1 for d in dims) if last_index else tuple(dims)


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
    def reach(self, grid: list[list[int]], k: int) -> bool:
        _in_grid, grid = grid, Grid(grid)
        _w_grid = grid
        try:
            q = deque([(0, 0)])
            seen = set()
            for (_, c) in levels(q, grid, seen, gte=k):
                q += nbrs(grid, c)
            return shape(grid, last_index=True) in seen
        finally:
            _in_grid[:] = _w_grid


sol = Solution()
print(sol.reach([[3, 1, 2], [3, 0, 2], [3, 3, 3]], 3))
assert sol.reach([[3, 1, 2], [3, 0, 2], [3, 3, 3]], 3) is True
assert sol.reach([[3, 1, 2], [3, 0, 2], [3, 3, 3]], 4) is False
assert sol.reach([[4, 1], [1, 4]], 2) is False
assert sol.reach([[1, 5], [5, 5]], 2) is False
assert sol.reach([[5, 5], [5, 1]], 2) is False
assert sol.reach([[7]], 7) is True
assert sol.reach([[6]], 7) is False
assert sol.reach([[0, 0], [0, 0]], 0) is True
assert sol.reach([[2, 2, 2, 2, 2]], 2) is True
assert sol.reach([[2, 2, 1, 2, 2]], 2) is False
assert sol.reach([[5, 5, 5], [0, 0, 5], [5, 5, 5], [5, 0, 0], [5, 5, 5]], 5) is True
assert sol.reach([[5, 5, 5], [0, 0, 5], [5, 5, 4], [5, 0, 0], [5, 5, 5]], 5) is False
assert sol.reach([[9] * 400 for _ in range(0, 400)], 9) is True
assert sol.reach([[9] * 400 for _ in range(0, 399)] + [[9] * 399 + [8]], 9) is False
