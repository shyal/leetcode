# REFERENCE: d102 Neighbour Values
def neighbour_values(grid: [[int]], r: int, c: int) -> [int]
  [grid[p] for p in nbrs(grid, r, c)]
