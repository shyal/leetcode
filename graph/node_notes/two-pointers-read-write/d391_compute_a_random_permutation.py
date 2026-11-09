# REFERENCE: d391 EPI 5.14 Compute a random permutation
class Solution:
    def compute_random_permutation(self, n):
        perm = list(range(n))
        for i in range(n):
            j = randint(i, n - 1)
            perm[i], perm[j] = perm[j], perm[i]
        return perm
