# REFERENCE: d119 Turn Knobs To A Total
def numTurns(a: int, b: int, limit: int, V: int) -> int
  def band(a, b)
    (min(a, b) + 1, max(a, b) + limit)

  if a + b == V
    return 0
  lo, hi = band(a, b)
  1 if lo <= V <= hi else 2
