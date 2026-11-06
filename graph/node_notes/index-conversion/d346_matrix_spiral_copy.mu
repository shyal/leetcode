# REFERENCE: d346 Matrix Spiral Copy
class Solution
  def spiral_copy(inputMatrix: [[int]]) -> [int]
    top, bottom = 0, len(inputMatrix) - 1
    left, right = 0, len(inputMatrix[0]) - 1
    ret res = []
    while top <= bottom and left <= right
      for c in left..right
        res <- inputMatrix[top][c]
      top += 1
      for r in top..bottom
        res <- inputMatrix[r][right]
      right -= 1
      if top <= bottom
        for c in right..left by -1
          res <- inputMatrix[bottom][c]
        bottom -= 1
      if left <= right
        for r in bottom..top by -1
          res <- inputMatrix[r][left]
        left += 1
