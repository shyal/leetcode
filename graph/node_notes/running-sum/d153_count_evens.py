# REFERENCE: d153 Count Evens
class Solution:
    def countEvens(self, nums):
        return sum(1 for x in nums if x % 2 == 0)
