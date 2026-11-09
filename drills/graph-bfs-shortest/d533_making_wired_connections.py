"""
EPI 18.6 Making wired connections

Given an undirected graph as an adjacency list graph, where graph[v] lists
the neighbors of vertex v, return True when the vertices can be split into
two sets such that each edge joins a vertex of one set to a vertex of the
other set. Return False otherwise. Each edge is in the lists of both of
its ends, and the vertices are 0 to len(graph) - 1.

Example 1:

Input: graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
Output: True
Explanation: the sets {0, 2} and {1, 3} work.

    0 --- 1
    |     |
    3 --- 2

Example 2:

Input: graph = [[1, 2], [0, 2], [0, 1]]
Output: False
Explanation: two of the three vertices are in the same set, and an edge
joins them.

Example 3:

Input: graph = [[]]
Output: True

Constraints:

    1 <= len(graph) <= 300
    0 <= total number of edges <= 5000
    No edge joins a vertex to itself, and no edge appears twice.
    The graph can have more than one component.

    REQUIRED: O(n + e) time for n vertices and e edges.
"""


class Solution:
    def is_any_placement_feasible(self, graph: list[list[int]]) -> bool:
        pass


sol = Solution()

draw_graphviz({0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2]})
print(sol.is_any_placement_feasible([[1, 3], [0, 2], [1, 3], [0, 2]]))  # True

# ring = lambda n: [[(v - 1) % n, (v + 1) % n] for v in range(n)]
# line = lambda n: [[w for w in (v - 1, v + 1) if 0 <= w < n] for v in range(n)]
# assert sol.is_any_placement_feasible([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
# assert sol.is_any_placement_feasible([[1, 2], [0, 2], [0, 1]]) is False
# assert sol.is_any_placement_feasible([[]]) is True
# assert sol.is_any_placement_feasible([[], []]) is True
# assert sol.is_any_placement_feasible([[1], [0]]) is True
# assert sol.is_any_placement_feasible(line(5)) is True
# assert sol.is_any_placement_feasible(ring(5)) is False
# assert sol.is_any_placement_feasible(ring(6)) is True
# assert sol.is_any_placement_feasible([[1], [0], [3, 4], [2, 4], [2, 3]]) is False
# assert sol.is_any_placement_feasible([[1, 2], [0, 2], [0, 1], [4], [3]]) is False
# assert sol.is_any_placement_feasible([[1, 2, 3, 4], [0], [0], [0], [0]]) is True
# assert sol.is_any_placement_feasible([[3, 4, 5], [3, 4, 5], [3, 4, 5], [0, 1, 2], [0, 1, 2], [0, 1, 2]]) is True
# assert sol.is_any_placement_feasible([[3, 4, 5], [3, 4, 5, 2], [3, 4, 5, 1], [0, 1, 2], [0, 1, 2], [0, 1, 2]]) is False
# assert sol.is_any_placement_feasible(line(300)) is True
# assert sol.is_any_placement_feasible(ring(300)) is True
# assert sol.is_any_placement_feasible(ring(299)) is False
# assert sol.is_any_placement_feasible(line(297) + [[298, 299], [297, 299], [297, 298]]) is False
# assert sol.is_any_placement_feasible([[w for w in range(100) if w % 2 != v % 2] for v in range(100)]) is True
