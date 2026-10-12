# REFERENCE: d301 Split Into A Run
class Solution:
    def splitIntoRun(self, n, k):
        t = k * (k - 1) // 2
        return n > t and (n - t) % k == 0
