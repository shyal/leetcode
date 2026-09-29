"""
DRILL: Node Distance Pairs
TRAINS: graph-bfs-shortest

Start on node 0 of the directed graph G. G maps each node to the list of
nodes its edges point to. Each step, move along one edge. Never visit a
node twice. For example, with G = {0: [1, 2], 1: [2], 2: [0]}:

    0 ---> 1
    ^ \    |
    |  \   |
    |   v  v
    +----- 2

we reach 1 and 2 in one step. Node 2 is also two steps away through 1,
and node 0 is two steps away through 2, but both are already visited.

Return the visited nodes as a set of pairs (node_value, distance). The
node_value is the value of the node. The distance is the fewest steps it
takes to reach the node from 0.

Example 1:

Input: G = {0: [1, 2], 1: [2], 2: [0]}
Output: {(0, 0), (1, 1), (2, 1)}

Example 2:

Input: G = {0: [1], 1: [2], 2: [3], 3: [1]}
Output: {(0, 0), (1, 1), (2, 2), (3, 3)}

    0 -> 1 -> 2
         ^    |
         |    v
         +--- 3

Explanation: The edge 3 -> 1 leads back to node 1, which is already
visited, so node 1 appears once.

Example 3:

Input: G = {0: [1], 1: [], 2: [0]}
Output: {(0, 0), (1, 1)}

    2 -> 0 -> 1

Explanation: No edge leads into node 2, so you never reach it.

Constraints:

    1 <= len(G) <= 100
    Every node in a list is a key of G.

    REQUIRED: O(n + m), one breadth-first search from node 0. Each node
    must appear once, with its fewest steps. A depth-first search gives
    (2, 2) in Example 1.
"""


# mu 0.7
# def distances(G: {int: [int]}) -> {(int, int)}
#   q = deque([0])
#   seen = {}
#   for (d, node) in levels(q)
#     if node in seen
#       continue
#     seen[node] = d
#     for nxt in G[node]
#       q.append(nxt)
#   set([(k, v) for (k, v) in seen.items()])

def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def levels(
    q, grid=None, seen=None, grouped=False, eq=None, lt=None, lte=None, gt=None, gte=None
):
    bare = eq is None and lt is None and lte is None and gt is None and gte is None
    row = list.__getitem__ if isinstance(grid, list) else lambda g, i: g[i]
    d = 0
    while q:
        level = []
        for _ in range(len(q)):
            x = q.popleft()
            if seen is not None and x in seen:
                continue
            if not bare:
                v = x if grid is None else row(grid, x[0])[x[1]]
                if not _holds(v, eq, lt, lte, gt, gte):
                    continue
            if seen is not None:
                seen.add(x)
            if grouped:
                level.append(x)
            else:
                yield d, x
        if grouped and level:
            yield d, level
        d += 1


class Solution:
    def distances(self, G: dict[int, list[int]]) -> set[tuple[int, int]]:
        q = deque([0])
        seen = {}
        for (d, node) in levels(q):
            if node in seen:
                continue
            seen[node] = d
            for nxt in G[node]:
                q.append(nxt)
        return set([(k, v) for (k, v) in seen.items()])


sol = Solution()
draw_graphviz({0: [1, 2], 1: [2], 2: [0]}, type='directed')
print(sol.distances({0: [1, 2], 1: [2], 2: [0]}))
assert sol.distances({0: [1, 2], 1: [2], 2: [0]}) == {(0, 0), (1, 1), (2, 1)}
assert sol.distances({0: [1], 1: [2], 2: [3], 3: [1]}) == {(0, 0), (1, 1), (2, 2), (3, 3)}
assert sol.distances({0: [1], 1: [], 2: [0]}) == {(0, 0), (1, 1)}
assert sol.distances({0: []}) == {(0, 0)}
assert sol.distances({0: [0]}) == {(0, 0)}
assert sol.distances({0: [1], 1: [0]}) == {(0, 0), (1, 1)}
assert sol.distances({0: [1, 2], 1: [3], 2: [3], 3: []}) == {(0, 0), (1, 1), (2, 1), (3, 2)}
assert sol.distances({0: [1, 4], 1: [2], 2: [3], 3: [4], 4: []}) == {(0, 0), (1, 1), (2, 2), (3, 3), (4, 1)}
assert sol.distances({0: [], 1: [2], 2: [1]}) == {(0, 0)}
