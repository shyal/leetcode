# REFERENCE: d130 Top Down Cell
class Solution:
    def cell(self, n, k):
        r, c = divmod(k, n)
        return [r, c]
