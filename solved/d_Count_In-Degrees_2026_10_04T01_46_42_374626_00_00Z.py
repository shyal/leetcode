"""
DRILL: Count In-Degrees

Given n nodes numbered 0 to n - 1 and edges, where [a, b] is an edge
from a to b, return indeg, where indeg[b] is the number of edges into b.

Example 1:

Input: n = 4, edges = [[0, 1], [0, 2], [1, 3], [2, 3]]

    0 --> 1 --.
    |         v
    '--> 2 --> 3

Output: [0, 1, 1, 2]

Example 2:

Input: n = 3, edges = []
Output: [0, 0, 0]

Constraints:

    1 <= n <= 2000
    0 <= len(edges) <= 5000

    REQUIRED: must run in O(n + len(edges)) time.
"""


# mu 0.7
# def inDegrees(n: int, edges: [[int]]) -> [int]
#   return indegrees(edges, n, type=list)

from collections import defaultdict


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def indegrees(edges, n=None, reverse=False, directed=True, type=defaultdict):
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


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def inDegrees(self, n: int, edges: list[list[int]]) -> list[int]:
        _in_edges, edges = edges, Grid(edges)
        _w_edges = edges
        try:
            return indegrees(edges, n, type=list)
        finally:
            _in_edges[:] = _w_edges


sol = Solution()
print(sol.inDegrees(4, [[0, 1], [0, 2], [1, 3], [2, 3]]))
assert uses(Solution, indegrees)
assert sol.inDegrees(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) == [0, 1, 1, 2]
assert sol.inDegrees(3, []) == [0, 0, 0]
assert sol.inDegrees(2, [[1, 0]]) == [1, 0]
assert sol.inDegrees(3, [[2, 0], [0, 1], [1, 2]]) == [1, 1, 1]
