# REFERENCE: d500 EPI 15.4 Generate permutations
class Solution
  def permutations(A: [int]) -> [[int]]
    ret out, perm = []..
    used = [false] * len(A)
    def extend()
      if len(perm) == len(A)
        out <- perm[:]
        return
      for >i, x in A
        if not used[i]
          used[i] = true
          perm <- x
          extend()
          perm .
          used[i] = false
    extend()
