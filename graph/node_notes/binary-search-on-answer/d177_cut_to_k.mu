# REFERENCE: d177 Cut To K
def cutToK(chunks: [[int]], k: int) -> [[int]]
  while len(chunks) < k
    for i, c in chunks
      if len(c) > 1
        chunks[i:i+1] = [[c[0]], c[1:]]
        break
  chunks
