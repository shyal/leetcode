# REFERENCE: d171 Fewest Cells Between
class Solution:
    def fewest(self, grid):
        q = deque(cells(grid, eq=1))
        for d, (r, c) in levels(q, seen=set()):
            if grid[r][c] == 2:
                return d - 1
            q += nbrs(grid, r, c)
