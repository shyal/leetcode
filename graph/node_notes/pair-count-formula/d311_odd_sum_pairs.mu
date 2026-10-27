# REFERENCE: d311 Odd Sum Pairs
class Solution
  def oddSumPairs(a: [int], b: [int]) -> int
    odd_a = count for a if odd(_)
    odd_b = count for b if odd(_)
    even_a = len(a) - odd_a
    even_b = len(b) - odd_b
    odd_a * even_b + even_a * odd_b
