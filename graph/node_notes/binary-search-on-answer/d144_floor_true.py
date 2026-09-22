# REFERENCE: d144 Floor True
class Solution:
    def floorTrue(self, lo, hi, ok):
        while lo <= hi:
            mid = (lo + hi) // 2
            if ok(mid):
                lo = mid + 1
            else:
                hi = mid - 1
        return hi
