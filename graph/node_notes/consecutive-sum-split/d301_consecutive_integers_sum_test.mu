# REFERENCE: d301 Consecutive Integers Sum Test
class Solution
  def isConsecutiveSum(n: int, k: int) -> bool
    t = k * (k - 1) // 2
    n > t and (n - t) % k == 0
