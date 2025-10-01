"""
URL: https://leetcode.com/problems/reshape-the-matrix/description/

566. Reshape the Matrix

In MATLAB, there is a handy function called reshape which can reshape an m x n matrix into a new one with a different size r x c keeping its original data.

You are given an m x n matrix mat and two integers r and c representing the number of rows and the number of columns of the wanted reshaped matrix.

The reshaped matrix should be filled with all the elements of the original matrix in the same row-traversing order as they were.

If the reshape operation with given parameters is possible and legal, output the new reshaped matrix; Otherwise, output the original matrix.


Example 1:

Input: mat = [[1,2],[3,4]], r = 1, c = 4
Output: [[1,2,3,4]]

Example 2:

Input: mat = [[1,2],[3,4]], r = 2, c = 4
Output: [[1,2],[3,4]]


Constraints:

        m == mat.length
        n == mat[i].length
        1 <= m, n <= 100
        -1000 <= mat[i][j] <= 1000
        1 <= r, c <= 300
"""

from itertools import chain
from itertools import zip_longest


def batched(s, n=1):
    r = list(range(0, len(s), n))
    return [s[a:b] for a, b in zip_longest(r, r[1:])]


class Solution:
    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:
        if r == len(mat) and c == len(mat[0]) or r * c != len(mat) * len(mat[0]):
            return mat
        return batched([*chain(*mat)], c)


sol = Solution()
assert sol.matrixReshape([[1, 2], [3, 4]], 1, 4) == [[1, 2, 3, 4]]

assert sol.matrixReshape([[1, 2], [3, 4]], 2, 4) == [[1, 2], [3, 4]]

assert sol.matrixReshape([[1]], 1, 1) == [[1]]

assert sol.matrixReshape([[1, 2, 3, 4, 5, 6, 7, 8]], 2, 4) == [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
]

assert sol.matrixReshape(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
    ],
    1,
    8,
) == [[1, 2, 3, 4, 5, 6, 7, 8]]


assert sol.matrixReshape(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
    ],
    4,
    2,
) == [[1, 2], [3, 4], [5, 6], [7, 8]]
