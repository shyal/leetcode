"""
URL: https://leetcode.com/problems/minimum-time-to-visit-disappearing-nodes/description/?envType=problem-list-v2&envId=vn57k9wr

3112. Minimum Time to Visit Disappearing Nodes

There is an undirected graph of n nodes. You are given a 2D array edges, where edges[i] = [u_i, v_i, length_i] describes an edge between node u_i and node v_i with a traversal time of length_i units.

Additionally, you are given an array disappear, where disappear[i] denotes the time when the node i disappears from the graph and you won't be able to visit it.

Note that the graph might be disconnected and might contain multiple edges.

Return the array answer, with answer[i] denoting the minimum units of time required to reach node i from node 0. If node i is unreachable from node 0 then answer[i] is -1.

Example 1:

Input: n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,1,5]
Output: [0,-1,4]
Explanation:
We are starting our journey from node 0, and our goal is to find the minimum time required to reach each node before it disappears.
- For node 0, we don't need any time as it is our starting point.
- For node 1, we need at least 2 units of time to traverse edges[0]. Unfortunately, it disappears at that moment, so we won't be able to visit it.
- For node 2, we need at least 4 units of time to traverse edges[2].

Example 2:

Input: n = 3, edges = [[0,1,2],[1,2,1],[0,2,4]], disappear = [1,3,5]
Output: [0,2,3]
Explanation:
We are starting our journey from node 0, and our goal is to find the minimum time required to reach each node before it disappears.
- For node 0, we don't need any time as it is the starting point.
- For node 1, we need at least 2 units of time to traverse edges[0].
- For node 2, we need at least 3 units of time to traverse edges[0] and edges[1].

Example 3:

Input: n = 2, edges = [[0,1,1]], disappear = [1,1]
Output: [0,-1]
Explanation:
Exactly when we reach node 1, it disappears.

Constraints:

    1 <= n <= 5 * 10^4
    0 <= edges.length <= 10^5
    edges[i] == [u_i, v_i, length_i]
    0 <= u_i, v_i <= n - 1
    1 <= length_i <= 10^5
    disappear.length == n
    1 <= disappear[i] <= 10^5
---
hinted on: min(G[a].get(b, inf), w)
"""


# mu 0.12
# class Solution
#   def minimumTime(n: int, edges: [[int]], disappear: [int]) -> [int]
#     G = {:list}
#     for a, b, w in edges
#       G[a] <- (b, w)
#       G[b] <- (a, w)
#     def bfs(t)
#       q = heap([(0, 0)])
#       seen = set([])
#       while q
#         weight, node = q.pop()
#         if node in seen
#           continue
#         res[node] = weight
#         seen.add(node)
#         for next, next_weight in G[node]
#           if next not in seen
#             if weight + next_weight < disappear[next]
#               q <- (weight + next_weight, next)
#       -1
#     ret res = table(n, fill=-1)
#     bfs(n-1)

from collections import defaultdict


def _down(h, i, before):
    (n, x) = (len(h), h[i])
    while (c := (2 * i + 1)) < n:
        if c + 1 < n and before(h[c + 1], h[c]):
            c += 1
        if not before(h[c], x):
            break
        h[i] = h[c]
        i = c
    h[i] = x


def _gt(a, b):
    return b < a


def _lt(a, b):
    return a < b


def _pop(h, before):
    last = h.pop()
    if not h:
        return last
    (top, h[0]) = (h[0], last)
    _down(h, 0, before)
    return top


def _up(h, i, before):
    x = h[i]
    while i:
        p = (i - 1) // 2
        if not before(x, h[p]):
            break
        h[i] = h[p]
        i = p
    h[i] = x


class heap:

    def __init__(self, items=(), type=min):
        self.before = _gt if type is max else _lt
        self.h = list(items)
        for i in reversed(range(len(self.h) // 2)):
            _down(self.h, i, self.before)

    def push(self, x):
        self.h.append(x)
        _up(self.h, len(self.h) - 1, self.before)
    append = push

    def pop(self):
        return _pop(self.h, self.before)

    def peek(self):
        return self.h[0]

    def __len__(self):
        return len(self.h)

    def __iter__(self):
        return iter(self.h)


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


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
    def minimumTime(self, n: int, edges: list[list[int]], disappear: list[int]) -> list[int]:
        _in_edges, edges = edges, Grid(edges)
        _w_edges = edges
        try:
            G = defaultdict(list)
            for a, b, w in edges:
                G[a].append((b, w))
                G[b].append((a, w))
            def bfs(t):
                q = heap([(0, 0)])
                seen = set([])
                while q:
                    weight, node = q.pop()
                    if node in seen:
                        continue
                    res[node] = weight
                    seen.add(node)
                    for next, next_weight in G[node]:
                        if next not in seen:
                            if weight + next_weight < disappear[next]:
                                q.append((weight + next_weight, next))
                return -1
            res = table(n, fill=-1)
            bfs(n - 1)
            return res
        finally:
            _in_edges[:] = _w_edges


sol = Solution()
_l, _r = sol.minimumTime(8, [[4, 0, 5], [3, 7, 3], [0, 2, 3], [3, 5, 3], [7, 0, 1], [2, 0, 3], [7, 7, 10]], [15, 8, 4, 3, 9, 18, 9, 13]), [0, -1, 3, -1, 5, -1, -1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[2, 0, 9], [1, 0, 5], [2, 2, 4], [0, 1, 10], [1, 1, 10], [1, 1, 10], [2, 2, 10], [1, 1, 10]], [4, 13, 19]), [0, 5, 9]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(7, [[1, 4, 3], [3, 4, 2], [2, 5, 5], [3, 3, 10]], [10, 1, 13, 1, 7, 1, 19]), [0, -1, -1, -1, -1, -1, -1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 2], [1, 2, 1], [0, 2, 4]], [1, 1, 5]), [0, -1, 4]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 2], [1, 2, 1], [0, 2, 4]], [1, 3, 5]), [0, 2, 3]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(2, [[0, 1, 1]], [1, 1]), [0, -1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(1, [], [1]), [0]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(2, [[0, 1, 1]], [2, 2]), [0, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(2, [[0, 1, 2]], [2, 1]), [0, -1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 1], [1, 2, 1], [0, 2, 3]], [5, 5, 5]), [0, 1, 2]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 10]], [2, 3, 4, 5]), [0, 1, 2, 3]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 1], [1, 2, 1], [0, 2, 1]], [1, 1, 1]), [0, -1, -1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 1], [1, 2, 1], [0, 2, 1], [0, 1, 1]], [3, 3, 3]), [0, 1, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1]], [10, 2, 3, 4, 5]), [0, 1, 2, 3, 4]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 100000], [1, 2, 100000]], [100000, 100000, 100000]), [0, -1, -1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 1], [1, 2, 1]], [1, 2, 3]), [0, 1, 2]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(3, [[0, 1, 1], [1, 2, 1]], [1, 1, 1]), [0, -1, -1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.minimumTime(2, [[0, 1, 1], [0, 1, 1]], [2, 2]), [0, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))


# FAILED: walked away after 50m 3s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
