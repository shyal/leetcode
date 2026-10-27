# REFERENCE: d310 Negative Positive Pairs
class Solution:
    def negativePositivePairs(self, a, b):
        neg = sum(x < 0 for x in a)
        pos = sum(y > 0 for y in b)
        return neg * pos
