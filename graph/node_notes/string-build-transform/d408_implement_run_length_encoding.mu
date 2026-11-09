# REFERENCE: d408 EPI 6.11 Implement run-length encoding
class Solution
  def encoding(s: str) -> str
    out, i = [], 0
    while i < len(s)
      j = i
      while j < len(s) and s[j] == s[i]
        j += 1
      out <- str(j - i) + s[i]
      i = j
    ''.join(out)

  def decoding(s: str) -> str
    out, count = [], 0
    for c in s
      if c.isdigit()
        count = count * 10 + int(c)
      else
        out <- c * count
        count = 0
    ''.join(out)
