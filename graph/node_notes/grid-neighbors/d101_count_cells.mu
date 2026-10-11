# REFERENCE: d101 Count Cells
class Solution
  def count(grid: [[int]], v: int) -> int
    count for p in cells(grid) if grid[p] == v
