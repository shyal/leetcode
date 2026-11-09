# REFERENCE: d478 EPI 13.5 Smallest nonconstructible value
class Solution
  def smallest_nonconstructible_value(A: [int]) -> int
    reach = 0
    for x in sort(A)
      if x > reach + 1
        break
      reach += x
    reach + 1
