# REFERENCE: d131 Top Down Cell From One
class Solution:
    def cell(self, n, k):
        r, c = divmod(k - 1, n)
        return [r, c]
