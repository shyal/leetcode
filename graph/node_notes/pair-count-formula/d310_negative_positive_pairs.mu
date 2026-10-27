# REFERENCE: d310 Negative Positive Pairs
class Solution
  def negativePositivePairs(a: [int], b: [int]) -> int
    neg = count for a if _ < 0
    pos = count for b if _ > 0
    neg * pos
