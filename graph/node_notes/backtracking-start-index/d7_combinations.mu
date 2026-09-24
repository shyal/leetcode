# REFERENCE: d7 Combinations
def combine(n: int, k: int) -> [[int]]
  def helper(i)
    if len(curr) == k
      ret <- curr[:]
      return
    for j in i..n
      curr <- j
      helper(j + 1)
      curr .

  ret = []
  curr = []
  helper(1)
  ret
