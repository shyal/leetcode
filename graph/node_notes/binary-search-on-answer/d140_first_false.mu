# REFERENCE: d140 First False
class Solution
  def firstFalse(lo: int, hi: int, ok: int -> bool) -> int
    while lo < hi
      mid = (lo + hi) // 2
      if ok(mid)
        lo = mid + 1
      else
        hi = mid
    lo
