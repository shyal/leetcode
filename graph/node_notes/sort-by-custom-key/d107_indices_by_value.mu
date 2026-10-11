# REFERENCE: d107 Indices By Value
class Solution
  def indicesByValue(nums2: [int]) -> [int]
    sort(0..<len(nums2), by = i -> nums2[i])
