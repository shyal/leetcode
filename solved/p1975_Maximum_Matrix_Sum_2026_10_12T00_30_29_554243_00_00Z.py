"""
URL: https://leetcode.com/problems/maximum-matrix-sum/description/?envType=problem-list-v2&envId=vn57k9wr

1975. Maximum Matrix Sum

You are given an n x n integer matrix. You can do the following operation any number of times:

- Choose any two adjacent elements of matrix and multiply each of them by -1.

Two elements are considered adjacent if and only if they share a border.

Your goal is to maximize the summation of the matrix's elements. Return the maximum sum of the matrix's elements using the operation mentioned above.

Example 1:

Input: matrix = [[1,-1],[-1,1]]
Output: 4
Explanation: We can follow the following steps to reach sum equals 4:
- Multiply the 2 elements in the first row by -1.
- Multiply the 2 elements in the first column by -1.

Example 2:

Input: matrix = [[1,2,3],[-1,-2,-3],[1,2,3]]
Output: 16
Explanation: We can follow the following step to reach sum equals 16:
- Multiply the 2 last elements in the second row by -1.

Constraints:

    n == matrix.length == matrix[i].length
    2 <= n <= 250
    -10^5 <= matrix[i][j] <= 10^5
---
[1,-1]
[-1,1]


[-1,1]
[-1,1]

[1,1]
[1,1]


[1,  2,  3]
[-1,-2, -3]
[1,  2,  3]

[1,  2,  3]
[-1, 2,  3]
[1,  2,  3]



[1, -1, 1, -1]
[1, -1, 1, -1]
[1, -1, 1, -1]
[1, -1, 1, -1]

[1, 1, 1, 1]
[1, 1, 1, 1]
[1, 1, 1, 1]
[1, 1, 1, 1]


[1, -1, 1]
[-1, 1, -1]
[1, -1, 1]

[1,   1, 1]
[-1, -1, -1]
[1,  -1, 1]

[1,  1, 1]
[-1, 1, -1]
[1,  1, 1]


[1,  1, 1]
[1, -1, -1]
[1,  1, 1]


[1,  1, 1]
[1,  1, 1]
[1,  1, 1]


[1, 2, 3, 4]
[5, -6, 7, -8]
[9, 10, -11, 12]
[13, 14, 15, -16]

[1, 2, 3, 4]
[5, 6, 7, 8]
[9, 10, 11, 12]
[13, 14, 15, 16]

It seems that if there's an even number of minuses in a row, or a column, then can get flipped to positive
If there's an odd number of -1 in a row, they can get reduced down to a single -1, at which point

LEETCODE: Accepted (323 ms, 29.3 MB)
"""


# mu 0.10
# class Solution
#   def maxMatrixSum(matrix: [[int]]) -> int
#     count = 0
#     total_positive = 0
#     _min = inf
#     for i, j in cells(matrix)
#       count += matrix[i][j] < 0
#       total_positive += abs(matrix[i][j])
#       _min = min(_min, abs(matrix[i][j]))
#     if even count
#       return total_positive
#     else
#       return total_positive - _min * 2

from math import inf


def _holds(v, eq=None, lt=None, lte=None, gt=None, gte=None):
    return (
        (eq is None or v == eq)
        and (lt is None or v < lt)
        and (lte is None or v <= lte)
        and (gt is None or v > gt)
        and (gte is None or v >= gte)
    )


def cells(grid, start=0, val=None, eq=None, lt=None, lte=None, gt=None, gte=None):
    eq = val if eq is None else eq
    for i in range(start, len(grid)):
        for j in range(start, len(grid[0])):
            if _holds(grid[i][j], eq, lt, lte, gt, gte):
                yield i, j


def even(n):
    return n % 2 == 0


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
    def maxMatrixSum(self, matrix: list[list[int]]) -> int:
        _in_matrix, matrix = matrix, Grid(matrix)
        _w_matrix = matrix
        try:
            count = 0
            total_positive = 0
            _min = inf
            for i, j in cells(matrix):
                count += matrix[i][j] < 0
                total_positive += abs(matrix[i][j])
                _min = min(_min, abs(matrix[i][j]))
            if even(count):
                return total_positive
            else:
                return total_positive - _min * 2
        finally:
            _in_matrix[:] = _w_matrix


sol = Solution()
print(sol.maxMatrixSum([[1, 2, 3], [-1, -2, -3], [1, 2, 3]]))
print(sol.maxMatrixSum([[1, -1], [-1, 1]]))
_l, _r = sol.maxMatrixSum([[1, -1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1, 2, 3], [-1, -2, -3], [1, 2, 3]]), 16
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1, -1], [-1, 1]]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[0, 0], [0, 0]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1, 1], [1, 1]]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[-1, -1], [-1, -1]]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[10 ** 5, -10 ** 5], [-10 ** 5, 10 ** 5]]), 400000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[10 ** 5] * 250 for _ in range(0, 250)]), 6250000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[-10 ** 5] * 250 for _ in range(0, 250)]), 6250000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[(-1) ** (i + j) * 10 ** 5 for j in range(0, 250)] for i in range(0, 250)]), 6250000000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1, -1, 1, -1], [1, -1, 1, -1], [1, -1, 1, -1], [1, -1, 1, -1]]), 16
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1, 2, 3, 4], [5, -6, 7, -8], [9, 10, -11, 12], [13, 14, 15, -16]]), 136
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxMatrixSum([[1, -1, 1], [-1, 1, -1], [1, -1, 1]]), 9
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
