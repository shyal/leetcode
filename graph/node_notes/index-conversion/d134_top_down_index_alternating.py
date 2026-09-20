# REFERENCE: d134 Top Down Index Alternating
class Solution:
    def index(self, n, r, c):
        if r % 2:
            c = n - 1 - c
        return r * n + c
