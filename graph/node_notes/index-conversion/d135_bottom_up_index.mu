# REFERENCE: d135 Bottom Up Index
def numbered(n: int) -> [[int]]
  grid = table(n, n)
  for (r, c) in cells(grid)
    grid[r][c] = (n - 1 - r) * n + c
  grid
