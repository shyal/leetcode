# REFERENCE: d342 Getting a Different Number
class Solution
  def get_different_number(arr: [int]) -> int
    n = len(arr)
    seen = table(n + 1, fill=false)
    for x in arr
      if x <= n
        seen[x] = true
    seen.index(false)
