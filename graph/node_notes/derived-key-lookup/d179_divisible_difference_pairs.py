# REFERENCE: d179 Divisible Difference Pairs
class Solution:
    def divisiblePairs(self, nums, m):
        return count_pairs(nums, key=lambda n: n % m)
