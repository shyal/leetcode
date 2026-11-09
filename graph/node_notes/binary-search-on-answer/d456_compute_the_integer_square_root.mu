# REFERENCE: d456 EPI 11.4 Compute the integer square root
class Solution
  def square_root(k: int) -> int
    lo, hi = 0, k
    while lo < hi
      mid = (lo + hi + 1) // 2
      if mid * mid <= k
        lo = mid
      else
        hi = mid - 1
    lo
