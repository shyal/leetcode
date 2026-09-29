# REFERENCE: d172 Node Distance Pairs
def distances(G: {int: [int]}) -> {(int, int)}
  dist = {0: 0}
  q = deque([0])
  while q
    node = q.popleft()
    for nxt in G[node]
      if nxt not in dist
        dist[nxt] = dist[node] + 1
        q <- nxt
  set(dist.items())
