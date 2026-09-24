# REFERENCE: d124 Companies Left
from dsa.union_find import UnionFind
extends UnionFind

def countCompanies() -> int
  count for x, p in self.parent if x == p
