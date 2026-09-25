# REFERENCE: d148 Reach The Far Corner
class Solution:
    def reach(self, grid, k):
        if grid[0][0] < k:
            return False
        q = deque([(0, 0)])
        seen = {(0, 0)}
        for _, (r, c) in levels(q):
            for i, j in nbrs(grid, r, c):
                if (i, j) in seen or grid[i][j] < k:
                    continue
                seen.add((i, j))
                q.append((i, j))
        return (len(grid) - 1, len(grid[0]) - 1) in seen
