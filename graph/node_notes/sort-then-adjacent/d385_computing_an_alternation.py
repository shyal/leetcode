# REFERENCE: d385 EPI 5.8 Computing an alternation
class Solution:
    def rearrange(self, A):
        for i in range(1, len(A)):
            if (i % 2 == 1 and A[i - 1] > A[i]) or (i % 2 == 0 and A[i - 1] < A[i]):
                A[i - 1], A[i] = A[i], A[i - 1]
