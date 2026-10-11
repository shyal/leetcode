# REFERENCE: d120 Last True
class Solution
  def lastTrue(lo: int, hi: int, ok: int -> bool) -> int
    while lo < hi
      mid = (lo + hi + 1) // 2
      if ok(mid)
        lo = mid
      else
        hi = mid - 1
    lo
