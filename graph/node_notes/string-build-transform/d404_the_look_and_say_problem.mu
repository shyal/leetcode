# REFERENCE: d404 EPI 6.7 The look-and-say problem
class Solution
  def look_and_say(n: int) -> str
    s = '1'
    for 0..<n - 1
      out, i = [], 0
      while i < len(s)
        j = i
        while j < len(s) and s[j] == s[i]
          j += 1
        out <- str(j - i) + s[i]
        i = j
      s = ''.join(out)
    s
