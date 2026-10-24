# REFERENCE: d300 Sum Of Consecutive Integers
class Solution:
    def sumOfConsecutive(self, s, c):
        return (2 * s + c - 1) * c // 2
