# REFERENCE: d154 Largest Even
class Solution:
    def largestEven(self, nums):
        return max((x for x in nums if x % 2 == 0), default=-1)
