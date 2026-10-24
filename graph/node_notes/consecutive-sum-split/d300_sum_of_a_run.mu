# REFERENCE: d300 Sum Of A Run
class Solution
  def sumOfRun(s: int, c: int) -> int
    (2 * s + c - 1) * c // 2
