# REFERENCE: d369 EPI 4.3 Reverse bits
class Solution
  def __init__()
    self.rev = [0] * 65536
    for i in 1..<65536
      self.rev[i] = (self.rev[i >> 1] >> 1) | ((i & 1) << 15)

  def reverse_bits(x: int) -> int
    out = 0
    for 0..<4
      out = (out << 16) | self.rev[x & 0xFFFF]
      x >>= 16
    out
