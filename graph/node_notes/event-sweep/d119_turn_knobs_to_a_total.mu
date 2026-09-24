# REFERENCE: d119 Turn Knobs To A Total
def numTurns(a: int, b: int, limit: int, T: int) -> int
  def band(a, b)
    (min(a, b) + 1, max(a, b) + limit)

  if a + b == T
    return 0
  lo, hi = band(a, b)
  1 if lo <= T <= hi else 2
