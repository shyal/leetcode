"""
https://leetcode.com/problems/transpose-matrix/description/

867. Transpose Matrix
Easy
Given a 2D integer array matrix, return the transpose of matrix.

The transpose of a matrix is the matrix flipped over its main diagonal, switching the matrix's row and column indices.

Example 1:

Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[1,4,7],[2,5,8],[3,6,9]]
Example 2:

Input: matrix = [[1,2,3],[4,5,6]]
Output: [[1,4],[2,5],[3,6]]
 

Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 1000
1 <= m * n <= 105
-109 <= matrix[i][j] <= 109
"""

"""
1 2 3
4 5 6
7 8 9


"""


class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        return [list(x) for x in zip(*matrix)]


sol = Solution()
assert sol.transpose(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
]

assert sol.transpose(matrix=[[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert sol.transpose(matrix=[[1]]) == [[1]]
assert sol.transpose(matrix=[[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
assert sol.transpose(matrix=[[5]]) == [[5]]
assert sol.transpose(matrix=[[1, 2, 3, 4]]) == [[1], [2], [3], [4]]
assert sol.transpose(matrix=[[1], [2], [3], [4]]) == [[1, 2, 3, 4]]
assert sol.transpose(matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
assert sol.transpose(matrix=[[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
assert sol.transpose(matrix=[[1, 3, 5], [2, 4, 6]]) == [[1, 2], [3, 4], [5, 6]]
assert sol.transpose(matrix=[[-1, -2], [-3, -4]]) == [[-1, -3], [-2, -4]]
assert sol.transpose(matrix=[[10, 20, 30], [40, 50, 60]]) == [
    [10, 40],
    [20, 50],
    [30, 60],
]
assert sol.transpose(matrix=[[7, 8, 9], [1, 2, 3], [4, 5, 6]]) == [
    [7, 1, 4],
    [8, 2, 5],
    [9, 3, 6],
]
assert sol.transpose(matrix=[[2]]) == [[2]]
assert sol.transpose(matrix=[[1, 2, 3]]) == [[1], [2], [3]]
assert sol.transpose(matrix=[[1], [2], [3]]) == [[1, 2, 3]]
assert sol.transpose(matrix=[[0]]) == [[0]]


