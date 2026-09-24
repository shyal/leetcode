# REFERENCE: d114 Sections Under Cap
def sections(weights: [int], cap: int) -> int
  count, total = 1, 0
  for w in weights
    if total + w > cap
      count += 1
      total = 0
    total += w
  count
