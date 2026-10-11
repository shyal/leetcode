# REFERENCE: d133 Top Down Index
class Solution
  def numbered(n: int) -> [[int]]
    grid = table(n, n)
    for (r, c) in cells(grid)
      grid[r][c] = r * n + c
    grid
