# REFERENCE: d140 First False
class Solution:
    def firstFalse(self, lo, hi, ok):
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                lo = mid + 1
            else:
                hi = mid
        return lo
