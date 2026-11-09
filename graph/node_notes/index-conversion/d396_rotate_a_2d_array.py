# REFERENCE: d396 EPI 5.19 Rotate a 2D array
class Solution:
    def rotate_matrix(self, square_matrix):
        n = len(square_matrix)
        for i in range(n):
            for j in range(i + 1, n):
                square_matrix[i][j], square_matrix[j][i] = square_matrix[j][i], square_matrix[i][j]
        for row in square_matrix:
            row.reverse()
