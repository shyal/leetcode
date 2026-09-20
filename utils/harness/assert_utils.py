# assert_utils.py
#
# Comparisons for asserts in drills and solves, where the answer is
# right up to some order the problem does not fix.

import ast
import inspect
from typing import Any, Callable, Iterable, Sequence


def same_rows(a: Sequence[Iterable[Any]], b: Sequence[Iterable[Any]]) -> bool:
    """Row i of a and row i of b hold the same elements, in any order.

    The rows themselves stay in order: an adjacency list keyed by index.
    """
    return len(a) == len(b) and all(set(x) == set(y) for x, y in zip(a, b))


def same_seq(a: Iterable[Any], b: Iterable[Any]) -> bool:
    """The same elements in the same order, whatever the container.

    A tuple from divmod against a list in the assert: (1, 2) matches [1, 2].
    """
    return list(a) == list(b)


def uses(cls: type, *helpers: Callable[..., Any]) -> bool:
    """Every helper is called somewhere in the source of cls.

    Raises AssertionError naming the first helper cls never calls. The
    check reads the class as written, so it lives in the test block of a
    solve and goes with the asserts, never to leetcode.
    """
    tree = ast.parse(inspect.getsource(cls))
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    for h in helpers:
        if h.__name__ not in called:
            raise AssertionError(f"{cls.__name__} never calls {h.__name__}")
    return True
