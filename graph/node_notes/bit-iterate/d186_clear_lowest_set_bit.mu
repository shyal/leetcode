# REFERENCE: d186 Clear Lowest Set Bit
def clearLowestSetBit(x: int) -> int
  x & (x - 1)
