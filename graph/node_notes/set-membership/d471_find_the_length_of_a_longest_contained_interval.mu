# REFERENCE: d471 EPI 12.9 Find the length of a longest contained interval
class Solution
  def longest_contained_range(A: [int]) -> int
    values = set(A)
    ret best = 0
    for x in values
      if x - 1 not in values
        y = x
        while y + 1 in values
          y += 1
        best = max(best, y - x + 1)
