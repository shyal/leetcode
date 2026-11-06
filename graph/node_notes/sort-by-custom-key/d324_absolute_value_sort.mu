# REFERENCE: d324 Absolute Value Sort
class Solution
  def absSort(arr: [int]) -> [int]
    sort(arr, by = x -> (abs(x), x))
