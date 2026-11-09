# REFERENCE: d403 EPI 6.6 Reverse all the words in a sentence
class Solution
  def reverse_words(s: [str]) -> none
    def flip(lo, hi)
      while lo < hi
        s[lo], s[hi] = s[hi], s[lo]
        lo, hi = lo + 1, hi - 1

    flip(0, len(s) - 1)
    i = 0
    while i < len(s)
      j = i
      while j < len(s) and s[j] != ' '
        j += 1
      flip(i, j - 1)
      i = j + 1
