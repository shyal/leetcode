# REFERENCE: d77 Each Element Once
def sumOnce(nums: [int], target: int) -> [[int]]
  def helper(i, total)
    if total == target
      ret <- curr[:]
      return
    for j in i..<len(nums)
      if total + nums[j] > target
        break
      curr <- nums[j]
      helper(j + 1, total + nums[j])
      curr .

  ret = []
  curr = []
  helper(0, 0)
  ret
