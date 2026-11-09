# REFERENCE: d460 EPI 11.8 Find the kth largest element
class Solution
  def find_kth_largest(k: int, A: [int]) -> int
    lo, hi = 0, len(A) - 1
    while true
      p = randint(lo, hi)
      A[p], A[hi] = A[hi], A[p]
      w = lo
      for r in lo..<hi
        if A[r] > A[hi]
          A[w], A[r] = A[r], A[w]
          w += 1
      A[w], A[hi] = A[hi], A[w]
      if w == k - 1
        return A[w]
      if w < k - 1
        lo = w + 1
      else
        hi = w - 1
