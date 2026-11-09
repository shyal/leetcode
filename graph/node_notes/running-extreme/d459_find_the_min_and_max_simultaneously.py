# REFERENCE: d459 EPI 11.7 Find the min and max simultaneously
class Solution:
    def find_min_max(self, A):
        n = len(A)
        if n % 2:
            lo = hi = A[0]
            start = 1
        else:
            lo, hi = (A[0], A[1]) if A[0] < A[1] else (A[1], A[0])
            start = 2
        for i in range(start, n, 2):
            a, b = (A[i], A[i + 1]) if A[i] < A[i + 1] else (A[i + 1], A[i])
            if a < lo:
                lo = a
            if hi < b:
                hi = b
        return lo, hi
