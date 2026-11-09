# REFERENCE: d379 EPI 5.2 Increment an arbitrary-precision integer
class Solution
  def plus_one(A: [int]) -> [int]
    i = len(A) - 1
    while i >= 0 and A[i] == 9
      A[i] = 0
      i -= 1
    if i < 0
      A[0] = 1
      A <- 0
    else
      A[i] += 1
    A
