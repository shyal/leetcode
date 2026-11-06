# REFERENCE: d349 Number Finder
class Solution
  def find_first(array: [int], num: int) -> int
    lo, hi = 0, len(array)
    while lo < hi
      mid = (lo + hi) // 2
      if array[mid] >= num
        hi = mid
      else
        lo = mid + 1
    lo if lo < len(array) and array[lo] == num else -1
