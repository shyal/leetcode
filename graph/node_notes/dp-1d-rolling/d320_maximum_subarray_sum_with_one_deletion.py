# REFERENCE: d320 Maximum Subarray Sum With One Deletion
class Solution:
    def maximumSum(self, nums):
        kept = deleted = best = -inf
        for x in nums:
            deleted = max(deleted + x, kept)
            kept = max(x, kept + x)
            best = max(best, kept, deleted)
        return best
