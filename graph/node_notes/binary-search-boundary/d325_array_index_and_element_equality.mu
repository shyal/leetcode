# REFERENCE: d325 Array Index & Element Equality
class Solution
  def index_equals_value_search(arr: [int]) -> int
    lo, hi = 0, len(arr)
    while lo < hi
      mid = (lo + hi) // 2
      if arr[mid] - mid >= 0
        hi = mid
      else
        lo = mid + 1
    lo if lo < len(arr) and arr[lo] == lo else -1
