# REFERENCE: d372 EPI 4.6 Compute quotient without arithmetical operators
class Solution:
    def divide(self, x, y):
        shift = 0
        while y << (shift + 1) <= x:
            shift += 1
        out = 0
        while shift >= 0:
            if y << shift <= x:
                x -= y << shift
                out += 1 << shift
            shift -= 1
        return out
