# REFERENCE: d528 EPI 18.1 Search a maze
class Solution:
    def search_maze(self, maze, s, e):
        rows, cols = len(maze), len(maze[0])
        parent = {s: None}
        stack = [s]
        while stack:
            cur = stack.pop()
            if cur == e:
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                return path[::-1]
            r, c = cur
            for nxt in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                nr, nc = nxt
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and nxt not in parent:
                    parent[nxt] = cur
                    stack.append(nxt)
        return []
