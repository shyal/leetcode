# REFERENCE: d353 Root of Number
class Solution:
    def root(self, x, n):
        lo, hi = 0.0, max(1.0, x)
        while hi - lo >= 0.001:
            mid = (lo + hi) / 2
            if mid**n > x:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2
