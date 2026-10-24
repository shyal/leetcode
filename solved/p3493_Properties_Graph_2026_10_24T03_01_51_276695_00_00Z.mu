# URL: https://leetcode.com/problems/properties-graph/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3493. Properties Graph
#
# You are given a 2D integer array properties having dimensions n x m and an integer k.
#
# Define a function intersect(a, b) that returns the number of distinct integers common to both arrays a and b.
#
# Construct an undirected graph where each index i corresponds to properties[i]. There is an edge between node i and node j if and only if intersect(properties[i], properties[j]) >= k, where i and j are in the range [0, n - 1] and i != j.
#
# Return the number of connected components in the resulting graph.
#
# Example 1:
#
# Input: properties = [[1,2],[1,1],[3,4],[4,5],[5,6],[7,7]], k = 1
# Output: 3
# Explanation:
# The graph formed has 3 connected components:
#
# Example 2:
#
# Input: properties = [[1,2,3],[2,3,4],[4,3,5]], k = 2
# Output: 1
# Explanation:
# The graph formed has 1 connected component:
#
# Example 3:
#
# Input: properties = [[1,1],[1,1]], k = 2
# Output: 2
# Explanation:
# intersect(properties[0], properties[1]) = 1, which is less than k. This means there is no edge between properties[0] and properties[1] in the graph.
#
# Constraints:
#
#     1 <= n == properties.length <= 100
#     1 <= m == properties[i].length <= 100
#     1 <= properties[i][j] <= 100
#     1 <= k <= m
#
# ---

# mu 0.12

class Solution
  def numberOfComponents(properties: [[int]], k: int) -> int
    def intersect(a, b)
      len(set(a) & set(b))
    G = {:set}
    n = len properties
    for i in 0..<n
      for j in 0..<n
        if i != j
          if intersect(properties[i], properties[j]) >= k
            G[i].add(j)
            G[j].add(i)
    seen = set([])
    def dfs(n)
      if n in seen
        return
      seen.add(n)
      for next in G[n]
        dfs(next)
    ret count = 0
    for i in 0..<n
      count += i not in seen
      dfs(i)


sol = Solution()
print(sol.numberOfComponents([[1, 2, 3], [2, 3, 4], [4, 3, 5]], 2))
print(sol.numberOfComponents([[1, 2], [1, 1], [3, 4], [4, 5], [5, 6], [7, 7]], 1))  # 3

# # assert uses(Solution, adjacency)
assert sol.numberOfComponents([[1, 2], [1, 1], [3, 4], [4, 5], [5, 6], [7, 7]], 1) == 3
assert sol.numberOfComponents([[1, 2, 3], [2, 3, 4], [4, 3, 5]], 2) == 1
assert sol.numberOfComponents([[1, 1], [1, 1]], 2) == 2

assert sol.numberOfComponents([[1]], 1) == 1
assert sol.numberOfComponents([[1], [1], [1]], 1) == 1
assert sol.numberOfComponents([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1) == 3
assert sol.numberOfComponents([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]], 3) == 4
assert sol.numberOfComponents([[1] * 100] * 100, 100) == 100
assert sol.numberOfComponents([[i for i in 1..<101] for _ in 0..<100], 100) == 1
assert sol.numberOfComponents([[i for i in 1..<101], [i for i in 51..<151]], 50) == 1
assert sol.numberOfComponents([[1, 2, 3], [1, 2, 3], [1, 2, 3]], 3) == 1
assert sol.numberOfComponents([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3]], 2) == 3
assert sol.numberOfComponents([[1, 2, 3], [3, 4, 5], [5, 6, 7], [7, 8, 9]], 1) == 1
assert sol.numberOfComponents([[1, 2, 3], [3, 4, 5], [5, 6, 7], [7, 8, 9]], 2) == 4
assert sol.numberOfComponents([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], 5) == 3
