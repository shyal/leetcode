"""
EPI 18.4 Deadlock detection

Given a directed graph as an adjacency list graph, where graph[v] lists
the vertices that vertex v has an edge to, return True when the graph has
a cycle and False otherwise. The vertices are 0 to len(graph) - 1.

Example 1:

Input: graph = [[1], [2], [3, 4], [1], []]
Output: True
Explanation: the edges 1 -> 2, 2 -> 3 and 3 -> 1 make a cycle.

    0 --> 1 --> 2 --> 4
          ^     |
          |     v
          '---- 3

Example 2:

Input: graph = [[1, 2], [2], []]
Output: False
Explanation: two paths go from 0 to 2, but no path comes back.

Example 3:

Input: graph = [[0]]
Output: True
Explanation: the edge 0 -> 0 is a cycle.

Constraints:

    1 <= len(graph) <= 300
    0 <= total number of edges <= 5000
    0 <= graph[v][i] < len(graph), and no edge appears twice.

    REQUIRED: O(n + e) time for n vertices and e edges.
"""


class Solution:
    def is_deadlocked(self, graph: list[list[int]]) -> bool:
        pass


sol = Solution()

draw_graphviz({0: [1], 1: [2], 2: [3, 4], 3: [1], 4: []}, directed=True)
print(sol.is_deadlocked([[1], [2], [3, 4], [1], []]))  # True

# assert sol.is_deadlocked([[1], [2], [3, 4], [1], []]) is True
# assert sol.is_deadlocked([[1, 2], [2], []]) is False
# assert sol.is_deadlocked([[0]]) is True
# assert sol.is_deadlocked([[]]) is False
# assert sol.is_deadlocked([[], []]) is False
# assert sol.is_deadlocked([[1], [0]]) is True
# assert sol.is_deadlocked([[1], [2], []]) is False
# assert sol.is_deadlocked([[1], [2], [0]]) is True
# assert sol.is_deadlocked([[], [0], [1]]) is False
# assert sol.is_deadlocked([[1], [], [3], [4], [2]]) is True
# assert sol.is_deadlocked([[1, 2], [3], [3], []]) is False
# assert sol.is_deadlocked([[1, 2], [], [1]]) is False
# assert sol.is_deadlocked([[], [], [2]]) is True
# assert sol.is_deadlocked([[i + 1] for i in range(299)] + [[]]) is False
# assert sol.is_deadlocked([[]] + [[i - 1] for i in range(1, 300)]) is False
# assert sol.is_deadlocked([[(i + 1) % 300] for i in range(300)]) is True
# assert sol.is_deadlocked([list(range(i + 1, 100)) for i in range(100)]) is False
# assert sol.is_deadlocked([list(range(i + 1, 100)) for i in range(99)] + [[0]]) is True
