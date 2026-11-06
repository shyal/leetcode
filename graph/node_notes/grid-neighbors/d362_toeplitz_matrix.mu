# REFERENCE: d362 Toeplitz Matrix
class Solution
  def isToeplitz(arr: [[int]]) -> bool
    all(arr[r][c] == arr[r - 1][c - 1] for r in 1..<len(arr) for c in 1..<len(arr[0]))
