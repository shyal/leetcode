# REFERENCE: d143 Unequal Pairs
class Solution:
    def unequalPairs(self, nums):
        count = left = 0
        for c in Counter(nums).values():
            count += left * c
            left += c
        return count
