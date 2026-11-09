# REFERENCE: d507 EPI 15.11 Compute a Gray code
class Solution
  def gray_code(num_bits: int) -> [int]
    ret codes = [0]
    for bit in 0..<num_bits
      codes += [x | 1 << bit for x in reversed(codes)]
