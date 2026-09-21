# adj_utils.py

from collections import defaultdict
from typing import Any, Deque, Iterator, List, Optional, Tuple

from grid_utils import table


def adjacency(
    edges: List[Any],
    n: Optional[int] = None,
    reverse: bool = False,
    directed: bool = True,
    weighted: bool = False,
) -> Any:
    """Adjacency from an edge list. Each edge is [a, b] or, with weighted,
    [a, b, w]. Unweighted returns a dict of lists in edge order; weighted a
    dict of dicts, adj[a][b] = w. With n, nodes 0 to n - 1 are all keys,
    isolated ones with an empty list. reverse reads each edge as b to a.
    directed=False adds both directions."""
    adj: Any = defaultdict(dict) if weighted else defaultdict(list)
    for c in range(n or 0):
        adj[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        if weighted:
            adj[a][b] = e[2]
            if not directed:
                adj[b][a] = e[2]
        else:
            adj[a].append(b)
            if not directed:
                adj[b].append(a)
    return adj


def indegrees(
    edges: List[Any],
    n: Optional[int] = None,
    reverse: bool = False,
    directed: bool = True,
    type: Any = defaultdict,
) -> Any:
    """In-degree of every node from an edge list, each edge [a, b] counting
    one into b. Default is a defaultdict(int), any node reading 0; with n,
    nodes 0 to n - 1 are all keys. type=list needs n and returns a plain
    list. reverse reads each edge as b to a. directed=False counts the edge
    into a as well, so the result is the plain degree of every node."""
    indeg: Any
    if type is list:
        if n is None:
            raise ValueError("type=list needs n")
        indeg = table(n)
    else:
        indeg = defaultdict(int)
        for c in range(n or 0):
            indeg[c]
    for e in edges:
        a, b = e[:2]
        if reverse:
            a, b = b, a
        indeg[b] += 1
        if not directed:
            indeg[a] += 1
    return indeg


def levels(q: Deque[Any], grouped: bool = False) -> Iterator[Tuple[int, Any]]:
    """Level-order BFS over a deque the caller keeps pushing onto.

    Yields (d, item) for every item popped, where d is the level the item
    was pushed at, starting from 0 for the items already in q. The caller
    appends the next level's items to q inside the loop body and keeps
    its own seen set. With grouped=True yields (d, items) once per level,
    items being the whole level as a list.
    """
    d = 0
    while q:
        if grouped:
            yield d, [q.popleft() for _ in range(len(q))]
        else:
            for _ in range(len(q)):
                yield d, q.popleft()
        d += 1
