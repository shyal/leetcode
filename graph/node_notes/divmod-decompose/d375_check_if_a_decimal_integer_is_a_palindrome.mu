# REFERENCE: d375 EPI 4.9 Check if a decimal integer is a palindrome
class Solution
  def is_palindrome_number(x: int) -> bool
    if x < 0
      return false
    high = 1
    while high * 10 <= x
      high *= 10
    while high > 1
      if x // high != x % 10
        return false
      x = x % high // 10
      high //= 100
    true
