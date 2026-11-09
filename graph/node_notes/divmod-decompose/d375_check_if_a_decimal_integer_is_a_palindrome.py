# REFERENCE: d375 EPI 4.9 Check if a decimal integer is a palindrome
class Solution:
    def is_palindrome_number(self, x):
        if x < 0:
            return False
        high = 1
        while high * 10 <= x:
            high *= 10
        while high > 1:
            if x // high != x % 10:
                return False
            x = x % high // 10
            high //= 100
        return True
