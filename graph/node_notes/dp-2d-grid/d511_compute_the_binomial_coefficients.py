# REFERENCE: d511 EPI 16.4 Compute the binomial coefficients
class Solution:
    def compute_binomial_coefficient(self, n, k):
        row = [1] + [0] * k
        for i in range(1, n + 1):
            for j in range(min(i, k), 0, -1):
                row[j] += row[j - 1]
        return row[k]
