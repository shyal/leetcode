"""
498. Diagonal Traverse
Medium
Given an m x n matrix mat, return an array of all the elements of the array in a diagonal order.

Example 1:

Input: mat = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,4,7,5,3,6,8,9]
Example 2:

Input: mat = [[1,2],[3,4]]
Output: [1,2,3,4]

Constraints:

m == mat.length
n == mat[i].length
1 <= m, n <= 104
1 <= m * n <= 104
-105 <= mat[i][j] <= 105
"""


class Dir:
    up = 0
    down = 1


class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        def diag_up(row, col):
            ret = []
            r = row
            c = col
            while r >= 0 and c <= len(mat[0]) - 1:
                ret.append(mat[r][c])
                c += 1
                r -= 1
            return ret

        def diag_down(row, col):
            return [*reversed(diag_up(row, col))]

        def diag(row, col, d):
            return diag_up(row, col) if d == Dir.up else diag_down(row, col)

        ret = []
        d = Dir.up
        rows = [*range(len(mat))] + ([len(mat) - 1] * (len(mat[0]) - 1))
        cols = [0] * len(mat) + [*range(1, len(mat[0]))]
        inds = [*zip(rows, cols)]
        for r, c in inds:
            ret.extend(diag(r, c, d))
            d = Dir.up if d == Dir.down else Dir.down
        return ret


sol = Solution()
assert sol.findDiagonalOrder(mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
    1,
    2,
    4,
    7,
    5,
    3,
    6,
    8,
    9,
]
assert sol.findDiagonalOrder(mat=[[1]]) == [1]
assert sol.findDiagonalOrder(mat=[[1, 2], [3, 4]]) == [1, 2, 3, 4]
assert sol.findDiagonalOrder(
    mat=[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]
) == [1, 2, 6, 11, 7, 3, 4, 8, 12, 13, 9, 5, 10, 14, 15]
assert sol.findDiagonalOrder(mat=[[1]]) == [1]
assert sol.findDiagonalOrder(mat=[[1, 2, 3, 4]]) == [1, 2, 3, 4]
assert sol.findDiagonalOrder(mat=[[1], [2], [3], [4]]) == [1, 2, 3, 4]
assert sol.findDiagonalOrder(mat=[[1, 2, 3], [4, 5, 6]]) == [1, 2, 4, 5, 3, 6]
assert sol.findDiagonalOrder(mat=[[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 5, 4, 6]
assert sol.findDiagonalOrder(mat=[[1, 2], [3, 4], [5, 6], [7, 8]]) == [
    1,
    2,
    3,
    5,
    4,
    6,
    7,
    8,
]
assert sol.findDiagonalOrder(mat=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [
    1,
    2,
    5,
    9,
    6,
    3,
    4,
    7,
    10,
    11,
    8,
    12,
]
assert sol.findDiagonalOrder(mat=[[-1, -2, -3], [-4, -5, -6]]) == [
    -1,
    -2,
    -4,
    -5,
    -3,
    -6,
]


