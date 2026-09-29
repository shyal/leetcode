# REFERENCE: d174 Longest Path From Zero
def longestPath(G: {int: [int]}) -> int
  memo longest(u) = max((1 + longest(v) for v in G[u]), default=0)
  longest(0)
