# REFERENCE: d371 EPI 4.5 Compute product without arithmetical operators
class Solution:
    def multiply(self, x, y):
        def add(a, b):
            while b:
                a, b = a ^ b, (a & b) << 1
            return a

        out = 0
        while x:
            if x & 1:
                out = add(out, y)
            x, y = x >> 1, y << 1
        return out
