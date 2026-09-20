# REFERENCE: d131 Bottom Up Cell
class Solution:
    def cell(self, n, k):
        r, c = divmod(k, n)
        return [n - 1 - r, c]
