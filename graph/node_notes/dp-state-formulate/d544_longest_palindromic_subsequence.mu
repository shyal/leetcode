# REFERENCE: d544 Longest Palindromic Subsequence
class Solution
  def longestPalindromeSubseq(s: str) -> int
    memo f(i, j) =
      | i > j        -> 0
      | i == j       -> 1
      | s[i] == s[j] -> 2 + f(i + 1, j - 1)
      | else         -> max(f(i + 1, j), f(i, j - 1))
    f(0, len(s) - 1)
