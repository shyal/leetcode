"""
URL: https://leetcode.com/problems/path-with-maximum-probability/description/?envType=problem-list-v2&envId=vn57k9wr

1514. Path with Maximum Probability

You are given an undirected weighted graph of n nodes (0-indexed), represented by an edge list where edges[i] = [a, b] is an undirected edge connecting the nodes a and b with a probability of success of traversing that edge succProb[i].

Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.

If there is no path from start to end, return 0. Your answer will be accepted if it differs from the correct answer by at most 1e-5.

Example 1:

Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
Output: 0.25000
Explanation: There are two paths from start to end, one having a probability of success = 0.2 and the other has 0.5 * 0.5 = 0.25.

Example 2:

Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2
Output: 0.30000

Example 3:

Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
Output: 0.00000
Explanation: There is no path between 0 and 2.

Constraints:

    2 <= n <= 10^4
    0 <= start, end < n
    start != end
    0 <= a, b < n
    a != b
    0 <= succProb.length == edges.length <= 2*10^4
    0 <= succProb[i] <= 1
    There is at most one edge between every two nodes.
---
took the official hint: Take log probabilities to sum up numbers instead of multiplying them.

LEETCODE: Accepted (283 ms, 31.8 MB)
"""


# mu 0.12
# class Solution
#   def maxProbability(n: int, edges: [[int]], succProb: [float], start_node: int, end_node: int) -> float
#     G = adjacency([x + [y] for x, y in zip(edges, succProb)], directed=False, weighted=True)
#     q = heap([(0, start_node)], type=max)
#     seen = set([])
#     while q
#       cost, node = q.pop()
#       if node in seen
#         continue
#       seen.add node
#       if node == end_node
#         return math.exp(cost)
#       for next in G[node]
#         q <- (cost + log(G[node][next]) if G[node][next] != 0 else -inf, next)
#     0

from collections import defaultdict
from math import inf


def adjacency(edges, n=None, reverse=False, directed=True, weighted=False):
    adj = defaultdict(dict) if weighted else defaultdict(list)
    for c in range(n or 0):
        adj[c]
    for e in edges:
        (a, b) = e[:2]
        if reverse:
            (a, b) = (b, a)
        if weighted:
            adj[a][b] = e[2]
            if not directed:
                adj[b][a] = e[2]
        else:
            adj[a].append(b)
            if not directed:
                adj[b].append(a)
    return adj


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
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:
        _in_edges, edges = edges, Grid(edges)
        _w_edges = edges
        try:
            G = adjacency([x + [y] for x, y in zip(edges, succProb)], directed=False, weighted=True)
            q = heap([(0, start_node)], type=max)
            seen = set([])
            while q:
                cost, node = q.pop()
                if node in seen:
                    continue
                seen.add(node)
                if node == end_node:
                    return math.exp(cost)
                for next in G[node]:
                    q.append((cost + log(G[node][next]) if G[node][next] != 0 else -inf, next))
            return 0
        finally:
            _in_edges[:] = _w_edges


sol = Solution()
print(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.2], 0, 2))
assert uses(Solution, adjacency)
_l, _r = abs(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.2], 0, 2) - 0.25), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.3], 0, 2) - 0.3), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(3, [[0, 1]], [0.5], 0, 2) - 0.0), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(2, [], [], 0, 1) - 0.0), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(2, [[0, 1]], [1.0], 0, 1) - 1.0), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(4, [[0, 1], [1, 2], [2, 3]], [0.9, 0.9, 0.9], 0, 3) - 0.7290000000000001), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(4, [[0, 1], [1, 2], [2, 3], [0, 3]], [0.5, 0.5, 0.5, 0.1], 0, 3) - 0.125), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(5, [[0, 1], [1, 2], [2, 3], [3, 4]], [0.0, 0.0, 0.0, 0.0], 0, 4) - 0.0), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.5], 0, 2) - 0.5), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.0], 0, 2) - 0.25), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(10000, [[i, i + 1] for i in range(0, 9999)], [1.0] * 9999, 0, 9999) - 1.0), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(10000, [[i, i + 1] for i in range(0, 9999)], [0.99999] * 9999, 0, 9999) - 0.9048460140748944), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.5], 1, 0) - 0.5), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.5], 2, 0) - 0.5), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
_l, _r = abs(sol.maxProbability(2, [[0, 1]], [0.0], 0, 1) - 0.0), 1e-05
assert _l < _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r))) + "\nop   : <"
