# REFERENCE: d523 EPI 17.4 The 3-sum problem
class Solution
  def has_three_sum(A: [int], t: int) -> bool
    A.sort()
    for a in A
      i, j = 0, len(A) - 1
      while i <= j
        s = a + A[i] + A[j]
        if s == t
          return true
        if s < t
          i += 1
        else
          j -= 1
    false
