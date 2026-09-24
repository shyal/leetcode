# REFERENCE: d96 Largest Of The Last K
from dsa.monotonic_queue import MonotonicQueue, Type

def largestOfLastK(nums: [int], k: int) -> [int]
  q = MonotonicQueue(Type.decreasing)
  res = []
  for i, x in nums
    q.push((x, i))
    if q.front()[1] <= i - k
      q.popleft()
    res <- q.front()[0]
  res
