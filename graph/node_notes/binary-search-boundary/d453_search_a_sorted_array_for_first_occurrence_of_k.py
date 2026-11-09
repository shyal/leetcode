# REFERENCE: d453 EPI 11.1 Search a sorted array for first occurrence of k
class Solution:
    def search_first_of_k(self, A, k):
        lo, hi = 0, len(A)
        while lo < hi:
            mid = (lo + hi) // 2
            if A[mid] < k:
                lo = mid + 1
            else:
                hi = mid
        return lo if lo < len(A) and A[lo] == k else -1
