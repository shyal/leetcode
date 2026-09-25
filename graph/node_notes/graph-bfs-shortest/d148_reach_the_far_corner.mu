# REFERENCE: d148 Reach The Far Corner
def reach(grid: [[int]], k: int) -> bool
  if grid[0][0] < k
    return false
  q = deque([(0, 0)])
  seen = {(0, 0)}
  for (_, c) in levels(q)
    for (i, j) in nbrs(grid, c)
      if (i, j) in seen or grid[i][j] < k
        continue
      seen.add((i, j))
      q <- (i, j)
  (len(grid) - 1, len(grid[0]) - 1) in seen
