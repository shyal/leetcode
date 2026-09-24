# REFERENCE: d20 Longest Run of Ones
def findMaxConsecutiveOnes(nums: [int]) -> int
  zeros, left = 0, 0
  for right, v in nums
    if v == 0
      zeros += 1
    if zeros
      if nums[left] == 0
        zeros -= 1
      left += 1
  len(nums) - left
