# REFERENCE: d106 Order By Other Array
def orderByOther(nums1: [int], nums2: [int]) -> [int]
  idx = sort(0..<len(nums2), by = i -> nums2[i])
  [nums1[i] for i in idx]
