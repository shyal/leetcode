# REFERENCE: d132 Alternating Cell
class Solution:
    def cell(self, n, k):
        r, c = divmod(k, n)
        if r % 2:
            c = n - 1 - c
        return [n - 1 - r, c]
