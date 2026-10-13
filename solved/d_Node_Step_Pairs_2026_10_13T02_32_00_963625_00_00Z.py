"""
DRILL: Node Step Pairs

Start on node 0 of the directed graph G. Each step, move along one edge,
for at most k steps. For example, with G = {0: [1], 1: [2], 2: [3], 3: [1]}
and k = 4:

    0 -> 1 -> 2
         ^    |
         |    v
         +--- 3

we traverse as so: 0 -> 1 -> 2 -> 3 -> 1.

Return the traversal as a set of pairs (node_value, distance). The
node_value is the value of the node. The distance is how many steps you
have taken to get there, so node 1 appears as (1, 1) and as (1, 4).
When a node has several edges, follow every one of them.

Example 1:

Input: G = {0: [1], 1: [2], 2: [3], 3: [1]}, k = 4
Output: {(0, 0), (1, 1), (2, 2), (3, 3), (1, 4)}

    0 -> 1 -> 2
         ^    |
         |    v
         +--- 3

Explanation: The path 0 -> 1 -> 2 -> 3 -> 1 reaches node 1 a second
time, with 4 edges.

Example 2:

Input: G = {0: [1, 2], 1: [2], 2: [0]}, k = 2
Output: {(0, 0), (1, 1), (2, 1), (2, 2), (0, 2)}

    0 ---> 1
    ^ \    |
    |  \   |
    |   v  v
    +----- 2

Example 3:

Input: G = {0: [1], 1: [2], 2: []}, k = 3
Output: {(0, 0), (1, 1), (2, 2)}

    0 -> 1 -> 2

Constraints:

    1 <= len(G) <= 100
    0 <= k <= 100

    REQUIRED: O(k * (n + m)), one breadth-first search from node 0. A
    visited set keyed on the node alone drops (1, 4) from Example 1.
"""


# mu 0.10
# class Solution
#   def reachable(G: {int: [int]}, k: int) -> {(int, int)}
#     q = deque([0])
#     seen = set()
#     for d, node in levels(q)
#       if d > k
#         break
#       if (node, d) in seen
#         continue
#       seen.add((node, d))
#       for next in G[node]
#         q <- next
#     seen

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


class Solution:
    def reachable(self, G: dict[int, list[int]], k: int) -> set[tuple[int, int]]:
        q = deque([0])
        seen = set()
        for d, node in levels(q):
            if d > k:
                break
            if (node, d) in seen:
                continue
            seen.add((node, d))
            for next in G[node]:
                q.append(next)
        return seen


sol = Solution()
draw_graphviz({0: [1], 1: [2], 2: [3], 3: [1]}, type='directed')
print(sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 4))
_l, _r = sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 4), {(0, 0), (1, 1), (1, 4), (2, 2), (3, 3)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 0), {(0, 0)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1], 1: [2], 2: [3], 3: [1]}, 2), {(0, 0), (1, 1), (2, 2)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1, 2], 1: [2], 2: [0]}, 2), {(0, 0), (0, 2), (1, 1), (2, 1), (2, 2)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1], 1: [2], 2: []}, 3), {(0, 0), (1, 1), (2, 2)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1], 1: [1]}, 3), {(0, 0), (1, 1), (1, 2), (1, 3)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: []}, 5), {(0, 0)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1], 1: [0]}, 3), {(0, 0), (0, 2), (1, 1), (1, 3)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [1, 2], 1: [3], 2: [3], 3: []}, 2), {(0, 0), (1, 1), (2, 1), (3, 2)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [0]}, 2), {(0, 0), (0, 1), (0, 2)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.reachable({0: [], 1: [2], 2: [1]}, 2), {(0, 0)}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
