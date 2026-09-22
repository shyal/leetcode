# counter_utils.py
#
# A Counter that drops a key the moment its count reaches 0, so `len(m)`
# is the number of distinct keys present and `k in m` means m[k] != 0.

from collections import Counter
from typing import Any


class Multiset(Counter[Any]):
    """A Counter whose keys vanish when their count hits 0.

    `m[k] += 1` and `m[k] -= 1` are the whole interface. With a plain
    Counter, `m[k] -= 1` leaves the key behind at 0, so `len(m)` and
    `k in m` stop meaning what a sliding window needs them to mean.
    Negative counts are kept: only an exact 0 deletes."""

    def __setitem__(self, key: Any, value: Any) -> None:
        if value == 0:
            self.pop(key, None)
        else:
            super().__setitem__(key, value)

    def update(self, iterable: Any = None, /, **kwds: Any) -> None:
        # Counter.update on an empty Counter is a bare dict.update, which
        # skips __setitem__; the pass below catches the zeros it let in.
        super().update(iterable, **kwds)
        for key in [k for k, v in self.items() if v == 0]:
            del self[key]
