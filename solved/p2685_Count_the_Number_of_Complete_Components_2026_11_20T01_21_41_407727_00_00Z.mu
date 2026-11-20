# URL: https://leetcode.com/problems/count-the-number-of-complete-components/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2685. Count the Number of Complete Components
#
# You are given an integer n. There is an undirected graph with n vertices, numbered from 0 to n - 1. You are given a 2D integer array edges where edges[i] = [a_i, b_i] denotes that there exists an undirected edge connecting vertices a_i and b_i.
#
# Return the number of complete connected components of the graph.
#
# A connected component is a subgraph of a graph in which there exists a path between any two vertices, and no vertex of the subgraph shares an edge with a vertex outside of the subgraph.
#
# A connected component is said to be complete if there exists an edge between every pair of its vertices.
#
# Example 1:
#
# Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4]]
# Output: 3
# Explanation: From the picture above, one can see that all of the components of this graph are complete.
#
# Example 2:
#
# Input: n = 6, edges = [[0,1],[0,2],[1,2],[3,4],[3,5]]
# Output: 1
# Explanation: The component containing vertices 0, 1, and 2 is complete since there is an edge between every pair of two vertices. On the other hand, the component containing vertices 3, 4, and 5 is not complete since there is no edge between vertices 4 and 5. Thus, the number of complete components in this graph is 1.
#
# Constraints:
#
#     1 <= n <= 50
#     0 <= edges.length <= n * (n - 1) / 2
#     edges[i].length == 2
#     0 <= a_i, b_i <= n - 1
#     a_i != b_i
#     There are no repeated edges.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# LEETCODE: Accepted (65 ms, 20 MB)

class Solution
  def countCompleteComponents(n: int, edges: [[int]]) -> int
    G = adjacency(edges, n, directed=false)
    ret num_connected = 0
    for comps in components(0..<n, u -> G[u])
      g = {u: G[u] for u in comps}
      num_connected += all(len(g[c]) == len(comps) -1 for c in comps)


sol = Solution()

print(sol.countCompleteComponents(6, [[0, 1], [0, 2], [1, 2], [3, 4]]))  # 3

assert uses(Solution, adjacency)
assert sol.countCompleteComponents(6, [[0, 1], [0, 2], [1, 2], [3, 4]]) == 3
assert sol.countCompleteComponents(6, [[0, 1], [0, 2], [1, 2], [3, 4], [3, 5]]) == 1
assert Solution().countCompleteComponents(1, []) == 1
assert Solution().countCompleteComponents(2, []) == 2
assert Solution().countCompleteComponents(2, [[0, 1]]) == 1
assert Solution().countCompleteComponents(3, [[0, 1], [1, 2]]) == 0
assert Solution().countCompleteComponents(3, [[0, 1], [1, 2], [0, 2]]) == 1
assert Solution().countCompleteComponents(4, [[0, 1], [1, 2], [2, 3]]) == 0
assert Solution().countCompleteComponents(4, [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3], [0, 3]]) == 1
assert Solution().countCompleteComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4], [0, 2], [1, 3]]) == 0
assert Solution().countCompleteComponents(50, []) == 50
assert Solution().countCompleteComponents(50, [[i, i + 1] for i in 0..<49]) == 0
assert Solution().countCompleteComponents(50, [[i, j] for i in 0..<50 for j in i + 1..<50]) == 1
assert Solution().countCompleteComponents(50, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]]) == 46
