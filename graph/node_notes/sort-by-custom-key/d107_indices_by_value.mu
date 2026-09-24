# REFERENCE: d107 Indices By Value
def indicesByValue(nums2: [int]) -> [int]
  sort(0..<len(nums2), by = i -> nums2[i])
