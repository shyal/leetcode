# REFERENCE: d472 EPI 12.10 Compute all string decompositions
class Solution
  def find_all_substrings(s: str, words: [str]) -> [int]
    size, count = len(words[0]), len(words)
    want = counter(words)
    [i for i in 0..len(s) - size * count if counter(s[i + j * size:i + (j + 1) * size] for j in 0..<count) == want]
