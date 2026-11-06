# REFERENCE: d343 Island Count
class Solution
  def get_number_of_islands(binaryMatrix: [[int]]) -> int
    count for p in cells(binaryMatrix, eq=1)
      stack = [p]
      while stack
        q = stack.pop()
        if binaryMatrix[q] == 1
          binaryMatrix[q] = 0
          for n in nbrs(binaryMatrix, q, eq=1)
            stack <- n
      true
