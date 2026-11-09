# REFERENCE: d373 EPI 4.7 Compute pow(x,y)
class Solution
  def power(x: float, y: int) -> float
    if y < 0
      x, y = 1 / x, -y
    out = 1.0
    while y
      if y & 1
        out *= x
      x *= x
      y >>= 1
    out
