# REFERENCE: d173 Largest By Flag
def largestByFlag(nums: [int], flag: [bool]) -> [int]
  pools = {true: [], false: []}
  for (x, f) in zip(nums, flag)
    pools[f] <- x
  pools[true].sort()
  pools[false].sort()
  [pools[f].pop() for f in flag]
