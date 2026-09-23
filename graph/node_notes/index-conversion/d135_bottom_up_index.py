# REFERENCE: d135 Bottom Up Index
class Solution:
    def numbered(self, n):
        grid = table(n, n)
        for r, c in cells(grid):
            grid[r][c] = (n - 1 - r) * n + c
        return grid
