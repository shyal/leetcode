# REFERENCE: d319 Maximum Alternating Subarray Sum
class Solution:
    def maxAlternatingSum(self, nums):
        plus = minus = best = -inf
        for x in nums:
            plus, minus = max(x, minus + x), plus - x
            best = max(best, plus, minus)
        return best
