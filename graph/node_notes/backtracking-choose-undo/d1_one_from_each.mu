# REFERENCE: d1 One From Each
def combos(groups: [[str]]) -> [str]
  def helper(d)
    if d == len(groups)
      ret <- "".join(curr)
      return
    for x in groups[d]
      curr <- x
      helper(d + 1)
      curr .

  ret = []
  curr = []
  helper(0)
  ret
