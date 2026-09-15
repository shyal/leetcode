# REFERENCE: d120 Last True
class Solution:
    def lastTrue(self, lo, hi, ok):
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ok(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
