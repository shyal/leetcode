# REFERENCE: d387 EPI 5.10 Permute the elements of an array
class Solution
  def apply_permutation(perm: [int], A: list)
    for i in 0..<len(A)
      while perm[i] != i
        j = perm[i]
        A[i], A[j] = A[j], A[i]
        perm[i], perm[j] = perm[j], perm[i]
