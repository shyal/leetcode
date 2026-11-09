# REFERENCE: d502 EPI 15.6 Generate all subsets of size k
class Solution:
    def combinations(self, n, k):
        out, subset = [], []

        def grow(start):
            if len(subset) == k:
                out.append(subset[:])
                return
            for x in range(start, n - (k - len(subset)) + 2):
                subset.append(x)
                grow(x + 1)
                subset.pop()

        grow(1)
        return out
