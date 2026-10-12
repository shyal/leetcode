# REFERENCE: d300 Sum Of A Run
class Solution
  def sumOfRun(n: int, k: int) -> int
    (2 * n + k - 1) * k // 2
