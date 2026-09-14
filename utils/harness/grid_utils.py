# grid_utils.py
#
# Grid helpers preloaded by sitecustomize: scan a grid, list a cell's
# in-bounds neighbours, build a table by shape or by size, multi-source BFS.

from collections import deque
from typing import Any, Callable, Iterator, List, Sequence, Tuple

Cell = Tuple[int, int]

CARDINALS: Tuple[Cell, ...] = ((-1, 0), (0, -1), (0, 1), (1, 0))
DIAGONALS: Tuple[Cell, ...] = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ALL_EIGHT: Tuple[Cell, ...] = CARDINALS + DIAGONALS


def cells(grid: Sequence[Sequence[Any]]) -> Iterator[Cell]:
    """Every (i, j) of grid in row-major order."""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            yield i, j


def nbrs(
    grid: Sequence[Sequence[Any]], r: int, c: int, dirs: Sequence[Cell] = CARDINALS
) -> Iterator[Cell]:
    """The cells (r + dr, c + dc) for (dr, dc) in dirs that lie on grid."""
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


def table(m: int, n: int, fill: Any = 0) -> List[List[Any]]:
    """A new m by n table, every cell set to fill; rows are distinct lists."""
    return [[fill] * n for _ in range(m)]


def like(grid: Sequence[Sequence[Any]], fill: Any = 0) -> List[List[Any]]:
    """A new table with the shape of grid, every cell set to fill."""
    return table(len(grid), len(grid[0]), fill)


def grid_bfs(
    grid: Sequence[Sequence[Any]],
    sources: Sequence[Cell],
    ok: Callable[[Any], bool] = lambda v: True,
    dirs: Sequence[Cell] = CARDINALS,
) -> List[List[int]]:
    """Steps from the nearest source to every cell; -1 where none reaches.

    A cell is entered only if ok(grid[cell]) holds. Sources are entered
    unconditionally at distance 0.
    """
    dist = like(grid, -1)
    q = deque(sources)
    for r, c in sources:
        dist[r][c] = 0
    while q:
        r, c = q.popleft()
        for nr, nc in nbrs(grid, r, c, dirs):
            if dist[nr][nc] == -1 and ok(grid[nr][nc]):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
