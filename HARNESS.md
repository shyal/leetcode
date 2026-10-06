# Leetcode sitecustomize, harness and helpers

Leetcode's python sitecustomize is full of everything one needs for solving, without needing to import much at all. This repo mimics that, and also adds a lot of very useful helpers for DSA solving.

Here's an example of `1926. Nearest Exit from Entrance in Maze`:

```python
class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        q = deque([[entrance[0], entrance[1], 0]])
        maze[entrance[0]][entrance[1]] = "+"
        while q:
            x, y, dist = q.popleft()
            if is_edge(maze, x, y) and maze[x][y] != "+":
                return dist
            maze[x][y] = "+"
            for nx, ny in nbrs(maze, x, y):
                if maze[nx][ny] != "+":
                    q.append([nx, ny, dist + 1])
        return -1
```

You can find the full harness in [utils/harness/README.md](utils/harness/README.md).

```python
root = build_tree([4, 2, 7, 1, 3, 6, 9])
draw_tree(root)
```

```text
      [4]
   ┌───┴───┐
  [2]     [7]
 ┌─┴─┐   ┌─┴─┐
[1] [3] [6] [9]
```

The drawing functions, with examples: [utils/harness/DRAWING.md](utils/harness/DRAWING.md).

And here's LCS, using an experimental DSA DSL called `mu` created specifically for this repo:

```python
def lcs(a: str, b: str) -> int
  memo f(i, j) =
    | i == len a or j == len b  -> 0
    | a[i] == b[j]              -> 1 + f(i + 1, j + 1)
    | else                      -> max(f(i + 1, j), f(i, j + 1))
  f(0, 0)
```

542. 01 Matrix:

```python
def updateMatrix(mat: [[int]]) -> [[int]]
  q = deque(cells(mat, val=0))
  put(mat, cells(mat, val=1), inf)
  for (d, p) in levels(q)
    for n in nbrs(mat, p, val=inf)
      mat[n] = d + 1
      q <- n
  mat
```

mu language spec: [v0.1](mu/spec/v0.1.md), [v0.2](mu/spec/v0.2.md), [v0.3](mu/spec/v0.3.md), [v0.4](mu/spec/v0.4.md), [v0.5](mu/spec/v0.5.md), [v0.6](mu/spec/v0.6.md), [v0.7](mu/spec/v0.7.md)
