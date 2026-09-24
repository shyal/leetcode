# REFERENCE: d8 Reuse Allowed
def combinationSum(nums: [int], target: int) -> [[int]]
  def helper(i, total)
    if total == target
      ret <- curr[:]
      return
    for j in i..<len(nums)
      if total + nums[j] > target
        break
      curr <- nums[j]
      helper(j, total + nums[j])
      curr .

  nums = sort(nums)
  ret = []
  curr = []
  helper(0, 0)
  ret
