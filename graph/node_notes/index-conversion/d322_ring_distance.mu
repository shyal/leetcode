# REFERENCE: d322 Ring Distance
class Solution
  def dist(a: int, b: int, m: int) -> int
    d = abs(a - b)
    min(d, m - d)
