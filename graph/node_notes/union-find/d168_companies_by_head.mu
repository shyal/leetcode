# REFERENCE: d168 Companies By Head
from dsa.union_find import UnionFind
extends UnionFind

def groups() -> {int: [int]}
  g = defaultdict(list)
  for x in 0..<len(self.parent)
    g[self.find(x)].append(x)
  g
