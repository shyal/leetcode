# REFERENCE: d452 EPI 10.6 Compute the k largest elements in a max-heap
class Solution
  def k_largest_in_binary_heap(A: [int], k: int) -> [int]
    cand, out = heap([(A[0], 0)], type=max), []
    while len(out) < k
      x, i = cand .
      out <- x
      for c in (2i + 1, 2i + 2)
        if c < len(A)
          cand <- (A[c], c)
    out
