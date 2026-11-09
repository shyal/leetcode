# REFERENCE: d369 EPI 4.3 Reverse bits
class Solution:
    def __init__(self):
        self.rev = [0] * (1 << 16)
        for i in range(1, 1 << 16):
            self.rev[i] = (self.rev[i >> 1] >> 1) | ((i & 1) << 15)

    def reverse_bits(self, x):
        out = 0
        for _ in range(4):
            out = (out << 16) | self.rev[x & 0xFFFF]
            x >>= 16
        return out
