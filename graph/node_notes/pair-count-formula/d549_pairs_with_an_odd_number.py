# REFERENCE: d549 Pairs With An Odd Number
class Solution:
    def odd_pairs(self, nums):
        n = len(nums)
        evens = sum(x % 2 == 0 for x in nums)
        return n * (n - 1) // 2 - evens * (evens - 1) // 2  # all pairs, minus the pairs of two evens
