# REFERENCE: d101 Count Cells
def count(grid: [[int]], v: int) -> int
  count for p in cells(grid) if grid[p] == v
