# REFERENCE: d512 EPI 16.5 Search for a sequence in a 2D array
class Solution
  def is_pattern_contained_in_grid(grid: [[int]], pattern: [int]) -> bool
    if not pattern
      return true
    m, n = len(grid), len(grid[0])
    ends = {(i, j) for i in 0..<m for j in 0..<n if grid[i][j] == pattern[0]}
    for x in pattern[1:]
      ends = {(a, b) for i, j in ends for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if 0 <= a < m and 0 <= b < n and grid[a][b] == x}
    bool(ends)
