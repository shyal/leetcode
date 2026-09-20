# REFERENCE: d136 Bottom Up Index Alternating
class Solution:
    def index(self, n, r, c):
        r = n - 1 - r
        if r % 2:
            c = n - 1 - c
        return r * n + c
