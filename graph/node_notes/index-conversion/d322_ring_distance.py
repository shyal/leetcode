# REFERENCE: d322 Ring Distance
class Solution:
    def dist(self, a, b, m):
        d = abs(a - b)
        return min(d, m - d)
