# REFERENCE: d381 EPI 5.4 Advancing through an array
class Solution
  def can_reach_end(A: [int]) -> bool
    reach = 0
    for >i, step in A
      if i > reach
        return false
      reach = max(reach, i + step)
    true
