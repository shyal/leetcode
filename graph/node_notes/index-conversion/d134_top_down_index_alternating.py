# REFERENCE: d134 Top Down Index Alternating
class Solution:
    def numbered(self, n):
        grid = table(n, n)
        for r, c in cells(grid):
            k = n - 1 - c if r % 2 else c
            grid[r][c] = r * n + k
        return grid
