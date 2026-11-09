# REFERENCE: d425 EPI 8.3 Is a string well-formed?
class Solution
  def is_well_formed(s: str) -> bool
    opener = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s
      if c not in opener
        stack <- c
      elif not stack or stack.pop() != opener[c]
        return false
    not stack
