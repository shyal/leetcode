# REFERENCE: d131 Bottom Up Cell
def numbered(n: int) -> [[int]]
  grid = table(n, n)
  for k in 0..<n * n
    r, c = divmod(k, n)
    grid[n - 1 - r][c] = k
  grid
