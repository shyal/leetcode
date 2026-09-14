# assert_utils.py
#
# Comparisons for asserts in drills and solves, where the answer is
# right up to some order the problem does not fix.

from typing import Any, Iterable, Sequence


def same_rows(a: Sequence[Iterable[Any]], b: Sequence[Iterable[Any]]) -> bool:
    """Row i of a and row i of b hold the same elements, in any order.

    The rows themselves stay in order: an adjacency list keyed by index.
    """
    return len(a) == len(b) and all(set(x) == set(y) for x, y in zip(a, b))
