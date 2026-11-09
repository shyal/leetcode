# REFERENCE: d398 EPI 6.1 Interconvert strings and integers
class Solution
  def int_to_string(x: int) -> str
    sign, x = (x < 0 ? '-' : ''), abs(x)
    out = []
    while true
      x, d = divmod(x, 10)
      out <- chr(ord('0') + d)
      if x == 0
        break
    sign + ''.join(reversed(out))

  def string_to_int(s: str) -> int
    n = 0
    for c in s[s[0] in '+-':]
      n = n * 10 + ord(c) - ord('0')
    s[0] == '-' ? -n : n
