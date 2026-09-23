# REFERENCE: d131 Bottom Up Cell
class Solution:
    def numbered(self, n):
        grid = table(n, n)
        for k in range(n * n):
            r, c = divmod(k, n)
            grid[n - 1 - r][c] = k
        return grid
