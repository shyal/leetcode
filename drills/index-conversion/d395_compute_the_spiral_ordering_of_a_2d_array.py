"""
EPI 5.18 Compute the spiral ordering of a 2D array

Given an n x n matrix square_matrix, return its elements in clockwise
spiral order, from the top-left element: the top row left to right,
the right column top to bottom, the bottom row right to left, the left
column bottom to top, then the same for the matrix inside.

Example 1:

Input: square_matrix = [[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9]]
Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]

Example 2:

Input: square_matrix = [[1, 2, 3, 4],
                        [5, 6, 7, 8],
                        [9, 10, 11, 12],
                        [13, 14, 15, 16]]
Output: [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]

Example 3:

Input: square_matrix = []
Output: []

Constraints:

    0 <= n <= 300
    len(square_matrix[i]) == n

    REQUIRED: O(n^2) time, O(1) extra space besides the list returned.
    NO zip(), NO change to square_matrix.
"""


class Solution:
    def matrix_in_spiral_order(self, square_matrix: list[list[int]]) -> list[int]:
        pass


sol = Solution()

print(sol.matrix_in_spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # [1, 2, 3, 6, 9, 8, 7, 4, 5]

# assert sol.matrix_in_spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
# assert sol.matrix_in_spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]) == [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
# assert sol.matrix_in_spiral_order([]) == []
# assert sol.matrix_in_spiral_order([[1]]) == [1]
# assert sol.matrix_in_spiral_order([[1, 2], [3, 4]]) == [1, 2, 4, 3]
# assert sol.matrix_in_spiral_order([[r * 5 + c + 1 for c in range(5)] for r in range(5)]) == [1, 2, 3, 4, 5, 10, 15, 20, 25, 24, 23, 22, 21, 16, 11, 6, 7, 8, 9, 14, 19, 18, 17, 12, 13]
# assert sol.matrix_in_spiral_order([[0, 0], [0, 0]]) == [0, 0, 0, 0]
# assert sol.matrix_in_spiral_order([[-1, 5], [7, -3]]) == [-1, 5, -3, 7]
# M = [[r * 6 + c for c in range(6)] for r in range(6)]
# assert sol.matrix_in_spiral_order(M)[-4:] == [14, 15, 21, 20]
# assert M == [[r * 6 + c for c in range(6)] for r in range(6)]
# M = [[r * 300 + c for c in range(300)] for r in range(300)]
# s = sol.matrix_in_spiral_order(M)
# assert len(s) == 90000 and sorted(s) == list(range(90000))
# assert s[:300] == list(range(300)) and s[300:599] == [r * 300 + 299 for r in range(1, 300)]
# assert s[-3:] == [44850, 45150, 45149]
