# REFERENCE: d136 Bottom Up Index Alternating
def numbered(n: int) -> [[int]]
  grid = table(n, n)
  for (r, c) in cells(grid)
    b = n - 1 - r
    k = n - 1 - c if b % 2 else c
    grid[r][c] = b * n + k
  grid
