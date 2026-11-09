# REFERENCE: d474 EPI 13.1 Compute the intersection of two sorted arrays
class Solution
  def intersect_two_sorted_arrays(A: [int], B: [int]) -> [int]
    ret out = []
    i, j = 0
    while i < len(A) and j < len(B)
      if A[i] < B[j]
        i += 1
      elif A[i] > B[j]
        j += 1
      else
        if not out or out[-1] != A[i]
          out <- A[i]
        i, j = i + 1, j + 1
