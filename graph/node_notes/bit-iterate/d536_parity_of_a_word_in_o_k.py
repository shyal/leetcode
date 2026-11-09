# REFERENCE: d536 Parity of a Word in O(k)
class Solution:
    def parity(self, x):
        result = 0
        while x:
            result ^= 1
            x &= x - 1  # clear the lowest set bit
        return result
