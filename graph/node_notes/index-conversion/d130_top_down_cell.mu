# REFERENCE: d130 Top Down Cell
def numbered(n: int) -> [[int]]
  grid = table(n, n)
  for k in 0..<n * n
    r, c = divmod(k, n)
    grid[r][c] = k
  grid
