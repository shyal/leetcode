# REFERENCE: d132 Bottom Up Cell
class Solution:
    def cell(self, n, k):
        r, c = divmod(k - 1, n)
        return [n - 1 - r, c]
