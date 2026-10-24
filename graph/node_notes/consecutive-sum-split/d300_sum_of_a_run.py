# REFERENCE: d300 Sum Of A Run
class Solution:
    def sumOfRun(self, s, c):
        return (2 * s + c - 1) * c // 2
