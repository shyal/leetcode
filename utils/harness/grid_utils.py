# grid_utils.py
#
# Grid helpers preloaded by sitecustomize: scan a grid, list a cell's
# in-bounds neighbours, test for and list the border cells, build a table
# by shape or by size, read a grid's shape, write one value into many cells,
# multi-source BFS.

from collections import deque
from typing import Any, Callable, Iterable, Iterator, List, Sequence, Tuple

Cell = Tuple[int, int]

CARDINALS: Tuple[Cell, ...] = ((-1, 0), (0, -1), (0, 1), (1, 0))
DIAGONALS: Tuple[Cell, ...] = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ALL_EIGHT: Tuple[Cell, ...] = CARDINALS + DIAGONALS


def _holds(
    v: Any,
    eq: Any = None,
    lt: Any = None,
    lte: Any = None,
    gt: Any = None,
    gte: Any = None,
) -> bool:
    """True if v passes every comparison given: v == eq, v < lt, v <= lte,
    v > gt, v >= gte. A comparison left as None is not tested."""
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def cells(
    grid: Sequence[Sequence[Any]],
    start: int = 0,
    val: Any = None,
    eq: Any = None,
    lt: Any = None,
    lte: Any = None,
    gt: Any = None,
    gte: Any = None,
) -> Iterator[Cell]:
    """Every (i, j) of grid with i >= start and j >= start, in row-major order.
    With eq, lt, lte, gt or gte, only the cells whose value passes them all
    (see _holds). val is the old name for eq."""
    eq = val if eq is None else eq
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            if _holds(grid[i][j], eq, lt, lte, gt, gte):
                yield i, j


def nbrs(
    grid: Sequence[Sequence[Any]],
    r: int,
    c: int,
    dirs: Sequence[Cell] = CARDINALS,
    val: Any = None,
    eq: Any = None,
    lt: Any = None,
    lte: Any = None,
    gt: Any = None,
    gte: Any = None,
) -> Iterator[Cell]:
    """The cells (r + dr, c + dc) for (dr, dc) in dirs that lie on grid.
    With eq, lt, lte, gt or gte, only the cells whose value passes them all
    (see _holds). val is the old name for eq."""
    eq = val if eq is None else eq
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if _holds(grid[nr][nc], eq, lt, lte, gt, gte):
                yield nr, nc


def is_edge(grid: Sequence[Sequence[Any]], r: int, c: int) -> bool:
    """True if (r, c) lies on the first or last row or column of grid."""
    return r == 0 or c == 0 or r == len(grid) - 1 or c == len(grid[0]) - 1


def edges(grid: Sequence[Sequence[Any]]) -> Iterator[Cell]:
    """Every (i, j) on the border of grid, each once, in row-major order."""
    for i, j in cells(grid):
        if is_edge(grid, i, j):
            yield i, j


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


def shape(*seqs: Any, last_index: bool = False) -> Tuple[int, ...]:
    """The sizes of a nested list, or of several sequences side by side.

    shape(grid) follows grid[0] down while it is a list: (rows, cols, ...).
    shape(a, b) is (len(a), len(b)). With last_index, every size less one:
    the index of the last cell."""
    if len(seqs) == 1:
        dims, x = [len(seqs[0])], seqs[0]
        while dims[-1] and isinstance(x[0], list):
            x = x[0]
            dims.append(len(x))
    else:
        dims = [len(s) for s in seqs]
    return tuple(d - 1 for d in dims) if last_index else tuple(dims)


def put(grid: List[List[Any]], at: Iterable[Cell], v: Any) -> None:
    """Set grid[i][j] = v for every (i, j) in at."""
    for i, j in at:
        grid[i][j] = v


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
