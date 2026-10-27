# REFERENCE: d311 Odd Sum Pairs
class Solution:
    def oddSumPairs(self, a, b):
        odd_a = sum(x % 2 for x in a)
        odd_b = sum(y % 2 for y in b)
        even_a = len(a) - odd_a
        even_b = len(b) - odd_b
        return odd_a * even_b + even_a * odd_b
