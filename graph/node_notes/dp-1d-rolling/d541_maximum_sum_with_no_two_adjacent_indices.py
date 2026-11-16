# REFERENCE: d541 Maximum Sum With No Two Adjacent Indices
class Solution:
    def maxSum(self, nums):
        a = b = 0
        for x in nums:
            a, b = b, max(b, a + x)
        return b
