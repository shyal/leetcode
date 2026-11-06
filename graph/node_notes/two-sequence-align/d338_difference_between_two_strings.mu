# REFERENCE: d338 Difference Between Two Strings
class Solution
  def diff_between_two_strings(source: str, target: str) -> [str]
    memo edits(i, j) =
      | i == len(source)      -> len(target) - j
      | j == len(target)      -> len(source) - i
      | source[i] == target[j] -> edits(i + 1, j + 1)
      | else                  -> 1 + min(edits(i + 1, j), edits(i, j + 1))
    ret res = []
    i, j = 0, 0
    while i < len(source) or j < len(target)
      if i < len(source) and j < len(target) and source[i] == target[j]
        res <- source[i]
        i += 1
        j += 1
      elif j == len(target) or (i < len(source) and edits(i + 1, j) <= edits(i, j + 1))
        res <- "-" + source[i]
        i += 1
      else
        res <- "+" + target[j]
        j += 1
