# REFERENCE: d455 EPI 11.3 Search a cyclically sorted array
class Solution
  def search_smallest(A: [int]) -> int
    lo, hi = 0, len(A) - 1
    while lo < hi
      mid = (lo + hi) // 2
      if A[mid] > A[hi]
        lo = mid + 1
      else
        hi = mid
    lo
