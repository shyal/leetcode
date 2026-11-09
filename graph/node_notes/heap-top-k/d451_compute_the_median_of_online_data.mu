# REFERENCE: d451 EPI 10.5 Compute the median of online data
class Solution
  def online_median(sequence: Iterator[int]) -> [float]
    low, high, out = heap(type=max), heap(), []
    for x in sequence
      low <- x
      high <- low .
      if len(high) > len(low)
        low <- high .
      out <- (len(low) > len(high) ? float(low.peek()) : (low.peek() + high.peek()) / 2)
    out
