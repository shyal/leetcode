# REFERENCE: d536 Parity of a Word in O(k)
class Solution
  def parity(x: int) -> int
    result = 0
    while x
      result ^= 1
      x &= x - 1  # clear the lowest set bit
    result
