# REFERENCE: d115 First True
class Solution:
    def firstTrue(self, lo, hi, ok):
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
