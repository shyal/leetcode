# REFERENCE: d462 EPI 11.10 Find the duplicate and missing elements
class Solution
  def find_duplicate_missing(A: [int]) -> (int, int)
    both = 0
    for i, a in enumerate(A)
      both ^= i ^ a
    bit = both & -both
    x = 0
    for i, a in enumerate(A)
      if i & bit
        x ^= i
      if a & bit
        x ^= a
    x in A ? (x, x ^ both) : (x ^ both, x)
