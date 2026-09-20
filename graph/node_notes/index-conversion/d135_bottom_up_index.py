# REFERENCE: d135 Bottom Up Index
class Solution:
    def index(self, n, r, c):
        return (n - 1 - r) * n + c
