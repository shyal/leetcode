# REFERENCE: d537 Odd Sum Subarrays
class Solution
  def oddSumSubarrays(nums: [int]) -> int
    oddc = 0
    for prefix in scan(+, nums)
      oddc += prefix is odd
    evenc = len nums - oddc + 1
    oddc * evenc
