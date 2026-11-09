# REFERENCE: d407 EPI 6.10 Write a string sinusoidally
class Solution
  def snake_string(s: str) -> str
    s[1::4] + s[::2] + s[3::4]
