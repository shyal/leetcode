# REFERENCE: d541 Maximum Sum With No Two Adjacent Indices
class Solution
  def maxSum(nums: [int]) -> int
    a, b = 0, 0
    for x in nums
      a, b = b, max(b, a + x)
    b
