# REFERENCE: d539 Maximum Sum With No Adjacent Same Colour
class Solution
  def maxSum(nums: [int], colors: [int]) -> int
    n = len nums
    memo {
      (i) ->
        if i >= n
          return 0
        same = i + 1 < n and colors[i] == colors[i + 1]
        max(mu(i + 1), nums[i] + mu(same ? i + 2 : i + 1))
    }(0)
