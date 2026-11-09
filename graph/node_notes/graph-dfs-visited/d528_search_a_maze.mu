# REFERENCE: d528 EPI 18.1 Search a maze
class Solution
  def search_maze(maze: [[int]], s: (int, int), e: (int, int)) -> [(int, int)]
    parent = {s: none}
    stack = [s]
    while stack
      cur = stack .
      if cur == e
        path = []
        while cur is not none
          path <- cur
          cur = parent[cur]
        return path[::-1]
      for nxt in nbrs(maze, cur, eq=0)
        if nxt not in parent
          parent[nxt] = cur
          stack <- nxt
    []
