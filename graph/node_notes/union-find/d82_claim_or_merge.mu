# REFERENCE: d82 Claim Or Merge
from dsa.union_find import UnionFind
extends UnionFind

def union_shared(accounts: [[str]]) -> {str: int}
  owner = {}
  for x, emails in accounts
    for email in emails
      first = owner.setdefault(email, x)
      if first != x
        self.union(x, first)
  owner
