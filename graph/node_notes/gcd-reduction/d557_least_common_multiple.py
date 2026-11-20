# REFERENCE: d557 Least Common Multiple
class Solution:
    def lcm(self, a, b):
        return a * b // gcd(a, b)  # the product has the common factor two times, the gcd removes it one time
