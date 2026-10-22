# URL: https://leetcode.com/problems/find-closest-node-to-given-two-nodes/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2359. Find Closest Node to Given Two Nodes
#
# You are given a directed graph of n nodes numbered from 0 to n - 1, where each node has at most one outgoing edge.
#
# The graph is represented with a given 0-indexed array edges of size n, indicating that there is a directed edge from node i to node edges[i]. If there is no outgoing edge from i, then edges[i] == -1.
#
# You are also given two integers node1 and node2.
#
# Return the index of the node that can be reached from both node1 and node2, such that the maximum between the distance from node1 to that node, and from node2 to that node is minimized. If there are multiple answers, return the node with the smallest index, and if no possible answer exists, return -1.
#
# Note that edges may contain cycles.
#
# Example 1:
#
# Input: edges = [2,2,3,-1], node1 = 0, node2 = 1
# Output: 2
# Explanation: The distance from node 0 to node 2 is 1, and the distance from node 1 to node 2 is 1.
# The maximum of those two distances is 1. It can be proven that we cannot get a node with a smaller maximum distance than 1, so we return node 2.
#
# Example 2:
#
# Input: edges = [1,2,-1], node1 = 0, node2 = 2
# Output: 2
# Explanation: The distance from node 0 to node 2 is 2, and the distance from node 2 to itself is 0.
# The maximum of those two distances is 2. It can be proven that we cannot get a node with a smaller maximum distance than 2, so we return node 2.
#
# Constraints:
#
#     n == edges.length
#     2 <= n <= 10^5
#     -1 <= edges[i] < n
#     edges[i] != i
#     0 <= node1, node2 < n
#
# ---
# LEETCODE: Accepted (604 ms, 62.5 MB)

# mu 0.12

class Solution
  def closestMeetingNode(edges: [int], node1: int, node2: int) -> int
    G = {}
    for >i, n in edges
      if n != -1
        G[i] = n
    def bfs(n)
      q = deque([n])
      seen = set([])
      dists = {:int}
      for d, node in levels(q, seen=seen)
        dists[node] = d
        if node in G
          q <- G[node]
      return dists
    
    one_dists = bfs(node1)
    two_dists = bfs(node2)
    max_distances = {}
    for >i in edges
      if i in one_dists and i in two_dists
        max_distances[i] = max(one_dists[i], two_dists[i])
    if not max_distances
      return -1
    min_max = min(max_distances.items(), key = x -> (x[1], x[0]))[0]
    return min_max
    

sol = Solution()


print(sol.closestMeetingNode([-1, -1], 0, 1))


# print(sol.closestMeetingNode([2, 2, 3, -1], 0, 1))  # 2

assert sol.closestMeetingNode([2, 2, 3, -1], 0, 1) == 2
assert sol.closestMeetingNode([1, 2, -1], 0, 2) == 2

assert sol.closestMeetingNode([-1, -1], 0, 1) == -1
assert sol.closestMeetingNode([1, 2, 3, 4, -1], 0, 4) == 4
assert sol.closestMeetingNode([1, 2, 3, 4, 0], 0, 2) == 2
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 0, 9) == 9
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 0, 5) == 0
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 9, 9) == 9
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 5, 6) == 6
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 0, 0) == 0
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 1, 2) == 2
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 8, 7) == 8
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, -1], 0, 9) == 9
assert sol.closestMeetingNode([1, 2, 3, 4, 5, 6, 7, 8, 9, 9], 0, 9) == 9
