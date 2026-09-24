# REFERENCE: d3 Permutations
def permute(nums: [int]) -> [[int]]
  def helper()
    if len(curr) == len(nums)
      ret <- curr[:]
      return
    for j in 0..<len(nums)
      if used[j]
        continue
      used[j] = true
      curr <- nums[j]
      helper()
      curr .
      used[j] = false

  ret = []
  curr = []
  used = table(len(nums), fill = false)
  helper()
  ret
