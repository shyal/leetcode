# REFERENCE: d141 Last False
def lastFalse(lo: int, hi: int, ok: int -> bool) -> int
  while lo < hi
    mid = (lo + hi + 1) // 2
    if ok(mid)
      hi = mid - 1
    else
      lo = mid
  lo
