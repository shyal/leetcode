# REFERENCE: d552 Sums Of K Parts
class Solution:
    def sums(self, n, k):
        return comb(n + k - 1, k - 1)  # n stars and k - 1 bars in a row: choose the places of the bars
