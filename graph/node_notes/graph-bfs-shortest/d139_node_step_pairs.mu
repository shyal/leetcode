# REFERENCE: d139 Node Step Pairs
def reachable(G: {int: [int]}, k: int) -> {(int, int)}
  seen = {(0, 0)}
  q = deque([0])
  for (d, node) in levels(q)
    for nxt in G[node]
      if d < k and (nxt, d + 1) not in seen
        seen.add((nxt, d + 1))
        q <- nxt
  seen
