# DRILL: Minimum Path Cost
#
# G is a dict mapping integer nodes to dicts of {neighbour: weight}; s and t are the start and target nodes. Treat G as a directed graph. Return the minimum path cost, the sum of edge weights, from s to t, or -1 if t is unreachable. Return 0 when s equals t. Use Dijkstra's algorithm.
#
# Example 1:
#
# Input: G={0: {1: 2, 2: 9}, 1: {2: 3}, 2: {}}, s=0, t=2
# Output: 5
#
#     0 --2--> 1 --3--> 2
#     |                 ^
#     +--------9--------+
#
# Explanation: 0 -> 1 -> 2 costs 2 + 3 = 5; breadth-first search selects 0 -> 2, costing 9.
#
# Example 2:
#
# Input: G={0: {1: 4}, 1: {}, 2: {}}, s=0, t=2
# Output: -1
#
#     0 --4--> 1     2
#
# Explanation: No path reaches 2 from 0, so return -1.
#
# Example 3:
#
# Input: G={0: {1: 7}, 1: {}}, s=1, t=1
# Output: 0
#
#     0 --7--> 1
#
# Explanation: The empty path from 1 to itself costs 0.
#
# Constraints:
#
#     1 <= n = len(G) <= 10.
#     Node keys are exactly the integers 0 through n - 1.
#     Every neighbour is a node key in G.
#     0 <= m <= n * (n - 1), where m counts directed edges.
#     Each edge connects distinct nodes.
#     Every weight is an integer from 0 through 20.
#     s and t are integer node keys in G.
#
#     REQUIRED: You must achieve O((n + m) log n) time and avoid Example 1's breadth-first-search error: fewer edges cost more than more edges.
#
# ---

# mu 0.12

class Solution
  def min_cost(G: {int: {int: int}}, s: int, t: int) -> int
    q = heap([(0, s)])
    seen = set([])
    while q
      weight, node = q.pop()
      if node in seen
        continue
      if node == t
        return weight
      seen.add node
      for next in G[node]
        q <- (weight + G[node][next], next)
    -1

sol = Solution()

G = {0: {1: 2, 2: 9}, 1: {2: 3}, 2: {}}
draw_graphviz(G, type='directed')
print(sol.min_cost(G, 0, 2))  # 5

assert sol.min_cost({0: {1: 2, 2: 9}, 1: {2: 3}, 2: {}}, 0, 2) == 5
assert sol.min_cost({0: {1: 4}, 1: {}, 2: {}}, 0, 2) == -1
assert sol.min_cost({0: {1: 7}, 1: {}}, 1, 1) == 0
assert sol.min_cost({0: {1: 7}, 1: {}}, 1, 0) == -1
assert sol.min_cost({0: {1: 0}, 1: {2: 0}, 2: {}}, 0, 2) == 0
assert sol.min_cost({0: {1: 10, 2: 1}, 1: {3: 1}, 2: {1: 1}, 3: {}}, 0, 3) == 3
assert sol.min_cost({0: {1: 1}, 1: {0: 1, 2: 5}, 2: {}}, 0, 2) == 6
assert sol.min_cost({0: {1: 1, 3: 20}, 1: {2: 1}, 2: {3: 1}, 3: {}}, 0, 3) == 3
assert sol.min_cost({0: {1: 3}, 1: {2: 3}, 2: {3: 3}, 3: {}}, 0, 3) == 9
assert sol.min_cost({0: {}}, 0, 0) == 0
