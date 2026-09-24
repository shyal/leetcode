# REFERENCE: d6 Triples
def triples(n: int) -> [[int]]
  [[a, b, c] for a in 0..<n for b in a + 1..<n for c in b + 1..<n]
