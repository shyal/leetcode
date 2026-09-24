# REFERENCE: d125 Companies Among
from dsa.union_find import UnionFind
extends UnionFind

def countCompaniesAmong(employees: [int]) -> int
  len({self.find(x) for x in employees})
