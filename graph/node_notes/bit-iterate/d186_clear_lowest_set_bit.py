# REFERENCE: d186 Clear Lowest Set Bit
class Solution:
    def clearLowestSetBit(self, x):
        return x & (x - 1)
