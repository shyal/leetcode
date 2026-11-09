# REFERENCE: d389 EPI 5.12 Sample offline data
class Solution:
    def random_sampling(self, k, A):
        for i in range(k):
            j = randint(i, len(A) - 1)
            A[i], A[j] = A[j], A[i]
