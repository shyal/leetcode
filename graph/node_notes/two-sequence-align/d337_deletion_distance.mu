# REFERENCE: d337 Deletion Distance
class Solution
  def deletion_distance(str1: str, str2: str) -> int
    memo f(i, j) =
      | i == len(str1)     -> len(str2) - j
      | j == len(str2)     -> len(str1) - i
      | str1[i] == str2[j] -> f(i + 1, j + 1)
      | else               -> 1 + min(f(i + 1, j), f(i, j + 1))
    f(0, 0)
