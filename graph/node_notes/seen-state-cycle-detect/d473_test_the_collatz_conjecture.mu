# REFERENCE: d473 EPI 12.11 Test the Collatz conjecture
class Solution
  def test_collatz_conjecture(n: int) -> bool
    for start in 3..n by 2
      path, x = set(), start
      while x >= start
        if x in path
          return false
        path.add(x)
        x = x is even ? x // 2 : 3x + 1
    true
