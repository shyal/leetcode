# REFERENCE: d538 Lowest Set Bit
class Solution
  def lowestSetBit(x: int) -> int
    x & ~(x - 1)
