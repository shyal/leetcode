# REFERENCE: d12 Kth Smallest Bounded Value
def kthSmallest(nums: [int], k: int) -> int
  count = table(101, fill = 0)
  for x in nums
    count[x] += 1
  for v in 0..100
    k -= count[v]
    if k <= 0
      return v
