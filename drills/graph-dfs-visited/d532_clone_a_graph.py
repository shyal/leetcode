"""
EPI 18.5 Clone a graph

Given a vertex graph of a directed graph, return a copy of the part of the
graph that graph reaches. Each vertex is a GraphNode with a label val and a
list neighbors of the vertices it has an edge to. The copy must hold a new
GraphNode for each reached vertex, with the same val and the same edges,
and must share no GraphNode with the input. Return the copy of graph.

The examples use two harness helpers. build_graph(adj) makes the vertices
1 to len(adj), gives vertex i an edge to each label in adj[i - 1], and
returns vertex 1. get_adj_list(v) lists, in the same form, the edges of the
vertices that v reaches.

Example 1:

Input: graph = build_graph([[2], [3], [1]])
Output: a copy with get_adj_list(copy) == [[2], [3], [1]]

    1 --> 2 --> 3
    ^           |
    '-----------'

Example 2:

Input: graph = build_graph([[2, 3], [3], []])
Output: a copy with get_adj_list(copy) == [[2, 3], [3], []]
Explanation: vertex 3 is reached twice, but the copy holds it once.

    1 --> 2
    |     |
    |     v
    '---> 3

Example 3:

Input: graph = build_graph([[2], [], [1]])
Output: a copy with get_adj_list(copy) == [[2], []]
Explanation: vertex 1 does not reach vertex 3, so the copy has no vertex 3.

Constraints:

    1 <= number of vertices <= 300
    The labels are distinct. A vertex can have an edge to itself.

    REQUIRED: O(n + e) time for n vertices and e edges.
"""


class Solution:
    def clone_graph(self, graph: GraphNode) -> GraphNode:
        pass


sol = Solution()

draw_graphviz({1: [2], 2: [3], 3: [1]}, directed=True)
print(get_adj_list(sol.clone_graph(build_graph([[2], [3], [1]]))))  # [[2], [3], [1]]

# reach = lambda v: ((seen := [v]), [seen.append(w) for u in seen for w in u.neighbors if w not in seen])[0]
# fresh = lambda a, b: not {id(x) for x in reach(a)} & {id(x) for x in reach(b)}
# clone_ok = lambda adj: ((g := build_graph(adj)), (c := sol.clone_graph(g))) and get_adj_list(c) == get_adj_list(g) and len(reach(c)) == len(reach(g)) and fresh(c, g)
# assert get_adj_list(sol.clone_graph(build_graph([[2], [3], [1]]))) == [[2], [3], [1]]
# assert get_adj_list(sol.clone_graph(build_graph([[2, 3], [3], []]))) == [[2, 3], [3], []]
# assert get_adj_list(sol.clone_graph(build_graph([[2], [], [1]]))) == [[2], []]
# assert clone_ok([[2], [3], [1]])
# assert clone_ok([[2, 3], [3], []])
# assert clone_ok([[2], [], [1]])
# assert clone_ok([[]])
# assert clone_ok([[1]])
# assert clone_ok([[2], [1]])
# assert clone_ok([[2, 3, 4], [4], [4], [1]])
# assert clone_ok([[2], [3], [4], [2]])
# assert clone_ok([[i + 2] for i in range(299)] + [[]])
# assert clone_ok([[i + 2] for i in range(299)] + [[1]])
# assert clone_ok([[j for j in range(1, 101) if j != i] for i in range(1, 101)])
