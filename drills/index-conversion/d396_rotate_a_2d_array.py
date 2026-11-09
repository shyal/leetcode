"""
EPI 5.19 Rotate a 2D array

Given an n x n matrix square_matrix, rotate it by 90 degrees clockwise,
in place.

Example 1:

Input: square_matrix = [[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]]
Output: square_matrix = [[7, 4, 1],
                         [8, 5, 2],
                         [9, 6, 3]]
Explanation: The left column, read bottom to top, becomes the top row.

Example 2:

Input: square_matrix = [[1, 2],
                        [3, 4]]
Output: square_matrix = [[3, 1],
                         [4, 2]]

Example 3:

Input: square_matrix = [[1]]
Output: square_matrix = [[1]]

Constraints:

    1 <= n <= 500
    len(square_matrix[i]) == n

    REQUIRED: O(n^2) time, O(1) extra space. NO zip(), NO second
    matrix.
"""


class Solution:
    def rotate_matrix(self, square_matrix: list[list[int]]) -> None:
        pass


sol = Solution()


def rotated(M):
    n = len(M)
    return [[M[n - 1 - j][i] for j in range(n)] for i in range(n)]


M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
sol.rotate_matrix(M)
print(M)  # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

# M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# sol.rotate_matrix(M)
# assert M == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
# M = [[1, 2], [3, 4]]
# sol.rotate_matrix(M)
# assert M == [[3, 1], [4, 2]]
# M = [[1]]
# sol.rotate_matrix(M)
# assert M == [[1]]
# M = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
# sol.rotate_matrix(M)
# assert M == [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
# M = [[r * 5 + c for c in range(5)] for r in range(5)]
# sol.rotate_matrix(M)
# assert M == rotated([[r * 5 + c for c in range(5)] for r in range(5)])
# M = [[0, 0], [0, 0]]
# sol.rotate_matrix(M)
# assert M == [[0, 0], [0, 0]]
# M = [[1, 2], [3, 4]]
# sol.rotate_matrix(M)
# sol.rotate_matrix(M)
# assert M == [[4, 3], [2, 1]]
# M = [[r * 7 + c for c in range(7)] for r in range(7)]
# sol.rotate_matrix(M)
# sol.rotate_matrix(M)
# sol.rotate_matrix(M)
# sol.rotate_matrix(M)
# assert M == [[r * 7 + c for c in range(7)] for r in range(7)]
# M = [[r * 500 + c for c in range(500)] for r in range(500)]
# sol.rotate_matrix(M)
# assert M == rotated([[r * 500 + c for c in range(500)] for r in range(500)])
# M = [[r * 501 + c for c in range(501)] for r in range(501)]
# sol.rotate_matrix(M)
# assert M[0][0] == 500 * 501 and M[250][250] == 250 * 501 + 250 and M[0][500] == 0
