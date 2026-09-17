import inspect
import shutil
import sys
from bisect import bisect_left
from typing import Any, Callable, Optional

from rich import print

PAIRS = (("left", "right"), ("low", "high"), ("lo", "hi"))

TRUE_MARK = "[bold green]✓[/bold green]"
FALSE_MARK = "[bold red]✗[/bold red]"
MID_MARK = "[bold yellow]▼[/bold yellow]"
IN_RANGE = "[cyan]█[/cyan]"
DROPPED = "[dim]·[/dim]"


def _ticks(lo: Any, hi: Any, width: int) -> str:
    """One row of numbers spanning [lo, hi] over `width` columns."""
    span = hi - lo
    row = [" "] * width
    if span <= 0:
        s = str(lo)
        row[width // 2 : width // 2 + len(s)] = s
        return "".join(row[:width])
    if isinstance(lo, int) and isinstance(hi, int) and span <= 20:
        values = list(range(lo, hi + 1))
    else:
        n = max(2, min(width // 10, 11))
        values = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    labels = []
    for v in values:
        s = str(int(v)) if isinstance(lo, int) else f"{v:.2f}"
        pos = int((v - lo) / span * (width - 1))
        labels.append((min(pos, width - len(s)), s))
    placed = [labels[0], labels[-1]]
    for pos, s in labels[1:-1]:
        if all(pos + len(s) < q or pos > q + len(t) for q, t in placed):
            placed.append((pos, s))
    for pos, s in placed:
        for i, ch in enumerate(s):
            row[pos + i] = ch
    return "".join(row)


def _record(calls: list, f: Callable, name: str) -> Callable:
    def wrapped(*a: Any, **k: Any) -> Any:
        r = f(*a, **k)
        calls.append((a[0] if a else None, r, name))
        return r

    return wrapped


class _Viz:
    def __init__(self, width: int) -> None:
        self.width = width
        self.lo0: Any = None
        self.hi0: Any = None
        self.names: Optional[tuple] = None
        self.pending: Optional[tuple] = None
        self.calls: list = []
        self.seen = 0
        self.step = 0

    def col(self, v: Any) -> int:
        span = self.hi0 - self.lo0
        if span <= 0:
            return self.width // 2
        return int((v - self.lo0) / span * (self.width - 1))

    def flush(self) -> None:
        if self.pending is None:
            return
        lo, hi, mid = self.pending
        verdict, name = None, "ok"
        for x, r, n in self.calls[self.seen :]:
            if x == mid:
                verdict, name = r, n
        self.seen = len(self.calls)
        mark = MID_MARK
        if isinstance(verdict, bool):
            mark = TRUE_MARK if verdict else FALSE_MARK
        self.step += 1
        row = []
        cl, cr, cm = self.col(lo), self.col(hi), self.col(mid)
        for c in range(self.width):
            if c == cm:
                row.append(mark)
            elif cl <= c <= cr:
                row.append(IN_RANGE)
            else:
                row.append(DROPPED)
        a, b, m = self.names or ("lo", "hi", "mid")
        ok = "" if verdict is None else f"  {name}({mid}) = {verdict}"
        print("".join(row))
        print(
            f"[dim]step {self.step:>2}[/dim]  "
            f"[cyan]{a}={lo}[/cyan]  [cyan]{b}={hi}[/cyan]  "
            f"[yellow]{m}={mid}[/yellow]{ok}"
        )
        self.pending = None

    def _detect(self, loc: dict) -> None:
        for a, b in PAIRS:
            if a in loc and b in loc:
                self.names = (a, b, self._mid_name(loc, a, b))
                return

    @staticmethod
    def _mid_name(loc: dict, a: str, b: str) -> Optional[str]:
        if "mid" in loc:
            return "mid"
        lo, hi = loc[a], loc[b]
        if not isinstance(lo, int) or not isinstance(hi, int):
            return None
        mids = {(lo + hi) // 2, (lo + hi + 1) // 2}
        for k, v in loc.items():
            if k not in (a, b) and isinstance(v, int) and v in mids:
                return k
        return None

    def observe(self, loc: dict) -> None:
        if self.names is None or self.names[2] is None:
            self._detect(loc)
            if self.names is None or self.names[2] is None:
                return
        a, b, m = self.names
        if a not in loc or b not in loc or m not in loc:
            return
        lo, hi, mid = loc[a], loc[b], loc[m]
        if lo > hi or abs(mid - (lo + hi) / 2) > 0.5:
            return
        state = (lo, hi, mid)
        if state == self.pending:
            return
        if self.lo0 is None:
            self.lo0, self.hi0 = lo, hi
            print(_ticks(self.lo0, self.hi0, self.width))
        self.flush()
        self.pending = state

    def finish(self, result: Any) -> None:
        self.flush()
        if self.lo0 is None:
            return
        c = self.col(result) if isinstance(result, (int, float)) else None
        row = [DROPPED] * self.width
        if c is not None and 0 <= c < self.width:
            row[c] = "[bold magenta]★[/bold magenta]"
        print("".join(row))
        print(f"[bold magenta]return {result!r}[/bold magenta]")


def viz_binary_search(func: Optional[Callable] = None, width: Optional[int] = None):
    """Trace a binary search: one bar per step, mid marked ✓/✗ by ok(mid)."""
    if width is None:
        width = min(100, shutil.get_terminal_size().columns)
    if callable(func):
        return viz_binary_search(width=width)(func)

    def decorator(f: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            viz = _Viz(width)
            bound = inspect.signature(f).bind(*args, **kwargs)
            for name, v in bound.arguments.items():
                if callable(v):
                    bound.arguments[name] = _record(viz.calls, v, name)
            args, kwargs = bound.args, bound.kwargs

            def trace(frame: Any, event: str, arg: Any) -> Any:
                if frame.f_code == f.__code__:
                    if event == "line":
                        viz.observe(frame.f_locals)
                    return trace
                back = frame.f_back
                if back is None or back.f_code != f.__code__:
                    return None
                if event == "return" and viz.pending is not None:
                    mid = viz.pending[2]
                    if any(v is mid for v in frame.f_locals.values()):
                        viz.calls.append((mid, arg, frame.f_code.co_name))
                return trace

            old = sys.gettrace()
            sys.settrace(trace)
            try:
                result = f(*args, **kwargs)
            finally:
                sys.settrace(old)
            viz.finish(result)
            return result

        return wrapper

    return decorator


def first_true(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi] with ok(x) True; ok is False then True.

    Returns hi + 1 when ok is False on the whole range."""
    return lo + bisect_left(range(lo, hi + 1), True, key=ok)


def last_true(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Largest x in [lo, hi] with ok(x) True; ok is True then False.

    Returns lo - 1 when ok is False on the whole range."""
    return first_true(lo, hi, lambda x: not ok(x)) - 1


def first_false(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi] with ok(x) False; ok is True then False.

    Returns hi + 1 when ok is True on the whole range."""
    return first_true(lo, hi, lambda x: not ok(x))


def last_false(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Largest x in [lo, hi] with ok(x) False; ok is False then True.

    Returns lo - 1 when ok is True on the whole range."""
    return first_true(lo, hi, ok) - 1
