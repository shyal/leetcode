"""
DRILL: Longest Path From Zero
TRAINS: memoize-recursion

G is a DAG (directed acyclic graph) as an adjacency list: G[u] is the
list of nodes u points to. Start on node 0. Let L(u) be the number of
edges on the longest path starting at u. If G[u] is empty, L(u) = 0.
Otherwise L(u) = 1 + max(L(v) for v in G[u]). For example, with
G = {0: [1, 2], 1: [2], 2: []}:

    0 ---> 1
     \     |
      \    v
       +-> 2

the longest path from 2 is 0, from 1 it is 1, and from 0 it is 2 through
node 1.

Return the number of edges on the longest path from node 0.

Example 1:

Input: G = {0: [1, 2], 1: [2], 2: []}
Output: 2

Example 2:

Input: G = {0: [1], 1: [2], 2: [3], 3: []}
Output: 3

    0 -> 1 -> 2 -> 3

Example 3:

Input: G = {0: [], 1: [0]}
Output: 0

    1 -> 0

Explanation: Node 0 has no edges, and node 1 is never reached.

Constraints:

    1 <= len(G) <= 200
    Every node in a list is a key of G.
    No path visits a node twice.

    REQUIRED: O(n + m) time. The longest path from each node must be
    computed once and remembered. Recomputing it on every visit walks
    every path in the graph, and a graph of 200 nodes where each node
    points to the next two has more paths than the clock allows.
---
Learning
"""


# mu 0.7
# def longestPath(G: {int: [int]}) -> int
#   memo longest(u) = max((1 + longest(v) for v in G[u]), default=0)
#   longest(0)

from functools import cache
import sys
import threading


sys.setrecursionlimit(1 << 20)


def deep(fn):
    """Run fn on a thread with a 256 MB stack, so deep memo recursion fits."""
    out, err = [], []

    def target():
        try:
            out.append(fn())
        except BaseException as e:
            err.append(e)

    threading.stack_size(1 << 28)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if err:
        raise err[0]
    return out[0]


class Solution:
    def longestPath(self, G: dict[int, list[int]]) -> int:
        def run():
            @cache
            def longest(u):
                return max((1 + longest(v) for v in G[u]), default=0)
            return longest(0)
        return deep(run)


sol = Solution()
draw_graphviz({0: [1, 2], 1: [2], 2: []}, type='directed')
print(sol.longestPath({0: [1, 2], 1: [2], 2: []}))
assert sol.longestPath({0: [1, 2], 1: [2], 2: []}) == 2
assert sol.longestPath({0: [1], 1: [2], 2: [3], 3: []}) == 3
assert sol.longestPath({0: [], 1: [0]}) == 0
assert sol.longestPath({0: []}) == 0
assert sol.longestPath({0: [1, 2], 1: [], 2: []}) == 1
assert sol.longestPath({0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}) == 3
assert sol.longestPath({0: [3, 1], 1: [2], 2: [], 3: []}) == 2
assert sol.longestPath({0: [1, 2], 1: [4], 2: [3], 3: [4], 4: []}) == 3
