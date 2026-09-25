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

Built some more helpers: shape(grid, last_index=True)
"""


# mu 0.3
# def reach(grid: [[int]], k: int) -> bool
#   q, seen = deque([(0, 0)]), set()
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
    def keep(x):
        v = x if grid is None else grid[x[0]][x[1]]
        if not _holds(v, eq, lt, lte, gt, gte) or (seen is not None and x in seen):
            return False
        if seen is not None:
            seen.add(x)
        return True

    d = 0
    while q:
        popped = (q.popleft() for _ in range(len(q)))
        if grouped:
            level = [x for x in popped if keep(x)]
            if level:
                yield d, level
        else:
            for x in popped:
                if keep(x):
                    yield d, x
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
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if _holds(grid[nr][nc], eq, lt, lte, gt, gte):
                yield nr, nc


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
        grid = Grid(grid)
        q, seen = deque([(0, 0)]), set()
        for (_, c) in levels(q, grid, seen, gte=k):
            q += nbrs(grid, c)
        return shape(grid, last_index=True) in seen


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
