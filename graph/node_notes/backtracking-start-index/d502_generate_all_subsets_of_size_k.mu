# REFERENCE: d502 EPI 15.6 Generate all subsets of size k
class Solution
  def combinations(n: int, k: int) -> [[int]]
    ret out, subset = []..
    def grow(start)
      if len(subset) == k
        out <- subset[:]
        return
      for x in start..n - (k - len(subset)) + 1
        subset <- x
        grow(x + 1)
        subset .
    grow(1)
