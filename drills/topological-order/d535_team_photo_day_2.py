"""
EPI 18.8 Team photo day - 2

Given a directed acyclic graph as an adjacency list graph, where graph[v]
lists the vertices that vertex v has an edge to, return the number of
vertices on a longest path. A path follows the edges in their direction,
and a single vertex is a path of 1 vertex. The vertices are 0 to
len(graph) - 1.

Example 1:

Input: graph = [[1, 2], [3], [3], [], [3]]
Output: 3
Explanation: the path 0 -> 1 -> 3 has 3 vertices. So does 0 -> 2 -> 3.

    0 --> 1 --> 3 <-- 4
    |           ^
    '---> 2 ----'

Example 2:

Input: graph = [[]]
Output: 1

Example 3:

Input: graph = [[], [], []]
Output: 1

Constraints:

    1 <= len(graph) <= 300
    0 <= total number of edges <= 5000
    The graph has no cycle, and no edge appears twice.

    REQUIRED: O(n + e) time for n vertices and e edges.
"""


class Solution:
    def find_largest_number_teams(self, graph: list[list[int]]) -> int:
        pass


sol = Solution()

draw_graphviz({0: [1, 2], 1: [3], 2: [3], 3: [], 4: [3]}, directed=True)
print(sol.find_largest_number_teams([[1, 2], [3], [3], [], [3]]))  # 3

# assert sol.find_largest_number_teams([[1, 2], [3], [3], [], [3]]) == 3
# assert sol.find_largest_number_teams([[]]) == 1
# assert sol.find_largest_number_teams([[], [], []]) == 1
# assert sol.find_largest_number_teams([[1], []]) == 2
# assert sol.find_largest_number_teams([[], [0]]) == 2
# assert sol.find_largest_number_teams([[1], [2], [3], [], [3]]) == 4
# assert sol.find_largest_number_teams([[], [0], [1], [2]]) == 4
# assert sol.find_largest_number_teams([[1], [], [3], [4], []]) == 3
# assert sol.find_largest_number_teams([list(range(1, 10))] + [[] for _ in range(9)]) == 2
# assert sol.find_largest_number_teams([[1, 2], [2], []]) == 3
# assert sol.find_largest_number_teams([[i + 1] for i in range(299)] + [[]]) == 300
# assert sol.find_largest_number_teams([[]] + [[i - 1] for i in range(1, 300)]) == 300
# assert sol.find_largest_number_teams([list(range(i + 1, 100)) for i in range(100)]) == 100
# assert sol.find_largest_number_teams([[10 * (v // 10 + 1) + k for k in range(10)] if v < 290 else [] for v in range(300)]) == 30
