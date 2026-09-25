"""
URL: https://leetcode.com/problems/01-matrix/description/?envType=problem-list-v2&envId=vn57k9wr

542. 01 Matrix

Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.

The distance between two cells sharing a common edge is 1.

Example 1:

Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
Output: [[0,0,0],[0,1,0],[0,0,0]]

Example 2:

Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
Output: [[0,0,0],[0,1,0],[1,2,1]]

Constraints:

    m == mat.length
    n == mat[i].length
    1 <= m, n <= 10^4
    1 <= m * n <= 10^4
    mat[i][j] is either 0 or 1.
    There is at least one 0 in mat.

Note: This question is the same as 1765: https://leetcode.com/problems/map-of-highest-peak/description/

---

LEETCODE: Accepted (623 ms, 24.1 MB)
"""


# mu source (current.mu), the candidate's solution. The Python
# under it is the transpiler's output, and it is what ran.
#
# def updateMatrix(mat: [[int]]) -> [[int]]
#   q = deque()
#   seen = set()
#   res = like(mat, fill=inf)
#   for (i, j) in cells(mat)
#     if mat[i][j] == 0
#       q <- (i, j, 0)
#       seen.add((i, j))
#   while q
#     i, j, dist = q.popleft()
#     seen.add((i, j))
#     if mat[i][j] == 1
#       res[i][j] = min(res[i][j], dist)
#     for (ii, jj) in nbrs(mat, i, j)
#       if (ii, jj) not in seen
#         q <- (ii, jj, dist+1)
#   for (i, j) in cells(res)
#     if res[i][j] == inf
#       res[i][j] = 0
#   res

from math import inf


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def like(grid, fill=0):
    return table(len(grid), len(grid[0]), fill=fill)


def cells(grid, start=0):
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            yield i, j


CARDINALS = ((-1, 0), (0, -1), (0, 1), (1, 0))


def nbrs(grid, r, c=None, dirs=CARDINALS):
    """On-grid cells next to (r, c): up, left, right, down. nbrs(grid, p)
    takes the cell as one pair."""
    if c is None:
        r, c = r
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            yield nr, nc


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        mat = Grid(mat)
        q = deque()
        seen = set()
        res = like(mat, fill=inf)
        for (i, j) in cells(mat):
            if mat[i][j] == 0:
                q.append((i, j, 0))
                seen.add((i, j))
        while q:
            i, j, dist = q.popleft()
            seen.add((i, j))
            if mat[i][j] == 1:
                res[i][j] = min(res[i][j], dist)
            for (ii, jj) in nbrs(mat, i, j):
                if (ii, jj) not in seen:
                    q.append((ii, jj, dist + 1))
        for (i, j) in cells(res):
            if res[i][j] == inf:
                res[i][j] = 0
        return res


sol = Solution()
print(sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))
print(sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]))
assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
