"""heapq with the order reversed.

    maxheappush, maxheappop, maxheapify, maxheappushpop, maxheapreplace, maxheappeek

Each function is its heapq namesake with the prefix max, same signature, and
the largest item comes out first. Items can be anything heapq accepts, tuples
included: there is no negation, so no minus sign to remember.

The list holds each item inside a small wrapper whose `<` is `>`. maxheappop
unwraps it; h[0] does not, so peek with maxheappeek(h), not h[0].

The harness preloads these names, so a solve calls them bare.
"""

import heapq
from typing import Any


class _Rev:
    __slots__ = ("item",)

    def __init__(self, item: Any):
        self.item = item

    def __lt__(self, other: "_Rev") -> bool:
        return other.item < self.item

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Rev) and self.item == other.item

    def __repr__(self) -> str:
        return repr(self.item)


def maxheapify(h: list) -> None:
    h[:] = [_Rev(x) for x in h]
    heapq.heapify(h)


def maxheappush(h: list, item: Any) -> None:
    heapq.heappush(h, _Rev(item))


def maxheappop(h: list) -> Any:
    return heapq.heappop(h).item


def maxheappushpop(h: list, item: Any) -> Any:
    return heapq.heappushpop(h, _Rev(item)).item


def maxheapreplace(h: list, item: Any) -> Any:
    return heapq.heapreplace(h, _Rev(item)).item


def maxheappeek(h: list) -> Any:
    return h[0].item


if __name__ == "__main__":
    h: list = []
    for x in [3, 1, 4, 1, 5]:
        maxheappush(h, x)
    assert maxheappeek(h) == 5
    assert [maxheappop(h) for _ in range(len(h))] == [5, 4, 3, 1, 1]

    h = [(2, "b"), (9, "a"), (5, "c")]
    maxheapify(h)
    assert maxheappop(h) == (9, "a")
    assert maxheappushpop(h, (7, "d")) == (7, "d")
    assert maxheapreplace(h, (1, "e")) == (5, "c")
    assert [maxheappop(h) for _ in range(len(h))] == [(2, "b"), (1, "e")]
    print("ok")
