# REFERENCE: d103 Neighbour Counts
def neighbour_counts(grid: [[int]]) -> [[int]]
  out = like(grid)
  for (r, c) in cells(grid)
    out[r][c] = count for _ in nbrs(grid, r, c)
  out
