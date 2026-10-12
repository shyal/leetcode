# REFERENCE: d300 Sum Of A Run
class Solution:
    def sumOfRun(self, n, k):
        return (2 * n + k - 1) * k // 2
