"""
DRILL: Component Count After Each Union
TRAINS: union-find

Given n nodes labeled 0..n-1 and a list of undirected edges, process the
edges in order and return a list where res[i] is the number of connected
components after processing edges[0..i].

An edge between two already-connected nodes changes nothing — the count
stays flat.

Example 1:

Input: n = 4, edges = [[0,1],[0,2],[1,2]]
Output: [3, 2, 2]
Explanation:
    [0,1] -> {0,1} {2} {3}        -> 3 components
    [0,2] -> {0,1,2} {3}          -> 2 components
    [1,2] -> already connected    -> still 2

Example 2:

Input: n = 3, edges = [[0,1],[1,2]]
Output: [2, 1]

Constraints:

    1 <= n <= 1000
    0 <= len(edges) <= 2000
    0 <= u, v < n

    REQUIRED: union-find (parent array + find + union), not BFS/DFS.
    find compresses the path; union links root to root.
"""


class Solution:
    def componentCounts(self, n: int, edges: list[list[int]]) -> list[int]:
        pass


sol = Solution()

assert sol.componentCounts(4, [[0, 1], [0, 2], [1, 2]]) == [3, 2, 2]
assert sol.componentCounts(3, [[0, 1], [1, 2]]) == [2, 1]
assert sol.componentCounts(5, []) == []
assert sol.componentCounts(6, [[0, 1], [2, 3], [4, 5], [0, 2], [3, 5]]) == [5, 4, 3, 2, 1]
assert sol.componentCounts(4, [[0, 1], [1, 0], [2, 3], [0, 3]]) == [3, 3, 2, 1]
assert sol.componentCounts(1, []) == []
assert sol.componentCounts(2, [[0, 1], [0, 1]]) == [1, 1]

print("All tests passed!")
