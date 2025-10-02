"""
URL: https://leetcode.com/problems/range-sum-query-2d-immutable/description/

304. Range Sum Query 2D - Immutable

Given a 2D matrix matrix, handle multiple queries of the following type:

    Calculate the sum of the elements of matrix inside the rectangle defined by its upper left corner (row1, col1) and lower right corner (row2, col2).

Implement the NumMatrix class:

    NumMatrix(int[][] matrix) Initializes the object with the integer matrix matrix.
    int sumRegion(int row1, int col1, int row2, int col2) Returns the sum of the elements of matrix inside the rectangle defined by its upper left corner (row1, col1) and lower right corner (row2, col2).

You must design an algorithm where sumRegion works on O(1) time complexity.


Example 1:

Input
["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
Output
[null, 8, 11, 12]

Explanation
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)


Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 200
    -104 <= matrix[i][j] <= 104
    0 <= row1 <= row2 < m
    0 <= col1 <= col2 < n
    At most 104 calls will be made to sumRegion.
"""


class Solution:
    def dummy(self):
        pass


class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        self.sums = [[*accumulate(row)] + [0] for row in matrix]

    def sumRange(self, i, j, row):
        return self.sums[row][j] - self.sums[row][i - 1]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return sum(self.sumRange(col1, col2, row) for row in range(row1, row2 + 1))


matrix = [
    [3, 0, 1, 4, 2],
    [5, 6, 3, 2, 1],
    [1, 2, 0, 1, 5],
    [4, 1, 0, 1, 7],
    [1, 0, 3, 0, 5],
]

matrix = [
    [3, 0, 1, 4, 2],
    [5, 6, 3, 2, 1],
    [1, 2, 0, 1, 5],
    [4, 1, 0, 1, 7],
    [1, 0, 3, 0, 5],
]
num_matrix = NumMatrix(matrix)
assert num_matrix.sumRegion(2, 1, 4, 3) == 8
assert num_matrix.sumRegion(1, 1, 2, 2) == 11
assert num_matrix.sumRegion(1, 2, 2, 4) == 12
assert num_matrix.sumRegion(0, 0, 0, 2) == 4
assert num_matrix.sumRegion(0, 0, 4, 4) == 58
assert num_matrix.sumRegion(0, 0, 0, 0) == 3
assert num_matrix.sumRegion(4, 4, 4, 4) == 5
assert num_matrix.sumRegion(3, 0, 4, 0) == 5
matrix2 = [[1]]
num_matrix2 = NumMatrix(matrix2)
assert num_matrix2.sumRegion(0, 0, 0, 0) == 1
matrix3 = [[0]]
num_matrix3 = NumMatrix(matrix3)
assert num_matrix3.sumRegion(0, 0, 0, 0) == 0
matrix4 = [[-5]]
num_matrix4 = NumMatrix(matrix4)
assert num_matrix4.sumRegion(0, 0, 0, 0) == -5
matrix5 = [[1, 2, 3]]
num_matrix5 = NumMatrix(matrix5)
assert num_matrix5.sumRegion(0, 0, 0, 0) == 1
assert num_matrix5.sumRegion(0, 1, 0, 1) == 2
assert num_matrix5.sumRegion(0, 1, 0, 2) == 5
assert num_matrix5.sumRegion(0, 0, 0, 2) == 6
matrix6 = [[1], [2], [3]]
num_matrix6 = NumMatrix(matrix6)
assert num_matrix6.sumRegion(0, 0, 0, 0) == 1
assert num_matrix6.sumRegion(1, 0, 1, 0) == 2
assert num_matrix6.sumRegion(0, 0, 2, 0) == 6
matrix7 = [[1, -1], [-2, 3]]
num_matrix7 = NumMatrix(matrix7)
assert num_matrix7.sumRegion(0, 0, 0, 0) == 1
assert num_matrix7.sumRegion(0, 1, 0, 1) == -1
assert num_matrix7.sumRegion(1, 0, 1, 0) == -2
assert num_matrix7.sumRegion(1, 1, 1, 1) == 3
assert num_matrix7.sumRegion(0, 0, 1, 1) == 1
assert num_matrix7.sumRegion(0, 1, 1, 1) == 2
assert num_matrix7.sumRegion(1, 0, 1, 1) == 1
