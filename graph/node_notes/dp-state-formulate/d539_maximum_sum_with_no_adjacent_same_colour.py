# REFERENCE: d539 Maximum Sum With No Adjacent Same Colour
class Solution:
    def maxSum(self, nums, colors):
        n = len(nums)
        best = [0] * (n + 2)
        for i in range(n - 1, -1, -1):
            same = i + 1 < n and colors[i] == colors[i + 1]
            best[i] = max(best[i + 1], nums[i] + best[i + 2 if same else i + 1])
        return best[0]
