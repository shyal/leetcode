# REFERENCE: d152 Sum Of Positives
class Solution:
    def sumOfPositives(self, nums):
        return sum(x for x in nums if x > 0)
