# REFERENCE: d554 Multiples Of A Or B
class Solution
  def multiples(n: int, a: int, b: int) -> int
    n // a + n // b - n // (a * b // gcd(a, b))
