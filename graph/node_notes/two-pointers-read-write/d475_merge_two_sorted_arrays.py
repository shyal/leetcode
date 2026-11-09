# REFERENCE: d475 EPI 13.2 Merge two sorted arrays
class Solution:
    def merge_two_sorted_arrays(self, A, m, B, n):
        i, j = m - 1, n - 1
        for w in range(m + n - 1, -1, -1):
            if j < 0 or i >= 0 and A[i] > B[j]:
                A[w], i = A[i], i - 1
            else:
                A[w], j = B[j], j - 1
