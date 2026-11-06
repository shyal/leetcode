# REFERENCE: d334 Decode Variations
class Solution
  def decodeVariations(S: str) -> int
    n = len(S)
    one_ahead, two_ahead = 1, 1
    for i in n - 1..0 by -1
      ways = 0
      if S[i] != "0"
        ways = one_ahead
        if i + 1 < n and int(S[i:i + 2]) <= 26
          ways += two_ahead
      one_ahead, two_ahead = ways, one_ahead
    one_ahead
