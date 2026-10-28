# REFERENCE: d314 Even Subarrays
class Solution
  def evenSubarrays(nums: [int]) -> int
    count_subarrays(nums, v -> v % 2 == 0)
