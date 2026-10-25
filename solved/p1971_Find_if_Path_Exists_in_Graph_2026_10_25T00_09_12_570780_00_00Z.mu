# URL: https://leetcode.com/problems/find-if-path-exists-in-graph/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1971. Find if Path Exists in Graph
#
# There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1 (inclusive). The edges in the graph are represented as a 2D integer array edges, where each edges[i] = [u_i, v_i] denotes a bi-directional edge between vertex u_i and vertex v_i. Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.
#
# You want to determine if there is a valid path that exists from vertex source to vertex destination.
#
# Given edges and the integers n, source, and destination, return true if there is a valid path from source to destination, or false otherwise.
#
# Example 1:
#
# Input: n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2
# Output: true
# Explanation: There are two paths from vertex 0 to vertex 2:
# - 0 -> 1 -> 2
# - 0 -> 2
#
# Example 2:
#
# Input: n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5
# Output: false
# Explanation: There is no path from vertex 0 to vertex 5.
#
# Constraints:
#
#     1 <= n <= 2 * 10^5
#     0 <= edges.length <= 2 * 10^5
#     edges[i].length == 2
#     0 <= u_i, v_i <= n - 1
#     u_i != v_i
#     0 <= source, destination <= n - 1
#     There are no duplicate edges.
#     There are no self edges.
#
# ---
# LEETCODE: Accepted (507 ms, 105.2 MB)

# mu 0.12

class Solution
  def validPath(n: int, edges: [[int]], source: int, destination: int) -> bool
    G = adjacency(edges, n, directed=False)
    q = deque([source])
    seen = set([])
    while q
      node = q.popleft()
      if node in seen
        continue
      if node == destination
        return true
      seen.add(node)
      for next in G[node]
        q <- next
    false

sol = Solution()

print(sol.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2))  # True

assert uses(Solution, adjacency)
assert sol.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2) == true
assert sol.validPath(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5) == false

assert sol.validPath(1, [], 0, 0) == true
assert sol.validPath(2, [], 0, 1) == false
assert sol.validPath(2, [[0, 1]], 0, 1) == true
assert sol.validPath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 0, 4) == true
assert sol.validPath(5, [[0, 1], [1, 2], [2, 3]], 0, 4) == false
assert sol.validPath(4, [[0, 1], [1, 2], [2, 3], [3, 0]], 3, 1) == true
assert sol.validPath(4, [[0, 1], [1, 2], [2, 3]], 3, 0) == true
assert sol.validPath(3, [[0, 1], [1, 2]], 2, 0) == true
assert sol.validPath(10, [[i, i + 1] for i in 0..<9], 0, 9) == true
assert sol.validPath(10 ** 5, [[i, i + 1] for i in 0..<10 ** 5 - 1], 0, 10 ** 5 - 1) == true
assert sol.validPath(10 ** 5, [], 0, 10 ** 5 - 1) == false
assert sol.validPath(3, [[0, 1], [1, 2]], 0, 0) == true
