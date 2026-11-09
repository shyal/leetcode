# REFERENCE: d457 EPI 11.5 Compute the real square root
class Solution
  def square_root(x: float) -> float
    lo, hi = min(x, 1.0), max(x, 1.0)
    while hi - lo > 1e-12 * hi
      mid = (lo + hi) / 2
      if mid * mid > x
        hi = mid
      else
        lo = mid
    lo
