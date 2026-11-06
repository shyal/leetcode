# REFERENCE: d331 Bracket Match
class Solution
  def bracket_match(text: str) -> int
    open_count = added = 0
    for c in text
      if c == '('
        open_count += 1
      elif open_count > 0
        open_count -= 1
      else
        added += 1
    added + open_count
