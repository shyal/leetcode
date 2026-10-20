"""
URL: https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/description/?envType=problem-list-v2&envId=vn57k9wr

3243. Shortest Distance After Road Addition Queries I

You are given an integer n and a 2D integer array queries.

There are n cities numbered from 0 to n - 1. Initially, there is a unidirectional road from city i to city i + 1 for all 0 <= i < n - 1.

queries[i] = [u_i, v_i] represents the addition of a new unidirectional road from city u_i to city v_i. After each query, you need to find the length of the shortest path from city 0 to city n - 1.

Return an array answer where for each i in the range [0, queries.length - 1], answer[i] is the length of the shortest path from city 0 to city n - 1 after processing the first i + 1 queries.

Example 1:

Input: n = 5, queries = [[2,4],[0,2],[0,4]]
Output: [3,2,1]
Explanation:
- Initially there is a path 0->1->2->3->4 of length 4.
- After adding road 2->4, shortest path 0->1->2->4 has length 3.
- After adding road 0->2, shortest path 0->2->4 has length 2.
- After adding road 0->4, shortest path 0->4 has length 1.

Example 2:

Input: n = 4, queries = [[0,3],[0,2]]
Output: [1,1]
Explanation:
- After adding road 0->3, shortest path 0->3 has length 1.
- After adding road 0->2, shortest path remains 0->3 of length 1.

Constraints:

    3 <= n <= 500
    1 <= queries.length <= 500
    queries[i].length == 2
    0 <= queries[i][0] < queries[i][1] < n
    1 < queries[i][1] - queries[i][0]
    There are no repeated roads among the queries.

---

hinted: needed the seen set else TLE

LEETCODE: Accepted (1074 ms, 19.6 MB)
"""


# mu 0.12
# class Solution
#   def shortestDistanceAfterQueries(n: int, queries: [[int]]) -> [int]
#     G = {:list}
#     for i in 0..<n-1
#       G[i] <- i + 1
#
#     def bfs(start)
#       q = deque([start])
#       for d, node in levels(q)
#         if node == n -1
#           return d
#         for next in G[node]
#           q <- next
#
#     ret res = []
#     _min = inf
#     for a, b in queries
#       G[a] <- b
#       # print(G)
#       if _min != inf and a > _min
#         res <- bfs(0)
#       else
#         res <- a + bfs(a)
#       _min = min(a, _min)

from collections import defaultdict
from math import inf


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (eq is None or v == eq) and (lt is None or v < lt) and (lte is None or v <= lte) and (gt is None or v > gt) and (gte is None or v >= gte)


def levels(q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None):

    def keep(x):
        v = x if grid is None else grid[x[0]][x[1]]
        if not _holds(v, eq, lt, lte, gt, gte) or (seen is not None and x in seen):
            return False
        if seen is not None:
            seen.add(x)
        return True
    d = 0
    while q:
        popped = (q.popleft() for _ in range(len(q)))
        if grouped:
            level = [x for x in popped if keep(x)]
            if level:
                yield (d, level)
        else:
            for x in popped:
                if keep(x):
                    yield (d, x)
        d += 1


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


# mu 0.12
# class Solution
#   def shortestDistanceAfterQueries(n: int, queries: [[int]]) -> [int]
#     G = {:list}
#     for i in 0..<n-1
#       G[i] <- i + 1
#
#     def bfs(start)
#       q = deque([start])
#       for d, node in levels(q, seen=set())
#         if node == n -1
#           return d
#         for next in G[node]
#           q <- next
#
#     ret res = []
#     _min = inf
#     for a, b in queries
#       G[a] <- b
#       # print(G)
#       if _min != inf and a > _min
#         res <- bfs(0)
#       else
#         res <- a + bfs(a)
#       _min = min(a, _min)

from collections import defaultdict
from math import inf


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (eq is None or v == eq) and (lt is None or v < lt) and (lte is None or v <= lte) and (gt is None or v > gt) and (gte is None or v >= gte)


def levels(q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None):

    def keep(x):
        v = x if grid is None else grid[x[0]][x[1]]
        if not _holds(v, eq, lt, lte, gt, gte) or (seen is not None and x in seen):
            return False
        if seen is not None:
            seen.add(x)
        return True
    d = 0
    while q:
        popped = (q.popleft() for _ in range(len(q)))
        if grouped:
            level = [x for x in popped if keep(x)]
            if level:
                yield (d, level)
        else:
            for x in popped:
                if keep(x):
                    yield (d, x)
        d += 1


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
    def shortestDistanceAfterQueries(self, n: int, queries: list[list[int]]) -> list[int]:
        _in_queries, queries = queries, Grid(queries)
        _w_queries = queries
        try:
            G = defaultdict(list)
            for i in range(0, n - 1):
                G[i].append(i + 1)
            def bfs(start):
                q = deque([start])
                for d, node in levels(q, seen=set()):
                    if node == n - 1:
                        return d
                    for next in G[node]:
                        q.append(next)
            res = []
            _min = inf
            for a, b in queries:
                G[a].append(b)
                if _min != inf and a > _min:
                    res.append(bfs(0))
                else:
                    res.append(a + bfs(a))
                _min = min(a, _min)
            return res
        finally:
            _in_queries[:] = _w_queries


sol = Solution()
_l, _r = sol.shortestDistanceAfterQueries(5, [[2, 4], [0, 2], [0, 4]]), [3, 2, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(4, [[0, 3], [0, 2]]), [1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(3, [[0, 2]]), [1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(4, [[1, 3], [0, 2]]), [2, 2]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(5, [[2, 4], [1, 3], [0, 3]]), [3, 3, 2]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(6, [[0, 5], [1, 4], [2, 5]]), [1, 1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(7, [[0, 6], [0, 5], [0, 4]]), [1, 1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(10, [[0, 9], [1, 8], [2, 9], [3, 7]]), [1, 1, 1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(500, [[0, 499]]), [1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.shortestDistanceAfterQueries(20, [[i, 19] for i in range(0, 18, 2)]), [1, 1, 1, 1, 1, 1, 1, 1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
