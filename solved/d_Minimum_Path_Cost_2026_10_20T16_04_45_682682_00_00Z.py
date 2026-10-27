"""
DRILL: Minimum Path Cost

G is a dict mapping integer nodes to dicts of {neighbour: weight}; s and t are the start and target nodes. Treat G as a directed graph. Return the minimum path cost, the sum of edge weights, from s to t, or -1 if t is unreachable. Return 0 when s equals t. Use Dijkstra's algorithm.

Example 1:

Input: G={0: {1: 2, 2: 9}, 1: {2: 3}, 2: {}}, s=0, t=2
Output: 5

    0 --2--> 1 --3--> 2
    |                 ^
    +--------9--------+

Explanation: 0 -> 1 -> 2 costs 2 + 3 = 5; breadth-first search selects 0 -> 2, costing 9.

Example 2:

Input: G={0: {1: 4}, 1: {}, 2: {}}, s=0, t=2
Output: -1

    0 --4--> 1     2

Explanation: No path reaches 2 from 0, so return -1.

Example 3:

Input: G={0: {1: 7}, 1: {}}, s=1, t=1
Output: 0

    0 --7--> 1

Explanation: The empty path from 1 to itself costs 0.

Constraints:

    1 <= n = len(G) <= 10.
    Node keys are exactly the integers 0 through n - 1.
    Every neighbour is a node key in G.
    0 <= m <= n * (n - 1), where m counts directed edges.
    Each edge connects distinct nodes.
    Every weight is an integer from 0 through 20.
    s and t are integer node keys in G.

    REQUIRED: You must achieve O((n + m) log n) time and avoid Example 1's breadth-first-search error: fewer edges cost more than more edges.
"""


# mu 0.12
# class Solution
#   def min_cost(G: {int: {int: int}}, s: int, t: int) -> int
#     q = heap([(0, s)])
#     seen = set([])
#     while q
#       weight, node = q.pop()
#       seen.add(node)
#       if node == t
#         return weight
#       for next in G[node]
#         if next not in seen
#           q <- (G[node][next] + weight, next)
#     -1

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


class Solution:
    def min_cost(self, G: dict[int, dict[int, int]], s: int, t: int) -> int:
        q = heap([(0, s)])
        seen = set([])
        while q:
            weight, node = q.pop()
            seen.add(node)
            if node == t:
                return weight
            for next in G[node]:
                if next not in seen:
                    q.append((G[node][next] + weight, next))
        return -1


sol = Solution()
G = {0: {1: 2, 2: 9}, 1: {2: 3}, 2: {}}
draw_graphviz(G, directed=True)
print(sol.min_cost(G, 0, 2))
_l, _r = sol.min_cost({0: {1: 2, 2: 9}, 1: {2: 3}, 2: {}}, 0, 2), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 4}, 1: {}, 2: {}}, 0, 2), -1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 7}, 1: {}}, 1, 1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 7}, 1: {}}, 1, 0), -1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 0}, 1: {2: 0}, 2: {}}, 0, 2), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 10, 2: 1}, 1: {3: 1}, 2: {1: 1}, 3: {}}, 0, 3), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 1}, 1: {0: 1, 2: 5}, 2: {}}, 0, 2), 6
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 1, 3: 20}, 1: {2: 1}, 2: {3: 1}, 3: {}}, 0, 3), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {1: 3}, 1: {2: 3}, 2: {3: 3}, 3: {}}, 0, 3), 9
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.min_cost({0: {}}, 0, 0), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
