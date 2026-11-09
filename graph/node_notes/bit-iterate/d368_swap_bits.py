# REFERENCE: d368 EPI 4.2 Swap bits
class Solution:
    def swap_bits(self, x, i, j):
        if (x >> i) & 1 != (x >> j) & 1:
            x ^= (1 << i) | (1 << j)
        return x
