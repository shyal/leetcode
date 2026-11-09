# REFERENCE: d390 EPI 5.13 Sample online data
class Solution
  def online_random_sample(stream: Iterator[int], k: int) -> [int]
    ret sample = []
    for seen, x in enumerate(stream, 1)
      if seen <= k
        sample <- x
      else
        j = randrange(seen)
        if j < k
          sample[j] = x
