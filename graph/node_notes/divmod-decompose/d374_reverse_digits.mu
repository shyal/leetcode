# REFERENCE: d374 EPI 4.8 Reverse digits
class Solution
  def reverse(x: int) -> int
    out, rest = 0, abs(x)
    while rest
      rest, d = divmod(rest, 10)
      out = out * 10 + d
    x >= 0 ? out : -out
