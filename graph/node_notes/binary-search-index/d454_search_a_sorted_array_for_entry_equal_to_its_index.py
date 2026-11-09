# REFERENCE: d454 EPI 11.2 Search a sorted array for entry equal to its index
class Solution:
    def search_entry_equal_to_its_index(self, A):
        lo, hi = 0, len(A) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if A[mid] < mid:
                lo = mid + 1
            elif A[mid] > mid:
                hi = mid - 1
            else:
                return mid
        return -1
