# REFERENCE: d76 Choose From an Array
def choose(nums: [int], k: int) -> [[int]]
  def helper(i)
    if len(curr) == k
      ret <- curr[:]
      return
    for j in i..<len(nums)
      curr <- nums[j]
      helper(j + 1)
      curr .

  ret = []
  curr = []
  helper(0)
  ret
