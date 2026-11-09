# REFERENCE: d458 EPI 11.6 Search in a 2D sorted array
class Solution
  def matrix_search(A: [[int]], x: int) -> bool
    r, c = 0, A ? len(A[0]) - 1 : -1
    while r < len(A) and c >= 0
      if A[r][c] == x
        return true
      if A[r][c] < x
        r += 1
      else
        c -= 1
    false
