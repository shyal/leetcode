# REFERENCE: d388 EPI 5.11 Compute the next permutation
class Solution
  def next_permutation(perm: [int]) -> [int]
    i = len(perm) - 2
    while i >= 0 and perm[i] >= perm[i + 1]
      i -= 1
    if i < 0
      return []
    j = len(perm) - 1
    while perm[j] <= perm[i]
      j -= 1
    perm[i], perm[j] = perm[j], perm[i]
    lo, hi = i + 1, len(perm) - 1
    while lo < hi
      perm[lo], perm[hi] = perm[hi], perm[lo]
      lo += 1
      hi -= 1
    perm
