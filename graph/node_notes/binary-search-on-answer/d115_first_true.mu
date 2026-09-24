# REFERENCE: d115 First True
def firstTrue(lo: int, hi: int, ok: int -> bool) -> int
  while lo < hi
    mid = (lo + hi) // 2
    if ok(mid)
      hi = mid
    else
      lo = mid + 1
  lo
