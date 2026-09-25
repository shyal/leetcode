# 743. Network Delay Time
def networkDelayTime(times: [(int, int, int)], n: int, k: int) -> int
  d = dijkstra(graph(1..n, times, directed=true), k)
  t = max for v in 1..n: d[v]
  t if t < inf else -1
