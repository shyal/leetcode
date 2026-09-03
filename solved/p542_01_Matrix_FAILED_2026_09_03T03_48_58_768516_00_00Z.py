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
"""


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:

        @cache
        def dfs(i, j):
            val = mat[i][j]
            if val == 0:
                return 0

            if i < 0 or i >= len(mat) - 1 or j < 0 or j >= len(mat[i]) - 1:
                return 0

            dist = float(0)

            dist = max(dfs(i - 1, j), dist)
            dist = max(dfs(i + 1, j), dist)
            dist = max(dfs(i, j - 1), dist)
            dist = max(dfs(i, j + 1), dist)

            return dist + 1

        res = [[] for _ in range(len(mat))]

        for i in range(len(mat)):
            for j in range(len(mat[i])):
                val = dfs(i, j)
                res[i].append(val)

        return res


sol = Solution()

# print(sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))  # [[0,0,0],[0,1,0],[0,0,0]]
print(sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]))

# assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == [
#     [0, 0, 0],
#     [0, 1, 0],
#     [0, 0, 0],
# ]
# assert sol.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [
#     [0, 0, 0],
#     [0, 1, 0],
#     [1, 2, 1],
# ]


# FAILED: walked away after 15m 29s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
