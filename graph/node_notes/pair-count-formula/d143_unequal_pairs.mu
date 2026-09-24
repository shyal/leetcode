# REFERENCE: d143 Unequal Pairs
def unequalPairs(nums: [int]) -> int
  count, left = 0, 0
  for c in counter(nums).values()
    count += left * c
    left += c
  count
