# REFERENCE: d144 Floor True
def floorTrue(lo: int, hi: int, ok: int -> bool) -> int
  while lo <= hi
    mid = (lo + hi) // 2
    if ok(mid)
      lo = mid + 1
    else
      hi = mid - 1
  hi
