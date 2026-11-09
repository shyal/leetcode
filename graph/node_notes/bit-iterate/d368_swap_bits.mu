# REFERENCE: d368 EPI 4.2 Swap bits
class Solution
  def swap_bits(x: int, i: int, j: int) -> int
    if (x >> i) & 1 != (x >> j) & 1
      x ^= (1 << i) | (1 << j)
    x
