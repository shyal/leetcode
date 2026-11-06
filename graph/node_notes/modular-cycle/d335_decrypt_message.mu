# REFERENCE: d335 Decrypt Message
class Solution
  def decrypt(word: str) -> str
    prev = 1
    out = []
    for c in word
      v = (ord(c) - prev - 97) % 26 + 97
      out <- chr(v)
      prev += v
    ''.join(out)
