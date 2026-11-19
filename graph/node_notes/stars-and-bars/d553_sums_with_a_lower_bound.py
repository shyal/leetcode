# REFERENCE: d553 Sums With A Lower Bound
class Solution:
    def sumsFrom(self, n, k, m):
        return 0 if n < m else comb(n - m + k - 1, k - 1)  # give m to the first integer, then count the sums of n - m
