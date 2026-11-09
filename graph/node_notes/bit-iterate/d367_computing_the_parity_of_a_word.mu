# REFERENCE: d367 EPI 4.1 Computing the parity of a word
class Solution
  def parity(x: int) -> int
    for shift in (32, 16, 8, 4, 2, 1)
      x ^= x >> shift
    x & 1
