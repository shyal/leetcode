# REFERENCE: d179 Divisible Difference Pairs
def divisiblePairs(nums: [int], m: int) -> int
  cnt = counter()
  sum for x in nums
    got = cnt[x % m]
    cnt[x % m] += 1
    got
