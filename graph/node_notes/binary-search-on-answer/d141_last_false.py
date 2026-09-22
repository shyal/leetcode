# REFERENCE: d141 Last False
class Solution:
    def lastFalse(self, lo, hi, ok):
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ok(mid):
                hi = mid - 1
            else:
                lo = mid
        return lo
