# REFERENCE: d556 Multiples Of A And B
class Solution
  def multiples(n: int, a: int, b: int) -> int
    n // (a * b // gcd(a, b))
