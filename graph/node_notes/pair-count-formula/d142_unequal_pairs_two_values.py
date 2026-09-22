# REFERENCE: d142 Unequal Pairs From Two Values
class Solution:
    def unequalPairs(self, nums):
        a, b = Counter(nums).values()
        return a * b
