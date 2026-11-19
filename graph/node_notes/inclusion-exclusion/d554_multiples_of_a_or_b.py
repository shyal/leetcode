# REFERENCE: d554 Multiples Of A Or B
class Solution:
    def multiples(self, n, a, b):
        return n // a + n // b - n // (a * b // gcd(a, b))  # the multiples of both were counted twice: take them away once
