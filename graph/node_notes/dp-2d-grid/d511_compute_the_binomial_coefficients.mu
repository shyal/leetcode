# REFERENCE: d511 EPI 16.4 Compute the binomial coefficients
class Solution
  def compute_binomial_coefficient(n: int, k: int) -> int
    row = [1] + [0] * k
    for i in 1..n
      for j in min(i, k)..1 by -1
        row[j] += row[j - 1]
    row[k]
