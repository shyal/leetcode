# combo_utils.py
#
# Index-combination helpers preloaded by sitecustomize: every pair and every
# triple of indices below n, in lexicographic order, without recursion.

from typing import Any, Callable, Iterable, Iterator

Maker = Callable[[Iterable[int]], Any]


def pairs(n: int, type: Maker = tuple, back: bool = False) -> Iterator[Any]:
    """Every (i, j) with 0 <= i < j < n, in lexicographic order.

    With back, the pairs are grouped by the later index instead: for each
    j in turn, every (i, j) with i < j. That is the dp order, where cell j
    looks back at every earlier cell.

    Each pair is built by type: tuple by default, list for a LeetCode answer.
    """
    if back:
        for j in range(n):
            for i in range(j):
                yield type((i, j))
        return
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))


def triples(n: int, type: Maker = tuple) -> Iterator[Any]:
    """Every (i, j, k) with 0 <= i < j < k < n, in lexicographic order.

    Each triple is built by type: tuple by default, list for a LeetCode answer.
    """
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                yield type((i, j, k))
