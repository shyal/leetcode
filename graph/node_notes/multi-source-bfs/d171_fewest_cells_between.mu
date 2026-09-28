# REFERENCE: d171 Fewest Cells Between
def fewest(grid: [[int]]) -> int
  q = deque(cells(grid, eq=1))
  for (d, c) in levels(q, seen=set())
    if grid[c] == 2
      return d - 1
    q += nbrs(grid, c)
