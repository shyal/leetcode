# REFERENCE: d300 Sum Of Consecutive Integers
class Solution
  def sumOfConsecutive(s: int, c: int) -> int
    (2 * s + c - 1) * c // 2
