# REFERENCE: d553 Sums With A Lower Bound
class Solution
  def sumsFrom(n: int, k: int, m: int) -> int
    n < m ? 0 : comb(n - m + k - 1, k - 1)
