# 1143. Longest Common Subsequence
def longestCommonSubsequence(a: str, b: str) -> int
  memo f(i, j) =
    | i == len(a) or j == len(b) -> 0
    | a[i] == b[j]               -> 1 + f(i + 1, j + 1)
    | else                       -> max(f(i + 1, j), f(i, j + 1))
  f(0, 0)
