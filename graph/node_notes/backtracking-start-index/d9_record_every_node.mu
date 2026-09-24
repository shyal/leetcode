# REFERENCE: d9 Record Every Node
def subsets(nums: [int]) -> [[int]]
  def helper(i)
    ret <- curr[:]
    for j in i..<len(nums)
      curr <- nums[j]
      helper(j + 1)
      curr .

  ret = []
  curr = []
  helper(0)
  ret
