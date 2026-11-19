# REFERENCE: d552 Sums Of K Parts
class Solution
  def sums(n: int, k: int) -> int
    comb(n + k - 1, k - 1)
