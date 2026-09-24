# REFERENCE: d2 No Repeat Siblings
def subsetsWithDup(nums: [int]) -> [[int]]
  def helper(i)
    ret <- curr[:]
    for j in i..<len(nums)
      if j > i and nums[j] == nums[j - 1]
        continue
      curr <- nums[j]
      helper(j + 1)
      curr .

  ret = []
  curr = []
  helper(0)
  ret
