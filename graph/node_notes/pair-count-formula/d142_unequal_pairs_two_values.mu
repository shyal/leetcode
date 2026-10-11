# REFERENCE: d142 Unequal Pairs From Two Values
class Solution
  def unequalPairs(nums: [int]) -> int
    a, b = counter(nums).values()
    a * b
