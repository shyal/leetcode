# REFERENCE: d301 Consecutive Integers Sum Test
class Solution:
    def isConsecutiveSum(self, n, k):
        t = k * (k - 1) // 2
        return n > t and (n - t) % k == 0
