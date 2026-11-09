# REFERENCE: d453 EPI 11.1 Search a sorted array for first occurrence of k
class Solution
  def search_first_of_k(A: [int], k: int) -> int
    lo, hi = 0, len(A)
    while lo < hi
      mid = (lo + hi) // 2
      if A[mid] < k
        lo = mid + 1
      else
        hi = mid
    lo < len(A) and A[lo] == k ? lo : -1
