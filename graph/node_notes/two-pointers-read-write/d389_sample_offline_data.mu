# REFERENCE: d389 EPI 5.12 Sample offline data
class Solution
  def random_sampling(k: int, A: [int])
    for i in 0..<k
      j = randint(i, len(A) - 1)
      A[i], A[j] = A[j], A[i]
