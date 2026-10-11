# REFERENCE: d5 Pairs
class Solution
  def pairs(n: int) -> [[int]]
    [[a, b] for a in 0..<n for b in a + 1..<n]
