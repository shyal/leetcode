# REFERENCE: d371 EPI 4.5 Compute product without arithmetical operators
class Solution
  def multiply(x: int, y: int) -> int
    def plus(a, b)
      while b
        a, b = a ^ b, (a & b) << 1
      a
    out = 0
    while x
      if x & 1
        out = plus(out, y)
      x, y = x >> 1, y << 1
    out
