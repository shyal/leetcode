# REFERENCE: d21 Slide, Never Shrink
def longestOnes(nums: [int], k: int) -> int
  zeros, left = 0, 0
  for right, v in nums
    if v == 0
      zeros += 1
    if zeros > k
      if nums[left] == 0
        zeros -= 1
      left += 1
  len(nums) - left
