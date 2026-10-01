# REFERENCE: d182 Bottom Up Cell Alternating
class Solution:
    def numbered(self, n):
        grid = table(n, n)
        for k in range(n * n):
            b, c = divmod(k, n)
            c = n - 1 - c if b % 2 else c
            grid[n - 1 - b][c] = k
        return grid
