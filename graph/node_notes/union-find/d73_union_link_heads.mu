# REFERENCE: d73 Union Links Head to Head
from dsa.union_find import UnionFind
extends UnionFind

def union(a: int, b: int) -> bool
  rootx, rooty = self.find(a), self.find(b)
  if rootx == rooty
    return false
  self.parent[rootx] = rooty
  true
