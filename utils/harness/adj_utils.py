# adj_utils.py

from collections import defaultdict
from typing import Any, List, Optional

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
    type: Any = defaultdict,
) -> Any:
    """In-degree of every node from an edge list, each edge [a, b] counting
    one into b. Default is a defaultdict(int), any node reading 0; with n,
    nodes 0 to n - 1 are all keys. type=list needs n and returns a plain
    list. reverse reads each edge as b to a."""
    indeg: Any
    if type is list:
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
    return indeg
