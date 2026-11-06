# REFERENCE: d330 Basic Regex Parser
class Solution
  def is_match(text: str, pattern: str) -> bool
    memo match(i, j)
      if j == len(pattern)
        return i == len(text)
      head = i < len(text) and pattern[j] in (".", text[i])
      if j + 1 < len(pattern) and pattern[j + 1] == "*"
        return match(i, j + 2) or (head and match(i + 1, j))
      head and match(i + 1, j + 1)
    match(0, 0)
