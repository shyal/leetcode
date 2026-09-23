# REFERENCE: d130 Top Down Cell
class Solution:
    def numbered(self, n):
        grid = table(n, n)
        for k in range(n * n):
            r, c = divmod(k, n)
            grid[r][c] = k
        return grid
