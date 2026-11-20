# REFERENCE: d556 Multiples Of A And B
class Solution:
    def multiples(self, n, a, b):
        return n // (a * b // gcd(a, b))  # the integers that a and b divide are the multiples of the lcm
