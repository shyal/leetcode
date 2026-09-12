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


0 0 0
0 1 0
1 1 1

0 0 0
0 x 0
1 1 1

0 0 0
0 1 0
1 1 1

0 0 0
0 1 0
1 1 1


Ok i think i need to do a (multi) bfs, but adding the 1s
to a queue, and look at cardinal neighbours until reaching
a zero.

Once a zero is reached, the min distance needs to be written
back into the originating cell.

"""


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        def bfs(i, j):
            q = deque([[i, j, i, j, 0]])
            visited = set([])
            while q:
                oi, oj, i, j, dist = q.popleft()
                if (i, j) in visited:
                    continue
                visited.add((i, j))
                if mat[i][j] == 0:
                    res[oi][oj] = min(res[oi][oj], dist)
                else:
                    if i > 0 and mat[i - 1][j] == 0:
                        q.append([oi, oj, i - 1, j, dist + 1])
                    if i < len(mat) - 1 and mat[i + 1][j] == 0:
                        q.append([oi, oj, i + 1, j, dist + 1])
                    if j > 0 and mat[i][j - 1] == 0:
                        q.append([oi, oj, i, j - 1, dist + 1])
                    if j < len(mat[0]) - 1 and mat[i][j + 1]:
                        q.append([oi, oj, i, j + 1, dist + 1])

        res = []
        for i in range(len(mat)):
            res.append([float("inf")] * len(mat[0]))

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == 1:
                    # print(i, j)
                    bfs(i, j)

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if res[i][j] == float("inf"):
                    res[i][j] = 0
        return res


sol = Solution()

# print(sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))  # [[0,0,0],[0,1,0],[0,0,0]]

print(sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]))


assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
]
assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [
    [0, 0, 0],
    [0, 1, 0],
    [1, 2, 1],
]
