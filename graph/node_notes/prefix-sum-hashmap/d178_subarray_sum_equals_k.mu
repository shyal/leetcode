# REFERENCE: d178 Subarray Sum Equals K
def subarraySum(nums: [int], k: int) -> int
  D = {:int}
  D[0] = 1
  prefix = 0
  res = 0
  for i, n in nums
    prefix += n
    if D[prefix - k]
      res += D[prefix - k]
    D[prefix] += 1
  res
