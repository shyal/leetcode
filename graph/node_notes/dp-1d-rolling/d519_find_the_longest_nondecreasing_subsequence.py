# REFERENCE: d519 EPI 16.12 Find the longest nondecreasing subsequence
class Solution:
    def longest_nondecreasing_subsequence_length(self, A):
        ends = [1] * len(A)
        for i in range(len(A)):
            for j in range(i):
                if A[j] <= A[i]:
                    ends[i] = max(ends[i], ends[j] + 1)
        return max(ends, default=0)
