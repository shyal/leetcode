"""
URL: https://leetcode.com/problems/graph-valid-tree/description/

261. Graph Valid Tree

You are given a graph with n nodes labeled from 0 to n-1. You also receive a list of edges where each edge edges[i] = [ai, bi] represents an undirected connection between nodes ai and bi.

Your task is to determine if these edges form a valid tree. Return true if the graph is a valid tree, and false otherwise.

A valid tree must satisfy these properties:
- It must be connected (all nodes are reachable from any other node)
- It must have no cycles (there's exactly one path between any two nodes)
- For n nodes, a tree must have exactly n-1 edges

Example 1:

Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: true
Explanation: The graph forms a tree: Node 0 connects to 1, 2, 3; Node 1 connects to 4. All nodes are reachable, there are no cycles, and the number of edges equals 4 (= 5-1).

Example 2:

Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
Output: false
Explanation: The first four edges already form a cycle (0-1-2-3-1). Adding the edge [1,4] does not remove the cycle, so the graph is not a tree.

Constraints:

    1 <= n <= 2000
    0 <= edges.length <= 5000
    edges[i].length == 2
    0 <= ai, bi < n
    ai != bi
    There are no repeated edges.
"""


class Solution:

    def graphValidTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parents = [i for i in range(n)]

        def find(x):
            if x != parents[x]:
                parents[x] = find(parents[x])
            return parents[x]

        for x, y in edges:
            rootx, rooty = find(x), find(y)
            if rootx == rooty:
                return False
            parents[rootx] = rooty

        return True


sol = Solution()
assert sol.graphValidTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) == True
assert sol.graphValidTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) == False
assert sol.graphValidTree(1, []) == True
assert sol.graphValidTree(2, []) == False
assert sol.graphValidTree(2, [[0, 1]]) == True
assert sol.graphValidTree(2, [[1, 0]]) == True
assert sol.graphValidTree(4, [[0, 1], [1, 2], [2, 3]]) == True
assert sol.graphValidTree(4, [[0, 1], [1, 2], [2, 0]]) == False
assert sol.graphValidTree(4, [[0, 1], [2, 3]]) == False
assert sol.graphValidTree(6, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]) == True
assert sol.graphValidTree(6, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]) == False
assert sol.graphValidTree(3, [[0, 1]]) == False
assert sol.graphValidTree(4, [[0, 1], [0, 2], [0, 3]]) == True
assert sol.graphValidTree(5, [[0, 1], [1, 2], [2, 0], [3, 4]]) == False
