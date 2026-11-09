# REFERENCE: d405 EPI 6.8 Convert from Roman to decimal
class Solution
  def roman_to_integer(s: str) -> int
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = value[s[-1]]
    for i in 0..<len(s) - 1
      v = value[s[i]]
      total += v < value[s[i + 1]] ? -v : v
    total
