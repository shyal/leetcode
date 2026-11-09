# REFERENCE: d519 EPI 16.12 Find the longest nondecreasing subsequence
class Solution
  def longest_nondecreasing_subsequence_length(A: [int]) -> int
    ends = [1] * len(A)
    for i in 0..<len(A)
      for j in 0..<i
        if A[j] <= A[i]
          ends[i] = max(ends[i], ends[j] + 1)
    max(ends, default=0)
