# REFERENCE: d312 Prefix Letter Sets
class Solution
  def prefixLetterSets(s: str) -> [{str}]
    scan(set.union, [set(c) for c in s], type=list)
