# REFERENCE: d313 Prefix Distinct Counts
class Solution
  def prefixDistinctCounts(s: str) -> [int]
    [len(p) for p in scan(set.union, [set(c) for c in s])]
