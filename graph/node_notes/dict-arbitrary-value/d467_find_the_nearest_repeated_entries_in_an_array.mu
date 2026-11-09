# REFERENCE: d467 EPI 12.5 Find the nearest repeated entries in an array
class Solution
  def find_nearest_repetition(words: [str]) -> int
    last, best = {}, inf
    for >i, w in words
      if w in last
        best = min(best, i - last[w])
      last[w] = i
    best or -1 if inf
