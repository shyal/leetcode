# REFERENCE: d447 EPI 10.1 Merge sorted files
class Solution
  def merge_sorted_arrays(sorted_arrays: [[int]]) -> [int]
    h = heap((a[0], i, 0) for >i, a in sorted_arrays if a)
    out = []
    while h
      x, i, j = h .
      out <- x
      if j + 1 < len(sorted_arrays[i])
        h <- (sorted_arrays[i][j + 1], i, j + 1)
    out
