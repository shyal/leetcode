# REFERENCE: d391 EPI 5.14 Compute a random permutation
class Solution
  def compute_random_permutation(n: int) -> [int]
    ret perm = list(0..<n)
    for i in 0..<n
      j = randint(i, n - 1)
      perm[i], perm[j] = perm[j], perm[i]
