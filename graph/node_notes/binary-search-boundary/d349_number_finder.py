# REFERENCE: d349 Number Finder
class Solution:
    def find_first(self, array, num):
        lo, hi = 0, len(array)
        while lo < hi:
            mid = (lo + hi) // 2
            if array[mid] >= num:
                hi = mid
            else:
                lo = mid + 1
        return lo if lo < len(array) and array[lo] == num else -1
