# REFERENCE: d72 Find with Path Compression
from dsa.union_find import UnionFind
extends UnionFind

def find(x: int) -> int
  if x != self.parent[x]
    self.parent[x] = self.find(self.parent[x])
  self.parent[x]
