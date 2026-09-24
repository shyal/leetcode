# REFERENCE: d71 How Many Companies
from dsa.union_find import UnionFind
extends UnionFind

def countCompanies(pairs: [[int]]) -> int
  len(self.parent) - (count for (a, b) in pairs if self.union(a, b))
