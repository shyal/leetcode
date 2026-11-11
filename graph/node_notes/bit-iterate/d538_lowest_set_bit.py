# REFERENCE: d538 Lowest Set Bit
class Solution:
    def lowestSetBit(self, x):
        return x & ~(x - 1)
