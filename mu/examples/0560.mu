# 560. Subarray Sum Equals K
def subarraySum(nums: [int], k: int) -> int
  cnt = counter([0])
  sum for p in scan(+, nums)
    got = cnt[p - k]
    cnt[p] += 1
    got
