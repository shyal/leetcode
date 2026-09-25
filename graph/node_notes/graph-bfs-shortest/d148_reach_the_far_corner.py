# REFERENCE: d148 Reach The Far Corner
class Solution:
    def reach(self, grid, k):
        q = deque([(0, 0)])
        seen = set()
        for _, (r, c) in levels(q, grid, seen, gte=k):
            q += nbrs(grid, r, c)
        return shape(grid, last_index=True) in seen
