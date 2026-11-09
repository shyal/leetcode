# REFERENCE: d448 EPI 10.2 Sort an increasing-decreasing array
class Solution
  def sort_k_increasing_decreasing_array(A: [int]) -> [int]
    runs, start = [], 0
    for i in 1..len(A)
      if i == len(A) or (i > start + 1 and (A[i - 1] < A[i]) != (A[start] < A[start + 1]))
        run = A[start:i]
        runs <- (run[0] <= run[-1] ? run : run[::-1])
        start = i
    h = heap((run[0], r, 0) for >r, run in runs)
    out = []
    while h
      x, r, j = h .
      out <- x
      if j + 1 < len(runs[r])
        h <- (runs[r][j + 1], r, j + 1)
    out
