# REFERENCE: d370 EPI 4.4 Find a closest integer with the same weight
class Solution:
    def closest_int_same_bit_count(self, x):
        for i in range(63):
            if (x >> i) & 1 != (x >> (i + 1)) & 1:
                return x ^ (0b11 << i)
