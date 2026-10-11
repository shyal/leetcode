# REFERENCE: d186 Clear Lowest Set Bit
class Solution
  def clearLowestSetBit(x: int) -> int
    x & (x - 1)
