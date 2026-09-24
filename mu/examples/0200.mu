# 200. Number of Islands
def numIslands(grid: [[char]]) -> int
  land = {p for p in cells(grid) if grid[p] == '1'}
  len(components(land, p -> nbrs(grid, p)))
