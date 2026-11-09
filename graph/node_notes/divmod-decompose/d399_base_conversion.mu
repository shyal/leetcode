# REFERENCE: d399 EPI 6.2 Base conversion
class Solution
  def convert_base(num_as_string: str, b1: int, b2: int) -> str
    DIGITS = '0123456789ABCDEF'
    negative = num_as_string[0] == '-'
    n = 0
    for c in num_as_string[negative:]
      n = n * b1 + DIGITS.index(c)
    out = []
    while true
      n, d = divmod(n, b2)
      out <- DIGITS[d]
      if n == 0
        break
    '-' * negative + ''.join(reversed(out))
