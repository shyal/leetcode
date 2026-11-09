# REFERENCE: d533 EPI 18.6 Making wired connections
class Solution
  def is_any_placement_feasible(graph: [[int]]) -> bool
    side = table(len(graph), fill=-1)
    for s in 0..<len(graph)
      if side[s] != -1
        continue
      side[s] = 0
      q = deque([s])
      while q
        v = q.popleft()
        for w in graph[v]
          if side[w] == -1
            side[w] = 1 - side[v]
            q <- w
          elif side[w] == side[v]
            return false
    true
