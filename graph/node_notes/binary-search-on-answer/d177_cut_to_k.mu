# REFERENCE: d177 Cut To K
def cutToK(chunks: [[int]], k: int) -> [[int]]
  out = [list(c) for c in chunks]
  while len(out) < k
    for i, c in out
      if len(c) > 1
        out[i:i+1] = [[c[0]], c[1:]]
        break
  out
