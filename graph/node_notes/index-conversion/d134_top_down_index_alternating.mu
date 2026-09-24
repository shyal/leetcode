# REFERENCE: d134 Top Down Index Alternating
def numbered(n: int) -> [[int]]
  grid = table(n, n)
  for (r, c) in cells(grid)
    k = n - 1 - c if r % 2 else c
    grid[r][c] = r * n + k
  grid
