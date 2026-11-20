# REFERENCE: d557 Least Common Multiple
class Solution
  def lcm(a: int, b: int) -> int
    a * b // gcd(a, b)
