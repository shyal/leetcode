# REFERENCE: d301 Split Into A Run
class Solution
  def splitIntoRun(n: int, k: int) -> bool
    t = k * (k - 1) // 2
    n > t and (n - t) % k == 0
