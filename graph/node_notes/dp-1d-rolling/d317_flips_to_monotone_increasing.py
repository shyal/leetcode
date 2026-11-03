# REFERENCE: d317 Flips To Monotone Increasing
class Solution:
    def minFlips(self, s):
        ones = flips = 0
        for c in s:
            if c == '1':
                ones += 1
            else:
                flips = min(flips + 1, ones)
        return flips
