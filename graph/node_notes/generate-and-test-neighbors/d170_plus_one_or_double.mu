# REFERENCE: d170 Plus One Or Double
def fewest(a: int, b: int, limit: int) -> int
  q = deque([a])
  for (d, x) in levels(q, seen=set(), lte=limit)
    if x == b
      return d
    q += [x + 1, 2 * x]
  -1
