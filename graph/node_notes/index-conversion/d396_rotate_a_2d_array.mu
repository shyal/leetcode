# REFERENCE: d396 EPI 5.19 Rotate a 2D array
class Solution
  def rotate_matrix(square_matrix: [[int]])
    n = len(square_matrix)
    for i in 0..<n
      for j in i + 1..<n
        square_matrix[i][j], square_matrix[j][i] = square_matrix[j][i], square_matrix[i][j]
    for row in square_matrix
      row.reverse()
