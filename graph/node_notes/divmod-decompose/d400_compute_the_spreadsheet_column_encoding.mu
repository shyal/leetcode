# REFERENCE: d400 EPI 6.3 Compute the spreadsheet column encoding
class Solution
  def ss_decode_col_id(col: str) -> int
    n = 0
    for c in col
      n = n * 26 + ord(c) - ord('A') + 1
    n
