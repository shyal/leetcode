"""
URL: https://leetcode.com/problems/minimum-falling-path-sum/description/?envType=problem-list-v2&envId=vn57k9wr

931. Minimum Falling Path Sum

Given an n x n array of integers matrix, return the minimum sum of any falling path through matrix.

A falling path starts at any element in the first row and chooses the element in the next row that is either directly below or diagonally left/right. Specifically, the next element from position (row, col) will be (row + 1, col - 1), (row + 1, col), or (row + 1, col + 1).

Example 1:

Input: matrix = [[2,1,3],[6,5,4],[7,8,9]]
Output: 13
Explanation: There are two falling paths with a minimum sum as shown.

Example 2:

Input: matrix = [[-19,57],[-40,-5]]
Output: -59
Explanation: The falling path with a minimum sum is shown.

Constraints:

    n == matrix.length == matrix[i].length
    1 <= n <= 100
    -100 <= matrix[i][j] <= 100

---

LEETCODE: Accepted (114 ms, 31.3 MB)
"""


# mu 0.6
# def minFallingPathSum(matrix: [[int]]) -> int
#   memo helper(row, col)
#     opts = []
#     for (i, j) in [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
#       if in_bounds(matrix, i, j)
#         opts <- helper(i, j)
#     return matrix[row][col] + (min(opts) if opts else 0)
#
#   min(helper(0, j) for j in range(len(matrix[0])))

from functools import cache
import sys
import threading


sys.setrecursionlimit(1 << 20)


def deep(fn):
    """Run fn on a thread with a 256 MB stack, so deep memo recursion fits."""
    out, err = [], []

    def target():
        try:
            out.append(fn())
        except BaseException as e:
            err.append(e)

    threading.stack_size(1 << 28)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if err:
        raise err[0]
    return out[0]


def in_bounds(grid, r, c=None):
    if c is None:
        r, c = r
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


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
    def minFallingPathSum(self, matrix: list[list[int]]) -> int:
        _in_matrix, matrix = matrix, Grid(matrix)
        _w_matrix = matrix
        try:
            def run():
                @cache
                def helper(row, col):
                    opts = []
                    for (i, j) in [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]:
                        if in_bounds(matrix, i, j):
                            opts.append(helper(i, j))
                    return matrix[row][col] + (min(opts) if opts else 0)
                return min(helper(0, j) for j in range(len(matrix[0])))
            return deep(run)
        finally:
            _in_matrix[:] = _w_matrix


sol = Solution()
print(sol.minFallingPathSum([[2, 1, 3], [6, 5, 4], [7, 8, 9]]))
assert sol.minFallingPathSum([[2, 1, 3], [6, 5, 4], [7, 8, 9]]) == 13
assert sol.minFallingPathSum([[-19, 57], [-40, -5]]) == -59
assert sol.minFallingPathSum([[5]]) == 5
assert sol.minFallingPathSum([[1, 2], [3, 4]]) == 4
assert sol.minFallingPathSum([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == 0
assert sol.minFallingPathSum([[100] * 100 for _ in range(0, 100)]) == 10000
assert sol.minFallingPathSum([[-100] * 100 for _ in range(0, 100)]) == -10000
assert sol.minFallingPathSum([[1, -1, 1], [-1, 1, -1], [1, -1, 1]]) == -3
assert sol.minFallingPathSum([[1, 2, 3, 4, 5]]) == 1
assert sol.minFallingPathSum([[10, -10, 10], [-10, 10, -10], [10, -10, 10]]) == -30
assert sol.minFallingPathSum([[0]]) == 0
assert sol.minFallingPathSum([[1] * 100 for _ in range(0, 100)]) == 100
