# REFERENCE: d136 Bottom Up Index Alternating
class Solution:
    def numbered(self, n):
        grid = table(n, n)
        for r, c in cells(grid):
            b = n - 1 - r
            k = n - 1 - c if b % 2 else c
            grid[r][c] = b * n + k
        return grid
