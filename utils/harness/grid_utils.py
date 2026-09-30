# grid_utils.py
#
# Grid helpers preloaded by sitecustomize: scan a grid, list a cell's
# in-bounds neighbours, test for and list the border cells, build a table
# by shape or by size, read a grid's shape, write one value or a stream of
# values into many cells, read or set a row or a column, multi-source BFS.

from collections import deque
from itertools import repeat
from typing import Any, Callable, Iterable, Iterator, List, Optional, Sequence, Tuple

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
        if in_bounds(grid, nr, nc):
            if _holds(grid[nr][nc], eq, lt, lte, gt, gte):
                yield nr, nc


def in_bounds(grid: Sequence[Sequence[Any]], r: Any, c: Optional[int] = None) -> bool:
    """True if (r, c) is a cell of grid. in_bounds(grid, p) takes the cell as
    one pair."""
    if c is None:
        r, c = r
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


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


def _spread(v: Any) -> Iterator[Any]:
    """v itself forever if it is one value, else v's items in order."""
    if isinstance(v, str) or not isinstance(v, Iterable):
        return repeat(v)
    return iter(v)


def put(grid: List[List[Any]], at: Iterable[Cell], v: Any) -> None:
    """Set grid[i][j] = v for every (i, j) in at.

    v is one value, or an iterable read once per cell in the order of at:
    put(dp, cells(dp), accumulate(...))."""
    for (i, j), x in zip(at, _spread(v)):
        grid[i][j] = x


def row(grid: Sequence[Sequence[Any]], i: int) -> List[Any]:
    """A copy of row i."""
    return list(grid[i])


def col(grid: Sequence[Sequence[Any]], j: int) -> List[Any]:
    """A copy of column j, top to bottom."""
    return [r[j] for r in grid]


def set_row(grid: List[List[Any]], i: int, v: Any) -> None:
    """Set every cell of row i to v, one value or an iterable read left to right."""
    put(grid, ((i, j) for j in range(len(grid[i]))), v)


def set_col(grid: List[List[Any]], j: int, v: Any) -> None:
    """Set every cell of column j to v, one value or an iterable read top to bottom."""
    put(grid, ((i, j) for i in range(len(grid))), v)


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
