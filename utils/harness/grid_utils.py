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


def cells(grid: Sequence[Sequence[Any]], start: int = 0) -> Iterator[Cell]:
    """Every (i, j) of grid with i >= start and j >= start, in row-major order."""
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            yield i, j


def nbrs(
    grid: Sequence[Sequence[Any]], r: int, c: int, dirs: Sequence[Cell] = CARDINALS
) -> Iterator[Cell]:
    """The cells (r + dr, c + dc) for (dr, dc) in dirs that lie on grid."""
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


def table(*dims: int, fill: Any = 0) -> List[Any]:
    """A new table of the given dimensions, every cell set to fill.

    table(n) is a list of n cells; table(m, n) is m rows of n cells, the
    rows distinct lists; table(l, m, n) nests one level deeper."""
    if len(dims) == 1:
        return [fill] * dims[0]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def like(grid: Sequence[Sequence[Any]], fill: Any = 0) -> List[List[Any]]:
    """A new table with the shape of grid, every cell set to fill."""
    return table(len(grid), len(grid[0]), fill=fill)


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
