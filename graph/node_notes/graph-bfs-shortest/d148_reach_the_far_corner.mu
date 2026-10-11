# REFERENCE: d148 Reach The Far Corner
class Solution
  def reach(grid: [[int]], k: int) -> bool
    q = deque([(0, 0)])
    seen = set()
    for (_, c) in levels(q, grid, seen, gte=k)
      q += nbrs(grid, c)
    shape(grid, last_index=True) in seen
