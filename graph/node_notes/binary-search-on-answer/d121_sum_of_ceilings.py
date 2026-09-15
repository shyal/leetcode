# REFERENCE: d121 Sum Of Ceilings
class Solution:
    def sumOfCeilings(self, nums, k):
        return sum((x + k - 1) // k for x in nums)
