# REFERENCE: d182 Bottom Up Cell Alternating
def numbered(n: int) -> [[int]]
  grid = table(n, n)
  for k in 0..<n * n
    b, c = divmod(k, n)
    c = n - 1 - c if b % 2 else c
    grid[n - 1 - b][c] = k
  grid
