# REFERENCE: d79 Clubs Sharing A Member
def clubGraph(n: int, clubs_of: {int: [int]}) -> [[int]]
  adj = [set() for _ in 0..<n]
  for clubs in clubs_of.values()
    for a in clubs
      for b in clubs
        if a != b
          adj[a].add(b)
  [list(s) for s in adj]
