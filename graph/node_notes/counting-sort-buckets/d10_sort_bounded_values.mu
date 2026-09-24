# REFERENCE: d10 Sort Bounded Values
def sortBounded(nums: [int]) -> [int]
  count = table(101, fill = 0)
  for x in nums
    count[x] += 1
  [v for v in 0..100 for _ in 0..<count[v]]
