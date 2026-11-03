# REFERENCE: d320 Maximum Subarray Sum With One Deletion
class Solution
  def maximumSum(nums: [int]) -> int
    kept = deleted = best = -inf
    for x in nums
      deleted = max(deleted + x, kept)
      kept = max(x, kept + x)
      best = max(best, kept, deleted)
    best
