# REFERENCE: d179 Divisible Difference Pairs
class Solution
  def divisiblePairs(nums: [int], m: int) -> int
    count_pairs(nums, by=n -> n % m)
